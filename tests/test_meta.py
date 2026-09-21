import math

import pandas as pd
import pytest

from iwe.meta import class_contrasts, cluster_robust_summary, fixed_effect_summary


def test_fixed_effect_summary_uses_inverse_variance_weights():
    df = pd.DataFrame(
        [
            {"interaction_type": "mutualist", "effect_oriented": 0.2, "variance_native": 0.04},
            {"interaction_type": "mutualist", "effect_oriented": 0.4, "variance_native": 0.01},
        ]
    )
    out = fixed_effect_summary(df)
    row = out.iloc[0]
    assert row["estimate"] == pytest.approx(0.36)
    assert row["se"] == pytest.approx((1 / 125) ** 0.5)
    assert row["k"] == 2
    assert row["method"] == "naive_inverse_variance_fixture_only"


def test_cluster_robust_summary_uses_dependence_id_as_replication_unit():
    df = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.2,
                "variance_native": 0.04,
            },
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.4,
                "variance_native": 0.04,
            },
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP2",
                "effect_oriented": 0.8,
                "variance_native": 0.04,
            },
        ]
    )
    row = cluster_robust_summary(df).iloc[0]
    assert row["estimate"] == pytest.approx((0.2 + 0.4 + 0.8) / 3)
    assert row["k_effects"] == 3
    assert row["m_dependence"] == 2
    assert row["df"] == 1
    assert row["inferential_status"] == "ok"
    assert math.isfinite(row["se"])


def test_one_dependence_cluster_never_gets_inferential_ci():
    df = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.2,
                "variance_native": 0.04,
            },
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.4,
                "variance_native": 0.01,
            },
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.8,
                "variance_native": 0.09,
            },
        ]
    )
    row = cluster_robust_summary(df).iloc[0]
    assert row["k_effects"] == 3
    assert row["m_dependence"] == 1
    assert row["inferential_status"] == "insufficient_dependence_clusters"
    assert math.isnan(row["se"])
    assert math.isnan(row["ci_low"])
    assert math.isnan(row["ci_high"])


def test_dependence_cluster_cannot_cross_interaction_classes():
    df = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_oriented": 0.2,
                "variance_native": 0.04,
            },
            {
                "interaction_type": "antagonist",
                "dependence_id": "DEP1",
                "effect_oriented": -0.2,
                "variance_native": 0.04,
            },
        ]
    )
    with pytest.raises(ValueError, match="cannot span multiple"):
        cluster_robust_summary(df)


def test_class_contrasts_return_preregistered_pairs():
    summary = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "estimate": 0.3,
                "se": 0.1,
                "df": 4,
            },
            {
                "interaction_type": "antagonist",
                "estimate": -0.2,
                "se": 0.1,
                "df": 4,
            },
            {
                "interaction_type": "mixed_pollinating_seed_predator",
                "estimate": 0.05,
                "se": 0.1,
                "df": 4,
            },
        ]
    )
    out = class_contrasts(summary)
    assert set(out["contrast"]) == {
        "mutualist - antagonist",
        "mutualist - mixed_pollinating_seed_predator",
        "antagonist - mixed_pollinating_seed_predator",
    }
    ma = out.loc[out["contrast"] == "mutualist - antagonist"].iloc[0]
    assert ma["estimate"] == pytest.approx(0.5)
    assert ma["inferential_status"] == "ok_independent_class_approximation"


def test_class_contrast_with_single_cluster_class_has_no_ci():
    summary = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "estimate": 0.3,
                "se": math.nan,
                "df": 0,
            },
            {
                "interaction_type": "antagonist",
                "estimate": -0.2,
                "se": 0.1,
                "df": 4,
            },
        ]
    )
    row = class_contrasts(summary).iloc[0]
    assert row["estimate"] == pytest.approx(0.5)
    assert row["inferential_status"] == "insufficient_dependence_clusters"
    assert math.isnan(row["ci_low"])


def test_cluster_robust_summary_refuses_mixed_effect_families_without_conversion():
    df = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_family": "fisher_z",
                "effect_oriented": 0.2,
                "variance_native": 0.04,
            },
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP2",
                "effect_family": "log_odds_ratio",
                "effect_oriented": 0.4,
                "variance_native": 0.04,
            },
        ]
    )
    with pytest.raises(ValueError, match="cannot pool multiple effect_family"):
        cluster_robust_summary(df)


def test_cluster_robust_summary_reports_common_effect_family():
    df = pd.DataFrame(
        [
            {
                "interaction_type": "mutualist",
                "dependence_id": "DEP1",
                "effect_family": "log_odds_ratio",
                "effect_oriented": 1.55,
                "variance_native": 0.0625,
            }
        ]
    )
    row = cluster_robust_summary(df).iloc[0]
    assert row["effect_family"] == "log_odds_ratio"
    assert row["estimate"] == pytest.approx(1.55)
    assert row["inferential_status"] == "insufficient_dependence_clusters"
