import pandas as pd

from iwe.replication_routes import (
    active_completion_routes,
    validate_replication_completion_routes,
)


def _candidate(candidate_id="C1", target_class="antagonist", status="blocked_summary_stats", priority="P1"):
    return {
        "candidate_id": candidate_id,
        "target_class": target_class,
        "status": status,
        "priority": priority,
    }


def _route(**overrides):
    row = {
        "candidate_id": "C1",
        "target_class": "antagonist",
        "route_rank": 1,
        "source_access": "longform_not_public",
        "public_search_status": "exhausted",
        "unlock_type": "correct_unit_variance",
        "unlock_requirement": "recover correct-unit variance",
        "next_action_type": "retrieve_longform",
        "next_action": "obtain the long-form source",
        "stop_rule": "do not reuse nested observations",
        "last_audited": "2026-09-25",
    }
    row.update(overrides)
    return row


def test_valid_completion_route():
    errors = validate_replication_completion_routes(
        pd.DataFrame([_route()]),
        pd.DataFrame([_candidate()]),
    )
    assert errors == []


def test_route_must_point_to_blocked_candidate():
    errors = validate_replication_completion_routes(
        pd.DataFrame([_route()]),
        pd.DataFrame([_candidate(status="rejected_timing", priority="DROP")]),
    )
    assert any("non-blocked status" in error for error in errors)
    assert any("requires P1/P2" in error for error in errors)


def test_route_class_must_match_candidate_ledger():
    errors = validate_replication_completion_routes(
        pd.DataFrame([_route(target_class="mixed_pollinating_seed_predator")]),
        pd.DataFrame([_candidate(target_class="antagonist")]),
    )
    assert any("target_class disagrees" in error for error in errors)


def test_inactive_repository_is_monitor_only():
    errors = validate_replication_completion_routes(
        pd.DataFrame(
            [
                _route(
                    source_access="repository_inactive",
                    public_search_status="active",
                )
            ]
        ),
        pd.DataFrame([_candidate()]),
    )
    assert any("inactive repository must use monitor_only" in error for error in errors)


def test_ranks_are_contiguous_within_class():
    routes = pd.DataFrame(
        [
            _route(candidate_id="C1", route_rank=1),
            _route(candidate_id="C2", route_rank=3),
        ]
    )
    candidates = pd.DataFrame([_candidate("C1"), _candidate("C2")])
    errors = validate_replication_completion_routes(routes, candidates)
    assert any("route_rank must be contiguous" in error for error in errors)


def test_active_routes_sort_by_class_and_rank():
    routes = pd.DataFrame(
        [
            _route(candidate_id="A2", route_rank=2),
            _route(candidate_id="A1", route_rank=1),
        ]
    )
    candidates = pd.DataFrame([_candidate("A1"), _candidate("A2")])
    out = active_completion_routes(routes, candidates)
    assert list(out["candidate_id"]) == ["A1", "A2"]
