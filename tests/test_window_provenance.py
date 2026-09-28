import pandas as pd

from iwe.window_provenance import validate_strict_window_provenance


def _effect(effect_id="E1", study_id="S1", timing="strict_window"):
    return {
        "effect_id": effect_id,
        "study_id": study_id,
        "evidence_tier": "A",
        "timing_analysis_class": timing,
        "source_id": "10.example/source",
    }


def _provenance(effect_id="E1", study_id="S1", basis="direct_visitation"):
    return {
        "effect_id": effect_id,
        "study_id": study_id,
        "window_basis": basis,
        "same_season": "yes",
        "source_id": "10.example/source",
        "source_measurement": "adult activity measured independently",
        "notes": "",
    }


def test_valid_strict_window_provenance():
    errors = validate_strict_window_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([_provenance()]),
    )
    assert errors == []


def test_egg_receipt_cannot_define_strict_partner_window():
    errors = validate_strict_window_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([_provenance(basis="egg_receipt")]),
    )
    assert any("forbidden partner-window basis" in error for error in errors)


def test_strict_effect_requires_provenance_row():
    errors = validate_strict_window_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame(
            columns=[
                "effect_id",
                "study_id",
                "window_basis",
                "same_season",
                "source_id",
                "source_measurement",
                "notes",
            ]
        ),
    )
    assert any("lacks strict partner-window provenance" in error for error in errors)


def test_non_strict_effect_does_not_require_window_provenance():
    errors = validate_strict_window_provenance(
        pd.DataFrame([_effect(timing="direct_timing_sensitivity")]),
        pd.DataFrame(
            columns=[
                "effect_id",
                "study_id",
                "window_basis",
                "same_season",
                "source_id",
                "source_measurement",
                "notes",
            ]
        ),
    )
    assert errors == []
