from __future__ import annotations

import pandas as pd


STRICT_H1_STATUSES = {"eligible", "ineligible", "unresolved"}
QUANTITATIVE_STATUSES = {
    "strict_extracted",
    "native_extracted",
    "pending_alternative",
    "pending_sensitivity",
    "pending",
    "not_applicable",
}


def validate_adjudication_registry(df: pd.DataFrame) -> list[str]:
    required = {
        "adjudication_id",
        "study_id",
        "component",
        "strict_h1_status",
        "quantitative_status",
        "expected_effect_id",
        "timing_metric_type",
        "timing_analysis_class",
        "timing_domain",
        "effect_family",
        "reason",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        return [f"missing adjudication columns: {', '.join(missing)}"]

    errors: list[str] = []
    if df["adjudication_id"].duplicated().any():
        errors.append("duplicate adjudication_id detected")

    unknown_status = sorted(set(df["strict_h1_status"].dropna()) - STRICT_H1_STATUSES)
    if unknown_status:
        errors.append(f"unknown strict_h1_status: {unknown_status}")

    unknown_quant = sorted(set(df["quantitative_status"].dropna()) - QUANTITATIVE_STATUSES)
    if unknown_quant:
        errors.append(f"unknown quantitative_status: {unknown_quant}")

    for idx, row in df.iterrows():
        prefix = f"adjudication row {idx}"
        strict_extracted = row["quantitative_status"] == "strict_extracted"
        effect_id = "" if pd.isna(row["expected_effect_id"]) else str(row["expected_effect_id"]).strip()

        if strict_extracted and row["strict_h1_status"] != "eligible":
            errors.append(f"{prefix}: strict_extracted requires strict_h1_status=eligible")
        if strict_extracted and not effect_id:
            errors.append(f"{prefix}: strict_extracted requires expected_effect_id")
        if row["strict_h1_status"] == "ineligible" and strict_extracted:
            errors.append(f"{prefix}: ineligible component cannot be strict_extracted")
    return errors


def validate_effect_adjudications(
    effects: pd.DataFrame,
    adjudications: pd.DataFrame,
) -> list[str]:
    errors = validate_adjudication_registry(adjudications)
    if errors:
        return errors

    required_effect = {
        "effect_id",
        "study_id",
        "timing_metric_type",
        "timing_analysis_class",
        "timing_domain",
        "effect_family",
    }
    missing = sorted(required_effect - set(effects.columns))
    if missing:
        return [f"missing effect columns for adjudication validation: {', '.join(missing)}"]

    adjudicated_studies = set(adjudications["study_id"].astype(str))
    for idx, row in effects.iterrows():
        study_id = str(row["study_id"])
        if study_id not in adjudicated_studies:
            errors.append(
                f"effect row {idx} effect_id={row['effect_id']}: study {study_id} has no strict-H1 adjudication"
            )

    strict_rows = effects.loc[effects["timing_analysis_class"] == "strict_window"]
    strict_adjudications = adjudications.loc[
        adjudications["quantitative_status"] == "strict_extracted"
    ]

    by_effect = {
        str(row["expected_effect_id"]): row
        for _, row in strict_adjudications.iterrows()
    }

    fields = [
        "study_id",
        "timing_metric_type",
        "timing_analysis_class",
        "timing_domain",
        "effect_family",
    ]
    for idx, effect in strict_rows.iterrows():
        effect_id = str(effect["effect_id"])
        adjudication = by_effect.get(effect_id)
        if adjudication is None:
            errors.append(
                f"effect row {idx} effect_id={effect_id}: strict_window effect lacks an eligible strict_extracted adjudication"
            )
            continue
        if adjudication["strict_h1_status"] != "eligible":
            errors.append(
                f"effect row {idx} effect_id={effect_id}: adjudication is not eligible"
            )
        for field in fields:
            observed = "" if pd.isna(effect[field]) else str(effect[field])
            expected = "" if pd.isna(adjudication[field]) else str(adjudication[field])
            if observed != expected:
                errors.append(
                    f"effect row {idx} effect_id={effect_id}: {field}={observed} "
                    f"does not match adjudication {expected}"
                )

    effect_ids = set(effects["effect_id"].astype(str))
    for idx, adjudication in strict_adjudications.iterrows():
        expected_effect_id = str(adjudication["expected_effect_id"])
        if expected_effect_id not in effect_ids:
            errors.append(
                f"adjudication row {idx}: expected strict effect {expected_effect_id} is missing"
            )

    return errors
