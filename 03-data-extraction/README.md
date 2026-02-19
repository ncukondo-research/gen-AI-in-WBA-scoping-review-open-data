# Data Extraction: AI Interaction Audit Trail

This directory documents the complete AI-assisted data extraction process for 13 included studies, conducted in February 2026.

## Process Overview

Data extraction used a dual-AI approach: OpenAI Codex CLI (GPT-5.3-Codex) performed initial extraction from fulltext articles, then three specialized Claude Opus 4.6 reviewer agents validated each extraction through iterative review-revision rounds. Human verification (TK) provided final quality assurance.

### Extraction Architecture

```
13 included articles (from screening)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Codex CLI Extraction                                │
│  (GPT-5.3-Codex reads fulltext + codebook)          │
│  → extraction-v1.yaml per article                    │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  3-Reviewer Validation (Claude Opus 4.6 agents)     │
│                                                      │
│  Fidelity Reviewer ─── verify facts vs fulltext     │
│  Framework Reviewer ── assess Downing classification │
│  Consistency Reviewer─ check YAML structure/coding   │
│                                                      │
│  → review-v1.yaml (structured YAML feedback)         │
└─────────────────────────────────────────────────────┘
        │
    ┌───┴───┐
    │       │
 Approved  Revise ──→ Codex re-extracts → review-v2.yaml → ...
    │
    ▼
 extraction-final.yaml
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Human Verification (TK)                             │
│  → verification-log.yaml                             │
└─────────────────────────────────────────────────────┘
```

### Extraction Statistics

| Metric | Value |
|--------|-------|
| Total articles extracted | 13 |
| Approved in Round 1 | 8 (62%) |
| Approved in Round 2 | 5 (38%) |
| Failed extractions | 0 |
| Unresolved major issues | 0 |

### Human Verification Results

| Verdict | Count | Description |
|---------|-------|-------------|
| Pass (no issues) | 3 | Extraction verified correct |
| Pass after correction | 6 | Minor corrections applied post-verification |
| Pass with minor issues | 4 | Acceptable with noted caveats |
| Fail | 0 | None required re-extraction |

## Extraction Framework

Data was extracted using Downing's validity framework with the following category structure:

| Category | Content |
|----------|---------|
| **A** (Study identification) | Country, specialty, participants, study design, aims |
| **B** (AI intervention) | Models, API/interface, prompt design, AI role, input/output data, comparator |
| **C** (WBA context) | Assessment tools, clinical setting |
| **D** (Validity evidence) | D1: Content, D2: Response process, D3: Internal structure, D4: Relationships, D5: Consequences |
| **E** (Limitations) | Study limitations, future research, funding/COI |
| **F** (Key findings) | Summary, RQ3 relevance, extractor confidence |

Each D-category includes detailed sub-items (e.g., D2a: reasoning transparency, D2b: hallucination assessment, D3c: inter-model agreement). See `validity-sub-items.yaml` for the complete mapping.

## Three Reviewer Roles

| Reviewer | Focus | Checks |
|----------|-------|--------|
| **Fidelity Reviewer** | Source accuracy | Statistics, quotes, and claims match fulltext; no hallucinated data |
| **Framework Reviewer** | Conceptual alignment | Downing validity categories correctly applied; evidence mapped to right sub-items |
| **Consistency Reviewer** | Structural quality | YAML format valid; null-value phrasing correct; cross-study coding consistent |

Each reviewer produces structured YAML feedback:
```yaml
verdict: approve  # or revise
confidence: high  # or medium, low
issues:
  major: []       # must be fixed before approval
  minor: []       # suggestions for improvement
commendations: [] # well-done aspects
```

All three reviewers must approve for an extraction to be finalized. If any reviewer issues a "revise" verdict, Codex re-extracts incorporating the feedback.

## Files in This Directory

### Top-Level Files

| File | Size | Description |
|------|------|-------------|
| `extraction-codebook.md` | 41 KB | Complete extraction instructions and field definitions (v1.6) |
| `validity-sub-items.yaml` | 8 KB | Downing's framework sub-item definitions for synthesis |
| `articles-index.yaml` | 4 KB | Master index of 13 included articles with metadata |
| `extraction-summary.yaml` | 3 KB | Workflow statistics (rounds, verdicts, timing) |
| `verification-log.yaml` | 12 KB | Human verification results and corrections applied |

### `extractions/` (13 article subdirectories)

Each article directory contains the complete extraction history:

```
article-id/
├── bibliography.json         # Article metadata (authors, DOI, PMID, journal)
├── extraction-v1.yaml        # Initial Codex extraction
├── review-v1.yaml            # 3-reviewer feedback on v1
├── extraction-v2.yaml        # Revised extraction (if needed)
├── review-v2.yaml            # Feedback on v2 (if applicable)
├── extraction-final.yaml     # Verified final extraction
└── log.yaml                  # Iteration log (versions, verdicts, timestamps)
```

The `extraction-final.yaml` is the authoritative extraction for each article. Version history files (`extraction-v1.yaml`, `review-v1.yaml`, etc.) document the iterative refinement process.

### `restructuring-reviews/` (39 review files)

Post-extraction field restructuring reviews organized by field:

| Directory | Field | Purpose |
|-----------|-------|---------|
| `archive-a4-restructure/` | A4 (study design) | Reviews of temporal vs. analytical approach split |
| `archive-d-restructure/` | D (validity evidence) | Reviews of evidence presence coding |
| `archive-f1-restructure/` | F1 (key findings) | Reviews of summary/detail structure conversion |

### `scripts/`

Helper scripts for the extraction workflow:

| Script | Purpose |
|--------|---------|
| `validate_yaml.py` | Validates YAML syntax, required fields, D-category sub-items, null-value phrasing |
| `merge_reviews.py` | Parses 3 reviewer feedback blocks, merges into per-article review-vN.yaml |
| `finalize.py` | Evaluates verdicts, copies approved extractions to extraction-final.yaml, handles force-accept |
| `generate_summary.py` | Generates extraction-summary.yaml with aggregate statistics |

## AI Skill Definition

The orchestration skill is in [`../ai-skill-definitions/extract-data.md`](../ai-skill-definitions/extract-data.md). Key workflow steps:

1. Codex CLI extracts data from fulltext using the codebook
2. `validate_yaml.py` checks extraction format
3. Three Claude Opus 4.6 Task agents review in parallel (fidelity, framework, consistency)
4. `merge_reviews.py` consolidates reviewer feedback
5. `finalize.py` determines if approved or needs revision
6. If revision needed: Codex re-extracts with feedback, loop back to step 2
7. Maximum 3 rounds; force-accept if unresolved after max rounds

## Included Articles

| # | Study ID | Specialty | AI Role |
|---|----------|-----------|---------|
| 1 | ahmad-2025 | Otolaryngology | LLM evaluation of resident feedback |
| 2 | atsukawa-2025 | Radiology | AI scoring of radiology exams |
| 3 | bala-2025 | Radiology | LLM evaluation of reporting skills |
| 4 | bany_abdelnabi-2025 | Internal Medicine | LLM feedback on H&P notes |
| 5 | furey-2025 | Surgery | AI-augmented operative notes |
| 6 | Gin2024-ss | Mixed | NLP analysis of learning curves |
| 7 | Jarry-Trujillo2024-kg | Surgery | LLM evaluation of narrative feedback |
| 8 | Kondo2025-jx | Mixed | Automated WBA evaluation quality |
| 9 | kwan-2025 | Surgery | LLM evaluation of narrative feedback |
| 10 | lyo-2025 | Radiology | LLM evaluation of reporting |
| 11 | Partin2025-nj | Family Medicine | ChatGPT competency committee alignment |
| 12 | preiksaitis-2025 | Emergency Medicine | AI vs human feedback differentiation |
| 13 | Zhou2025-fj | Radiology | AI scoring in radiology exams |

## Notes on Copyright

Article fulltexts (`fulltext.md`) and figures (`fulltext_artifacts/`) are not included in this repository due to copyright restrictions. The extraction YAML files contain only structured data fields extracted from the articles, not verbatim reproductions of article text beyond brief quotations for verification purposes.
