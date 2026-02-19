---
name: press-review
description: Systematic PRESS 2015 (Peer Review of Electronic Search Strategies) evaluation of a completed search strategy. Assesses 6 elements and produces a structured review with recommendations.
argument-hint: [session-id or query file path]
allowed-tools: Bash(search-hub *, ref *), Read, Grep, Glob, WebSearch, WebFetch
---

# PRESS 2015 Peer Review of Search Strategy

Target: $ARGUMENTS

## Background

The PRESS (Peer Review of Electronic Search Strategies) 2015 guideline provides a systematic framework for peer reviewing search strategies used in systematic and scoping reviews. This skill evaluates a search strategy against all 6 PRESS elements.

**Reference**: McGowan J, Sampson M, Salzwedel DM, et al. PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. J Clin Epidemiol. 2016;75:40-46.

## Workflow

### Step 1: Load the search strategy

Determine whether `$ARGUMENTS` is a session ID or a query file path.

**If session ID**:
```bash
search-hub summary <session-id>
search-hub results <session-id>
```
Then read the session directory files:
- `search-sessions/<session-id>/session.yaml` for metadata and hit counts
- `search-sessions/<session-id>/query_common.yaml` for the query as executed
- The original query YAML file (referenced in `session.yaml` under `query.file`)

**If query file path**:
Read the file directly and check for any associated sessions.

Also read the study protocol (`protocol/protocol.md`) to understand the research question and scope.

Inspect how the query resolves per provider to understand database-specific translations:
```bash
search-hub query inspect <query-file>
search-hub query inspect <query-file> --db pubmed  # single provider
```

### Step 2: Evaluate each PRESS element

For each element, assess adequacy and identify issues.

#### Element 1: Translation of the research question

- Does the search strategy reflect the research question/PICO/PCC framework?
- Are all key concepts from the protocol represented as concept blocks?
- Are concept blocks combined with appropriate Boolean logic (AND for across concepts)?
- Is any concept missing or inadequately represented?

#### Element 2: Boolean and proximity operators

- Is OR used correctly within concept blocks (to combine synonyms)?
- Is AND used correctly between concept blocks (to intersect concepts)?
- Is NOT/exclude used appropriately and not overly restrictive?
- Are proximity operators used where beneficial (if supported by the database)?
- Is operator precedence correct (parenthetical grouping)?

#### Element 3: Subject headings

- Are appropriate controlled vocabulary terms used for each database?
  - PubMed: MeSH headings
  - ERIC: ERIC descriptors
- Are subject headings exploded where appropriate?
- Are any key subject headings missing?
- Are any subject headings too broad (capturing irrelevant subtopics)?
- Note: Some concepts may lack appropriate controlled vocabulary (e.g., no MeSH for "generative AI" as of 2025)

#### Element 4: Text word search (free-text terms)

- Are sufficient synonyms, abbreviations, and variant spellings included?
- Are acronyms included alongside full terms?
- Are truncation/wildcard operators used where appropriate?
- Are phrase searches used correctly?
- Are any important text word terms missing?
- Are model-specific terms included where relevant (e.g., specific AI model names)?

#### Element 5: Spelling, syntax, and line numbers

- Are all terms spelled correctly?
- Is the YAML syntax valid? Validate with:
  ```bash
  search-hub query validate <query-file>
  ```
- Are field codes correct (e.g., `title_abstract`)?
- Are database-specific syntax requirements met? Verify per-provider resolution:
  ```bash
  search-hub query inspect <query-file>
  ```
- Are there any logical contradictions (term in both include and exclude)?

#### Element 6: Limits and filters

- Are date limits appropriate for the research question?
- Are language filters justified and documented?
- Are publication type filters appropriate (if any)?
- Are any filters overly restrictive, risking missed relevant articles?

### Step 3: Check for additional considerations

Using WebSearch if needed:
- Are there recently introduced MeSH headings or ERIC descriptors that should be included?
- Are there additional synonyms or terms used in recent literature?
- Has the controlled vocabulary changed for any key concepts?

### Step 4: Generate structured review

Output the review in the following format:

```
## PRESS 2015 Peer Review

**Query**: [query file name]
**Session**: [session ID if applicable]
**Date of review**: [date]
**Reviewer**: Claude (AI-assisted)

### Element-by-Element Assessment

#### 1. Translation of Research Question
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

#### 2. Boolean and Proximity Operators
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

#### 3. Subject Headings
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

#### 4. Text Word Search
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

#### 5. Spelling, Syntax, and Line Numbers
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

#### 6. Limits and Filters
- **Adequacy**: Adequate / Partially adequate / Inadequate
- **Findings**: [description]
- **Recommendations**: [if any]

### Overall Assessment
- **Recommendation**: Approve as-is / Revise and resubmit / Major revision required
- **Summary**: [overall summary of key strengths and concerns]
- **Priority changes**: [numbered list of most important changes, if any]
```

### Step 5: Save review to session notes

If `$ARGUMENTS` included a session ID, persist the review result so that `/develop-search-strategy` can pick it up:

```bash
search-hub notes assess <session-id> \
  --precision "<estimate>" \
  --verdict <good|refine|reject> \
  --comment "<summary of findings and priority changes>"
```

Map your Overall Assessment to a verdict:
- "Approve as-is" → `good`
- "Revise and resubmit" → `refine`
- "Major revision required" → `refine` (or `reject` if fundamentally flawed)

The `--comment` should include a concise summary of your Priority Changes list from Step 4. This text will be read by `/develop-search-strategy` to guide refinement, so be specific about which concept blocks need changes and what terms to add/remove.

### Step 6: Suggest next steps

Based on the review:
- If approved: Confirm the search is ready for execution/screening
- If revisions needed: Suggest using `/develop-search-strategy resume <session-id>` to implement the recommended changes. The assessment saved in Step 5 will be automatically picked up.
- If major issues: Identify which concept blocks need the most work
