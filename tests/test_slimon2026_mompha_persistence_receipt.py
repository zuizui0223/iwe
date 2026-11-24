"""Source-backed Mompha persistence receipt is one non-promoting programme."""
from pathlib import Path

import pandas as pd


DATA="data/source_reconstructions/slimon2026_prior_mompha_persistence.csv"


def test_2023_experimental_components_not_independent_annual_studies():
    df=pd.read_csv(DATA).set_index("original_experiment")
    assert set(df.index)=={"exp1","exp2"}
    assert set(df.flowering_calendar_year)=={2023}
    assert df.loc["exp1","shared_original_plants"]==148
    assert df.loc["exp2","shared_original_plants"]==123
    assert df.loc["exp1","complete_source_plant_visits"]==1055
    assert df.loc["exp2","complete_source_plant_visits"]==731
    assert set(df.valid_plant_bootstrap_replicates)=={120}


def test_prior_mompha_does_not_erase_prior_flowering_association_in_source():
    df=pd.read_csv(DATA)
    assert df.prior_open_slope_with_prior_mompha.gt(0).all()
    assert (df.prior_open_slope_without_prior_mompha>
            df.prior_open_slope_with_prior_mompha).all()
    assert df.prior_open_plant_bootstrap_low.gt(0).all()
    assert df.prior_mompha_joint_bootstrap_low.gt(0).all()
    assert df.prior_open_log1p_count_joint_slope.gt(0).all()
    assert df.stage_and_flower_fe_r2_in_sample.gt(
        df.flower_only_fe_r2_in_sample
    ).all()


def test_previously_detected_stage_is_not_adult_flight_or_intact_seeds():
    df=pd.read_csv(DATA)
    assert df.original_intact_seed_observed.eq("no").all()
    assert df.original_oviposition_date_observed.eq("no").all()
    assert df.strict_h1_effect.eq("no").all()
    notes=Path(
        "docs/SLIMON2026_PRIOR_MOMPHA_PERSISTENCE_20261011.md"
    ).read_text(encoding="utf-8").lower()
    normalized=" ".join(notes.split())
    for phrase in (
        "not a causal test", "previous observed mompha",
        "source-resampling stability", "bud availability",
        "zero new strict antagonist-h1",
    ):
        assert phrase in normalized
    effects=pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.study_id.astype(str).str.contains(
        "SLIMON",case=False
    ).any()
