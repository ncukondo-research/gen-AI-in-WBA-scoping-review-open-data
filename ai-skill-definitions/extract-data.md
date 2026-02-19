---
name: extract-data
description: Data extraction from included studies using Codex CLI, with iterative multi-agent review and revision. Extracts structured data per the extraction codebook, validates via 3 reviewers producing structured YAML feedback, and loops Codex revisions until all reviewers approve or max rounds reached.
argument-hint: [data-dir] [--pilot] [--limit N] [--review-only] [--extract-only] [--max-rounds N] [--round N]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Task, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage, TaskOutput
---

# Data Extraction with Iterative Review-Revision Loop

Input: $ARGUMENTS

## Purpose

Orchestrates data extraction from included studies with an iterative quality loop:

1. **Codex CLI extraction**: Runs `codex exec` on each study's fulltext.md to produce `extraction-v1.yaml`.
2. **Structured Agent Team review**: 3 reviewers produce structured YAML feedback with actionable revision instructions.
3. **Codex revision**: Codex revises extraction based on structured issues.
4. **Repeat** until all reviewers approve or max rounds reached.
5. **Report**: Saves `extraction-final.yaml` and iteration statistics.

## Directory Structure

```
data-extraction/                      # Base directory (configurable)
  extraction-codebook.md              # Extraction codebook
  articles-index.yaml                 # Index of included articles
  extraction-summary.yaml             # Batch-level statistics (output)
  <ref-key>/                          # Per-article directory (ref library key)
    bibliography.json                 # CSL-JSON bibliographic data (input)
    fulltext.md                       # Full text (input)
    fulltext_artifacts/               # Images referenced by fulltext.md (input)
    extraction/                       # Extraction output subdirectory
      extraction-v1.yaml              # Initial Codex extraction
      review-v1.yaml                  # Merged structured review of v1
      extraction-v2.yaml              # Codex revision based on review-v1
      review-v2.yaml                  # Review of v2 (if needed)
      extraction-v3.yaml              # Further revision (if needed)
      review-v3.yaml                  # Final review (if needed)
      extraction-final.yaml           # Copy of approved version
      log.yaml                        # Iteration history
```

## Workflow

### Step 1: Parse arguments

Extract from `$ARGUMENTS`:
- **Data directory** (optional, default: `data-extraction`): Path to the base directory containing per-article subdirectories with fulltext.md and bibliography.json
- **Options**:
  - `--pilot`: Extract only 3 articles (for testing codebook and prompts)
  - `--limit N`: Number of articles to extract (default: all included with fulltext)
  - `--review-only`: Skip initial extraction, review existing extraction files only
  - `--extract-only`: Run extraction only, skip Agent Team review loop
  - `--max-rounds N`: Maximum review-revision rounds (default: 3)
  - `--round N`: Resume from a specific round (requires existing extraction-vN.yaml files)

Derive paths:
```
BASEDIR="data-extraction"  (or value from first positional argument)
CODEBOOK="$BASEDIR/extraction-codebook.md"
MAX_ROUNDS=3  (or value from --max-rounds)
```

### Step 2: Validate environment

```bash
# Check codex is available
codex --version

# Check codebook exists
test -f "$CODEBOOK" && echo "Codebook found" || echo "ERROR: codebook not found"

# Check base directory exists and has article subdirectories
test -d "$BASEDIR" && echo "Base directory found" || echo "ERROR: base directory not found"
```

If codebook is missing, abort with message to create one first.

### Step 3: Identify target articles

Find article directories containing fulltext.md:

```bash
# List article directories with fulltext
ls "$BASEDIR"/*/fulltext.md
```

Each subdirectory of `$BASEDIR` that contains `fulltext.md` is treated as an article directory. The directory name is the ref library key (e.g., `Gin2024-ss`, `kwan-2025`).

Build the article list as an array of objects:
```
article_id: directory name = ref_key (e.g., "Gin2024-ss")
fulltext_path: absolute path to $BASEDIR/<ref_key>/fulltext.md
extraction_dir: absolute path to $BASEDIR/<ref_key>/extraction/
```

Apply `--limit` or `--pilot` (limit=3) if specified.

If `--pilot` is set, select the first 3 articles alphabetically.

Create per-article extraction output directories:
```bash
for article_id in <article_list>; do
  mkdir -p "$BASEDIR/$article_id/extraction"
done
```

Report the plan:
```
Extraction plan: <N> articles, max <MAX_ROUNDS> review-revision rounds
  Codebook: <codebook_path>
  Base directory: <basedir>
  Articles:
    1. <article_id>
    2. ...
```

### Step 4: Run Codex initial extraction (skip if `--review-only` or `--round N`)

For each article, launch `codex exec` as a background Bash command:

```bash
codex exec \
  --sandbox read-only \
  -o "$BASEDIR/<article_id>/extraction/extraction-v1.yaml" \
  "You are a data extractor for a scoping review on generative AI in workplace-based assessment. Your task is to extract structured data from a research article following the codebook.

INSTRUCTIONS:
1. Read the codebook at: <absolute_codebook_path>
2. Read the full text at: <absolute_fulltext_path>
3. Extract ALL items defined in the codebook (Categories A through F).
4. Output ONLY the YAML extraction form as defined in the codebook. No preamble, no explanation, no markdown fences.
5. For items not found in the article, code as 'Not reported'.
6. For ambiguous items, code as 'Unclear: [explanation]'.
7. For D-category sub-items where evidence is absent, use the exact phrase 'No evidence reported'.
8. Wrap multi-line text values in YAML using | (literal block scalar).
9. Verify every extracted data point can be traced to a specific passage in the full text.
10. Set the extractor field to exactly: 'ai:codex-gpt-5'
11. Pay special attention to the Coding Decision Rules in the codebook (especially rules #6 on D3 threshold including D3f bias/fairness, rule #11 on D3f vs D5 bias distinction, and D_summary consistency).

Output the complete YAML extraction now."
```

**Parallelism**: Launch up to 5 Codex processes in parallel using `run_in_background: true`. Monitor completion using TaskOutput.

**Timeout**: 10 minutes per article (600000ms).

After all complete, verify each output file:

```bash
python3 .claude/skills/extract-data/scripts/validate_yaml.py "$BASEDIR"/*/extraction/extraction-v1.yaml
```

Report any failures.

If `--extract-only`, skip to Step 6.

### Step 5: Iterative Review-Revision Loop

```
For round N = 1 to MAX_ROUNDS:
  5a. Identify pending articles
  5b. Create review team
  5c. Spawn 3 review agents (parallel) → structured YAML output
  5d. Collect & merge reviews → review-vN.yaml per article
  5e. Evaluate verdicts → approve or queue for revision
  5f. Shutdown team
  5g. Codex revision for non-approved articles → extraction-v(N+1).yaml
  5h. If all approved, break
```

#### Step 5a: Identify pending articles and choose review mode

Find articles that have `extraction/extraction-vN.yaml` but do NOT have `extraction/extraction-final.yaml`.

If none are pending, all articles are approved. Break out of the loop.

**Lightweight review shortcut (Round 2+)**: If ALL of the following conditions are met, skip the full 3-agent team review and instead have the team lead directly verify the fix and approve:
- Only 1-2 articles remain pending
- The previous review had only 1 major issue per article
- The issue is a mechanical text fix (e.g., D_summary wording, null-value phrasing) rather than a judgment call
- The validate_yaml.py script passes with zero errors on the revised file

In this case, run validation, visually confirm the fix, write a review-vN.yaml manually noting "lightweight review by team lead", and proceed to finalize.

#### Step 5b: Create review team

```
TeamCreate: extraction-review-r<N>
```

Create 3 tasks on the team task list:

**Task 1: Source Fidelity Review**
- Verify all extracted statistics, quotes, and claims against the original fulltexts
- Check that "Not reported" items are truly absent
- Identify any hallucinated/fabricated data points
- Flag important information present in fulltext but missing from extraction

**Task 2: Downing Framework Mapping Review**
- Assess whether validity evidence (D1-D5) is correctly classified
- Check "Evidence present: Yes/No" determinations for consistency
- Identify findings placed under wrong validity source
- Apply codebook decision rule #5 (empirical data threshold) consistently
- Pay attention to: false-positive-as-hallucination coding (D2c), D3 threshold for qualitative mentions, D3f bias/fairness placement (statistical bias = D3f, not D5), D4 comparator quality

**Task 3: Consistency and Completeness Review**
- Check YAML structure consistency across all extraction files
- Verify null-value phrasing standardization ("Not reported" vs "No evidence reported" vs "No")
- Confirm all codebook items and sub-items are present
- Assess coding category consistency (B4, B7, etc.)

#### Step 5c: Spawn 3 review agents

Launch all 3 agents in a SINGLE message (parallel):

Each agent receives:
- Agent name: `fidelity-reviewer`, `framework-reviewer`, `consistency-reviewer`
- `subagent_type`: `"general-purpose"`
- `run_in_background`: `true`
- `team_name`: `"extraction-review-r<N>"`

Each agent's prompt MUST include:
1. Their role and task assignment
2. Paths to ALL pending extraction YAML files (`extraction/extraction-vN.yaml` in each article dir)
3. Paths to ALL corresponding fulltext.md files
4. Path to the codebook
5. If round N > 1: path to previous `extraction/review-v(N-1).yaml` for each article, with instruction to verify whether prior issues were addressed
6. **Output format instruction** (critical): The agent must output a structured YAML review for EACH article, using the format below

**Structured Review Output Format (per reviewer per article)**:

Instruct each reviewer to send their results as a message containing one YAML block per article, delimited by `--- BEGIN REVIEW: <article_id> ---` and `--- END REVIEW: <article_id> ---` markers. Each YAML block must follow this schema:

```yaml
article_id: "<article_id>"
reviewer: "fidelity-reviewer"  # or framework-reviewer, consistency-reviewer
round: N
verdict: "approve"  # or "revise"
confidence: "high"  # or "medium" or "low"
issues:
  - item: "D4b"                        # Codebook item code
    severity: "major"                  # "major" (must fix) or "minor" (optional)
    type: "correct_value"              # One of: reclassify, correct_value, add_missing, rephrase, remove
    current_value: "..."               # What the extraction currently says
    recommended_value: "..."           # What it should say
    rationale: "..."                   # Why this change is needed
    source_passage: "fulltext line N"  # Where in fulltext the evidence is
commendations:
  - "Accurate extraction of sample sizes and statistics"
notes: "Any additional observations"
```

**Verdict rules for reviewers**:
- Set `verdict: "approve"` only if there are ZERO major issues
- Set `verdict: "revise"` if there is at least one major issue
- Minor issues alone do NOT block approval

#### Step 5d: Collect and merge reviews

Wait for all 3 agents to complete by monitoring task list and incoming messages. Timeout: 15 minutes.

Once all reviews are received, use the merge script to parse reviewer messages and produce per-article `review-vN.yaml` files:

```bash
python3 .claude/skills/extract-data/scripts/merge_reviews.py \
  ~/.claude/teams/extraction-review-r<N>/inboxes/team-lead.json \
  <N> \
  "$BASEDIR"
```

This automatically:
- Parses YAML review blocks from between `--- BEGIN REVIEW ---` / `--- END REVIEW ---` delimiters
- Groups reviews by article_id
- Merges 3 reviewer outputs into a single `review-vN.yaml` per article with `raised_by` attribution
- Sets `overall_verdict: "approve"` only if ALL 3 reviewers approve; `"revise"` if ANY says revise

If a reviewer's output cannot be parsed, the script will skip it. Check the script output for any missing reviewers and save raw output manually as `review-vN-<reviewer>-raw.txt` if needed.

#### Step 5e: Evaluate verdicts and finalize

Use the finalize script to evaluate verdicts, copy approved extractions to `extraction-final.yaml`, and update `log.yaml`:

```bash
python3 .claude/skills/extract-data/scripts/finalize.py "$BASEDIR" <N> --max-rounds $MAX_ROUNDS
```

This automatically handles:
- **All 3 reviewers approve**: copies `extraction-vN.yaml` to `extraction-final.yaml`, updates `log.yaml`
- **Any "revise" AND N < MAX_ROUNDS**: reports article as needing revision (exit code 2)
- **Any "revise" AND N = MAX_ROUNDS**: force-accepts with `force_accepted: true` header, updates `log.yaml`

Also validate all newly finalized extractions:

```bash
python3 .claude/skills/extract-data/scripts/validate_yaml.py "$BASEDIR"/*/extraction/extraction-final.yaml
```

#### Step 5f: Shutdown team

Send shutdown requests to all 3 agents, then delete the team.

#### Step 5g: Codex revision for non-approved articles

For each article queued for revision, launch `codex exec`:

```bash
codex exec \
  --sandbox read-only \
  -o "$BASEDIR/<article_id>/extraction/extraction-v<N+1>.yaml" \
  "You are revising a data extraction for a scoping review on generative AI in workplace-based assessment. Reviewers have identified issues that need to be corrected.

INSTRUCTIONS:
1. Read the codebook at: <absolute_codebook_path>
2. Read the full text at: <absolute_fulltext_path>
3. Read the current extraction at: <absolute_path_to_extraction-vN.yaml>
4. Read the structured review at: <absolute_path_to_review-vN.yaml>

REVISION RULES:
- Apply ALL major issues (mandatory). Each major issue has: item code, type, current_value, recommended_value, rationale, and source_passage.
- Apply minor issues UNLESS the fulltext contradicts the recommendation. If you disagree with a minor issue, explain your reasoning in F3b (extractor_flags).
- Do NOT change any items that have no flagged issues. Preserve them exactly.
- For every revision you make, verify the new value against the specific passage cited in source_passage.
- CRITICAL: If any D-category evidence_present field (D1a-D5a) was changed, you MUST also update D_summary to be consistent. A D_summary that lists a validity source as 'Absent' while the corresponding evidence_present field reads 'Yes' is an error. Note that D3a should be 'Yes' if any sub-item D3b-D3f (including D3f bias/fairness) has empirical evidence.
- After applying revisions, output the COMPLETE revised YAML extraction (all categories A through F). No preamble, no explanation, no markdown fences.
- Add to F3b a note listing which issues you addressed and any you disagreed with.

Output the complete revised YAML extraction now."
```

**Parallelism**: Launch up to 5 Codex revision processes in parallel using `run_in_background: true`.

**Timeout**: 10 minutes per article (600000ms).

After all complete, validate each output:

```bash
python3 .claude/skills/extract-data/scripts/validate_yaml.py "$BASEDIR"/*/extraction/extraction-v<N+1>.yaml
```

If a file is invalid YAML, keep previous version (`extraction-vN.yaml`), flag in log.yaml as `revision_failed: true`.

#### Step 5h: Check loop termination

If all articles now have `extraction/extraction-final.yaml`, break out of the loop.

Otherwise, increment N and return to Step 5a.

### Step 6: Generate summary report

#### Step 6a: Write extraction-summary.yaml

Generate the summary from per-article log files:

```bash
python3 .claude/skills/extract-data/scripts/generate_summary.py "$BASEDIR" data-extraction --max-rounds $MAX_ROUNDS
```

#### Step 6b: Present summary to user

```
## Extraction Complete

### Articles: N total
- Approved round 1: N/M
- Approved round 2: N/M
- Approved round 3: N/M
- Force-accepted: N (unresolved issues flagged for human review)
- Extraction failed: N

### Iteration Statistics
- Average rounds to approval: X.X
- Total major issues raised: N
- Total major issues resolved by revision: N
- Total minor issues raised: N

### Force-Accepted Articles (require human attention)
[List article IDs and their unresolved issues]

### Files
- Per-article extractions: <basedir>/<ref-key>/extraction/extraction-final.yaml
- Per-article reviews: <basedir>/<ref-key>/extraction/review-v*.yaml
- Per-article logs: <basedir>/<ref-key>/extraction/log.yaml
- Batch summary: <basedir>/extraction-summary.yaml

### Next steps
- Human verification (TK) of all extracted data, prioritizing force-accepted articles
- Address any unresolved issues flagged in extraction-summary.yaml
- Review log.yaml files to understand revision patterns
```

## Error Handling

| Scenario | Action |
|---|---|
| Codex extraction fails for an article | Log error, continue with remaining articles |
| Codex output is not valid YAML | Log, mark as failed, continue |
| Reviewer agent times out | Use available reviewers' verdicts (skip missing reviewer) |
| Review YAML malformed | Save raw output as `review-vN-<reviewer>-raw.txt`, flag for manual review |
| Codex revision produces invalid YAML | Keep previous extraction version, set `revision_failed: true` in log |
| Codex ignores major issues | Caught in next review round; force-accept at max rounds |
| Codebook not found | Abort with clear error message |
| No article directories with fulltext.md | Abort with message to populate `data-extraction/` first |

## Notes

- The protocol specifies pilot extraction (~3 studies) before full extraction. Use `--pilot` for this.
- All AI-extracted data must be verified by a human reviewer (TK) per protocol.
- The extraction codebook (`extraction-codebook.md`) must exist in the data-extraction directory before running this skill.
- Codex CLI is used for extraction (not Claude) to provide an independent AI perspective.
- Agent Team review uses Claude agents for multi-perspective validation.
- Review findings should inform codebook refinements before scaling to full extraction.
- Use `--review-only` to run reviews on existing extractions (e.g., after codebook changes). When used, the loop starts at round 1 reviewing existing `extraction-v1.yaml` files.
- Use `--extract-only` to run extraction without review (e.g., for quick iteration).
- Use `--round N` to resume from a specific round (e.g., after a crash). Requires `extraction-vN.yaml` files to already exist.
- Structured YAML reviews enable Codex to act on specific issues programmatically, unlike narrative markdown reviews.
- The 3-reviewer approval gate ensures non-overlapping validation: fidelity (facts), framework (classification), consistency (format).
- Force-accepted articles are explicitly flagged for human prioritization.
- **Pilot findings (v1.2)**: Common Codex extraction errors include (1) confusing D1d content review with D4 AI-human agreement, (2) missing inter-model comparison as D3 evidence, (3) failing to update D_summary after revising D-category fields. These are now addressed by codebook decision rules and the validate_yaml.py D_summary consistency check. **Codebook v1.2 changes**: D3f (bias/fairness) added under Internal Structure per Downing (2003); former D5d removed, D5e renumbered to D5d. Pilot extraction data (3 studies) was generated under codebook v1.1 schema and is retained as-is; full extraction uses the v1.2 schema.
- **Helper scripts** in `.claude/skills/extract-data/scripts/`:
  - `validate_yaml.py`: Validates structure, required fields, null-value phrasing, and D_summary consistency
  - `merge_reviews.py`: Parses reviewer messages from team inbox and merges into per-article review-vN.yaml
  - `finalize.py`: Evaluates verdicts, copies approved extractions, handles force-accept, updates log.yaml
  - `generate_summary.py`: Generates extraction-summary.yaml from per-article log files
