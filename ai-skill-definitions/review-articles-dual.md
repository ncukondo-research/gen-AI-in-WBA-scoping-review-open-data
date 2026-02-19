---
name: review-articles-dual
description: Dual-AI screening with Claude Code Task agents and Codex CLI in parallel batches.
argument-hint: <session-id> <stage: title|abstract|fulltext> [--pilot] [--limit N] [--seed N] [--timeout N] [--merge-only]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Task
---

# Dual-AI Article Screening (Batch Architecture)

Input: $ARGUMENTS

## Purpose

Orchestrates dual-AI screening as specified by the protocol: Claude Opus 4.6 and OpenAI gpt-5.3-codex independently screen the same set of articles. Articles are split into batches to respect output token limits. Claude batches run as Task tool agents (run_in_background). Codex batches run via `run-codex-batches.py` (ProcessPoolExecutor). After both complete, results are merged and agreement is reported.

## Batch Sizes

| Stage | Batch size | Rationale |
|---|---|---|
| title | 50 | Title-only ~50 tokens/article |
| abstract | 20 | Title+abstract ~300-500 tokens/article |
| fulltext | 5 | Full article text, context pressure |

## Batch Naming Convention

```
<stage>-<reviewer>-batch-<NN>
```

NN is zero-padded from 01. Examples: `title-claude-batch-01`, `title-codex-batch-13`, `abstract-claude-batch-05`.

## Workflow

### Step 1: Parse arguments

Extract from `$ARGUMENTS`:
- **Session ID** (required): The search session to review
- **Stage** (required): `title`, `abstract`, or `fulltext` (determines `--basis` flag)
- **Options**:
  - `--pilot`: Run exactly 1 batch per reviewer. Sets `--limit` to the stage batch size (title=50, abstract=20, fulltext=5) and `--seed 42`.
  - `--limit N`: Number of articles to screen (default: all pending)
  - `--seed N`: Random seed for reproducible article selection (default: 42)
  - `--timeout N`: Max seconds to wait for all batches (default: 1800)
  - `--merge-only`: Skip extraction and screening, go straight to merge + finalize

If `--pilot` is provided alongside explicit `--limit` or `--seed`, the explicit values take precedence.

Pilot limit by stage: `title` -> 50, `abstract` -> 20, `fulltext` -> 5 (always = 1 batch).

### Step 2: Validate environment

Check prerequisites:

```bash
# Check codex is available
codex --version

# Check session exists
search-hub summary <session-id>
```

No tmux check needed. This architecture uses Task tool agents and subprocess-based Codex execution.

### Step 3: Initialize review (if needed)

Check if reviews.yaml exists for this session. If not, initialize:

```bash
search-hub review init --session <session-id>
```

Check current status:
```bash
search-hub review status --session <session-id>
```

If `--merge-only` is set, skip to Step 8 (Merge results).

### Step 4: Compute batch plan

Determine batch size from stage:
- `title` -> 50
- `abstract` -> 20
- `fulltext` -> 5

Count total pending articles (from `--limit` or all pending). Compute:
- `num_batches = ceil(total_articles / batch_size)`
- For each batch: `offset = i * batch_size`, `limit = batch_size` (last batch may be smaller)

**For fulltext stage**: The batch plan is determined by the preparation script (count depends on articles with available markdown). Skip the manual computation above; the script output will report the plan.

Print the plan:
```
Batch plan: <total_articles> articles, batch_size=<batch_size>, <num_batches> batches per reviewer
  Claude: <stage>-claude-batch-01 .. <stage>-claude-batch-<NN>
  Codex:  <stage>-codex-batch-01  .. <stage>-codex-batch-<NN>
```

### Step 5: Extract batches

**If stage is `title` or `abstract`:**

For each batch index `i` (0-based), for each reviewer (`claude`, `codex`):

```bash
search-hub review extract \
  --session <session-id> \
  --name <stage>-<reviewer>-batch-<NN> \
  --basis <stage> \
  --reviewer "ai:<reviewer>" \
  --filter pending \
  --sort random \
  --seed <seed> \
  --limit <batch_size> \
  --offset <i * batch_size>
```

Where `<NN>` is zero-padded batch number (01, 02, ...).

Omit `--limit` and `--offset` only if screening ALL pending articles in a single batch (unlikely with this architecture).

Note the resulting directory paths:
```
search-sessions/<session-id>/for-review/<stage>-claude-batch-01/review.yaml
search-sessions/<session-id>/for-review/<stage>-codex-batch-01/review.yaml
...
```

**If stage is `fulltext`:**

Use `prepare-fulltext-batches.py` instead of `search-hub review extract`. This script filters articles with available fulltext markdown, copies fulltext.md files into batch directories, and writes review.yaml with `fulltext.file` references.

For each reviewer (`claude`, `codex`):

```bash
SKILL_DIR=".claude/skills/review-articles-dual/scripts"
PROJECT_DIR="$(pwd)"

python3 "$SKILL_DIR/prepare-fulltext-batches.py" \
  --session-id <session-id> \
  --reviewer "ai:<reviewer>" \
  --batch-size 5 \
  --seed <seed> \
  --limit <limit> \
  --project-dir "$PROJECT_DIR"
```

Omit `--limit` if screening all eligible articles. The script will:
- Filter candidates with `screening_status` in (`include`, `uncertain`)
- Resolve fulltext.md via session fulltext lookup and `ref fulltext get`
- Copy fulltext.md files into each batch directory as `<ref_key>-fulltext.md`
- Write `review.yaml` with `fulltext.file` references pointing to the local copies
- Write `fulltext-not-retrieved.yaml` listing articles without available fulltext
- Print a summary of candidates, resolved, and not-available counts

Note the resulting directory paths:
```
search-sessions/<session-id>/for-review/fulltext-claude-batch-01/review.yaml
search-sessions/<session-id>/for-review/fulltext-codex-batch-01/review.yaml
...
```

### Step 6: Expand templates

For each batch directory, run `expand-templates.py` with the `--batch-id` argument:

```bash
SKILL_DIR=".claude/skills/review-articles-dual/scripts"
PROJECT_DIR="$(pwd)"

# Count articles in this batch
ARTICLE_COUNT=$(grep -c '^ *- title:' "<batch-dir>/review.yaml")

python3 "$SKILL_DIR/expand-templates.py" \
  --session-id <session-id> \
  --stage <stage> \
  --reviewer-name <stage>-<reviewer>-batch-<NN> \
  --reviewer-id "ai:<reviewer>" \
  --article-count "$ARTICLE_COUNT" \
  --project-dir "$PROJECT_DIR" \
  --batch-id "batch-<NN>"
```

Run this for every batch directory (both claude and codex batches).

### Step 7: Launch screening

#### Step 7a: Launch Claude batches (Task tool agents)

For each Claude batch directory, launch a Task tool agent with:
- `subagent_type`: `"general-purpose"`
- `model`: `"opus"`
- `mode`: `"bypassPermissions"`
- `run_in_background`: `true`
- `name`: `"claude-batch-<NN>"`

The prompt for each agent MUST include the full CLAUDE.md content (read from the expanded file in the batch directory). Structure:

```
Screen batch <NN> of <TOTAL> for <stage> screening.

<full content of <batch-dir>/CLAUDE.md>

## Your Task
1. Read: <absolute-path-to-batch-dir>/review.yaml
2. Screen each article. Edit review.yaml to record decisions.
3. When done: touch <absolute-path-to-batch-dir>/.claude-done
Process all <ARTICLE_COUNT> articles. Do not skip any.
```

**For fulltext stage**, add to the prompt:
```
IMPORTANT: For each article, read the fulltext markdown file referenced in
the `fulltext.file` field BEFORE making your decision. The file is located
in this batch directory: <absolute-path-to-batch-dir>/<fulltext.file>
Read the FULL text. Do not skip sections.
```

Launch all Claude batch agents in a SINGLE message with multiple Task tool calls (parallel launch).

Record each agent's task_id for monitoring.

#### Step 7b: Launch Codex batches (single background process)

Collect all Codex batch directory absolute paths. Launch a single Bash command with `run_in_background: true`:

```bash
python3 .claude/skills/review-articles-dual/scripts/run-codex-batches.py \
  --batch-dirs "<dir1>,<dir2>,<dir3>,..." \
  --max-workers 4 \
  --timeout 300
```

Record the task_id for monitoring.

#### Step 7c: Monitor progress

Poll for completion every 30 seconds using done markers (`.claude-done`, `.codex-done`, `.claude-failed`, `.codex-failed`):

```bash
# Count completed Claude batches
ls search-sessions/<session-id>/for-review/<stage>-claude-batch-*/.claude-done 2>/dev/null | wc -l

# Count completed Codex batches
ls search-sessions/<session-id>/for-review/<stage>-codex-batch-*/.codex-done 2>/dev/null | wc -l
```

Display progress: `Claude: 5/13, Codex: 3/13 [120s/1800s]`

Continue until all batches complete or timeout is reached. If timeout is reached, report which batches are incomplete and proceed with completed batches only.

### Step 8: Merge results

For each completed batch (has `.claude-done` or `.codex-done` marker):

```bash
search-hub review merge \
  --session <session-id> \
  --name <stage>-<reviewer>-batch-<NN>
```

Skip batches that have `.claude-failed` or `.codex-failed` markers (or no marker at all). Report skipped batches to the user.

If ALL Codex batches failed, inform the user that Claude results alone can be used with `--min-reviewers 1` (protocol deviation).

### Step 9: Finalize and report

Preview finalization with dual-reviewer requirement:

```bash
search-hub review finalize \
  --session <session-id> \
  --min-reviewers 2 \
  --dry-run
```

Report to the user:
- Total articles screened by each reviewer
- Agreement rate (agreed-include + agreed-exclude) / total
- Number of conflicts requiring human adjudication
- Number of articles where one or both reviewers marked `uncertain`
- Any batches that failed or timed out

Do NOT run `search-hub review finalize` without `--dry-run` unless the user explicitly requests it. The user should review the agreement report first.

**Stage-specific finalization rules:**
- **title/abstract stage**: Do NOT finalize `include` decisions. Includes must be confirmed by fulltext screening. Only finalize `exclude` consensus:
  ```bash
  search-hub review finalize \
    --session <session-id> \
    --min-reviewers 2 \
    --decision exclude
  ```
- **fulltext stage**: Finalize all decisions (both include and exclude). Omit `--decision` to finalize both.

List conflicting articles for human review:
```bash
search-hub review list --session <session-id> --filter conflicting
```

## Error Handling

| Scenario | Action |
|---|---|
| Some Claude batches timeout | Merge completed batches only. Report to user. |
| Some Codex batches fail | .codex-failed created. Merge completed only. Report. |
| ALL Codex batches fail | Claude results only, --min-reviewers 1 (protocol deviation). |
| Partial batch completion | Merge as-is; uncertain articles remain for next extraction. |

## Notes

- The protocol requires two AI reviewers with human adjudication for disagreements
- Use `--reviewer "ai:claude"` and `--reviewer "ai:codex"` to distinguish reviewers
- Always include exclusion criterion number in comments for traceability
- For pilot runs, `--pilot` always runs exactly 1 batch per reviewer (limit = batch size: title=50, abstract=20, fulltext=5)
- Both CLAUDE.md and AGENTS.md are generated from the same template for consistency; Claude reads CLAUDE.md, Codex reads AGENTS.md
- If Codex screening fails, Claude results alone can be used with `--min-reviewers 1` (but this should be documented as a protocol deviation)
- Claude Task agents use `model: "opus"` to ensure consistent Opus 4.6 reasoning quality across all batches
