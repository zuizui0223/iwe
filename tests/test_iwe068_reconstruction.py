import math

import numpy as np
import pandas as pd

from iwe.reconstruction import (
    histogram_intersection,
    leave_one_out_overlaps,
    prepare_maxfield_phenology,
    prepare_maxfield_seeds,
    source_seed_outcome,
)


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


def test_prepare_maxfield_phenology_rebuilds_ids_recodes_dates_and_completes_zeros():
    phen = pd.DataFrame(
        {
            "date": ["2021-06-30", "2021-07-02"],
            "plot": [1, 2],
            "subplot": ["B", "A"],
            "plant": [10, 20],
            "open_1": [2, 3],
            "buds_1": [1, 2],
            "eggs_1": [1, np.nan],
            "open_2": [np.nan, 4],
            "buds_2": [np.nan, 1],
            "eggs_2": [np.nan, 2],
        }
    )
    metadata = pd.DataFrame(
        {
            "plantid": ["1B10", "2A20"],
            "snow": ["normal", "early"],
            "temp": ["control", "OTC"],
        }
    )
    out = prepare_maxfield_phenology(phen, metadata)

    assert set(out["plantid"]) == {"1B10", "2A20"}
    assert out["census"].nunique() == 1
    by_plant = out.set_index("plantid")
    assert by_plant.loc["1B10", "floral"] == 3
    assert by_plant.loc["1B10", "eggs"] == 1
    assert by_plant.loc["2A20", "floral"] == 10
    assert by_plant.loc["2A20", "eggs"] == 2
    assert by_plant.loc["1B10", "temp"] == "control"
    assert by_plant.loc["2A20", "snow"] == "early"


def test_prepare_maxfield_seeds_splits_early_and_last_collection_and_rebuilds_outcome():
    seeds = pd.DataFrame(
        {
            "plot": [1, 1],
            "subplot": ["B", "B"],
            "plant": [10, 10],
            "date": ["2021-08-16", "2021-08-23"],
            "seeds": [20, 0],
            "fruits": [4, 0],
            "fruits_split": [1, 0],
            "aborts": [2, 1],
            "fruits_fly_no_seeds": [1, 0],
            "fruits_fly_with_seeds": [1, 0],
            "seeds_fly": [3, 0],
            "fruits_caterpillar": [0, 0],
            "fruits_early_uncountable": [1, 0],
            "flowers_buds": [2, 3],
        }
    )
    metadata = pd.DataFrame({"plantid": ["1B10"], "snow": ["normal"], "temp": ["control"]})
    out = prepare_maxfield_seeds(seeds, metadata).set_index("plantid")
    row = out.loc["1B10"]
    assert row["flowers_buds_collected_early"] == 2
    assert row["flowers_buds_collected_last"] == 3
    assert row["flowers_buds"] == 5
    assert np.isfinite(row["seeds_per_flower"])


def test_leave_one_out_overlap_avoids_own_egg_mechanical_correlation():
    rows = []
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
    assert math.isclose(overlap["A"], 0.5)
    assert math.isnan(overlap["B"])
    assert math.isclose(overlap["C"], 0.5)
