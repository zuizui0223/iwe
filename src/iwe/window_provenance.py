from __future__ import annotations

import pandas as pd


ALLOWED_WINDOW_BASIS = {
    "direct_adult_census",
    "trapping",
    "direct_visitation",
    "source_defined_visit_evidence",
    "explicit_overlap_metric",
    "experimental_partner_availability",
}

FORBIDDEN_WINDOW_BASIS = {
    "egg_receipt",
    "oviposition_success",
    "attack",
    "infestation",
    "larval_occupancy",
    "damage",
    "seed_predation",
}


def validate_strict_window_provenance(
    effects: pd.DataFrame,
    provenance: pd.DataFrame,
) -> list[str]:
    """Require every real strict-window effect to have admissible partner-window provenance."""
    required = {
        "effect_id",
        "study_id",
        "window_basis",
        "same_season",
        "source_id",
        "source_measurement",
        "notes",
    }
    missing = sorted(required - set(provenance.columns))
    if missing:
        return [f"missing strict-window provenance columns: {', '.join(missing)}"]

    errors: list[str] = []
    if provenance["effect_id"].astype(str).duplicated().any():
        errors.append("duplicate effect_id in strict-window provenance registry")

    blank_fields = ("effect_id", "study_id", "window_basis", "source_id", "source_measurement")
    for idx, row in provenance.iterrows():
        prefix = f"provenance row {idx}"
        for field in blank_fields:
            if pd.isna(row[field]) or not str(row[field]).strip():
                errors.append(f"{prefix}: {field} must be non-empty")

        basis = str(row["window_basis"])
        if basis in FORBIDDEN_WINDOW_BASIS:
            errors.append(
                f"{prefix}: forbidden partner-window basis {basis}; realized interaction "
                "outcomes cannot define strict partner availability"
            )
        elif basis not in ALLOWED_WINDOW_BASIS:
            errors.append(f"{prefix}: unknown window_basis={basis}")

        if str(row["same_season"]).lower() != "yes":
            errors.append(f"{prefix}: strict partner window must be same-season")

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
            f"missing effect columns for strict-window provenance validation: {', '.join(missing_effect)}"
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
        for _, row in provenance.iterrows()
    }
    strict_ids = set(strict["effect_id"].astype(str))

    for idx, effect in strict.iterrows():
        effect_id = str(effect["effect_id"])
        row = by_effect.get(effect_id)
        if row is None:
            errors.append(
                f"effect row {idx} effect_id={effect_id}: strict_window effect lacks "
                "strict partner-window provenance"
            )
            continue
        if str(row["study_id"]) != str(effect["study_id"]):
            errors.append(
                f"effect row {idx} effect_id={effect_id}: provenance study_id="
                f"{row['study_id']} does not match effect study_id={effect['study_id']}"
            )

    for idx, row in provenance.iterrows():
        effect_id = str(row["effect_id"])
        if effect_id not in strict_ids:
            errors.append(
                f"provenance row {idx}: effect_id={effect_id} is not a current real strict-window effect"
            )

    return errors
