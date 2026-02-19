# Search Strategy Development: AI Interaction Audit Trail

This directory documents the complete AI-assisted search strategy development process, conducted over February 12--16, 2026.

## Process Overview

The search strategy was developed through 8 iterative query versions (v1 through v8), refined via AI-assisted PRESS 2015 peer review followed by human expert review. The process involved three phases:

1. **Initial development (v1--v3)**: Protocol-derived concept framework, noise reduction
2. **PRESS-driven refinement (v4--v6)**: AI-identified MeSH gaps, model name coverage
3. **Human expert review and finalization (v7--v8)**: Abbreviation optimization, co-author audit

### Workflow Diagram

```
Protocol (PCC Framework)
        │
        ▼
┌─────────────────────────────────┐
│  /develop-search-strategy       │  ← AI skill definition
│  (Create/refine query YAML)     │
└───────────┬─────────────────────┘
            │
            ▼
     Execute search via Search-Hub
     (PubMed, Scopus, ERIC, arXiv)
            │
            ▼
     Review results + assess precision/recall
            │
            ▼
┌─────────────────────────────────┐
│  /press-review                  │  ← AI skill definition
│  (PRESS 2015 6-element review)  │
└───────────┬─────────────────────┘
            │
        ┌───┴───┐
        │       │
     Approve  Refine ──→ (loop back to /develop-search-strategy)
        │
        ▼
   Human PRESS review (TK)
        │
        ▼
   Co-author audit (YK)
        │
        ▼
   Final strategy (v8)
```

## AI Skill Definitions Used

These are the AI instruction sets that directed Claude Code's behavior during search development. See [`../ai-skill-definitions/`](../ai-skill-definitions/) for the full definitions.

| Skill | Purpose | Invocations |
|-------|---------|-------------|
| `develop-search-strategy` | Iterative query creation, execution, assessment, and refinement | Used for each version (v1--v8) |
| `press-review` | PRESS 2015 peer review of completed search strategies | Used after v3, v4, v5, v6 |
| `validate-search` | Recall validation against known relevant articles | Used for validation checks throughout |

### How Skills Work

Each skill is a Markdown file with structured step-by-step instructions. When the lead author invoked a skill (e.g., typing `/develop-search-strategy resume <session-id>`), Claude Code executed the workflow defined in the skill file: reading session data, analyzing results, proposing refinements, executing searches, and recording assessments.

The skill definitions constrain the AI's behavior:
- **Allowed tools**: Each skill specifies which CLI tools and file operations the AI may use
- **Decision criteria**: Explicit rules for when to accept, refine, or reject a query
- **Output format**: Structured assessment format with precision estimates and verdicts

## Files in This Directory

### `query-versions/`

Query YAML files for all 9 iterations (v1 through v8, plus one test variant). Each file defines:
- Concept blocks with keywords, MeSH terms, and ERIC descriptors
- Boolean logic (OR within blocks, AND between blocks)
- Database-specific replacement rules (e.g., simplified terms for ERIC/arXiv)
- Filters (year range, language)

These files are the input to Search-Hub's `search` command. To reproduce a search, install Search-Hub and run:
```bash
search-hub search query-versions/genai_wba_v8.yaml
```

| File | Version | Key Changes |
|------|---------|-------------|
| `genai_wba_v1.yaml` | v1 (Initial) | Protocol-derived PCC framework; preview only |
| `genai_wba_v2.yaml` | v2 | Removed noisy standalone terms (feedback, scoring, grading) |
| `genai_wba_v3.yaml` | v3 | Removed broad WBA terms; added specific compound terms |
| `genai_wba_v4.yaml` | v4 | Added MeSH "Generative Artificial Intelligence"; GPT-5 |
| `genai_wba_v5.yaml` | v5 | Added MeSH "Large Language Models", "Chatbot" |
| `genai_wba_v6.yaml` | v6 | Added DeepSeek (o1-preview/Grok excluded after ERIC testing) |
| `genai_wba_v7.yaml` | v7 | Removed ambiguous abbreviations; added GPT-4.1/4.5 with ERIC fix |
| `genai_wba_v7_b2test.yaml` | v7 B2 test | Isolation test for Block 2 keyword additions |
| `genai_wba_v8.yaml` | v8 (Final) | Removed 3 redundant child MeSH from concept-meded |

### `session-assessments.yaml`

Consolidated metadata and reviewer notes from all 11 search sessions. Each session entry includes:
- Per-database hit counts (PubMed, ERIC, arXiv, Scopus)
- AI reviewer assessments with precision estimates and verdicts
- PRESS 2015 peer review findings
- Human reviewer comments and approval decisions
- Co-author review notes

This file preserves the complete decision audit trail verbatim from the original session notes.

### `final-rendered-queries/`

The exact query strings sent to each database for the final search (v8, session `20260216_genaiwbav8_0134a3`):

| File | Database | Hits |
|------|----------|------|
| `pubmed_query.txt` | PubMed | 470 |
| `scopus_query.txt` | Scopus | 90 |
| `eric_query.txt` | ERIC | 181 |
| `arxiv_query.txt` | arXiv | 4 |

Total: 745 hits (707 unique after deduplication).

## Version History Summary

| Version | Date | Unique Articles | Reviewer | Verdict |
|---------|------|-----------------|----------|---------|
| v1 | Feb 12 | (preview) | AI | Refine |
| v2 | Feb 12 | 764 | AI | Refine |
| v3 | Feb 12 | 674 | AI (PRESS) | Refine |
| v4 | Feb 12 | 690 | AI (PRESS) | Refine |
| v5 | Feb 12 | 690 | AI (PRESS) | Refine |
| v6 | Feb 12 | 706 | AI (PRESS x2) + Human | Human: Refine |
| v7 | Feb 13 | 706 | Human (TK) | Approved |
| v8 | Feb 16 | 706 | Human (TK) | Approved |

All versions maintained 100% recall against the validation set (2/2 seed articles).

## Key Methodological Decisions

1. **Abbreviation removal (v7)**: Short abbreviations (LLM, EPA, DOPS, WBA, CBME) were removed after empirical testing confirmed 0 relevant articles lost while reducing false positives from unrelated fields (environmental science, law)

2. **ERIC parser workarounds (v6--v7)**: Three Lucene parsing issues were discovered and addressed through provider-specific replacement blocks: hyphen-as-NOT, case-insensitive matching, and period parsing

3. **GPT\* wildcard rejection (v8 testing)**: Consolidating GPT model names into `GPT*` was rejected after discovering false positives from "GPT" = "General Practice Training" in family medicine literature

4. **Forward citation gap analysis (v7)**: Two uncaptured articles from citation tracking were confirmed as database coverage gaps (journals not yet indexed), not search term deficiencies
