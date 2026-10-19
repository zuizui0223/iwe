"""Source-grain and five-shelter software fixtures, not biological effect estimates."""
import math
import pytest

from scripts.analyze_hofer2022_resource_limits import (
    _finite, link_plants, validate, MODELS,
)


def fixture():
    source = {
        "Floral_traits.csv": [],
        "Plantlist.csv": [],
        "Int_data.csv": [],
    }
    for i in range(53):
        plant = f"P{i}"
        mother = f"M{i % 20}"
        shelter = str(1 + (i % 5))
        water = ("Control", "PrecipRed", "Drought")[i % 3]
        plot = f"BLOCK{i % 15}"
        flowers = 80 + (i % 13) * 8
        visit = 0.03 + (i % 7) / 20
        source["Floral_traits.csv"].append({
            "plantID": plant, "motherID": mother, "treatment": water,
            "shelterID": shelter, "plotID": plot,
            "sumflower": str(flowers),
            "floweringtime": str(14 + i % 12),
            "seedsperplant": str(flowers * (i % 5 + 10)),
            "SWP": str(-0.08 - i % 7 / 100),
        })
        source["Plantlist.csv"].append({
            "plantID": plant, "motherID": mother, "treatment": water,
            "shelter": shelter, "plotID": plot,
        })
        for g in range(8 + (1 if i < 3 else 0)):
            source["Int_data.csv"].append({
                "plantID": plant,
                "motherID": mother, "treatment": water,
                "shelter": shelter, "plotID": plot,
                "visitorgroup": f"G{g}",
                "NrInt_day_flower": str(visit / 8),
            })
    return source


def test_53_original_plant_id_join_and_source_grain_not_427_experiments():
    source = fixture()
    assert len(source["Int_data.csv"]) == 427
    plants, excluded, repeated = link_plants(source)
    assert len(plants) == 53
    assert not excluded
    assert repeated == 0
    assert len(set(x["mother"] for x in plants)) == 20
    assert len(set(x["shelter"] for x in plants)) == 5
    assert sum(x["visitGroupRows"] for x in plants) == 427
    assert plants[0]["waterPotential"] < 0
    assert all(x["estimatedTotalSeeds"] > 0 for x in plants)


def test_shelter_heldout_models_and_no_separate_visitor_group_replication():
    plants, _, _ = link_plants(fixture())
    r = validate(plants)
    assert set(r) == set(MODELS)
    for m in r.values():
        assert m["n_plants"] == 53
        assert m["n_shelters"] == 5
        assert len(m["by_shelter_mse"]) == 5
        assert math.isfinite(m["mean_shelter_rmse"])
        assert m["mean_shelter_rmse"] >= 0


def test_metadata_mismatch_is_not_silently_merged():
    s = fixture()
    s["Int_data.csv"][0]["motherID"] = "unrelated"
    with pytest.raises(ValueError, match="visitor plant metadata mismatch"):
        link_plants(s)
    s = fixture()
    s["Floral_traits.csv"][0]["treatment"] = "wrong"
    with pytest.raises(ValueError, match="trait source disagree"):
        link_plants(s)


def test_unknown_seeds_reduce_eligible_plants_without_zero_fill():
    s = fixture()
    s["Floral_traits.csv"][0]["seedsperplant"] = "NA"
    plants, excluded, _ = link_plants(s)
    assert len(plants) == 52
    assert excluded["required_plant_or_visit_data_missing"] == 1
    assert all(z["plant"] != "P0" for z in plants)


def test_signed_water_potential_not_seed_count():
    assert _finite({"SWP": "-0.147"}, "SWP", allow_negative=True) == -0.147
    with pytest.raises(ValueError, match="invalid negative"):
        _finite({"seedsperplant": "-4"}, "seedsperplant")
    assert _finite({"seedsperplant": "NA"}, "seedsperplant") is None
    assert _finite({"seedsperplant": "0"}, "seedsperplant") == 0


def test_single_plant_group_labels_should_not_create_source_independence():
    s = fixture()
    s["Int_data.csv"][0]["visitorgroup"] = s["Int_data.csv"][1]["visitorgroup"]
    plants, _, repeated = link_plants(s)
    assert repeated == 1
    assert len(plants) == 53
