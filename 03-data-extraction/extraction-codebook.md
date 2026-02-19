# Data Extraction Codebook

Version: 1.6
Date: 2026-02-19
Revision: Split A4_study_design into A4a_data_collection (temporal data-collection frame) and A4b_analytical_approach (analytical methodology). Previous single-label design categories conflated data-collection timing with analytical approach.

This codebook defines all items to be extracted from each included study. Each item includes a definition, coding instructions, and examples. Extractors must follow these instructions exactly and report "Not reported" for any item where the information is absent or cannot be determined from the full text.


## General Instructions for Extractors

1. Source fidelity
   - Extract only information explicitly stated in the article. Do NOT infer, assume, or generate information not present in the text.
2. Missing data (non-D items)
   - If an item is not reported or cannot be determined, code it as `"Not reported"`. Do NOT leave fields blank or guess.
3. Missing data (D-category sub-items)
   - For D-category sub-items (D1b–D5d) where the validity evidence is absent, use the exact phrase `"No evidence reported"`. Do NOT use `"Not reported"` or `"No"` for D sub-items.
4. Categorical items with explicit options
   - For items that provide explicit categorical options including `"No"` (e.g., B3a, B3c), use `"No"` when the feature is confirmed absent, and `"Not reported"` when the article does not address the topic at all.
5. Ambiguous data
   - If information is present but ambiguous, code it as `"Unclear: [brief explanation]"`. Quote the relevant passage if possible.
6. Direct quotation
   - When extracting qualitative findings, key conclusions, or definitions, include brief direct quotes with page/section references where helpful.
7. Multiple values
   - Some items may have multiple values (e.g., multiple AI models used). List all values separated by semicolons.
8. Source verification
   - Before finalizing extraction, verify that every extracted data point can be traced to a specific passage in the full text. Flag any item you are uncertain about.
9. Abbreviation list
   - At the end of each extraction, compile a list of all abbreviations used in field values throughout the YAML output.
   - **Do NOT introduce new abbreviations.** Only use abbreviations that the source article itself uses. If the article writes a term in full (e.g., "electronic health record", "quality assurance"), do NOT replace it with an abbreviation (e.g., "EHR", "QA") in field values.
   - For each abbreviation, record the full spelling AS DEFINED IN THE ARTICLE. If the article uses an abbreviation but does not define it, code as: `"Not defined in text (likely: [probable full spelling])"`.
   - Do NOT include field-key prefixes (A1, B3a, D4b, etc.). Only list abbreviations that actually appear in both the source article and the values of the current extraction.

---

## Category A: Basic Study Information

### A1. Country / countries

- Definition
    - Country or countries where the study was conducted (i.e., where data were collected), NOT the authors' institutional affiliations.
- Coding
    - Use the country where clinical data or assessments originated. If multiple countries, list all. If the study uses a publicly available dataset without specifying the country of origin, code as `"Not reported (dataset-based study)"`.
- Example
    - `United States`, `Japan; United Kingdom`

### A2. Clinical domain / specialty

- Definition
    - The medical specialty or clinical domain in which the WBA takes place.
- Coding
    - Use standardized specialty names. If the study spans multiple specialties, list all. If a general/non-specialty-specific setting, code as `"General / non-specialty-specific"`.
- Examples
    - `Radiology`, `Surgery`, `Family Medicine`, `Emergency Medicine`, `Internal Medicine`, `General / non-specialty-specific`

### A3. Participants

- Definition
    - Description of the learners or clinicians whose assessment data were used.
- Sub-items
    - A3a. Participant type
        - Category of participant (e.g., medical students, residents, fellows, attending physicians).
    - A3b. Training level
        - Specific training level if reported (e.g., PGY-1, PGY-3, third-year medical students, junior residents).
    - A3c. Sample size (participants)
        - Number of participants whose assessment data were analyzed. If the study analyzes documents rather than individuals, report the number of documents (see A3d) and code participants as `"Not applicable (document-level analysis)"`.
    - A3d. Number of assessment records / documents
        - Total number of assessment entries, feedback narratives, reports, or other documents analyzed (if applicable).

### A4. Study design

Study design is captured along two orthogonal axes: temporal data-collection frame (A4a) and analytical approach (A4b).

#### A4a. Data collection

- Definition
    - The temporal frame or sampling strategy for data collection.
- Coding
    - Select the most appropriate:
        - `Prospective`
        - `Retrospective`
        - `Cross-sectional`

#### A4b. Analytical approach

- Definition
    - The primary analytical methodology employed.
- Coding
    - Select the most appropriate:
        - `Quantitative`
        - `Qualitative`
        - `Mixed methods`

### A5. Study aim / objectives

- Definition
    - The stated aim(s) or research question(s) of the study, in the authors' own words.
- Coding
    - Provide a concise summary (1–3 sentences). Include direct quotes where the aim is clearly articulated.

---

## Category B: Generative AI Intervention Details

### B1. AI model(s) used

- Definition
    - The specific generative AI model(s) or LLM(s) used in the study.
- Coding
    - Record exact model name and version as reported. If multiple models are compared, list all.
- Examples
    - `GPT-4 Turbo`, `GPT-3.5`, `ChatGPT (version not specified)`, `Claude-3.5 Sonnet`, `DeepSeek-R1`, `Google "Help me write"`
- Note
    - If the authors only mention a product name without specifying the underlying model version, record what is reported and add `"(version not specified)"`.

### B2. API vs. interface

- Definition
    - Whether the AI was accessed through an API (programmatic access) or a user-facing interface (e.g., ChatGPT web interface).
- Coding
    - `API`, `Web interface`, `Browser extension`, `Other: [describe]`, or `"Not reported"`.

### B3. Prompt design

- Definition
    - Whether prompts (instructions given to the AI) are described, and if so, the level of detail.
- Sub-items
    - B3a. Prompt reported
        - `Yes (full text provided)`, `Yes (summarized/paraphrased)`, `Partially (key elements described)`, `No`, or `Not applicable (non-generative model)`.
    - B3b. Prompt engineering techniques
        - Any reported techniques such as chain-of-thought, few-shot examples, role assignment, rubric inclusion, structured output format, etc. Code as `"Not reported"` if not mentioned. For studies using embedding/classification models rather than generative models, code as `"Not applicable (non-generative model)"` if no generative prompt was used.
    - B3c. Prompt iteration / refinement
        - Whether the authors report iterating or refining prompts. `Yes: [brief description]` or `No` or `"Not reported"` or `"Not applicable (non-generative model)"`.

### B4. AI role in WBA

- Definition
    - The primary function(s) the AI performs in relation to workplace-based assessment. This directly addresses RQ1.
- Coding
    - Select ALL that apply from the following categories. If a role does not fit these categories, describe it.
        - `Scoring / grading`: AI assigns scores, ratings, grades, or milestone levels to learner performance.
        - `Feedback generation`: AI generates written feedback for learners based on assessment data.
        - `Feedback analysis / coding`: AI analyzes, categorizes, or codes existing human-written feedback or narrative assessment data.
        - `Report comparison / discrepancy detection`: AI compares learner-generated reports with expert reports to identify differences.
        - `Clinical experience tracking`: AI analyzes learning logs or clinical records to track exposure and experience.
        - `Entrustment decision support`: AI supports entrustment or competency decisions.
        - `Observation substitution / simulation`: AI replaces or supplements human observation of clinical performance.
        - `Mindset language transformation`: AI modifies the language of feedback (e.g., converting fixed to growth mindset language).
        - `Other: [describe]`

### B5. Input data to AI

- Definition
    - What type of data is provided to the AI as input.
- Coding
    - Describe the input data type(s):
        - `Narrative feedback / free-text comments`
        - `Structured assessment scores + narrative`
        - `Clinical notes / medical records`
        - `Radiology reports (preliminary and/or final)`
        - `Learning logs / clinical experience records`
        - `Clinical scenarios / vignettes (constructed for the study)`
        - `Other: [describe]`

### B6. Output data from AI

- Definition
    - What the AI produces as output.
- Coding
    - Describe the output type(s):
        - `Numerical scores / ratings`
        - `Written feedback text`
        - `Categorization / classification labels`
        - `Structured report / summary`
        - `Identified discrepancies / errors`
        - `Competency mapping / milestone assignment`
        - `Other: [describe]`

### B7. Comparison / reference standard

- Definition
    - What the AI output is compared against to evaluate its performance.
- Coding
    - Describe the comparator(s):
        - `Expert human raters (number: [N])`: Human experts independently rate the same material as the AI
        - `Expert review of AI outputs (number: [N])`: Human experts review/validate AI-generated outputs (rather than independently rating the same inputs)
        - `Learner self-report (number: [N])`: Learners validate AI outputs against their own experience (note: weaker ground truth than expert raters)
        - `Faculty evaluations (existing)`: Pre-existing faculty ratings or assessments used as ground truth
        - `No comparator`: AI output is described but not formally compared
        - `Other AI model`: One AI model compared against another
        - `Other: [describe]`

### B8. Model customization

- Definition
    - Whether the AI model was used off-the-shelf or customized for the study.
- Coding
    - `Off-the-shelf (no customization)`
    - `Fine-tuned: [brief description of fine-tuning data/approach]`
    - `RAG (Retrieval-Augmented Generation): [brief description]`
    - `Custom training: [brief description]`
    - `Not reported`

---

## Category C: Assessment Tools and Context

### C1. WBA tool(s) covered

- Definition
    - The specific workplace-based assessment instrument(s) or methods involved.
- Coding
    - Select ALL that apply, or describe if not listed:
        - `Mini-CEX (Mini Clinical Evaluation Exercise)`
        - `DOPS (Direct Observation of Procedural Skills)`
        - `MSF / 360-degree evaluation`
        - `EPA (Entrustable Professional Activities)`
        - `Chart / medical record evaluation`
        - `Radiology report review`
        - `Operative / procedural notes review`
        - `Clinical learning logs / portfolios`
        - `In-training examination (workplace-linked)`
        - `Narrative feedback forms (general / institution-specific: [name if given])`
        - `Milestone assessment (ACGME or equivalent)`
        - `Competency committee review`
        - `Other: [describe]`

### C2. Assessment context

- Definition
    - The specific setting or workflow in which the assessment occurs.
- Coding
    - Free text description. Include whether the assessment is formative or summative (if stated), and the clinical context.
- Example
    - `"Formative feedback on preliminary radiology reports reviewed by attending radiologist next morning"`, `"Summative milestone assessment for family medicine residency semiannual review"`

---

## Category D: Mapping to Downing's Validity Evidence Framework

### Framework Adaptation Note

This codebook adapts Downing's (2003) five validity evidence sources for the
context of generative AI in workplace-based assessment. Where the original
framework was designed for traditional written and performance examinations,
this adaptation maps analogous concepts to AI-specific phenomena. Key
adaptations are annotated with "[Adaptation]" in each sub-item definition.
The mapping rationale is documented in protocol/protocol.md.

Instructions for Category D:

- For each of the five sources of validity evidence below, determine whether the study provides relevant evidence. This directly addresses RQ2.
- For each source:
    - First code `"Evidence present"` or `"No evidence"`.
    - If evidence is present, code the sub-item using the **structured format** described below.
    - If no evidence is present, code the sub-item as the scalar string `"No evidence reported"`.

It is critical to distinguish between:

- Evidence the study explicitly reports (even if the authors do not use the term "validity")
- Evidence that is absent/not examined in the study

#### Structured sub-item format

When a D sub-item (D1b–D5d) has evidence to report, use a three-field object instead of a flat string:

```yaml
D1b_prompt_rubric_alignment:
  approach: "Competency framework-aligned prompt design"
  key_finding: "AI prompt replicated faculty instructions using ACGME competency definitions"
  detail: "ChatGPT was given 'the same prompt given to faculty members' under Instructions,
    and faculty/artificial intelligence coding used ACGME core competency definitions
    adapted from NEJM language."
```

When no evidence is present, use a scalar string as before:

```yaml
D1b_prompt_rubric_alignment: "No evidence reported"
```

The three fields serve distinct purposes:

- **`approach`** (3–8 words): A short label describing *how* the evidence was obtained — the methodology or approach used. This categorizes the type of evidence concisely. See recommended vocabulary below each sub-item definition.
- **`key_finding`** (10–25 words): A single concise sentence summarizing *what was found* — the main result. This should be suitable for direct use in a summary table cell. Include key quantitative metrics where applicable. Do not begin with "The study..." or similar filler phrases.
- **`detail`**: The full narrative description as previously required. This preserves source-traceable evidence for supplementary materials and auditing. All existing coding rules (source fidelity, direct quotation, etc.) apply to this field.

### D1. Content validity evidence

- Definition
    - Evidence that the AI assessment adequately represents the construct being measured. This includes whether the AI prompts align with the assessment rubric, whether the AI's scoring criteria match the intended competency domains, and whether the content of AI-generated feedback is relevant and appropriate.
- What to look for
    - Was the prompt designed to align with a specific rubric or competency framework?
    - Did experts review the AI prompt or output for content appropriateness?
    - Was the AI's coverage of assessment domains evaluated?
    - Did the study assess whether AI-generated feedback addressed the correct competencies?
- Sub-items
    - D1a. Evidence present
        - `Yes` or `No`
    - D1b. Prompt-rubric alignment
        - How was the AI prompt designed in relation to the assessment rubric or competency framework? Was alignment checked? Summarize findings.
        - Recommended `approach` vocabulary: "Rubric-based prompt design", "Competency framework-aligned prompt design", "Task-specific prompt design", "Domain-specific prompt alignment"
    - D1c. Content coverage
        - Did the study evaluate whether the AI adequately covered the intended assessment domains or competencies? Summarize findings.
        - Recommended `approach` vocabulary: "Domain-specific coverage evaluation", "Competency distribution analysis", "Construct coverage assessment"
    - D1d. Expert review of content
        - Was expert review conducted on the AI's output for content validity? Describe the process and findings.
        - Recommended `approach` vocabulary: "Expert panel review", "Dual-rater review with reconciliation", "Single expert review", "Iterative expert consensus"

### D2. Response process validity evidence

- Definition
    - Evidence about the process by which the AI generates its responses, including transparency of AI reasoning, quality assurance of AI outputs, and data handling procedures.
- What to look for
    - Was chain-of-thought reasoning or explanation of AI decisions examined?
    - Was the presence or absence of hallucinations (fabricated information) reported?
    - Were data security or privacy considerations addressed?
    - Was the fidelity of the AI input data (e.g., quality of text conversion) verified?
    - Was there a description of quality control procedures for AI outputs?
- Sub-items
    - D2a. Evidence present
        - `Yes` or `No`
    - D2b. AI reasoning transparency
        - Did the study examine or report on the AI's reasoning process (e.g., chain-of-thought, rationale for scores)? Summarize findings.
        - [Adaptation]: Downing's original "response process" focused on data integrity and scoring quality control. AI reasoning transparency extends this concept to encompass the process by which AI generates its outputs.
        - Note: Using CoT prompting techniques is NOT sufficient for D2b; the study must examine or evaluate the quality of the AI's reasoning output. If CoT was used but not evaluated, code as: `"CoT prompting techniques used but reasoning quality not independently examined."`
        - Recommended `approach` vocabulary: "Reasoning quality evaluated", "CoT used but not evaluated"
    - D2c. Hallucination assessment
        - Did the study assess or report instances of AI-generated content not grounded in the source data (hallucinations/fabricated information)? Summarize findings including rates if reported.
        - Note: False-positive analysis (AI outputs not matching ground truth) may serve as an indirect hallucination proxy. If the study reports false positives but does not explicitly frame them as hallucination, code as `"Yes (indirect: false-positive analysis as proxy)"` and note the interpretive mapping in F3b. Apply this coding consistently across all studies.
        - Recommended `approach` vocabulary: "Direct hallucination assessment", "False-positive analysis as proxy", "Self-reported hallucination", "Content fabrication analysis"
    - D2d. Data security / privacy
        - Did the study address data security, patient privacy, or de-identification procedures related to AI processing? Summarize.
        - Recommended `approach` vocabulary: "De-identification procedures", "Secure/local processing", "Synthetic data used", "IRB-approved processing", "HIPAA-compliant environment"
    - D2e. Quality assurance procedures
        - Were procedures described for checking or ensuring the quality of AI outputs before use? Summarize.
        - Recommended `approach` vocabulary: "Expert output review", "Multi-step quality assurance", "Validation subset", "Algorithmic bias mitigation"

### D3. Internal structure validity evidence

- Definition
    - Evidence about the internal psychometric properties of AI assessment outputs, including reproducibility, consistency, reliability, dimensionality, and bias/fairness. Following Downing (2003, p.835), internal structure evidence encompasses all analyses that examine whether the measurement behaves as expected from its internal properties: reproducibility of scores, internal consistency, item/rater analysis, dimensionality, and differential item functioning (DIF) or equivalent bias analyses.
- What to look for
    - Was reproducibility of AI outputs tested (same input, multiple runs)?
    - Was inter-model agreement assessed (different AI models on same data)?
    - Was internal consistency of AI scoring reported?
    - Was the effect of temperature or other model parameters on consistency examined?
    - Were statistical measures of reliability reported (ICC, kappa, Cronbach's alpha)?
    - Was bias or fairness across demographic groups examined (DIF-equivalent analysis)?
    - Was the dimensionality of AI scoring examined?
- Threshold rule
    - Mentioning reproducibility as a model selection criterion or describing that models were "compared" without reporting quantitative reproducibility/reliability metrics does NOT meet the threshold for D3a = `Yes`. Code as `No` and note the qualitative mention under F2 (RQ3 relevance) as a gap in reproducibility reporting.
    - For D3f, merely noting that "bias was not examined" in the Discussion does NOT constitute evidence. Empirical subgroup analysis or DIF-equivalent testing is required for D3f to have reported evidence.
- Sub-items
    - D3a. Evidence present
        - `Yes` or `No`. Code as `Yes` if any sub-item (D3b–D3f) has empirical evidence.
    - D3b. Reproducibility (test-retest)
        - Was the same input processed multiple times to assess consistency? Report methodology and results (e.g., ICC values, percentage agreement across runs).
        - Requires quantitative metrics (ICC, kappa, percentage agreement, CV, etc.) to code as present.
        - Recommended `approach` vocabulary: "Repeated inference runs", "Test-retest with quantitative metrics"
    - D3c. Inter-model agreement
        - Were different AI models compared on the same data? Report which models and agreement metrics.
        - Recommended `approach` vocabulary: "Multi-model comparison with agreement metrics"
    - D3d. Internal consistency
        - Was internal consistency of AI scoring assessed? Report statistical measures.
        - Recommended `approach` vocabulary: "Internal consistency analysis"
    - D3e. Model parameter effects
        - Was the effect of model parameters (temperature, top-p, etc.) on output consistency examined? Summarize findings.
        - Recommended `approach` vocabulary: "Parameter sensitivity analysis"
    - D3f. Bias and fairness (DIF-equivalent)
        - Did the study examine whether AI assessment outputs differ systematically across demographic groups (gender, race/ethnicity, language background, training level) in a way that constitutes statistical bias? Report any DIF-equivalent analyses, subgroup comparisons of AI performance metrics, or systematic error patterns across groups. Summarize methodology and findings.
        - [Adaptation]: Downing (2003, p.835) explicitly places bias analyses (DIF) under internal structure. This item captures the *statistical detection* of bias in AI outputs; the *impact and consequences* of such bias on learners are captured under D5.
        - Recommended `approach` vocabulary: "Subgroup comparison", "Algorithmic bias testing and mitigation", "DIF-equivalent analysis"

### D4. Relationship to other variables (convergent/discriminant validity evidence)

- Definition
    - Evidence about the relationship between AI-generated assessments and other measures, particularly human expert assessments. This is the most common form of validity evidence in this literature and examines whether AI scores/judgments correlate with or agree with human expert judgments.
- What to look for
    - Was AI output compared to human expert ratings/assessments?
    - Were agreement metrics reported (Cohen's/Fleiss' kappa, ICC, Pearson/Spearman correlation, percentage agreement, sensitivity/specificity)?
    - Did the AI distinguish between different performance levels (discriminant ability)?
    - Were AI results compared to other established assessment tools?
- Sub-items
    - D4a. Evidence present
        - `Yes` or `No`
    - D4b. AI-human agreement
        - What level of agreement was found between AI and human assessments? Report the specific metrics used and their values (e.g., `kappa = 0.65`, `ICC = 0.78`, `percentage agreement = 85%`, `sensitivity = 79.2%`).
        - Note: If the study uses regression/correlation (e.g., OR, logistic coefficients) to relate AI outputs to human assessments rather than direct agreement metrics, this still qualifies as D4 evidence. Code as `"Yes (association/correlation, not direct agreement)"` and report the specific association metrics.
        - Recommended `approach` vocabulary: "Agreement metrics", "Association/correlation analysis", "Multi-metric agreement analysis"
    - D4c. Human raters
        - Who were the human comparators? (e.g., attending physicians, subject matter experts, trained raters). Report number of human raters and their qualifications.
    - D4d. Discriminant ability (known-groups validity)
        - Did the study assess whether AI could distinguish between different learner performance levels (e.g., high vs. low performers, different PGY levels)? Summarize findings.
        - [Adaptation]: This corresponds to known-groups validity evidence. Downing's original "divergent validity" (showing no correlation with unrelated constructs) is captured under D4e if applicable.
        - Recommended `approach` vocabulary: "Known-groups comparison", "Training-level differentiation", "Performance-level discrimination"
    - D4e. Comparison with other measures
        - Were AI assessments compared with other established assessment tools or outcomes? Summarize.
        - Recommended `approach` vocabulary: "Cross-instrument comparison"

### D5. Consequences validity evidence

- Definition
    - Evidence about the impact and consequences of using AI in assessment, including effects on learner performance, acceptability to stakeholders, and unintended consequences.
    - Note: Statistical detection of bias/fairness (DIF-equivalent analyses) is classified under D3f (Internal Structure) per Downing (2003). D5 captures the *downstream impact and consequences* of biased or unfair AI assessment on learners and programs.
- What to look for
    - Was the impact of AI-generated feedback on learner performance or behavior measured?
    - Were learner or faculty perceptions, satisfaction, or trust in AI assessment reported?
    - Were unintended consequences or risks identified?
    - Were implementation barriers or facilitators described?
    - Were consequences of biased AI assessment on learners or programs documented?
- Sub-items
    - D5a. Evidence present
        - `Yes` or `No`.
        - Threshold rule: For D5a to be `Yes`, at least one sub-item (D5b–D5d) must have empirical evidence. Discussion-only mentions of consequences without empirical data do NOT qualify; note such mentions under F2 instead.
    - D5b. Impact on learner performance
        - Did the study measure whether AI-based assessment improved learner performance, learning, or feedback uptake? Summarize findings.
        - Recommended `approach` vocabulary: "Pre-post comparison", "Self-reported learning impact", "Objective outcome measurement"
    - D5c. Stakeholder acceptability
        - Were learner or faculty perceptions of AI assessment reported? Summarize findings including any quantitative measures (e.g., Likert scale ratings, satisfaction percentages).
        - [Adaptation]: Stakeholder acceptability is not explicitly named in Downing (2003) but is included here as a consequential aspect relevant to AI assessment implementation.
        - Recommended `approach` vocabulary: "Student satisfaction survey", "Expert relevance rating", "Faculty acceptability survey", "Mixed stakeholder survey"
    - D5d. Unintended consequences
        - Were unintended consequences, risks, or ethical concerns of AI use in assessment identified or discussed based on empirical data? Summarize.
        - Recommended `approach` vocabulary: "Empirical risk identification", "Error pattern documentation", "Self-reported challenges"

### D_summary. Validity evidence profile

- Definition
    - A brief narrative summary of the overall validity evidence profile for this study, to facilitate cross-study synthesis.
- Format
    - List which validity sources have evidence (Primary/Secondary) and which are absent.
- Example
    - `"Primary: D4 (AI-human agreement with kappa/ICC); Secondary: D1 (prompt-rubric alignment), D2 (data security); Absent: D3 (no reproducibility data), D5 (no impact/acceptability data)"`

---

## Category E: Methodological Characteristics

### E1. Limitations acknowledged

- Definition
    - Key methodological limitations reported by the authors that are relevant to generative AI use in WBA.
- Coding
    - List the main limitations as bullet points. Focus on limitations related to:
        - AI model limitations (generalizability across models/versions, prompt dependence)
        - Data limitations (sample size, single institution, specific specialty)
        - Methodological limitations (lack of comparator, retrospective design)
        - Validity limitations (limited validity evidence collected)

### E2. Future research directions

- Definition
    - Specific future research recommendations stated by the authors.
- Coding
    - List as bullet points. Focus on recommendations related to AI in WBA.

### E3. Funding and conflicts of interest

- Definition
    - Reported funding sources and conflicts of interest relevant to AI tools.
- Coding
    - Summarize. If the authors report using a commercial AI tool and have industry affiliations, note this specifically.

---

## Category F: Additional Notes

### F1. Key findings summary

- Definition
    - A structured summary of the study's main findings relevant to generative AI in WBA.
- Sub-fields
    - `summary`: 1–2 sentences (15–40 words). State what the AI did (role) and the key quantitative or qualitative outcome. This text is used directly as a Table 1 cell, so it must be self-contained and concise. Do not begin with "The study..." or similar filler.
    - `detail`: 2–4 sentence narrative summary. Write in the extractor's own words, but ensure every claim can be traced to the source text. When restructuring from a prior flat-string format, preserve the original text verbatim.

### F2. Relevance to RQ3 (methodological challenges and research gaps)

- Definition
    - Any findings or observations relevant to RQ3, which asks about methodological challenges and research gaps not sufficiently addressed by the prior Kane-framework review (Khan 2025).
- Coding
    - Note any of the following if present:
        - Novel methodological approaches not covered in existing reviews
        - Challenges unique to generative AI (as opposed to traditional ML)
        - Evidence gaps that Downing's framework highlights but Kane's framework does not
        - Cross-cutting issues (e.g., reproducibility across model versions, prompt sensitivity)
    - If nothing specific is relevant, code as `"No additional observations"`.

### F3. Extractor confidence and flags

- Definition
    - The extractor's self-assessment of extraction quality for this article.
- Sub-items
    - F3a. Overall confidence
        - `High`, `Medium`, or `Low` with brief justification.
    - F3b. Items requiring verification
        - List any specific item codes (e.g., D2c, D4b) where the extracted information may need additional review, with a brief explanation of why.
    - F3c. Uncertain extraction flags
        - List any extracted items where the extractor is uncertain whether the information is truly present in the source text.

---

## Output Format

For each included study, the extraction output should be structured as a YAML document with the following structure:

```yaml
study_id: "[First author last name]-[year]"
extraction_date: "YYYY-MM-DD"
extractor: "[extractor identifier]"

# Category A: Basic Study Information
A1_country: ""
A2_specialty: ""
A3_participants:
  A3a_type: ""
  A3b_training_level: ""
  A3c_sample_size: ""
  A3d_num_documents: ""
A4_study_design:
  A4a_data_collection: ""    # Prospective / Retrospective / Cross-sectional
  A4b_analytical_approach: "" # Quantitative / Qualitative / Mixed methods
A5_study_aim: ""

# Category B: Generative AI Intervention Details
B1_ai_models: ""
B2_api_or_interface: ""
B3_prompt_design:
  B3a_prompt_reported: ""
  B3b_engineering_techniques: ""
  B3c_prompt_iteration: ""
B4_ai_role: ""
B5_input_data: ""
B6_output_data: ""
B7_comparator: ""
B8_model_customization: ""

# Category C: Assessment Tools and Context
C1_wba_tools: ""
C2_assessment_context: ""

# Category D: Downing's Validity Evidence
# Sub-items use structured format when evidence is present:
#   field:
#     approach: "short label (3-8 words)"
#     key_finding: "concise summary (10-25 words)"
#     detail: "full narrative description"
# When no evidence: field: "No evidence reported"
D1_content:
  D1a_evidence_present: ""
  D1b_prompt_rubric_alignment:        # structured or "No evidence reported"
    approach: ""
    key_finding: ""
    detail: ""
  D1c_content_coverage:
    approach: ""
    key_finding: ""
    detail: ""
  D1d_expert_review:
    approach: ""
    key_finding: ""
    detail: ""
D2_response_process:
  D2a_evidence_present: ""
  D2b_reasoning_transparency:         # structured or scalar (see special coding rules)
    approach: ""
    key_finding: ""
    detail: ""
  D2c_hallucination_assessment:
    approach: ""
    key_finding: ""
    detail: ""
  D2d_data_security:
    approach: ""
    key_finding: ""
    detail: ""
  D2e_quality_assurance:
    approach: ""
    key_finding: ""
    detail: ""
D3_internal_structure:
  D3a_evidence_present: ""
  D3b_reproducibility:
    approach: ""
    key_finding: ""
    detail: ""
  D3c_inter_model_agreement:
    approach: ""
    key_finding: ""
    detail: ""
  D3d_internal_consistency:
    approach: ""
    key_finding: ""
    detail: ""
  D3e_parameter_effects:
    approach: ""
    key_finding: ""
    detail: ""
  D3f_bias_fairness:
    approach: ""
    key_finding: ""
    detail: ""
D4_relationship_to_other_variables:
  D4a_evidence_present: ""
  D4b_ai_human_agreement:
    approach: ""
    key_finding: ""
    detail: ""
  D4c_human_raters: ""                # remains scalar (descriptive, not evidence)
  D4d_discriminant_ability:
    approach: ""
    key_finding: ""
    detail: ""
  D4e_comparison_other_measures:
    approach: ""
    key_finding: ""
    detail: ""
D5_consequences:
  D5a_evidence_present: ""
  D5b_learner_performance_impact:
    approach: ""
    key_finding: ""
    detail: ""
  D5c_stakeholder_acceptability:
    approach: ""
    key_finding: ""
    detail: ""
  D5d_unintended_consequences:
    approach: ""
    key_finding: ""
    detail: ""

# Category D Summary
D_summary: ""  # e.g., "Primary: D4 (AI-human agreement); Secondary: D1, D2; Absent: D3, D5"

# Category E: Methodological Characteristics
E1_limitations: ""
E2_future_research: ""
E3_funding_coi: ""

# Category F: Additional Notes
F1_key_findings_summary:
  summary: ""   # 15-40 words; AI role + key outcome; used directly in Table 1
  detail: ""    # 2-4 sentence narrative (preserve original text verbatim when restructuring)
F2_rq3_relevance: ""
F3_confidence:
  F3a_overall: ""
  F3b_items_for_verification: ""
  F3c_uncertain_flags: ""

# Abbreviations used in this extraction
abbreviations:
  EPA: "Entrustable Professional Activity"           # defined in article
  ICC: "Intraclass Correlation Coefficient"          # defined in article
  CoT: "Not defined in text (likely: Chain of Thought)"  # not defined in article
  # ... list all abbreviations appearing in field values above
```

---

## Coding Decision Rules

1. When a study uses multiple AI models
   - Create separate entries for B1 but report results in a single extraction form, noting per-model results in the relevant validity evidence sections.
2. When a study examines multiple WBA tools
   - List all in C1 and note which findings apply to which tool if results are reported separately.
3. Validity evidence classification
   - A study may not use the terminology of "validity evidence." The extractor must map the study's findings to Downing's categories based on the definitions above, regardless of the authors' own framing.
4. Systematic reviews included in scope
   - For systematic reviews or meta-analyses, extract the review-level information (number of included studies, synthesis findings) and note that individual study data are not extracted.
5. Threshold for "evidence present"
   - Code a validity source as having evidence present (`Yes`) only if the study reports empirical data or findings directly relevant to that source. Merely mentioning a concept in the Discussion without reporting data is NOT sufficient; however, note such mentions under F2 as relevant to research gaps.
6. D3 threshold (Internal Structure)
   - Mentioning reproducibility as a model selection criterion or describing that models were "compared" without reporting quantitative metrics (ICC, kappa, percentage agreement, etc.) does NOT meet the threshold for D3a = `Yes`. Code as `No` and note the qualitative mention under F2.
   - For D3f (bias/fairness), empirical subgroup analysis or DIF-equivalent testing with quantitative metrics is required; qualitative discussion of potential bias alone does not qualify.
7. D5a threshold (Consequences)
   - For D5a to be `Yes`, at least one sub-item (D5b–D5d) must contain empirical evidence. Discussion-only mentions belong in F2, not D5.
8. False positives as D2c evidence
   - When a study reports false-positive rates (AI outputs not matching ground truth) but does not explicitly frame them as hallucination, code D2c as `"Yes (indirect: false-positive analysis as proxy)"` and note the interpretive mapping in F3b. Apply this coding consistently across all studies.
9. D4 comparator quality notation
   - When coding D4c, note the type and strength of the human comparator. Expert raters independently evaluating the same material provide the strongest evidence. Learner self-correction or non-independent comparisons should be explicitly flagged as weaker ground truth.
10. Non-generative AI models
    - For studies using embedding or classification models (e.g., BERT, Universal Sentence Encoder) rather than generative LLMs, code B3 items as `"Not applicable (non-generative model)"` where no generative prompt was used. Note in F2 that this study's AI methodology differs from typical LLM-based approaches.
11. D3f vs D5 bias distinction
    - Statistical detection of bias in AI outputs (subgroup comparisons, DIF-equivalent analyses, systematic error patterns across demographic groups) belongs under D3f (Internal Structure). The downstream *impact and consequences* of biased AI assessment on learners or programs (e.g., documented harm, differential educational outcomes) belongs under D5. If a study reports both statistical bias detection and its consequences, code evidence under both D3f and D5.
12. Abbreviation list compilation
    - After completing all extraction fields, scan every field value and collect all abbreviations or acronyms used. Record each as a key-value pair under the `abbreviations` field.
    - **Source-fidelity rule**: Only list abbreviations that ALREADY APPEAR IN THE SOURCE ARTICLE (fulltext). Do NOT introduce new abbreviations that the article does not use. If the article writes "electronic health record" in full, do NOT abbreviate it to "EHR" in field values and then list "EHR" as an abbreviation. Use the same terminology as the source article.
    - For each abbreviation, check whether the full spelling is explicitly defined in the source article:
        - If defined in the article: record the full spelling as given in the article.
        - If NOT defined in the article but the abbreviation itself IS used in the article: code as `"Not defined in text (likely: [probable full spelling])"`. The "likely" annotation is provided for reader convenience but is clearly marked as not sourced from the article.
    - Include abbreviations from all domains when they appear in field values: medical (e.g., Mini-CEX, EPA, DOPS, MSF), statistical (e.g., ICC, DIF), technical (e.g., LLM, NLP, RAG, CoT, API), and study-specific terms.
    - Do NOT include: (a) field-key codes (A1, B3a, D4b, etc.), (b) abbreviations absent from the current extraction's field values, (c) product/model names that are not abbreviations (e.g., GPT-4), or (d) abbreviations introduced by the extractor that do not appear in the source article (e.g., WBA, QA, COI, DIF, PHI, EHR when the article only uses the spelled-out form).
    - Standard abbreviations (e.g., RCT, PGY) should be included only when they appear in the source article itself, not when introduced by the extractor as shorthand.
