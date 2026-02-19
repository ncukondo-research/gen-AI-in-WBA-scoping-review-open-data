#!/usr/bin/env python3
"""Validate extraction YAML files against codebook structure.

Usage:
    python validate_yaml.py <extraction-file>...
    python validate_yaml.py extraction/*/extraction-v*.yaml

Checks:
- Valid YAML syntax
- All required top-level fields present
- All D-category sub-items present
- D_summary consistency with D*a evidence_present fields
- Null-value phrasing conventions (D sub-items vs non-D items)

Exit code: 0 if all valid, 1 if any errors.
"""

import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = [
    "study_id", "extraction_date", "extractor",
    "A1_country", "A2_specialty",
    "A3_participants", "A4_study_design", "A5_study_aim",
    "B1_ai_models", "B2_api_or_interface", "B3_prompt_design",
    "B4_ai_role", "B5_input_data", "B6_output_data", "B7_comparator",
    "B8_model_customization",
    "C1_wba_tools", "C2_assessment_context",
    "D1_content", "D2_response_process", "D3_internal_structure",
    "D4_relationship_to_other_variables", "D5_consequences",
    "D_summary",
    "E1_limitations", "E2_future_research", "E3_funding_coi",
    "F1_key_findings_summary", "F2_rq3_relevance", "F3_confidence",
]

D_CATEGORY_SUBITEMS = {
    "D1_content": ["D1a_evidence_present", "D1b_prompt_rubric_alignment",
                    "D1c_content_coverage", "D1d_expert_review"],
    "D2_response_process": ["D2a_evidence_present", "D2b_reasoning_transparency",
                             "D2c_hallucination_assessment", "D2d_data_security",
                             "D2e_quality_assurance"],
    "D3_internal_structure": ["D3a_evidence_present", "D3b_reproducibility",
                               "D3c_inter_model_agreement", "D3d_internal_consistency",
                               "D3e_parameter_effects", "D3f_bias_fairness"],
    "D4_relationship_to_other_variables": ["D4a_evidence_present", "D4b_ai_human_agreement",
                                            "D4c_human_raters", "D4d_discriminant_ability",
                                            "D4e_comparison_other_measures"],
    "D5_consequences": ["D5a_evidence_present", "D5b_learner_performance_impact",
                         "D5c_stakeholder_acceptability",
                         "D5d_unintended_consequences"],
}

EVIDENCE_PRESENT_MAP = {
    "D1a_evidence_present": "D1",
    "D2a_evidence_present": "D2",
    "D3a_evidence_present": "D3",
    "D4a_evidence_present": "D4",
    "D5a_evidence_present": "D5",
}


def validate_file(filepath: Path) -> list[str]:
    errors = []

    # 1. YAML syntax
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Invalid YAML: {e}"]

    if not isinstance(data, dict):
        return ["YAML root is not a mapping"]

    # 2. Required top-level fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # 2b. A4_study_design structure (codebook v1.6: dict with A4a/A4b)
    a4 = data.get("A4_study_design")
    if a4 is not None:
        if isinstance(a4, dict):
            for sub in ("A4a_data_collection", "A4b_analytical_approach"):
                if sub not in a4:
                    errors.append(f"Missing sub-item: A4_study_design.{sub}")
            valid_a4a = {"Prospective", "Retrospective", "Cross-sectional"}
            valid_a4b = {"Quantitative", "Qualitative", "Mixed methods"}
            a4a_val = str(a4.get("A4a_data_collection", "")).strip()
            a4b_val = str(a4.get("A4b_analytical_approach", "")).strip()
            if a4a_val and a4a_val not in valid_a4a:
                errors.append(
                    f"A4_study_design.A4a_data_collection: unexpected value '{a4a_val}' "
                    f"(expected one of {sorted(valid_a4a)})"
                )
            if a4b_val and a4b_val not in valid_a4b:
                errors.append(
                    f"A4_study_design.A4b_analytical_approach: unexpected value '{a4b_val}' "
                    f"(expected one of {sorted(valid_a4b)})"
                )
        elif not isinstance(a4, str):
            errors.append(f"A4_study_design should be a mapping or string, got {type(a4).__name__}")

    # 3. D-category sub-items
    for parent, subitems in D_CATEGORY_SUBITEMS.items():
        parent_val = data.get(parent)
        if not isinstance(parent_val, dict):
            if parent in data:
                errors.append(f"{parent} should be a mapping, got {type(parent_val).__name__}")
            continue
        for sub in subitems:
            if sub not in parent_val:
                errors.append(f"Missing sub-item: {parent}.{sub}")

    # 4. D_summary consistency with evidence_present fields
    d_summary = data.get("D_summary", "")
    if isinstance(d_summary, str):
        for parent, subitems in D_CATEGORY_SUBITEMS.items():
            parent_val = data.get(parent, {})
            if not isinstance(parent_val, dict):
                continue
            ep_key = subitems[0]  # *a_evidence_present
            ep_val = str(parent_val.get(ep_key, "")).strip().lower()
            d_label = EVIDENCE_PRESENT_MAP[ep_key]

            if ep_val.startswith("yes") and f"absent: {d_label.lower()}" in d_summary.lower():
                errors.append(
                    f"D_summary inconsistency: {ep_key}='Yes' but D_summary lists {d_label} as Absent "
                    f"(codebook decision rule #13)"
                )
            if ep_val == "no" and f"secondary: {d_label.lower()}" in d_summary.lower():
                errors.append(
                    f"D_summary inconsistency: {ep_key}='No' but D_summary lists {d_label} as Secondary"
                )

    # 5. Null-value phrasing
    for parent, subitems in D_CATEGORY_SUBITEMS.items():
        parent_val = data.get(parent, {})
        if not isinstance(parent_val, dict):
            continue
        for sub in subitems[1:]:  # skip *a_evidence_present
            val = str(parent_val.get(sub, ""))
            if val.strip() == "Not reported":
                errors.append(
                    f"Null-value phrasing: {parent}.{sub} uses 'Not reported' "
                    f"instead of 'No evidence reported'"
                )

    # 6. Abbreviations field (codebook v1.5)
    abbrevs = data.get("abbreviations")
    if abbrevs is None:
        errors.append("Missing required field: abbreviations")
    elif not isinstance(abbrevs, dict):
        errors.append(f"abbreviations should be a mapping, got {type(abbrevs).__name__}")

    # 7. Deprecated fields (removed in codebook v1.5)
    for deprecated in ("doi", "published_year"):
        if deprecated in data:
            errors.append(f"Deprecated field present: {deprecated} (removed in codebook v1.5)")

    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    files = [Path(f) for f in sys.argv[1:]]
    total_errors = 0

    for filepath in files:
        if not filepath.exists():
            print(f"SKIP  {filepath} (not found)")
            continue

        errors = validate_file(filepath)
        if errors:
            print(f"FAIL  {filepath}")
            for e in errors:
                print(f"  - {e}")
            total_errors += len(errors)
        else:
            print(f"OK    {filepath}")

    print(f"\n{len(files)} files checked, {total_errors} errors")
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
