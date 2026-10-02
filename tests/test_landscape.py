import pandas as pd
import pytest

from iwe.landscape import (
    landscape_pilot_summary,
    validate_landscape_registry,
)


def _rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "component_id": "A",
                "study_id": "IWEA",
                "interaction_type": "mutualist",
                "window_reference_class": "independent_partner_activity",
                "timing_geometry": "ordered_window",
                "fitness_channel": "net_reproduction",
                "outcome_finality": "final",
                "current_quant_status": "extracted",
                "landscape_status": "strong_candidate",
                "dependence_id": "DEP_A",
                "notes": "anchor",
            },
            {
                "component_id": "B",
                "study_id": "IWEB",
                "interaction_type": "antagonist",
                "window_reference_class": "realized_interaction_window",
                "timing_geometry": "seasonal_gradient",
                "fitness_channel": "net_reproduction",
                "outcome_finality": "final",
                "current_quant_status": "pending",
                "landscape_status": "candidate_noncausal_window",
                "dependence_id": "DEP_B",
                "notes": "descriptive realized window",
            },
        ]
    )


def test_landscape_registry_accepts_separated_reference_classes():
    assert validate_landscape_registry(_rows()) == []


def test_strong_candidate_requires_independent_reference_and_final_outcome():
    df = _rows()
    df.loc[0, "window_reference_class"] = "realized_interaction_window"
    errors = validate_landscape_registry(df)
    assert any("strong_candidate requires" in error for error in errors)


def test_pilot_summary_counts_programmes_not_rows_for_recovery():
    df = pd.concat(
        [_rows(), _rows().iloc[[0]].assign(component_id="A2")],
        ignore_index=True,
    )
    summary = landscape_pilot_summary(df)
    assert summary["n_components"] == 3
    assert summary["recoverable_programmes_by_class"]["mutualist"] == 1
    assert summary["recoverable_programmes_by_class"]["antagonist"] == 1


def test_invalid_registry_fails_before_summary():
    df = _rows()
    df.loc[0, "interaction_type"] = "unknown"
    with pytest.raises(ValueError):
        landscape_pilot_summary(df)


def test_channel_decoupling_is_reserved_for_mixed_interactions():
    df = _rows()
    df.loc[1, "landscape_status"] = "channel_decoupling_evidence"
    errors = validate_landscape_registry(df)
    assert any("channel_decoupling_evidence must be a mixed interaction" in error for error in errors)


def test_experimental_timing_requires_direct_manipulation_and_final_outcome():
    df = _rows()
    df.loc[1, "landscape_status"] = "experimental_timing_evidence"
    errors = validate_landscape_registry(df)
    assert any("experimental_timing_evidence requires" in error for error in errors)


def test_selection_shift_requires_final_outcome():
    df = _rows()
    df.loc[1, "landscape_status"] = "selection_shift_evidence"
    df.loc[1, "outcome_finality"] = "not_final"
    errors = validate_landscape_registry(df)
    assert any("selection_shift_evidence requires a final outcome" in error for error in errors)


def test_realized_window_evidence_requires_realized_window_and_final_outcome():
    df = _rows()
    df.loc[1, "landscape_status"] = "realized_window_evidence"
    assert validate_landscape_registry(df) == []

    df.loc[1, "window_reference_class"] = "seasonal_position_only"
    errors = validate_landscape_registry(df)
    assert any("realized_window_evidence requires" in error for error in errors)
