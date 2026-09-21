from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd
from scipy.stats import t


_REQUIRED_COLUMNS = {
    "state",
    "partner_availability",
    "mean_filled_seed_pct",
    "ci95_low_pct",
    "ci95_high_pct",
    "n_clones",
}


@dataclass(frozen=True)
class IWE084Effect:
    n_low: int
    n_high: int
    theta_low: float
    theta_high: float
    sd_low: float
    sd_high: float
    pooled_sd: float
    cohen_d: float
    hedges_j: float
    hedges_g: float
    variance_native: float


def angular_transform_percent(value: float) -> float:
    """Source angular transform for a percentage/proportion outcome."""
    p = float(value) / 100.0
    if not 0.0 <= p <= 1.0:
        raise ValueError("percentage must lie in [0, 100]")
    return math.asin(math.sqrt(p))


def _hedges_correction(df: int) -> float:
    if df <= 1:
        raise ValueError("Hedges correction requires df > 1")
    # Exact gamma-ratio correction, evaluated on the log scale.
    return math.exp(
        math.lgamma(df / 2.0)
        - 0.5 * math.log(df / 2.0)
        - math.lgamma((df - 1.0) / 2.0)
    )


def _recover_group(row: pd.Series) -> tuple[int, float, float]:
    n = int(row["n_clones"])
    if n < 2:
        raise ValueError("each IWE084 group requires at least two clones")

    mean = angular_transform_percent(row["mean_filled_seed_pct"])
    low = angular_transform_percent(row["ci95_low_pct"])
    high = angular_transform_percent(row["ci95_high_pct"])

    if not low < mean < high:
        raise ValueError("published CI must bracket the transformed mean")

    lower_width = mean - low
    upper_width = high - mean

    # Back-transformation plus printed rounding creates tiny asymmetry.
    # Large asymmetry would mean the source cannot be inverted under the
    # preregistered angular-CI route.
    mean_width = (lower_width + upper_width) / 2.0
    if abs(lower_width - upper_width) > max(0.002, 0.05 * mean_width):
        raise ValueError("transformed CI is not symmetric enough to invert")

    critical = float(t.ppf(0.975, df=n - 1))
    se = mean_width / critical
    sd = se * math.sqrt(n)
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("recovered transformed SD must be finite and positive")
    return n, mean, sd


def reconstruct_iwe084(source_rows: pd.DataFrame) -> IWE084Effect:
    """Reconstruct the frozen early/late S. graminifolia Hedges-g effect."""
    missing = _REQUIRED_COLUMNS - set(source_rows.columns)
    if missing:
        raise ValueError(f"missing IWE084 source columns: {sorted(missing)}")

    if len(source_rows) != 2:
        raise ValueError("IWE084 primary reconstruction requires exactly two source rows")

    rows = source_rows.copy()
    if set(rows["state"].astype(str)) != {"low", "high"}:
        raise ValueError("IWE084 states must be exactly low/high")
    if set(rows["partner_availability"].astype(str)) != {"lower", "higher"}:
        raise ValueError("IWE084 partner availability must be lower/higher")

    low_row = rows.loc[rows["state"].astype(str) == "low"].iloc[0]
    high_row = rows.loc[rows["state"].astype(str) == "high"].iloc[0]

    n_low, theta_low, sd_low = _recover_group(low_row)
    n_high, theta_high, sd_high = _recover_group(high_row)

    df = n_low + n_high - 2
    pooled_sd = math.sqrt(
        ((n_low - 1) * sd_low**2 + (n_high - 1) * sd_high**2) / df
    )
    d = (theta_high - theta_low) / pooled_sd
    j = _hedges_correction(df)
    g = j * d

    variance_d = (
        (n_low + n_high) / (n_low * n_high)
        + d**2 / (2.0 * df)
    )
    variance_g = j**2 * variance_d

    return IWE084Effect(
        n_low=n_low,
        n_high=n_high,
        theta_low=theta_low,
        theta_high=theta_high,
        sd_low=sd_low,
        sd_high=sd_high,
        pooled_sd=pooled_sd,
        cohen_d=d,
        hedges_j=j,
        hedges_g=g,
        variance_native=variance_g,
    )
