import pandas as pd
import pytest

from iwe.replication import replication_target_status


def _row(interaction_type, dependence_id, effect_family="standardized_mean_difference"):
    return {
        "interaction_type": interaction_type,
        "dependence_id": dependence_id,
        "effect_family": effect_family,
    }


def test_replication_target_reports_one_missing_cluster_per_class():
    df = pd.DataFrame(
        [
            _row("mutualist", "M1"),
            _row("antagonist", "A1"),
            _row("mixed_pollinating_seed_predator", "X1"),
            _row("mixed_pollinating_seed_predator", "X1"),
        ]
    )
    out = replication_target_status(df)
    assert out["current_independent_clusters_by_class"] == {
        "antagonist": 1,
        "mixed_pollinating_seed_predator": 1,
        "mutualist": 1,
    }
    assert out["clusters_needed_by_class"] == {
        "antagonist": 1,
        "mixed_pollinating_seed_predator": 1,
        "mutualist": 1,
    }
    assert out["priority_classes"] == [
        "mixed_pollinating_seed_predator",
        "antagonist",
        "mutualist",
    ]
    assert out["status"] == "incomplete"


def test_extra_rows_in_same_programme_do_not_advance_replication():
    df = pd.DataFrame(
        [
            _row("mixed_pollinating_seed_predator", "X1"),
            _row("mixed_pollinating_seed_predator", "X1"),
            _row("mixed_pollinating_seed_predator", "X1"),
        ]
    )
    out = replication_target_status(df)
    assert out["current_independent_clusters_by_class"]["mixed_pollinating_seed_predator"] == 1
    assert out["clusters_needed_by_class"]["mixed_pollinating_seed_predator"] == 1


def test_other_effect_families_do_not_satisfy_smd_target():
    df = pd.DataFrame(
        [
            _row("mutualist", "M1", "log_odds_ratio"),
            _row("mutualist", "M2", "log_odds_ratio"),
        ]
    )
    out = replication_target_status(df)
    assert out["current_independent_clusters_by_class"]["mutualist"] == 0
    assert out["clusters_needed_by_class"]["mutualist"] == 2


def test_replication_target_completes_at_two_independent_clusters_per_class():
    df = pd.DataFrame(
        [
            _row("mutualist", "M1"),
            _row("mutualist", "M2"),
            _row("antagonist", "A1"),
            _row("antagonist", "A2"),
            _row("mixed_pollinating_seed_predator", "X1"),
            _row("mixed_pollinating_seed_predator", "X2"),
        ]
    )
    out = replication_target_status(df)
    assert out["priority_classes"] == []
    assert out["status"] == "complete"


def test_invalid_replication_minimum_fails():
    with pytest.raises(ValueError):
        replication_target_status(pd.DataFrame(), minimum_clusters=0)
