"""2023 original same-plant/same-visit bud-borer evidence, no adult-window promotion."""
from pathlib import Path

import pandas as pd

SOURCE = "data/source_reconstructions/slimon2026_exact_plant_visit_mompha_stage.csv"


def test_original_source_stage_rows_sum_to_actual_join_counts():
    df = pd.read_csv(SOURCE)
    assert len(df) == 7
    assert set(df.flowering_calendar_year) == {2023}
    assert set(df.experiment) == {"exp1", "exp2"}
    assert (df.strict_h1_effect == "no").all()
    for exp, expected_plants, dates, visits in (
        ("exp1", 149, 11, 1468),
        ("exp2", 123, 9, 987),
    ):
        sub = df.loc[df.experiment == exp]
        assert set(sub.shared_source_plants) == {expected_plants}
        assert set(sub.common_survey_dates) == {dates}
        assert set(sub.paired_plant_visits) == {visits}
        assert sub.phase_plant_visits.sum() == visits
        assert sub.mompha_positive_plant_visits.sum() <= visits
    assert "missing_or_invalid_window" in set(
        df[df.experiment == "exp2"].relative_to_observed_flowering
    )


def test_bud_stage_detection_is_not_adult_oviposition_date():
    rows = pd.read_csv(SOURCE).set_index(
        ["experiment", "relative_to_observed_flowering"]
    )
    assert rows.loc[("exp1", "before_first_recorded_flower"),
                    "mompha_positive_plant_visits"] == 1
    assert rows.loc[("exp2", "before_first_recorded_flower"),
                    "mompha_positive_plant_visits"] == 28
    assert rows.loc[("exp2", "before_first_recorded_flower"),
                    "sum_new_mompha_observations"] == 74
    assert rows.loc[("exp1", "within_recorded_flower_window"),
                    "mompha_positive_visits_zero_open_flower"] == 290
    assert rows.loc[("exp2", "within_recorded_flower_window"),
                    "mompha_positive_visits_zero_open_flower"] == 156
    assert rows.loc[("exp1", "after_last_recorded_flower"),
                    "mompha_positive_plant_visits"] == 0
    assert rows.loc[("exp2", "after_last_recorded_flower"),
                    "mompha_positive_plant_visits"] == 0


def test_stage_count_receipt_no_h1_promotion_or_oviposition_inference():
    doc = Path(
        "docs/SLIMON2026_BUD_VS_OPEN_FLOWER_STAGE_AUDIT_20261010.md"
    ).read_text(encoding="utf-8")
    assert "bud" in doc.lower()
    assert "not evidence" in doc
    assert "oviposition" in doc
    assert "Bruzzese et al. (2019)" in doc
    assert "SMD" in doc
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.study_id.astype(str).str.contains("SLIMON", case=False).any()
