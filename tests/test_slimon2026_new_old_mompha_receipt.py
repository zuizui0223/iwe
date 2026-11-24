"""Original source new/old stage records are exploratory, not marked insect transitions."""
from pathlib import Path
import pandas as pd

CSV="data/source_reconstructions/slimon2026_new_old_mompha_original_stage.csv"


def test_keyed_original_new_old_source_units_are_not_original_row_counts():
    d=pd.read_csv(CSV).set_index("experiment")
    assert set(d.index)=={"exp1","exp2"}
    assert set(d.source_flowering_calendar_year)=={2023}
    assert d.loc["exp1","matched_original_plant_ids"]==153
    assert d.loc["exp1","matched_exact_source_plant_week_pairs"]==795
    assert d.loc["exp2","matched_original_plant_ids"]==122
    assert d.loc["exp2","matched_exact_source_plant_week_pairs"]==641
    assert d.loc["exp2","old_original_rows"]==951
    assert d.loc["exp2","old_original_ids"]==123
    assert d.loc["exp1","old_original_rows"]==159
    assert d.loc["exp1","old_original_ids"]==157


def test_observed_following_week_old_stage_association_both_experiments():
    d=pd.read_csv(CSV)
    assert (d.old_t_plus7_positive_new_t_positive <=
            d.new_at_t_positive_pairs).all()
    assert (d.old_t_plus7_positive_new_t_zero <=
            d.new_t_zero_pairs).all()
    assert (d.old_t_plus7_positive_new_t_positive+
            d.old_t_plus7_positive_new_t_zero ==
            d.old_at_t_plus_7_positive_pairs).all()
    assert (d.new_at_t_positive_pairs+d.new_t_zero_pairs ==
            d.matched_exact_source_plant_week_pairs).all()
    assert d.joint_fe_new_t_slope.gt(0.20).all()
    assert d.joint_fe_old_t_slope.gt(0.17).all()
    assert d.joint_fe_future_new_slope.lt(0).all()
    assert d.strict_h1_effect.eq("no").all()
    assert d.known_individual_stage_transition.eq("no").all()
    assert d.independent_adult_activity_known.eq("no").all()
    assert d.observed_mature_intact_seeds.eq("no").all()
    fx=pd.read_csv("data/extraction/direct_effects.csv")
    assert not fx.study_id.astype(str).str.contains("SLIMON",case=False).any()
