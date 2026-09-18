import pandas as pd

from iwe.feasibility import common_scale_gate


CLASSES = ["mutualist", "antagonist", "mixed_pollinating_seed_predator"]


def make_df(n_per_class: int) -> pd.DataFrame:
    rows = []
    for interaction_type in CLASSES:
        for i in range(n_per_class):
            rows.append(
                {
                    "interaction_type": interaction_type,
                    "dependence_id": f"{interaction_type}_{i}",
                }
            )
    return pd.DataFrame(rows)


def test_one_programme_per_class_is_coverage_only():
    gate = common_scale_gate(make_df(1))
    assert gate.coverage_complete is True
    assert gate.cross_class_fit_allowed is False
    assert gate.primary_claim_gate is False
    assert gate.status == "coverage_only"


def test_two_programmes_per_class_allows_only_exploratory_fit():
    gate = common_scale_gate(make_df(2))
    assert gate.cross_class_fit_allowed is True
    assert gate.primary_claim_gate is False
    assert gate.status == "exploratory_model_only"


def test_five_programmes_per_class_opens_primary_gate():
    gate = common_scale_gate(make_df(5))
    assert gate.primary_claim_gate is True
    assert gate.status == "primary_model_allowed"


def test_duplicate_rows_do_not_inflate_programme_counts():
    df = make_df(1)
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    gate = common_scale_gate(df)
    assert gate.programme_counts["mutualist"] == 1