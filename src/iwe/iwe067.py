from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd


_REQUIRED_PHENOLOGY = {
    "year",
    "plant_id",
    "treatment",
    "census",
    "open_flowers",
    "detected_eggs",
}
_REQUIRED_FRUIT = {
    "year",
    "plant_id",
    "treatment",
    "fruit_fate",
}

_ALLOWED_FATES = {
    "aborted",
    "expanded_unparasitized",
    "parasitized",
}


@dataclass(frozen=True)
class IWE067YearEffect:
    year: int
    n: int
    pearson_r: float
    fisher_z_native: float
    variance_native: float


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{label} missing columns: {sorted(missing)}")


def _normalize_nonnegative(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if (values.dropna() < 0).any():
        raise ValueError("counts must be nonnegative")
    return values


def build_iwe067_plant_table(
    phenology: pd.DataFrame,
    fruit: pd.DataFrame,
    *,
    year: int,
    treatment: str = "control",
) -> pd.DataFrame:
    """Reconstruct the frozen IWE067 plant-level overlap and final-fitness table.

    Expected canonical phenology columns:
      year, plant_id, treatment, census, open_flowers, detected_eggs

    Expected canonical fruit columns:
      year, plant_id, treatment, fruit_fate

    fruit_fate must be one of:
      aborted, expanded_unparasitized, parasitized

    The implementation follows docs/EXTRACTION_IWE067.md: focal flowering is
    open flowers; antagonist activity is leave-one-plant-out detected eggs per
    open flower at each census; both curves are normalized over shared valid
    censuses and overlap is histogram intersection. Final fitness is the
    fraction of scored marked flowers that become expanded unparasitized fruit.
    """
    _require_columns(phenology, _REQUIRED_PHENOLOGY, "phenology")
    _require_columns(fruit, _REQUIRED_FRUIT, "fruit")

    ph = phenology.loc[
        (phenology["year"] == year) & (phenology["treatment"] == treatment)
    ].copy()
    fr = fruit.loc[
        (fruit["year"] == year) & (fruit["treatment"] == treatment)
    ].copy()

    if ph.empty:
        raise ValueError(f"no phenology rows for year={year}, treatment={treatment}")
    if fr.empty:
        raise ValueError(f"no fruit rows for year={year}, treatment={treatment}")

    ph["open_flowers"] = _normalize_nonnegative(ph["open_flowers"])
    ph["detected_eggs"] = _normalize_nonnegative(ph["detected_eggs"])

    bad_fates = set(fr["fruit_fate"].dropna().astype(str)) - _ALLOWED_FATES
    if bad_fates:
        raise ValueError(f"unknown fruit_fate values: {sorted(bad_fates)}")

    # Multiple raw records at one plant x census are safely aggregated.
    ph = (
        ph.groupby(["plant_id", "census"], as_index=False, dropna=False)
        .agg(
            open_flowers=("open_flowers", lambda s: s.sum(min_count=1)),
            detected_eggs=("detected_eggs", lambda s: s.sum(min_count=1)),
        )
    )

    fruit_summary = (
        fr.loc[fr["fruit_fate"].isin(_ALLOWED_FATES)]
        .groupby("plant_id", as_index=False)
        .agg(
            scored_marked_flowers=("fruit_fate", "size"),
            expanded_unparasitized_fruits=(
                "fruit_fate",
                lambda s: int((s == "expanded_unparasitized").sum()),
            ),
        )
    )
    fruit_summary = fruit_summary.loc[fruit_summary["scored_marked_flowers"] > 0].copy()
    fruit_summary["fitness"] = (
        fruit_summary["expanded_unparasitized_fruits"]
        / fruit_summary["scored_marked_flowers"]
    )

    totals = (
        ph.groupby("census", as_index=False)
        .agg(
            total_open=("open_flowers", lambda s: s.sum(min_count=1)),
            total_eggs=("detected_eggs", lambda s: s.sum(min_count=1)),
        )
        .set_index("census")
    )

    plant_rows: list[dict] = []
    for plant_id, focal in ph.groupby("plant_id", sort=False):
        focal = focal.set_index("census").sort_index()
        joined = focal.join(totals, how="left")
        joined["ref_open"] = joined["total_open"] - joined["open_flowers"]
        joined["ref_eggs"] = joined["total_eggs"] - joined["detected_eggs"]

        valid = joined.loc[
            joined["open_flowers"].notna()
            & joined["ref_open"].notna()
            & joined["ref_eggs"].notna()
            & (joined["ref_open"] > 0)
        ].copy()
        if valid.empty:
            continue

        valid["activity"] = valid["ref_eggs"] / valid["ref_open"]
        flower_sum = float(valid["open_flowers"].sum())
        activity_sum = float(valid["activity"].sum())
        if flower_sum <= 0 or activity_sum <= 0:
            continue

        valid["flower_norm"] = valid["open_flowers"] / flower_sum
        valid["activity_norm"] = valid["activity"] / activity_sum
        overlap = float(
            valid[["flower_norm", "activity_norm"]].min(axis=1).sum()
        )
        plant_rows.append(
            {
                "year": int(year),
                "plant_id": plant_id,
                "overlap": overlap,
                "n_shared_censuses": int(len(valid)),
            }
        )

    overlap_df = pd.DataFrame(plant_rows)
    if overlap_df.empty:
        return pd.DataFrame(
            columns=[
                "year",
                "plant_id",
                "overlap",
                "n_shared_censuses",
                "scored_marked_flowers",
                "expanded_unparasitized_fruits",
                "fitness",
            ]
        )

    out = overlap_df.merge(fruit_summary, on="plant_id", how="inner", validate="one_to_one")
    return out.sort_values("plant_id").reset_index(drop=True)


def estimate_iwe067_year_effect(plant_table: pd.DataFrame, *, year: int) -> IWE067YearEffect:
    required = {"overlap", "fitness"}
    missing = required - set(plant_table.columns)
    if missing:
        raise ValueError(f"plant table missing columns: {sorted(missing)}")

    complete = plant_table[["overlap", "fitness"]].dropna()
    n = int(len(complete))
    if n < 4:
        raise ValueError("at least 4 complete plants are required for Fisher-z variance")

    r = float(complete["overlap"].corr(complete["fitness"], method="pearson"))
    if not math.isfinite(r):
        raise ValueError("Pearson correlation is not finite")
    if abs(r) >= 1:
        raise ValueError("absolute Pearson r must be < 1 for finite Fisher z")

    z = math.atanh(r)
    variance = 1.0 / (n - 3)
    return IWE067YearEffect(
        year=int(year),
        n=n,
        pearson_r=r,
        fisher_z_native=z,
        variance_native=variance,
    )


def reconstruct_iwe067(
    phenology: pd.DataFrame,
    fruit: pd.DataFrame,
    *,
    years: tuple[int, ...] = (2017, 2018),
    treatment: str = "control",
) -> tuple[pd.DataFrame, list[IWE067YearEffect]]:
    """Run the frozen IWE067 reconstruction for the registered primary years."""
    plant_tables: list[pd.DataFrame] = []
    effects: list[IWE067YearEffect] = []

    for year in years:
        table = build_iwe067_plant_table(
            phenology,
            fruit,
            year=year,
            treatment=treatment,
        )
        effect = estimate_iwe067_year_effect(table, year=year)
        plant_tables.append(table)
        effects.append(effect)

    combined = pd.concat(plant_tables, ignore_index=True)
    return combined, effects
