"""Original source new/old Mompha receipt prevents phantom plants and fitness."""
from pathlib import Path
import pandas as pd

GRAIN="data/source_reconstructions/slimon2026_new_old_mompha_grain.csv"
RESULT="data/source_reconstructions/slimon2026_new_old_mompha_original_stage.csv"


def test_stage_grain_rejects_828_phantom_exp2_independent_plants():
    a=pd.read_csv(GRAIN).set_index(["experiment","record_type"])
    assert len(a)==4
    assert set(a.original_year)=={2023}
    assert a.loc[("exp2","old_Mompha"),"original_rows"]==951
    assert a.loc[("exp2","old_Mompha"),"rows_with_original_plant_id"]==123
    assert a.loc[("exp2","old_Mompha"),"rows_without_original_plant_id"]==828
    assert a.loc[("exp2","old_Mompha"),"unkeyed_rows_with_numeric_stage_values"]==0
    assert a.loc[("exp2","old_Mompha"),"unkeyed_rows_with_positive_stage_values"]==0
    assert a.loc[("exp2","old_Mompha"),"unkeyed_rows_with_nonempty_other_metadata"]==0
    assert a.repeated_original_plant_ids.eq(0).all()
    assert a.source_stage_join_admissible.eq("yes").all()
    assert a.strict_h1_effect.eq("no").all()


def test_new_to_old_stage_result_bounded_and_not_marked_individual_insects():
    d=pd.read_csv(RESULT).set_index("experiment")
    assert set(d.index)=={"exp1","exp2"}
    assert (d.old_t_plus7_positive_new_t_positive
            +d.old_t_plus7_positive_new_t_zero
            ==d.old_at_t_plus_7_positive_pairs).all()
    for exp in ("exp1","exp2"):
        x=d.loc[exp]
        p=x.old_t_plus7_positive_new_t_positive/x.new_at_t_positive_pairs
        q=x.old_t_plus7_positive_new_t_zero/x.new_t_zero_pairs
        assert p>q
        assert x.joint_fe_new_t_slope>0
    assert d.observed_mature_intact_seeds.eq("no").all()
    assert d.known_individual_stage_transition.eq("no").all()
    assert d.strict_h1_effect.eq("no").all()
    assert not pd.read_csv("data/extraction/direct_effects.csv").study_id.astype(str).str.contains(
        "SLIMON",case=False
    ).any()


def test_document_never_promotes_gall_visibility_to_oviposition_date():
    report=Path("docs/SLIMON2026_NEW_OLD_STAGE_PROVENANCE_20261011.md").read_text(
        encoding="utf-8"
    )
    normalized=" ".join(report.lower().split())
    for phrase in (
        "828 additional rows", "not 828 additional",
        "new mompha", "old mompha", "original plant",
        "individually linked", "cannot", "strict-h1"
    ):
        assert phrase in normalized
