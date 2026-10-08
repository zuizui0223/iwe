"""Synthetic-only tests: public derivative sources lack Hurlburt's original IDs."""
import pandas as pd
import pytest

from iwe.hurlburt_join import audit_marked_unit_join


def _tables():
    marked = pd.DataFrame([
        {"year": 1999, "clone_id": "C01", "inflorescence_id": "I01",
         "first_flower_date": "1999-06-15", "last_flower_date": "1999-07-05"},
        {"year": 1999, "clone_id": "C02", "inflorescence_id": "I02",
         "first_flower_date": "1999-06-18", "last_flower_date": "1999-07-10"},
    ])
    adult = pd.DataFrame([
        {"year": 1999, "census_date": "1999-06-20", "adult_moth_count": 5},
        {"year": 1999, "census_date": "1999-06-25", "adult_moth_count": 2},
    ])
    fruits = pd.DataFrame([
        {"year": 1999, "clone_id": "C01", "inflorescence_id": "I01",
         "fruit_id": "1", "viable_seeds": 43},
        {"year": 1999, "clone_id": "C01", "inflorescence_id": "I01",
         "fruit_id": "2", "viable_seeds": 0},
        {"year": 1999, "clone_id": "C02", "inflorescence_id": "I02",
         "fruit_id": "1", "viable_seeds": 120},
    ])
    manifest = {"mode": "synthetic_fixture"}
    return marked, adult, fruits, manifest


def test_synthetic_join_keeps_fruits_nested_and_prevents_smd():
    result = audit_marked_unit_join(*_tables())
    assert result["status"] == "source_unit_lineage_structurally_present_not_an_effect"
    assert result["linked_marked_inflorescences"] == 2
    assert result["mature_fruits_with_exact_marked_unit_join"] == 3
    assert result["unmatched_mature_fruits"] == 0
    assert result["year_breakdown"]["1999"]["adult_census_days"] == 2
    assert result["date_resolved_adult_and_mature_fruit_join_present"] is False
    assert result["strict_h1_effect_promoted"] is False
    assert result["plant_fitness_effect_estimated"] is False
    assert result["unobserved_aborted_fruits_imputed"] is False


def test_annual_aggregate_does_not_carry_source_marked_join():
    marked, adult, fruits, manifest = _tables()
    marked = marked.drop(columns=["clone_id", "inflorescence_id"])
    with pytest.raises(ValueError, match="missing"):
        audit_marked_unit_join(marked, adult, fruits, manifest)


def test_unknown_mature_fruit_keys_do_not_become_phenology_matches():
    marked, adult, fruits, manifest = _tables()
    fruits.loc[:, "inflorescence_id"] = "different"
    status = audit_marked_unit_join(marked, adult, fruits, manifest)
    assert status["status"] == "blocked_no_mature_fruit_to_marked_flowering_unit_join"
    assert status["unmatched_mature_fruits"] == 3


def test_partial_join_flags_survivor_selection_risk():
    marked, adult, fruits, manifest = _tables()
    fruits.loc[2, "inflorescence_id"] = "unknown"
    status = audit_marked_unit_join(marked, adult, fruits, manifest)
    assert status["status"] == "blocked_partial_matched_subset_selection_risk"
    assert status["mature_fruits_with_exact_marked_unit_join"] == 2


def test_moth_activity_requires_repeated_censuses_in_same_year():
    marked, adult, fruits, manifest = _tables()
    adult = adult.iloc[:1].copy()
    status = audit_marked_unit_join(marked, adult, fruits, manifest)
    assert status["status"] == "blocked_insufficient_same_season_adult_and_linked_units"


def test_source_mode_requires_actual_original_pdf_locators():
    marked, adult, fruits, _ = _tables()
    manifest = {
        "mode": "original_source_review",
        "site": "Onefour",
        "thesis_doi": "10.7939/r3-fe1d-kj80",
        "original_pdf_inspected": False,
    }
    with pytest.raises(ValueError, match="PDF review"):
        audit_marked_unit_join(marked, adult, fruits, manifest)
    manifest["original_pdf_inspected"] = True
    with pytest.raises(ValueError, match="locator"):
        audit_marked_unit_join(marked, adult, fruits, manifest)


def test_duplicate_fruit_rejected_instead_of_double_counting():
    marked, adult, fruits, manifest = _tables()
    fruits = pd.concat([fruits, fruits.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate source fruit"):
        audit_marked_unit_join(marked, adult, fruits, manifest)


def test_same_year_join_does_not_join_across_years():
    marked, adult, fruits, manifest = _tables()
    fruits.loc[0, "year"] = 2000
    fruits.loc[0, "fruit_id"] = "different"
    status = audit_marked_unit_join(marked, adult, fruits, manifest)
    assert status["status"] == "blocked_partial_matched_subset_selection_risk"


def test_invalid_intervals_and_seed_values_fail_closed():
    marked, adult, fruits, manifest = _tables()
    marked.loc[0, "last_flower_date"] = "1999-06-01"
    with pytest.raises(ValueError, match="ends before"):
        audit_marked_unit_join(marked, adult, fruits, manifest)
    marked, adult, fruits, manifest = _tables()
    fruits.loc[0, "viable_seeds"] = -1
    with pytest.raises(ValueError, match="non-negative"):
        audit_marked_unit_join(marked, adult, fruits, manifest)
