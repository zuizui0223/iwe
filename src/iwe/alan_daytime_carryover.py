"""Source-pinned daytime-only pollination after night-light and slug exposure.

The author preprint (Grognuz & Knop 2026, ResearchGate Table S3)
provides 28 daytime pollinator-choice rounds with four crossed treatment
combinations. ALAN's draft PR #78 transcribed the source into four
per-round MEANS and observed-n counts; this is NOT original raw data,
nor 28 independent light assignments. This module checks those
published eight group means before any source calculation.

No nocturnal access by insects to the designated target flower was
intended; bagged controls show rare leakage (3 of 39), so absolute
exclusion cannot be claimed. All effects below are descriptive and
must not be interpreted as a light-by-nocturnal-pollinator interaction.
"""
from __future__ import annotations

import csv
import hashlib
import math
from collections import Counter
from pathlib import Path

CELLS = ("dark_no_slug", "dark_slug", "lit_no_slug", "lit_slug")
PUBLISHED = {
    "Trifolium pratense": (4.56, 5.34, 3.66, 3.39),
    "Centaurea jacea": (1.71, 1.53, 0.41, 1.85),
}
COUNTS = {"Trifolium pratense": 20, "Centaurea jacea": 8}
ORIGINAL_AUTHOR_DOI = "10.13140/RG.2.2.36822.10563"
ORIGINAL_AUTHOR_DATA_DOI = "10.17632/drhzznh4ps.1"
ALAN_SOURCE_GIT_BLOB = "92283023f36872d24b17a637e493e9d3bcda9bb0"
ALAN_PINNED_COMMIT = "331b729ec43b680f6b1f20cfd796a40e92307994"


def _gitblob(source: bytes) -> str:
    return hashlib.sha1(f"blob {len(source)}\0".encode() + source).hexdigest()


def read_alan_derived_source(source: bytes, verify: bool = True) -> list[dict]:
    if verify and _gitblob(source) != ALAN_SOURCE_GIT_BLOB:
        raise ValueError("The pinned ALAN-derived four-arm source changed")
    try:
        text = source.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ValueError("Incorrect source encoding") from exc
    import io
    reader = csv.DictReader(io.StringIO(text))
    expected = {"block_id"} | {
        prefix + cell for prefix in ("mean_", "n_") for cell in CELLS
    }
    if set(reader.fieldnames or []) != expected:
        raise ValueError("Derived source table missing or adding columns")
    source_rows = list(reader)
    if verify and len(source_rows) != 28:
        raise ValueError("Expected exactly 28 original daytime choice rounds")
    rows = []
    names = set()
    for src in source_rows:
        key = src["block_id"]
        if not key or key in names:
            raise ValueError("Empty or duplicate original choice round identifier")
        names.add(key)
        species = (
            "Trifolium pratense" if key.startswith("T")
            else "Centaurea jacea" if key.startswith("C")
            else None
        )
        if species is None:
            raise ValueError("No evidence linking source block to original plant species")
        means = []
        ns = []
        for cell in CELLS:
            try:
                mean = float(src["mean_" + cell])
                n = int(src["n_" + cell])
            except (TypeError, ValueError) as exc:
                raise ValueError("Unrecoverable original arm mean/count") from exc
            if not math.isfinite(mean) or mean < 0 or not 1 <= n <= 4:
                raise ValueError("Impossible original seed mean or pot count")
            means.append(mean)
            ns.append(n)
        rows.append({"block_id": key, "species": species, "mean": means, "n": ns})
    if verify:
        if set(names) != (
            {f"T{i:02d}" for i in range(1,21)} |
            {f"C{i:02d}" for i in range(1,9)}
        ):
            raise ValueError("Missing, unexpected, or misassigned source block")
        if sum(sum(row["n"]) for row in rows) != 425:
            raise ValueError("The original source has 425 observed seeds outcomes of 448 pots")
        for species, expected_means in PUBLISHED.items():
            subset = [row for row in rows if row["species"] == species]
            if len(subset) != COUNTS[species]:
                raise ValueError("Original research plant/choice-round count drift")
            for i, expected_mean in enumerate(expected_means):
                numerator = sum(row["mean"][i] * row["n"][i] for row in subset)
                denominator = sum(row["n"][i] for row in subset)
                if abs(numerator / denominator - expected_mean) > .011:
                    raise ValueError("Derived seed table disagrees with author Table S3 mean")
    return rows


def _means(rows: list[dict]) -> list[float]:
    if not rows:
        raise ValueError("Zero original study rounds")
    return [sum(r["mean"][i] for r in rows) / len(rows) for i in range(4)]


def _label_sign(values: list[float]) -> dict:
    return {
        "negative_rounds":sum(v < -1e-12 for v in values),
        "positive_rounds":sum(v > 1e-12 for v in values),
        "tied_rounds":sum(abs(v) <= 1e-12 for v in values),
        "total_rounds":len(values),
        "sign_test_valid_for_independent_light_allocations":False,
    }


def summarize_daytime_carryover(rows: list[dict], *, verified: bool = True) -> tuple[list[dict], dict]:
    if not rows or set(row["species"] for row in rows) != set(COUNTS):
        raise ValueError("Both plant species required, and no others")
    outcome = []
    for species, expected_n in COUNTS.items():
        group = [r for r in rows if r["species"] == species]
        if verified and len(group) != expected_n:
            raise ValueError("Original source has wrong choice-round count")
        means = _means(group)
        dark_noslug, dark_slug, lit_noslug, lit_slug = means
        dark = (dark_noslug + dark_slug) / 2
        lit = (lit_noslug + lit_slug) / 2
        no_slug = lit_noslug - dark_noslug
        slug = lit_slug - dark_slug
        paired_noslug = [r["mean"][2] - r["mean"][0] for r in group]
        paired_slug = [r["mean"][3] - r["mean"][1] for r in group]
        number_by_cell = [sum(r["n"][i] for r in group) for i in range(4)]
        sums_by_cell = [
            sum(r["mean"][i] * r["n"][i] for r in group) for i in range(4)
        ]
        dark_total = sums_by_cell[0] + sums_by_cell[1]
        lit_total = sums_by_cell[2] + sums_by_cell[3]
        no_observation = [4*len(group) - n for n in number_by_cell]
        missing_lit = no_observation[2] + no_observation[3]
        tipping = (
            (dark_total - lit_total) / missing_lit if missing_lit > 0 else None
        )
        outcome.append({
            "species":species,
            "source_choice_rounds":len(group),
            "dark_no_slug_seed_mean":dark_noslug,
            "lit_no_slug_seed_mean":lit_noslug,
            "dark_slug_seed_mean":dark_slug,
            "lit_slug_seed_mean":lit_slug,
            "no_slug_lit_dark_ratio":(
                lit_noslug / dark_noslug if dark_noslug > 0 else None
            ),
            "slug_lit_dark_ratio":(
                lit_slug / dark_slug if dark_slug > 0 else None
            ),
            "all_slug_conditions_dark_mean":dark,
            "all_slug_conditions_lit_mean":lit,
            "equal_choice_round_lit_dark_ratio":lit / dark if dark > 0 else None,
            "light_no_slug_seed_difference":no_slug,
            "light_slug_seed_difference":slug,
            "slug_x_light_additive_difference_of_differences":slug - no_slug,
            "night_pollination_window_for_target_flower":"bagged_except_daytime_90_min",
            "no_slug_block_sign_counts":_label_sign(paired_noslug),
            "slug_block_sign_counts":_label_sign(paired_slug),
            "observed_pot_seeds_by_cell":list(map(float,sums_by_cell)),
            "observed_pots_by_cell":number_by_cell,
            "source_missing_pots_by_cell":no_observation,
            "tipping_missing_lit_pot_seed_per_pot_if_dark_missing_assumed_zero":tipping,
            "tipping_is_pessimistic_dark_missing_zero_assumption":True,
            "source_plant_reused_over_weeks":True,
            "source_choice_rounds_are_independent_lamp_installations":False,
            "valid_new_lighting_study_effect_SE":False,
        })
    if verified:
        obs = sum(sum(o["observed_pots_by_cell"]) for o in outcome)
        if obs != 425:
            raise ValueError("All source-observed target pots must reconcile")
        for o in outcome:
            expected_total = {
                "Trifolium pratense": (783,540),
                "Centaurea jacea": (94,62),
            }[o["species"]]
            sums = o["observed_pot_seeds_by_cell"]
            dark, lit = sums[0]+sums[1],sums[2]+sums[3]
            if not math.isclose(dark, expected_total[0], abs_tol=.001) or not math.isclose(lit, expected_total[1], abs_tol=.001):
                raise ValueError("Source seed totals disagree with Table S3")
    receipt = {
        "schema":"iwe_alan_daytime_carryover_from_published_TableS3_v0.1",
        "author_preprint_DOI":ORIGINAL_AUTHOR_DOI,
        "author_data_DOI":ORIGINAL_AUTHOR_DATA_DOI,
        "upstream_alan_branch_pinned_commit":ALAN_PINNED_COMMIT,
        "upstream_alan_derived_git_blob":ALAN_SOURCE_GIT_BLOB,
        "source_kind":"transcribed_per_round_derived_means_not_original_pot_records",
        "published_original_model_seed_beta":-.40,
        "published_original_model_seed_beta_CI95":[-.73,-.08],
        "published_original_model_seed_p":.014,
        "published_original_visit_beta":-.38,
        "published_original_visit_beta_CI95":[-.60,-.16],
        "original_n_daytime_choice_rounds":28,
        "original_n_target_pots":448,
        "original_n_observed_seed_outcomes":425,
        "original_n_missing_seed_outcomes":23,
        "original_fully_bagged_control_flower_total":39,
        "fully_bagged_control_flower_seed_positive":3,
        "Trifolium_bagged_control_seed_positive":0,
        "Trifolium_bagged_control_total":9,
        "Centaurea_bagged_control_seed_positive":3,
        "Centaurea_bagged_control_total":30,
        "pollination_exclusively_daytime_verified_without_exception":False,
        "vast_majority_of_seed_producing_pollination_during_daytime_trial":True,
        "different_potted_plants_and_blocks_are_independent_light_installations":False,
        "all_pot_level_original_observations_recovered":False,
        "original_model_beta_equals_descriptive_log_seed_ratio":False,
        "statistical_light_by_slug_effect_from_derived_means_estimated":False,
        "source_site_cluster_SE_obtained":False,
        "focal_species_original_nocturnal_dependence_measured":False,
        "daylight_carryover_mechanism_identified":False,
        "strict_h1_effects_created":0,
        "ALAN_by_night_dependence_global_beta_estimated":False,
        "claim_ceiling":"Illuminated nighttime history is associated with lower subsequent daytime-window seed output in two author preprint plants, but source treatment-site clustering, reused plants, seed missingness and mechanism preclude a new independent causal meta-effect.",
    }
    return outcome, receipt
