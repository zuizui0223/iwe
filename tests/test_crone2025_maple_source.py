"""Independent Acer mast/pollinator/exclusion archive is not IWE strict H1."""
import pytest
from scripts.probe_crone2025_maple_source import (
    API,_allowed,source_csv,source_R_code,EXPECTED_NAMES,
    SOURCE_MD5,original_file_url
)


def test_zenodo_record_link_is_exact_not_arbitrary_data():
    assert _allowed(API)
    # Zenodo supplies /api/files/<bucket>/<file> URLs for original
    # record entries; this is not an external search or forged DOI.
    assert _allowed("https://zenodo.org/api/files/UUID/from_exact_record.csv")
    assert _allowed(
        "https://zenodo.org/api/records/15090572/files/HFmaple.seedcounts.csv/content"
    )
    assert not _allowed("https://zenodo.org/api/records/19488509")
    assert not _allowed("https://somewhere-else.org/api/records/15090572")


def test_original_plant_year_values_reported_not_invented_flowering_dates():
    raw=(b"tree,year,flowering,filled_seed,predated_seed\n"
         b"A,2012,2,12,7\nB,2013,4,25,8\n")
    r=source_csv(raw,"HFmaple.seedcounts.csv")
    assert r["source_n_rows"]==2
    assert r["source_year_values"]==["2012","2013"]
    assert "tree" in r["source_headers"]
    assert "filled_seed" in r["biological_stage_column_candidates"]
    assert r["exact_tree_year_join_verified"] is False
    assert r["source_raw_total_viable_seed_effect_inferred"] is False


def test_source_R_code_leads_are_not_causal_reproduction_proof():
    r=source_R_code(
        b"model <- glm(seed_predation ~ flowering)\n",
        "mast patterns only.R"
    )
    assert r["source_R_lines"]==1
    assert r["original_source_reanalysis_leads"][0]["original_line"]==1
    assert r["real_biological_effect_recomputed"] is False


def test_expected_archive_has_independent_year_and_exclusion_approaches():
    assert "HFmaple.pollenexclusion.2012_2017.csv" in EXPECTED_NAMES
    assert "HFmaple.seedcounts.2011_2024.csv" in EXPECTED_NAMES
    assert "HFmaple.flowering.qual.2011_2024.csv" in EXPECTED_NAMES


def test_record_pinned_source_urls_and_checksums():
    assert set(SOURCE_MD5)==EXPECTED_NAMES
    url=original_file_url("EOS only.R")
    assert url=="https://zenodo.org/records/15090572/files/EOS%20only.R?download=1"
    assert _allowed(url)
    assert SOURCE_MD5["HFmaple.pollenexclusion.2012_2017.csv"] == (
        "ce3ac3911f898d84743f850485ce2c2e"
    )
    with pytest.raises(ValueError,match="not in the frozen"):
        original_file_url("../an-unrelated-file")
