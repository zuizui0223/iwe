from __future__ import annotations

import pandas as pd


ALLOWED_DESIGN_TYPES = {
    "experimental_individual_timing",
    "observational_individual_timing",
    "fixed_context_group_comparison",
}
ALLOWED_VARIANCE_INTERPRETATIONS = {
    "individual_effect_sampling",
    "source_model_sampling",
    "within_context_response_sampling",
}
ALLOWED_INFERENCE_SCOPE = {
    "experimental_manipulation",
    "descriptive_association",
}


def validate_strict_unit_provenance(
    effects: pd.DataFrame,
    units: pd.DataFrame,
) -> list[str]:
    """Validate unit semantics for every current real strict-window effect."""
    required = {
        "effect_id",
        "study_id",
        "design_type",
        "exposure_grain",
        "response_grain",
        "variance_interpretation",
        "inference_scope",
        "causal_claim_allowed",
        "notes",
    }
    missing = sorted(required - set(units.columns))
    if missing:
        return [f"missing strict unit provenance columns: {', '.join(missing)}"]

    errors: list[str] = []
    if units["effect_id"].astype(str).duplicated().any():
        errors.append("duplicate effect_id in strict unit provenance registry")

    for idx, row in units.iterrows():
        prefix = f"unit provenance row {idx}"
        for field in required - {"notes"}:
            if pd.isna(row[field]) or not str(row[field]).strip():
                errors.append(f"{prefix}: {field} must be non-empty")

        design = str(row["design_type"])
        variance = str(row["variance_interpretation"])
        scope = str(row["inference_scope"])
        causal = str(row["causal_claim_allowed"]).lower()

        if design not in ALLOWED_DESIGN_TYPES:
            errors.append(f"{prefix}: unknown design_type={design}")
        if variance not in ALLOWED_VARIANCE_INTERPRETATIONS:
            errors.append(f"{prefix}: unknown variance_interpretation={variance}")
        if scope not in ALLOWED_INFERENCE_SCOPE:
            errors.append(f"{prefix}: unknown inference_scope={scope}")
        if causal not in {"yes", "no"}:
            errors.append(f"{prefix}: causal_claim_allowed must be yes or no")

        exposure_grain = str(row["exposure_grain"])
        response_grain = str(row["response_grain"])
        if exposure_grain != response_grain:
            if variance != "within_context_response_sampling":
                errors.append(
                    f"{prefix}: nested/fixed-context response sampling must use "
                    "variance_interpretation=within_context_response_sampling"
                )
            if scope != "descriptive_association":
                errors.append(
                    f"{prefix}: exposure/response grain mismatch requires descriptive_association scope"
                )
            if causal != "no":
                errors.append(
                    f"{prefix}: exposure/response grain mismatch cannot authorize a causal claim"
                )

        if design == "experimental_individual_timing":
            if exposure_grain != response_grain:
                errors.append(
                    f"{prefix}: experimental individual timing requires aligned exposure/response grain"
                )
            if scope != "experimental_manipulation":
                errors.append(
                    f"{prefix}: experimental individual timing requires experimental_manipulation scope"
                )

    required_effect_cols = {
        "effect_id",
        "study_id",
        "evidence_tier",
        "timing_analysis_class",
        "source_id",
    }
    missing_effect = sorted(required_effect_cols - set(effects.columns))
    if missing_effect:
        return errors + [
            f"missing effect columns for strict unit provenance validation: {', '.join(missing_effect)}"
        ]

    real = effects.loc[
        ~effects["source_id"].astype(str).str.startswith("synthetic:")
    ].copy()
    strict = real.loc[
        (real["evidence_tier"].astype(str) == "A")
        & (real["timing_analysis_class"].astype(str) == "strict_window")
    ].copy()

    by_effect = {
        str(row["effect_id"]): row
        for _, row in units.iterrows()
    }
    strict_ids = set(strict["effect_id"].astype(str))

    for idx, effect in strict.iterrows():
        effect_id = str(effect["effect_id"])
        row = by_effect.get(effect_id)
        if row is None:
            errors.append(
                f"effect row {idx} effect_id={effect_id}: strict_window effect lacks unit provenance"
            )
            continue
        if str(row["study_id"]) != str(effect["study_id"]):
            errors.append(
                f"effect row {idx} effect_id={effect_id}: unit provenance study_id="
                f"{row['study_id']} does not match effect study_id={effect['study_id']}"
            )

    for idx, row in units.iterrows():
        effect_id = str(row["effect_id"])
        if effect_id not in strict_ids:
            errors.append(
                f"unit provenance row {idx}: effect_id={effect_id} is not a current real strict-window effect"
            )

    return errors
