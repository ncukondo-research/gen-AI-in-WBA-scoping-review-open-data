---
protocol-version: "3.4"
last-updated: 2026-02-17
---

# Title

Toward Responsible AI in Medical Education: An AI-Enhanced Scoping Review of the Application and Validity Evidence of Generative AI in Workplace-Based Assessment Using Downing's Framework

## Description

This scoping review maps and synthesizes the literature on the application of generative AI in workplace-based assessment (WBA) in medical education, using Downing's five sources of validity evidence (Content, Response Process, Internal Structure, Relationship to Other Variables, Consequences) as the organizing framework. The review examines what roles generative AI plays in WBA, which aspects of validity evidence the current literature addresses, and what methodological challenges and research gaps remain. As a distinguishing feature, the review process itself employs AI tools at each stage (search, screening, data extraction) with transparent documentation, serving as a practical example of responsible AI use in evidence synthesis.

## Protocol Registration

- Registration template: Generalized Systematic Review Registration Form
- Registry: Open Science Framework (OSF)
- OSF URL: https://osf.io/nux2e/
- Protocol version: 3.0
- Registration date: 2026-02-11
- Target discipline: Medical education / Health professions education

## Research Team

### Authors

1. Takeshi Kondo, MD, MHPE, PhD (Corresponding Author)
   - Center for Medical Education, Nagoya University Graduate School of Medicine, Nagoya, Aichi, Japan
   - The School of Health Professions Education, Maastricht University, Maastricht, The Netherlands
   - ORCID: 0000-0002-3307-671X
   - Email: ncukondo@gmail.com

2. Hiroshi Nishigori, MD, MMEd, PhD
   - Center for Medical Education, Nagoya University Graduate School of Medicine, Nagoya, Aichi, Japan
   - ORCID: 0000-0002-0715-7073

3. Seiko Miura, MD, PhD
   - Kanazawa Medical University, Ishikawa, Japan
   - ORCID: 0000-0002-4545-2671

4. Hiromu Yakura, PhD
   - Center for Humans and Machines, Max Planck Institute for Human Development, Berlin, Germany
   - ORCID: 0000-0002-2558-735X

5. Yuki Kataoka, MD, MPH, DrPH
   - Center for Postgraduate Clinical Training and Career Development, Nagoya University Hospital, Nagoya, Aichi, Japan
   - ORCID: 0000-0001-7982-5213

6. Jeroen Donkers, PhD
   - The School of Health Professions Education, Maastricht University, Maastricht, The Netherlands
   - Department of Educational Research and Educational Design, Maastricht University, Maastricht, The Netherlands
   - ORCID: 0000-0002-6769-0355

### Author Contributions (Provisional)

The following CRediT (Contributor Roles Taxonomy) assignments are provisional and will be confirmed by all team members prior to submission.

| Role                       | TK | HN | SM | HY | YK | JD |
|----------------------------|----|----|----|----|----|----|
| Conceptualization          | X  | X  |    |    |    | X  |
| Methodology                | X  |    |    |    | X  | X  |
| Software                   | X  |    |    |    |    |    |
| Validation                 |    | X  |    |    | X  | X  |
| Investigation              | X  |    | X  | X  |    |    |
| Data Curation              | X  |    | X  | X  |    |    |
| Writing (Original Draft)   | X  |    | X  | X  |    |    |
| Writing (Review & Editing) | X  | X  |    |    | X  | X  |
| Visualization              | X  |    |    |    |    |    |
| Supervision                |    | X  |    |    |    | X  |
| Project Administration     | X  |    |    |    |    |    |

TK = Takeshi Kondo, HN = Hiroshi Nishigori, SM = Seiko Miura, HY = Hiromu Yakura, YK = Yuki Kataoka, JD = Jeroen Donkers

## Ethics Statement

This scoping review synthesizes data from published literature and does not involve human participants, personal data, or primary data collection. Ethics approval is therefore not required.

## Review Methods

### Type of review

Scoping review, following the JBI methodology for scoping reviews [@Peters2020-qv] and the PRISMA-ScR reporting guideline [@tricco2018]. This review employs AI tools at each stage of the review process (search, screening, data extraction) with transparent documentation of all AI interactions, guided by the joint position statement by Cochrane, Campbell Collaboration, JBI, and the Collaboration for Environmental Evidence endorsing AI use in evidence synthesis under human oversight [@flemyng-2025]. This approach is supported by evidence demonstrating the feasibility of LLM-assisted screening [@oami-2024; @tran-2024] and data extraction [@Gartlehner2025-ky].

### Review stages

Preparation, Search Development, PRESS Peer Review, Pilot Screening (~10 records), Title Screening, Abstract Screening, Full-text Acquisition and Conversion, Full-text Screening, Pilot Extraction (~3 studies), Data Extraction, Human Verification, Narrative Synthesis, Reporting.

### Current review stage

Protocol development (pre-search). This is the initial preregistration.

### Start date

November 2025.

### End date

February 2026.

### Background

Competency-based medical education (CBME) has become the dominant paradigm in medical training, placing workplace-based assessment (WBA) at the center of learner evaluation [@masters-2025]. WBA encompasses a range of tools (e.g., Mini-CEX, DOPS, MSF, EPA) used to evaluate learners in authentic clinical environments. Unlike standardized assessments such as Objective Structured Clinical Examinations (OSCEs), which are conducted in simulated settings with predetermined scenarios, WBA occurs in real clinical contexts where patient presentations, clinical complexity, and learning opportunities vary unpredictably. This fundamental difference gives rise to challenges unique to WBA: clinical narratives, free-text comments, and observational notes generate unstructured data that are inherently more difficult to analyze than structured scoring rubrics; the variability of clinical contexts (specialty, acuity, patient complexity) introduces contextual diversity that complicates the standardization of assessment; and the need for longitudinal assessment over extended training periods demands consistency in evaluator judgments across time and settings.

Generative AI, particularly large language models (LLMs), has emerged as a promising approach to address these WBA-specific challenges. LLMs can process narrative assessment data, generate structured feedback from clinical observations, and potentially support consistency in assessment judgments across diverse clinical settings [@Gordon2024-fu]. Yet the evidence regarding the validity of AI-assisted assessments remains scattered across the literature. In this review, validity is understood following @Downing2003-hm as the degree to which evidence and theory support the interpretation of assessment scores or measures for their intended uses. Downing's five sources of validity evidence (Content, Response Process, Internal Structure, Relationship to Other Variables, Consequences) provide a systematic framework for organizing and evaluating such evidence.

A recent scoping review by @khan2025 used Kane's argument-based validity framework [@kane-2013] to map the evidence for generative AI in both OSCEs and WBA. However, further investigation is warranted for two reasons.

First, this field is evolving rapidly in step with advances in LLM capabilities, and new empirical studies continue to emerge. For example, recent work has compared AI-generated feedback with human tutor feedback in clinical education [@Ali2025-fd], introduced multimodal AI frameworks for competency-based assessment [@gershov-2026], and explored AI-augmented competence committees within CBME [@yasin-2026]. The literature published since @khan2025 needs to be captured in an updated synthesis. Notably, only two of the empirical studies included in @khan2025 fall within the scope of WBA as defined in the present review, highlighting the limited WBA-specific coverage in that earlier work. In addition, @khan2025 provided minimal methodological detail regarding search and screening procedures, making the completeness and reproducibility of their findings difficult to assess.

Second, the choice of validity framework shapes how evidence is organized and interpreted. @khan2025 adopted Kane's argument-based framework (scoring, generalization, extrapolation, implications), which is well suited to constructing validity arguments justifying score "use" within specific assessment programs. In contrast, Downing's five sources of validity evidence [@Downing2003-hm] may serve as a more appropriate classification framework for scoping reviews that aim to categorize and map evidence across the literature. In particular, issues specific to generative AI, such as the AI reasoning process (Response Process) and reproducibility (Internal Structure), can be more explicitly organized using Downing's framework.

### Primary research question(s)

This scoping review maps the literature to answer the following research questions (RQs):

RQ1: What roles (scoring, feedback generation, substitution for observation) does generative AI play in WBA?

RQ2: Which aspects of Downing's validity framework [@Downing2003-hm] (Content, Response Process, Internal Structure, Relationship, Consequences) does the current evidence address, and which aspects remain unexamined?

RQ3: What methodological challenges and research gaps in generative AI-assisted WBA have not been sufficiently addressed by the prior review using Kane's framework [@kane-2013; @khan2025]?

### Secondary research question(s)

No secondary research questions. All three research questions equally informed the review design.

### Expectations / hypotheses

Not applicable. As a scoping review, this study aims to map the breadth of available evidence rather than test specific hypotheses.

### Dependent variable(s) / outcome(s) / main variables

This review uses the PCC (Population, Concept, Context) framework rather than traditional independent/dependent variable categorization (see Inclusion and exclusion criteria for the PCC definitions).

The main variables of interest are the types and extent of validity evidence (mapped to Downing's five sources: Content, Response Process, Internal Structure, Relationship to Other Variables, Consequences) reported for generative AI applications in WBA.

### Independent variable(s) / intervention(s) / treatment(s)

Generative AI tools and models (e.g., ChatGPT, GPT-4, LLaMA, Gemini) applied to WBA tasks, including their specific roles (scoring, feedback generation, observation substitution) and implementation characteristics (prompt design, model version).

### Additional variable(s) / covariate(s)

WBA tool type (e.g., Mini-CEX, DOPS, MSF, EPA), clinical setting and specialty, participant characteristics (training level, profession), and study design (quantitative, qualitative, mixed methods).

### Software

Search: Search-Hub (https://github.com/ncukondo/search-hub) with Anthropic Claude Opus 4.6.
Screening: Anthropic Claude Opus 4.6 and OpenAI gpt-5.3-codex (via Codex CLI).
Full-text conversion: Docling v2.63.0 (PDF to Markdown); academic-fulltext (https://github.com/ncukondo/academic-fulltext) (PMC XML to Markdown).
Data extraction: Codex CLI (OpenAI GPT-5.3-Codex) for extraction; Claude Code (Anthropic Claude Opus 4.6) with Agent Teams feature for multi-perspective review.
Reference management: reference-manager (https://github.com/ncukondo/reference-manager).

### Funding

This work was supported by JSPS KAKENHI Grant Number 25K06542 and by Near-peer teaching in community oriented medical education based on Onsite and Virtual learning Integrated with Anthropology (NOVI+A), which is supported by the MEXT project, "Establishing Bases for Fostering Medical Personnel in the Post-COVID Era Project."

### Conflicts of interest

TK is the developer of Search-Hub, the search software used in this study, and reference-manager, the reference management software used in this study. These potential conflicts are mitigated by transparent documentation of all search and reference management processes and by independent peer review of search strategies by co-authors. All other authors declare no conflicts of interest.

### Overlapping authorships

TK and HN are co-authors of a study [@Kondo2025-jx] that may meet the inclusion criteria of this review. To mitigate potential bias, screening and data extraction for this study will follow the same AI-led procedures applied to all other studies. TK's final verification of AI-extracted data for this study will be independently checked by a co-author (YK) who is not an author of the study in question.

## Search Strategy

The use of AI tools throughout the search process is guided by principles from the joint position statement by Cochrane, Campbell Collaboration, JBI, and the Collaboration for Environmental Evidence [@flemyng-2025], which endorse AI in evidence synthesis under transparency and human oversight.

### Databases

The following databases will be searched (timeframe: 2022 to present, focusing on the period since the rise of generative AI). To support a rapid review, the search is limited to English-language articles.

1. PubMed: Comprehensive coverage of medicine and biomedical sciences.
2. Scopus: Interdisciplinary coverage (intersection of medicine and education).
3. arXiv: Capture of the latest research through preprints.
4. ERIC: Comprehensive coverage of education sciences.

### Interfaces

1. PubMed: NCBI E-utilities API (via Search-Hub).
2. Scopus: Scopus Search API (via Search-Hub).
3. arXiv: arXiv API (via Search-Hub).
4. ERIC: ERIC API (via Search-Hub).

### Grey literature

No separate grey literature search strategy is employed. However, the inclusion of arXiv captures preprints not yet indexed in peer-reviewed databases.

### Inclusion and exclusion criteria

The PCC (Population, Concept, Context) framework is used to establish the inclusion and exclusion criteria.

Participants: Medical students, residents/fellows, and physicians.

Concept:
- Target technologies: Generative AI, large language models (LLMs: ChatGPT, GPT-4, LLaMA, etc.), multimodal models (Gemini, GPT-4V, etc.). Studies limited to conventional machine learning (e.g., traditional NLP, predictive models) are excluded.
- Target activities: Assessment, feedback, and analysis of observation records. Assessments conducted entirely in simulated environments, such as OSCEs (Objective Structured Clinical Examinations), are excluded (see Background for rationale).
- Key outcomes: Studies must include data on at least one of the following: (a) validity evidence (e.g., content alignment, response process documentation, internal consistency, correlation with human judgments); (b) reliability (e.g., reproducibility of AI outputs, inter-rater agreement between AI and human assessors); (c) acceptability (e.g., learner or faculty perceptions, satisfaction, trust); or (d) educational impact (e.g., effects on learner performance, feedback uptake, assessment practices). Studies that solely describe AI tool design or capabilities without reporting empirical data on these outcomes will be excluded.
- Study types: Original research articles (quantitative, qualitative, mixed methods), systematic reviews, meta-analyses, and preprints. Conference abstracts and editorials are excluded.

Context: Workplace-based assessment (WBA) and related clinical education settings. Examples include Mini-CEX, DOPS, MSF (360-degree evaluation), EPA (Entrustable Professional Activities) assessments, and chart (medical record) evaluation. Fully laboratory-based written examinations (e.g., MCQ generation) are excluded; tasks close to clinical reasoning and practice are prioritized.

### Query strings

At the protocol stage, the search strategy is presented at the conceptual level. Fully optimized search strings for each database will be published as an appendix to the final manuscript.

The search concepts, derived from the PCC framework (see Inclusion and exclusion criteria), are structured along the following three axes:

Concept 1 (Generative AI): "Generative AI" OR "Large Language Models" OR "ChatGPT" OR "GPT-4" OR "Artificial Intelligence"
Concept 2 (Medical education): "Medical Education" OR "Clinical Education" OR "Graduate Medical Education" OR "Residency" OR "Undergraduate Medical Education"
Concept 3 (Workplace-based assessment): "Workplace-based assessment" OR "WBA" OR "Clinical assessment" OR "Feedback" OR "Mini-CEX" OR "DOPS" OR "Entrustable Professional Activities" OR "EPA"

The final search strings will combine controlled vocabulary (e.g., MeSH) and free-text terms (synonyms, abbreviations, truncation, etc.) for each concept, linked with AND across concepts.

Search strings will be developed with AI assistance and confirmed through human review. AI (Anthropic Claude Opus 4.6) will assist in identifying synonyms, abbreviations, and controlled vocabulary terms; the lead author (TK) will verify all AI-suggested terms to mitigate the known risk of LLM-fabricated controlled vocabulary [@qureshi-2023] and finalize the search strings. The MeSH hierarchy will be reviewed and adjusted as needed, moving to broader or narrower headings based on retrieval results and supplementing with free-text terms for concepts not adequately captured by available controlled vocabulary. Search strings will be iteratively refined, prioritizing sensitivity (recall). After each modification, the lead author will review changes in retrieved results to ensure that potentially relevant studies are not inadvertently excluded.

The finalized search strategy will be peer-reviewed based on the PRESS 2015 Evidence-Based Checklist [@McGowan2016-en]. The entire search development process, including AI outputs and human decisions, will be documented in detail in the supplementary materials to ensure transparency (see Supplementary File: Search Development Log).

### Search validation procedure

External validation and pearl growing will be conducted using the reference list of the most closely related prior review [@khan2025] as a starting point. From the references cited in @khan2025, original empirical studies that fall within the scope of the present review (WBA, narrative feedback in clinical settings, or clinical note assessment using generative AI) will be identified as seed articles. References that are exclusively about OSCE (conducted entirely in simulated environments), methodological/framework papers, guidelines, policy documents, commentaries, and reviews will be excluded. The lead author (TK) will make the final determination of the seed article set, with rationale documented for each inclusion/exclusion decision. Pearl growing will then be conducted from these seed articles:

1. Backward citation tracking: The reference lists of seed articles will be reviewed to identify additional relevant studies not captured by the database search.
2. Forward citation tracking: Articles that cite the seed articles will be identified (using citation databases) to capture recent relevant studies.
3. Capture rate assessment: The finalized database search results will be checked against the seed article set to determine capture rate (number of seed articles retrieved / total seed articles). Any seed articles not captured by the database search will be examined to identify potential gaps in the search strategy (e.g., missing synonyms, overly restrictive filters). If the analysis reveals systematic gaps, the search strings will be revised accordingly and the search will be re-run. If non-captured studies fall outside the search's date range or database coverage, this will be documented as a known limitation rather than a search strategy deficiency.

The seed article set (with inclusion/exclusion rationale for each reference), capture rate, pearl growing results, and any resulting search modifications will be reported in the supplementary materials.

### Other search strategies

In addition to the database search, supplementary identification of studies will be conducted through the following methods:

1. Pearl growing / citation tracking: As described in the Search validation procedure, backward and forward citation tracking from seed articles (identified from @khan2025) will be conducted to identify relevant studies not captured by the database search.
2. Inclusion of studies from prior review: From the included studies of @khan2025, those that fall within the scope of the present review (WBA-focused studies) will be directly incorporated. These studies will be recorded in the PRISMA flow diagram under "Identification via other methods."

Studies identified through these supplementary methods will undergo the same screening process as database-identified studies.

### Procedures to contact authors

Contacting authors of included studies for additional data is not planned. If critical information is missing from a published report, the item will be coded as "not reported" in the data charting form.

### Results of contacting authors

Not applicable. No author contact is planned (see Procedures to contact authors).

### Search expiration and repetition

The database search will be conducted once at the time of the review. If a substantial delay (more than 6 months) occurs between the initial search and manuscript submission, the search will be updated to capture newly published studies. No living review process is planned.

### Search strategy justification

The search strategy balances comprehensiveness with pragmatic feasibility. Four databases (PubMed, Scopus, arXiv, ERIC) were selected to cover the core domains of medicine, education, and emerging preprint research. The exclusion of other databases (e.g., Embase, CINAHL, PsycINFO) is acknowledged as a limitation (see Limitations in Other Information). The PRESS peer review process provides quality assurance for the search strings. The choice to limit the search to English-language articles from 2022 onward reflects the focus on generative AI (which emerged in late 2022) and the scope of a rapid review. Author contact was not planned because the review extracts data from published reports only, and missing items are coded as "not reported" (see Missing data).

### Miscellaneous search strategy details

No additional details.

## Screening

### Screening stages

Title screening, abstract screening, and full-text screening (three sequential stages with progressively detailed assessment).

Before screening, duplicates will be removed using DOI and title/author matching.

1. Title screening: Two AI models (Anthropic Claude Opus 4.6 and OpenAI gpt-5.3-codex) will independently screen all records based on titles. AI reviewer performance will first be calibrated on a pilot sample of ~50 randomly selected records: TK will compare AI screening results against human judgments and refine prompts as needed. Once screening performance is deemed acceptable by TK and a co-author (YK), full screening will proceed. In the full screening, a liberal (inclusive) approach will be applied: only records excluded by both AI models will be excluded, and all other records (i.e., those included by at least one model) will advance to the next screening phase. TK will then review all excluded records and either confirm or override each exclusion decision. Screening will be performed by AI supervised by a human.
2. Abstract screening: Two AI models will independently screen all remaining records based on titles and abstracts. AI reviewer performance will first be calibrated on a pilot sample of ~20 randomly selected records, with TK refining prompts and TK and YK approving performance before full screening. In the full screening, the same liberal approach will be applied: only records excluded by both AI models will be excluded, and all other records will advance to the next screening phase. TK will then review all excluded records and either confirm or override each exclusion decision. Screening will be performed by AI supervised by a human.
3. Full-text acquisition and conversion: Full texts will be obtained and converted to Markdown format prior to AI processing. Prior research has demonstrated that LLM accuracy for data extraction is substantially higher with text input than with direct PDF input [@konet-2024]. For articles available in PubMed Central (PMC) with XML, the XML will be parsed and converted to Markdown. For articles obtained as PDF, Docling (v2.63.0) will be used for conversion. A human reviewer (TK) will visually inspect all converted documents for quality assurance before proceeding.
4. Full-text screening: Two AI models will independently screen all remaining records based on the full texts converted to Markdown. AI reviewer performance will first be calibrated on a pilot sample of up to 5 randomly selected records, with TK refining prompts as needed. Once screening performance is deemed acceptable by TK and YK, full screening will proceed. After full screening, TK will review all results: confirm inclusion decisions, resolve divided cases (disagreement between the two AI models), and resolve conflicts in exclusion reasons where the two models cite different grounds for exclusion. Screening will be performed by AI supervised by a human.

The selection process will be recorded using a PRISMA flow diagram, including both the database identification pathway and the "Identification via other methods" pathway for studies identified through citation tracking and the prior review [@khan2025].

### Screened fields / blinding

At the title screening stage, only titles will be presented to AI reviewers. At the abstract screening stage, titles and abstracts will be presented. At the full-text screening stage, full texts converted to Markdown will be presented. No masking of author names, journal names, or other bibliographic fields will be applied, as this is a scoping review without quality assessment.

### Used exclusion criteria

The following exclusion criteria will be applied during screening (derived from the Inclusion and exclusion criteria):

1. Not about generative AI or LLMs (studies limited to conventional machine learning, traditional NLP, or predictive models)
2. Not about assessment, feedback, or analysis of observation records
3. Assessment conducted entirely in simulated environments (e.g., OSCEs)
4. Not in a workplace-based or clinical education setting
5. No data on validity, reliability, acceptability, or educational impact
6. Participants are not medical learners
7. Not an original research article, systematic review, meta-analysis, or preprint (conference abstracts and editorials are excluded)
8. Published before 2022
9. Not in English

### Screener instructions

AI reviewers will receive structured prompts based on the PCC eligibility criteria (see Inclusion and exclusion criteria). Prompts will be piloted on a small sample and refined based on agreement with human judgments before full screening. Final prompts will be published as supplementary materials.

### Screening reliability

At each screening stage, two AI models (Anthropic Claude Opus 4.6 and OpenAI gpt-5.3-codex) will independently screen all records. The two models will serve as independent screeners. AI reviewer performance will first be evaluated against human judgments on a pilot sample, and prompts will be refined as needed before full screening.

### Screening reconciliation procedure

For title and abstract screening, a liberal (inclusive) approach will be applied: records will be excluded only when both AI models agree on exclusion. In cases of disagreement (one model includes, the other excludes), the record will advance to the next phase. TK will review all excluded records and either confirm or override each exclusion decision; TK's decision will be final. For full-text screening, both AI models will independently screen all records, and TK will review all results: confirming inclusion decisions, resolving divided cases (disagreement between the two models), and resolving conflicts in exclusion reasons. TK's decision will be final.

### Sampling and sample size

All sources identified through the screening procedure will be included. No sampling from the screened sources is planned.

### Screening procedure justification

The dual-AI plus human review approach was adopted to balance efficiency with rigor. Two independent AI models reduce the risk of model-specific biases, while human oversight ensures final decision quality. The three-stage screening process (title, abstract, full-text) follows standard systematic review practice and efficiently narrows the candidate set at each stage. The use of AI screeners is supported by evidence demonstrating the feasibility and performance of LLM-assisted screening [@oami-2024; @tran-2024; @nordmann-2025], and aligns with guidance from the joint position statement endorsing AI use in evidence synthesis under human oversight [@flemyng-2025].

### Data management and sharing

All screening decisions (include/exclude with reasons) from both AI models and the human reviewer will be recorded and made available in JSON/YAML/CSV/Markdown format via the OSF project page upon completion of the review.

### Miscellaneous screening details

No additional details.

## Extraction

### Entities to extract

The following entities will be extracted from each included source:

1. Basic information: Authors, year, country, domain (specialty), participants.
2. Intervention details: AI model used (including version), presence/absence of prompts, AI role (rater vs simulated patient vs feedback generation).
3. Assessment tools: WBA tools covered (Mini-CEX, chart evaluation, etc.).
4. Mapping to Downing's validity evidence:
   (a) Content: Prompt quality and alignment with rubrics.
   (b) Response Process: AI reasoning process (chain-of-thought), presence/absence of hallucinations, data security/privacy.
   (c) Internal Structure: Reproducibility, inter-rater reliability (AI vs AI), bias and fairness (DIF-equivalent analysis).
   (d) Relationship to Other Variables: Agreement/correlation with humans (supervisors/experts).
   (e) Consequences: Learner performance improvement, acceptability of feedback.

### Extraction stages

Data extraction will follow an iterative extraction-review-revision cycle using two complementary AI systems:

- Extractor: Codex CLI (OpenAI GPT-5.3-Codex) will extract structured data from each full-text article according to the extraction codebook, which includes Downing's validity evidence mapping.
- Reviewers: The Agent Teams feature of Claude Code (Anthropic Claude Opus 4.6) will review the extracted data from multiple perspectives (e.g., validity evidence mapping, intervention details, methodological characteristics). Each reviewer will produce structured feedback identifying errors, omissions, or misclassifications.
- Revision cycle: Codex CLI will revise the extraction based on reviewer feedback. This extraction-review-revision cycle will repeat until all reviewers approve the extraction or a predefined maximum number of rounds is reached.

Data extraction will proceed through the following stages:

1. Pilot extraction (~3 included studies): The iterative extraction-review-revision cycle will be applied with human verification (TK) to optimize prompts, coding rules, and the data charting form. TK will approve the extraction quality before proceeding to full extraction. Extraction will be performed by AI supervised by a human.
2. Full extraction (all included studies): The optimized iterative cycle will be applied to all remaining studies using the refined prompts and coding rules. Extraction will be performed by AI supervised by a human.
3. Human verification (all studies): TK will verify all AI-extracted data against the original full-text articles. Discrepancies will be corrected by the human reviewer.

### Extractor instructions

Codex CLI will receive structured prompts specifying each entity to extract, with definitions and coding rules for each data charting item (the extraction codebook). Agent Teams reviewers will receive prompts specifying review criteria aligned with the codebook. Both extractor and reviewer prompts will be piloted on a small sample of included studies and refined based on accuracy against human judgments before full extraction. Final prompts, the extraction codebook, and the data extraction form will be published as supplementary materials via the OSF project page.

### Extractor masking

Not applicable. AI extractors will process the full text of each article without masking of author names, journal names, or other bibliographic information. This is consistent with scoping review methodology, which does not involve quality assessment where masking would be relevant.

To mitigate the risk of hallucination (AI-generated information not present in the source article), TK will monitor AI outputs throughout the iterative extraction-review-revision cycle and during the final human verification stage (Step 3 of Extraction stages). Because the iterative cycle with continuous human intervention makes it impractical to calculate a precise hallucination rate, significant hallucinations (fabricated data points, misattributed findings, or invented references) will instead be recorded with a description of each instance. These records will be reported as part of the transparency reporting of the AI-assisted review process.

### Extraction reliability

Data extraction will employ an iterative extraction-review-revision cycle: Codex CLI (GPT-5.3-Codex) will perform extraction, and the Agent Teams feature of Claude Code (multiple AI agents) will independently review each extraction from multiple perspectives. The cycle will repeat until all reviewers approve or a maximum number of rounds is reached. All AI-extracted data will be subsequently verified by a human reviewer (TK) against the original articles.

### Extraction reconciliation procedure

Discrepancies between AI-extracted data and the original articles, identified during human verification, will be corrected by the human reviewer (TK). The human reviewer's corrected values will be final.

### Extraction procedure justification

The iterative extraction-review-revision approach was chosen because data charting for this review requires complex, multi-dimensional judgments across Downing's validity framework. Codex CLI (GPT-5.3-Codex) performs the initial extraction, and the Agent Teams feature of Claude Code (Opus 4.6) provides multi-perspective review; the iterative cycle enables progressive refinement until reviewer consensus is reached. This is supported by evidence demonstrating the feasibility and accuracy of LLM-based data extraction [@gartlehner-2024; @Gartlehner2025-ky]. Full-text conversion to Markdown prior to extraction is based on evidence that text input yields higher AI extraction accuracy than direct PDF input [@konet-2024]. Human verification of all extracted data ensures accuracy.

### Data management and sharing

Completed data charting forms (CSV format), AI prompts used for extraction, and AI output logs will be made available via the OSF project page upon completion of the review.

### Miscellaneous extraction details

No additional details.

## Synthesis and Quality Assessment

### Planned data transformations

No quantitative data transformations or statistical conversions are planned. All synthesis will be narrative and descriptive, with tabular and visual summaries of the evidence map.

### Missing data

Where included studies do not report information relevant to a data charting item, the item will be coded as "not reported." No imputation or estimation of missing data will be performed. Patterns of missing or unreported information will be noted in the synthesis as potential gaps in the literature.

### Data validation

AI-extracted data will be verified by a human reviewer (TK) against the original full-text articles. Any discrepancies identified during verification will be corrected. Because the iterative extraction-review-revision cycle with continuous human intervention makes it impractical to calculate a precise error rate, significant discrepancies identified during human verification will be recorded with a description of each instance and reported as part of the transparency reporting of the AI-assisted review process.

### Quality assessment

Consistent with scoping review methodology [@tricco2018; @Peters2020-qv], individual study quality or risk-of-bias assessment will not be conducted. The objective is to map the breadth of evidence rather than to appraise its quality.

### Synthesis plan

Evidence will be classified by the five sources of Downing's validity framework and synthesized narratively. For each validity source, the review will summarize the types of studies, AI models used, WBA tools addressed, and key findings. Tabular and visual summaries (evidence maps) will be created to display the distribution of evidence across validity sources, AI roles, and WBA tools.

A separate narrative synthesis will address the AI-assisted review methodology, reporting the following:
- Comparison of AI PRESS review and human PRESS review results for the search strategy (points of agreement and disagreement).
- Agreement rates between AI models and between AI models and humans at each screening stage.
- Documentation of methodological challenges associated with AI use (hallucinations, reproducibility of judgments, etc.).
- Through the above, provide insights into the reliability and limitations of AI-assisted reviews.

No quantitative pooling of effect sizes is planned.

### Criteria for conclusions / inference criteria

Conclusions will be based on the patterns and gaps identified across the evidence map, organized by Downing's five validity sources. No statistical thresholds or minimum study counts are applied. Instead, conclusions will reflect the extent of coverage, consistency of findings, and areas where evidence is absent or limited.

### Synthesist blinding

Not applicable. Narrative synthesis will be conducted by the lead author (TK), who will be aware of the research questions and hypotheses. This is consistent with standard scoping review practice.

### Synthesis reliability

Narrative synthesis will be conducted by the lead author (TK) and reviewed by co-authors (HN, YK, JD). No independent parallel synthesis is planned.

### Synthesis reconciliation procedure

Disagreements between the lead author and co-reviewers regarding synthesis interpretations will be resolved through discussion until consensus is reached.

### Publication bias analyses

Not applicable. Assessment of publication bias (e.g., funnel plots) is not applicable in scoping reviews, as the objective is to map the breadth of evidence rather than to quantify pooled effect sizes.

### Sensitivity analyses / robustness checks

Not applicable. No quantitative pooling of effect sizes will be performed in this scoping review.

### Synthesis procedure justification

Narrative synthesis was chosen as this is a scoping review aimed at mapping the breadth of evidence rather than quantifying effect sizes. Downing's five sources of validity evidence provide a well-established organizational framework that aligns with the review's objectives. The additional transparency reporting of the AI-assisted review process is a methodological contribution that documents the reliability and limitations of AI tools in evidence synthesis. Co-author review of the synthesis provides quality assurance without the need for independent parallel synthesis, which is not standard practice in scoping reviews.

### Synthesis data management and sharing

Analysis notes, evidence map tables, and any visualization scripts will be made available via the OSF project page upon completion of the review.

### Miscellaneous synthesis details

No additional details.

## Other Information

### Limitations

- The search is limited to four databases (PubMed, Scopus, arXiv, ERIC) and does not include Embase, CINAHL, PsycINFO, or others. This may result in relevant literature from nursing and psychology domains being missed.
- The restriction to English-language articles excludes research published in other languages.
- The search period is limited to 2022 onward, excluding foundational research predating the rise of generative AI.
- The use of AI tools in the search, screening, and data extraction processes introduces limitations related to model-specific biases, prompt dependence, and reproducibility across model versions [@clark-2025; @oconnor-2024]. These risks are mitigated through the dual-AI and human review process, controlled vocabulary validation, and transparent documentation of all AI interactions.

### Timeline

| Milestone | Target Date | Responsible |
| --------- | ----------- | ----------- |
| Manuscript structure and section assignments | November 21, 2025 | TK |
| Section drafts completed | December 9, 2025 | TK, SM, HY |
| Integrated full draft | December 12, 2025 | TK |
| Senior review and feedback; methodology review | December 20, 2025 | JD, HN; YK |
| Revision incorporating feedback | January 12, 2026 | TK, SM, HY |
| Final review | January 14, 2026 | HN, YK, JD |
| Submission to Assessment & Evaluation in Higher Education | February 15, 2026 | TK |

### Data Availability Statement

Upon completion of the review, the following materials will be made publicly available as supplementary files or via the OSF project page:
- Final search strings for all databases
- Data charting forms (blank and completed)
- PRISMA-ScR flow diagram
- AI prompts used at each review stage (search, screening, data extraction)
- AI output logs documenting the review process

### Amendments

Any substantive amendments to this protocol made after OSF registration will be documented with the date, description of the change, and rationale. A table of amendments will be maintained and published alongside the final manuscript. Minor typographical or formatting corrections will not be recorded as amendments.

| Date | Version | Description | Rationale |
| ---- | ------- | ----------- | --------- |
| 2026-02-12 | 3.1 | Added external validation procedure to Search validation procedure using the reference list of Khan (2025) as a validation set | To strengthen search recall assessment by checking capture of known relevant studies from the most closely related prior scoping review, complementing the existing internal (diff-based) validation |
| 2026-02-13 | 3.2 | Revised based on co-author review (YK): restructured Background for unidirectional logic flow and updated novelty rationale; added validity definition; moved OSCE exclusion rationale to Background with detailed WBA-specific challenges; moved AI-as-methodology description from Background to Methods; narrowed participant scope to medical learners; added conference abstract exclusion; simplified search tool description; added pearl growing (backward/forward citation tracking) and Khan reference list incorporation as supplementary search strategies; updated PRISMA flow diagram to include other-methods pathway; added single-agent vs. multi-agent pilot comparison for extraction; added hallucination mitigation procedure; unified procedure tense to future | To address co-author review comments improving logical flow, methodological rigor, and clarity of novelty claims |
| 2026-02-13 | 3.3 | Further revisions based on co-author review (YK): added specific 2026 citations in Background to demonstrate emerging literature post-Khan; elaborated Key outcomes criteria with explicit definitions of validity evidence, reliability, acceptability, and educational impact; substantially simplified search tool description in protocol body and moved technical details (Search-Hub procedures, diff-based validation, PRESS peer review details) to supplementary file (supplementary-search-development.md); removed internal (diff-based) validation from protocol body; simplified Search strategy justification | To strengthen novelty claims with concrete examples, clarify inclusion criteria, and reduce protocol complexity by separating technical implementation details from methodological commitments |
| 2026-02-13 | 3.3 | Conducted forward citation tracking on seed articles (Kwan 2025, Burke 2024) from khan2025-validation-set. Kwan 2025: 0 citations (too recent). Burke 2024: 10 citing papers identified via Semantic Scholar API; 3 potentially in scope, of which 1 already captured by database search (10.2196/81718) and 2 not captured (10.1145/3712298, 10.1056/aics2400631). Results recorded in protocol/validation/khan2025-forward-citations.yaml. Two uncaptured papers added to reference library for screening via PRISMA "Identification via other methods" pathway | Execution of pearl growing / forward citation tracking procedure specified in protocol v3.2 Search validation procedure |
| 2026-02-17 | 3.4 | Updated Screening stages with detailed pilot calibration and reconciliation procedures: specified pilot sample sizes (~50 title, ~20 abstract, ~5 full-text) with TK and YK approval gates; title and abstract screening use liberal approach (exclude only when both AI models agree) with TK reviewing all exclusions; full-text screening adds TK review of inclusions, divided cases, and exclusion reason conflicts. Updated Extraction stages to describe iterative extraction-review-revision cycle: Codex CLI (GPT-5.3-Codex) extracts data per codebook, Agent Teams (Claude Code Opus 4.6) reviews from multiple perspectives, Codex revises until reviewers approve; pilot optimization with TK approval before full extraction. Updated Software to list both Codex CLI and Claude Code Agent Teams for data extraction. Replaced hallucination rate calculation with recording of significant hallucination instances, and replaced error rate calculation with recording of significant discrepancies, reflecting the impracticality of precise rate calculation under the iterative cycle with continuous human intervention. Removed single-agent vs. multi-agent pilot comparison | To document the implemented screening and extraction workflows with greater procedural specificity, and to align transparency reporting with the realities of the iterative human-in-the-loop process |

### License

This protocol is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/.

## References

::: {#refs}
:::
