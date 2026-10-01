from __future__ import annotations

import math

import pandas as pd

from .adjudication import validate_effect_adjudications
from .unit_provenance import validate_strict_unit_provenance
from .validation import validate_effect_rows
from .window_provenance import validate_strict_window_provenance


STUDY_ID = "IWE015"
SOURCE_ID = "10.1111/evo.13965"
DATASET_ID = "DRYAD_6Q573N5W1"
DEPENDENCE_ID = "DEP_SILENE_STELLATA_HADENA_MLBS"

EFFECT_IDS = {
    2012: "IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD",
    2013: "IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD",
}
ADJUDICATION_IDS = {
    2012: "ADJ_IWE015_2012",
    2013: "ADJ_IWE015_2013",
}


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")


def _study_is_include(studies: pd.DataFrame) -> None:
    _require_columns(studies, {"study_id", "screening_status"}, "studies")
    part = studies.loc[studies["study_id"].astype(str) == STUDY_ID]
    if len(part) != 1:
        raise ValueError("IWE015 promotion requires exactly one study-registry row")
    if str(part.iloc[0]["screening_status"]) != "include":
        raise ValueError("IWE015 must be screening_status=include before promotion")


def _validate_raw_candidates(raw_effects: pd.DataFrame) -> pd.DataFrame:
    required = {
        "year",
        "raw_effect_ready",
        "effect_native",
        "variance_native",
        "n_early",
        "n_late",
    }
    _require_columns(raw_effects, required, "raw_effects")
    part = raw_effects.copy()
    part["year"] = pd.to_numeric(part["year"], errors="raise").astype(int)
    if set(part["year"]) != {2012, 2013} or len(part) != 2:
        raise ValueError("IWE015 promotion requires exactly the 2012 and 2013 raw effect rows")
    if part["year"].duplicated().any():
        raise ValueError("IWE015 raw effect years must be unique")

    for _, row in part.iterrows():
        ready = row["raw_effect_ready"]
        if isinstance(ready, str):
            ready_bool = ready.strip().lower() in {"true", "1", "yes"}
        else:
            ready_bool = bool(ready)
        if not ready_bool:
            raise ValueError(f"year={int(row['year'])}: raw effect is not ready")
        effect = float(row["effect_native"])
        variance = float(row["variance_native"])
        n_early = int(row["n_early"])
        n_late = int(row["n_late"])
        if not math.isfinite(effect):
            raise ValueError(f"year={int(row['year'])}: effect_native must be finite")
        if not math.isfinite(variance) or variance <= 0:
            raise ValueError(f"year={int(row['year'])}: variance_native must be finite and positive")
        if n_early < 2 or n_late < 2:
            raise ValueError(f"year={int(row['year'])}: both raw groups require n>=2")
    return part.sort_values("year").reset_index(drop=True)


def build_iwe015_promotion_packet(
    raw_effects: pd.DataFrame,
    studies: pd.DataFrame,
    current_effects: pd.DataFrame,
    adjudications: pd.DataFrame,
    window_provenance: pd.DataFrame,
    unit_provenance: pd.DataFrame,
) -> dict[str, pd.DataFrame | dict[str, object]]:
    """Build a validated, non-mutating IWE015 strict re-admission draft."""
    _study_is_include(studies)
    raw = _validate_raw_candidates(raw_effects)

    draft_effects: list[dict[str, object]] = []
    draft_adjudications: list[dict[str, object]] = []
    draft_windows: list[dict[str, object]] = []
    draft_units: list[dict[str, object]] = []

    for _, row in raw.iterrows():
        year = int(row["year"])
        effect_id = EFFECT_IDS[year]
        n_early = int(row["n_early"])
        n_late = int(row["n_late"])
        draft_effects.append(
            {
                "effect_id": effect_id,
                "study_id": STUDY_ID,
                "dataset_id": f"{DATASET_ID}_{year}_FEMALE",
                "dependence_id": DEPENDENCE_ID,
                "plant_taxon": "Silene stellata",
                "animal_taxon": "Hadena ectypa",
                "interaction_type": "mixed_pollinating_seed_predator",
                "evidence_tier": "A",
                "phenology_source": "direct_activity",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "exposure_direction": "synchrony",
                "outcome_family": "successful_fruit_count",
                "effect_family": "standardized_mean_difference",
                "effect_native": float(row["effect_native"]),
                "variance_native": float(row["variance_native"]),
                "sample_size": n_early + n_late,
                "source_id": SOURCE_ID,
                "site_id": "Mountain_Lake_Biological_Station",
                "year": year,
                "latitude": "",
                "elevation_m": "",
                "island_context": "",
                "specialization": "",
                "redundancy": "",
                "notes": (
                    f"Raw Dryad female data verified for {year}: early H. ectypa-dominant "
                    "minus late co-pollinator-dominant successful-fruit count. "
                    "Same-season adult moth density is source-backed by Zhou et al. "
                    "Figure 1 (moths per flower x100); egg density is not used as the "
                    "partner-window basis. "
                    f"n_early={n_early}; n_late={n_late}; all rows share {DEPENDENCE_ID}."
                ),
            }
        )
        draft_adjudications.append(
            {
                "adjudication_id": ADJUDICATION_IDS[year],
                "study_id": STUDY_ID,
                "component": (
                    f"{year}_Hadena_dominant_vs_copollinator_dominant_successful_fruits"
                ),
                "strict_h1_status": "eligible",
                "quantitative_status": "strict_extracted",
                "expected_effect_id": effect_id,
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "standardized_mean_difference",
                "reason": (
                    f"{year} early/late windows are ordered by same-season adult moth "
                    "density in Zhou et al. Figure 1; raw Dryad female data reproduce "
                    "the published experiment and supply the final successful-fruit "
                    "SMD and variance directly."
                ),
            }
        )
        draft_windows.append(
            {
                "effect_id": effect_id,
                "study_id": STUDY_ID,
                "window_basis": "direct_adult_census",
                "same_season": "yes",
                "source_id": SOURCE_ID,
                "source_measurement": (
                    f"Zhou et al. Figure 1 reports {year} H. ectypa and co-pollinating "
                    "adult moth density as number of moths observed per flower x100 "
                    "across the flowering season."
                ),
                "notes": (
                    "The separate egg-density series is a realized oviposition outcome "
                    "and is not used to define the strict partner window."
                ),
            }
        )
        draft_units.append(
            {
                "effect_id": effect_id,
                "study_id": STUDY_ID,
                "design_type": "observational_individual_timing",
                "exposure_grain": "plant",
                "response_grain": "plant",
                "variance_interpretation": "individual_effect_sampling",
                "inference_scope": "descriptive_association",
                "causal_claim_allowed": "no",
                "notes": (
                    f"Distinct plants were selected for the {year} early and late "
                    "seasonal experiments; successful fruits are plant-level. The "
                    "contrast is observational seasonal context, not randomized timing."
                ),
            }
        )

    effects_append = pd.DataFrame(draft_effects)
    adjudications_replacement = pd.DataFrame(draft_adjudications)
    window_append = pd.DataFrame(draft_windows)
    unit_append = pd.DataFrame(draft_units)

    effect_errors = validate_effect_rows(effects_append)
    if effect_errors:
        raise ValueError("; ".join(effect_errors))

    existing_effect_ids = set(current_effects["effect_id"].astype(str))
    collisions = sorted(set(effects_append["effect_id"].astype(str)) & existing_effect_ids)
    if collisions:
        raise ValueError(f"IWE015 effect_id collision: {collisions}")

    pending_ids = set(ADJUDICATION_IDS.values())
    found = adjudications.loc[
        adjudications["adjudication_id"].astype(str).isin(pending_ids)
    ]
    if set(found["adjudication_id"].astype(str)) != pending_ids or len(found) != 2:
        raise ValueError("IWE015 promotion requires both current pending adjudications")

    adjudications_after = pd.concat(
        [
            adjudications.loc[
                ~adjudications["adjudication_id"].astype(str).isin(pending_ids)
            ],
            adjudications_replacement,
        ],
        ignore_index=True,
    )
    effects_after = pd.concat([current_effects, effects_append], ignore_index=True)
    windows_after = pd.concat([window_provenance, window_append], ignore_index=True)
    units_after = pd.concat([unit_provenance, unit_append], ignore_index=True)

    all_effect_errors = validate_effect_rows(effects_after)
    if all_effect_errors:
        raise ValueError("; ".join(all_effect_errors))

    adj_errors = validate_effect_adjudications(effects_after, adjudications_after)
    if adj_errors:
        raise ValueError("; ".join(adj_errors))

    window_errors = validate_strict_window_provenance(effects_after, windows_after)
    if window_errors:
        raise ValueError("; ".join(window_errors))

    unit_errors = validate_strict_unit_provenance(effects_after, units_after)
    if unit_errors:
        raise ValueError("; ".join(unit_errors))

    manifest = {
        "schema": "iwe015_promotion_packet_v1",
        "study_id": STUDY_ID,
        "source_id": SOURCE_ID,
        "dependence_id": DEPENDENCE_ID,
        "effect_rows_to_append": 2,
        "adjudications_to_replace": sorted(pending_ids),
        "window_provenance_rows_to_append": 2,
        "unit_provenance_rows_to_append": 2,
        "window_basis": "direct_adult_census",
        "egg_receipt_used_as_window": False,
        "direct_repo_mutation_performed": False,
        "transactional_validation_passed": True,
    }

    return {
        "effects_append": effects_append,
        "adjudications_replacement": adjudications_replacement,
        "window_provenance_append": window_append,
        "unit_provenance_append": unit_append,
        "effects_after": effects_after,
        "adjudications_after": adjudications_after,
        "window_provenance_after": windows_after,
        "unit_provenance_after": units_after,
        "manifest": manifest,
    }
