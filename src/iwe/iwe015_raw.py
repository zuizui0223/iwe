from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from .effects import hedges_g_from_summary


SOURCE_SUCCESSFUL_FRUITS_COL = "ft"

PUBLISHED_IWE015 = {
    "2012_early": {
        "year": 2012,
        "window": "early",
        "n": 59,
        "successful_fruits_mean": 2.66,
        "successful_fruits_dispersion": 2.95,
        "fruit_initiation_mean": 0.91,
        "fruit_initiation_dispersion": 0.19,
        "predation_rate_mean": 0.59,
        "predation_rate_dispersion": 0.36,
    },
    "2012_late": {
        "year": 2012,
        "window": "late",
        "n": 58,
        "successful_fruits_mean": 3.91,
        "successful_fruits_dispersion": 4.13,
        "fruit_initiation_mean": 0.92,
        "fruit_initiation_dispersion": 0.19,
        "predation_rate_mean": 0.41,
        "predation_rate_dispersion": 0.35,
    },
    "2013_early": {
        "year": 2013,
        "window": "early",
        "n": 55,
        "successful_fruits_mean": 9.77,
        "successful_fruits_dispersion": 6.91,
        "fruit_initiation_mean": 0.93,
        "fruit_initiation_dispersion": 0.10,
        "predation_rate_mean": 0.20,
        "predation_rate_dispersion": 0.30,
    },
    "2013_late": {
        "year": 2013,
        "window": "late",
        "n": 55,
        "successful_fruits_mean": 8.60,
        "successful_fruits_dispersion": 7.01,
        "fruit_initiation_mean": 0.93,
        "fruit_initiation_dispersion": 0.10,
        "predation_rate_mean": 0.19,
        "predation_rate_dispersion": 0.24,
    },
}


def _numeric_values(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        raise ValueError(f"missing column: {column}")
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if len(values) < 2:
        raise ValueError(f"{column}: at least two non-missing values are required")
    return values.astype(float)


def summarize_column(df: pd.DataFrame, column: str) -> dict[str, float | int]:
    """Return n, mean, sample SD and SE for one raw column."""
    values = _numeric_values(df, column)
    sd = float(values.std(ddof=1))
    return {
        "n": int(len(values)),
        "mean": float(values.mean()),
        "sd": sd,
        "se": sd / math.sqrt(len(values)),
    }


def printed_dispersion_match(
    raw_sd: float,
    raw_se: float,
    printed_dispersion: float,
    tolerance: float = 0.0051,
) -> str:
    """Classify whether a rounded printed dispersion matches raw SD or raw SE."""
    sd_match = abs(float(raw_sd) - float(printed_dispersion)) <= tolerance
    se_match = abs(float(raw_se) - float(printed_dispersion)) <= tolerance
    if sd_match and se_match:
        return "ambiguous"
    if sd_match:
        return "sd"
    if se_match:
        return "se"
    return "neither"


def bounded_dispersion_check(
    mean: float,
    printed_dispersion: float,
    n: int,
    lower: float = 0.0,
    upper: float = 1.0,
    tolerance: float = 1e-12,
) -> dict[str, float | bool]:
    """Check whether a printed dispersion can be an SD or SE for bounded data.

    Bhatia-Davis gives Var(X) <= (upper - mean) * (mean - lower) for a variable
    bounded to [lower, upper]. Interpreting a printed value as an SE implies
    SD = SE * sqrt(n). This provides a distribution-free impossibility check.
    """
    mean = float(mean)
    printed_dispersion = float(printed_dispersion)
    if n < 2:
        raise ValueError("bounded dispersion check requires n >= 2")
    if not lower <= mean <= upper:
        raise ValueError("mean must lie within the declared bounds")
    max_sd = math.sqrt(max(0.0, (upper - mean) * (mean - lower)))
    implied_sd_if_se = printed_dispersion * math.sqrt(n)
    return {
        "max_possible_sd": max_sd,
        "printed_as_sd_possible": printed_dispersion <= max_sd + tolerance,
        "implied_sd_if_printed_is_se": implied_sd_if_se,
        "printed_as_se_possible": implied_sd_if_se <= max_sd + tolerance,
    }


def audit_iwe015_group(
    df: pd.DataFrame,
    group: str,
    successful_fruits_col: str = SOURCE_SUCCESSFUL_FRUITS_COL,
    fruit_initiation_col: str | None = None,
    predation_rate_col: str | None = None,
    rounding_tolerance: float = 0.0051,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Audit one Dryad female file against the published Table 1 row."""
    if group not in PUBLISHED_IWE015:
        raise ValueError(f"unknown IWE015 group: {group}")
    published = PUBLISHED_IWE015[group]
    sf_values = _numeric_values(df, successful_fruits_col)
    if (sf_values < 0).any():
        raise ValueError("successful fruits must be non-negative")
    sf = summarize_column(df, successful_fruits_col)

    row: dict[str, object] = {
        "group": group,
        "year": published["year"],
        "window": published["window"],
        "expected_n": published["n"],
        "raw_n": sf["n"],
        "n_matches": sf["n"] == published["n"],
        "published_successful_fruits_mean": published["successful_fruits_mean"],
        "raw_successful_fruits_mean": sf["mean"],
        "mean_matches": abs(
            float(sf["mean"]) - float(published["successful_fruits_mean"])
        )
        <= rounding_tolerance,
        "published_successful_fruits_dispersion": published[
            "successful_fruits_dispersion"
        ],
        "raw_successful_fruits_sd": sf["sd"],
        "raw_successful_fruits_se": sf["se"],
        "printed_dispersion_matches": printed_dispersion_match(
            float(sf["sd"]),
            float(sf["se"]),
            float(published["successful_fruits_dispersion"]),
            tolerance=rounding_tolerance,
        ),
    }
    row["raw_group_ready"] = bool(
        row["n_matches"]
        and row["mean_matches"]
        and math.isfinite(float(sf["sd"]))
        and float(sf["sd"]) > 0
    )

    component_rows: list[dict[str, object]] = []
    specs = [
        (
            "fruit_initiation",
            fruit_initiation_col,
            "fruit_initiation_mean",
            "fruit_initiation_dispersion",
        ),
        (
            "predation_rate",
            predation_rate_col,
            "predation_rate_mean",
            "predation_rate_dispersion",
        ),
    ]
    for component, column, mean_key, dispersion_key in specs:
        if column is None:
            continue
        bounded_values = _numeric_values(df, column)
        if ((bounded_values < 0) | (bounded_values > 1)).any():
            raise ValueError(f"{column}: bounded proportion values must lie in [0, 1]")
        raw = summarize_column(df, column)
        bounded = bounded_dispersion_check(
            float(published[mean_key]),
            float(published[dispersion_key]),
            int(published["n"]),
        )
        component_rows.append(
            {
                "group": group,
                "component": component,
                "column": column,
                "expected_n": published["n"],
                "raw_n": raw["n"],
                "published_mean": published[mean_key],
                "raw_mean": raw["mean"],
                "published_dispersion": published[dispersion_key],
                "raw_sd": raw["sd"],
                "raw_se": raw["se"],
                "printed_dispersion_matches": printed_dispersion_match(
                    float(raw["sd"]),
                    float(raw["se"]),
                    float(published[dispersion_key]),
                    tolerance=rounding_tolerance,
                ),
                **bounded,
            }
        )
    return row, component_rows


def audit_iwe015_raw_files(
    files: dict[str, str | Path],
    successful_fruits_col: str,
    fruit_initiation_col: str | None = None,
    predation_rate_col: str | None = None,
    rounding_tolerance: float = 0.0051,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Audit all four female files and reconstruct year-specific raw Hedges g.

    The function is non-promoting. It produces:
    - one row per published experiment for sample-size/mean/dispersion checks;
    - optional bounded-component checks;
    - one raw early-minus-late Hedges-g row per year when both group audits pass.
    """
    missing = sorted(set(PUBLISHED_IWE015) - set(files))
    extra = sorted(set(files) - set(PUBLISHED_IWE015))
    if missing or extra:
        raise ValueError(f"file mapping mismatch; missing={missing}, extra={extra}")

    audit_rows: list[dict[str, object]] = []
    component_rows: list[dict[str, object]] = []
    raw_summaries: dict[str, dict[str, float | int]] = {}

    for group in PUBLISHED_IWE015:
        df = pd.read_csv(Path(files[group]))
        audit, components = audit_iwe015_group(
            df,
            group,
            successful_fruits_col=successful_fruits_col,
            fruit_initiation_col=fruit_initiation_col,
            predation_rate_col=predation_rate_col,
            rounding_tolerance=rounding_tolerance,
        )
        audit_rows.append(audit)
        component_rows.extend(components)
        raw_summaries[group] = summarize_column(df, successful_fruits_col)

    audit_df = pd.DataFrame(audit_rows)
    components_df = pd.DataFrame(component_rows)

    effect_rows: list[dict[str, object]] = []
    for year in (2012, 2013):
        early_key = f"{year}_early"
        late_key = f"{year}_late"
        early_audit = audit_df.loc[audit_df["group"] == early_key].iloc[0]
        late_audit = audit_df.loc[audit_df["group"] == late_key].iloc[0]
        ready = bool(early_audit["raw_group_ready"] and late_audit["raw_group_ready"])
        if not ready:
            effect_rows.append(
                {
                    "year": year,
                    "raw_effect_ready": False,
                    "effect_native": math.nan,
                    "variance_native": math.nan,
                    "n_early": int(raw_summaries[early_key]["n"]),
                    "n_late": int(raw_summaries[late_key]["n"]),
                    "reason": "raw n/mean does not reproduce the published experiment row",
                }
            )
            continue

        early = raw_summaries[early_key]
        late = raw_summaries[late_key]
        g, variance = hedges_g_from_summary(
            mean_high=float(early["mean"]),
            sd_high=float(early["sd"]),
            n_high=int(early["n"]),
            mean_low=float(late["mean"]),
            sd_low=float(late["sd"]),
            n_low=int(late["n"]),
        )
        effect_rows.append(
            {
                "year": year,
                "raw_effect_ready": True,
                "effect_native": g,
                "variance_native": variance,
                "n_early": int(early["n"]),
                "n_late": int(late["n"]),
                "reason": "raw Dryad successful-fruit values reproduce published n and rounded means",
            }
        )

    return audit_df, components_df, pd.DataFrame(effect_rows)
