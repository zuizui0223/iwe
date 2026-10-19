"""Software tests only, NOT real Höfer biological effect estimates."""
import math
import pytest
from scripts.analyze_hofer2022_conversion_components import (
    STAGE_NAMES, COMPARISON_MODELS, stage_plants, stage_validate,
)


def fixture():
    source = {
        "Floral_traits.csv": [], "Plantlist.csv": [], "Int_data.csv": []
    }
    for i in range(53):
        pid = "P" + str(i)
        mother = "M" + str(i % 20)
        shelter = str(1 + i % 5)
        water = ("Control", "PrecipRed", "Drought")[i % 3]
        plot = "PLOT" + str(i % 15)
        flowers = 80 + (i % 13) * 8
        pods = 12 + i % 8
        avgseed = 10 + i % 4
        visit = .03 + (i % 7)/20
        a = {
            "plantID": pid, "motherID": mother, "treatment": water,
            "shelterID": shelter, "plotID": plot,
            "sumflower": str(flowers),
            "floweringtime": str(14 + i % 12),
            "seedsperplant": str(pods * avgseed),
            "SWP": str(-.08 - i % 7 / 100),
            "pollenstigma": str(150 + i % 7 * 20),
            "pods": str(pods), "avgseed": str(avgseed),
        }
        source["Floral_traits.csv"].append(a)
        source["Plantlist.csv"].append({
            "plantID": pid, "motherID": mother, "treatment": water,
            "shelter": shelter, "plotID": plot
        })
        for group in range(8 + (1 if i < 3 else 0)):
            source["Int_data.csv"].append({
                "plantID": pid,
                "motherID": mother, "treatment": water,
                "shelter": shelter, "plotID": plot,
                "visitorgroup": "G" + str(group),
                "NrInt_day_flower": str(visit/8),
                "NrInt_day": str(visit*flowers/8),
            })
    assert len(source["Int_data.csv"]) == 427
    return source


def test_original_grain_and_stage_metadata_are_not_independent_effects():
    plants, meta = stage_plants(fixture())
    assert len(plants) == 53
    assert meta["stage_n"] == 53
    assert meta["n_shelters"] == 5
    assert meta["n_plots"] == 15
    assert meta["initial_source_excluded"] == {}
    assert sum(meta["shelter_counts"].values()) == 53
    assert set(STAGE_NAMES) == set(plants[0]["stages"])
    x = next(z for z in plants if z["plant"] == "P0")
    assert x["sourcePods"] == 12
    assert x["sourceAvgSeedsPerPod"] == 10
    assert x["podsPerFlower"] == pytest.approx(12/80)
    assert x["sourceSeedsPerFlower"] == pytest.approx(120/80)
    assert x["expectedFromPodRatio"] == pytest.approx(1)
    assert x["sourcePods"] != 53


def test_unknown_fruit_and_pod_stages_are_excluded_not_filled_with_zero():
    source = fixture()
    source["Floral_traits.csv"][0]["avgseed"] = "NA"
    plants, info = stage_plants(source)
    assert len(plants) == 52
    assert info["stage_excluded"]["missing_pod_or_seed_per_pod"] == 1
    assert "P0" not in {r["plant"] for r in plants}
    source = fixture()
    source["Floral_traits.csv"][0]["pods"] = "0"
    source["Floral_traits.csv"][0]["avgseed"] = "0"
    plants, info = stage_plants(source)
    assert len(plants) == 52
    assert info["stage_excluded"][
        "zero_source_pod_cannot_define_seeds_per_pod"
    ] == 1


def test_model_comparison_preserves_each_shelter_and_same_individual_subset():
    records, _ = stage_plants(fixture())
    outputs = stage_validate(records)
    assert set(outputs) == set(STAGE_NAMES)
    for stage, a in outputs.items():
        assert a["n_plants"] == 53
        assert a["n_shelters"] == 5
        assert set(a["model_rmse"]) == set(COMPARISON_MODELS)
        assert set(a["per_shelter_errors"]["flowers"]) == {
            "1", "2", "3", "4", "5"
        }
        assert all(math.isfinite(x) and x >= 0
                   for x in a["model_rmse"].values())
        assert 0 <= a["paired_comparisons"][
            "add_visits_per_day"
        ]["shelter_wins_over_flower_only"] <= 5
        assert 0 <= a["paired_comparisons"][
            "visitor_day_after_measured_SWP"
        ]["shelter_wins"] <= 5


def test_bad_original_pod_reference_or_missing_shelter_fails_closed():
    source = fixture()
    source["Floral_traits.csv"][0]["pods"] = "-100"
    with pytest.raises(ValueError, match="invalid negative"):
        stage_plants(source)
    source = fixture()
    for row in source["Floral_traits.csv"]:
        if row["shelterID"] == "1":
            row["avgseed"] = "NA"
    with pytest.raises(ValueError, match="fewer than five"):
        stage_plants(source)


def test_stage_count_must_not_create_fake_big_sample_from_taxa():
    source = fixture()
    records, info = stage_plants(source)
    assert info["stage_n"] == 53
    assert len(source["Int_data.csv"]) == 427
    assert len(set(x["plant"] for x in records)) == 53
    assert len(set(x["mother"] for x in records)) == 20
    assert len(set(x["shelter"] for x in records)) == 5
