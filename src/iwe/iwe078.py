from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import pandas as pd


_REQUIRED_FLOWER_COLUMNS = {
    "experiment",
    "plant_id",
    "treatment",
    "date",
    "potential_flowers",
}
_REQUIRED_ATTACK_COLUMNS = {
    "experiment",
    "plant_id",
    "treatment",
    "date",
    "mompha_acquired",
}
_REQUIRED_FITNESS_COLUMNS = {
    "experiment",
    "plant_id",
    "treatment",
    "final_reproduction",
}


@dataclass(frozen=True)
class IWE078ExperimentEffect:
    experiment: str
    n: int
    pearson_r: float
    fisher_z_native: float
    variance_native: float


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{label} missing columns: {sorted(missing)}")


def _numeric_nonnegative(series: pd.Series, label: str) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if (values.dropna() < 0).any():
        raise ValueError(f"{label} must be nonnegative")
    return values


def build_iwe078_plant_table(
    flowering: pd.DataFrame,
    attacks: pd.DataFrame,
    fitness: pd.DataFrame,
    *,
    experiment: str,
    treatment: str = "control",
) -> pd.DataFrame:
    """Build the frozen IWE078 control-plant overlap/fitness table.

    Inputs are canonicalized source tables. The source adapter must construct:

    - potential_flowers using the source correction
      open flowers + fresh Mompha galls / 9;
    - mompha_acquired using the source week-over-week acquisition correction;
    - final_reproduction as source realized reproduction after seed-predator loss.

    For each focal control plant, Mompha activity is estimated from all other
    eligible control plants in the same experiment. Both temporal curves are
    normalized before histogram-intersection overlap is calculated.
    """
    _require_columns(flowering, _REQUIRED_FLOWER_COLUMNS, "flowering")
    _require_columns(attacks, _REQUIRED_ATTACK_COLUMNS, "attacks")
    _require_columns(fitness, _REQUIRED_FITNESS_COLUMNS, "fitness")

    fl = flowering.loc[
        (flowering["experiment"].astype(str) == str(experiment))
        & (flowering["treatment"] == treatment)
    ].copy()
    at = attacks.loc[
        (attacks["experiment"].astype(str) == str(experiment))
        & (attacks["treatment"] == treatment)
    ].copy()
    ft = fitness.loc[
        (fitness["experiment"].astype(str) == str(experiment))
        & (fitness["treatment"] == treatment)
    ].copy()

    if fl.empty:
        raise ValueError(f"no flowering rows for experiment={experiment}, treatment={treatment}")
    if at.empty:
        raise ValueError(f"no attack rows for experiment={experiment}, treatment={treatment}")
    if ft.empty:
        raise ValueError(f"no fitness rows for experiment={experiment}, treatment={treatment}")

    fl["potential_flowers"] = _numeric_nonnegative(
        fl["potential_flowers"], "potential_flowers"
    )
    at["mompha_acquired"] = _numeric_nonnegative(
        at["mompha_acquired"], "mompha_acquired"
    )
    ft["final_reproduction"] = _numeric_nonnegative(
        ft["final_reproduction"], "final_reproduction"
    )

    fl = (
        fl.groupby(["plant_id", "date"], as_index=False, dropna=False)
        .agg(
            potential_flowers=(
                "potential_flowers",
                lambda s: s.sum(min_count=1),
            )
        )
    )
    at = (
        at.groupby(["plant_id", "date"], as_index=False, dropna=False)
        .agg(
            mompha_acquired=(
                "mompha_acquired",
                lambda s: s.sum(min_count=1),
            )
        )
    )

    if ft["plant_id"].duplicated().any():
        raise ValueError("fitness must contain at most one row per plant within experiment")

    ft = ft.loc[ft["final_reproduction"].notna()].copy()
    ft["log_total_fitness"] = np.log1p(ft["final_reproduction"].astype(float))

    eligible_ids = set(fl["plant_id"].dropna()) & set(at["plant_id"].dropna()) & set(
        ft["plant_id"].dropna()
    )

    rows: list[dict] = []
    for plant_id in sorted(eligible_ids, key=str):
        focal = fl.loc[fl["plant_id"] == plant_id, ["date", "potential_flowers"]].copy()
        reference = (
            at.loc[at["plant_id"] != plant_id]
            .groupby("date", as_index=False)
            .agg(
                reference_mompha=(
                    "mompha_acquired",
                    lambda s: s.sum(min_count=1),
                )
            )
        )

        shared = focal.merge(reference, on="date", how="inner", validate="one_to_one")
        shared = shared.loc[
            shared["potential_flowers"].notna()
            & shared["reference_mompha"].notna()
        ].copy()
        if shared.empty:
            continue

        flower_total = float(shared["potential_flowers"].sum())
        mompha_total = float(shared["reference_mompha"].sum())
        if flower_total <= 0 or mompha_total <= 0:
            continue

        shared["flower_norm"] = shared["potential_flowers"] / flower_total
        shared["mompha_norm"] = shared["reference_mompha"] / mompha_total
        overlap = float(
            shared[["flower_norm", "mompha_norm"]].min(axis=1).sum()
        )

        outcome = ft.loc[ft["plant_id"] == plant_id].iloc[0]
        rows.append(
            {
                "experiment": str(experiment),
                "plant_id": plant_id,
                "overlap": overlap,
                "n_shared_dates": int(len(shared)),
                "final_reproduction": float(outcome["final_reproduction"]),
                "log_total_fitness": float(outcome["log_total_fitness"]),
            }
        )

    return pd.DataFrame(rows)


def estimate_iwe078_experiment_effect(
    plant_table: pd.DataFrame,
    *,
    experiment: str,
) -> IWE078ExperimentEffect:
    required = {"overlap", "log_total_fitness"}
    missing = required - set(plant_table.columns)
    if missing:
        raise ValueError(f"plant table missing columns: {sorted(missing)}")

    complete = plant_table[["overlap", "log_total_fitness"]].dropna()
    n = int(len(complete))
    if n < 4:
        raise ValueError("at least 4 complete control plants are required")

    r = float(complete["overlap"].corr(complete["log_total_fitness"], method="pearson"))
    if not math.isfinite(r):
        raise ValueError("Pearson correlation is not finite")
    if abs(r) >= 1:
        raise ValueError("absolute Pearson r must be < 1 for finite Fisher z")

    return IWE078ExperimentEffect(
        experiment=str(experiment),
        n=n,
        pearson_r=r,
        fisher_z_native=math.atanh(r),
        variance_native=1.0 / (n - 3),
    )


def reconstruct_iwe078(
    flowering: pd.DataFrame,
    attacks: pd.DataFrame,
    fitness: pd.DataFrame,
    *,
    experiments: tuple[str, ...] = ("1", "2"),
    treatment: str = "control",
) -> tuple[pd.DataFrame, list[IWE078ExperimentEffect]]:
    """Run the frozen IWE078 reconstruction on canonicalized source data."""
    tables: list[pd.DataFrame] = []
    effects: list[IWE078ExperimentEffect] = []
    for experiment in experiments:
        table = build_iwe078_plant_table(
            flowering,
            attacks,
            fitness,
            experiment=experiment,
            treatment=treatment,
        )
        effect = estimate_iwe078_experiment_effect(table, experiment=experiment)
        tables.append(table)
        effects.append(effect)

    return pd.concat(tables, ignore_index=True), effects
