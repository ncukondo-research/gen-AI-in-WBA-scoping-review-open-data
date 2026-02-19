#!/usr/bin/env python3
"""Evaluate review verdicts and finalize approved extractions.

Usage:
    python finalize.py <extraction-dir> <round-number> [--max-rounds N]

Example:
    python finalize.py search-sessions/.../extraction 2 --max-rounds 3

For each article directory in <extraction-dir>:
- Reads review-v<round>.yaml
- If overall_verdict == "approve": copies extraction-v<round>.yaml to extraction-final.yaml
- If overall_verdict == "revise" and round == max_rounds: force-accepts with flag
- If overall_verdict == "revise" and round < max_rounds: reports as needing revision
- Updates log.yaml for each article

Exit code: 0 if all finalized, 2 if some need revision.
"""

import shutil
import sys
import yaml
from pathlib import Path


def update_log(article_dir: Path, article_id: str, round_num: int,
               review: dict, final_status: str | None = None):
    log_path = article_dir / "log.yaml"

    if log_path.exists():
        with open(log_path) as f:
            log = yaml.safe_load(f) or {}
    else:
        log = {"article_id": article_id, "iterations": []}

    # Add this round
    major = sum(1 for i in review.get("issues", []) if i.get("severity") == "major")
    minor = sum(1 for i in review.get("issues", []) if i.get("severity") == "minor")

    iteration = {
        "round": round_num,
        "extraction_file": f"extraction-v{round_num}.yaml",
        "review_file": f"review-v{round_num}.yaml",
        "verdict": review.get("overall_verdict", "unknown"),
        "major_issues": major,
        "minor_issues": minor,
    }

    # Replace if round already exists, otherwise append
    existing = [i for i in log.get("iterations", []) if i.get("round") != round_num]
    existing.append(iteration)
    existing.sort(key=lambda x: x.get("round", 0))
    log["iterations"] = existing

    if final_status:
        log["final_status"] = final_status
        log["final_round"] = round_num
        log["final_file"] = "extraction-final.yaml"

    with open(log_path, "w") as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    extraction_dir = Path(sys.argv[1])
    round_num = int(sys.argv[2])
    max_rounds = 3

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--max-rounds" and i + 1 < len(sys.argv):
            max_rounds = int(sys.argv[i + 1])

    approved = []
    needs_revision = []
    force_accepted = []
    skipped = []

    for article_dir in sorted(extraction_dir.iterdir()):
        if not article_dir.is_dir():
            continue

        ext_subdir = article_dir / "extraction"
        if not ext_subdir.is_dir():
            continue

        article_id = article_dir.name
        review_path = ext_subdir / f"review-v{round_num}.yaml"
        extraction_path = ext_subdir / f"extraction-v{round_num}.yaml"
        final_path = ext_subdir / "extraction-final.yaml"

        # Skip if already finalized
        if final_path.exists():
            skipped.append(article_id)
            continue

        if not review_path.exists():
            skipped.append(article_id)
            continue

        if not extraction_path.exists():
            print(f"WARN  {article_id}: review exists but extraction-v{round_num}.yaml missing")
            skipped.append(article_id)
            continue

        with open(review_path) as f:
            review = yaml.safe_load(f) or {}

        verdict = review.get("overall_verdict", "unknown")

        if verdict == "approve":
            shutil.copy2(extraction_path, final_path)
            update_log(ext_subdir, article_id, round_num, review, final_status="approved")
            approved.append(article_id)
            print(f"OK    {article_id}: approved at round {round_num}")

        elif verdict == "revise" and round_num >= max_rounds:
            # Force accept
            with open(extraction_path) as f:
                content = f.read()
            unresolved = [i for i in review.get("issues", []) if i.get("severity") == "major"]
            header = (
                f"# force_accepted: true\n"
                f"# unresolved_major_issues: {len(unresolved)}\n"
            )
            with open(final_path, "w") as f:
                f.write(header + content)
            update_log(ext_subdir, article_id, round_num, review, final_status="force_accepted")
            force_accepted.append(article_id)
            print(f"FORCE {article_id}: force-accepted at round {round_num} ({len(unresolved)} unresolved)")

        elif verdict == "revise":
            update_log(ext_subdir, article_id, round_num, review)
            needs_revision.append(article_id)
            major = sum(1 for i in review.get("issues", []) if i.get("severity") == "major")
            print(f"REV   {article_id}: needs revision ({major} major issues)")

        else:
            skipped.append(article_id)
            print(f"SKIP  {article_id}: unknown verdict '{verdict}'")

    print(f"\n--- Round {round_num} Summary ---")
    print(f"Approved: {len(approved)}")
    print(f"Needs revision: {len(needs_revision)}")
    print(f"Force-accepted: {len(force_accepted)}")
    print(f"Skipped/already final: {len(skipped)}")

    if needs_revision:
        print(f"\nArticles needing revision: {', '.join(needs_revision)}")
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
