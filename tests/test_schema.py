from iwe.schema import (
    EFFECT_FAMILIES,
    EVIDENCE_TIERS,
    INTERACTION_TYPES,
    TIMING_ANALYSIS_CLASSES,
    TIMING_DOMAINS,
    TIMING_METRIC_TYPES,
)


def test_registered_interaction_types_are_frozen():
    assert INTERACTION_TYPES == {
        "mutualist",
        "antagonist",
        "mixed_pollinating_seed_predator",
    }


def test_registered_evidence_tiers_are_frozen():
    assert EVIDENCE_TIERS == {"A", "B", "C"}


def test_registered_effect_families_are_explicit():
    assert EFFECT_FAMILIES == {
        "standardized_slope",
        "fisher_z",
        "standardized_mean_difference",
        "log_response_ratio",
    }


def test_registered_timing_metric_types_match_contract():
    assert TIMING_METRIC_TYPES == {
        "overlap_index",
        "absolute_mismatch",
        "plant_minus_partner",
        "partner_minus_plant",
        "experimental_plant_shift",
        "seasonal_position",
        "other_registered",
    }


def test_registered_timing_analysis_classes_are_explicit():
    assert TIMING_ANALYSIS_CLASSES == {
        "strict_window",
        "direct_timing_sensitivity",
        "directional_mismatch",
        "unresolved_for_strict_h1",
        "proxy_only",
    }


def test_registered_timing_domains_are_explicit():
    assert TIMING_DOMAINS == {
        "nonnegative",
        "plant_earlier_only",
        "partner_earlier_only",
        "both_sides",
        "ordered_by_measured_window",
        "unknown",
        "not_applicable",
    }
