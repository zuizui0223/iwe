from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd

from .effects import hedges_g_from_summary


EXPECTED_WEEKS = (1, 2, 3, 4)
EXPECTED_N_PER_WEEK = 10
PUBLISHED_F = 1.01
PUBLISHED_RESIDUAL_DF = 36
PUBLISHED_RELATIVE_MEANS = {
    1: 0.85,
    2: 1.00,
    3: 0.91,
    4: 0.69,
}


def _coerce_week(value: object) -> int:
    if pd.isna(value):
        raise ValueError("phenology week contains missing values")
    if isinstance(value, (int, float)) and float(value).is_integer():
        week = int(value)
    else:
        text = str(value).strip().lower()
        match = re.fullmatch(r"(?:week\s*)?([1-4])", text)
        if match is None:
            raise ValueError(
                f"cannot parse phenology week {value!r}; expected 1..4 or 'week 1'..'week 4'"
            )
        week = int(match.group(1))
    if week not in EXPECTED_WEEKS:
        raise ValueError(f"unexpected phenology week: {week}")
    return week


def _clean_plant_table(
    df: pd.DataFrame,
    week_col: str,
    seed_set_col: str,
    plant_id_col: str | None = None,
) -> pd.DataFrame:
    required = {week_col, seed_set_col}
    if plant_id_col is not None:
        required.add(plant_id_col)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing IWE023 raw columns: {missing}")

    columns = [week_col, seed_set_col]
    if plant_id_col is not None:
        columns.append(plant_id_col)
    out = df.loc[:, columns].copy()
    out["week"] = out[week_col].map(_coerce_week)
    out["seed_set"] = pd.to_numeric(out[seed_set_col], errors="raise")

    if out["seed_set"].isna().any():
        raise ValueError("seed-set column contains missing values")
    if not out["seed_set"].map(math.isfinite).all():
        raise ValueError("seed-set values must be finite")
    if (out["seed_set"] < 0).any():
        raise ValueError("seed-set values must be non-negative")

    if plant_id_col is not None:
        if out[plant_id_col].isna().any():
            raise ValueError("plant ID contains missing values")
        ids = out[plant_id_col].astype(str)
        if pd.DataFrame({"week": out["week"], "plant_id": ids}).duplicated(
            ["week", "plant_id"]
        ).any():
            raise ValueError(
                "plant ID must be unique within phenology week in the IWE023 plant-level table"
            )

    return out


def _group_summary(table: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for week in EXPECTED_WEEKS:
        values = table.loc[table["week"] == week, "seed_set"]
        if values.empty:
            rows.append(
                {
                    "week": week,
                    "n": 0,
                    "mean": math.nan,
                    "sd": math.nan,
                    "published_relative_mean": PUBLISHED_RELATIVE_MEANS[week],
                }
            )
            continue
        rows.append(
            {
                "week": week,
                "n": int(len(values)),
                "mean": float(values.mean()),
                "sd": float(values.std(ddof=1)) if len(values) >= 2 else math.nan,
                "published_relative_mean": PUBLISHED_RELATIVE_MEANS[week],
            }
        )
    summary = pd.DataFrame(rows)
    maximum = float(summary["mean"].max())
    summary["relative_mean"] = summary["mean"] / maximum if maximum > 0 else math.nan
    summary["n_matches"] = summary["n"] == EXPECTED_N_PER_WEEK
    summary["relative_mean_difference"] = (
        summary["relative_mean"] - summary["published_relative_mean"]
    )
    return summary


def _anova_from_raw(table: pd.DataFrame) -> dict[str, float | int]:
    n_total = int(len(table))
    k = len(EXPECTED_WEEKS)
    residual_df = n_total - k

    means = table.groupby("week")["seed_set"].mean()
    grand_mean = float(table["seed_set"].mean())
    ss_between = 0.0
    ss_within = 0.0
    for week in EXPECTED_WEEKS:
        values = table.loc[table["week"] == week, "seed_set"]
        if values.empty:
            raise ValueError(f"week {week} has no raw observations")
        mean = float(means.loc[week])
        ss_between += len(values) * (mean - grand_mean) ** 2
        ss_within += float(((values - mean) ** 2).sum())

    if residual_df <= 0:
        raise ValueError("raw IWE023 table has no residual degrees of freedom")
    ms_between = ss_between / (k - 1)
    ms_within = ss_within / residual_df
    f_statistic = ms_between / ms_within if ms_within > 0 else math.inf
    return {
        "n_total": n_total,
        "residual_df": residual_df,
        "ss_between": ss_between,
        "ss_within": ss_within,
        "ms_between": ms_between,
        "ms_within": ms_within,
        "residual_sd": math.sqrt(ms_within),
        "f_statistic": f_statistic,
    }


def audit_iwe023_dataframe(
    df: pd.DataFrame,
    week_col: str,
    seed_set_col: str,
    plant_id_col: str | None = None,
    relative_mean_tolerance: float = 0.015,
    f_tolerance: float = 0.08,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Audit plant-level IWE023 raw data and reconstruct the frozen week-1 vs week-4 SMD.

    The primary raw reconstruction preserves the current IWE023 estimand:
    week 1 minus week 4, standardized by the common within-week residual SD
    estimated from all four balanced experimental groups (residual df=36).

    A contrast-only week-1/week-4 Hedges-g sensitivity is returned separately.
    """
    table = _clean_plant_table(df, week_col, seed_set_col, plant_id_col)
    summary = _group_summary(table)
    anova = _anova_from_raw(table)

    groups_present = set(table["week"].unique()) == set(EXPECTED_WEEKS)
    n_match = bool(summary["n_matches"].all())
    df_match = int(anova["residual_df"]) == PUBLISHED_RESIDUAL_DF
    means_match = bool(
        summary["relative_mean_difference"].abs().le(relative_mean_tolerance).all()
    )
    f_match = abs(float(anova["f_statistic"]) - PUBLISHED_F) <= f_tolerance
    ready = groups_present and n_match and df_match and means_match and f_match

    summary["expected_n"] = EXPECTED_N_PER_WEEK
    summary["published_f"] = PUBLISHED_F
    summary["raw_f"] = float(anova["f_statistic"])
    summary["raw_residual_sd"] = float(anova["residual_sd"])
    summary["raw_residual_df"] = int(anova["residual_df"])
    summary["raw_design_ready"] = ready

    week1 = table.loc[table["week"] == 1, "seed_set"]
    week4 = table.loc[table["week"] == 4, "seed_set"]

    rows: list[dict[str, object]] = []
    if ready:
        common_sd = float(anova["residual_sd"])
        g_common, var_common = hedges_g_from_summary(
            mean_high=float(week1.mean()),
            sd_high=common_sd,
            n_high=len(week1),
            mean_low=float(week4.mean()),
            sd_low=common_sd,
            n_low=len(week4),
            standardizer_df=int(anova["residual_df"]),
        )
        g_pair, var_pair = hedges_g_from_summary(
            mean_high=float(week1.mean()),
            sd_high=float(week1.std(ddof=1)),
            n_high=len(week1),
            mean_low=float(week4.mean()),
            sd_low=float(week4.std(ddof=1)),
            n_low=len(week4),
        )
        rows.append(
            {
                "contrast": "week1_minus_week4",
                "raw_effect_ready": True,
                "primary_standardizer": "all_four_week_common_residual_sd",
                "effect_native": g_common,
                "variance_native": var_common,
                "contrast_only_g_sensitivity": g_pair,
                "contrast_only_variance_sensitivity": var_pair,
                "residual_df": int(anova["residual_df"]),
                "raw_f": float(anova["f_statistic"]),
                "reason": "raw plant-level data reproduce the published balanced four-week design",
            }
        )
    else:
        blockers: list[str] = []
        if not groups_present:
            blockers.append("weeks 1-4 not all present")
        if not n_match:
            blockers.append("n != 10 in one or more weeks")
        if not df_match:
            blockers.append("residual df != 36")
        if not means_match:
            blockers.append("relative group means do not reproduce published values")
        if not f_match:
            blockers.append("raw F does not reproduce published F=1.01")
        rows.append(
            {
                "contrast": "week1_minus_week4",
                "raw_effect_ready": False,
                "primary_standardizer": "all_four_week_common_residual_sd",
                "effect_native": math.nan,
                "variance_native": math.nan,
                "contrast_only_g_sensitivity": math.nan,
                "contrast_only_variance_sensitivity": math.nan,
                "residual_df": int(anova["residual_df"]),
                "raw_f": float(anova["f_statistic"]),
                "reason": "; ".join(blockers),
            }
        )

    return summary, pd.DataFrame(rows)


def audit_iwe023_workbook(
    path: str | Path,
    week_col: str,
    seed_set_col: str,
    plant_id_col: str | None = None,
    sheet_name: str | int = 0,
    relative_mean_tolerance: float = 0.015,
    f_tolerance: float = 0.08,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load one workbook sheet and run the non-promoting IWE023 raw audit."""
    df = pd.read_excel(Path(path), sheet_name=sheet_name)
    return audit_iwe023_dataframe(
        df,
        week_col=week_col,
        seed_set_col=seed_set_col,
        plant_id_col=plant_id_col,
        relative_mean_tolerance=relative_mean_tolerance,
        f_tolerance=f_tolerance,
    )
