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
    "exposure_direction",
    "outcome_family",
    "effect_family",
    "effect_native",
    "variance_native",
    "sample_size",
    "source_id",
]
