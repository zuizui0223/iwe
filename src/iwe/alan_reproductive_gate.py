"""Non-promoting study-programme evidence gates for ALAN × IWE × chocho.

A paper, an experimental field block, an observed plant and a published
meta-analysis are distinct replication units. Relative visits, pollen,
mature seeds and introduced-host geography cannot be pooled as one effect.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pandas as pd


PROG_COLS = {
    "study_id", "doi", "source_release", "exposure_kind", "alan_manipulated",
    "visitor_events_measured", "conspecific_pollen_deposition_measured",
    "direct_seed_or_fruit_outcome_measured", "mature_seed_counts_measured",
    "fruit_infestation_measured", "floral_schedule_measured",
    "independent_seasonal_partner_activity_measured",
    "autonomous_selfing_assessed", "complete_causal_mediation_identified",
    "island_mainland_matched", "source_field_blocks",
    "published_plant_species_in_focal_test", "source_grain",
    "dependence_group", "source_reconstruction_class",
}
CLAIM_COLS = {
    "study_id", "endpoint", "plant_or_guild", "observed_effect_label",
    "numeric_value", "numeric_unit", "verified_source_scope",
    "never_interpret_as",
}
BOOL_COLS = (
    "alan_manipulated", "visitor_events_measured",
    "conspecific_pollen_deposition_measured",
    "direct_seed_or_fruit_outcome_measured",
    "mature_seed_counts_measured", "fruit_infestation_measured",
    "floral_schedule_measured",
    "independent_seasonal_partner_activity_measured",
    "autonomous_selfing_assessed", "complete_causal_mediation_identified",
    "island_mainland_matched",
)
ORIGINAL_STUDY_DOIS = {
    "KNOP2017_SWISS": "10.1038/nature23288",
    "GIAVI2021_SWISS": "10.1038/s41467-021-22011-8",
    "BOOM2020_NETHERLANDS": "10.1038/s41598-020-75471-1",
    "LU_NETWORK2026_TIBET": "10.1002/ece3.74368",
    "LU_REPRO2026_TIBET": "10.1093/jpe/rtag160",
    "LI2026_UK": "10.64898/2026.07.10.737511",
    "GROGNUZ2026_SWISS": "10.13140/RG.2.2.36822.10563",
    "SWISS_PHENO2026": "10.1016/j.biocon.2025.111650",
    "KENDALL2025_DIEL_META": "10.1111/ele.70036",
}
CLAIM_VALUES = {
    ("KNOP2017_SWISS", "nocturnal_visit_count"): -62.0,
    ("KNOP2017_SWISS", "fruit_set"): -13.0,
    ("LU_REPRO2026_TIBET", "night_Lepidoptera_visitation"): -49.1,
    ("LU_REPRO2026_TIBET", "nocturnal_conspecific_pollen_receipt"): -53.8,
    ("LU_REPRO2026_TIBET", "seed_set"): -56.0,
    ("LU_REPRO2026_TIBET", "autonomous_selfing_seed_contribution"): 65.0,
    ("LU_REPRO2026_TIBET", "nocturnal_pollination_seed_contribution"): 35.71,
    ("LI2026_UK", "seed_presence_linear_array"): 20.0,
    ("LI2026_UK", "seed_presence_control"): 8.0,
    ("BOOM2020_NETHERLANDS", "estimated_seeds_per_flower"): None,
    ("BOOM2020_NETHERLANDS", "estimated_seed_mean_ANOVA"): 0.63,
    ("KENDALL2025_DIEL_META", "night_bloom_minus_day_bloom_night_reproductive_share"): 21.475,
    ("KENDALL2025_DIEL_META", "night_bloom_x_prior_PCNLeffect"): 1.738,
}


def _require(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{label}: required columns missing: {missing}")


def _text(value: Any) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _bool(column: pd.Series, name: str) -> pd.Series:
    values = column.map(_text).str.lower()
    if not values.isin(("yes", "no")).all():
        raise ValueError(f"{name}: must explicitly be yes or no, no unknown imputation")
    return values.eq("yes")


def build_crossstudy_readiness(
    programmes: pd.DataFrame, claims: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Check source identities and display scientifically separate endpoints."""
    _require(programmes, PROG_COLS, "ALAN programme ledger")
    _require(claims, CLAIM_COLS, "ALAN source claim ledger")
    p = programmes.copy()
    c = claims.copy()
    for col in PROG_COLS - set(BOOL_COLS):
        p[col] = p[col].map(_text)
    for col in CLAIM_COLS - {"numeric_value"}:
        c[col] = c[col].map(_text)
    if len(p) != len(ORIGINAL_STUDY_DOIS) or p["study_id"].duplicated().any():
        raise ValueError("ALAN programme ledger expected nine unique source rows")
    if set(p["study_id"]) != set(ORIGINAL_STUDY_DOIS):
        raise ValueError("ALAN programme ID/source roster drift")
    for ident, doi in ORIGINAL_STUDY_DOIS.items():
        row = p.loc[p["study_id"] == ident].iloc[0]
        if row["doi"] != doi:
            raise ValueError(f"ALAN source DOI drift: {ident}")
        if not row["dependence_group"] or not row["source_grain"]:
            raise ValueError(f"Missing dependence/site grain: {ident}")
    if p.loc[p["study_id"].str.startswith("LU_"), "dependence_group"].nunique() != 1:
        raise ValueError("Lu author/programme dependence unresolved: do not count as 2 independent trials")
    if p.loc[p["study_id"] == "KENDALL2025_DIEL_META", "exposure_kind"].iloc[0] != (
        "observational_prioryear_PCNLand_pollinator_exclusion"
    ):
        raise ValueError("Kendall preceding satellite light is not an ALAN intervention")
    if p.loc[p["study_id"] == "KENDALL2025_DIEL_META", "alan_manipulated"].iloc[0].lower() != "no":
        raise ValueError("Kendall diel pollination exclusions are not an ALAN intervention")
    for col in BOOL_COLS:
        p[col] = _bool(p[col], col)
    if p.loc[p["study_id"] == "KENDALL2025_DIEL_META", "floral_schedule_measured"].any():
        raise ValueError("Source botanical bloom class is not same-site flowering phenophase")
    if not p.loc[
        p["study_id"] == "SWISS_PHENO2026", "floral_schedule_measured"
    ].all():
        raise ValueError("Swiss real floral phenophase source coverage lost")
    if not p.loc[p["study_id"] == "LU_REPRO2026_TIBET",
                 ["visitor_events_measured", "conspecific_pollen_deposition_measured",
                  "direct_seed_or_fruit_outcome_measured"]].all(axis=None):
        raise ValueError("Lu source published visit/pollen/seed chain must all be retained")
    if not p.loc[p["study_id"] == "BOOM2020_NETHERLANDS",
                 "fruit_infestation_measured"].all():
        raise ValueError("Boom original documented infestation missing")
    if p.loc[p["study_id"] == "BOOM2020_NETHERLANDS", "mature_seed_counts_measured"].any():
        raise ValueError("Boom rounded model-derived seed per flower is NOT raw counted mature seeds")
    if p.loc[p["study_id"] == "LI2026_UK", "visitor_events_measured"].any():
        raise ValueError("Li original author seedset.csv did not observe insect visitors")
    if p.loc[p["study_id"] == "LI2026_UK", "conspecific_pollen_deposition_measured"].any():
        raise ValueError("Li pollinated=Seeds>0 is not actually counted pollen deposition")
    if p["complete_causal_mediation_identified"].any():
        raise ValueError("No publication identifies full ALAN->same-flower pollen->seed mediation")
    if p["island_mainland_matched"].any():
        raise ValueError("No direct island/mainland light manipulation with true pollen rescue is in scope")

    c["numeric_value"] = pd.to_numeric(c["numeric_value"], errors="coerce")
    if c["numeric_value"].isna().any() or not c["numeric_value"].map(math.isfinite).all():
        raise ValueError("Claim values must be explicitly numeric and finite")
    if not set(c["study_id"]) <= set(ORIGINAL_STUDY_DOIS):
        raise ValueError("Claim references unknown source study")
    if c.duplicated(["study_id", "endpoint", "observed_effect_label"]).any():
        raise ValueError("Duplicate source endpoint in exact study")
    if len(c) != 14:
        raise ValueError("Reported effect ledger row count drift")

    # All source named effects except the two original Boom treatment
    # means have one unique source key; both means use distinct labels.
    for (study, endpoint), value in CLAIM_VALUES.items():
        rows = c[(c["study_id"] == study) & (c["endpoint"] == endpoint)]
        needed = 2 if value is None else 1
        if len(rows) != needed:
            raise ValueError(f"Missing source endpoint or duplicate: {study}, {endpoint}")
        if value is not None and float(rows.iloc[0]["numeric_value"]) != value:
            raise ValueError(f"Reported endpoint numeric drift: {study}, {endpoint}")
    seeds = c[(c["study_id"] == "BOOM2020_NETHERLANDS") &
              (c["endpoint"] == "estimated_seeds_per_flower")]
    if dict(zip(seeds["observed_effect_label"], seeds["numeric_value"])) != {
        "dark_source_rounded_treatment_mean": 117.0,
        "green_source_rounded_treatment_mean": 61.0,
    }:
        raise ValueError("Boom original rounded reproductive means changed")
    if c.loc[
        c["study_id"] == "KENDALL2025_DIEL_META", "verified_source_scope"
    ].eq("original_author_publication_direct").any():
        raise ValueError("ALAN fitted PCNL reanalysis coefficient is not Kendall paper's original result")

    p["direct_light_manipulation"] = p["alan_manipulated"]
    p["observed_visit_pollen_reproduction_chain_in_one_paper"] = (
        p["alan_manipulated"] & p["visitor_events_measured"] &
        p["conspecific_pollen_deposition_measured"] &
        p["direct_seed_or_fruit_outcome_measured"]
    )
    p["complete_day_year_stage_x_partner_x_seed_chain"] = (
        p["observed_visit_pollen_reproduction_chain_in_one_paper"] &
        p["floral_schedule_measured"] &
        p["independent_seasonal_partner_activity_measured"]
    )
    p["light_x_nursery_seedpredation_pollen_viable_seed_chain"] = (
        p["alan_manipulated"] &
        p["conspecific_pollen_deposition_measured"] &
        p["fruit_infestation_measured"] &
        p["mature_seed_counts_measured"]
    )
    p["cross_repo_chocho_locality_year_effect_estimable"] = False
    p["strict_iwe_h1_effects_created"] = 0
    report = {
        "schema": "iwe_chocho_alan_functional_outcome_gate_v0.1",
        "n_source_rows_including_secondary_literature_synthesis": int(len(p)),
        "n_original_ALAN_manipulation_paper_rows": int(p["alan_manipulated"].sum()),
        "n_original_papers_with_reported_visit_pollen_reproduction": int(
            p["observed_visit_pollen_reproduction_chain_in_one_paper"].sum()
        ),
        "those_papers": p.loc[
            p["observed_visit_pollen_reproduction_chain_in_one_paper"],
            "study_id",
        ].tolist(),
        "n_complete_independent_seasonal_or_diel_phenophase_fitness_chains": int(
            p["complete_day_year_stage_x_partner_x_seed_chain"].sum()
        ),
        "n_complete_light_nursery_pollen_seedpredation_viableseed_chains": int(
            p["light_x_nursery_seedpredation_pollen_viable_seed_chain"].sum()
        ),
        "n_true_island_mainland_light_pollen_partner_reproduction_comparisons": int(
            p["island_mainland_matched"].sum()
        ),
        "lu_papers_independence_status": "potential_same_research_programme_not_resolved",
        "original_studies_within_Kendall_meta_cannot_be_added_to_paper_count": True,
        "cross_source_visits_pollen_seeds_must_not_be_multiplied": True,
        "biological_effect_signs_are_heterogeneous_but_estimands_differ": True,
        "source_reported_night_bloom_reproduction_association_not_same_as_light_causation": True,
        "light_specific_reproductive_meta_effect": None,
        "seasonal_synchrony_effect": None,
        "new_strict_iwe_h1_effects": 0,
        "original_chocho_paper_modified": False,
        "claim_ceiling": (
            "Source-audited ALAN effects concern distinct measured endpoints. "
            "A Lu paper co-reports visits, pollen and reproduction; only "
            "Li provides original author raw plant seed counts here. "
            "No global common-unit light×time×functional substitution effect."
        ),
    }
    return p, c, report
