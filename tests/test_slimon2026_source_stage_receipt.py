"""Actual source-stage inventory cannot become a strict antagonist effect."""
import pandas as pd
from pathlib import Path


SOURCE = "data/source_reconstructions/slimon2026_original_focal_stage_observations.csv"


def test_exp1_source_adult_counts_are_sparse_direct_focal_host_detections():
    rows = pd.read_csv(SOURCE)
    adult = rows.loc[rows.source_component.eq("focal_host_adult_schinia")]
    assert len(adult) == 6
    assert (adult.experiment == "exp1").all()
    assert set(adult.flowering_calendar_year) == {2023}
    assert adult.sum_reported_events.sum() == 18
    assert adult.positive_rows.sum() == 12  # repeat appearances across dates
    assert set(adult.nonmissing_numeric_observations) == {169}
    assert set(adult.shared_host_stage_fruit_ids) == {153}
    assert set(adult.observed_event_date) == {
        "07-11", "07-12", "07-18", "07-20", "07-21", "07-26"
    }


def test_exp2_has_larval_only_window_and_no_fake_adult_or_seed_finality():
    rows = pd.read_csv(SOURCE)
    exp2 = rows.loc[rows.experiment.eq("exp2")]
    assert len(exp2) == 1
    assert exp2.iloc[0].flowering_calendar_year == 2023
    assert exp2.iloc[0].source_component == "focal_host_larval_schinia_only"
    assert exp2.iloc[0].distinct_plant_ids == 123
    assert exp2.iloc[0].source_rows == 951
    assert rows.adult_host_activity_independent_of_host_sampling_verified.eq("no").all()
    assert rows.direct_postcost_intact_seed_counts_verified.eq("no").all()
    assert rows.strict_h1_effect.eq("no").all()


def test_source_method_audit_records_provenance_assumptions_explicitly():
    doc = Path("docs/SLIMON2026_WINDOW_EDGE_CANCELLATION_SOURCE_AUDIT.md").read_text()
    for phrase in (
        "fitness_frt", "fitness_seed", "0.2", "genotype-specific",
        "not admitted", "focal-host conditional", "2023",
    ):
        assert phrase in doc
    extracted = pd.read_csv("data/extraction/direct_effects.csv")
    assert "PIVOT_SLIMON2026" not in set(extracted.study_id)
