INTERACTION_TYPES = {
    "mutualist",
    "antagonist",
    "mixed_pollinating_seed_predator",
}

EVIDENCE_TIERS = {"A", "B", "C"}

PHENOLOGY_SOURCES = {
    "direct_interaction",
    "direct_activity",
    "experimental_timing",
    "occurrence_proxy",
}

EXPOSURE_DIRECTIONS = {"synchrony", "mismatch"}

TIMING_METRIC_TYPES = {
    "overlap_index",
    "absolute_mismatch",
    "plant_minus_partner",
    "partner_minus_plant",
    "experimental_plant_shift",
    "seasonal_position",
    "other_registered",
}

TIMING_ANALYSIS_CLASSES = {
    "strict_window",
    "direct_timing_sensitivity",
    "directional_mismatch",
    "unresolved_for_strict_h1",
    "proxy_only",
}

TIMING_DOMAINS = {
    "nonnegative",
    "plant_earlier_only",
    "partner_earlier_only",
    "both_sides",
    "ordered_by_measured_window",
    "unknown",
    "not_applicable",
}

EFFECT_FAMILIES = {
    "standardized_slope",
    "fisher_z",
    "standardized_mean_difference",
    "log_response_ratio",
}

REQUIRED_EFFECT_COLUMNS = [
    "effect_id",
    "study_id",
    "dataset_id",
    "dependence_id",
    "plant_taxon",
    "animal_taxon",
    "interaction_type",
    "evidence_tier",
    "phenology_source",
    "timing_metric_type",
    "timing_analysis_class",
    "timing_domain",
    "exposure_direction",
    "outcome_family",
    "effect_family",
    "effect_native",
    "variance_native",
    "sample_size",
    "source_id",
]
