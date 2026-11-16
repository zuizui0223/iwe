import pandas as pd
import pytest

from iwe.cardamine_promotion import (
    CARDAMINE_CANDIDATE_ID,
    PENDING_ADJUDICATION_ID,
    build_cardamine_promotion_packet,
)


def _plant_timing():
    return pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 114, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "doy": 120, "flowers": 3},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "doy": 106, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "doy": 108, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E5", "doy": 135, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E6", "doy": 138, "flowers": 2},
        ]
    )


def _adult_events():
    rows = []
    for year in (2012, 2013, 2014):
        for doy in (110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130):
            rows.append({"year": year, "event_doy": doy})
    return pd.DataFrame(rows)


def _provenance(**overrides):
    item = {
        "candidate_id": CARDAMINE_CANDIDATE_ID,
        "site": "Dibbinsdale Nature Reserve",
        "sex": "female",
        "record_basis": "female_capture_recapture_events",
        "years": [2012, 2013, 2014],
        "source_id": "author_archive:cardamine_female_mrr",
        "source_backed": True,
        "synthetic_fixture": False,
        "adult_event_doy_basis": "calendar_day_of_year",
        "plant_observation_doy_basis": "calendar_day_of_year",
        "adult_calendar_origin_source_locator": "original 2012-2014 female capture/recapture calendar-date records",
        "figure_digitization_performed": False,
    }
    item.update(overrides)
    return item


def _summaries():
    return pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "max_ru": 10, "final_intact_ru": 8},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "max_ru": 10, "final_intact_ru": 6},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "max_ru": 10, "final_intact_ru": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "max_ru": 10, "final_intact_ru": 1},
            {"year": 2012, "ecotype": "early", "plant_id": "E5", "max_ru": 10, "final_intact_ru": 7},
            {"year": 2012, "ecotype": "early", "plant_id": "E6", "max_ru": 10, "final_intact_ru": 5},
        ]
    )


def _studies():
    return pd.DataFrame(
        [
            {
                "study_id": "IWE032",
                "source_id": "10.1002/ece3.11330",
                "title": "Cardamine study",
                "system_id": "SYS008",
                "screening_status": "include",
                "screening_reason": "direct timing and final reproduction",
                "interaction_type_candidate": "antagonist",
                "notes": "",
            }
        ]
    )


def _empty_effects():
    return pd.DataFrame(
        columns=[
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
            "site_id",
            "year",
            "latitude",
            "elevation_m",
            "island_context",
            "specialization",
            "redundancy",
            "notes",
        ]
    )


def _adjudications():
    return pd.DataFrame(
        [
            {
                "adjudication_id": PENDING_ADJUDICATION_ID,
                "study_id": "IWE032",
                "component": "pending_cardamine",
                "strict_h1_status": "unresolved",
                "quantitative_status": "pending",
                "expected_effect_id": "",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "standardized_mean_difference",
                "reason": "waiting for adult timing",
            }
        ]
    )


def _candidates():
    return pd.DataFrame(
        [
            {
                "candidate_id": CARDAMINE_CANDIDATE_ID,
                "source_id": "10.1002/ece3.11330",
                "plant_taxon": "Cardamine pratensis",
                "animal_taxon": "Anthocharis cardamines",
                "target_class": "antagonist",
                "effect_family_target": "standardized_mean_difference",
                "independent_programme": "yes",
                "timing_window_measured": "yes",
                "post_predation_final_reproduction": "yes",
                "smd_summary_stats": "partial",
                "status": "blocked_timing_linkage",
                "blocker": "adult dates missing",
                "priority": "P1",
                "notes": "top route",
            }
        ]
    )


def _routes():
    return pd.DataFrame(
        [
            {
                "candidate_id": CARDAMINE_CANDIDATE_ID,
                "target_class": "antagonist",
                "route_rank": 1,
                "source_access": "public_source_insufficient",
                "public_search_status": "exhausted",
                "unlock_type": "timing_linkage",
                "unlock_requirement": "recover adult dates",
                "next_action_type": "contact_or_archive",
                "next_action": "request adult dates",
                "stop_rule": "do not digitize",
                "last_audited": "2026-09-27",
            }
        ]
    )


def _packet(**kwargs):
    args = dict(
        plant_observations=_plant_timing(),
        adult_events=_adult_events(),
        adult_provenance=_provenance(),
        plant_summaries=_summaries(),
        studies=_studies(),
        current_effects=_empty_effects(),
        adjudications=_adjudications(),
        candidates=_candidates(),
        completion_routes=_routes(),
    )
    args.update(kwargs)
    return build_cardamine_promotion_packet(**args)


def test_valid_packet_is_non_mutating_but_transactionally_ready():
    packet = _packet()
    assert packet["manifest"]["transactional_validation_passed"] is True
    assert packet["manifest"]["direct_repo_mutation_performed"] is False
    assert len(packet["effects_append"]) == 2
    assert set(packet["effects_append"]["study_id"]) == {"IWE032"}
    assert set(packet["effects_append"]["dependence_id"]) == {
        "DEP_CARDAMINE_DIBBINSDALE_2012_2014"
    }
    assert set(packet["effects_append"]["sample_size"]) == {4}
    assert any("CORE_VS_EARLY" in value for value in packet["effects_append"]["effect_id"])
    assert any("CORE_VS_LATE" in value for value in packet["effects_append"]["effect_id"])
    assert packet["candidate_ready_row"].iloc[0]["status"] == "ready"
    assert packet["candidate_ready_row"].iloc[0]["smd_summary_stats"] == "yes"
    assert packet["completion_routes_after"].empty
    assert PENDING_ADJUDICATION_ID not in set(
        packet["adjudications_after"]["adjudication_id"]
    )


def test_synthetic_timing_cannot_generate_promotion():
    with pytest.raises(ValueError, match="synthetic"):
        _packet(
            adult_provenance=_provenance(
                source_id="synthetic:test",
                source_backed=False,
                synthetic_fixture=True,
            )
        )


def test_existing_effect_id_collision_fails_transaction():
    first = _packet()["effects_append"].copy()
    with pytest.raises(ValueError, match="duplicate effect_id"):
        _packet(current_effects=first)


def test_study_must_be_registered_include():
    studies = _studies()
    studies.loc[0, "screening_status"] = "unresolved"
    with pytest.raises(ValueError, match="screening_status=include"):
        _packet(studies=studies)
