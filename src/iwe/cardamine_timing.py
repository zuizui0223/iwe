from __future__ import annotations

import pandas as pd


PLANT_TIMING_COLUMNS = ("year", "ecotype", "plant_id", "doy", "flowers")
ADULT_TIMING_COLUMNS = ("year", "event_doy")


def _require_columns(df: pd.DataFrame, required: tuple[str, ...], label: str) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"{label} missing columns: {', '.join(missing)}")


def first_flowering_dates(plant_observations: pd.DataFrame) -> pd.DataFrame:
    """Return first observed flowering DOY for each year x ecotype x plant.

    Only timing columns are read. Extra response/mechanism columns are ignored.
    Plants with no observation containing >0 open flowers are omitted.
    """
    _require_columns(plant_observations, PLANT_TIMING_COLUMNS, "plant_observations")
    timing = plant_observations.loc[:, PLANT_TIMING_COLUMNS].copy()
    timing["flowers"] = pd.to_numeric(timing["flowers"], errors="raise")
    timing["doy"] = pd.to_numeric(timing["doy"], errors="raise")
    if timing[list(PLANT_TIMING_COLUMNS)].isna().any().any():
        raise ValueError("plant timing columns must not contain missing values")

    flowering = timing.loc[timing["flowers"] > 0].copy()
    if flowering.empty:
        return pd.DataFrame(
            columns=["year", "ecotype", "plant_id", "first_flowering_doy"]
        )

    out = (
        flowering.groupby(["year", "ecotype", "plant_id"], as_index=False)["doy"]
        .min()
        .rename(columns={"doy": "first_flowering_doy"})
    )
    return out.sort_values(["year", "ecotype", "plant_id"]).reset_index(drop=True)


def adult_flight_windows(
    adult_events: pd.DataFrame,
    lower_quantile: float = 0.10,
    upper_quantile: float = 0.90,
) -> pd.DataFrame:
    """Return year-specific empirical adult-flight quantile windows.

    The default 10th-90th percentile window mirrors the whiskers reported for the
    source female capture+recapture distribution. Quantiles use pandas default
    linear interpolation (equivalent to R default type-7 quantiles).
    """
    _require_columns(adult_events, ADULT_TIMING_COLUMNS, "adult_events")
    if not 0 <= lower_quantile < upper_quantile <= 1:
        raise ValueError("quantiles must satisfy 0 <= lower < upper <= 1")

    timing = adult_events.loc[:, ADULT_TIMING_COLUMNS].copy()
    timing["event_doy"] = pd.to_numeric(timing["event_doy"], errors="raise")
    if timing[list(ADULT_TIMING_COLUMNS)].isna().any().any():
        raise ValueError("adult timing columns must not contain missing values")

    rows: list[dict[str, float | int]] = []
    for year, group in timing.groupby("year", sort=True):
        days = group["event_doy"]
        if len(days) < 2:
            raise ValueError(f"year={year}: at least two adult timing events are required")
        rows.append(
            {
                "year": year,
                "adult_q10_doy": float(days.quantile(lower_quantile)),
                "adult_q90_doy": float(days.quantile(upper_quantile)),
                "n_adult_events": int(len(days)),
            }
        )
    return pd.DataFrame(rows)


def cardamine_timing_only_exposure(
    plant_observations: pd.DataFrame,
    adult_events: pd.DataFrame,
) -> pd.DataFrame:
    """Classify response-blind onset exposure to the female adult-flight window.

    The source describes two phenological refugia on opposite sides of the
    female flight period. First flowering is therefore kept as a three-level
    exposure rather than collapsing early and late escape into one group:

    - early_refugium: first flowering before the female q10 boundary;
    - core_flight: first flowering inside/on the female q10-q90 window;
    - late_refugium: first flowering after the female q90 boundary.

    Ecotype is retained. Downstream SMDs compare core_flight separately against
    each refugium so biologically distinct escape routes are never pooled.
    """
    plants = first_flowering_dates(plant_observations)
    windows = adult_flight_windows(adult_events)
    if plants.empty:
        return plants.assign(
            adult_q10_doy=pd.Series(dtype=float),
            adult_q90_doy=pd.Series(dtype=float),
            n_adult_events=pd.Series(dtype=int),
            timing_group=pd.Series(dtype=str),
        )

    out = plants.merge(windows, on="year", how="left", validate="many_to_one")
    if out[["adult_q10_doy", "adult_q90_doy"]].isna().any().any():
        missing_years = sorted(
            out.loc[out["adult_q10_doy"].isna(), "year"].drop_duplicates().tolist()
        )
        raise ValueError(f"missing adult timing window for plant years: {missing_years}")

    out["timing_group"] = "core_flight"
    out.loc[
        out["first_flowering_doy"] < out["adult_q10_doy"], "timing_group"
    ] = "early_refugium"
    out.loc[
        out["first_flowering_doy"] > out["adult_q90_doy"], "timing_group"
    ] = "late_refugium"
    return out.sort_values(["year", "ecotype", "plant_id"]).reset_index(drop=True)
