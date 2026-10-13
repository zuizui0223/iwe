import pandas as pd
import pytest

from iwe.selection_shift import (
    selection_shift_summary,
    validate_selection_shift_registry,
)


def _rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "shift_id": "A",
                "study_key": "STUDY_A",
                "source_id": "doi:a",
                "plant_taxon": "Plant a",
                "agent_class": "antagonist",
                "agent": "Predator",
                "design_type": "population_context",
                "trait_native": "earliness",
                "canonical_axis": "earlier_flowering",
                "effect_definition": "present_minus_absent",
                "estimate_native": -0.4,
                "native_positive_meaning": "earlier_flowering",
                "orientation_multiplier": 1,
                "estimate_canonical": -0.4,
                "se_canonical": None,
                "uncertainty_status": "source_interaction_test_no_delta_se",
                "formal_test": "p<0.001",
                "direction_result": "shift_to_later",
                "dependence_id": "DEP_A",
                "provenance": "source",
                "notes": "test",
            },
            {
                "shift_id": "B",
                "study_key": "STUDY_B",
                "source_id": "doi:b",
                "plant_taxon": "Plant b",
                "agent_class": "mutualist",
                "agent": "Pollinator",
                "design_type": "factorial_manipulation",
                "trait_native": "DOY",
                "canonical_axis": "earlier_flowering",
                "effect_definition": "open_minus_supplemented",
                "estimate_native": 0.16,
                "native_positive_meaning": "later_flowering",
                "orientation_multiplier": -1,
                "estimate_canonical": -0.16,
                "se_canonical": 0.05,
                "uncertainty_status": "effect_size_ready_independent_groups",
                "formal_test": "contrast",
                "direction_result": "shift_to_later",
                "dependence_id": "DEP_B",
                "provenance": "table",
                "notes": "test",
            },
        ]
    )


def test_selection_shift_registry_accepts_mixed_uncertainty_states():
    assert validate_selection_shift_registry(_rows()) == []


def test_orientation_is_machine_checked():
    df = _rows()
    df.loc[1, "estimate_canonical"] = 0.16
    errors = validate_selection_shift_registry(df)
    assert any("canonical estimate" in error for error in errors)


def test_non_ready_row_cannot_invent_delta_se():
    df = _rows()
    df.loc[0, "se_canonical"] = 0.1
    errors = validate_selection_shift_registry(df)
    assert any("must not invent a delta SE" in error for error in errors)


def test_summary_counts_clusters_not_rows():
    summary = selection_shift_summary(_rows())
    assert summary["n_rows"] == 2
    assert summary["n_clusters"] == 2
    assert summary["effect_ready_rows"] == 1
    assert summary["effect_ready_clusters"] == 1


def test_invalid_agent_class_fails():
    df = _rows()
    df.loc[0, "agent_class"] = "enemy"
    with pytest.raises(ValueError):
        selection_shift_summary(df)
