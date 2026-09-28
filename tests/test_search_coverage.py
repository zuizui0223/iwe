import pandas as pd

from iwe.search_coverage import (
    search_coverage_status,
    validate_search_runs,
)


def _row(**overrides):
    row = {
        "run_id": "R1",
        "source": "web_of_science",
        "query_family": "mutualist",
        "coverage_requirement": "required",
        "source_query": "TS=(phenolog* AND pollinat*)",
        "status": "planned",
        "run_date": "",
        "result_count": "",
        "export_path": "",
        "dedup_status": "pending",
        "notes": "",
    }
    row.update(overrides)
    return row


def test_planned_required_runs_keep_systematic_claim_closed():
    df = pd.DataFrame(
        [
            _row(run_id="R1"),
            _row(
                run_id="R2",
                source="openalex",
                coverage_requirement="supplementary",
            ),
        ]
    )
    assert validate_search_runs(df) == []
    out = search_coverage_status(df)
    assert out["required_runs"] == 1
    assert out["required_completed"] == 0
    assert out["systematic_claim_status"] == "targeted_only"


def test_all_required_completed_opens_systematic_claim_gate():
    df = pd.DataFrame(
        [
            _row(
                status="completed",
                run_date="2026-09-28",
                result_count=12,
                export_path="data/search/R1.csv",
                dedup_status="complete",
            )
        ]
    )
    assert validate_search_runs(df) == []
    out = search_coverage_status(df)
    assert out["systematic_claim_status"] == "systematic_ready"


def test_completed_run_requires_export_count_and_dedup():
    df = pd.DataFrame(
        [
            _row(
                status="completed",
                run_date="2026-09-28",
                result_count="",
                export_path="",
                dedup_status="pending",
            )
        ]
    )
    errors = validate_search_runs(df)
    assert any("result_count" in error for error in errors)
    assert any("export_path" in error for error in errors)
    assert any("dedup_status=complete" in error for error in errors)


def test_noncompleted_run_cannot_claim_dedup_complete():
    errors = validate_search_runs(
        pd.DataFrame([_row(dedup_status="complete")])
    )
    assert any("non-completed run" in error for error in errors)
