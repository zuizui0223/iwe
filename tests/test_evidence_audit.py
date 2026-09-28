import pandas as pd

from iwe.evidence_audit import evidence_audit_summary, render_evidence_audit_status


def _studies():
    return pd.DataFrame(
        [
            {
                "study_id": "M1",
                "screening_status": "include",
                "interaction_type_candidate": "mutualist",
            },
            {
                "study_id": "A1",
                "screening_status": "include",
                "interaction_type_candidate": "antagonist",
            },
            {
                "study_id": "X1",
                "screening_status": "context_only",
                "interaction_type_candidate": "mixed_pollinating_seed_predator",
            },
        ]
    )


def _effects():
    return pd.DataFrame(
        [
            {
                "study_id": "M1",
                "dependence_id": "DM1",
                "interaction_type": "mutualist",
                "evidence_tier": "A",
                "timing_analysis_class": "strict_window",
                "effect_family": "standardized_mean_difference",
            },
            {
                "study_id": "A1",
                "dependence_id": "DA1",
                "interaction_type": "antagonist",
                "evidence_tier": "A",
                "timing_analysis_class": "strict_window",
                "effect_family": "standardized_mean_difference",
            },
            {
                "study_id": "M1",
                "dependence_id": "DM1",
                "interaction_type": "mutualist",
                "evidence_tier": "A",
                "timing_analysis_class": "direct_timing_sensitivity",
                "effect_family": "standardized_mean_difference",
            },
        ]
    )


def _adjudications():
    return pd.DataFrame(
        [
            {"quantitative_status": "strict_extracted"},
            {"quantitative_status": "strict_extracted"},
            {"quantitative_status": "pending"},
        ]
    )


def _candidates():
    return pd.DataFrame(
        [
            {"status": "rejected_timing"},
            {"status": "blocked_final_surface"},
            {"status": "ready"},
        ]
    )


def _routes():
    return pd.DataFrame(
        [
            {
                "target_class": "antagonist",
                "public_search_status": "exhausted",
                "source_access": "public_source_insufficient",
                "next_action_type": "contact_or_archive",
            },
            {
                "target_class": "mixed_pollinating_seed_predator",
                "public_search_status": "monitor_only",
                "source_access": "active_project_unreleased",
                "next_action_type": "monitor_source_release",
            },
        ]
    )


def test_evidence_audit_keeps_denominators_separate():
    out = evidence_audit_summary(
        _studies(), _effects(), _adjudications(), _candidates(), _routes()
    )
    assert out["registered_publications"] == 3
    assert out["replication_candidates"] == 3
    assert out["strict_effect_rows"] == 2
    assert out["strict_studies"] == 2
    assert out["smd_by_class"]["mutualist"]["clusters"] == 1
    assert out["smd_by_class"]["antagonist"]["clusters"] == 1
    assert out["smd_by_class"]["mixed_pollinating_seed_predator"]["clusters"] == 0
    assert out["candidate_rejected"] == 1
    assert out["candidate_blocked"] == 1
    assert out["candidate_ready"] == 1


def test_rendered_audit_states_inference_boundary():
    text = render_evidence_audit_status(
        _studies(), _effects(), _adjudications(), _candidates(), _routes()
    )
    assert "discovery milestone only" in text
    assert "evidence-architecture gap" in text
    assert "not a count of unique screened publications" in text
    assert "active generic public-search routes" in text
