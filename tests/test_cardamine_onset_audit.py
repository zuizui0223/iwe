"""Original-onset partial identification must not silently use visit cadence."""
import pandas as pd
import pytest

from iwe.cardamine_onset_audit import audit_cardamine_onset_intervals


def _plants():
    return pd.DataFrame([
        {"year": 2012, "ecotype": "late", "plant_id": "E", "doy": 100, "flowers": 2, "final_ru": 99},
        {"year": 2012, "ecotype": "late", "plant_id": "B", "doy": 112, "flowers": 1, "final_ru": 99},
        {"year": 2012, "ecotype": "late", "plant_id": "C", "doy": 119, "flowers": 3, "final_ru": 99},
        {"year": 2012, "ecotype": "late", "plant_id": "L", "doy": 135, "flowers": 2, "final_ru": 99},
    ])


def _adults():
    return pd.DataFrame({
        "year": [2012] * 11,
        "event_doy": [100, 110, 112, 114, 116, 118, 120, 122, 125, 130, 150],
    })


def test_source_left_censor_cannot_certify_late_or_core():
    out = audit_cardamine_onset_intervals(_plants(), _adults()).set_index("plant_id")
    assert out.loc["E", "source_identified_group"] == "early_refugium"
    assert out.loc["B", "source_identified_group"] == "unresolved_left_censored"
    assert out.loc["C", "source_identified_group"] == "unresolved_left_censored"
    assert out.loc["L", "source_identified_group"] == "unresolved_left_censored"
    assert out.loc["B", "scenario_stable_group"] == "boundary_sensitive"
    assert out.loc["C", "scenario_stable_group"] == "core_flight"
    assert out.loc["L", "scenario_stable_group"] == "boundary_sensitive"
    assert not out["strict_h1_admission_from_this_audit"].any()
    assert not out["scenario_is_source_verified"].any()


def test_source_original_bounds_separate_certified_from_boundary_sensitive():
    bounds = pd.DataFrame([
        {"year": 2012, "ecotype": "late", "plant_id": "B",
         "earliest_possible_doy": 108, "source_locator": "verified original marked visit row B"},
        {"year": 2012, "ecotype": "late", "plant_id": "C",
         "earliest_possible_doy": 116, "source_locator": "verified original marked visit row C"},
        {"year": 2012, "ecotype": "late", "plant_id": "L",
         "earliest_possible_doy": 141, "source_locator": "verified original marked visit row L"},
    ])
    # Original bounds cannot start after first observed flowering.
    with pytest.raises(ValueError, match="exceeds"):
        audit_cardamine_onset_intervals(_plants(), _adults(), bounds)
    bounds.loc[bounds["plant_id"].eq("L"), "earliest_possible_doy"] = 132
    out = audit_cardamine_onset_intervals(_plants(), _adults(), bounds).set_index("plant_id")
    assert out.loc["B", "source_identified_group"] == "boundary_sensitive"
    assert out.loc["C", "source_identified_group"] == "core_flight"
    assert out.loc["L", "source_identified_group"] == "late_refugium"
    assert out.loc["E", "source_identified_group"] == "early_refugium"


def test_source_lower_bounds_require_keys_and_original_locator():
    b = pd.DataFrame([{"year": 2012, "ecotype": "late", "plant_id": "C",
                       "earliest_possible_doy": 112, "source_locator": ""}])
    with pytest.raises(ValueError, match="locator"):
        audit_cardamine_onset_intervals(_plants(), _adults(), b)
    b["source_locator"] = "Appendix original event row C"
    with pytest.raises(ValueError, match="duplicate"):
        audit_cardamine_onset_intervals(_plants(), _adults(), pd.concat([b, b]))
    b["plant_id"] = "unlisted"
    with pytest.raises(ValueError, match="unknown plant"):
        audit_cardamine_onset_intervals(_plants(), _adults(), b)


def test_outcome_blind_and_lag_scenario_is_not_source_provenance():
    p = _plants()
    a = audit_cardamine_onset_intervals(p, _adults())
    p["final_ru"] = 0
    p["larvae"] = [0, 10, 20, 30]
    b = audit_cardamine_onset_intervals(p, _adults())
    pd.testing.assert_frame_equal(a, b)
    assert set(b["scenario_max_detection_lag_days"]) == {7}
    assert set(b["source_bound_is_originally_verified"]) == {False}
    with pytest.raises(ValueError, match="integer 0..366"):
        audit_cardamine_onset_intervals(p, _adults(), scenario_max_detection_lag_days=-1)
