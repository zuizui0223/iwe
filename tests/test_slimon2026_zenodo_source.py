"""Synthetic checks: public metadata discovery is not a real adult census."""
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts.probe_slimon2026_zenodo_source import (
    archive_inventory, contexts, file_info, safe_source_link,
)


def test_fixed_zenodo_uris_reject_off_record_sources():
    assert safe_source_link("https://zenodo.org/api/records/19488509")
    assert safe_source_link(
        "https://zenodo.org/api/records/19488509/files/file/content")
    assert not safe_source_link("https://zenodo.org/api/records/OTHER")
    assert not safe_source_link("http://zenodo.org/api/records/19488509")
    assert not safe_source_link("https://evil.test/api/records/19488509")


def test_record_parses_only_two_source_named_files():
    metadata = {"files": {"entries": {
        "a": {"key": "Freese Stats.zip", "size": 100, "checksum": "md5:ok",
              "links": {"content": "https://zenodo.org/api/records/19488509/files/a/content"}},
        "b": {"key": "unrelated.txt", "size": 20,
              "links": {"content": "https://zenodo.org/api/records/19488509/files/b/content"}}
    }}}
    result = file_info(metadata)
    assert len(result) == 1
    assert result[0]["name"] == "Freese Stats.zip"


def test_zip_inventory_reports_real_headers_not_fake_activity():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("data/traits.csv", "plant_id,flower_start,seed_total\na,100,22\n")
        z.writestr("R/run.R", "# adult flight? method not verified\n")
    out = archive_inventory(b.getvalue())
    assert out[0]["headers"] == ["plant_id", "flower_start", "seed_total"]
    assert out[0]["rows"] == 1
    assert out[1]["candidate_timing_lines"]
    assert not any("adult_partner_window_verified" in o for o in out)


def test_archive_rejects_path_traversal_and_readme_leads_do_not_certify():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("../secret.csv", "a\n1")
    with pytest.raises(ValueError, match="unsafe"):
        archive_inventory(b.getvalue())
    hits = contexts("Study flowering and seed predator adult activity.")
    assert hits
    assert all(x["source_verified_method_claim"] is False for x in hits)


def test_malformed_csv_remains_a_source_warning_not_imputed_data():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("raw/old_export.csv", "plant,adult\na,1\u0000\u000bb,2\n")
    out = archive_inventory(b.getvalue())
    assert len(out) == 1
    # A corrupted source must not be silently treated as an adult census.
    assert out[0]["member"] == "raw/old_export.csv"
    assert "adult_partner_window_verified" not in out[0]


def test_synthetic_stage_preflight_separates_2022_adult_from_2023_larvae():
    from scripts.probe_slimon2026_zenodo_source import stage_linkage_preflight
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("Freese Stats/df2_exp1F.csv",
                   "ID #,sf_adult_7_11,sf_larvae_7_19\na,2,0\nb,0,3\n")
        z.writestr("Freese Stats/df2_exp2F.csv",
                   "ID,sf_larvae_7_26\na,1\nb,0\n")
        z.writestr("Freese Stats/main_exp1.csv", "ID,first_flr\na,190\nb,195\n")
        z.writestr("Freese Stats/main_exp2.csv", "ID,first_flr\na,191\nb,193\n")
        z.writestr("Freese Stats/fitness_exp1.csv", "ID,lg frt,schinia\na,5,0\nb,6,2\n")
        z.writestr("Freese Stats/Exp 2 fitness.csv", "ID,lg frt,schinia\na,8,1\nb,2,0\n")
    audit = stage_linkage_preflight(b.getvalue())
    assert audit["join_by_original_plant_id"]["2022"]["host_stage_fruit_shared_ids"] == 2
    assert audit["date_resolved_focal_adult_counts"]["adult"]["sf_adult_7_11"]["positive_rows"] == 1
    assert audit["exp2_2023_has_sf_adult_columns"] is False
    assert audit["independent_adult_partner_availability_identified"] is False
    assert audit["original_mature_intact_seed_by_date_verified"] is False
    assert audit["strict_h1_effect"] is False


def test_published_fitness_code_leads_are_not_an_unverified_seed_formula():
    from scripts.probe_slimon2026_zenodo_source import fitness_model_code_leads
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("Freese Stats/exp1_pubver.R",
                   "# seed estimate unverified\n"
                   "plantfitness <- total_fruit * mean_seed\n")
        z.writestr("Freese Stats/exp2_pubver.R", "x <- 2\n")
    source = fitness_model_code_leads(b.getvalue())
    hits = source["Freese Stats/exp1_pubver.R"]
    assert len(hits) == 1
    assert hits[0]["source_line"] == 2
    assert hits[0]["derived_seed_fitness_formula_verified"] is False
