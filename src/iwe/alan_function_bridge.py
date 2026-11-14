"""A source-pinned, non-promoting ALAN × IWE × chocho functional bridge.

Different plant–animal systems and non-equivalent endpoints remain separate.
Diel visitation ≠ seasonal phenological synchrony ≠ effective pollination;
ALAN satellite radiance ≠ experimental local lux/spectrum; potential larval
host resource geography ≠ realized butterfly occupancy or seed production.
"""
from __future__ import annotations

import math
from typing import Any
import pandas as pd


LU_ID = "LU2026_TIBET"
BOOM_ID = "BOOM2020_NL"
IWE_MIXED_ID = "MIX002_BIERE_HONDERS_1996"
LU_COMMIT = "7c065318e9476ea92541df1d89c36c54edb8d268"
BOOM_COMMIT = "7a249f22286d60e2dcf2f5979c35f4e80220bd4c"
LU_RAW_SHA = "ba7e15e66986f64943a38fd294e49d7128cf7719d318578f6b805d29cde8f98f"
BOOM_JATS_SHA = "182dafe1e99fef5453ecf0d1d1401361fe949fd8d8617ae040588fd19795154f"

LU_COLS = {
    "study_id", "source_sheet", "diel_period", "metric", "guild",
    "dark_visits", "lit_visits", "independent_blocks", "study_doi",
    "alan_source_commit", "original_workbook_sha256",
}
BOOM_COLS = {
    "study_id", "light_spectrum", "plant", "insect", "fruit_set_fraction",
    "fruit_infestation_fraction", "uninfested_ovule_fertilized_fraction",
    "reported_estimated_seeds_per_flower", "mean_ovules_per_fruit",
    "reported_seed_mean_anova_p", "field_sites", "study_doi",
    "alan_source_commit", "source_jats_sha256",
}
IWE_COLS = {
    "candidate_id", "plant_taxon", "animal_taxon", "target_class",
    "status", "timing_window_measured",
}
LIGHT_COLOURS = ("dark", "white", "green", "red")


def _require(df: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ValueError(f"{name}: missing {missing}")


def _nonnegative_int(values: pd.Series, label: str) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    if numeric.isna().any() or (numeric < 0).any() or (numeric % 1 != 0).any():
        raise ValueError(f"{label}: expected nonnegative integer counts")
    return numeric.astype("int64")


def _fractions(values: pd.Series, label: str) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    if numeric.isna().any() or ((numeric < 0) | (numeric > 1)).any():
        raise ValueError(f"{label}: expected measured source fraction in [0,1]")
    return numeric.astype(float)


def _single_exact(df: pd.DataFrame, field: str, value: object, label: str) -> None:
    if df[field].isna().any() or not df[field].astype(str).str.strip().eq(str(value)).all():
        raise ValueError(f"{label}: pinned field {field} must be {value}")


def analyze_lu_night_channels(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Original all-survey sheet only; NEVER pool with focal species worksheet.

    Fly replacement threshold is *hypothetical pollen efficacy* relative
    to Lepidoptera for just these two orders, not estimated compensation.
    """
    _require(df, LU_COLS, "Lu night guild")
    if len(df) != 3 or df["guild"].duplicated().any() or set(df["guild"]) != {
        "all_documented_visits", "Lepidoptera", "Diptera"
    }:
        raise ValueError("Lu night guild: require three distinct all-survey rows")
    for field, value in (
        ("study_id", LU_ID),
        ("source_sheet", "visitation"),
        ("diel_period", "night"),
        ("metric", "visit_events"),
        ("independent_blocks", "5"),
        ("study_doi", "10.1002/ece3.74368"),
        ("alan_source_commit", LU_COMMIT),
        ("original_workbook_sha256", LU_RAW_SHA),
    ):
        _single_exact(df, field, value, "Lu night guild")
    visits = df.copy()
    for key in ("dark_visits", "lit_visits"):
        visits[key] = _nonnegative_int(visits[key], key)
    source = visits.set_index("guild")
    if source.loc["all_documented_visits", "dark_visits"] < (
        source.loc[["Lepidoptera", "Diptera"], "dark_visits"].sum()
    ) or source.loc["all_documented_visits", "lit_visits"] < (
        source.loc[["Lepidoptera", "Diptera"], "lit_visits"].sum()
    ):
        raise ValueError("Lu all-survey total cannot be smaller than recorded subset")
    original = {
        "all_documented_visits": (1312, 848),
        "Lepidoptera": (838, 357),
        "Diptera": (54, 151),
    }
    for group, (dark, light) in original.items():
        if (int(source.loc[group, "dark_visits"]),
                int(source.loc[group, "lit_visits"])) != (dark, light):
            raise ValueError(f"Lu original-source published count drift: {group}")
    visits["lit_over_dark_visits"] = visits["lit_visits"] / visits["dark_visits"]
    visits["relative_visit_change"] = visits["lit_over_dark_visits"] - 1.0
    visits["outcome_type"] = "visit_count_only_not_pollen_or_seeds"

    lost_lepid = int(source.loc["Lepidoptera", "dark_visits"]
                     - source.loc["Lepidoptera", "lit_visits"])
    gained_flies = int(source.loc["Diptera", "lit_visits"]
                       - source.loc["Diptera", "dark_visits"])
    if lost_lepid <= 0 or gained_flies <= 0:
        raise ValueError("Lu dark-light direction invalid for proposed compensation bound")
    threshold = lost_lepid / gained_flies
    # Report the full stated parameter sweep, not just the break-even value.
    scenarios = []
    for relative_fly_pollen in (0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0):
        dark_weighted = (838 + 54 * relative_fly_pollen)
        lit_weighted = (357 + 151 * relative_fly_pollen)
        scenarios.append({
            "assumed_fly_over_lepidoptera_pollen_effectiveness_per_visit":
                relative_fly_pollen,
            "dark_two_guild_hypothetical_units": dark_weighted,
            "lit_two_guild_hypothetical_units": lit_weighted,
            "lit_over_dark_two_guild_hypothetical_ratio": (
                lit_weighted / dark_weighted
            ),
            "is_real_measured_pollen_delivery": False,
        })
    result = {
        "study_id": LU_ID,
        "independent_original_field_blocks": 5,
        "lepidoptera_visits_lost": lost_lepid,
        "diptera_visits_gained": gained_flies,
        "count_only_substitution_share": gained_flies / lost_lepid,
        "hypothetical_per_visit_fly_effectiveness_break_even": threshold,
        "observed_effectiveness_per_visit": None,
        "actual_net_pollen_service_measured": False,
        "source_sheet_is_all_surveys": True,
        "other_author_worksheet_can_be_subtracted_from_this_one": False,
        "seasonal_flight_phenology_measured_for_iwe": False,
        "strict_h1_effects_created": 0,
    }
    return visits, pd.DataFrame(scenarios), result


def analyze_boom_spectral_nursery(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Reconstruct authors' reported SEED-OUTPUT ARITHMETIC from rounded means.

    Final seed outcome significance is the SOURCE paper p=0.63 (not a
    new test), and individual units/variance are NOT back-computed here.
    """
    _require(df, BOOM_COLS, "Boom dual-role spectrum")
    if len(df) != 4 or df["light_spectrum"].duplicated().any() or (
        set(df["light_spectrum"]) != set(LIGHT_COLOURS)
    ):
        raise ValueError("Boom: exactly dark, red, green and white original arms needed")
    for field, value in (
        ("study_id", BOOM_ID),
        ("plant", "Silene latifolia"),
        ("insect", "Hadena bicruris"),
        ("field_sites", "4"),
        ("study_doi", "10.1038/s41598-020-75471-1"),
        ("alan_source_commit", BOOM_COMMIT),
        ("source_jats_sha256", BOOM_JATS_SHA),
    ):
        _single_exact(df, field, value, "Boom dual-role spectrum")
    table = df.copy()
    for col in ("fruit_set_fraction", "fruit_infestation_fraction",
                "uninfested_ovule_fertilized_fraction", "reported_seed_mean_anova_p"):
        table[col] = _fractions(table[col], col)
    for col in ("reported_estimated_seeds_per_flower", "mean_ovules_per_fruit"):
        table[col] = _nonnegative_int(table[col], col)
    if table["mean_ovules_per_fruit"].nunique() != 1 or (
        table["mean_ovules_per_fruit"].iloc[0] != 404
    ):
        raise ValueError("Boom: 404 original mean ovules per fruit required")
    if not table["reported_seed_mean_anova_p"].eq(0.63).all():
        raise ValueError("Boom: reported net seed ANOVA p not source-compatible")
    expected = {
        "dark": (0.73, 0.28, 0.56, 117),
        "white": (0.78, 0.44, 0.49, 86),
        "green": (0.75, 0.53, 0.43, 61),
        "red": (0.71, 0.33, 0.47, 90),
    }
    for _, row in table.iterrows():
        f, inf, fertil, seeds = expected[row["light_spectrum"]]
        if any(abs(row[col] - val) > 1e-12 for col, val in (
            ("fruit_set_fraction", f),
            ("fruit_infestation_fraction", inf),
            ("uninfested_ovule_fertilized_fraction", fertil),
        )) or row["reported_estimated_seeds_per_flower"] != seeds:
            raise ValueError("Boom: published spectrum data drift")
    table["noninfested_fruit_fraction"] = 1.0 - table["fruit_infestation_fraction"]
    table["model_seeds_from_rounded_components"] = (
        table["fruit_set_fraction"] *
        table["noninfested_fruit_fraction"] *
        table["uninfested_ovule_fertilized_fraction"] *
        table["mean_ovules_per_fruit"]
    )
    if ((table["model_seeds_from_rounded_components"]
         - table["reported_estimated_seeds_per_flower"]).abs() > 2.0).any():
        raise ValueError("Boom: model seeds diverge from source rounded means")
    dark = table.set_index("light_spectrum").loc["dark"]
    table["rounded_mean_seeds_ratio_to_dark"] = (
        table["model_seeds_from_rounded_components"] /
        dark["model_seeds_from_rounded_components"]
    )
    table["net_seeds_significant_reported"] = False
    table["is_actual_counted_mature_seed_observation"] = False
    table["interpretable_as_causal_mediation"] = False
    green = table.set_index("light_spectrum").loc["green"]
    result = {
        "study_id": BOOM_ID,
        "field_sites_in_one_original_study": 4,
        "insect_species": "Hadena bicruris",
        "plant_name_as_published": "Silene latifolia",
        "dark_published_model_seeds_per_flower": int(
            dark["reported_estimated_seeds_per_flower"]
        ),
        "green_published_model_seeds_per_flower": int(
            green["reported_estimated_seeds_per_flower"]
        ),
        "green_over_dark_rounded_component_product": float(
            green["rounded_mean_seeds_ratio_to_dark"]
        ),
        "reported_net_seed_anova_p": 0.63,
        "source_supports_significant_net_seed_reduction": False,
        "source_supports_change_in_fruit_infestation": True,
        "no_independent_seasonal_hadena_activity_window": True,
        "single_fruit_plant_variances_reconstructed": False,
        "strict_h1_effects_created": 0,
    }
    return table, result


def check_iwe_taxon_relation(candidates: pd.DataFrame) -> dict:
    """Read the true frozen IWE candidate; DO NOT add ALAN as a new SMD."""
    _require(candidates, IWE_COLS, "IWE replication candidate registry")
    selected = candidates.loc[candidates["candidate_id"] == IWE_MIXED_ID]
    if len(selected) != 1:
        raise ValueError("IWE Silene-Hadena historic source candidate not unique")
    row = selected.iloc[0]
    if (row["animal_taxon"] != "Hadena bicruris"
            or row["plant_taxon"] != "Silene alba / Silene dioica"
            or row["target_class"] != "mixed_pollinating_seed_predator"
            or row["status"] != "rejected_timing"
            or str(row["timing_window_measured"]).strip().lower() != "no"):
        raise ValueError("IWE source/partner timing gate changed; re-adjudicate")
    return {
        "iwe_candidate_id": IWE_MIXED_ID,
        "historical_original_publication_year": 1996,
        "light_experiment_original_publication_year": 2020,
        "exact_shared_insect": "Hadena bicruris",
        "original_iwe_plant_names": "Silene alba / Silene dioica",
        "light_experiment_plant": "Silene latifolia",
        "taxonomy": (
            "Silene alba recognized by POWO as synonym of "
            "Silene latifolia subsp. alba; NOT same as the full "
            "Silene alba / Silene dioica mixed source population"
        ),
        "same_original_programme": False,
        "same_population_time_exposure_unit": False,
        "alan_measures_diel_pollination_seedpredation_components": True,
        "alan_measures_iwe_strict_seasonal_partner_window": False,
        "iwe_current_adjudication": "rejected_timing",
        "promote_alan_to_iwe_strict_h1": False,
    }


def build_three_repo_receipt(
    lu: pd.DataFrame, boom: pd.DataFrame, candidates: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    lu_rates, efficacy_scenarios, lu_report = analyze_lu_night_channels(lu)
    boom_spectra, boom_report = analyze_boom_spectral_nursery(boom)
    iwe_relation = check_iwe_taxon_relation(candidates)
    receipt: dict[str, Any] = {
        "schema": "iwe_chocho_alan_function_bridge_v0.1",
        "reference_date": "2026-11-14",
        "source_programmes": 2,
        "light_study_level": "one Lu Tibetan manipulated experiment and one Boom Netherlands manipulated experiment",
        "same_experiment_repeated_as_independent_studies": False,
        "original_alan_source_status": "source_reproduced_on_draft_PRs_not_merged_ALAN_main",
        "lu": lu_report,
        "boom": boom_report,
        "iwe_shared_taxon": iwe_relation,
        "chocho": {
            "reference_role": "independent_historic_butterfly_larval_host_potential_resource_geography",
            "shared_reference_butterfly": "Anthocharis cardamines",
            "same_species_site_year_alan_experiment": False,
            "light_exposure_linked_to_chocho_accepted_hosts": False,
            "source_derived_learnt_flowering_phenophase": False,
            "cross_scale_model_evaluable": False,
        },
        "treatment_exposure_modes": [
            "local_manipulated_alighting_with_spectrum_boom",
            "manipulated_lit_vs_dark_lu",
        ],
        "satellite_annual_VIIRS_is_not_equivalent_to_ground_lux": True,
        "diel_night_visits_is_not_day_of_year_seasonal_overlap": True,
        "light_dependent_pollen_transfer_measured_for_substitution": False,
        "seasonal_flower_and_adult_overlap_measured_same_unit": False,
        "measured_island_mainland_light_x_partner_shift": False,
        "pooled_meta_effect_claimed": False,
        "new_iwe_h1_effects": 0,
        "original_iwe_meta_claim_unchanged": True,
        "original_chocho_paper_unchanged": True,
        "original_alan_paper_claim_unchanged": True,
    }
    return lu_rates, efficacy_scenarios, boom_spectra, receipt
