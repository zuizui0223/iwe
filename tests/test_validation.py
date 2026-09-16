import pandas as pd

from iwe.validation import build_primary_dataset, validate_effect_rows


def _row(**overrides):
    row = {
        "effect_id": "E1",
        "study_id": "S1",
        "dataset_id": "D1",
        "dependence_id": "DEP1",
        "plant_taxon": "Plant a",
        "animal_taxon": "Animal a",
        "interaction_type": "mutualist",
        "evidence_tier": "A",
        "phenology_source": "direct_interaction",
        "exposure_direction": "synchrony",
        "outcome_family": "seed_set",
        "effect_family": "standardized_slope",
        "effect_native": 0.2,
        "variance_native": 0.04,
        "sample_size": 30,
        "source_id": "doi:test",
    }
    row.update(overrides)
    return row


def test_valid_row_has_no_errors():
    assert validate_effect_rows(pd.DataFrame([_row()])) == []


def test_tier_c_is_excluded_from_primary_dataset():
    df = pd.DataFrame([_row(effect_id="A", evidence_tier="A"), _row(effect_id="C", evidence_tier="C", phenology_source="occurrence_proxy")])
    out = build_primary_dataset(df)
    assert list(out["effect_id"]) == ["A"]


def test_missing_variance_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(variance_native=None)]))
    assert any("variance_native" in error for error in errors)


def test_duplicate_effect_id_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(), _row()]))
    assert any("duplicate effect_id" in error for error in errors)


def test_unknown_interaction_type_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(interaction_type="commensal")]))
    assert any("interaction_type" in error for error in errors)


def test_mismatch_is_oriented_in_primary_dataset():
    out = build_primary_dataset(pd.DataFrame([_row(exposure_direction="mismatch", effect_native=0.3)]))
    assert out.iloc[0]["effect_oriented"] == -0.3
