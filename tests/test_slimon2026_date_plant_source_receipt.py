"""Source-grounded 2023 contrasts must never enter strict H1 extraction."""
from pathlib import Path

import pandas as pd

DATA = "data/source_reconstructions/slimon2026_date_plant_stage_confounding.csv"


def test_both_original_experiments_one_year_and_original_visit_denominators():
    x = pd.read_csv(DATA).set_index("experiment")
    assert set(x.index) == {"exp1", "exp2"}
    assert set(x.flowering_year) == {2023}
    assert x.loc["exp1", "n_plants"] == 150
    assert x.loc["exp1", "n_matched_plant_visits"] == 1470
    assert x.loc["exp2", "n_plants"] == 123
    assert x.loc["exp2", "n_matched_plant_visits"] == 987
    assert (
        x.open_flower_n + x.no_open_flower_n
        == x.n_matched_plant_visits
    ).all()
    assert (x.bootstrap_original_plants_n == 400).all()


def test_seasonal_and_plant_controls_not_equivalent():
    x = pd.read_csv(DATA).set_index("experiment")
    for exp in ["exp1", "exp2"]:
        row = x.loc[exp]
        observed_diff = (row.open_flower_mompha_positive / row.open_flower_n
                         - row.no_open_flower_mompha_positive / row.no_open_flower_n)
        assert abs(observed_diff - row.pooled_positivity_difference) < 1e-6
        assert row.date_matched_difference > 0
        assert row.within_plant_difference > 0
        assert row.within_plant_difference < row.date_matched_difference
        assert row.plant_resample_interval_low <= row.within_plant_difference
        assert row.plant_resample_interval_high >= row.within_plant_difference
    assert x.loc["exp1", "plant_resample_interval_low"] > 0
    assert x.loc["exp2", "plant_resample_interval_low"] < 0


def test_source_emphasis_is_detection_not_oviposition_or_mature_seeds():
    x = pd.read_csv(DATA)
    assert x.experimental_year_replicate.eq("no").all()
    assert x.independent_mompha_adult_availability.eq("no").all()
    assert x.observed_direct_mature_intact_seed_fitness.eq("no").all()
    assert x.strict_h1_admission.eq("no").all()
    notes = Path(
        "docs/SLIMON2026_DATE_VS_PLANT_STAGE_CONTROL_20261010.md"
    ).read_text(encoding="utf-8")
    for token in (
        "same-date", "2.5–97.5", "not a joint fixed-effect model",
        "149/1,468", "buds and oviposition"
    ):
        assert token in notes
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.study_id.astype(str).str.contains("SLIMON").any()
