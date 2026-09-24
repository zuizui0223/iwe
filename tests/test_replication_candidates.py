import pandas as pd
import pytest

from iwe.replication_candidates import (
    ready_replication_candidates,
    validate_replication_candidates,
)


def _row(**overrides):
    row = {
        "candidate_id": "C1",
        "source_id": "doi:test",
        "plant_taxon": "Plant",
        "animal_taxon": "Animal",
        "target_class": "mixed_pollinating_seed_predator",
        "effect_family_target": "standardized_mean_difference",
        "independent_programme": "yes",
        "timing_window_measured": "yes",
        "post_predation_final_reproduction": "yes",
        "smd_summary_stats": "yes",
        "status": "ready",
        "blocker": "",
        "priority": "P1",
        "notes": "",
    }
    row.update(overrides)
    return row


def test_ready_requires_all_four_gates():
    errors = validate_replication_candidates(
        pd.DataFrame([_row(smd_summary_stats="no")])
    )
    assert any("ready candidate fails gates" in e for e in errors)


def test_all_four_gates_force_ready_status():
    errors = validate_replication_candidates(
        pd.DataFrame([_row(status="blocked_summary_stats")])
    )
    assert any("all four gates pass" in e for e in errors)


def test_blocked_candidate_is_valid_when_gate_fails():
    row = _row(
        smd_summary_stats="no",
        status="blocked_summary_stats",
        blocker="summary missing",
    )
    assert validate_replication_candidates(pd.DataFrame([row])) == []


def test_ready_filter_returns_only_ready_candidates():
    df = pd.DataFrame(
        [
            _row(candidate_id="R1"),
            _row(
                candidate_id="B1",
                smd_summary_stats="no",
                status="blocked_summary_stats",
            ),
        ]
    )
    out = ready_replication_candidates(df)
    assert list(out["candidate_id"]) == ["R1"]


def test_duplicate_candidate_id_fails():
    errors = validate_replication_candidates(pd.DataFrame([_row(), _row()]))
    assert any("duplicate candidate_id" in e for e in errors)


def test_partial_timing_linkage_can_remain_blocked():
    row = _row(
        timing_window_measured="partial",
        smd_summary_stats="partial",
        status="blocked_timing_linkage",
        blocker="partner activity and final fitness are measured but not linked at the focal unit",
    )
    assert validate_replication_candidates(pd.DataFrame([row])) == []
