import pandas as pd
import pytest

from iwe.endpoint_audit import endpoint_sensitivity, validate_endpoint_audit


def _registered():
    return (
        pd.read_csv("data/registry/temporal_signal_components.csv"),
        pd.read_csv("data/registry/propagation_endpoint_audit.csv"),
    )


def test_every_propagation_link_has_an_audited_endpoint():
    propagation, endpoints = _registered()
    assert validate_endpoint_audit(propagation, endpoints) == []
    assert len(propagation) == len(endpoints) == 33


def test_endpoint_strict_sensitivity_does_not_silently_promote_proxies():
    propagation, endpoints = _registered()
    summary = endpoint_sensitivity(propagation, endpoints)
    counts = summary["endpoint_counts"]
    assert counts["observed_mature_seed_or_yield"] == 18
    assert counts["observed_postcost_reproductive_units"] == 2
    assert counts["observed_terminal_fate"] == 3
    assert counts["derived_reproductive_index"] == 5
    assert counts["source_model_predicted_final"] == 1
    assert counts["observed_seed_damage_only"] == 1
    assert counts["intermediate_only"] == 3

    rows = {(x["scope"], x["reference"]): x for x in summary["summary"]}
    strict = rows[("mature_seed_yield", "prospective_design")]
    assert (strict["links"], strict["comparable"], strict["retained"]) == (14, 14, 12)
    strict_realized = rows[("mature_seed_yield", "realized_or_seasonal")]
    assert (strict_realized["links"], strict_realized["comparable"], strict_realized["retained"]) == (4, 4, 1)
    original = rows[("original_final", "prospective_design")]
    assert (original["links"], original["retained"]) == (18, 14)
    original_realized = rows[("original_final", "realized_or_seasonal")]
    assert (original_realized["links"], original_realized["comparable"], original_realized["retained"]) == (12, 11, 3)


def test_antagonist_cluster_grain_does_not_count_repeated_links():
    propagation, endpoints = _registered()
    summary = endpoint_sensitivity(propagation, endpoints)
    d = {(x["scope"], x["reference"]): x
         for x in summary["ant_programmes"]}
    assert d[("mature_seed_yield", "prospective_design")] == {
        "scope": "mature_seed_yield",
        "reference": "prospective_design",
        "programmes": 3,
        "all": 3,
        "mixed": 0,
        "none": 0,
    }
    assert d[("mature_seed_yield", "realized_or_seasonal")] == {
        "scope": "mature_seed_yield",
        "reference": "realized_or_seasonal",
        "programmes": 1,
        "all": 0,
        "mixed": 0,
        "none": 1,
    }


def test_missing_classification_fails_closed():
    propagation, endpoints = _registered()
    endpoints = endpoints.iloc[1:].copy()
    assert any("unclassified IDs" in e
               for e in validate_endpoint_audit(propagation, endpoints))
    with pytest.raises(ValueError):
        endpoint_sensitivity(propagation, endpoints)


def test_unknown_and_duplicate_classification_fail_closed():
    propagation, endpoints = _registered()
    extra = endpoints.iloc[[0]].copy()
    extra.loc[:, "propagation_id"] = "MADE_UP"
    wrong = pd.concat([endpoints, extra], ignore_index=True)
    assert any("unknown IDs" in e
               for e in validate_endpoint_audit(propagation, wrong))
    duplicate = pd.concat([endpoints, endpoints.iloc[[0]]], ignore_index=True)
    assert any("duplicate propagation_id" in e
               for e in validate_endpoint_audit(propagation, duplicate))


def test_intermediate_cannot_be_relabelled_as_final():
    propagation, endpoints = _registered()
    bad = endpoints.copy()
    bad.loc[bad["propagation_id"].eq("SIG_KULA2012_REVERSAL"),
            "endpoint_class"] = "observed_mature_seed_or_yield"
    assert any("endpoint/final-link inconsistency" in e
               for e in validate_endpoint_audit(propagation, bad))


def test_endpoint_audit_requires_reason_and_known_class():
    propagation, endpoints = _registered()
    bad = endpoints.copy()
    bad.loc[0, "rationale"] = ""
    bad.loc[1, "endpoint_class"] = "super_fitness"
    errors = validate_endpoint_audit(propagation, bad)
    assert any("rationale" in e for e in errors)
    assert any("invalid endpoint_class" in e for e in errors)


def test_endpoint_strict_comparison_displays_class_imbalance():
    propagation, endpoints = _registered()
    summary = endpoint_sensitivity(propagation, endpoints)
    d = {(x["interaction_type"], x["reference"]): x
         for x in summary["strict_class_mix"]}
    assert d[("mutualist", "prospective_design")]["links"] == 11
    assert d[("mutualist", "prospective_design")]["retained"] == 9
    assert d[("antagonist", "prospective_design")]["links"] == 3
    assert d[("antagonist", "realized_or_seasonal")]["links"] == 1
    assert d[("mixed_pollinating_seed_predator", "prospective_design")]["links"] == 0
    assert d[("mixed_pollinating_seed_predator", "realized_or_seasonal")]["links"] == 1
