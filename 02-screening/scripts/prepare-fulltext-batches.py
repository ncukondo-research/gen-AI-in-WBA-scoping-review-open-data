#!/usr/bin/env python3
"""Prepare fulltext screening batches from fulltext-status.yaml.

Filters candidate articles (screening_status include/uncertain), resolves
fulltext.md paths via session lookup and ref-manager, copies them into batch
directories, and writes review.yaml files referencing the local copies.

Also copies fulltext_artifacts/ directories alongside fulltext.md so that
image references (e.g. ./fulltext_artifacts/image_*.png) remain valid.
Images use content-hash filenames, so merging multiple articles' artifacts
into a shared directory is safe.

Usage:
    python3 prepare-fulltext-batches.py \
        --session-id <session-id> \
        --reviewer ai:claude \
        --batch-size 5 \
        --seed 42 \
        --project-dir /abs/path
"""

import argparse
import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


def load_fulltext_status(session_dir: Path) -> list[dict]:
    """Load fulltext-status.yaml and return the articles list."""
    status_file = session_dir / "fulltext-status.yaml"
    if not status_file.exists():
        print(f"Error: {status_file} not found", file=sys.stderr)
        sys.exit(1)
    with open(status_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("articles", [])


def build_fulltext_lookup(session_dir: Path) -> dict[str, Path]:
    """Scan fulltext/*/meta.json to build DOI/PMID -> fulltext.md path lookup."""
    lookup: dict[str, Path] = {}
    fulltext_dir = session_dir / "fulltext"
    if not fulltext_dir.is_dir():
        return lookup
    for meta_path in fulltext_dir.glob("*/meta.json"):
        try:
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        ft_path = meta_path.parent / "fulltext.md"
        if not ft_path.exists():
            continue
        doi = meta.get("doi", "")
        pmid = meta.get("pmid", "")
        if doi:
            lookup[f"doi:{doi.lower()}"] = ft_path
        if pmid:
            lookup[f"pmid:{pmid}"] = ft_path
    return lookup


def batch_resolve_via_ref(ref_keys: list[str]) -> dict[str, Path | None]:
    """Batch-get fulltext.md paths from ref-manager for multiple keys.

    Returns a dict mapping each ref_key to its markdown Path (or None).
    """
    if not ref_keys:
        return {}
    try:
        result = subprocess.run(
            ["ref", "fulltext", "get"] + ref_keys + ["--markdown", "-o", "json"],
            capture_output=True, text=True,
            timeout=max(10, len(ref_keys) * 2),
        )
        if result.returncode != 0 and not result.stdout.strip():
            return {k: None for k in ref_keys}
        data = json.loads(result.stdout)
        if isinstance(data, dict):
            data = [data]
        mapping: dict[str, Path | None] = {}
        for item in data:
            key = item.get("id", "")
            md_path_str = item.get("paths", {}).get("markdown", "")
            if item.get("success") and md_path_str:
                p = Path(md_path_str)
                mapping[key] = p if p.exists() else None
            else:
                mapping[key] = None
        return mapping
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return {k: None for k in ref_keys}


# Module-level cache populated by batch_resolve_via_ref, used as fallback
_ref_path_cache: dict[str, Path | None] = {}


def resolve_via_ref(ref_key: str) -> Path | None:
    """Get fulltext.md path from ref-manager (uses cache, then single call)."""
    if ref_key in _ref_path_cache:
        return _ref_path_cache[ref_key]
    result = batch_resolve_via_ref([ref_key])
    path = result.get(ref_key)
    _ref_path_cache[ref_key] = path
    return path


def resolve_fulltext_path(
    article: dict,
    lookup: dict[str, Path],
) -> Path | None:
    """Find fulltext.md for an article using session lookup, then ref-manager."""
    doi = article.get("doi", "")
    pmid = str(article.get("pmid", ""))

    # Try session fulltext directory lookup
    if doi:
        path = lookup.get(f"doi:{doi.lower()}")
        if path:
            return path
    if pmid:
        path = lookup.get(f"pmid:{pmid}")
        if path:
            return path

    # Fallback: ref-manager via `ref fulltext get`
    ref_key = article.get("ref_key", "")
    if ref_key:
        return resolve_via_ref(ref_key)

    return None


def _copy_artifacts_from_dir(artifacts_src: Path, dest_fulltext_dir: Path) -> int:
    """Copy all files from an artifacts directory into the destination.

    Returns the number of newly copied files.
    """
    if not artifacts_src.is_dir():
        return 0
    artifacts_dest = dest_fulltext_dir / "fulltext_artifacts"
    artifacts_dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in artifacts_src.iterdir():
        if f.is_file():
            dest = artifacts_dest / f.name
            if not dest.exists():
                shutil.copy2(f, dest)
                copied += 1
    return copied


def copy_fulltext_artifacts(
    src_md_path: Path,
    dest_fulltext_dir: Path,
    ref_key: str = "",
) -> int:
    """Copy fulltext_artifacts/ alongside fulltext.md into the batch directory.

    First tries the directory containing src_md_path (session fulltext dir).
    If no artifacts are found there, falls back to the ref-manager attachment
    directory (which typically contains Docling-generated artifacts).

    Merges into dest_fulltext_dir/fulltext_artifacts/. Returns the number
    of files copied.  Hash-based filenames prevent collisions across articles.
    """
    # Try source directory first (session fulltext dir)
    copied = _copy_artifacts_from_dir(
        src_md_path.parent / "fulltext_artifacts", dest_fulltext_dir,
    )
    if copied > 0:
        return copied

    # Fallback: ref-manager attachment directory
    if not ref_key:
        return 0
    ref_md_path = resolve_via_ref(ref_key)
    if ref_md_path and ref_md_path.resolve() != src_md_path.resolve():
        copied = _copy_artifacts_from_dir(
            ref_md_path.parent / "fulltext_artifacts", dest_fulltext_dir,
        )
    return copied


def make_safe_filename(ref_key: str) -> str:
    """Convert ref_key to a safe filename component."""
    return ref_key.lower().replace("_", "-")


def reviewer_short(reviewer: str) -> str:
    """Extract short name from reviewer ID (e.g. 'ai:claude' -> 'claude')."""
    return reviewer.split(":")[-1] if ":" in reviewer else reviewer


def write_review_yaml(
    batch_dir: Path,
    session_id: str,
    reviewer: str,
    articles: list[dict],
    filenames: list[str],
) -> None:
    """Write review.yaml for a batch with fulltext.file references."""
    entries = []
    for article, fname in zip(articles, filenames):
        entry: dict = {
            "title": article["title"],
            "reviews": [{"decision": "uncertain", "comment": ""}],
        }
        if article.get("doi"):
            entry["doi"] = article["doi"]
        if article.get("pmid"):
            entry["pmid"] = str(article["pmid"])
        if article.get("authors"):
            entry["authors"] = article["authors"]
        if article.get("year"):
            entry["year"] = str(article["year"])
        if article.get("abstract"):
            entry["abstract"] = article["abstract"]
        entry["fulltext"] = {"file": fname, "format": "markdown"}
        entries.append(entry)

    data = {
        "sessionId": session_id,
        "basis": "fulltext",
        "reviewer": reviewer,
        "articles": entries,
    }

    header = (
        "# yaml-language-server: $schema=./review.schema.json\n"
        "# Screening by full text. This is the final decision stage.\n"
        '# Decide "include" or "exclude" for each item.\n'
        '# Use "uncertain" only when absolutely unavoidable, with a comment explaining why.\n'
    )
    out_path = batch_dir / "review.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )


def main():
    parser = argparse.ArgumentParser(
        description="Prepare fulltext screening batches from fulltext-status.yaml."
    )
    parser.add_argument("--session-id", required=True, help="Search session ID")
    parser.add_argument(
        "--reviewer", required=True,
        help="Reviewer ID (e.g. ai:claude)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=5,
        help="Articles per batch (default: 5)",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducible ordering (default: 42)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max articles to include (default: all eligible)",
    )
    parser.add_argument(
        "--project-dir", required=True,
        help="Absolute path to project root",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    session_dir = project_dir / "search-sessions" / args.session_id
    for_review_dir = session_dir / "for-review"
    short = reviewer_short(args.reviewer)

    if not session_dir.is_dir():
        print(f"Error: session directory not found: {session_dir}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Load fulltext-status.yaml
    articles = load_fulltext_status(session_dir)

    # Step 2: Filter candidates (include/uncertain)
    candidates = [
        a for a in articles
        if a.get("screening_status") in ("include", "uncertain")
    ]
    print(f"Candidates (include/uncertain): {len(candidates)}")

    # Step 3: Resolve fulltext.md paths
    lookup = build_fulltext_lookup(session_dir)

    # Pre-populate ref path cache with a single batch call for all ref_keys
    all_ref_keys = list({a["ref_key"] for a in candidates if a.get("ref_key")})
    if all_ref_keys:
        _ref_path_cache.update(batch_resolve_via_ref(all_ref_keys))

    resolved = []
    not_retrieved = []
    for article in candidates:
        path = resolve_fulltext_path(article, lookup)
        if path:
            resolved.append((article, path))
        else:
            not_retrieved.append(article)

    print(f"Fulltext resolved: {len(resolved)}")
    print(f"Fulltext not available: {len(not_retrieved)}")

    # Step 4: Shuffle for reproducibility
    rng = random.Random(args.seed)
    rng.shuffle(resolved)

    if args.limit is not None:
        resolved = resolved[: args.limit]

    if not resolved:
        print("No articles with available fulltext to screen.")
        # Still write not-retrieved list
        if not_retrieved:
            _write_not_retrieved(for_review_dir, not_retrieved)
        sys.exit(0)

    # Step 5: Split into batches
    num_batches = math.ceil(len(resolved) / args.batch_size)

    print(f"\nBatch plan: {len(resolved)} articles, batch_size={args.batch_size}, "
          f"{num_batches} batches for {args.reviewer}")

    # Step 6: Create batch directories
    for_review_dir.mkdir(parents=True, exist_ok=True)

    for i in range(num_batches):
        start = i * args.batch_size
        end = min(start + args.batch_size, len(resolved))
        batch_articles = resolved[start:end]

        batch_nn = f"{i + 1:02d}"
        batch_name = f"fulltext-{short}-batch-{batch_nn}"
        batch_dir = for_review_dir / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        fulltext_subdir = batch_dir / "fulltext"
        fulltext_subdir.mkdir(parents=True, exist_ok=True)

        filenames = []
        batch_artifact_count = 0
        for article, src_path in batch_articles:
            ref_key = article.get("ref_key", "unknown")
            safe_name = make_safe_filename(ref_key)
            dest_name = f"{safe_name}-fulltext.md"
            dest_path = fulltext_subdir / dest_name
            shutil.copy2(src_path, dest_path)
            filenames.append(f"fulltext/{dest_name}")
            batch_artifact_count += copy_fulltext_artifacts(
                src_path, fulltext_subdir,
                ref_key=article.get("ref_key", ""),
            )

        articles_only = [a for a, _ in batch_articles]
        write_review_yaml(batch_dir, args.session_id, args.reviewer, articles_only, filenames)

        img_note = f", {batch_artifact_count} images" if batch_artifact_count else ""
        print(f"  Created {batch_name}: {len(batch_articles)} articles{img_note}")

    # Step 7: Write not-retrieved list
    if not_retrieved:
        _write_not_retrieved(for_review_dir, not_retrieved)

    # Summary
    print(f"\nSummary:")
    print(f"  Candidates (include/uncertain): {len(candidates)}")
    print(f"  Fulltext resolved: {len(resolved)}")
    print(f"  Fulltext not available: {len(not_retrieved)}")
    print(f"  Batches created: {num_batches}")


def _write_not_retrieved(for_review_dir: Path, articles: list[dict]) -> None:
    """Write list of articles without fulltext markdown for PRISMA reporting."""
    entries = []
    for a in articles:
        entry = {
            "ref_key": a.get("ref_key", ""),
            "title": a.get("title", ""),
            "doi": a.get("doi", ""),
            "pmid": str(a.get("pmid", "")),
            "reason": "fulltext markdown not available",
        }
        entries.append(entry)

    out_path = for_review_dir / "fulltext-not-retrieved.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"articles": entries},
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
    print(f"  Not-retrieved list: {out_path} ({len(entries)} articles)")


if __name__ == "__main__":
    main()
