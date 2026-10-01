import pandas as pd
import pytest

from iwe.iwe015_promotion import build_iwe015_promotion_packet


EFFECT_COLUMNS = [
    "effect_id", "study_id", "dataset_id", "dependence_id", "plant_taxon",
    "animal_taxon", "interaction_type", "evidence_tier", "phenology_source",
    "timing_metric_type", "timing_analysis_class", "timing_domain",
    "exposure_direction", "outcome_family", "effect_family", "effect_native",
    "variance_native", "sample_size", "source_id", "site_id", "year",
    "latitude", "elevation_m", "island_context", "specialization", "redundancy",
    "notes",
]


def _raw():
    return pd.DataFrame(
        [
            {
                "year": 2012,
                "raw_effect_ready": True,
                "effect_native": -0.35,
                "variance_native": 0.034,
                "n_early": 59,
                "n_late": 58,
            },
            {
                "year": 2013,
                "raw_effect_ready": True,
                "effect_native": 0.17,
                "variance_native": 0.036,
                "n_early": 55,
                "n_late": 55,
            },
        ]
    )


def _studies():
    return pd.DataFrame([{"study_id": "IWE015", "screening_status": "include"}])


def _effects():
    return pd.DataFrame(columns=EFFECT_COLUMNS)


def _adjudications():
    cols = [
        "adjudication_id", "study_id", "component", "strict_h1_status",
        "quantitative_status", "expected_effect_id", "timing_metric_type",
        "timing_analysis_class", "timing_domain", "effect_family", "reason",
    ]
    return pd.DataFrame(
        [
            {
                "adjudication_id": "ADJ_IWE015_2012",
                "study_id": "IWE015",
                "component": "2012_pending",
                "strict_h1_status": "eligible",
                "quantitative_status": "pending",
                "expected_effect_id": "",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "standardized_mean_difference",
                "reason": "raw variance pending",
            },
            {
                "adjudication_id": "ADJ_IWE015_2013",
                "study_id": "IWE015",
                "component": "2013_pending",
                "strict_h1_status": "eligible",
                "quantitative_status": "pending",
                "expected_effect_id": "",
                "timing_metric_type": "seasonal_position",
                "timing_analysis_class": "strict_window",
                "timing_domain": "ordered_by_measured_window",
                "effect_family": "standardized_mean_difference",
                "reason": "raw variance pending",
            },
        ],
        columns=cols,
    )


def _window():
    return pd.DataFrame(
        columns=[
            "effect_id", "study_id", "window_basis", "same_season", "source_id",
            "source_measurement", "notes",
        ]
    )


def _units():
    return pd.DataFrame(
        columns=[
            "effect_id", "study_id", "design_type", "exposure_grain",
            "response_grain", "variance_interpretation", "inference_scope",
            "causal_claim_allowed", "notes",
        ]
    )


def _packet(**overrides):
    args = {
        "raw_effects": _raw(),
        "studies": _studies(),
        "current_effects": _effects(),
        "adjudications": _adjudications(),
        "window_provenance": _window(),
        "unit_provenance": _units(),
    }
    args.update(overrides)
    return build_iwe015_promotion_packet(**args)


def test_ready_raw_effects_build_atomic_promotion_packet():
    packet = _packet()
    assert len(packet["effects_append"]) == 2
    assert set(packet["effects_append"]["year"]) == {2012, 2013}
    assert set(packet["window_provenance_append"]["window_basis"]) == {
        "direct_adult_census"
    }
    assert set(packet["window_provenance_append"]["same_season"]) == {"yes"}
    assert set(packet["unit_provenance_append"]["design_type"]) == {
        "observational_individual_timing"
    }
    assert set(packet["unit_provenance_append"]["causal_claim_allowed"]) == {"no"}
    assert packet["manifest"]["egg_receipt_used_as_window"] is False
    assert packet["manifest"]["transactional_validation_passed"] is True


def test_unready_raw_year_fails_closed():
    raw = _raw()
    raw.loc[raw["year"] == 2012, "raw_effect_ready"] = False
    with pytest.raises(ValueError, match="raw effect is not ready"):
        _packet(raw_effects=raw)


def test_effect_collision_fails_closed():
    current = _effects()
    current.loc[len(current)] = {
        "effect_id": "IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD",
        "study_id": "IWE015",
        "dataset_id": "old",
        "dependence_id": "DEP_OLD",
        "plant_taxon": "Silene stellata",
        "animal_taxon": "Hadena ectypa",
        "interaction_type": "mixed_pollinating_seed_predator",
        "evidence_tier": "A",
        "phenology_source": "direct_activity",
        "timing_metric_type": "seasonal_position",
        "timing_analysis_class": "direct_timing_sensitivity",
        "timing_domain": "not_applicable",
        "exposure_direction": "synchrony",
        "outcome_family": "successful_fruit_count",
        "effect_family": "standardized_mean_difference",
        "effect_native": 0.0,
        "variance_native": 0.1,
        "sample_size": 10,
        "source_id": "10.1111/evo.13965",
        "site_id": "x",
        "year": 2012,
        "latitude": "",
        "elevation_m": "",
        "island_context": "",
        "specialization": "",
        "redundancy": "",
        "notes": "",
    }
    with pytest.raises(ValueError, match="effect_id collision"):
        _packet(current_effects=current)


def test_study_must_remain_screening_include():
    studies = _studies()
    studies.loc[0, "screening_status"] = "unresolved"
    with pytest.raises(ValueError, match="screening_status=include"):
        _packet(studies=studies)
