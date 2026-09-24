from __future__ import annotations

import math

from .schema import EXPOSURE_DIRECTIONS


def orient_effect(value: float, exposure_direction: str) -> float:
    """Orient an extracted effect so positive always means more synchrony -> higher reproduction."""
    if exposure_direction not in EXPOSURE_DIRECTIONS:
        raise ValueError(f"unknown exposure_direction: {exposure_direction}")
    return float(value) if exposure_direction == "synchrony" else -float(value)


def hedges_g_from_summary(
    mean_high: float,
    sd_high: float,
    n_high: int,
    mean_low: float,
    sd_low: float,
    n_low: int,
) -> tuple[float, float]:
    """Return Hedges g and its sampling variance from two independent summaries.

    The contrast is high-exposure minus low-exposure. The pooled-SD Cohen d is
    corrected with J = 1 - 3 / (4*df - 1). Sampling variance uses the same J
    correction applied to the conventional independent-groups variance of d.
    """
    if n_high < 2 or n_low < 2:
        raise ValueError("Hedges g requires at least two observations per group")
    if sd_high <= 0 or sd_low <= 0:
        raise ValueError("Hedges g requires positive group standard deviations")

    df = n_high + n_low - 2
    pooled_variance = (
        (n_high - 1) * float(sd_high) ** 2
        + (n_low - 1) * float(sd_low) ** 2
    ) / df
    pooled_sd = math.sqrt(pooled_variance)
    d = (float(mean_high) - float(mean_low)) / pooled_sd
    correction = 1.0 - 3.0 / (4.0 * df - 1.0)
    g = correction * d
    variance_d = (
        (n_high + n_low) / (n_high * n_low)
        + d**2 / (2.0 * df)
    )
    variance_g = correction**2 * variance_d
    return float(g), float(variance_g)



def hedges_g_from_mean_se(
    mean_high: float,
    se_high: float,
    n_high: int,
    mean_low: float,
    se_low: float,
    n_low: int,
) -> tuple[float, float]:
    """Return Hedges g when a source reports group means and standard errors.

    Standard deviations are reconstructed as SE * sqrt(n), then passed to the
    independent-groups Hedges-g implementation. The contrast remains
    high-exposure minus low-exposure.
    """
    if se_high <= 0 or se_low <= 0:
        raise ValueError("Hedges g from SE requires positive standard errors")
    sd_high = float(se_high) * math.sqrt(n_high)
    sd_low = float(se_low) * math.sqrt(n_low)
    return hedges_g_from_summary(
        mean_high=mean_high,
        sd_high=sd_high,
        n_high=n_high,
        mean_low=mean_low,
        sd_low=sd_low,
        n_low=n_low,
    )



def hedges_g_from_balanced_anova_means(
    group_means: list[float] | tuple[float, ...],
    n_per_group: int,
    f_statistic: float,
    high_index: int,
    low_index: int,
) -> tuple[float, float]:
    """Reconstruct Hedges g from balanced one-way ANOVA means and F.

    This is valid when the reported F tests the same outcome across all groups,
    every group has the same independent sample size, and the supplied means are
    on one common linear scale. Because an SMD is scale invariant, means may be
    reported after multiplication by one common positive constant (for example,
    relative to the largest group mean).

    The ANOVA identity F = MS_between / MS_within deterministically recovers the
    pooled within-group variance on that same scale. No missing variance is
    imputed and no regression coefficient is converted to an SMD.
    """
    means = [float(value) for value in group_means]
    if len(means) < 2:
        raise ValueError("balanced ANOVA reconstruction requires at least two groups")
    if n_per_group < 2:
        raise ValueError("balanced ANOVA reconstruction requires n_per_group >= 2")
    if not math.isfinite(float(f_statistic)) or float(f_statistic) <= 0:
        raise ValueError("balanced ANOVA reconstruction requires a positive finite F statistic")
    if any(not math.isfinite(value) for value in means):
        raise ValueError("balanced ANOVA reconstruction requires finite group means")
    if not (0 <= high_index < len(means)) or not (0 <= low_index < len(means)):
        raise ValueError("balanced ANOVA contrast index out of range")
    if high_index == low_index:
        raise ValueError("high_index and low_index must identify different groups")

    grand_mean = sum(means) / len(means)
    ss_between = n_per_group * sum((value - grand_mean) ** 2 for value in means)
    if ss_between <= 0:
        raise ValueError("balanced ANOVA reconstruction requires between-group variation")
    ms_between = ss_between / (len(means) - 1)
    ms_within = ms_between / float(f_statistic)
    pooled_sd = math.sqrt(ms_within)

    return hedges_g_from_summary(
        mean_high=means[high_index],
        sd_high=pooled_sd,
        n_high=n_per_group,
        mean_low=means[low_index],
        sd_low=pooled_sd,
        n_low=n_per_group,
    )
