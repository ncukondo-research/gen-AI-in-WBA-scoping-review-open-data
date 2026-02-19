---
name: develop-search-strategy
description: Iterative search query development workflow for systematic/scoping reviews using search-hub CLI. Develops, executes, assesses, and refines search queries until acceptable precision and recall are achieved.
argument-hint: [research topic, protocol reference, or "resume <session-id>"]
allowed-tools: Bash(search-hub *, ref *), Read, Write, Edit, Grep, Glob
---

# Develop Search Strategy

Topic/input: $ARGUMENTS

## Workflow

### Step 0: Check for resume mode

If `$ARGUMENTS` matches the pattern `resume <session-id>`:

1. Read the session's assessment notes:
   ```bash
   search-hub notes list <session-id> --json
   ```
2. Read the session metadata to find the query file used:
   - Read `search-sessions/<session-id>/session.yaml` and locate the `query.file` field
3. Read the original query YAML file and the protocol (`protocol/protocol.md`) to understand context

**If notes contain a verdict of `refine`**:
- Summarize the assessment rationale (from `--comment`) to the user (the specific issues and recommended changes)
- Skip directly to **Step 6** (Iterate), using the assessment rationale to guide refinement
- The new query version should reference the review findings in its `description` field (e.g., "v3: Refined based on PRESS review of session <id>: removed broad terms X, added specific terms Y")

**If notes contain a verdict of `good`**:
- Report that the session is already accepted and no refinement is needed
- Skip to **Step 8** (Final output)

**If no assessment notes exist**:
- Inform the user that no prior assessment was found for this session
- Offer to either run a fresh assessment (proceed from Step 4) or start a new search (proceed from Step 1)

If `$ARGUMENTS` does NOT match the resume pattern, proceed to Step 1 as normal.

### Step 1: Extract search concepts from protocol

Read the study protocol to identify:
- **PCC framework**: Population, Concept, Context
- **Target databases**: Which databases to search (check `.search-hub.toml` for enabled providers)
- **Date filters**: Publication year range
- **Language filters**: e.g., English only
- **Inclusion/exclusion criteria**: To inform exclude terms

```bash
# Check available databases
cat .search-hub.toml
```

Read `protocol/protocol.md` and any existing query files in `search-sessions/` to understand prior work.

### Step 2: Create initial query YAML

Generate a template with `query init`, then edit it based on the concepts from Step 1:

```bash
# Generate template
search-hub query init -o search-sessions/<descriptive_name>.yaml

# Edit the file: set name, description, concept blocks, filters
```

Key points for editing the template:
- Set `name` and `description` (include version notes)
- Create one block per concept (blocks are AND'd together)
- Within each block, terms are combined with the specified `operator` (usually OR)
- Add `mesh` / `eric` controlled vocabulary terms where appropriate
- Use `exclude` to filter out false matches from ambiguous terms
- Set `filters` (year range, language, etc.)
- Use `providers.<name>.replaces` to override specific blocks for a provider (e.g., simplified terms for arXiv)
- Use `providers.<name>.adds` to add provider-specific filters (see Step 7 for details)

After editing, validate and inspect the query file before executing:

```bash
# Validate syntax and controlled vocabulary
search-hub query validate search-sessions/<descriptive_name>.yaml

# Inspect how the query resolves per database (block replacements, added filters)
search-hub query inspect search-sessions/<descriptive_name>.yaml
```

### Step 3: Pre-check and execute search

Before downloading full results, verify that hit counts and content are reasonable.

#### 3a. Check hit counts

```bash
search-hub search search-sessions/<query-file>.yaml --count-only
```

Evaluate the counts per database:

- **Errors** (API failure, query syntax rejected by a provider): Note the error, check if it is a database-specific issue (see Step 7) or a query problem. If the query itself is flawed, record the reason in the query YAML `description` field and revise the YAML (return to Step 2).
- **Clearly too many** (e.g., thousands of hits suggesting overly broad terms): Record the reason in the query YAML `description` field, revise the YAML, and return to Step 2.
- **Clearly too few or zero**: Record the reason in the query YAML `description` field, revise the YAML, and return to Step 2.
- **Uncertain**: Proceed to 3b.
- **Acceptable**: Skip to 3c.

#### 3b. Preview titles (when counts alone are inconclusive)

```bash
search-hub search search-sessions/<query-file>.yaml --preview
```

This returns hit counts plus the first 5 titles per database, without creating a session. Inspect the titles for relevance:

- **Mostly irrelevant**: Record the reason in the query YAML `description` field (e.g., "v1: preview showed dental/nursing dominance, need tighter population terms"), revise the YAML, and return to Step 2.
- **Mostly relevant or mixed**: Proceed to 3c.

#### 3c. Execute full search

```bash
search-hub search search-sessions/<query-file>.yaml
```

Note the session ID from the output (format: `YYYYMMDD_name_hash`).

If a search is interrupted, resume it:
```bash
search-hub resume <session-id>
search-hub resume <session-id> --retry-failed  # retry failed databases
```

### Step 4: Review results

```bash
# View session summary with hit counts
search-hub summary <session-id>

# List article titles
search-hub results <session-id>

# Filter results by field (title, author, year, journal, source, etc.)
search-hub results <session-id> -q "source:pubmed"
search-hub results <session-id> -q "year:2024"

# Show results with abstracts for relevance assessment
search-hub results <session-id> --abstract
```

You can also read session files directly for detailed inspection:

- `search-sessions/<session-id>/session.yaml` for hit counts per database

Scan titles to estimate precision (proportion of relevant articles).

### Step 5: Record assessment

```bash
search-hub notes assess <session-id> \
  --precision "<estimate>" \
  --verdict <good|refine|reject> \
  --comment "<rationale>"
```

Provide structured assessment:
- **Precision estimate** (`--precision`): e.g., `~25-35%`
- **Verdict** (`--verdict`): `good` (proceed to screening), `refine` (iterate query), or `reject` (start over)
- **Rationale** (`--comment`): What is causing noise? What relevant articles might be missed?
- **Recall check**: Verify that known relevant articles from the protocol are captured (see below)

#### Recall check against known relevant articles

References cited in `protocol/protocol.md` are registered in the ref library. Pre-curated validation DOI lists are stored in `protocol/validation/`. Use them to verify recall:

```bash
# Check available validation sets
ls protocol/validation/*.txt

# Search for a known relevant article by topic or author
ref search "<topic or author>"

# Read fulltext as Markdown to inspect indexing terms and keywords
ref fulltext get --markdown --stdout <key>

# Check whether known articles appear in session results using search-hub check
search-hub check <session-id> --pmid "12345678,23456789"
search-hub check <session-id> --doi "10.xxxx/yyyy"

# Or search within results by author/title
search-hub results <session-id> -q "author:<surname>"
```

If known relevant articles are missing from the results, note them in the assessment rationale and address in Step 6.

### Step 6: Iterate if verdict is "refine"

If the verdict is `refine`:

1. Identify the source of noise (irrelevant articles) and potential recall gaps
2. Create a new query version file (e.g., `<name>_v2.yaml`)
   - Record the refinement rationale in the new file's `description` field (e.g., "v2: narrowed population terms to reduce nursing/dental noise identified in v1 assessment")
3. Validate and inspect the new query:
   ```bash
   search-hub query validate search-sessions/<name>_v2.yaml
   search-hub query inspect search-sessions/<name>_v2.yaml
   ```
4. Run Step 3a (`--count-only`) and 3b (`--preview`) to verify the refinement before full execution:
   ```bash
   # 3a: Check counts
   search-hub search search-sessions/<name>_v2.yaml --count-only
   # 3b: Preview titles if counts are uncertain
   search-hub search search-sessions/<name>_v2.yaml --preview
   ```
   If counts or preview titles indicate the revision is still inadequate, record the reason in the query YAML `description`, revise again (e.g., `_v3.yaml`), and repeat this step.
5. Execute full search (Step 3c) and compare sessions to verify refinement:
   ```bash
   search-hub search search-sessions/<name>_v2.yaml
   search-hub diff <session-id-v1> <session-id-v2>
   # --show removed  to review excluded articles
   # --show added    to review newly captured articles
   ```

Common refinement strategies:
- Remove overly broad MeSH headings that capture unwanted subtopics
- Add exclude terms for known noise categories
- Narrow keyword terms to more specific phrases
- Add or remove specific model/tool names

### Step 7: Handle database-specific issues

When a specific provider needs different query terms or additional filters (e.g., arXiv requires shorter queries due to URL length limits, or PubMed needs extra MeSH terms), use the `providers` section in the query YAML rather than creating separate query files.

#### `providers.<name>.replaces` — replace a query block for one provider

Use `replaces` to swap an entire query block (matched by `id`) with a simplified or customized version for that provider. The replacement block must include `field`, `terms`, and `operator`.

#### `providers.<name>.adds` — add provider-specific filters

Use `adds` to append extra filters (year range, language, publication types, categories, source types) that apply only to that provider.

#### Supported providers

`pubmed`, `scopus`, `eric`, `arxiv`, `wos`, `embase`

#### Example: simplify query blocks for arXiv

```yaml
query:
  - id: concept-ai
    field: title_abstract
    terms:
      keywords:
        - "generative artificial intelligence"
        - "large language model*"
        - "ChatGPT"
        - "GPT-4"
        # ... many terms ...
      mesh:
        - "Natural Language Processing"
    operator: OR

  - id: concept-education
    field: title_abstract
    terms:
      keywords:
        - "medical education"
        - "clinical education"
        # ... many terms ...
      mesh:
        - "Education, Medical"
    operator: OR

providers:
  arxiv:
    replaces:
      concept-ai:
        field: title_abstract
        terms:
          keywords:
            - "generative AI"
            - "large language model"
            - "LLM"
            - "ChatGPT"
            - "GPT-4"
        operator: OR
      concept-education:
        field: title_abstract
        terms:
          keywords:
            - "medical education"
            - "clinical education"
            - "medical student"
            - "residency"
        operator: OR
```

Use `search-hub query inspect` to verify how each provider resolves the query, including any replacements:

```bash
search-hub query inspect search-sessions/<query-file>.yaml
```

#### Fallback: separate query file and merge

If provider overrides are insufficient (e.g., the provider needs a fundamentally different query structure), create a separate query file and merge sessions as a last resort:

```bash
search-hub search search-sessions/<name>_<provider>.yaml
search-hub merge <session-id-1> <session-id-2> --name "<merged-name>"
```

### Step 8: Final output

When verdict is `accept` or `good`, report:

- **Accepted session ID**: The session to use for screening
- **Total hits**: Combined across all databases
- **Per-database breakdown**: Hits per database
- **Assessment summary**: Final precision estimate and rationale
- **Query file**: Path to the final query YAML
- **Iteration history**: Number of versions and key changes between them

## Notes

- Always check for existing query files before creating new ones
- Version query files descriptively (v1, v2, etc.) with change notes in the description field
- Keep a clear record of why each refinement was made
- Validate recall against known relevant articles when possible (use `/validate-search`)
- For PRESS peer review of the final strategy, use `/press-review`
