#!/usr/bin/env python3
"""Merge reviewer messages from team inbox into per-article review-vN.yaml files.

Usage:
    python merge_reviews.py <inbox-json> <round-number> <output-dir>

Example:
    python merge_reviews.py \
        ~/.claude/teams/extraction-review-xyz-r1/inboxes/team-lead.json \
        1 \
        search-sessions/.../extraction

Parses structured YAML review blocks from reviewer messages, merges
per-article reviews from all reviewers into a single review-vN.yaml,
and writes to each article's extraction directory.
"""

import json
import re
import sys
import yaml
from pathlib import Path


def parse_reviews_from_message(text: str) -> list[dict]:
    """Extract YAML review blocks from a reviewer message."""
    reviews = []

    # Try delimited blocks: --- BEGIN REVIEW: <id> --- ... --- END REVIEW: <id> ---
    pattern = r'--- BEGIN REVIEW:?\s*(\S+)\s*---\s*\n(.*?)\n\s*--- END REVIEW'
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        for article_id, yaml_block in matches:
            try:
                data = yaml.safe_load(yaml_block)
                if isinstance(data, dict):
                    if "article_id" not in data:
                        data["article_id"] = article_id
                    reviews.append(data)
            except yaml.YAMLError:
                pass
        return reviews

    # Try single block delimited by --- BEGIN REVIEW --- / --- END REVIEW ---
    pattern2 = r'--- BEGIN REVIEW ---\s*\n(.*?)\n\s*--- END REVIEW ---'
    matches2 = re.findall(pattern2, text, re.DOTALL)
    for yaml_block in matches2:
        try:
            data = yaml.safe_load(yaml_block)
            if isinstance(data, dict):
                reviews.append(data)
        except yaml.YAMLError:
            pass

    if reviews:
        return reviews

    # Try code-fenced YAML blocks
    pattern3 = r'```(?:yaml)?\s*\n(.*?)\n```'
    matches3 = re.findall(pattern3, text, re.DOTALL)
    for yaml_block in matches3:
        try:
            data = yaml.safe_load(yaml_block)
            if isinstance(data, dict) and "verdict" in data:
                reviews.append(data)
        except yaml.YAMLError:
            pass

    if reviews:
        return reviews

    # Try bare YAML (whole message)
    try:
        data = yaml.safe_load(text)
        if isinstance(data, dict) and "verdict" in data:
            reviews.append(data)
    except yaml.YAMLError:
        pass

    return reviews


def merge_article_reviews(article_reviews: list[dict], round_num: int, article_id: str) -> dict:
    """Merge reviews from multiple reviewers for a single article."""
    merged = {
        "article_id": article_id,
        "round": round_num,
        "reviewers": {},
        "overall_verdict": "approve",
        "issues": [],
        "commendations": [],
        "notes": [],
    }

    for review in article_reviews:
        reviewer = review.get("reviewer", "unknown")
        verdict = review.get("verdict", "approve")
        confidence = review.get("confidence", "medium")

        merged["reviewers"][reviewer] = {
            "verdict": verdict,
            "confidence": confidence,
        }

        if verdict == "revise":
            merged["overall_verdict"] = "revise"

        for issue in review.get("issues", []):
            issue_copy = dict(issue)
            if "raised_by" not in issue_copy:
                issue_copy["raised_by"] = reviewer
            merged["issues"].append(issue_copy)

        commendations = review.get("commendations", [])
        if isinstance(commendations, list):
            for c in commendations:
                if isinstance(c, str):
                    merged["commendations"].append({"reviewer": reviewer, "text": c})
                elif isinstance(c, dict):
                    merged["commendations"].append(c)

        notes_val = review.get("notes", "")
        if isinstance(notes_val, str) and notes_val:
            merged["notes"].append({"reviewer": reviewer, "text": notes_val})
        elif isinstance(notes_val, list):
            for n in notes_val:
                if isinstance(n, str):
                    merged["notes"].append({"reviewer": reviewer, "text": n})
                elif isinstance(n, dict):
                    merged["notes"].append(n)

    return merged


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)

    inbox_path = Path(sys.argv[1])
    round_num = int(sys.argv[2])
    output_dir = Path(sys.argv[3])

    if not inbox_path.exists():
        print(f"ERROR: Inbox not found: {inbox_path}")
        sys.exit(1)

    with open(inbox_path) as f:
        messages = json.load(f)

    # Collect all reviews grouped by article_id
    by_article: dict[str, list[dict]] = {}

    for msg in messages:
        text = msg.get("text", "")
        # Skip idle notifications and structured JSON messages
        if text.startswith("{") and '"type"' in text:
            continue

        reviews = parse_reviews_from_message(text)
        for review in reviews:
            aid = review.get("article_id", "unknown")
            by_article.setdefault(aid, []).append(review)

    if not by_article:
        print("WARNING: No review blocks found in inbox messages")
        sys.exit(1)

    # Merge and write
    for article_id, reviews in sorted(by_article.items()):
        merged = merge_article_reviews(reviews, round_num, article_id)
        out_path = output_dir / article_id / "extraction" / f"review-v{round_num}.yaml"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w") as f:
            yaml.dump(merged, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        n_reviewers = len(merged["reviewers"])
        n_issues = len(merged["issues"])
        print(f"WROTE {out_path} ({n_reviewers} reviewers, {n_issues} issues, verdict: {merged['overall_verdict']})")

    print(f"\nMerged reviews for {len(by_article)} articles (round {round_num})")


if __name__ == "__main__":
    main()
