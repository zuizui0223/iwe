from __future__ import annotations

import pandas as pd

from .effects import hedges_g_from_summary


OUTCOME_COLUMNS = (
    "year",
    "ecotype",
    "plant_id",
    "max_ru",
    "final_intact_ru",
)
EXPOSURE_COLUMNS = (
    "year",
    "ecotype",
    "plant_id",
    "synchrony_group",
)
ALLOWED_GROUPS = {"higher_synchrony", "lower_synchrony"}
DEPENDENCE_ID = "DEP_CARDAMINE_DIBBINSDALE_2012_2014"


def _require_columns(df: pd.DataFrame, required: tuple[str, ...], label: str) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"{label} missing columns: {', '.join(missing)}")


def cardamine_realized_fraction(plant_summaries: pd.DataFrame) -> pd.DataFrame:
    """Build the frozen source-compatible Cardamine reproductive outcome.

    The input must already contain source-backed plant-level maximum reproductive
    units (max_ru) and final intact reproductive units at dehiscence
    (final_intact_ru). No timing, egg or larval columns are read.

    realized_fraction = final_intact_ru / max_ru
    """
    _require_columns(plant_summaries, OUTCOME_COLUMNS, "plant_summaries")
    out = plant_summaries.loc[:, OUTCOME_COLUMNS].copy()
    if out.duplicated(["year", "ecotype", "plant_id"]).any():
        raise ValueError("plant_summaries must be unique by year x ecotype x plant_id")

    for column in ("max_ru", "final_intact_ru"):
        out[column] = pd.to_numeric(out[column], errors="raise")
    if out[list(OUTCOME_COLUMNS)].isna().any().any():
        raise ValueError("Cardamine outcome columns must not contain missing values")
    if (out["max_ru"] <= 0).any():
        raise ValueError("max_ru must be positive")
    if (out["final_intact_ru"] < 0).any():
        raise ValueError("final_intact_ru must be non-negative")
    if (out["final_intact_ru"] > out["max_ru"]).any():
        raise ValueError("final_intact_ru cannot exceed max_ru")

    out["realized_fraction"] = out["final_intact_ru"] / out["max_ru"]
    return out.sort_values(["year", "ecotype", "plant_id"]).reset_index(drop=True)


def cardamine_smd_audit(
    exposure: pd.DataFrame,
    plant_summaries: pd.DataFrame,
) -> pd.DataFrame:
    """Audit every year x ecotype stratum under the frozen high-vs-low contrast.

    No stratum is selected by effect direction. A stratum is mathematically
    estimable only when both timing groups contain >=2 source-backed outcome
    observations and both group SDs are positive.
    """
    _require_columns(exposure, EXPOSURE_COLUMNS, "exposure")
    exp = exposure.loc[:, EXPOSURE_COLUMNS].copy()
    if exp.duplicated(["year", "ecotype", "plant_id"]).any():
        raise ValueError("exposure must be unique by year x ecotype x plant_id")
    unknown = sorted(set(exp["synchrony_group"].dropna()) - ALLOWED_GROUPS)
    if unknown:
        raise ValueError(f"unknown Cardamine synchrony groups: {unknown}")
    if exp[list(EXPOSURE_COLUMNS)].isna().any().any():
        raise ValueError("Cardamine exposure columns must not contain missing values")

    outcomes = cardamine_realized_fraction(plant_summaries)
    merged = exp.merge(
        outcomes[["year", "ecotype", "plant_id", "realized_fraction"]],
        on=["year", "ecotype", "plant_id"],
        how="left",
        validate="one_to_one",
        indicator=True,
    )

    rows: list[dict[str, object]] = []
    for (year, ecotype), group in merged.groupby(["year", "ecotype"], sort=True):
        high_all = group.loc[group["synchrony_group"] == "higher_synchrony"]
        low_all = group.loc[group["synchrony_group"] == "lower_synchrony"]
        high = high_all["realized_fraction"].dropna()
        low = low_all["realized_fraction"].dropna()
        n_high_total = int(len(high_all))
        n_low_total = int(len(low_all))
        n_high = int(len(high))
        n_low = int(len(low))
        missing_high = n_high_total - n_high
        missing_low = n_low_total - n_low
        sd_high = float(high.std(ddof=1)) if n_high >= 2 else float("nan")
        sd_low = float(low.std(ddof=1)) if n_low >= 2 else float("nan")

        blocker = ""
        if n_high < 2 or n_low < 2:
            blocker = "requires at least two outcome observations in each timing group"
        elif sd_high <= 0 or sd_low <= 0:
            blocker = "requires positive within-group SD in both timing groups"

        rows.append(
            {
                "year": year,
                "ecotype": ecotype,
                "n_higher_synchrony_total": n_high_total,
                "n_lower_synchrony_total": n_low_total,
                "n_higher_synchrony": n_high,
                "n_lower_synchrony": n_low,
                "n_higher_synchrony_missing_outcome": missing_high,
                "n_lower_synchrony_missing_outcome": missing_low,
                "mean_higher_synchrony": float(high.mean()) if n_high else float("nan"),
                "mean_lower_synchrony": float(low.mean()) if n_low else float("nan"),
                "sd_higher_synchrony": sd_high,
                "sd_lower_synchrony": sd_low,
                "eligible_smd": blocker == "",
                "blocker": blocker,
            }
        )
    return pd.DataFrame(rows)


def cardamine_smd_effects(
    exposure: pd.DataFrame,
    plant_summaries: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate all mathematically estimable year x ecotype Cardamine SMDs.

    The contrast is higher_synchrony minus lower_synchrony. All returned effects
    share one dependence cluster because they arise from the same Dibbinsdale
    2012-2014 programme.
    """
    audit = cardamine_smd_audit(exposure, plant_summaries)
    rows: list[dict[str, object]] = []
    for _, row in audit.loc[audit["eligible_smd"]].iterrows():
        g, variance = hedges_g_from_summary(
            mean_high=float(row["mean_higher_synchrony"]),
            sd_high=float(row["sd_higher_synchrony"]),
            n_high=int(row["n_higher_synchrony"]),
            mean_low=float(row["mean_lower_synchrony"]),
            sd_low=float(row["sd_lower_synchrony"]),
            n_low=int(row["n_lower_synchrony"]),
        )
        rows.append(
            {
                "year": row["year"],
                "ecotype": row["ecotype"],
                "effect_family": "standardized_mean_difference",
                "effect_native": g,
                "variance_native": variance,
                "n_higher_synchrony": int(row["n_higher_synchrony"]),
                "n_lower_synchrony": int(row["n_lower_synchrony"]),
                "dependence_id": DEPENDENCE_ID,
            }
        )
    return pd.DataFrame(rows)
