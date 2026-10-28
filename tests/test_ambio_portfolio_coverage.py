from pathlib import Path
import json
import subprocess
import sys
import pandas as pd
import pytest

from iwe.ambio_portfolio_coverage import summarize_ambio_portfolio_coverage

ROOT = Path(__file__).resolve().parents[1]


def inputs():
    p = [
        "data/registry/ambio_2015_table1_2010_host_use.csv",
        "data/registry/oikos_2018_to_chocho_taxonomy.csv",
        "data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv",
    ]
    return [pd.read_csv(ROOT / x, dtype=str, keep_default_na=False) for x in p]


def test_focal_host_taxonomic_coverage_outside_chocho_source():
    regional, taxa, receipt = summarize_ambio_portfolio_coverage(*inputs())
    assert receipt["total_eggs"] == 547
    assert receipt["exact_frozen_portfolio_eggs"] == 200
    assert receipt["separate_octoploid_cardamine_eggs"] == 245
    assert receipt["other_documented_host_taxa_eggs"] == 102
    assert receipt["exact_portfolio_coverage_fraction_of_eggs"] == pytest.approx(200 / 547)
    assert receipt["hypothetical_with_octoploid_grouped_fraction"] == pytest.approx(445 / 547)
    assert receipt["strict_accepted_portfolio_host_taxa"] == 3
    assert receipt["octoploid_is_currently_mapped_to_species"] is False
    assert receipt["strict_h1_effects_created"] == 0
    assert regional["total_published_eggs"].tolist() == [110, 194, 243]
    assert regional["eggs_on_exact_frozen_portfolio_taxa"].tolist() == [36, 67, 97]
    assert len(taxa) == 7
    groups = dict(zip(taxa.species_as_published, taxa.source_egg_total))
    assert groups["Cardamine paludosa"] == 245
    assert groups["Arabis hirsuta"] == 66
    assert groups["Arabidopsis thaliana"] == 16
    assert groups["Thlaspi caerulescens"] == 20


def test_absent_hosts_remain_absent_not_unobserved_zeros():
    source, taxon, geo = inputs()
    zero_invented = source.copy()
    i = zero_invented["sampling_status"] == "host_not_found"
    zero_invented.loc[i, "n_eggs"] = "0"
    with pytest.raises(ValueError, match="invented zero"):
        summarize_ambio_portfolio_coverage(zero_invented, taxon, geo)


def test_cli_writes_reproducible_coverage_and_noninferential_receipt(tmp_path):
    p = subprocess.run(
        [sys.executable, str(ROOT / "scripts/audit_ambio_portfolio_coverage.py"),
         "--out-dir", str(tmp_path)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert p.returncode == 0, p.stderr
    receipt = json.loads((tmp_path / "portfolio_coverage_receipt.json").read_text())
    assert receipt["other_unmatched_taxa_are_true_nonhosts"] is False
    assert receipt["source_overlap_with_oikos2018"] == "possible_same_programme_not_independent"
    assert len(receipt["input_sha256"]) == 3
    assert len(pd.read_csv(tmp_path / "region_portfolio_coverage.csv")) == 3
    assert len(pd.read_csv(tmp_path / "reported_host_taxon_egg_coverage.csv")) == 7
