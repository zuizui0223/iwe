import pandas as pd
import pytest
from iwe.host_geography import analyze_focal_host_geography


def source():
    return dict(
        pairs=pd.DataFrame([
            {"insect_species": "Anthocharis cardamines",
             "accepted_plant_name_id": "F", "accepted_name": "Cardamine pratensis"},
            {"insect_species": "Anthocharis cardamines",
             "accepted_plant_name_id": "O", "accepted_name": "Alliaria petiolata"},
        ]),
        native_units=pd.DataFrame([
            {"accepted_plant_name_id": "F", "area_code_l3": "A"},
            {"accepted_plant_name_id": "O", "area_code_l3": "B"},
        ]),
        contemporary_units=pd.DataFrame([
            {"accepted_plant_name_id": i, "area_code_l3": u}
            for i, units in (("F", ("A", "C", "D")), ("O", ("B", "D", "E")))
            for u in units
        ]),
        species_metrics=pd.DataFrame([{
            "species": "Anthocharis cardamines",
            "native_resource_units": 2, "contemporary_resource_units": 5,
            "introduced_added_units": 3, "resolved_host_species": 2,
        }]),
    )


def test_source_attribution_shared_vs_exclusive():
    result, hosts, regions = analyze_focal_host_geography(**source())
    assert result["source_pair_status"] == "confirmed_exact_in_chocho_HOSTS_sidecar"
    assert result["native_butterfly_units"] == 2
    assert result["contemporary_butterfly_units"] == 5
    assert result["added_butterfly_units"] == 3
    assert result["focal_native_units"] == 1
    assert result["focal_contemporary_units"] == 3
    assert result["focal_introduced_only_units"] == 2
    assert result["added_units_covered_by_focal"] == 2
    assert result["added_units_exclusively_covered_by_focal"] == 1
    assert result["fractional_added_units_focal"] == pytest.approx(1.5)
    assert result["fractional_credit_sum"] == pytest.approx(3)
    assert result["strict_h1_effects_created"] == 0
    assert len(regions) == 3
    region = regions.set_index("wgsrpd3_unit")
    assert bool(region.loc["C", "focal_exclusively_supplies_unit"])
    assert not bool(region.loc["D", "focal_exclusively_supplies_unit"])
    assert region.loc["E", "focal_host_status"] == "not_in_this_host_union"
    assert hosts["fractional_added_unit_credit"].sum() == pytest.approx(3)


def test_missing_pair_does_not_mean_zero_ecological_use():
    rows = source()
    rows["pairs"].loc[0, "accepted_name"] = "Different plant"
    result, _, regions = analyze_focal_host_geography(**rows)
    assert result["source_pair_status"] == "not_found_exact_in_this_HOSTS_sidecar"
    assert result["focal_native_units"] is None
    assert result["added_units_covered_by_focal"] is None
    assert set(regions["focal_host_status"]) == {"not_verified_in_HOSTS_source"}


def test_fixed_metrics_mismatch_is_a_hard_error():
    rows = source()
    rows["species_metrics"].loc[0, "introduced_added_units"] = 4
    with pytest.raises(ValueError, match="drift"):
        analyze_focal_host_geography(**rows)


def test_bad_native_subset_is_a_hard_error():
    rows = source()
    rows["contemporary_units"] = rows["contemporary_units"].loc[
        ~((rows["contemporary_units"]["accepted_plant_name_id"] == "F")
          & (rows["contemporary_units"]["area_code_l3"] == "A"))
    ]
    with pytest.raises(ValueError, match="native not subset"):
        analyze_focal_host_geography(**rows)


def test_source_id_name_conflict_is_a_hard_error():
    rows = source()
    rows["pairs"] = pd.concat([
        rows["pairs"],
        pd.DataFrame([{"insect_species": "Anthocharis cardamines",
                       "accepted_plant_name_id": "F",
                       "accepted_name": "Cardamine amara"}])
    ], ignore_index=True)
    with pytest.raises(ValueError, match="inconsistent accepted name"):
        analyze_focal_host_geography(**rows)


def test_counts_can_preserve_region_codes_with_leading_zero():
    rows = source()
    for key in ("native_units", "contemporary_units"):
        rows[key]["area_code_l3"] = rows[key]["area_code_l3"].replace("D", "001D")
    result, _, region = analyze_focal_host_geography(**rows)
    assert result["added_butterfly_units"] == 3
    assert "001D" in set(region["wgsrpd3_unit"])


def test_source_prefilter_excludes_nonfocal_rows(tmp_path):
    import csv
    from pathlib import Path
    import importlib.util
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "filter_hosts_focal_butterfly.py"
    spec = importlib.util.spec_from_file_location("iwe_host_filter_script", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    filter_focal_hosts = module.filter_focal_hosts
    original = tmp_path / "source.csv"
    header = ["Insect Genus", "Insect Species", "Hostplant Genus", "Hostplant Species"]
    data = [
        ["Anthocharis", "cardamines", "Cardamine", "pratensis"],
        ["Anthocharis", "cardamines", "Alliaria", "petiolata"],
        ["Other", "species", "Cardamine", "pratensis"],
    ]
    with original.open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(data)
    destination = tmp_path / "reduced" / "resource.csv"
    receipt = filter_focal_hosts(original, destination)
    assert receipt["focal_source_rows"] == 2
    assert receipt["distinct_nonblank_species_level_host_names"] == 2
    with destination.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert all(r["Insect Genus"] == "Anthocharis" for r in rows)
    assert original.exists()
