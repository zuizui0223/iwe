from __future__ import annotations

import pandas as pd


DEPENDENCY_STATUSES = {"confirmed", "unresolved"}


def validate_dependency_registry(df: pd.DataFrame) -> list[str]:
    required = {
        "study_id",
        "dependency_status",
        "required_dependence_id",
        "scope",
        "notes",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        return [f"missing dependency-registry columns: {', '.join(missing)}"]

    errors: list[str] = []
    if df["study_id"].duplicated().any():
        errors.append("duplicate study_id in dependency registry")

    unknown = sorted(set(df["dependency_status"].dropna()) - DEPENDENCY_STATUSES)
    if unknown:
        errors.append(f"unknown dependency_status: {unknown}")

    confirmed = df["dependency_status"] == "confirmed"
    missing_id = confirmed & (
        df["required_dependence_id"].isna()
        | (df["required_dependence_id"].astype(str).str.strip() == "")
    )
    if missing_id.any():
        studies = sorted(df.loc[missing_id, "study_id"].astype(str))
        errors.append(f"confirmed dependency rows missing required_dependence_id: {studies}")

    unresolved = df["dependency_status"] == "unresolved"
    has_id = unresolved & df["required_dependence_id"].notna() & (
        df["required_dependence_id"].astype(str).str.strip() != ""
    )
    if has_id.any():
        studies = sorted(df.loc[has_id, "study_id"].astype(str))
        errors.append(
            f"unresolved dependency rows must not pre-assign required_dependence_id: {studies}"
        )
    return errors


def validate_effect_dependency_assignments(
    effects: pd.DataFrame,
    dependency_registry: pd.DataFrame,
) -> list[str]:
    errors = validate_dependency_registry(dependency_registry)
    if errors:
        return errors

    required_effect = {"study_id", "dependence_id", "effect_id"}
    missing = sorted(required_effect - set(effects.columns))
    if missing:
        return [f"missing effect columns for dependency validation: {', '.join(missing)}"]

    confirmed = dependency_registry.loc[
        dependency_registry["dependency_status"] == "confirmed",
        ["study_id", "required_dependence_id"],
    ]
    lookup = dict(
        zip(
            confirmed["study_id"].astype(str),
            confirmed["required_dependence_id"].astype(str),
            strict=True,
        )
    )

    for idx, row in effects.iterrows():
        study_id = str(row["study_id"])
        required_id = lookup.get(study_id)
        if required_id is None:
            continue
        observed = str(row["dependence_id"]).strip()
        if observed != required_id:
            errors.append(
                f"row {idx} effect_id={row['effect_id']}: study {study_id} requires "
                f"dependence_id={required_id}, observed {observed}"
            )
    return errors
