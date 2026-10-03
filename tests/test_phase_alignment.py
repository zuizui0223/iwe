import pandas as pd
import pytest

from iwe.phase_alignment import (
    phase_alignment_summary,
    validate_phase_alignment_registry,
)


def _rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate_id": "READY",
                "study_id": "STUDY_READY",
                "interaction_type": "antagonist",
                "dependence_id": "DEP_READY",
                "raw_or_adult_timing": "yes",
                "effective_consumer_timing": "yes",
                "prefinal_host_filter": "yes",
                "phase_alignment_varies": "yes",
                "final_plant_endpoint": "yes",
                "paired_simpler_vs_stage_comparison": "yes",
                "status": "confirmatory_ready",
                "blocker": "none",
                "notes": "synthetic complete row",
            },
            {
                "candidate_id": "NULL",
                "study_id": "STUDY_NULL",
                "interaction_type": "antagonist",
                "dependence_id": "DEP_NULL",
                "raw_or_adult_timing": "yes",
                "effective_consumer_timing": "yes",
                "prefinal_host_filter": "yes",
                "phase_alignment_varies": "yes",
                "final_plant_endpoint": "yes",
                "paired_simpler_vs_stage_comparison": "yes",
                "status": "boundary_null",
                "blocker": "none; retained as null",
                "notes": "synthetic null row",
            },
        ]
    )


def test_phase_alignment_registry_accepts_complete_and_null_rows():
    assert validate_phase_alignment_registry(_rows()) == []


def test_confirmatory_ready_requires_all_six_evidence_states_yes():
    df = _rows()
    df.loc[0, "effective_consumer_timing"] = "partial"
    errors = validate_phase_alignment_registry(df)
    assert any("confirmatory_ready requires all six" in error for error in errors)


def test_boundary_null_requires_final_paired_comparison():
    df = _rows()
    df.loc[1, "paired_simpler_vs_stage_comparison"] = "no"
    errors = validate_phase_alignment_registry(df)
    assert any("boundary_null requires" in error for error in errors)


def test_near_confirmatory_can_be_explicitly_blocked():
    df = _rows().iloc[[0]].copy()
    df.loc[:, "candidate_id"] = "BLOCKED"
    df.loc[:, "status"] = "near_confirmatory"
    df.loc[:, "raw_or_adult_timing"] = "blocked"
    df.loc[:, "paired_simpler_vs_stage_comparison"] = "blocked"
    df.loc[:, "blocker"] = "one recoverable timing object"
    assert validate_phase_alignment_registry(df) == []


def test_summary_separates_ready_near_and_null_states():
    df = _rows()
    near = df.iloc[[0]].copy()
    near.loc[:, "candidate_id"] = "NEAR"
    near.loc[:, "study_id"] = "STUDY_NEAR"
    near.loc[:, "dependence_id"] = "DEP_NEAR"
    near.loc[:, "status"] = "near_confirmatory"
    near.loc[:, "raw_or_adult_timing"] = "blocked"
    near.loc[:, "paired_simpler_vs_stage_comparison"] = "blocked"
    near.loc[:, "blocker"] = "missing numeric timing"
    combined = pd.concat([df, near], ignore_index=True)

    summary = phase_alignment_summary(combined)
    assert summary["confirmatory_ready"] == 1
    assert summary["near_confirmatory"] == 1
    assert summary["boundary_null"] == 1


def test_invalid_status_fails_before_summary():
    df = _rows()
    df.loc[0, "status"] = "wishful_thinking"
    with pytest.raises(ValueError):
        phase_alignment_summary(df)
