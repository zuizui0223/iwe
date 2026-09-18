import math

import pandas as pd
import pytest

from iwe.iwe078 import (
    build_iwe078_plant_table,
    estimate_iwe078_experiment_effect,
)


def flowering_table() -> pd.DataFrame:
    values = {
        "P1": [4, 0, 0],
        "P2": [3, 1, 0],
        "P3": [0, 1, 3],
        "P4": [0, 0, 4],
    }
    rows = []
    for plant_id, counts in values.items():
        for date, count in enumerate(counts, start=1):
            rows.append(
                {
                    "experiment": "1",
                    "plant_id": plant_id,
                    "treatment": "control",
                    "date": date,
                    "potential_flowers": count,
                }
            )
    return pd.DataFrame(rows)


def attack_table() -> pd.DataFrame:
    values = {
        # Deliberately huge focal P1 attack on date 1. P1's own attack must not
        # create P1's reference activity curve.
        "P1": [100, 0, 0],
        "P2": [2, 0, 0],
        "P3": [0, 0, 1],
        "P4": [0, 0, 1],
    }
    rows = []
    for plant_id, counts in values.items():
        for date, count in enumerate(counts, start=1):
            rows.append(
                {
                    "experiment": "1",
                    "plant_id": plant_id,
                    "treatment": "control",
                    "date": date,
                    "mompha_acquired": count,
                }
            )
    return pd.DataFrame(rows)


def fitness_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "experiment": ["1"] * 4,
            "plant_id": ["P1", "P2", "P3", "P4"],
            "treatment": ["control"] * 4,
            "final_reproduction": [1, 4, 2, 3],
        }
    )


def test_iwe078_overlap_is_normalized_and_leave_one_out():
    table = build_iwe078_plant_table(
        flowering_table(),
        attack_table(),
        fitness_table(),
        experiment="1",
    )
    p1 = table.loc[table["plant_id"] == "P1"].iloc[0]

    # Excluding P1, reference Mompha activity is [2, 0, 2], normalized to
    # [0.5, 0, 0.5]. P1 flowering is [1, 0, 0] after normalization.
    assert p1["overlap"] == pytest.approx(0.5)
    assert p1["log_total_fitness"] == pytest.approx(math.log1p(1))


def test_iwe078_overlap_is_invariant_to_abundance_scale():
    base = build_iwe078_plant_table(
        flowering_table(),
        attack_table(),
        fitness_table(),
        experiment="1",
    ).set_index("plant_id")

    fl = flowering_table()
    fl["potential_flowers"] = fl["potential_flowers"] * 17
    at = attack_table()
    at["mompha_acquired"] = at["mompha_acquired"] * 23

    scaled = build_iwe078_plant_table(
        fl,
        at,
        fitness_table(),
        experiment="1",
    ).set_index("plant_id")

    for plant_id in base.index:
        assert scaled.loc[plant_id, "overlap"] == pytest.approx(
            base.loc[plant_id, "overlap"]
        )


def test_iwe078_effect_uses_source_log_fitness_and_fisher_variance():
    table = build_iwe078_plant_table(
        flowering_table(),
        attack_table(),
        fitness_table(),
        experiment="1",
    )
    effect = estimate_iwe078_experiment_effect(table, experiment="1")

    expected_r = float(table["overlap"].corr(table["log_total_fitness"]))
    assert effect.n == 4
    assert effect.pearson_r == pytest.approx(expected_r)
    assert effect.fisher_z_native == pytest.approx(math.atanh(expected_r))
    assert effect.variance_native == pytest.approx(1.0)


def test_iwe078_negative_attack_counts_fail_closed():
    attacks = attack_table()
    attacks.loc[0, "mompha_acquired"] = -1

    with pytest.raises(ValueError, match="mompha_acquired must be nonnegative"):
        build_iwe078_plant_table(
            flowering_table(),
            attacks,
            fitness_table(),
            experiment="1",
        )


def test_iwe078_focal_without_external_activity_is_excluded():
    attacks = attack_table()
    # Leave P1 as the only attacked plant. Its reference curve then has zero
    # total activity and must not yield an artificial synchrony value.
    attacks.loc[attacks["plant_id"] != "P1", "mompha_acquired"] = 0

    table = build_iwe078_plant_table(
        flowering_table(),
        attacks,
        fitness_table(),
        experiment="1",
    )
    assert "P1" not in set(table["plant_id"])
