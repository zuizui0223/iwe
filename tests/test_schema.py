from iwe.schema import INTERACTION_TYPES, EVIDENCE_TIERS, EFFECT_FAMILIES


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
