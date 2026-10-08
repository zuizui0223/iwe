"""Non-promoting response-blind Cardamine onset-misclassification effect audit.

The temporal groups are constructed without outcomes. Outcomes are joined only
after all point, interval-certified, assumed-lag stable, and assumed-lag
earliest-onset assignments are fixed. No analysis generates strict-H1 rows.
"""
from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from .cardamine_onset_audit import audit_cardamine_onset_intervals
from .cardamine_outcome import CONTRASTS, cardamine_smd_audit, cardamine_smd_effects

GROUPS = frozenset(("early_refugium", "core_flight", "late_refugium"))
DEFAULT_LAGS = (0, 3, 5, 7, 10, 14)
KEY = ("year", "ecotype", "plant_id")


def cardamine_onset_effect_sensitivity(
    plant_observations: pd.DataFrame,
    adult_events: pd.DataFrame,
    plant_summaries: pd.DataFrame,
    *,
    source_lower_bounds: pd.DataFrame | None = None,
    scenario_lags: Sequence[int] = DEFAULT_LAGS,
) -> pd.DataFrame:
    """Return strata-level SMD stability audit, never evidence promotion.

    Interpretation:
    - observed_point: first *observed* open flower, a directly observed proxy.
    - source_certified_only: keep only classifications with independently
      supplied individual-level lower bounds (early needs no lower bound).
    - scenario_stable_only: keep plants whose group cannot change under an
      *assumed* maximum delay of lag days.
    - scenario_earliest_all: place every true onset at its scenario earliest
      possible date, an adverse coherent shift, NOT source evidence.

    All assumed scenarios are sensitivity analyses, not estimates of true
    biological onset or new independent effects.
    """
    lags = list(scenario_lags)
    if not lags:
        raise ValueError("scenario_lags must be nonempty")
    if len(set(lags)) != len(lags):
        raise ValueError("scenario_lags must not repeat values")
    if any(isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 366
           for n in lags):
        raise ValueError("each scenario lag must be an integer 0..366")

    first = audit_cardamine_onset_intervals(
        plant_observations, adult_events, source_lower_bounds, lags[0]
    )
    if first.empty:
        return pd.DataFrame(columns=[
            "year", "ecotype", "contrast", "assignment_method",
            "assumed_detection_lag_days", "n_total_observed",
            "n_excluded_uncertain", "n_high", "n_low", "eligible_smd",
            "blocker", "effect_native", "variance_native",
            "source_verified_assumed_lag", "strict_h1_effect_promoted",
        ])

    strata = first[["year", "ecotype"]].drop_duplicates().to_dict("records")
    rows: list[dict[str, object]] = []

    def collect(data: pd.DataFrame, mode: str, lag: int | None) -> None:
        valid = data.loc[data["timing_group"].isin(GROUPS)].copy()
        audit = (cardamine_smd_audit(valid, plant_summaries)
                 if not valid.empty else pd.DataFrame())
        effects = (cardamine_smd_effects(valid, plant_summaries)
                   if not valid.empty else pd.DataFrame())
        for stratum in strata:
            year, ecotype = stratum["year"], stratum["ecotype"]
            original_n = int(((first["year"] == year) &
                              (first["ecotype"] == ecotype)).sum())
            included_n = int(((valid["year"] == year) &
                              (valid["ecotype"] == ecotype)).sum())
            for contrast, high_group, low_group in CONTRASTS:
                out: dict[str, object] = {
                    "year": year,
                    "ecotype": ecotype,
                    "contrast": contrast,
                    "assignment_method": mode,
                    "assumed_detection_lag_days": lag,
                    "n_total_observed": original_n,
                    "n_excluded_uncertain": original_n - included_n,
                    "n_high": 0,
                    "n_low": 0,
                    "eligible_smd": False,
                    "blocker": "no estimable groups under this assignment",
                    "effect_native": float("nan"),
                    "variance_native": float("nan"),
                    "source_verified_assumed_lag": False,
                    "strict_h1_effect_promoted": False,
                }
                if not audit.empty:
                    hit = audit.loc[(audit["year"] == year) &
                                    (audit["ecotype"] == ecotype) &
                                    (audit["contrast"] == contrast)]
                    if len(hit) == 1:
                        result = hit.iloc[0]
                        out.update({
                            "n_high": int(result["n_high"]),
                            "n_low": int(result["n_low"]),
                            "eligible_smd": bool(result["eligible_smd"]),
                            "blocker": str(result["blocker"]),
                        })
                if not effects.empty:
                    hit = effects.loc[(effects["year"] == year) &
                                      (effects["ecotype"] == ecotype) &
                                      (effects["contrast"] == contrast)]
                    if len(hit) == 1:
                        out["effect_native"] = float(hit.iloc[0]["effect_native"])
                        out["variance_native"] = float(hit.iloc[0]["variance_native"])
                rows.append(out)

    collect(first, "observed_point", None)
    source = first.copy()
    source["timing_group"] = source["source_identified_group"]
    collect(source, "source_certified_only", None)

    for lag in lags:
        audit = audit_cardamine_onset_intervals(
            plant_observations, adult_events, source_lower_bounds, lag
        )
        stable = audit.copy()
        stable["timing_group"] = stable["scenario_stable_group"]
        collect(stable, "scenario_stable_only", lag)
        shifted = audit.copy()
        early = shifted["scenario_earliest_possible_doy"]
        shifted["timing_group"] = "core_flight"
        shifted.loc[early < shifted["adult_q10_doy"], "timing_group"] = (
            "early_refugium"
        )
        shifted.loc[early > shifted["adult_q90_doy"], "timing_group"] = (
            "late_refugium"
        )
        collect(shifted, "scenario_earliest_all", lag)

    return pd.DataFrame(rows).sort_values(
        ["year", "ecotype", "contrast", "assignment_method",
         "assumed_detection_lag_days"], na_position="first"
    ).reset_index(drop=True)
