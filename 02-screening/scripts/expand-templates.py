#!/usr/bin/env python3
"""Expand screening templates with session-specific values.

Reads CLAUDE.md and prompt.md from the templates/ directory, substitutes
placeholders, and writes the expanded files to the reviewer's for-review
directory.  The context file is output as both CLAUDE.md (for Claude CLI)
and AGENTS.md (for Codex CLI) so that each tool reads the same content
via its own convention.

Usage:
    python3 expand-templates.py \
        --session-id <session-id> \
        --stage <title|abstract|fulltext> \
        --reviewer-name <screening-name> \
        --reviewer-id <ai:claude|ai:codex> \
        --article-count <N> \
        --project-dir <abs-path> \
        [--batch-id <batch-NN>]
"""

import argparse
import sys
from pathlib import Path

STAGE_RULES = {
    "title": (
        "Be conservative. At the title stage, only two decisions are permitted: "
        "`exclude` or `uncertain`. Do NOT use `include`.\n"
        "Mark as `uncertain` when the title is ambiguous "
        "or does not provide enough information. Only mark as `exclude` when "
        "the title clearly and unambiguously violates an exclusion criterion. "
        "When in doubt, mark as `uncertain` to retain the article for "
        "abstract screening.\n\n"
        "**Calibration note**: Titles mentioning AI/LLM in medical education "
        "are often ambiguous. Prefer `uncertain` over `exclude` unless the "
        "title explicitly rules out generative AI or WBA."
    ),
    "abstract": (
        "Three decisions are permitted: `include`, `exclude`, or `uncertain`.\n"
        "Make a definitive decision for most articles. Use `uncertain` only "
        "when the abstract is genuinely insufficient to determine eligibility. "
        "You should be able to decide most articles at this stage.\n\n"
        "**No-abstract rule**: If an article has no abstract (the `abstract` "
        "field is empty, missing, or blank), mark it as `uncertain` with the "
        'comment "No abstract available; forwarded to full-text screening." '
        "Do NOT attempt to judge eligibility without an abstract.\n\n"
        "**Calibration note**: Articles studying AI-generated feedback on "
        "clinical performance may qualify even if they do not explicitly "
        "mention 'workplace-based assessment'."
    ),
    "fulltext": (
        "Only two decisions are permitted: `include` or `exclude`. "
        "No `uncertain` decisions are allowed at the full-text stage.\n"
        "Decide ALL articles definitively. Every article must be marked as "
        "either `include` or `exclude` with clear justification."
    ),
}

CALIBRATION_EXAMPLES = {
    "title": """### Calibration Examples
- "ML Algorithms for Predicting Surgical Outcomes" -> exclude (criterion 1: conventional ML, not generative AI)
- "ChatGPT on USMLE Questions" -> uncertain (abstract may reveal WBA elements)
- "AI in Medical Education: Trends and Directions" -> uncertain (too broad to judge from title)
- "VR Simulation for Laparoscopic Training" -> exclude (criterion 1: VR, not generative AI)
- "Enhancing reflective practice with ChatGPT" -> uncertain (reflection is core to WBA)
- "LLM improves clinicians' diagnostic performance" -> uncertain (may involve clinical assessment)""",
    "abstract": """### Calibration Examples
- Abstract describes GPT-4 generating feedback on clinical notes written by residents -> uncertain or include (feedback on clinical documentation in workplace)
- Abstract describes ML model predicting readmission risk -> exclude (criterion 1: conventional ML)
- Abstract describes LLM grading OSCE stations only -> exclude (criterion 3: simulated environment only)
- Abstract describes ChatGPT analyzing Mini-CEX narratives -> include (generative AI + WBA)
- Abstract describes LLM for medical education curriculum design -> exclude (criterion 2: not about assessment/feedback)""",
    "fulltext": """### Calibration Examples
- Study uses GPT-4 to generate feedback on workplace clinical encounters -> include
- Study tests LLM on exam questions only, no workplace component -> exclude (criterion 3/4)
- Study describes an LLM tool for clinical documentation but no assessment/feedback data -> exclude (criterion 5)""",
}

FULLTEXT_INSTRUCTIONS = {
    "title": "",
    "abstract": "",
    "fulltext": (
        "## Fulltext Reading Instructions\n\n"
        "For each article, read the fulltext before making your decision. "
        "The `fulltext.file` field in review.yaml contains a relative path "
        "to the article's fulltext markdown inside the `fulltext/` "
        "subdirectory of this batch directory. Read the file using the Read tool.\n\n"
        "For example, if `fulltext.file` is `fulltext/kondo-2025-fulltext.md`, "
        "read the file at `<this-batch-directory>/fulltext/kondo-2025-fulltext.md`.\n\n"
        "Focus on: (1) whether generative AI is used, (2) whether the "
        "setting is workplace-based, (3) whether assessment/feedback data "
        "is presented.\n\n"
        "**Important**: Read the FULL text of each article. Do not skip "
        "sections. Pay attention to Methods, Results, and Discussion."
    ),
}

DONE_MARKERS = {
    "ai:claude": ".claude-done",
    "ai:codex": ".codex-done",
}


def substitute(text: str, replacements: dict[str, str]) -> str:
    """Replace all {{KEY}} placeholders in text."""
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Expand screening templates with session-specific values."
    )
    parser.add_argument("--session-id", required=True, help="Search session ID")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["title", "abstract", "fulltext"],
        help="Screening stage",
    )
    parser.add_argument(
        "--reviewer-name", required=True, help="Reviewer directory name"
    )
    parser.add_argument(
        "--reviewer-id", required=True, help="Reviewer ID (e.g. ai:claude)"
    )
    parser.add_argument(
        "--article-count", required=True, type=int, help="Number of articles"
    )
    parser.add_argument(
        "--project-dir", required=True, help="Absolute path to project root"
    )
    parser.add_argument(
        "--batch-id", default="", help="Batch identifier (e.g. batch-03)"
    )
    args = parser.parse_args()

    # Resolve paths (scripts/ is one level below the skill root)
    skill_dir = Path(__file__).resolve().parent.parent
    templates_dir = skill_dir / "templates"
    review_dir = (
        Path(args.project_dir)
        / "search-sessions"
        / args.session_id
        / "for-review"
        / args.reviewer_name
    )
    review_file_path = f"search-sessions/{args.session_id}/for-review/{args.reviewer_name}/review.yaml"

    if not review_dir.is_dir():
        print(f"Error: review directory does not exist: {review_dir}", file=sys.stderr)
        sys.exit(1)

    # Determine done marker from reviewer ID
    done_marker = DONE_MARKERS.get(args.reviewer_id, ".done")

    # Build replacement map
    replacements = {
        "SESSION_ID": args.session_id,
        "STAGE": args.stage,
        "REVIEWER_ID": args.reviewer_id,
        "ARTICLE_COUNT": str(args.article_count),
        "STAGE_RULES": STAGE_RULES[args.stage],
        "REVIEW_FILE_PATH": review_file_path,
        "PROJECT_DIR": args.project_dir,
        "DONE_MARKER": done_marker,
        "BATCH_ID": args.batch_id,
        "CALIBRATION_EXAMPLES": CALIBRATION_EXAMPLES[args.stage],
        "FULLTEXT_INSTRUCTIONS": FULLTEXT_INSTRUCTIONS[args.stage],
    }

    # Expand CLAUDE.md template -> both CLAUDE.md and AGENTS.md
    claude_src = templates_dir / "CLAUDE.md"
    if not claude_src.exists():
        print(f"Error: template not found: {claude_src}", file=sys.stderr)
        sys.exit(1)

    content = claude_src.read_text(encoding="utf-8")
    expanded = substitute(content, replacements)

    for filename in ["CLAUDE.md", "AGENTS.md"]:
        dst = review_dir / filename
        dst.write_text(expanded, encoding="utf-8")
        print(f"  CLAUDE.md -> {dst}")

    # Expand prompt.md
    prompt_src = templates_dir / "prompt.md"
    if not prompt_src.exists():
        print(f"Error: template not found: {prompt_src}", file=sys.stderr)
        sys.exit(1)

    content = prompt_src.read_text(encoding="utf-8")
    expanded = substitute(content, replacements)
    dst = review_dir / "prompt.md"
    dst.write_text(expanded, encoding="utf-8")
    print(f"  prompt.md -> {dst}")

    print(f"\nTemplate expansion complete for {args.reviewer_name}")


if __name__ == "__main__":
    main()
