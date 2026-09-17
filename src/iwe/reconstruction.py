from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd


def histogram_intersection(a: Sequence[float], b: Sequence[float]) -> float:
    """Return histogram intersection after normalizing two nonnegative curves.

    Both curves must have the same length and a positive finite total. The
    returned overlap is in [0, 1].
    """
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    if x.shape != y.shape:
        raise ValueError("curves must have the same shape")
    if x.ndim != 1:
        raise ValueError("curves must be one-dimensional")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("curves must be finite")
    if np.any(x < 0) or np.any(y < 0):
        raise ValueError("curves must be nonnegative")
    sx = float(x.sum())
    sy = float(y.sum())
    if sx <= 0 or sy <= 0:
        raise ValueError("curves must have positive totals")
    xn = x / sx
    yn = y / sy
    return float(np.minimum(xn, yn).sum())


def _count(row: Mapping[str, object], key: str) -> float:
    value = row.get(key, 0.0)
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    return float(value)


def _id_token(value: object) -> str:
    """Format spreadsheet numeric identifiers like R's character coercion."""
    if pd.isna(value):
        raise ValueError("identifier component cannot be missing")
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    return str(value).strip()


def prepare_maxfield_phenology(phen_raw: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the Maxfield 2021 phenology preparation needed by IWE068.

    This mirrors the source workflow's rebuilt plant IDs, row sums, two date
    recodes, metadata join, and plant-by-census completion. Inserted rows have
    zero flowers/buds and zero eggs because a completed zero-floral census
    cannot contain an oviposition event on that focal plant.
    """
    required_phen = {"date", "plot", "subplot", "plant"}
    missing_phen = required_phen - set(phen_raw.columns)
    if missing_phen:
        raise ValueError(f"missing phenology columns: {sorted(missing_phen)}")
    required_meta = {"plantid", "snow", "temp"}
    missing_meta = required_meta - set(metadata.columns)
    if missing_meta:
        raise ValueError(f"missing metadata columns: {sorted(missing_meta)}")

    work = phen_raw.copy()
    open_cols = [c for c in work.columns if c.startswith("open_")]
    bud_cols = [c for c in work.columns if c.startswith("buds_")]
    egg_cols = [c for c in work.columns if c.startswith("eggs_")]
    if not open_cols or not bud_cols or not egg_cols:
        raise ValueError("phenology table must contain open_*, buds_*, and eggs_* columns")

    work["plantid"] = [
        f"{_id_token(plot)}{_id_token(subplot)}{_id_token(plant)}"
        for plot, subplot, plant in zip(work["plot"], work["subplot"], work["plant"])
    ]
    numeric_cols = open_cols + bud_cols + egg_cols
    work[numeric_cols] = work[numeric_cols].apply(pd.to_numeric, errors="coerce")
    work["open"] = work[open_cols].sum(axis=1, skipna=True)
    work["buds"] = work[bud_cols].sum(axis=1, skipna=True)
    work["eggs"] = work[egg_cols].sum(axis=1, skipna=True)
    work["floral"] = work["open"] + work["buds"]

    census = pd.to_datetime(work["date"], errors="raise").dt.normalize()
    census = census.replace(
        {
            pd.Timestamp("2021-07-02"): pd.Timestamp("2021-06-30"),
            pd.Timestamp("2021-07-26"): pd.Timestamp("2021-07-20"),
        }
    )
    work["census"] = census

    meta = metadata[["plantid", "snow", "temp"]].copy()
    if meta["plantid"].duplicated().any():
        raise ValueError("metadata plantid must be unique")
    work = work.merge(meta, on="plantid", how="left", validate="m:1")
    work = work.dropna(subset=["snow", "temp"])

    observed = (
        work.groupby(["plantid", "snow", "temp", "census"], as_index=False)[["floral", "eggs"]]
        .sum()
        .sort_values(["plantid", "census"])
    )
    plant_meta = observed[["plantid", "snow", "temp"]].drop_duplicates()
    dates = pd.DataFrame({"census": sorted(observed["census"].unique())})
    plant_meta["_key"] = 1
    dates["_key"] = 1
    grid = plant_meta.merge(dates, on="_key", how="inner").drop(columns="_key")
    out = grid.merge(observed, on=["plantid", "snow", "temp", "census"], how="left")
    out[["floral", "eggs"]] = out[["floral", "eggs"]].fillna(0.0)
    return out.sort_values(["plantid", "census"]).reset_index(drop=True)


def source_seed_outcome(row: Mapping[str, object]) -> dict[str, float]:
    """Reproduce the Maxfield 2021 seed-fitness definitions in traits.Rmd.

    R arithmetic propagates NA even when an undefined rate is multiplied by
    zero (``0 * NA`` is ``NA``). We preserve that behavior rather than turning
    fruitless plants into artificial zero-fitness observations.
    """
    seeds = _count(row, "seeds")
    fruits = _count(row, "fruits")
    fruits_split = _count(row, "fruits_split")
    aborts = _count(row, "aborts")
    fly_no_seeds = _count(row, "fruits_fly_no_seeds")
    fly_with_seeds = _count(row, "fruits_fly_with_seeds")
    seeds_fly = _count(row, "seeds_fly")
    fruits_caterpillar = _count(row, "fruits_caterpillar")
    early_uncountable = _count(row, "fruits_early_uncountable")
    flowers_buds = _count(row, "flowers_buds")
    collected_early = _count(row, "flowers_buds_collected_early")
    collected_last = _count(row, "flowers_buds_collected_last")

    seeds_per_fruit = seeds / fruits if fruits > 0 else np.nan
    fruits_aborted = aborts + collected_last
    source_seed_denominator = (
        fruits
        + fruits_aborted
        + fly_with_seeds
        + fly_no_seeds
        + fruits_caterpillar
    )
    mean_source_seeds = seeds / source_seed_denominator if source_seed_denominator > 0 else np.nan

    # Match the source R expression literally: both rate terms are present in
    # the expression even when their multipliers are zero, so any undefined
    # rate propagates NA through seeds_est.
    if not np.isfinite(mean_source_seeds) or not np.isfinite(seeds_per_fruit):
        seeds_est = np.nan
    else:
        seeds_est = (
            seeds
            + seeds_fly
            + (collected_early + early_uncountable) * mean_source_seeds
            + fruits_split * seeds_per_fruit
        )

    fruits_with_seeds = fruits + fruits_split + fly_with_seeds
    fruits_nonaborted = fruits_with_seeds + fly_no_seeds + fruits_caterpillar + fruits_split
    flowers_est = fruits_nonaborted + aborts + flowers_buds
    seeds_per_flower = seeds_est / flowers_est if flowers_est > 0 and np.isfinite(seeds_est) else np.nan

    return {
        "seeds_per_fruit": float(seeds_per_fruit),
        "fruits_aborted": float(fruits_aborted),
        "seeds_est": float(seeds_est),
        "fruits_with_seeds": float(fruits_with_seeds),
        "fruits_nonaborted": float(fruits_nonaborted),
        "flowers_est": float(flowers_est),
        "seeds_per_flower": float(seeds_per_flower),
    }


def leave_one_out_overlaps(
    df: pd.DataFrame,
    *,
    plant_col: str,
    time_col: str,
    floral_col: str,
    egg_col: str,
) -> pd.DataFrame:
    """Compute focal-plant flower overlap with leave-one-out egg activity.

    The activity curve at each census is total eggs divided by total floral
    availability among all *other* plants. Each focal plant's floral curve and
    the reference activity curve are then normalized over shared valid dates
    and compared by histogram intersection.
    """
    required = {plant_col, time_col, floral_col, egg_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    work = df[[plant_col, time_col, floral_col, egg_col]].copy()
    work[floral_col] = pd.to_numeric(work[floral_col], errors="coerce")
    work[egg_col] = pd.to_numeric(work[egg_col], errors="coerce")
    if work[[floral_col, egg_col]].isna().any().any():
        raise ValueError("floral and egg values must be numeric and non-missing")
    if (work[[floral_col, egg_col]] < 0).any().any():
        raise ValueError("floral and egg counts must be nonnegative")

    per_plant_time = (
        work.groupby([plant_col, time_col], as_index=False)[[floral_col, egg_col]]
        .sum()
        .sort_values([plant_col, time_col])
    )
    totals = per_plant_time.groupby(time_col)[[floral_col, egg_col]].sum()

    records: list[dict[str, object]] = []
    for plant, focal in per_plant_time.groupby(plant_col, sort=True):
        focal = focal.set_index(time_col)
        common_times = totals.index.intersection(focal.index)
        reference_floral = totals.loc[common_times, floral_col] - focal.loc[common_times, floral_col]
        reference_eggs = totals.loc[common_times, egg_col] - focal.loc[common_times, egg_col]
        valid = reference_floral > 0
        common_times = common_times[valid.to_numpy()]
        if len(common_times) == 0:
            overlap = np.nan
        else:
            floral_curve = focal.loc[common_times, floral_col].to_numpy(dtype=float)
            activity_curve = (
                reference_eggs.loc[common_times].to_numpy(dtype=float)
                / reference_floral.loc[common_times].to_numpy(dtype=float)
            )
            if floral_curve.sum() <= 0 or activity_curve.sum() <= 0:
                overlap = np.nan
            else:
                overlap = histogram_intersection(floral_curve, activity_curve)
        records.append({plant_col: plant, "overlap": overlap})

    return pd.DataFrame.from_records(records)
