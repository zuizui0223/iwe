"""No fake observations can count as evidence; deterministic software fixtures only."""
from copy import deepcopy

import pytest

from scripts.analyze_maple_crossscale_2012_2024 import (
    FLOWER_FILE, MODEL_FEATURES, FORWARD_ADDITIONS,
    build_panel, evaluate, original_csv, annual_summary,
)


def synthetic_source():
    """Fixture uses 20 trees/year and original-shaped data, never source values."""
    flowers, autumn = [], []
    for year in range(2011, 2025):
        for i in range(1, 21):
            tree = f"HF{i}"
            category = (
                "none" if year in (2018, 2022, 2024)
                else ("high" if i <= (year % 6) + 1
                      else ("none", "low", "medium", "high")[(i + year) % 4])
            )
            if year >= 2012:
                flowers.append({
                    "year": str(year),
                    "tree.num": tree,
                    "first.sex": "NA",
                    "flowering.intensity": category,
                })
            # Exchange one original harvest-only 2022 tree label: unmatched.
            if year == 2022 and i == 20:
                tree = "HF28"
            score = {"none": 0, "low": 1, "medium": 2, "high": 3}[category]
            seed = (0 if category == "none" else i % 4 + 2 * score)
            if year == 2011:
                seed = i % 7 + 1
            autumn.append({
                "tree": tree,
                "date": f"9/10/{year}",
                "EC.count": str(seed // 2),
                "JR.count": str(seed - seed // 2),
                "total.count": str(seed),
                "": "",
            })
    return flowers, autumn


def test_20_tree_13year_source_join_does_not_fill_one_missing_tree():
    f, s = synthetic_source()
    panel, prov = build_panel(f, s)
    assert len(panel) == 259
    assert prov["original_flowering_tree_years"] == 260
    assert prov["original_autumn_tree_years"] == 260
    assert prov["unmatched_original_autumn"] == [{
        "year": 2022, "tree": "HF28", "autumn_sample_count": 0
    }]
    assert len(annual_summary(panel)) == 13
    p = next(x for x in panel if x["year"] == 2019 and x["tree"] == "HF1")
    assert p["other"] == pytest.approx(
        (sum(r["focal"] for r in panel if r["year"] == 2019) -
         p["focal"]) / 19
    )
    assert p["lag"] >= 0
    assert p["parity"] == 1


def test_nested_year_evaluation_and_future_prediction_are_separated():
    p, _ = build_panel(*synthetic_source())
    result = evaluate(p)
    all_years = result["all_tree_years"]
    assert all_years["row_count"] == 259
    assert all_years["n_year_blocks"] == 13
    assert all_years["year_loo"]["constant"]["heldout_year_count"] == 13
    assert "previous_autumn_seed_mean" not in all_years["year_loo"]
    assert "focal_plus_previous_seed_mean" not in MODEL_FEATURES
    assert "focal_plus_previous_seed_mean" in FORWARD_ADDITIONS
    future = all_years[
        "fixed_train_2012_to_2017_future_test_2018_to_2024"
    ]
    assert future["train_rows"] == 120
    assert future["test_rows"] == 139
    assert future["training_years"] == list(range(2012, 2018))
    assert future["testing_years"] == list(range(2018, 2025))
    active = result["actually_flowering_trees"]
    assert 2022 not in active["year_blocks"]
    assert 2024 not in active["year_blocks"]
    assert active["row_count"] < 200


def test_source_grain_data_quality_fail_closed():
    f, s = synthetic_source()
    f2 = deepcopy(f)
    f2.append(dict(f2[0]))
    with pytest.raises(ValueError, match="duplicate spring tree-year"):
        build_panel(f2, s)
    f2 = deepcopy(f)
    f2[0]["flowering.intensity"] = "unknown"
    with pytest.raises(ValueError, match="unknown source flowering"):
        build_panel(f2, s)
    s2 = deepcopy(s)
    s2[0]["total.count"] = "999"
    with pytest.raises(ValueError, match="does not close"):
        build_panel(f, s2)
    s2 = deepcopy(s)
    s2[0]["date"] = "2011-09-10"
    with pytest.raises(ValueError):
        build_panel(f, s2)
    f2 = deepcopy(f)
    f2.pop()
    with pytest.raises(ValueError, match="incorrect original flowering"):
        build_panel(f2, s)


def test_off_source_and_modified_file_digests_fail_closed(monkeypatch):
    import scripts.analyze_maple_crossscale_2012_2024 as module
    monkeypatch.setattr(module, "_get", lambda url: b"modified bytes")
    with pytest.raises(ValueError, match="MD5 mismatch"):
        original_csv(FLOWER_FILE)
    with pytest.raises(ValueError, match="not frozen"):
        original_csv("other-file.csv")


def test_exposure_and_endpoint_are_not_declared_fitness_or_larval_stages():
    f, s = synthetic_source()
    panel, info = build_panel(f, s)
    assert set(panel[0]) == {
        "year", "tree", "focal", "other", "population", "parity",
        "lag", "sample_count", "y_log1p", "spring_active_tree_n",
    }
    assert info["n_source_year_blocks"] == 13
    # Same-year seed counts do not define a pre-spring predictor.
    assert all(r["lag"] >= 0 for r in panel)
