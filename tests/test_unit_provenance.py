import pandas as pd

from iwe.unit_provenance import validate_strict_unit_provenance


COLUMNS = [
    "effect_id",
    "study_id",
    "design_type",
    "exposure_grain",
    "response_grain",
    "variance_interpretation",
    "inference_scope",
    "causal_claim_allowed",
    "notes",
]


def _effect(effect_id="E1", study_id="S1", timing="strict_window"):
    return {
        "effect_id": effect_id,
        "study_id": study_id,
        "evidence_tier": "A",
        "timing_analysis_class": timing,
        "source_id": "10.example/source",
    }


def _unit(**overrides):
    row = {
        "effect_id": "E1",
        "study_id": "S1",
        "design_type": "fixed_context_group_comparison",
        "exposure_grain": "plot",
        "response_grain": "plant",
        "variance_interpretation": "within_context_response_sampling",
        "inference_scope": "descriptive_association",
        "causal_claim_allowed": "no",
        "notes": "",
    }
    row.update(overrides)
    return row


def test_fixed_context_response_sampling_is_allowed_but_noncausal():
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([_unit()]),
    )
    assert errors == []


def test_nested_response_sampling_cannot_be_labeled_causal():
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([_unit(causal_claim_allowed="yes")]),
    )
    assert any("cannot authorize a causal claim" in error for error in errors)


def test_nested_response_sampling_must_use_fixed_context_variance_semantics():
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([_unit(variance_interpretation="individual_effect_sampling")]),
    )
    assert any("within_context_response_sampling" in error for error in errors)


def test_experimental_individual_timing_requires_aligned_units():
    unit = _unit(
        design_type="experimental_individual_timing",
        exposure_grain="plant",
        response_grain="plant",
        variance_interpretation="individual_effect_sampling",
        inference_scope="experimental_manipulation",
        causal_claim_allowed="yes",
    )
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame([unit]),
    )
    assert errors == []


def test_current_strict_effect_requires_unit_provenance():
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect()]),
        pd.DataFrame(columns=COLUMNS),
    )
    assert any("lacks unit provenance" in error for error in errors)


def test_non_strict_effect_does_not_require_unit_provenance():
    errors = validate_strict_unit_provenance(
        pd.DataFrame([_effect(timing="direct_timing_sensitivity")]),
        pd.DataFrame(columns=COLUMNS),
    )
    assert errors == []
