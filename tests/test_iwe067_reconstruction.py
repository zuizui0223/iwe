import math

import pandas as pd
import pytest

from iwe.iwe067 import build_iwe067_plant_table, estimate_iwe067_year_effect


def synthetic_phenology() -> pd.DataFrame:
    rows = []
    values = {
        "P1": ([4, 0, 0], [2, 0, 0]),
        "P2": ([3, 1, 0], [2, 0, 0]),
        "P3": ([0, 1, 3], [0, 0, 1]),
        "P4": ([0, 0, 4], [0, 0, 1]),
    }
    for plant_id, (flowers, eggs) in values.items():
        for census, (open_flowers, detected_eggs) in enumerate(
            zip(flowers, eggs, strict=True), start=1
        ):
            rows.append(
                {
                    "year": 2017,
                    "plant_id": plant_id,
                    "treatment": "control",
                    "census": census,
                    "open_flowers": open_flowers,
                    "detected_eggs": detected_eggs,
                }
            )
    return pd.DataFrame(rows)


def synthetic_fruit() -> pd.DataFrame:
    successes = {"P1": 1, "P2": 2, "P3": 3, "P4": 2}
    rows = []
    for plant_id, n_success in successes.items():
        fates = (
            ["expanded_unparasitized"] * n_success
            + ["aborted"] * (4 - n_success)
        )
        for fate in fates:
            rows.append(
                {
                    "year": 2017,
                    "plant_id": plant_id,
                    "treatment": "control",
                    "fruit_fate": fate,
                }
            )
    return pd.DataFrame(rows)


def test_iwe067_leave_one_out_overlap_and_final_fitness():
    table = build_iwe067_plant_table(
        synthetic_phenology(),
        synthetic_fruit(),
        year=2017,
    )

    assert list(table["plant_id"]) == ["P1", "P2", "P3", "P4"]
    assert table["overlap"].between(0, 1).all()

    p1 = table.loc[table["plant_id"] == "P1"].iloc[0]
    # P1 flowers entirely at census 1. Excluding P1, the Hylemya activity
    # vector is (2/3, 0/2, 2/7), which normalizes to (0.7, 0, 0.3).
    assert p1["overlap"] == pytest.approx(0.7)
    assert p1["fitness"] == pytest.approx(0.25)
    assert int(p1["scored_marked_flowers"]) == 4


def test_iwe067_year_effect_uses_fisher_z_variance():
    table = build_iwe067_plant_table(
        synthetic_phenology(),
        synthetic_fruit(),
        year=2017,
    )
    effect = estimate_iwe067_year_effect(table, year=2017)

    expected_r = float(table["overlap"].corr(table["fitness"]))
    assert effect.n == 4
    assert effect.pearson_r == pytest.approx(expected_r)
    assert effect.fisher_z_native == pytest.approx(math.atanh(expected_r))
    assert effect.variance_native == pytest.approx(1.0)


def test_iwe067_rejects_unknown_fruit_fate():
    fruit = synthetic_fruit()
    fruit.loc[0, "fruit_fate"] = "simulated_no_hylemya"

    with pytest.raises(ValueError, match="unknown fruit_fate"):
        build_iwe067_plant_table(
            synthetic_phenology(),
            fruit,
            year=2017,
        )


def test_iwe067_missing_counts_are_not_silently_zero_imputed():
    phenology = synthetic_phenology()
    phenology.loc[
        (phenology["plant_id"] == "P1") & (phenology["census"] == 1),
        "open_flowers",
    ] = float("nan")

    table = build_iwe067_plant_table(
        phenology,
        synthetic_fruit(),
        year=2017,
    )
    p1 = table.loc[table["plant_id"] == "P1"].iloc[0]

    # The missing focal census is excluded rather than converted to zero.
    assert int(p1["n_shared_censuses"]) == 2
