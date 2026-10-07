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


def test_paired_realized_positive_requires_phase_final_and_paired_comparison():
    df = _rows().iloc[[0]].copy()
    df.loc[:, "candidate_id"] = "PAIRED"
    df.loc[:, "study_id"] = "STUDY_PAIRED"
    df.loc[:, "dependence_id"] = "DEP_PAIRED"
    df.loc[:, "raw_or_adult_timing"] = "partial"
    df.loc[:, "effective_consumer_timing"] = "partial"
    df.loc[:, "prefinal_host_filter"] = "partial"
    df.loc[:, "status"] = "paired_realized_positive"
    df.loc[:, "blocker"] = "realized exposure; not adult timing"

    assert validate_phase_alignment_registry(df) == []

    df.loc[:, "paired_simpler_vs_stage_comparison"] = "no"
    errors = validate_phase_alignment_registry(df)
    assert any("paired_realized_positive requires" in error for error in errors)


def test_summary_counts_nonconfirmatory_positive_pair_separately():
    df = _rows()
    paired = df.iloc[[0]].copy()
    paired.loc[:, "candidate_id"] = "PAIRED"
    paired.loc[:, "study_id"] = "STUDY_PAIRED"
    paired.loc[:, "dependence_id"] = "DEP_PAIRED"
    paired.loc[:, "raw_or_adult_timing"] = "partial"
    paired.loc[:, "effective_consumer_timing"] = "partial"
    paired.loc[:, "prefinal_host_filter"] = "partial"
    paired.loc[:, "status"] = "paired_realized_positive"
    paired.loc[:, "blocker"] = "realized exposure; not adult timing"

    combined = pd.concat([df, paired], ignore_index=True)
    summary = phase_alignment_summary(combined)
    assert summary["confirmatory_ready"] == 1
    assert summary["paired_realized_positive"] == 1


def test_host_sensitivity_final_requires_filter_phase_and_final_endpoint():
    df = _rows().iloc[[0]].copy()
    df.loc[:, "candidate_id"] = "HOST_FINAL"
    df.loc[:, "study_id"] = "STUDY_HOST_FINAL"
    df.loc[:, "dependence_id"] = "DEP_HOST_FINAL"
    df.loc[:, "status"] = "host_sensitivity_final"
    df.loc[:, "paired_simpler_vs_stage_comparison"] = "no"
    assert validate_phase_alignment_registry(df) == []

    df.loc[:, "prefinal_host_filter"] = "partial"
    errors = validate_phase_alignment_registry(df)
    assert any("host_sensitivity_final requires" in error for error in errors)


def test_duplicate_study_dependence_phase_rows_fail():
    df = _rows()
    duplicate = df.iloc[[0]].copy()
    duplicate.loc[:, "candidate_id"] = "READY_DUPLICATE"
    combined = pd.concat([df, duplicate], ignore_index=True)

    errors = validate_phase_alignment_registry(combined)
    assert any("duplicate phase-alignment programme rows" in error for error in errors)


def test_paired_predictive_stress_test_separates_positive_and_nulls():
    df = _rows()
    positive = df.iloc[[0]].copy()
    positive["candidate_id"] = "POSITIVE"
    positive["study_id"] = "POS_STUDY"
    positive["dependence_id"] = "POS_DEP"
    positive["raw_or_adult_timing"] = "partial"
    positive["effective_consumer_timing"] = "partial"
    positive["prefinal_host_filter"] = "partial"
    positive["phase_alignment_varies"] = "yes"
    positive["final_plant_endpoint"] = "yes"
    positive["paired_simpler_vs_stage_comparison"] = "yes"
    positive["status"] = "paired_realized_positive"
    positive["blocker"] = "realized exposure only"

    null = positive.copy()
    null["candidate_id"] = "NULL"
    null["study_id"] = "NULL_STUDY"
    null["dependence_id"] = "NULL_DEP"
    null["raw_or_adult_timing"] = "yes"
    null["effective_consumer_timing"] = "yes"
    null["prefinal_host_filter"] = "yes"
    null["status"] = "boundary_null"
    null["blocker"] = "none"

    combined = pd.concat([positive, null], ignore_index=True)
    summary = phase_alignment_summary(combined)
    assert summary["paired_final_comparisons"] == 2
    assert summary["paired_positive_nonconfirmatory"] == 1
    assert summary["paired_boundary_null"] == 1
    assert summary["paired_positive_ids"] == ["POSITIVE"]
    assert summary["paired_null_ids"] == ["NULL"]
