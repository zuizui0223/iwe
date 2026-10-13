import pandas as pd

from iwe.adjudication import (
    validate_adjudication_registry,
    validate_effect_adjudications,
)


def _adjudications():
    return pd.DataFrame(
        [
            {
                "adjudication_id": "A1",
                "study_id": "IWE001",
                "component": "native",
                "strict_h1_status": "ineligible",
                "quantitative_status": "native_extracted",
                "expected_effect_id": None,
                "timing_metric_type": "partner_minus_plant",
                "timing_analysis_class": "unresolved_for_strict_h1",
                "timing_domain": "both_sides",
                "effect_family": "fisher_z",
                "reason": "two sided",
            },
            {
                "adjudication_id": "A2",
                "study_id": "IWE029",
                "component": "late_vs_peak",
                "strict_h1_status": "eligible",
                "quantitative_status": "strict_extracted",
                "expected_effect_id": "E29",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "log_odds_ratio",
                "reason": "measured window",
            },
        ]
    )


def _effects():
    return pd.DataFrame(
        [
            {
                "effect_id": "E1",
                "study_id": "IWE001",
                "timing_metric_type": "partner_minus_plant",
                "timing_analysis_class": "unresolved_for_strict_h1",
                "timing_domain": "both_sides",
                "effect_family": "fisher_z",
            },
            {
                "effect_id": "E29",
                "study_id": "IWE029",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "log_odds_ratio",
            },
        ]
    )


def test_effects_match_adjudication_registry():
    assert validate_effect_adjudications(_effects(), _adjudications()) == []


def test_strict_effect_without_exact_gate_fails():
    effects = _effects()
    effects.loc[effects["effect_id"] == "E29", "effect_id"] = "OTHER"
    errors = validate_effect_adjudications(effects, _adjudications())
    assert any("lacks an eligible strict_extracted adjudication" in e for e in errors)


def test_strict_effect_field_mismatch_fails():
    effects = _effects()
    effects.loc[effects["effect_id"] == "E29", "effect_family"] = "fisher_z"
    errors = validate_effect_adjudications(effects, _adjudications())
    assert any("effect_family=fisher_z" in e for e in errors)


def test_effect_from_unadjudicated_study_fails():
    effects = _effects()
    effects.loc[len(effects)] = {
        "effect_id": "E4",
        "study_id": "IWE004",
        "timing_metric_type": "seasonal_position",
        "timing_analysis_class": "direct_timing_sensitivity",
        "timing_domain": "not_applicable",
        "effect_family": "standardized_slope",
    }
    errors = validate_effect_adjudications(effects, _adjudications())
    assert any("study IWE004 has no strict-H1 adjudication" in e for e in errors)


def test_strict_extracted_requires_eligible_status():
    adjudications = _adjudications()
    adjudications.loc[
        adjudications["adjudication_id"] == "A2", "strict_h1_status"
    ] = "ineligible"
    errors = validate_adjudication_registry(adjudications)
    assert any("strict_extracted requires strict_h1_status=eligible" in e for e in errors)


def test_iwe015_is_unresolved_until_matching_final_fruit_units_are_verified():
    registry = pd.read_csv("data/registry/strict_h1_adjudications.csv")
    sub = registry[registry["study_id"] == "IWE015"]
    assert len(sub) == 2
    assert set(sub["strict_h1_status"]) == {"unresolved"}
    assert set(sub["quantitative_status"]) == {"pending"}
    assert sub["expected_effect_id"].isna().all()
    for note in sub["reason"]:
        assert "linkage" in note
        assert "variance" in note
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.loc[
        (effects["study_id"] == "IWE015")
        & (effects["timing_analysis_class"] == "strict_window")
    ].shape[0]
    assert validate_effect_adjudications(effects, registry) == []
