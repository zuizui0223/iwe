from __future__ import annotations

import math

import pandas as pd
from scipy.stats import t

from .schema import INTERACTION_TYPES


_CLASS_ORDER = [
    "mutualist",
    "antagonist",
    "mixed_pollinating_seed_predator",
]



def _single_effect_family(df: pd.DataFrame) -> str | None:
    if "effect_family" not in df.columns:
        return None
    families = sorted(set(df["effect_family"].dropna().astype(str)))
    if len(families) > 1:
        raise ValueError(
            "cannot pool multiple effect_family values without a registered conversion: "
            + ", ".join(families)
        )
    return families[0] if families else None


def fixed_effect_summary(df: pd.DataFrame, group_col: str = "interaction_type") -> pd.DataFrame:
    """Naive inverse-variance summary used only for low-level software checks.

    This function does not model cross-row dependence and must not be used for
    empirical IWE primary inference. The executable primary workflow uses
    cluster_robust_summary with dependence_id as the cluster.
    """
    rows: list[dict] = []
    for group, part in df.groupby(group_col, sort=False):
        weights = 1.0 / part["variance_native"].astype(float)
        effects = part["effect_oriented"].astype(float)
        weight_sum = float(weights.sum())
        estimate = float((weights * effects).sum() / weight_sum)
        se = math.sqrt(1.0 / weight_sum)
        q = float((weights * (effects - estimate) ** 2).sum())
        rows.append(
            {
                group_col: group,
                "effect_family": effect_family,
                "estimate": estimate,
                "se": se,
                "ci_low": estimate - 1.96 * se,
                "ci_high": estimate + 1.96 * se,
                "q": q,
                "k": int(len(part)),
                "method": "naive_inverse_variance_fixture_only",
            }
        )
    out = pd.DataFrame(rows)
    if group_col == "interaction_type" and not out.empty:
        order = {name: i for i, name in enumerate(_CLASS_ORDER)}
        out = out.sort_values(group_col, key=lambda s: s.map(order)).reset_index(drop=True)
    return out


def cluster_robust_summary(
    df: pd.DataFrame,
    group_col: str = "interaction_type",
    cluster_col: str = "dependence_id",
) -> pd.DataFrame:
    """Inverse-variance point estimate with CR1 cluster-robust uncertainty.

    dependence_id is the inferential replication unit. Correlation within a
    dependence cluster is left unrestricted by the sandwich variance. With only
    one cluster in a class, an estimate may be shown descriptively but no SE or
    confidence interval is produced.
    """
    effect_family = _single_effect_family(df)
    required = {group_col, cluster_col, "effect_oriented", "variance_native"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns for cluster-robust summary: {missing}")

    if df.empty:
        return pd.DataFrame(
            columns=[
                group_col,
                "effect_family",
                "estimate",
                "se",
                "ci_low",
                "ci_high",
                "k_effects",
                "m_dependence",
                "df",
                "method",
                "inferential_status",
            ]
        )

    if df[cluster_col].isna().any() or (df[cluster_col].astype(str).str.strip() == "").any():
        raise ValueError(f"{cluster_col} must be non-empty for cluster-robust inference")

    cluster_group_counts = df.groupby(cluster_col, dropna=False)[group_col].nunique()
    crossing = sorted(cluster_group_counts[cluster_group_counts > 1].index.astype(str))
    if crossing:
        raise ValueError(
            f"{cluster_col} cannot span multiple {group_col} values: {crossing}"
        )

    rows: list[dict[str, object]] = []
    for group, part in df.groupby(group_col, sort=False):
        weights = 1.0 / part["variance_native"].astype(float)
        effects = part["effect_oriented"].astype(float)
        weight_sum = float(weights.sum())
        estimate = float((weights * effects).sum() / weight_sum)
        residual = effects - estimate

        score = (weights * residual).groupby(part[cluster_col]).sum()
        m = int(score.shape[0])
        k = int(len(part))
        df_t = m - 1

        if m < 2:
            se = math.nan
            ci_low = math.nan
            ci_high = math.nan
            status = "insufficient_dependence_clusters"
        else:
            variance = (m / (m - 1.0)) * float((score**2).sum()) / (weight_sum**2)
            se = math.sqrt(max(variance, 0.0))
            critical = float(t.ppf(0.975, df=df_t))
            ci_low = estimate - critical * se
            ci_high = estimate + critical * se
            status = "ok"

        rows.append(
            {
                group_col: group,
                "estimate": estimate,
                "se": se,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "k_effects": k,
                "m_dependence": m,
                "df": df_t,
                "method": "inverse_variance_cr1_by_dependence_id",
                "inferential_status": status,
            }
        )

    out = pd.DataFrame(rows)
    if group_col == "interaction_type" and not out.empty:
        order = {name: i for i, name in enumerate(_CLASS_ORDER)}
        out = out.sort_values(group_col, key=lambda s: s.map(order)).reset_index(drop=True)
    return out


def class_contrasts(summary: pd.DataFrame) -> pd.DataFrame:
    """Return preregistered pairwise class contrasts.

    Contrast uncertainty combines class-level cluster-robust SEs using an
    independent-class approximation. The smaller class degrees of freedom is
    used for the t critical value. If either class lacks two dependence
    clusters, the contrast remains descriptive and carries no CI.
    """
    if summary.empty:
        return pd.DataFrame(
            columns=[
                "contrast",
                "estimate",
                "se",
                "ci_low",
                "ci_high",
                "df",
                "inferential_status",
            ]
        )
    if set(summary["interaction_type"]) - INTERACTION_TYPES:
        raise ValueError("summary contains unknown interaction_type")
    if "effect_family" in summary.columns:
        families = sorted(set(summary["effect_family"].dropna().astype(str)))
        if len(families) > 1:
            raise ValueError(
                "class contrasts require one common effect_family; observed: "
                + ", ".join(families)
            )

    lookup = {row["interaction_type"]: row for _, row in summary.iterrows()}
    pairs = [
        ("mutualist", "antagonist"),
        ("mutualist", "mixed_pollinating_seed_predator"),
        ("antagonist", "mixed_pollinating_seed_predator"),
    ]
    rows: list[dict[str, object]] = []
    for left, right in pairs:
        if left not in lookup or right not in lookup:
            continue
        estimate = float(lookup[left]["estimate"] - lookup[right]["estimate"])

        left_se = float(lookup[left]["se"])
        right_se = float(lookup[right]["se"])
        left_df = int(lookup[left].get("df", 0))
        right_df = int(lookup[right].get("df", 0))

        if math.isfinite(left_se) and math.isfinite(right_se) and min(left_df, right_df) >= 1:
            se = math.sqrt(left_se**2 + right_se**2)
            df_t = min(left_df, right_df)
            critical = float(t.ppf(0.975, df=df_t))
            ci_low = estimate - critical * se
            ci_high = estimate + critical * se
            status = "ok_independent_class_approximation"
        else:
            se = math.nan
            ci_low = math.nan
            ci_high = math.nan
            df_t = min(left_df, right_df)
            status = "insufficient_dependence_clusters"

        rows.append(
            {
                "contrast": f"{left} - {right}",
                "estimate": estimate,
                "se": se,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "df": df_t,
                "inferential_status": status,
            }
        )
    return pd.DataFrame(rows)
