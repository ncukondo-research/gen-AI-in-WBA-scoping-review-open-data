# Open Data: AI-Enhanced Scoping Review of Generative AI in Workplace-Based Assessment

This repository provides the complete AI interaction audit trail for the scoping review:

> **Toward Responsible AI in Medical Education: An AI-Enhanced Scoping Review of the Application and Validity Evidence of Generative AI in Workplace-Based Assessment Using Downing's Framework**

The review employed AI tools (Claude Code with Claude Opus 4.6 via Anthropic API) at each stage of the review process, with transparent documentation of all AI interactions as specified in the study protocol. This repository fulfills the protocol's commitment to making AI prompts and output logs publicly available.

## Repository Structure

```
.
├── ai-skill-definitions/                  # AI prompt definitions (all phases)
│   ├── develop-search-strategy.md         # Iterative query development workflow
│   ├── press-review.md                    # PRESS 2015 peer review evaluation
│   └── validate-search.md                 # Search recall validation
│
├── 01-search-strategy-development/        # Search strategy development phase
│   ├── README.md                          # Detailed process documentation
│   ├── query-versions/                    # Query YAML files (v1 through v8)
│   ├── session-assessments.yaml           # Consolidated session metadata and notes
│   └── final-rendered-queries/            # Database-specific query strings (v8)
│
├── 02-screening/                          # Article screening phase (forthcoming)
│
└── 03-data-extraction/                    # Data extraction phase (forthcoming)
```

## How AI Was Used

AI tools were used throughout the review under human oversight, following the joint position statement by Cochrane, Campbell Collaboration, JBI, and the Collaboration for Environmental Evidence endorsing AI use in evidence synthesis.

### AI Tool Stack

| Component | Tool | Role |
|-----------|------|------|
| AI coding assistant | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Orchestration of all AI-assisted tasks |
| AI model | Claude Opus 4.6 (Anthropic) | Search development, PRESS review, screening, extraction |
| Search management | [Search-Hub](https://github.com/ncukondo/search-hub) | Multi-database query execution and session tracking |
| Reference management | [Reference-Manager](https://github.com/ncukondo/reference-manager) | Citation management and fulltext retrieval |

### Skill Definitions as AI Prompts

This review used Claude Code's "skill" system to define structured, reproducible AI workflows. Each skill is a Markdown file containing step-by-step instructions that Claude Code follows when invoked. These skill definitions serve as the functional equivalent of "AI prompts" and are the primary mechanism through which AI behavior was directed.

The skill definitions are provided in [`ai-skill-definitions/`](ai-skill-definitions/) and document:
- The exact instructions given to the AI at each step
- The CLI tools and commands the AI was permitted to use
- The decision criteria and output formats expected
- The workflow logic (iteration, branching, error handling)

### Human Oversight

All AI outputs were reviewed by human researchers before adoption:
- **Search strategy development**: Lead author (TK) reviewed and approved all query modifications
- **PRESS peer review**: Both AI-generated and human PRESS reviews were conducted
- **Co-author review**: Independent audit by information specialist (YK)

## Related Resources

- **Study Protocol**: [OSF registration] (link to be added)
- **Manuscript Repository**: (private during review; to be made public upon acceptance)
- **Search-Hub**: https://github.com/ncukondo/search-hub

## How to Navigate This Repository

1. **Start with the skill definitions** in [`ai-skill-definitions/`](ai-skill-definitions/) to understand what instructions the AI received
2. **Read the phase-specific README** (e.g., [`01-search-strategy-development/README.md`](01-search-strategy-development/README.md)) for a narrative account of the process
3. **Examine the raw data** (query YAMLs, session assessments) for the complete audit trail

## Citation

If you use these materials, please cite the associated manuscript:

> [Citation to be added upon publication]

## License

This repository is made available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
