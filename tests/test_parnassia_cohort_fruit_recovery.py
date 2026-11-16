"""Source-preserving descriptive recovery counts (never flower-level H1 inference).

Wen et al. 2024, 10.1002/ece3.70380, Methods 2.5, Site A.
"""
from pathlib import Path

import pandas as pd


PATH = Path("data/source_reconstructions/parnassia_siteA_cohort_fruit_recovery_2024.csv")


def test_plant_reproduction_cohorts_are_complete_as_source_described():
    df = pd.read_csv(PATH)
    assert df["flowering_period"].tolist() == ["early", "middle", "late"]
    assert df["site"].tolist() == ["A"] * 3
    assert df["marked_bagged_flowers"].tolist() == [60, 60, 60]
    assert df["recovered_fruits_september"].tolist() == [31, 41, 25]
    assert df["unrecovered_marked_flowers"].tolist() == [29, 19, 35]
    assert (
        df["marked_bagged_flowers"] == (
            df["recovered_fruits_september"] + df["unrecovered_marked_flowers"]
        )
    ).all()


def test_recovery_is_nonmonotone_and_its_grain_is_not_pseudoreplicated():
    df = pd.read_csv(PATH).set_index("flowering_period")
    rates = (
        df["recovered_fruits_september"] / df["marked_bagged_flowers"]
    )
    assert abs(rates["early"] - 31 / 60) < 1e-12
    assert abs(rates["middle"] - 41 / 60) < 1e-12
    assert abs(rates["late"] - 25 / 60) < 1e-12
    assert (rates["middle"] > rates["early"] > rates["late"])
    assert (abs(df["fruit_recovery_fraction"] - rates) < 1e-6).all()
    assert df["grain_status"].eq("flower_n_nested_in_single_site_period").all()
    assert df["outcome_definition"].eq(
        "September_fruit_recovery_per_initially_marked_flower"
    ).all()


def test_no_beetle_fate_or_seed_count_was_fabricated():
    df = pd.read_csv(PATH)
    assert not set(df.columns) & {
        "beetle_caused_loss_count",
        "seeds_per_missing_flower",
        "seed_set_per_initial_flower",
        "adult_beetle_flight_curve",
        "hedges_g",
        "effect_variance",
    }
    assert "none_observed" == df.loc[0, "beetle_florivory_presence"]
    assert "<" not in str(df.loc[1, "fruit_recovery_fraction"])
