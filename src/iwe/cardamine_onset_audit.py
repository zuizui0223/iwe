"""Response-blind identification audit for interval-censored Cardamine flowering onset.

Davies & Saccheri 2024 revisited transects every 5–7 days and tagged
newly flowering ramets on visits. Their first *observed* flower is an
upper bound on the true onset, not necessarily its exact DOY.

Do not convert the typical visit interval into a source-certified bound.
A 7-day lag is displayed *only as an explicit scenario*. In the default
source-bound audit, a lower bound is unknown unless supplied with an
original-observation locator. This module never produces H1 effects.
"""
from __future__ import annotations

import pandas as pd

from .cardamine_timing import cardamine_timing_only_exposure

KEY = ["year", "ecotype", "plant_id"]
REQUIRED_BOUND_COLUMNS = KEY + ["earliest_possible_doy", "source_locator"]


def _interval_class(
    low: float | None, high: float, q10: float, q90: float
) -> str:
    """Assign only when every possible onset day is in one class."""
    if high < q10:
        return "early_refugium"
    if low is None:
        return "unresolved_left_censored"
    if low > q90:
        return "late_refugium"
    if low >= q10 and high <= q90:
        return "core_flight"
    return "boundary_sensitive"


def audit_cardamine_onset_intervals(
    plant_observations: pd.DataFrame,
    adult_events: pd.DataFrame,
    source_lower_bounds: pd.DataFrame | None = None,
    scenario_max_detection_lag_days: int = 7,
) -> pd.DataFrame:
    """Audit source-identifiable vs assumed-lag timing classes, response-blind.

    Input source_lower_bounds must be independently inspected, documented,
    keyed by (year, ecotype, plant_id), and contain the inclusive earliest
    possible true onset DOY and a source locator. A preceding zero flower
    count *may* be informative but is not automatically proof that a brief
    earlier flowering episode did not occur between visits.

    The observed first-positive date is the right endpoint. Missing lower
    bounds remain unknown. The scenario results have no admissibility power
    and never replace the source-certified classification.
    """
    if (isinstance(scenario_max_detection_lag_days, bool)
            or not isinstance(scenario_max_detection_lag_days, int)
            or scenario_max_detection_lag_days < 0
            or scenario_max_detection_lag_days > 366):
        raise ValueError("scenario_max_detection_lag_days needs integer 0..366")

    exposure = cardamine_timing_only_exposure(
        plant_observations, adult_events
    ).copy()
    if exposure.empty:
        return exposure.assign(
            source_earliest_possible_doy=pd.Series(dtype=float),
            source_locator=pd.Series(dtype=str),
            source_identified_group=pd.Series(dtype=str),
            scenario_earliest_possible_doy=pd.Series(dtype=float),
            scenario_stable_group=pd.Series(dtype=str),
            observed_group_scenario_stable=pd.Series(dtype=bool),
        )

    if source_lower_bounds is None:
        exposure["source_earliest_possible_doy"] = float("nan")
        exposure["source_locator"] = ""
    else:
        bounds = source_lower_bounds.copy()
        missing = sorted(set(REQUIRED_BOUND_COLUMNS) - set(bounds))
        if missing:
            raise ValueError("source lower-bound table missing: " + ", ".join(missing))
        bounds = bounds[REQUIRED_BOUND_COLUMNS]
        if bounds.duplicated(KEY).any():
            raise ValueError("duplicate source onset lower bounds for a plant")
        locators = bounds["source_locator"]
        if locators.isna().any() or locators.astype(str).str.strip().eq("").any():
            raise ValueError("source onset bounds require original observation locator")
        try:
            nums = pd.to_numeric(bounds["earliest_possible_doy"], errors="raise")
        except (TypeError, ValueError) as exc:
            raise ValueError("source earliest_possible_doy must be numeric") from exc
        if (nums.isna().any() or (nums < 1).any() or (nums > 366).any()
                or (nums % 1 != 0).any()):
            raise ValueError("source onset lower bounds require integer DOY 1..366")
        bounds["earliest_possible_doy"] = nums.astype(int)
        check = bounds.merge(exposure[KEY], on=KEY, how="left", indicator=True,
                             validate="one_to_one")
        if check["_merge"].ne("both").any():
            raise ValueError("source onset bound contains unknown plant key")
        exposure = exposure.merge(
            bounds.rename(columns={
                "earliest_possible_doy": "source_earliest_possible_doy"
            }),
            on=KEY, how="left", validate="one_to_one"
        )
        if (exposure["source_earliest_possible_doy"].notna()
                & (exposure["source_earliest_possible_doy"]
                   > exposure["first_flowering_doy"])).any():
            raise ValueError("source earliest onset exceeds first observed flower DOY")
        exposure["source_locator"] = exposure["source_locator"].fillna("")

    classifications: list[str] = []
    scenarios: list[str] = []
    for row in exposure.itertuples(index=False):
        high = float(row.first_flowering_doy)
        q10 = float(row.adult_q10_doy)
        q90 = float(row.adult_q90_doy)
        low = (None if pd.isna(row.source_earliest_possible_doy)
               else float(row.source_earliest_possible_doy))
        classifications.append(_interval_class(low, high, q10, q90))
        scenario_low = max(1.0, high - scenario_max_detection_lag_days)
        scenarios.append(_interval_class(scenario_low, high, q10, q90))

    exposure["source_identified_group"] = classifications
    exposure["scenario_earliest_possible_doy"] = (
        exposure["first_flowering_doy"] - scenario_max_detection_lag_days
    ).clip(lower=1)
    exposure["scenario_stable_group"] = scenarios
    exposure["observed_group_scenario_stable"] = (
        exposure["timing_group"] == exposure["scenario_stable_group"]
    )
    exposure["scenario_max_detection_lag_days"] = scenario_max_detection_lag_days
    exposure["source_bound_is_originally_verified"] = False
    exposure["source_bound_verification_note"] = (
        "Provided source locators require human original-record review; "
        "software cannot authenticate them"
    )
    exposure["scenario_is_source_verified"] = False
    exposure["strict_h1_admission_from_this_audit"] = False
    return exposure
