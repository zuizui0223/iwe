import pandas as pd
import pytest

from iwe.propagation import propagation_summary, validate_propagation_registry


def _rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "propagation_id": "SIG_A",
                "study_id": "IWEA",
                "interaction_type": "mutualist",
                "from_stage": "partner_activity",
                "to_stage": "final_seed",
                "transformation": "preserved",
                "final_fitness_reached": "yes",
                "dependence_id": "DEP_A",
                "window_reference_class": "independent_partner_activity",
                "evidence_note": "final link",
            },
            {
                "propagation_id": "SIG_B",
                "study_id": "IWEB",
                "interaction_type": "antagonist",
                "from_stage": "oviposition",
                "to_stage": "larval_load",
                "transformation": "erased",
                "final_fitness_reached": "no",
                "dependence_id": "DEP_B",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "signal disappears before final fitness",
            },
        ]
    )


def test_propagation_registry_accepts_valid_links():
    assert validate_propagation_registry(_rows()) == []


def test_invalid_transformation_fails():
    df = _rows()
    df.loc[0, "transformation"] = "magic"
    errors = validate_propagation_registry(df)
    assert any("transformation: invalid values" in error for error in errors)


def test_summary_counts_dependence_and_final_studies():
    df = pd.concat(
        [
            _rows(),
            _rows().iloc[[0]].assign(
                propagation_id="SIG_A2",
                from_stage="raw_exposure",
                to_stage="effective_exposure",
                transformation="shifted_filtered",
            ),
        ],
        ignore_index=True,
    )
    summary = propagation_summary(df)
    assert summary["n_links"] == 3
    assert summary["n_studies"] == 2
    assert summary["n_dependence_clusters"] == 2
    assert summary["final_links"] == 2
    assert summary["final_studies"] == 1
    assert summary["final_transformations_by_class"]["mutualist"]["preserved"] == 1
    assert summary["final_transformations_by_class"]["mutualist"]["shifted_filtered"] == 1


def test_duplicate_propagation_id_fails():
    df = pd.concat([_rows(), _rows().iloc[[0]]], ignore_index=True)
    errors = validate_propagation_registry(df)
    assert any("duplicate propagation_id" in error for error in errors)


def test_summary_rejects_invalid_registry():
    df = _rows()
    df.loc[0, "final_fitness_reached"] = "maybe"
    with pytest.raises(ValueError):
        propagation_summary(df)
