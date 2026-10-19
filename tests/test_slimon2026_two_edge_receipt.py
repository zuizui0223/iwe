"""Two-edge original-data receipt is non-promoting and calendar-correct."""
import pandas as pd

SOURCE = "data/source_reconstructions/slimon2026_two_edge_observed_component_associations.csv"


def test_source_fitness_is_not_invented_and_both_experiments_flowered_2023():
    df = pd.read_csv(SOURCE)
    assert len(df) == 4
    assert set(df.experiment) == {"exp1", "exp2"}
    assert set(df.flowering_calendar_year) == {2023}
    assert set(df.phenology_axis) == {"first_doy", "last_doy"}
    assert df.original_intact_mature_seed_count_verified.eq("no").all()
    assert df.independent_partner_activity_verified.eq("no").all()
    assert df.strict_h1_effect.eq("no").all()


def test_original_within_experiment_counts_and_directional_patterns():
    df = pd.read_csv(SOURCE).set_index(["experiment", "phenology_axis"])
    assert df.loc[("exp1", "first_doy"), "n_four_file_plant_join"] == 148
    assert df.loc[("exp2", "last_doy"), "n_four_file_plant_join"] == 123
    first = df.xs("first_doy", level="phenology_axis")
    assert first.mompha_count_spearman_rho.between(0, 0.1).all()
    assert first.mompha_share_proxy_spearman_rho.gt(0.28).all()
    assert first.conditional_mompha_share_partial_rank_rho.gt(0.18).all()
    assert first.raw_large_fruit_spearman_rho.lt(-0.4).all()
    last = df.xs("last_doy", level="phenology_axis")
    assert last.raw_large_fruit_spearman_rho.gt(0.2).all()
    assert last.loc["exp1", "mompha_share_proxy_spearman_rho"] < 0
    assert last.loc["exp2", "mompha_share_proxy_spearman_rho"] > 0.4
    assert df.conditional_rank_n.le(df.n_four_file_plant_join).all()


def test_receipt_is_not_an_added_strict_effect_or_another_year():
    df = pd.read_csv("data/extraction/direct_effects.csv")
    assert not df.study_id.astype(str).str.contains("SLIMON", case=False).any()
    report = open("docs/SLIMON2026_TWO_EDGE_RAW_REANALYSIS_20261009.md", encoding="utf-8").read()
    assert "not 2022 and 2023 annual replication" in report
    assert "not an individually observed" in report
