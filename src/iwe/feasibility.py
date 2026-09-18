from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .schema import INTERACTION_TYPES


@dataclass(frozen=True)
class CommonScaleGate:
    programme_counts: dict[str, int]
    coverage_complete: bool
    cross_class_fit_allowed: bool
    primary_claim_gate: bool
    status: str


def common_scale_gate(
    df: pd.DataFrame,
    *,
    min_for_fit: int = 2,
    min_for_primary: int = 5,
) -> CommonScaleGate:
    """Gate cross-class modelling by independent programme counts, not row counts.

    These thresholds are IWE execution rules, not universal meta-analysis laws.
    """
    required = {"interaction_type", "dependence_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    unknown = set(df["interaction_type"].dropna()) - INTERACTION_TYPES
    if unknown:
        raise ValueError(f"unknown interaction_type: {sorted(unknown)}")

    counts = {
        interaction_type: int(
            df.loc[df["interaction_type"] == interaction_type, "dependence_id"]
            .dropna()
            .nunique()
        )
        for interaction_type in sorted(INTERACTION_TYPES)
    }

    coverage_complete = all(n >= 1 for n in counts.values())
    cross_class_fit_allowed = all(n >= min_for_fit for n in counts.values())
    primary_claim_gate = all(n >= min_for_primary for n in counts.values())

    if primary_claim_gate:
        status = "primary_model_allowed"
    elif cross_class_fit_allowed:
        status = "exploratory_model_only"
    elif coverage_complete:
        status = "coverage_only"
    else:
        status = "incomplete_class_coverage"

    return CommonScaleGate(
        programme_counts=counts,
        coverage_complete=coverage_complete,
        cross_class_fit_allowed=cross_class_fit_allowed,
        primary_claim_gate=primary_claim_gate,
        status=status,
    )