---
name: review-articles
description: Article screening and review workflow using search-hub review module. Supports title screening, abstract screening, and full-text screening with dual-reviewer consensus and human oversight.
argument-hint: [session-id] [stage: title|abstract|fulltext] or "status <session-id>"
allowed-tools: Bash(search-hub *, ref *), Read, Write, Edit, Grep, Glob
---

# Review Articles

Input: $ARGUMENTS

## Purpose

Manages the systematic screening workflow for a scoping review session. Supports the protocol's three-stage screening process (title, abstract, full-text) with dual-AI review and human oversight.

## Workflow

### Step 1: Parse arguments

Extract from `$ARGUMENTS`:
- **Session ID**: The search session to review
- **Stage**: `title`, `abstract`, or `fulltext` (determines the `--basis` flag)
- **Action**: `init`, `extract`, `mark`, `merge`, `finalize`, `status`, or `export`

If only a session ID is provided, show current review status.

### Step 2: Initialize review (first time only)

Generate the reviews.yaml file from deduplicated search results:

```bash
search-hub review init --session <session-id>
```

This creates `search-sessions/<session-id>/reviews.yaml` with all articles set to `pending`.

Check initial status:
```bash
search-hub review status --session <session-id>
```

### Step 3: Extract articles for review

Extract a batch of articles for a specific screening stage:

```bash
# Extract for title screening (AI reviewer)
search-hub review extract \
  --session <session-id> \
  --name title-screening-claude \
  --basis title \
  --reviewer "ai:claude" \
  --filter pending

# Extract for abstract screening
search-hub review extract \
  --session <session-id> \
  --name abstract-screening-claude \
  --basis abstract \
  --reviewer "ai:claude" \
  --filter pending

# Extract for full-text screening
search-hub review extract \
  --session <session-id> \
  --name fulltext-screening-claude \
  --basis fulltext \
  --reviewer "ai:claude" \
  --filter pending

# Extract with limit for pilot batches
search-hub review extract \
  --session <session-id> \
  --name pilot-title \
  --basis title \
  --reviewer "ai:claude" \
  --filter pending \
  --limit 50 \
  --sort random \
  --seed 42
```

The extracted file is saved to `search-sessions/<session-id>/for-review/<name>/review.yaml`.

### Step 4: Screen articles

Read the extracted review file and make decisions for each article.

For each article, apply the exclusion criteria from the protocol:
1. Not about generative AI or LLMs
2. Not about assessment, feedback, or analysis of observation records
3. Assessment conducted entirely in simulated environments (e.g., OSCEs)
4. Not in a workplace-based or clinical education setting
5. No data on validity, reliability, acceptability, or educational impact
6. Participants are not medical/health-professional learners
7. Not an original research article, systematic review, meta-analysis, or preprint
8. Published before 2022
9. Not in English

Mark decisions in the work file:

```bash
# Mark individual articles
search-hub review mark \
  --file search-sessions/<session-id>/for-review/<name>/review.yaml \
  --id <article-id> \
  --decision include \
  --comment "GenAI used for WBA feedback"

search-hub review mark \
  --file search-sessions/<session-id>/for-review/<name>/review.yaml \
  --id <article-id> \
  --decision exclude \
  --comment "Exclusion criterion 1: conventional ML, not generative AI"

search-hub review mark \
  --file search-sessions/<session-id>/for-review/<name>/review.yaml \
  --id <article-id> \
  --decision uncertain \
  --comment "Unclear if workplace-based; needs abstract review"
```

You can also directly edit the review YAML file to batch-process decisions.

### Step 5: Merge reviewed file back

After completing a review batch, merge it back into the main reviews.yaml:

```bash
search-hub review merge \
  --session <session-id> \
  --name title-screening-claude
```

### Step 6: Monitor progress

Check review progress at any time:

```bash
# Overall progress
search-hub review status --session <session-id>

# List articles filtered by status
search-hub review list --session <session-id> --filter pending
search-hub review list --session <session-id> --filter agreed-include
search-hub review list --session <session-id> --filter conflicting
```

Available filter values: `pending`, `incomplete`, `uncertain`, `agreed-include`, `agreed-exclude`, `conflicting`, `finalized`

### Step 7: Finalize consensus decisions

After all reviewers have completed their assessments, auto-set finalDecision for articles with consensus:

```bash
# Preview finalization
search-hub review finalize --session <session-id> --dry-run

# Finalize (requires at least 1 agreeing reviewer by default)
search-hub review finalize --session <session-id>

# Require 2 agreeing reviewers for consensus
search-hub review finalize --session <session-id> --min-reviewers 2
```

**Stage-specific finalization rules:**
- **title/abstract stage**: Do NOT finalize `include` decisions. Includes must be confirmed by fulltext screening. Only finalize `exclude` consensus:
  ```bash
  search-hub review finalize \
    --session <session-id> \
    --min-reviewers 2 \
    --decision exclude
  ```
- **fulltext stage**: Finalize all decisions (both include and exclude). Omit `--decision` to finalize both.

For conflicting decisions, extract for human adjudication:
```bash
search-hub review extract \
  --session <session-id> \
  --name conflicts-human \
  --filter conflicting \
  --finalize
```

### Step 8: Export results

Export articles based on final decisions:

```bash
# Export included articles
search-hub review export \
  --session <session-id> \
  --only included \
  -o search-sessions/<session-id>/included.yaml

# Export excluded articles
search-hub review export \
  --session <session-id> \
  --only excluded \
  -o search-sessions/<session-id>/excluded.yaml

# Export as JSON
search-hub review export \
  --session <session-id> \
  --only included \
  --format json \
  -o search-sessions/<session-id>/included.json
```

### Step 9: Register included articles to ref library

After screening is complete, register only the included articles:

```bash
search-hub register <session-id> --reviewed --with-abstracts
```

## Multi-stage workflow

The protocol specifies three sequential screening stages. After each stage:

1. **Title screening** → Merge results → Finalize → Next stage uses articles with `finalDecision=include`
2. **Abstract screening** → Merge results → Finalize → Next stage uses articles with `finalDecision=include`
3. **Full-text screening** → Merge results → Finalize → Export final included set

For each stage, extract with `--filter pending` to get only articles that passed the previous stage.

## Notes

- The protocol requires two AI reviewers (Claude and GPT) with human adjudication
- Use `--reviewer "ai:claude"` and `--reviewer "ai:gpt"` to track which model made each decision
- Always include the exclusion criterion number in comments for traceability
- For pilot batches, use `--limit` and `--seed` for reproducible random samples
- Use `/manage-fulltext` to prepare full texts before the full-text screening stage
