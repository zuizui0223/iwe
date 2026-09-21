import pandas as pd

from iwe.validation import build_primary_dataset, validate_effect_rows


def _row(**overrides):
    row = {
        "effect_id": "E1",
        "study_id": "S1",
        "dataset_id": "D1",
        "dependence_id": "DEP1",
        "plant_taxon": "Plant a",
        "animal_taxon": "Animal a",
        "interaction_type": "mutualist",
        "evidence_tier": "A",
        "phenology_source": "direct_interaction",
        "timing_metric_type": "overlap_index",
        "timing_analysis_class": "strict_window",
        "timing_domain": "nonnegative",
        "exposure_direction": "synchrony",
        "outcome_family": "seed_set",
        "effect_family": "standardized_slope",
        "effect_native": 0.2,
        "variance_native": 0.04,
        "sample_size": 30,
        "source_id": "doi:test",
    }
    row.update(overrides)
    return row


def test_valid_row_has_no_errors():
    assert validate_effect_rows(pd.DataFrame([_row()])) == []


def test_tier_c_is_excluded_from_primary_dataset():
    df = pd.DataFrame(
        [
            _row(effect_id="A", evidence_tier="A"),
            _row(
                effect_id="C",
                evidence_tier="C",
                phenology_source="occurrence_proxy",
                timing_analysis_class="proxy_only",
            ),
        ]
    )
    out = build_primary_dataset(df)
    assert list(out["effect_id"]) == ["A"]


def test_missing_variance_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(variance_native=None)]))
    assert any("variance_native" in error for error in errors)


def test_duplicate_effect_id_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(), _row()]))
    assert any("duplicate effect_id" in error for error in errors)


def test_unknown_interaction_type_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(interaction_type="commensal")]))
    assert any("interaction_type" in error for error in errors)


def test_missing_timing_metric_type_column_fails_validation():
    df = pd.DataFrame([_row()]).drop(columns=["timing_metric_type"])
    errors = validate_effect_rows(df)
    assert any("timing_metric_type" in error for error in errors)


def test_unknown_timing_metric_type_fails_validation():
    errors = validate_effect_rows(pd.DataFrame([_row(timing_metric_type="generic_mismatch")]))
    assert any("timing_metric_type" in error for error in errors)


def test_strict_signed_lag_requires_one_sided_domain():
    errors = validate_effect_rows(
        pd.DataFrame(
            [
                _row(
                    timing_metric_type="partner_minus_plant",
                    timing_domain="unknown",
                    exposure_direction="mismatch",
                )
            ]
        )
    )
    assert any("one-sided timing_domain" in error for error in errors)


def test_strict_signed_lag_rejects_both_sides_domain():
    errors = validate_effect_rows(
        pd.DataFrame(
            [
                _row(
                    timing_metric_type="plant_minus_partner",
                    timing_domain="both_sides",
                    exposure_direction="mismatch",
                )
            ]
        )
    )
    assert any("one-sided timing_domain" in error for error in errors)


def test_signed_lag_direction_is_derived_from_metric_and_domain():
    row = _row(
        timing_metric_type="partner_minus_plant",
        timing_domain="plant_earlier_only",
        exposure_direction="mismatch",
    )
    assert validate_effect_rows(pd.DataFrame([row])) == []


def test_wrong_signed_lag_orientation_fails_validation():
    errors = validate_effect_rows(
        pd.DataFrame(
            [
                _row(
                    timing_metric_type="plant_minus_partner",
                    timing_domain="plant_earlier_only",
                    exposure_direction="mismatch",
                )
            ]
        )
    )
    assert any("exposure_direction=synchrony" in error for error in errors)


def test_unresolved_signed_lag_is_not_admitted_to_strict_primary():
    df = pd.DataFrame(
        [
            _row(
                timing_metric_type="partner_minus_plant",
                timing_analysis_class="unresolved_for_strict_h1",
                timing_domain="unknown",
                exposure_direction="mismatch",
            )
        ]
    )
    out = build_primary_dataset(df)
    assert out.empty


def test_direct_timing_sensitivity_is_not_admitted_to_strict_primary():
    df = pd.DataFrame(
        [
            _row(
                phenology_source="experimental_timing",
                timing_metric_type="experimental_plant_shift",
                timing_analysis_class="direct_timing_sensitivity",
                timing_domain="not_applicable",
                exposure_direction="mismatch",
            )
        ]
    )
    out = build_primary_dataset(df)
    assert out.empty


def test_mismatch_is_oriented_in_primary_dataset():
    out = build_primary_dataset(
        pd.DataFrame(
            [
                _row(
                    timing_metric_type="absolute_mismatch",
                    timing_domain="nonnegative",
                    exposure_direction="mismatch",
                    effect_native=0.3,
                )
            ]
        )
    )
    assert out.iloc[0]["effect_oriented"] == -0.3
