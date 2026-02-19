# Article Screening: AI Interaction Audit Trail

This directory documents the complete dual-AI screening process for 709 articles across three stages (title, abstract, fulltext), conducted in February 2026.

## Process Overview

The protocol required two independent AI reviewers screening each article, with human adjudication for disagreements. A liberal (inclusive) advancement approach was used: articles were excluded only when both AI reviewers agreed.

### Screening Architecture

```
709 articles (from search v8)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Title Screening (14 batches x 2 reviewers)         │
│  Claude Opus 4.6 ──┐                                │
│                     ├── Consensus → Exclude (127)    │
│  GPT-5.3-Codex  ───┘   Advance  → 582 articles     │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Abstract Screening (21 batches x 2 reviewers)      │
│  Claude Opus 4.6 ──┐                                │
│                     ├── Consensus → Exclude (535)    │
│  GPT-5.3-Codex  ───┘   Advance  → 47 articles      │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Fulltext Screening (9 batches x 2 reviewers)       │
│  Claude Opus 4.6 ──┐                                │
│                     ├── Human adjudication (TK)      │
│  GPT-5.3-Codex  ───┘   for conflicts                │
└─────────────────────────────────────────────────────┘
        │
        ▼
   13 articles included
```

### Reviewers

| Reviewer | Model | Role |
|----------|-------|------|
| `ai:claude` | Claude Opus 4.6 (Anthropic) | Independent AI reviewer |
| `ai:codex` | GPT-5.3-Codex (OpenAI) | Independent AI reviewer |
| `TK` / `human:TK` | Human (lead author) | Conflict adjudication, final decisions |

### Batch Configuration

| Stage | Batch Size | Batches per Reviewer | Total Batches |
|-------|-----------|---------------------|---------------|
| Title | 50 articles | 14 | 28 |
| Abstract | 20 articles | 21 | 42 |
| Fulltext | 5 articles | 9 | 18 |

## Screening Statistics

| Metric | Value |
|--------|-------|
| Total articles screened | 709 |
| Total screening decisions | 2,326 |
| Final included | 13 (1.8%) |
| Final excluded | 696 (98.2%) |

### Exclusion Criteria Distribution

| Criterion | Count | Description |
|-----------|-------|-------------|
| 2 | 504 | Not about assessment, feedback, or analysis of observation records |
| 1 | 395 | Not about generative AI or LLMs |
| 4 | 342 | Not in workplace-based or clinical education setting |
| 7 | 132 | Not original research article |
| 3 | 121 | Assessment conducted entirely in simulated environments (OSCEs) |
| 6 | 63 | Participants not medical/health-professional learners |
| 5 | 4 | No validity/reliability/acceptability/impact data |

Criteria 1, 2, and 4 account for 71% of all exclusion citations, reflecting the main filtering dimensions: generative AI focus, assessment/feedback focus, and workplace-based setting.

### Decision Flow by Stage

| Stage | Screened | Excluded (consensus) | Advanced |
|-------|----------|---------------------|----------|
| Title | 709 | 127 | 582 |
| Abstract | 582 | 535 | 47 |
| Fulltext | 47 | 34 | 13 |

## How AI Screening Worked

### 1. Skill Invocation

The lead author invoked the `/review-articles-dual` skill for each screening stage:
```
/review-articles-dual 20260216_genaiwbav8_0134a3 title
/review-articles-dual 20260216_genaiwbav8_0134a3 abstract
/review-articles-dual 20260216_genaiwbav8_0134a3 fulltext
```

### 2. Batch Extraction and Template Expansion

For each stage, the skill:
1. Split articles into batches (size depends on stage)
2. Extracted `review.yaml` files per batch via `search-hub review extract`
3. Expanded the `CLAUDE.md` template with stage-specific rules and calibration examples using `expand-templates.py`

### 3. Parallel Dual-AI Screening

Two independent processes ran in parallel:
- **Claude batches**: Each batch launched as a Claude Code Task agent (background), reading the expanded `CLAUDE.md` instructions and editing `review.yaml`
- **Codex batches**: All batches launched via `run-codex-batches.py` (ProcessPoolExecutor), each reading `AGENTS.md` (same content as CLAUDE.md) and editing `review.yaml`

### 4. Merge and Consensus

After both reviewers completed:
1. Batch results merged back into central `reviews.yaml` via `search-hub review merge`
2. Consensus calculated: agreed-include, agreed-exclude, or conflicting
3. For title/abstract stages: only agreed-exclude decisions finalized (liberal approach)
4. For fulltext stage: human (TK) adjudicated all conflicts and made final decisions

## Files in This Directory

### `reviews.yaml` (2.1 MB, 22,489 lines)

The complete screening audit trail. Each of the 709 articles contains:

```yaml
- title: "Article Title"
  doi: "10.xxxx/..."
  pmid: "12345678"
  authors: "Author1, Author2, ..."
  year: "2024"
  abstract: "Full abstract text..."
  reviews:
    - decision: exclude          # or include, uncertain
      comment: "Exclusion criterion 1: conventional ML, not generative AI"
      reviewer: ai:claude        # or ai:codex, TK, human:TK
      basis: title               # or abstract, fulltext
      timestamp: "2026-02-17T..."
    - decision: exclude
      comment: "Exclusion criterion 1: ..."
      reviewer: ai:codex
      basis: title
      timestamp: "2026-02-17T..."
  finalDecision: exclude         # or include
  mergedFrom:
    - source: pubmed             # or scopus, eric, arxiv
```

This file enables:
- Inter-rater agreement analysis (compare ai:claude vs ai:codex decisions)
- Exclusion pattern analysis per criterion
- Decision evolution tracking across stages
- Human adjudication pattern analysis

### `screening-templates/`

Template files that defined the AI reviewers' behavior:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Main instruction template with inclusion/exclusion criteria, stage-specific rules, and calibration examples. Contains `{{placeholders}}` expanded per batch. |
| `prompt.md` | Short task prompt instructing the AI to begin screening and create a completion marker. |

The `CLAUDE.md` template includes:
- PCC framework inclusion criteria
- 9 numbered exclusion criteria with detailed descriptions
- `{{STAGE_RULES}}` placeholder for stage-specific decision rules
- `{{CALIBRATION_EXAMPLES}}` placeholder for worked examples
- `{{FULLTEXT_INSTRUCTIONS}}` placeholder for fulltext reading instructions

### `scripts/`

Python scripts that orchestrated the dual-AI screening:

| Script | Purpose |
|--------|---------|
| `expand-templates.py` | Substitutes `{{placeholders}}` in templates with session-specific values (stage rules, calibration examples, batch IDs). Generates both `CLAUDE.md` (for Claude) and `AGENTS.md` (for Codex) per batch. |
| `prepare-fulltext-batches.py` | For fulltext screening: resolves fulltext markdown paths, copies files into batch directories, writes `review.yaml` with `fulltext.file` references. |
| `run-codex-batches.py` | Launches Codex screening on multiple batches in parallel using ProcessPoolExecutor. Creates `.codex-done` or `.codex-failed` markers. |

## AI Skill Definitions

The skill definitions that orchestrated the entire workflow are in [`../ai-skill-definitions/`](../ai-skill-definitions/):

| Skill | Purpose |
|-------|---------|
| `review-articles-dual` | Primary orchestration skill: batch planning, parallel dual-AI launch, monitoring, merge, and finalize |
| `review-articles` | Base workflow skill: single-reviewer screening with `search-hub review` commands |

## Stage-Specific Rules (from expand-templates.py)

### Title Screening
- Only `exclude` or `uncertain` allowed (no `include` at title stage)
- Conservative approach: exclude only when clearly outside scope
- Uncertain articles advance to abstract screening

### Abstract Screening
- `include`, `exclude`, or `uncertain` allowed
- More definitive decisions expected with abstract context
- Uncertain articles advance to fulltext screening

### Fulltext Screening
- Only `include` or `exclude` allowed (no `uncertain`)
- Must read complete fulltext markdown before deciding
- Focus on: generative AI use, workplace-based setting, assessment/feedback data
