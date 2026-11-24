import pandas as pd

from iwe.propagation_screening import (
    propagation_screening_summary,
    validate_propagation_screening,
)


def _screen() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "study_id": "IWE001",
                "interaction_type": "mutualist",
                "screening_state": "registered",
                "reason_code": "registered_propagation",
                "priority": "REGISTERED",
                "candidate_chain": "timing -> final",
                "notes": "registered",
            },
            {
                "study_id": "IWE002",
                "interaction_type": "mutualist",
                "screening_state": "candidate",
                "reason_code": "needs_source_audit",
                "priority": "P1",
                "candidate_chain": "timing -> final",
                "notes": "candidate",
            },
            {
                "study_id": "IWE009",
                "interaction_type": "mutualist",
                "screening_state": "ineligible",
                "reason_code": "no_final_fitness",
                "priority": "DROP",
                "candidate_chain": "timing",
                "notes": "no final",
            },
        ]
    )


def test_propagation_screening_accepts_valid_rows():
    assert validate_propagation_screening(_screen()) == []


def test_screening_summary_tracks_candidates_separately():
    summary = propagation_screening_summary(_screen())
    assert summary["n_studies"] == 3
    assert summary["by_state"] == {
        "registered": 1,
        "candidate": 1,
        "ineligible": 1,
    }
    assert summary["p1_candidates"] == ["IWE002"]


def test_ineligible_rows_must_be_drop_priority():
    df = _screen()
    df.loc[df["study_id"].eq("IWE009"), "priority"] = "P1"
    errors = validate_propagation_screening(df)
    assert any("ineligible rows must use DROP" in error for error in errors)


def test_full_screen_matches_study_registry_exactly():
    screen = pd.read_csv("data/registry/temporal_propagation_screening.csv")
    studies = pd.read_csv("data/registry/studies.csv")
    assert validate_propagation_screening(screen, studies) == []
    assert len(screen) == len(studies) == 32
    assert set(screen["study_id"]) == set(studies["study_id"])
