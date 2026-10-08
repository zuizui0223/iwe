"""Non-promoting source-table audit for Zhou et al. (2020) Table 1.

Published group means are descriptive. The printed dispersions are labelled SE
but cannot be interpreted as plant-level SE at the reported n; only raw Dryad
verification can support quantitative strict-H1 readmission.
"""

from pathlib import Path
from math import sqrt

import pandas as pd


TABLE_PATH = Path("data/source_reconstructions/iwe015_published_table1.csv")


def _table() -> pd.DataFrame:
    return pd.read_csv(TABLE_PATH)


def test_published_groups_are_exactly_the_four_source_experiments():
    t = _table().sort_values(["year", "period"]).reset_index(drop=True)
    assert len(t) == 4
    assert t[["year", "period"]].apply(tuple, axis=1).tolist() == [
        (2012, "early"),
        (2012, "late"),
        (2013, "early"),
        (2013, "late"),
    ]
    assert t["adult_plants"].tolist() == [59, 58, 55, 55]
    assert set(t["printed_dispersion_label"]) == {"SE"}
    for name in ("fruit_initiation_mean", "predation_rate_mean"):
        assert t[name].between(0, 1).all()
    assert t["successful_fruits_mean"].ge(0).all()


def test_table_means_switch_the_yearwise_early_minus_late_direction():
    t = _table().set_index(["year", "period"])
    d_fruit_2012 = (
        t.loc[(2012, "early"), "successful_fruits_mean"]
        - t.loc[(2012, "late"), "successful_fruits_mean"]
    )
    d_fruit_2013 = (
        t.loc[(2013, "early"), "successful_fruits_mean"]
        - t.loc[(2013, "late"), "successful_fruits_mean"]
    )
    d_pred_2012 = (
        t.loc[(2012, "early"), "predation_rate_mean"]
        - t.loc[(2012, "late"), "predation_rate_mean"]
    )
    d_pred_2013 = (
        t.loc[(2013, "early"), "predation_rate_mean"]
        - t.loc[(2013, "late"), "predation_rate_mean"]
    )
    assert round(d_fruit_2012, 2) == -1.25
    assert round(d_fruit_2013, 2) == +1.17
    assert round(d_pred_2012, 2) == +0.18
    assert round(d_pred_2013, 2) == +0.01
    # A crossover of published group means, not a significance test.
    assert d_fruit_2012 < 0 < d_fruit_2013


def test_printed_proportion_dispersions_cannot_be_plant_level_se_at_reported_n():
    # For n observations x_i in [0, 1] with mean mu:
    # sample SE <= sqrt(mu * (1 - mu) / (n - 1)).
    # This exact finite-n upper bound does not assume Bernoulli observations.
    t = _table()
    for _, row in t.iterrows():
        n = int(row["adult_plants"])
        assert n > 1
        for metric in ("fruit_initiation", "predation_rate"):
            mean = float(row[metric + "_mean"])
            printed = float(row[metric + "_printed_dispersion"])
            se_upper = sqrt(mean * (1 - mean) / (n - 1))
            assert printed > se_upper + 0.005, (
                row["year"], row["period"], metric, printed, se_upper
            )
    # No guessing SD, pooling years, or adding effects to strict H1 here.
