import math

import numpy as np
import pandas as pd

from iwe.reconstruction import histogram_intersection, source_seed_outcome, leave_one_out_overlaps


def test_histogram_intersection_uses_normalized_curves():
    assert histogram_intersection([1, 1], [2, 0]) == 0.5
    assert histogram_intersection([0, 3, 0], [0, 5, 0]) == 1.0


def test_source_seed_outcome_matches_frozen_r_definition():
    row = {
        "seeds": 20.0,
        "fruits": 4.0,
        "fruits_split": 1.0,
        "aborts": 2.0,
        "fruits_fly_no_seeds": 1.0,
        "fruits_fly_with_seeds": 1.0,
        "seeds_fly": 3.0,
        "fruits_caterpillar": 0.0,
        "fruits_early_uncountable": 1.0,
        "flowers_buds": 2.0,
        "flowers_buds_collected_early": 1.0,
        "flowers_buds_collected_last": 1.0,
    }
    result = source_seed_outcome(row)
    seeds_per_fruit = 20.0 / 4.0
    fruits_aborted = 2.0 + 1.0
    expected_seed_rate = 20.0 / (4.0 + fruits_aborted + 1.0 + 1.0 + 0.0)
    seeds_est = 20.0 + 3.0 + (1.0 + 1.0) * expected_seed_rate + 1.0 * seeds_per_fruit
    fruits_with_seeds = 4.0 + 1.0 + 1.0
    fruits_nonaborted = fruits_with_seeds + 1.0 + 0.0 + 1.0
    flowers_est = fruits_nonaborted + 2.0 + 2.0
    assert math.isclose(result["seeds_est"], seeds_est)
    assert math.isclose(result["flowers_est"], flowers_est)
    assert math.isclose(result["seeds_per_flower"], seeds_est / flowers_est)


def test_source_seed_outcome_preserves_r_na_when_no_counted_fruits():
    """R source uses 0 * NA = NA, so fruitless plants cannot become zero-fitness rows."""
    row = {
        "seeds": 0.0,
        "fruits": 0.0,
        "fruits_split": 0.0,
        "aborts": 1.0,
        "fruits_fly_no_seeds": 0.0,
        "fruits_fly_with_seeds": 0.0,
        "seeds_fly": 0.0,
        "fruits_caterpillar": 0.0,
        "fruits_early_uncountable": 0.0,
        "flowers_buds": 0.0,
        "flowers_buds_collected_early": 0.0,
        "flowers_buds_collected_last": 0.0,
    }
    result = source_seed_outcome(row)
    assert math.isnan(result["seeds_per_fruit"])
    assert math.isnan(result["seeds_est"])
    assert math.isnan(result["seeds_per_flower"])


def test_leave_one_out_overlap_avoids_own_egg_mechanical_correlation():
    rows = []
    # Plant A flowers only early and receives many eggs early.
    # Plant B flowers only late and receives many eggs late.
    # Plant C provides an early activity reference.
    for plant, floral, eggs in [
        ("A", [10, 0], [10, 0]),
        ("B", [0, 10], [0, 10]),
        ("C", [10, 0], [10, 0]),
    ]:
        for t, (f, e) in enumerate(zip(floral, eggs)):
            rows.append({"plantid": plant, "census": t, "floral": f, "eggs": e})
    df = pd.DataFrame(rows)
    out = leave_one_out_overlaps(df, plant_col="plantid", time_col="census", floral_col="floral", egg_col="eggs")
    overlap = dict(zip(out["plantid"], out["overlap"]))
    # A sees B+C activity split early/late, so overlap is 0.5 rather than 1.0 from its own eggs.
    assert math.isclose(overlap["A"], 0.5)
    # B sees only early activity in A+C, so its late flowering has zero overlap.
    assert math.isclose(overlap["B"], 0.0)
    # C sees A+B activity split, so overlap is 0.5.
    assert math.isclose(overlap["C"], 0.5)
