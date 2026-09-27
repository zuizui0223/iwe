from __future__ import annotations

from collections.abc import Mapping

import pandas as pd

from .adjudication import validate_effect_adjudications
from .cardamine_pipeline import run_cardamine_preflight
from .cardamine_provenance import CARDAMINE_CANDIDATE_ID
from .replication_candidates import validate_replication_candidates
from .replication_routes import validate_replication_completion_routes
from .screening import validate_study_registry
from .validation import validate_effect_rows


STUDY_ID = "IWE032"
PENDING_ADJUDICATION_ID = "ADJ_IWE032_PENDING"
SOURCE_ID = "10.1002/ece3.11330"
DEPENDENCE_ID = "DEP_CARDAMINE_DIBBINSDALE_2012_2014"


def _single_row(df: pd.DataFrame, column: str, value: str, label: str) -> pd.Series:
    part = df.loc[df[column].astype(str) == value]
    if len(part) != 1:
        raise ValueError(f"{label} requires exactly one {column}={value} row")
    return part.iloc[0].copy()


def _renumber_routes(routes: pd.DataFrame) -> pd.DataFrame:
    out = routes.copy()
    pieces: list[pd.DataFrame] = []
    for target_class, group in out.groupby("target_class", sort=False):
        group = group.sort_values("route_rank").copy()
        group["route_rank"] = list(range(1, len(group) + 1))
        pieces.append(group)
    if not pieces:
        return out.iloc[0:0].copy()
    return pd.concat(pieces, ignore_index=True)


def _effect_id(year: object, ecotype: object) -> str:
    return f"IWE032_{int(year)}_{str(ecotype).upper()}_SYNC_REALIZEDFRAC_SMD"


def build_cardamine_promotion_packet(
    plant_observations: pd.DataFrame,
    adult_events: pd.DataFrame,
    adult_provenance: Mapping[str, object],
    plant_summaries: pd.DataFrame,
    studies: pd.DataFrame,
    current_effects: pd.DataFrame,
    adjudications: pd.DataFrame,
    candidates: pd.DataFrame,
    completion_routes: pd.DataFrame,
) -> dict[str, pd.DataFrame | dict[str, object]]:
    """Build and transactionally validate a non-mutating Cardamine promotion draft."""
    if adult_provenance.get("synthetic_fixture") is True:
        raise ValueError("synthetic Cardamine timing cannot generate a promotion packet")
    if adult_provenance.get("source_backed") is not True:
        raise ValueError("Cardamine promotion requires source-backed adult timing")

    study = _single_row(studies, "study_id", STUDY_ID, "Cardamine promotion")
    if str(study["screening_status"]) != "include":
        raise ValueError("IWE032 must be screening_status=include before promotion")
    study_errors = validate_study_registry(studies)
    if study_errors:
        raise ValueError("; ".join(study_errors))

    exposure, audit, smd = run_cardamine_preflight(
        plant_observations,
        adult_events,
        adult_provenance,
        plant_summaries,
    )
    if smd.empty:
        raise ValueError("Cardamine preflight produced no estimable SMD strata")

    draft_effects: list[dict[str, object]] = []
    draft_adjudications: list[dict[str, object]] = []
    timing_source = str(adult_provenance["source_id"])

    for _, row in smd.sort_values(["year", "ecotype"]).iterrows():
        year = int(row["year"])
        ecotype = str(row["ecotype"])
        effect_id = _effect_id(year, ecotype)
        n_high = int(row["n_higher_synchrony"])
        n_low = int(row["n_lower_synchrony"])
        draft_effects.append(
            {
                "effect_id": effect_id,
                "study_id": STUDY_ID,
                "dataset_id": f"DRYAD_V9S4MW741_{year}_{ecotype.upper()}",
                "dependence_id": DEPENDENCE_ID,
                "plant_taxon": "Cardamine pratensis",
                "animal_taxon": "Anthocharis cardamines",
                "interaction_type": "antagonist",
                "evidence_tier": "A",
                "phenology_source": "direct_activity",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "exposure_direction": "synchrony",
                "outcome_family": "realized_reproductive_fraction",
                "effect_family": "standardized_mean_difference",
                "effect_native": float(row["effect_native"]),
                "variance_native": float(row["variance_native"]),
                "sample_size": n_high + n_low,
                "source_id": SOURCE_ID,
                "site_id": "Dibbinsdale_Nature_Reserve",
                "year": year,
                "latitude": "",
                "elevation_m": "",
                "island_context": "",
                "specialization": "",
                "redundancy": "",
                "notes": (
                    f"Frozen Cardamine contrast within {year} {ecotype}: first flowering "
                    "inside/on the source female q10-q90 capture/recapture window is "
                    "higher synchrony; outside is lower synchrony. Response is "
                    "final_intact_ru/max_ru. "
                    f"Adult timing provenance={timing_source}. "
                    f"n_high={n_high}; n_low={n_low}. All rows share {DEPENDENCE_ID}."
                ),
            }
        )
        draft_adjudications.append(
            {
                "adjudication_id": f"ADJ_IWE032_{year}_{ecotype.upper()}",
                "study_id": STUDY_ID,
                "component": (
                    f"{year}_{ecotype}_first_flowering_vs_female_q10_q90_"
                    "realized_fraction"
                ),
                "strict_h1_status": "eligible",
                "quantitative_status": "strict_extracted",
                "expected_effect_id": effect_id,
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "standardized_mean_difference",
                "reason": (
                    "Exposure is frozen response-blind from source-backed female "
                    "capture/recapture timing; realized_fraction is frozen before "
                    "adult-date recovery; this year x ecotype stratum passes the "
                    "predeclared group-size and variance gate."
                ),
            }
        )

    effects_append = pd.DataFrame(draft_effects)
    adjudications_append = pd.DataFrame(draft_adjudications)

    effect_errors = validate_effect_rows(effects_append)
    if effect_errors:
        raise ValueError("; ".join(effect_errors))

    pending = adjudications.loc[
        adjudications["adjudication_id"].astype(str) == PENDING_ADJUDICATION_ID
    ]
    if len(pending) != 1:
        raise ValueError("Cardamine promotion requires exactly one pending adjudication")

    adjudications_after = pd.concat(
        [
            adjudications.loc[
                adjudications["adjudication_id"].astype(str)
                != PENDING_ADJUDICATION_ID
            ],
            adjudications_append,
        ],
        ignore_index=True,
    )
    effects_after = pd.concat([current_effects, effects_append], ignore_index=True)
    all_effect_errors = validate_effect_rows(effects_after)
    if all_effect_errors:
        raise ValueError("; ".join(all_effect_errors))
    adj_errors = validate_effect_adjudications(effects_after, adjudications_after)
    if adj_errors:
        raise ValueError("; ".join(adj_errors))

    candidate = _single_row(
        candidates, "candidate_id", CARDAMINE_CANDIDATE_ID, "Cardamine promotion"
    )
    ready = candidate.copy()
    ready["smd_summary_stats"] = "yes"
    ready["status"] = "ready"
    ready["blocker"] = ""
    ready["priority"] = "DONE"
    ready["notes"] = (
        str(ready["notes"])
        + " Promotion packet validated: source-backed adult timing plus frozen "
        "preflight produced one or more estimable SMD strata."
    )

    candidates_after = pd.concat(
        [
            candidates.loc[
                candidates["candidate_id"].astype(str) != CARDAMINE_CANDIDATE_ID
            ],
            pd.DataFrame([ready]),
        ],
        ignore_index=True,
    )
    candidate_errors = validate_replication_candidates(candidates_after)
    if candidate_errors:
        raise ValueError("; ".join(candidate_errors))

    routes_after = completion_routes.loc[
        completion_routes["candidate_id"].astype(str) != CARDAMINE_CANDIDATE_ID
    ].copy()
    routes_after = _renumber_routes(routes_after)
    route_errors = validate_replication_completion_routes(
        routes_after, candidates_after
    )
    if route_errors:
        raise ValueError("; ".join(route_errors))

    manifest = {
        "schema": "iwe_cardamine_promotion_packet_v1",
        "candidate_id": CARDAMINE_CANDIDATE_ID,
        "study_id": STUDY_ID,
        "adult_timing_source_id": timing_source,
        "effect_rows_to_append": int(len(effects_append)),
        "pending_adjudication_to_replace": PENDING_ADJUDICATION_ID,
        "completion_route_to_remove": CARDAMINE_CANDIDATE_ID,
        "candidate_status_after": "ready",
        "direct_repo_mutation_performed": False,
        "transactional_validation_passed": True,
    }
    return {
        "exposure": exposure,
        "audit": audit,
        "effects_append": effects_append,
        "adjudications_append": adjudications_append,
        "adjudications_after": adjudications_after,
        "candidate_ready_row": pd.DataFrame([ready]),
        "candidates_after": candidates_after,
        "completion_routes_after": routes_after,
        "manifest": manifest,
    }
