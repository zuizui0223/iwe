from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import t

from .schema import INTERACTION_TYPES


MIN_REFERENCE_DF = 4

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


def _reml_tau2(effects: np.ndarray, variances: np.ndarray) -> float:
    """Estimate working-model between-effect heterogeneity by REML."""
    if effects.size < 2:
        return 0.0

    def objective(tau2: float) -> float:
        total_variance = variances + float(tau2)
        weights = 1.0 / total_variance
        weight_sum = float(weights.sum())
        estimate = float((weights * effects).sum() / weight_sum)
        q = float((weights * (effects - estimate) ** 2).sum())
        return float(np.log(total_variance).sum() + math.log(weight_sum) + q)

    observed_variance = float(np.var(effects, ddof=1)) if effects.size > 1 else 0.0
    upper = max(1.0, 100.0 * observed_variance, 100.0 * float(variances.max()))
    result = minimize_scalar(
        objective,
        bounds=(0.0, upper),
        method="bounded",
        options={"xatol": 1e-12},
    )
    candidate = float(result.x)
    if objective(0.0) <= objective(candidate) + 1e-10:
        return 0.0
    return max(candidate, 0.0)


def _cr2_intercept_se(
    effects: np.ndarray,
    variances: np.ndarray,
    clusters: np.ndarray,
    tau2: float,
) -> tuple[float, float]:
    """Return the random-effects intercept and CR2 cluster-robust SE.

    The CR2 adjustment is applied in the whitened working-model space with
    inverse-(sampling variance + tau2) weights. Within-cluster covariance is
    otherwise left unrestricted.
    """
    weights = 1.0 / (variances + float(tau2))
    weight_sum = float(weights.sum())
    estimate = float((weights * effects).sum() / weight_sum)
    sqrt_weights = np.sqrt(weights)
    whitened_residuals = sqrt_weights * (effects - estimate)

    meat = 0.0
    for cluster in pd.unique(clusters):
        index = np.flatnonzero(clusters == cluster)
        x_cluster = sqrt_weights[index]
        leverage = np.outer(x_cluster, x_cluster) / weight_sum
        residual_maker = np.eye(len(index)) - leverage
        eigenvalues, eigenvectors = np.linalg.eigh(residual_maker)
        if float(eigenvalues.min()) <= 1e-12:
            raise ValueError("CR2 adjustment is singular for a dependence cluster")
        adjustment = (
            eigenvectors
            @ np.diag(1.0 / np.sqrt(eigenvalues))
            @ eigenvectors.T
        )
        adjusted_score = float(
            x_cluster @ (adjustment @ whitened_residuals[index])
        )
        meat += adjusted_score**2

    variance = meat / (weight_sum**2)
    return estimate, math.sqrt(max(float(variance), 0.0))


def cluster_robust_summary(
    df: pd.DataFrame,
    group_col: str = "interaction_type",
    cluster_col: str = "dependence_id",
) -> pd.DataFrame:
    """Random-effects REML summary with CR2 dependence-robust uncertainty.

    dependence_id is the inferential replication unit. REML supplies a working
    between-effect heterogeneity variance once at least two independent
    dependence clusters exist. CR2 then leaves within-cluster covariance
    unrestricted. Reference inference is withheld whenever the conservative
    cluster degrees of freedom m-1 is below MIN_REFERENCE_DF (=4), because
    RVE has too little information for trustworthy small-sample inference.
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
                "tau2",
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
        effects = part["effect_oriented"].astype(float).to_numpy()
        variances = part["variance_native"].astype(float).to_numpy()
        clusters = part[cluster_col].astype(str).to_numpy()
        if (variances <= 0).any() or not np.isfinite(variances).all():
            raise ValueError("variance_native must be finite and positive")
        if not np.isfinite(effects).all():
            raise ValueError("effect_oriented must be finite")

        m = int(pd.Series(clusters).nunique())
        k = int(len(part))
        df_t = m - 1
        tau2 = _reml_tau2(effects, variances) if m >= 2 else 0.0

        weights = 1.0 / (variances + tau2)
        estimate = float((weights * effects).sum() / weights.sum())

        if df_t < MIN_REFERENCE_DF:
            se = math.nan
            ci_low = math.nan
            ci_high = math.nan
            status = "insufficient_cluster_information"
        else:
            estimate, se = _cr2_intercept_se(effects, variances, clusters, tau2)
            critical = float(t.ppf(0.975, df=df_t))
            ci_low = estimate - critical * se
            ci_high = estimate + critical * se
            status = "ok"

        rows.append(
            {
                group_col: group,
                "effect_family": effect_family,
                "estimate": estimate,
                "se": se,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "tau2": tau2,
                "k_effects": k,
                "m_dependence": m,
                "df": df_t,
                "method": "random_effects_reml_cr2_by_dependence_id",
                "inferential_status": status,
            }
        )

    out = pd.DataFrame(rows)
    if group_col == "interaction_type" and not out.empty:
        order = {name: i for i, name in enumerate(_CLASS_ORDER)}
        out = out.sort_values(group_col, key=lambda series: series.map(order)).reset_index(drop=True)
    return out

def class_contrasts(summary: pd.DataFrame) -> pd.DataFrame:
    """Return preregistered pairwise class contrasts.

    Contrast uncertainty combines class-level cluster-robust SEs using an
    independent-class approximation. The smaller class degrees of freedom is
    used for the t critical value. If either class lacks two dependence
    clusters or either class falls below the reference information floor, the contrast remains descriptive and carries no CI.
    """
    if summary.empty:
        return pd.DataFrame(
            columns=[
                "effect_family",
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
    effect_family = None
    if "effect_family" in summary.columns:
        families = sorted(set(summary["effect_family"].dropna().astype(str)))
        if len(families) > 1:
            raise ValueError(
                "class contrasts require one common effect_family; observed: "
                + ", ".join(families)
            )
        effect_family = families[0] if families else None

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
            status = "insufficient_cluster_information"

        rows.append(
            {
                "effect_family": effect_family,
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
