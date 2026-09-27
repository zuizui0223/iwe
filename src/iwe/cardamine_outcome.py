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
    "timing_group",
)
ALLOWED_GROUPS = {"early_refugium", "core_flight", "late_refugium"}
CONTRASTS = (
    ("core_vs_early", "core_flight", "early_refugium"),
    ("core_vs_late", "core_flight", "late_refugium"),
)
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
    """Audit core-flight versus each phenological refugium separately.

    Early and late escape are biologically distinct routes in the source study,
    so they are never pooled into one lower-synchrony group. A contrast is
    mathematically estimable only when both groups contain >=2 source-backed
    outcome observations and both group SDs are positive.
    """
    _require_columns(exposure, EXPOSURE_COLUMNS, "exposure")
    exp = exposure.loc[:, EXPOSURE_COLUMNS].copy()
    if exp.duplicated(["year", "ecotype", "plant_id"]).any():
        raise ValueError("exposure must be unique by year x ecotype x plant_id")
    unknown = sorted(set(exp["timing_group"].dropna()) - ALLOWED_GROUPS)
    if unknown:
        raise ValueError(f"unknown Cardamine timing groups: {unknown}")
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
        for contrast, high_group, low_group in CONTRASTS:
            high_all = group.loc[group["timing_group"] == high_group]
            low_all = group.loc[group["timing_group"] == low_group]
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
                    "contrast": contrast,
                    "high_group": high_group,
                    "low_group": low_group,
                    "n_high_total": n_high_total,
                    "n_low_total": n_low_total,
                    "n_high": n_high,
                    "n_low": n_low,
                    "n_high_missing_outcome": missing_high,
                    "n_low_missing_outcome": missing_low,
                    "mean_high": float(high.mean()) if n_high else float("nan"),
                    "mean_low": float(low.mean()) if n_low else float("nan"),
                    "sd_high": sd_high,
                    "sd_low": sd_low,
                    "eligible_smd": blocker == "",
                    "blocker": blocker,
                }
            )
    return pd.DataFrame(rows)


def cardamine_smd_effects(
    exposure: pd.DataFrame,
    plant_summaries: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate estimable core-flight versus refugium Cardamine SMDs.

    The contrast is always greater onset exposure to adult females (core_flight)
    minus one lower-exposure phenological refugium. Core-vs-early and
    core-vs-late remain separate rows and all rows share one dependence cluster.
    """
    audit = cardamine_smd_audit(exposure, plant_summaries)
    rows: list[dict[str, object]] = []
    for _, row in audit.loc[audit["eligible_smd"]].iterrows():
        g, variance = hedges_g_from_summary(
            mean_high=float(row["mean_high"]),
            sd_high=float(row["sd_high"]),
            n_high=int(row["n_high"]),
            mean_low=float(row["mean_low"]),
            sd_low=float(row["sd_low"]),
            n_low=int(row["n_low"]),
        )
        rows.append(
            {
                "year": row["year"],
                "ecotype": row["ecotype"],
                "contrast": row["contrast"],
                "high_group": row["high_group"],
                "low_group": row["low_group"],
                "effect_family": "standardized_mean_difference",
                "effect_native": g,
                "variance_native": variance,
                "n_high": int(row["n_high"]),
                "n_low": int(row["n_low"]),
                "dependence_id": DEPENDENCE_ID,
            }
        )
    return pd.DataFrame(rows)

