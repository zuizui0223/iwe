from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd

from .effects import hedges_g_from_summary


PUBLISHED_RELATIVE_MEANS = (0.85, 1.00, 0.91, 0.69)
PUBLISHED_F = 1.01
PUBLISHED_N_PER_WEEK = 10


def _read_table(path: str | Path, sheet: str | int | None = None) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        book = pd.ExcelFile(path)
        if sheet is None:
            if len(book.sheet_names) != 1:
                raise ValueError(
                    "workbook has multiple sheets; choose one explicitly with --sheet. "
                    f"available={book.sheet_names}"
                )
            sheet = book.sheet_names[0]
        return pd.read_excel(path, sheet_name=sheet)
    if suffix == ".csv":
        if sheet is not None:
            raise ValueError("--sheet is only valid for Excel workbooks")
        return pd.read_csv(path)
    raise ValueError(f"unsupported input format: {path.suffix}")


def workbook_inventory(path: str | Path) -> pd.DataFrame:
    """Return sheet names, dimensions and column names without analyzing outcomes."""
    path = Path(path)
    suffix = path.suffix.lower()
    rows: list[dict[str, object]] = []
    if suffix in {".xlsx", ".xls"}:
        book = pd.ExcelFile(path)
        for sheet in book.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet)
            rows.append(
                {
                    "sheet": sheet,
                    "n_rows": int(len(df)),
                    "n_columns": int(len(df.columns)),
                    "columns": " | ".join(str(c) for c in df.columns),
                }
            )
        return pd.DataFrame(rows)

    if suffix == ".csv":
        df = pd.read_csv(path)
        return pd.DataFrame(
            [
                {
                    "sheet": "",
                    "n_rows": int(len(df)),
                    "n_columns": int(len(df.columns)),
                    "columns": " | ".join(str(c) for c in df.columns),
                }
            ]
        )
    raise ValueError(f"unsupported input format: {path.suffix}")


def _coerce_week_order(
    values: pd.Series,
    explicit_order: list[str] | tuple[str, ...] | None,
) -> tuple[list[object], pd.Series]:
    """Return four raw week values in temporal order and a normalized week index."""
    if values.isna().any():
        raise ValueError("week column must not contain missing values")

    raw_unique = list(pd.unique(values))
    if explicit_order is not None:
        order = list(explicit_order)
        if len(order) != 4:
            raise ValueError("week_order must contain exactly four values")
        mapping: dict[str, object] = {str(v): v for v in raw_unique}
        missing = [item for item in order if str(item) not in mapping]
        if missing:
            raise ValueError(f"week_order values not found in data: {missing}")
        ordered_raw = [mapping[str(item)] for item in order]
    else:
        if len(raw_unique) != 4:
            raise ValueError(
                "automatic week ordering requires exactly four unique values; "
                "otherwise provide --week-order"
            )
        numeric = pd.to_numeric(pd.Series(raw_unique), errors="coerce")
        if numeric.notna().all():
            ordered_raw = [
                item
                for _, item in sorted(zip(numeric.astype(float), raw_unique), key=lambda x: x[0])
            ]
        else:
            parsed: list[tuple[float, object]] = []
            for item in raw_unique:
                match = re.search(r"(\d+(?:\.\d+)?)", str(item))
                if not match:
                    raise ValueError(
                        "cannot infer temporal order from non-numeric week labels; "
                        "provide --week-order"
                    )
                parsed.append((float(match.group(1)), item))
            if len({number for number, _ in parsed}) != 4:
                raise ValueError(
                    "week labels do not contain four distinct numeric order values; "
                    "provide --week-order"
                )
            ordered_raw = [item for _, item in sorted(parsed)]

    if set(map(str, ordered_raw)) != set(map(str, raw_unique)):
        raise ValueError(
            "week_order must enumerate exactly the four observed week values"
        )
    to_index = {str(raw): i + 1 for i, raw in enumerate(ordered_raw)}
    normalized = values.map(lambda value: to_index[str(value)])
    return ordered_raw, normalized


def _plant_seed_set(
    df: pd.DataFrame,
    week_col: str,
    plant_col: str,
    seed_set_col: str | None,
    mature_seeds_col: str | None,
    flowers_col: str | None,
) -> pd.DataFrame:
    required = {week_col, plant_col}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    direct = seed_set_col is not None
    derived = mature_seeds_col is not None or flowers_col is not None
    if direct and derived:
        raise ValueError(
            "choose either --seed-set-col or the mature-seeds/flowers pair, not both"
        )
    if not direct:
        if mature_seeds_col is None or flowers_col is None:
            raise ValueError(
                "provide --seed-set-col or both --mature-seeds-col and --flowers-col"
            )

    if df[plant_col].isna().any():
        raise ValueError("plant identifier must not contain missing values")

    if direct:
        if seed_set_col not in df.columns:
            raise ValueError(f"missing seed-set column: {seed_set_col}")
        work = df.loc[:, [week_col, plant_col, seed_set_col]].copy()
        work[seed_set_col] = pd.to_numeric(work[seed_set_col], errors="raise")
        if work[seed_set_col].isna().any():
            raise ValueError("seed-set column must not contain missing values")

        rows: list[dict[str, object]] = []
        for (week, plant), group in work.groupby([week_col, plant_col], sort=False):
            values = group[seed_set_col].astype(float)
            if values.nunique(dropna=False) != 1:
                raise ValueError(
                    f"plant={plant} week={week}: repeated rows have conflicting seed-set values"
                )
            rows.append(
                {"raw_week": week, "plant_id": plant, "seed_set": float(values.iloc[0])}
            )
        out = pd.DataFrame(rows)
    else:
        assert mature_seeds_col is not None and flowers_col is not None
        for column in (mature_seeds_col, flowers_col):
            if column not in df.columns:
                raise ValueError(f"missing response column: {column}")
        work = df.loc[
            :, [week_col, plant_col, mature_seeds_col, flowers_col]
        ].copy()
        for column in (mature_seeds_col, flowers_col):
            work[column] = pd.to_numeric(work[column], errors="raise")
            if work[column].isna().any():
                raise ValueError(f"{column} must not contain missing values")
            if (work[column] < 0).any():
                raise ValueError(f"{column} must be non-negative")

        rows = []
        for (week, plant), group in work.groupby([week_col, plant_col], sort=False):
            flowers = float(group[flowers_col].sum())
            if flowers <= 0:
                raise ValueError(f"plant={plant} week={week}: flowers must sum to >0")
            seeds = float(group[mature_seeds_col].sum())
            rows.append(
                {
                    "raw_week": week,
                    "plant_id": plant,
                    "seed_set": seeds / flowers,
                }
            )
        out = pd.DataFrame(rows)

    if (out["seed_set"] < 0).any():
        raise ValueError("seed set must be non-negative")
    return out


def audit_iwe023_raw(
    path: str | Path,
    week_col: str,
    plant_col: str,
    seed_set_col: str | None = None,
    mature_seeds_col: str | None = None,
    flowers_col: str | None = None,
    sheet: str | int | None = None,
    week_order: list[str] | tuple[str, ...] | None = None,
    mean_tolerance: float = 0.02,
    f_tolerance: float = 0.03,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Reconstruct the published four-week experiment directly from plant-level data.

    The current IWE023 estimator is preserved: all four phenology groups define
    the common one-way-ANOVA residual variance, and week 1 versus week 4 is then
    standardized by that residual SD using the full residual degrees of freedom.
    """
    raw = _read_table(path, sheet=sheet)
    plant = _plant_seed_set(
        raw,
        week_col=week_col,
        plant_col=plant_col,
        seed_set_col=seed_set_col,
        mature_seeds_col=mature_seeds_col,
        flowers_col=flowers_col,
    )
    ordered_raw, normalized = _coerce_week_order(plant["raw_week"], week_order)
    plant = plant.copy()
    plant["week"] = normalized.astype(int)

    if plant.duplicated(["week", "plant_id"]).any():
        raise ValueError("plant-level normalized table must be unique by week x plant")

    rows: list[dict[str, object]] = []
    for week in range(1, 5):
        values = plant.loc[plant["week"] == week, "seed_set"].astype(float)
        if len(values) < 2:
            raise ValueError(f"week {week}: at least two plant responses are required")
        rows.append(
            {
                "week": week,
                "raw_week_value": ordered_raw[week - 1],
                "n": int(len(values)),
                "mean": float(values.mean()),
                "sd": float(values.std(ddof=1)),
                "se": float(values.std(ddof=1) / math.sqrt(len(values))),
            }
        )
    summary = pd.DataFrame(rows)

    total_n = int(summary["n"].sum())
    k = 4
    residual_df = total_n - k
    grand_mean = float(plant["seed_set"].mean())

    ss_between = 0.0
    ss_within = 0.0
    for week in range(1, 5):
        values = plant.loc[plant["week"] == week, "seed_set"].astype(float)
        group_mean = float(values.mean())
        ss_between += len(values) * (group_mean - grand_mean) ** 2
        ss_within += float(((values - group_mean) ** 2).sum())

    if residual_df <= 0 or ss_within <= 0:
        raise ValueError("raw experiment does not provide positive residual variance")
    ms_between = ss_between / (k - 1)
    ms_within = ss_within / residual_df
    f_statistic = ms_between / ms_within
    residual_sd = math.sqrt(ms_within)

    max_mean = float(summary["mean"].max())
    if max_mean <= 0:
        raise ValueError("raw group means must include a positive maximum")
    summary["mean_relative_to_max"] = summary["mean"] / max_mean
    summary["published_relative_mean"] = list(PUBLISHED_RELATIVE_MEANS)
    summary["relative_mean_matches"] = (
        summary["mean_relative_to_max"] - summary["published_relative_mean"]
    ).abs() <= float(mean_tolerance)
    summary["published_n"] = PUBLISHED_N_PER_WEEK
    summary["n_matches"] = summary["n"] == PUBLISHED_N_PER_WEEK

    high = summary.loc[summary["week"] == 1].iloc[0]
    low = summary.loc[summary["week"] == 4].iloc[0]
    g, variance = hedges_g_from_summary(
        mean_high=float(high["mean"]),
        sd_high=residual_sd,
        n_high=int(high["n"]),
        mean_low=float(low["mean"]),
        sd_low=residual_sd,
        n_low=int(low["n"]),
        standardizer_df=residual_df,
    )

    anova = pd.DataFrame(
        [
            {
                "total_n": total_n,
                "k_groups": k,
                "residual_df": residual_df,
                "grand_mean": grand_mean,
                "ss_between": ss_between,
                "ss_within": ss_within,
                "ms_between": ms_between,
                "ms_within": ms_within,
                "residual_sd": residual_sd,
                "f_statistic": f_statistic,
                "published_f": PUBLISHED_F,
                "f_matches": abs(f_statistic - PUBLISHED_F) <= float(f_tolerance),
            }
        ]
    )

    all_n = bool(summary["n_matches"].all())
    all_means = bool(summary["relative_mean_matches"].all())
    f_matches = bool(anova.iloc[0]["f_matches"])
    effect = pd.DataFrame(
        [
            {
                "effect_id": "IWE023_2015_W1_VS_W4_SEEDSET_SMD",
                "raw_effect_ready": bool(all_n and all_means and f_matches),
                "effect_native": g,
                "variance_native": variance,
                "n_week1": int(high["n"]),
                "n_week4": int(low["n"]),
                "residual_df": residual_df,
                "residual_sd": residual_sd,
                "raw_f_statistic": f_statistic,
                "published_f_statistic": PUBLISHED_F,
                "all_group_n_match": all_n,
                "all_relative_means_match": all_means,
                "f_matches": f_matches,
                "reason": (
                    "raw four-week plant-level experiment reproduces published n, "
                    "relative group means and ANOVA F"
                    if all_n and all_means and f_matches
                    else "raw experiment does not reproduce every frozen published check"
                ),
            }
        ]
    )
    return summary, anova, effect
