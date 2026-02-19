#!/usr/bin/env python3
"""Generate extraction-summary.yaml from per-article log files.

Usage:
    python generate_summary.py <extraction-dir> <session-id> [--max-rounds N]

Example:
    python generate_summary.py search-sessions/.../extraction 20260213_genaiwbav7_d5dcc5

Reads log.yaml from each article directory and produces a batch-level
extraction-summary.yaml with aggregate statistics.
"""

import sys
from datetime import date
import yaml
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    extraction_dir = Path(sys.argv[1])
    session_id = sys.argv[2]
    max_rounds = 3

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--max-rounds" and i + 1 < len(sys.argv):
            max_rounds = int(sys.argv[i + 1])

    articles = []
    round_counts = {}
    force_count = 0
    failed_count = 0

    for article_dir in sorted(extraction_dir.iterdir()):
        if not article_dir.is_dir():
            continue

        ext_subdir = article_dir / "extraction"
        if not ext_subdir.is_dir():
            continue

        log_path = ext_subdir / "log.yaml"
        if not log_path.exists():
            continue

        with open(log_path) as f:
            log = yaml.safe_load(f) or {}

        article_id = article_dir.name
        final_status = log.get("final_status", "incomplete")
        final_round = log.get("final_round", 0)

        total_major_raised = sum(it.get("major_issues", 0) for it in log.get("iterations", []))
        total_minor_raised = sum(it.get("minor_issues", 0) for it in log.get("iterations", []))

        # Count resolved = total raised minus unresolved (last round's issues if not approved)
        last_iter = log.get("iterations", [{}])[-1] if log.get("iterations") else {}
        if final_status == "approved":
            major_resolved = total_major_raised
            minor_resolved = total_minor_raised
        else:
            major_resolved = total_major_raised - last_iter.get("major_issues", 0)
            minor_resolved = total_minor_raised - last_iter.get("minor_issues", 0)

        article_entry = {
            "article_id": article_id,
            "final_status": final_status,
            "final_round": final_round,
            "major_issues_raised": total_major_raised,
            "major_issues_resolved": major_resolved,
            "minor_issues_raised": total_minor_raised,
            "minor_issues_resolved": minor_resolved,
        }

        if final_status == "force_accepted":
            force_count += 1
            unresolved = last_iter.get("major_issues", 0)
            if unresolved > 0:
                article_entry["unresolved_major_issues"] = unresolved

        if final_status == "approved" or final_status == "force_accepted":
            round_counts[final_round] = round_counts.get(final_round, 0) + 1
        elif final_status == "incomplete":
            failed_count += 1

        articles.append(article_entry)

    total = len(articles)
    results = {}
    for r in range(1, max_rounds + 1):
        results[f"approved_round_{r}"] = round_counts.get(r, 0)
    results["force_accepted"] = force_count
    results["extraction_failed"] = failed_count
    results["unresolved_major_issues"] = sum(
        a.get("unresolved_major_issues", 0) for a in articles
    )

    summary = {
        "session_id": session_id,
        "date": date.today().isoformat(),
        "total_articles": total,
        "max_rounds": max_rounds,
        "results": results,
        "articles": articles,
    }

    out_path = extraction_dir / "extraction-summary.yaml"
    with open(out_path, "w") as f:
        yaml.dump(summary, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Summary written to {out_path}")
    print(f"\nTotal: {total} articles")
    for r in range(1, max_rounds + 1):
        count = round_counts.get(r, 0)
        if count > 0:
            print(f"  Approved round {r}: {count}")
    if force_count:
        print(f"  Force-accepted: {force_count}")
    if failed_count:
        print(f"  Failed/incomplete: {failed_count}")


if __name__ == "__main__":
    main()
