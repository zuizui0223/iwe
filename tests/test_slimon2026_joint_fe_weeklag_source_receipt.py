"""Original source stage coefficients are not a strict H1 seed effect."""
from pathlib import Path

import pandas as pd

CSV = "data/source_reconstructions/slimon2026_joint_fe_weeklag_source.csv"


def test_two_original_experiments_are_only_one_2023_source_programme():
    d = pd.read_csv(CSV)
    assert len(d) == 6
    assert set(d.experiment) == {"exp1", "exp2"}
    assert set(d.flowering_calendar_year) == {2023}
    assert set(d.model_exposure) == {
        "prior_open_7d", "current_open", "future_open_7d"
    }
    assert d.strict_h1_effect.eq("no").all()
    assert d.observed_oviposition.eq("no").all()
    assert d.source_bud_denominator.eq("no").all()
    assert d.observed_postlarval_intact_seeds.eq("no").all()
    assert d.experimental_year_replicate.ne("yes").all() if (
        "experimental_year_replicate" in d
    ) else True


def test_source_prior_open_coefficient_largest_in_both_experiments():
    d = pd.read_csv(CSV).set_index(["experiment", "model_exposure"])
    for exp, expected_n, visits, dates in (
        ("exp1", 148, 1055, 8),
        ("exp2", 123, 731, 7)
    ):
        g = d.loc[exp]
        assert set(g.original_unique_plant_ids) == {expected_n}
        assert set(g.exact_triple_window_plant_visits) == {visits}
        assert set(g.source_survey_dates) == {dates}
        past = g.loc["prior_open_7d"]
        current = g.loc["current_open"]
        future = g.loc["future_open_7d"]
        assert past.additive_joint_twfe_slope > current.additive_joint_twfe_slope
        assert past.additive_joint_twfe_slope > future.additive_joint_twfe_slope
        assert past.source_plant_bootstrap_95_low > 0
        assert past.single_axis_vs_fe_incremental_in_sample_r2 > (
            current.single_axis_vs_fe_incremental_in_sample_r2
        )
        assert set(g.bootstrap_replicates) == {160}


def test_ecological_interpretation_explicitly_separates_bud_and_visible_mompha():
    report = Path(
        "docs/SLIMON2026_JOINT_PLANT_DATE_WEEKLAG_AUDIT_20261010.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(report.lower().split())
    for term in (
        "oviposition", "susceptible buds", "complete-case source subset",
        "not two independent", "cannot constitute a clean", "zero strict-h1"
    ):
        assert term.lower() in normalized
    original_effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert not original_effects.study_id.astype(str).str.contains(
        "SLIMON", case=False
    ).any()
