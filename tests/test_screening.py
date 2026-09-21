import pandas as pd
import pytest

from iwe.screening import (
    render_screening_snapshot,
    replace_screening_snapshot,
    screening_count_table,
    validate_study_registry,
)


def _registry():
    return pd.DataFrame(
        [
            {
                "study_id": "IWE001",
                "source_id": "doi:1",
                "title": "Mutualist include",
                "system_id": "SYS1",
                "screening_status": "include",
                "screening_reason": "reason",
                "interaction_type_candidate": "mutualist",
                "notes": "",
            },
            {
                "study_id": "IWE002",
                "source_id": "doi:2",
                "title": "Mutualist unresolved",
                "system_id": "SYS1",
                "screening_status": "unresolved",
                "screening_reason": "reason",
                "interaction_type_candidate": "mutualist",
                "notes": "",
            },
            {
                "study_id": "IWE003",
                "source_id": "doi:3",
                "title": "Antagonist context",
                "system_id": "SYS2",
                "screening_status": "context_only",
                "screening_reason": "reason",
                "interaction_type_candidate": "antagonist",
                "notes": "",
            },
            {
                "study_id": "IWE004",
                "source_id": "doi:4",
                "title": "Mixed include",
                "system_id": "SYS3",
                "screening_status": "include",
                "screening_reason": "reason",
                "interaction_type_candidate": "mixed_pollinating_seed_predator",
                "notes": "",
            },
        ]
    )


def test_screening_counts_are_derived_from_registry():
    counts = screening_count_table(_registry())
    total = counts.loc[counts["candidate_class"] == "Total"].iloc[0]
    assert total["include"] == 2
    assert total["unresolved"] == 1
    assert total["context_only"] == 1
    assert total["exclude"] == 0
    assert total["total"] == 4


def test_rendered_snapshot_contains_every_registry_row():
    snapshot = render_screening_snapshot(_registry())
    assert "**Registered publications: 4.**" in snapshot
    for study_id in ["IWE001", "IWE002", "IWE003", "IWE004"]:
        assert f"`{study_id}`" in snapshot


def test_replacement_requires_generated_markers():
    with pytest.raises(ValueError, match="missing generated snapshot markers"):
        replace_screening_snapshot("# no markers", render_screening_snapshot(_registry()))


def test_unknown_screening_status_fails_registry_validation():
    df = _registry()
    df.loc[0, "screening_status"] = "maybe"
    errors = validate_study_registry(df)
    assert any("unknown screening_status" in error for error in errors)
