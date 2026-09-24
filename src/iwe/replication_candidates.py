from __future__ import annotations

import pandas as pd


READY_VALUES = {"yes"}
CANDIDATE_STATUSES = {
    "ready",
    "blocked_summary_stats",
    "blocked_effect_form",
    "blocked_final_surface",
    "rejected_timing",
    "rejected_dependence",
    "rejected_other",
}


def validate_replication_candidates(df: pd.DataFrame) -> list[str]:
    required = {
        "candidate_id",
        "source_id",
        "plant_taxon",
        "animal_taxon",
        "target_class",
        "effect_family_target",
        "independent_programme",
        "timing_window_measured",
        "post_predation_final_reproduction",
        "smd_summary_stats",
        "status",
        "blocker",
        "priority",
        "notes",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        return [f"missing replication-candidate columns: {', '.join(missing)}"]

    errors: list[str] = []
    if df["candidate_id"].duplicated().any():
        errors.append("duplicate candidate_id detected")

    unknown = sorted(set(df["status"].dropna()) - CANDIDATE_STATUSES)
    if unknown:
        errors.append(f"unknown replication candidate status: {unknown}")

    for idx, row in df.iterrows():
        gates = {
            "independent_programme": str(row["independent_programme"]).strip().lower() == "yes",
            "timing_window_measured": str(row["timing_window_measured"]).strip().lower() == "yes",
            "post_predation_final_reproduction": str(
                row["post_predation_final_reproduction"]
            ).strip().lower() == "yes",
            "smd_summary_stats": str(row["smd_summary_stats"]).strip().lower() == "yes",
        }
        ready = all(gates.values())
        if row["status"] == "ready" and not ready:
            failed = [name for name, passed in gates.items() if not passed]
            errors.append(
                f"row {idx} candidate_id={row['candidate_id']}: ready candidate fails gates {failed}"
            )
        if ready and row["status"] != "ready":
            errors.append(
                f"row {idx} candidate_id={row['candidate_id']}: all four gates pass but status is {row['status']}"
            )
    return errors


def ready_replication_candidates(df: pd.DataFrame) -> pd.DataFrame:
    errors = validate_replication_candidates(df)
    if errors:
        raise ValueError("; ".join(errors))
    return df.loc[df["status"] == "ready"].copy().reset_index(drop=True)
