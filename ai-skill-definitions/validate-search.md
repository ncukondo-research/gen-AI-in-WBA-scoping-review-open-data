---
name: validate-search
description: Validate search recall by checking whether known relevant articles are captured in search results. Compares session results against a validation set (reference list or known PMIDs/DOIs) and reports capture rate.
argument-hint: [session-id] [ref-key, PMID list, DOI list, or file path]
context: fork
allowed-tools: Bash(search-hub *, ref *), Read, Write, Grep, Glob
---

# Validate Search Recall

Input: $ARGUMENTS

## Purpose

Validates that a search strategy captures known relevant articles. This is a critical quality check: if the search misses articles that should be included per the protocol's inclusion criteria, the query needs refinement.

## Workflow

### Step 1: Parse arguments

Extract from `$ARGUMENTS`:
- **Session ID**: The search session to validate (e.g., `20260211_wbagenaiv4_c63edc`)
- **Validation source**: One of:
  - A pre-built validation file in `protocol/validation/` (e.g., `protocol/validation/khan2025-validation-dois.txt`)
  - A `ref` library key (e.g., `Khan2025-ab`) pointing to a review article whose reference list serves as the validation set
  - A comma-separated list of PMIDs (e.g., `39158925,38456789`)
  - A comma-separated list of DOIs
  - A file path containing identifiers (one per line)

### Step 2: Prepare identifier file for `search-hub check`

The `search-hub check` command accepts identifiers via `--file`, `--pmid`, or `--doi` flags. Prepare the input accordingly.

**If validation file exists in `protocol/validation/`**: Use the file directly. These are pre-curated DOI/PMID lists:
```bash
# List available validation sets
ls protocol/validation/*.txt
```

**If ref key**: Read the article's fulltext to extract cited references:
```bash
# Read fulltext as Markdown
ref fulltext get --markdown --stdout <key>
```
Focus on articles cited in the results/discussion sections that represent the study's included articles. Collect PMIDs and DOIs from these references and save to `protocol/validation/<key>-validation-dois.txt` (one per line):
```
# File format: one identifier per line
10.1001/jama.2023.12345   (DOI, starts with "10.")
37654321                   (PMID, numeric only)
# comment lines are ignored
```

**If PMID/DOI list**: Use directly with `--pmid` or `--doi` flags, or write to a file for larger lists.

**If file path**: Use the file directly with `--file`.

For any identifiers not in the ref library, add them for metadata:
```bash
ref add <identifier>
```

### Step 3: Run coverage check with `search-hub check`

Use the native `search-hub check` command for automated matching:

```bash
# Check from file (supports DOIs, PMIDs, arXiv IDs)
search-hub check <session-id> --file <path-to-identifiers>

# Or check specific PMIDs/DOIs directly
search-hub check <session-id> --pmid "39158925,38456789"
search-hub check <session-id> --doi "10.1001/jama.2023.12345"

# Use --json for structured output
search-hub check <session-id> --file <path> --json

# Use --missing-only to focus on gaps
search-hub check <session-id> --file <path> --missing-only
```

### Step 4: Investigate missing articles

For articles reported as missing by `search-hub check`, determine whether each is a genuine gap or outside scope.

For each missing article, look up details:
```bash
ref search "<author or keyword>"
ref cite <key> --style apa
```

If needed, search within session results using query filtering:
```bash
search-hub results <session-id> -q "author:<surname>"
search-hub results <session-id> -q "title:<keyword>"
```

### Step 5: Classify missing articles

For each missing article, classify as:

- **MISSED - Outside scope**: The article falls outside the search protocol's scope:
  - Published outside the date range
  - Not in a searched database
  - Uses conventional AI/ML rather than generative AI (per protocol exclusion)
  - Not about workplace-based assessment
  - Not about medical education
  - Written in a non-English language
- **MISSED - Genuine gap**: The article should have been captured per the protocol's inclusion criteria. This indicates a gap in the search strategy.

Read the study protocol (`protocol/protocol.md`) to make scope determinations.

### Step 6: Generate recall report

Output the report in the following format:

```
## Search Validation Report

**Session**: [session-id]
**Validation source**: [source description]
**Date**: [date]

### Results

| # | Article | Status | Detail |
|---|---------|--------|--------|
| 1 | Author (Year). Title | CAPTURED | PMID match |
| 2 | Author (Year). Title | MISSED - Outside scope | Pre-2022 publication |
| 3 | Author (Year). Title | MISSED - Genuine gap | GenAI + WBA, not captured |

### Summary

- **Total validation articles**: N
- **Captured**: X (X%)
- **Missed - Outside scope**: Y (Y%)
- **Missed - Genuine gap**: Z (Z%)
- **Recall (in-scope only)**: X / (X + Z) = R%

### Recommendations

[If genuine gaps exist:]
- Specific terms or headings that would capture missed articles
- Whether the gap is systematic (missing concept) or incidental (unusual terminology)

[If all in-scope articles captured:]
- Confirm adequate recall for the search strategy
```

### Step 7: Suggest next steps

- If genuine gaps found: Recommend using `/develop-search-strategy` to refine the query, with specific term suggestions
- If recall is adequate: Confirm the search strategy is validated and ready for screening
- If validation set is small: Note the limitation and suggest additional validation sources
