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
                "direction_comparable": "yes",
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
                "direction_comparable": "yes",
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


def test_summary_separates_final_transformations_by_reference_provenance():
    df = pd.DataFrame(
        [
            {
                "propagation_id": "P1",
                "study_id": "S1",
                "interaction_type": "mutualist",
                "from_stage": "adult_service",
                "to_stage": "final_seed",
                "transformation": "preserved",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "D1",
                "window_reference_class": "independent_partner_activity",
                "evidence_note": "prospective",
            },
            {
                "propagation_id": "P2",
                "study_id": "S2",
                "interaction_type": "antagonist",
                "from_stage": "timed_damage",
                "to_stage": "final_seed",
                "transformation": "erased",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "D2",
                "window_reference_class": "direct_interaction_manipulation",
                "evidence_note": "prospective null",
            },
            {
                "propagation_id": "P3",
                "study_id": "S3",
                "interaction_type": "mixed_pollinating_seed_predator",
                "from_stage": "calendar",
                "to_stage": "final_seed",
                "transformation": "preserved_net_changed_mechanism",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "D3",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "realized reference",
            },
            {
                "propagation_id": "P4",
                "study_id": "S4",
                "interaction_type": "antagonist",
                "from_stage": "season",
                "to_stage": "final_seed",
                "transformation": "buffered",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "D4",
                "window_reference_class": "seasonal_position_only",
                "evidence_note": "seasonal reference",
            },
        ]
    )
    summary = propagation_summary(df)
    assert summary["prospective_final_links"] == 2
    assert summary["prospective_exact_preserved"] == 1
    assert summary["prospective_direction_comparable_links"] == 2
    assert summary["prospective_direction_retaining"] == 1
    assert summary["realized_or_seasonal_final_links"] == 2
    assert summary["realized_or_seasonal_exact_preserved"] == 0
    assert summary["realized_or_seasonal_direction_comparable_links"] == 2
    assert summary["realized_or_seasonal_direction_retaining"] == 1
    assert (
        summary["final_transformations_by_reference"]["independent_partner_activity"]["preserved"]
        == 1
    )


def test_antagonist_programme_sensitivity_collapses_duplicate_links():
    df = pd.DataFrame(
        [
            {
                "propagation_id": "AP1",
                "study_id": "A1",
                "interaction_type": "antagonist",
                "from_stage": "adult",
                "to_stage": "final",
                "transformation": "preserved",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "DP1",
                "window_reference_class": "independent_partner_activity",
                "evidence_note": "prospective retained",
            },
            {
                "propagation_id": "AP2",
                "study_id": "A2",
                "interaction_type": "antagonist",
                "from_stage": "timed",
                "to_stage": "final",
                "transformation": "erased",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "DP2",
                "window_reference_class": "direct_interaction_manipulation",
                "evidence_note": "prospective null",
            },
            {
                "propagation_id": "AR1",
                "study_id": "A3",
                "interaction_type": "antagonist",
                "from_stage": "egg",
                "to_stage": "effective",
                "transformation": "shifted_filtered",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "DR1",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "same programme first link",
            },
            {
                "propagation_id": "AR2",
                "study_id": "A3",
                "interaction_type": "antagonist",
                "from_stage": "phase",
                "to_stage": "final",
                "transformation": "preserved",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "DR1",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "same programme second link",
            },
            {
                "propagation_id": "AR3",
                "study_id": "A4",
                "interaction_type": "antagonist",
                "from_stage": "season",
                "to_stage": "final",
                "transformation": "buffered",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "DR2",
                "window_reference_class": "seasonal_position_only",
                "evidence_note": "realized none retained",
            },
        ]
    )
    summary = propagation_summary(df)
    assert summary["final_programmes"] == 4
    assert summary["antagonist_programmes"] == 4
    assert summary["antagonist_retention_by_provenance"]["prospective"] == {
        "n": 2,
        "all_retained": 1,
        "mixed": 0,
        "none_retained": 1,
    }
    assert summary["antagonist_retention_by_provenance"]["realized_or_seasonal"] == {
        "n": 2,
        "all_retained": 0,
        "mixed": 1,
        "none_retained": 1,
    }


def test_iwe023_is_frozen_as_buffered_not_preserved():
    registry = pd.read_csv("data/registry/temporal_signal_components.csv")
    row = registry.loc[registry["propagation_id"].eq("SIG_IWE023_SERVICE_FINAL")]
    assert len(row) == 1
    assert row.iloc[0]["transformation"] == "buffered"
    note = str(row.iloc[0]["evidence_note"]).lower()
    assert "fivefold" in note or "5-fold" in note
    assert "buffer" in note


def test_direction_incomparable_link_is_not_counted_as_directional_failure():
    df = pd.DataFrame(
        [
            {
                "propagation_id": "C1",
                "study_id": "S1",
                "interaction_type": "antagonist",
                "from_stage": "raw_egg_window",
                "to_stage": "active_egg_window",
                "transformation": "shifted_filtered",
                "final_fitness_reached": "yes",
                "direction_comparable": "no",
                "dependence_id": "D1",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "window center/width changes; sign is not a comparable quantity",
            },
            {
                "propagation_id": "C2",
                "study_id": "S1",
                "interaction_type": "antagonist",
                "from_stage": "phase_margin",
                "to_stage": "final_fate",
                "transformation": "preserved",
                "final_fitness_reached": "yes",
                "direction_comparable": "yes",
                "dependence_id": "D1",
                "window_reference_class": "realized_interaction_window",
                "evidence_note": "comparable direction",
            },
        ]
    )
    summary = propagation_summary(df)
    assert summary["realized_or_seasonal_final_links"] == 2
    assert summary["realized_or_seasonal_direction_comparable_links"] == 1
    assert summary["realized_or_seasonal_direction_retaining"] == 1
    assert summary["antagonist_retention_by_provenance"]["realized_or_seasonal"] == {
        "n": 1,
        "all_retained": 1,
        "mixed": 0,
        "none_retained": 0,
    }
