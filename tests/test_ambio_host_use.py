import json
from pathlib import Path
import subprocess
import sys
import pandas as pd
import pytest
from iwe.ambio_host_use import build_ambio_host_use

ROOT = Path(__file__).resolve().parents[1]


def files():
    return (
        pd.read_csv(ROOT / "data/registry/ambio_2015_table1_2010_host_use.csv",
                    dtype=str, keep_default_na=False),
        pd.read_csv(ROOT / "data/registry/oikos_2018_to_chocho_taxonomy.csv",
                    dtype=str, keep_default_na=False),
        pd.read_csv(ROOT / "data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv",
                    dtype=str, keep_default_na=False),
    )


def test_2010_real_published_count_reconciliation_and_source_warning():
    table, contrast, receipt = build_ambio_host_use(*files())
    assert len(table) == 21
    assert receipt["sampled_region_host_rows"] == 18
    assert receipt["host_not_found_rows_not_assigned_zero"] == 3
    assert receipt["sampled_plant_count"] == 16453
    assert receipt["observed_egg_count"] == 547
    assert receipt["plant_trait_record_count"] == 6187
    assert len(contrast) == 3
    assert len(receipt["material_published_ratio_discrepancies"]) == 1
    error = receipt["material_published_ratio_discrepancies"][0]
    assert error["region"] == "South"
    assert error["published_host"] == "Cardamine paludosa"
    assert error["reported"] == pytest.approx(0.085)
    assert error["derived_eggs_div_plants"] == pytest.approx(11 / 369)
    assert receipt["strict_h1_effects_created"] == 0
    assert receipt["source_overlap_with_oikos2018"] == "possible_same_programme_not_independent"


def test_exact_three_geographic_hosts_without_cytotype_or_genus_shortcut():
    table, _, receipt = build_ambio_host_use(*files())
    assert receipt["matched_chocho_host_species"] == [
        "Capsella bursa-pastoris", "Cardamine pratensis", "Turritis glabra"
    ]
    alias = table.loc[table["species_as_published"] == "Arabis glabra"].iloc[0]
    assert alias["normalized_accepted_name"] == "Turritis glabra"
    assert alias["accepted_plant_name_id"] == "2431978"
    cytotype = table.loc[table["species_as_published"] == "Cardamine paludosa"].iloc[0]
    assert cytotype["accepted_plant_name_id"] == ""
    assert cytotype["portfolio_match"] == "not_in_frozen_11_host_portfolio"
    assert table.loc[
        table["species_as_published"] == "Thlaspi caerulescens",
        "accepted_plant_name_id"
    ].eq("").all()


def test_missing_host_is_not_zero_egg_record():
    table, _, _ = build_ambio_host_use(*files())
    absent = table.loc[table["sampling_status"] == "host_not_found"]
    assert len(absent) == 3
    assert absent["n_eggs"].isna().all()
    assert absent["eggs_per_plant_recomputed"].isna().all()


def test_three_region_descriptive_reversal_not_independent_effect_size():
    _, contrast, _ = build_ambio_host_use(*files())
    rr = contrast.set_index("region")["observed_rate_ratio_cardamine_over_capsella"]
    assert rr["South"] == pytest.approx((30 / 2307) / (6 / 795))
    assert rr["Central"] == pytest.approx((21 / 67) / (24 / 556))
    assert rr["North"] == pytest.approx((2 / 180) / (42 / 719))
    assert rr["South"] > 1 and rr["Central"] > 1 and rr["North"] < 1
    assert all(contrast["comparison_type"] == "descriptive_observed_egg_rate_not_causal")


def test_source_drift_and_taxon_conflation_fail_closed():
    source, taxa, geo = files()
    with pytest.raises(ValueError, match="duplicate region-species"):
        build_ambio_host_use(pd.concat([source, source.iloc[[0]]]), taxa, geo)
    altered = source.copy()
    altered.loc[0, "n_eggs"] = "-1"
    with pytest.raises(ValueError, match="nonnegative"):
        build_ambio_host_use(altered, taxa, geo)
    altered = source.copy()
    altered.loc[altered["sampling_status"] == "host_not_found", "n_eggs"] = "0"
    with pytest.raises(ValueError, match="invented zero"):
        build_ambio_host_use(altered, taxa, geo)
    altered_taxa = taxa.copy()
    altered_taxa.loc[
        altered_taxa["species_as_published"] == "Arabis glabra",
        "accepted_plant_name_id"
    ] = "invalid"
    with pytest.raises(ValueError, match="missing frozen host ID"):
        build_ambio_host_use(source, altered_taxa, geo)


def test_cli_builds_original_source_receipts_without_inference(tmp_path):
    p = subprocess.run([
        sys.executable, str(ROOT / "scripts/audit_ambio_host_use.py"),
        "--output-dir", str(tmp_path)
    ], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    report = json.loads((tmp_path / "ambio_source_audit.json").read_text())
    assert report["observed_egg_count"] == 547
    assert len(report["source_input_sha256"]) == 3
    assert report["female_adult_flight_window_extracted"] is False
    assert report["strict_h1_effects_created"] == 0
    assert len(pd.read_csv(tmp_path / "ambio_region_host_2010_egg_rates.csv")) == 21
    assert len(pd.read_csv(tmp_path / "cardamine_vs_capsella_2010_descriptive.csv")) == 3
