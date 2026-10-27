from pathlib import Path
import math
import pandas as pd
import pytest
from iwe.oikos_sampling_bridge import build_oikos_sampling_crosswalk

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "data/registry/oikos_2018_table_a1_sampling.csv"
TAXON = BASE / "data/registry/oikos_2018_to_chocho_taxonomy.csv"
HOSTS = BASE / "data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv"


def load():
    return [
        pd.read_csv(path, dtype=str, keep_default_na=False)
        for path in (SOURCE, TAXON, HOSTS)
    ]


def test_oikos_sampling_denominators_are_exact_and_nonpromoting():
    strata, species, audit = build_oikos_sampling_crosswalk(*load())
    assert len(strata) == 60
    assert len(species) == 6
    assert audit["plant_records_sum_across_strata"] == 22933
    assert audit["unique_region_species_cohorts"] == 15
    assert audit["year_region_species_strata"] == 60
    assert audit["individual_phenophase_values_extracted"] is False
    assert audit["individual_oviposition_incidence_values_extracted"] is False
    assert audit["strict_h1_effects_created"] == 0
    assert audit["ecological_claim_permitted"] is False
    sums = species.set_index("species_as_published")["n_plants_all_strata"].to_dict()
    assert sums == {
        "Arabis glabra": 1032,
        "Arabis hirsuta": 3455,
        "Cardamine pratensis": 7842,
        "Arabidopsis thaliana": 4893,
        "Capsella bursa-pastoris": 3495,
        "Thlaspi caerulescens": 2216,
    }
    regions = strata.groupby("region")["n_plants"].sum().to_dict()
    assert regions == {"Skåne": 8063, "Uppland": 9408, "Ångermanland": 5462}


def test_verified_homotypic_synonym_adds_third_biological_match():
    _, species, audit = build_oikos_sampling_crosswalk(*load())
    matches = species.loc[species["portfolio_match"] == "matched"]
    assert len(matches) == 3
    assert set(matches["normalized_accepted_name"]) == {
        "Turritis glabra", "Cardamine pratensis", "Capsella bursa-pastoris"
    }
    alias = matches.set_index("species_as_published").loc["Arabis glabra"]
    assert alias["normalized_accepted_name"] == "Turritis glabra"
    assert alias["accepted_plant_name_id"] == "2431978"
    assert alias["normalization"] == "homotypic_synonym"
    assert audit["matched_plant_records_sum"] == 12369
    assert math.isclose(
        audit["matched_hosts_fractional_geographic_credit"],
        43 + 0.4 + 2.083333333333333, abs_tol=1e-9
    )
    assert audit["matched_share_of_added_resource_credit"] == pytest.approx(
        (43 + 0.4 + 2.083333333333333) / 110
    )


def test_no_false_thlaspi_genus_match():
    _, species, _ = build_oikos_sampling_crosswalk(*load())
    thlaspi = species.set_index("species_as_published").loc["Thlaspi caerulescens"]
    assert thlaspi["normalized_accepted_name"] == "Noccaea caerulescens"
    assert thlaspi["portfolio_match"] == "not_in_frozen_11_host_portfolio"
    assert thlaspi["accepted_plant_name_id"] == ""
    assert pd.isna(thlaspi["fractional_added_unit_credit"])


def test_drift_missing_names_and_duplicated_cohort_fail_closed():
    table, taxonomy, hosts = load()
    with pytest.raises(ValueError, match="duplicated"):
        build_oikos_sampling_crosswalk(pd.concat([table, table.iloc[[0]]]), taxonomy, hosts)
    bad = taxonomy.copy()
    bad.loc[bad.species_as_published == "Arabis glabra", "accepted_plant_name_id"] = "999"
    with pytest.raises(ValueError, match="accepted plant ID mismatch"):
        build_oikos_sampling_crosswalk(table, bad, hosts)
    bad2 = taxonomy.copy()
    bad2.loc[bad2.species_as_published == "Thlaspi caerulescens",
             "normalized_accepted_name"] = "Thlaspi arvense"
    with pytest.raises(ValueError, match="portfolio match disagreement"):
        build_oikos_sampling_crosswalk(table, bad2, hosts)
    bad3 = table.copy()
    bad3.loc[0, "n_2010"] = "-1"
    with pytest.raises(ValueError, match="nonnegative integer"):
        build_oikos_sampling_crosswalk(bad3, taxonomy, hosts)


def test_cli_generates_source_auditable_outputs(tmp_path):
    import subprocess
    import sys
    import json
    completed = subprocess.run(
        [sys.executable, str(BASE / "scripts/audit_oikos_sampling_bridge.py"),
         "--output-dir", str(tmp_path)],
        cwd=BASE, text=True, capture_output=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads((tmp_path / "source_crosswalk_receipt.json").read_text(encoding="utf-8"))
    assert result["plant_records_sum_across_strata"] == 22933
    assert result["year_region_species_strata"] == 60
    assert result["host_species_in_frozen_chocho_portfolio"] == 3
    assert len(result["input_sha256"]) == 3
    assert result["strict_h1_effects_created"] == 0
    assert len(pd.read_csv(tmp_path / "oikos_region_species_year_strata.csv")) == 60
    assert len(pd.read_csv(tmp_path / "oikos_species_to_chocho_hosts.csv")) == 6
