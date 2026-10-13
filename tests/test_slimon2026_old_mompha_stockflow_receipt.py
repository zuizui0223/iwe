"""Source-backed new/old Mompha damage-stock arithmetic receipt is not H1."""
from pathlib import Path
import pandas as pd

CSV="data/source_reconstructions/slimon2026_old_mompha_stock_flow.csv"


def test_nontrivial_observation_arithmetic_not_majority_identity():
    d=pd.read_csv(CSV).set_index("experiment")
    assert set(d.index)=={"exp1","exp2"}
    assert set(d.flowering_year)=={2023}
    for exp, n, active, matches in (
        ("exp1",795,571,196),("exp2",641,341,82)
    ):
        row=d.loc[exp]
        assert row.numeric_consecutive_plant_weeks==n
        assert row.nontrivial_stage_weeks==active
        assert row.old_t_plus7_eq_old_t_plus_new_t_nontrivial_pairs==matches
        assert row.all_zero_new_old_stage_weeks+active==n
        assert abs(row.stockflow_identity_fraction_nontrivial-matches/active)<1e-6
        assert row.stockflow_identity_fraction_nontrivial<0.35
        assert row.stockflow_identity_fraction_nontrivial<(
            row.stockflow_identity_fraction_all_pairs
        )
    assert d.loc["exp1","sum_change_in_old_counts"]==47
    assert d.loc["exp2","sum_change_in_old_counts"]==-50


def test_original_R_tissue_stage_semantics_and_nonpromotion_are_pinned():
    d=pd.read_csv(CSV)
    assert d.source_R_gall_and_desiccated_bud_definitions_verified.eq("yes").all()
    assert d.individually_tracked_moths.eq("no").all()
    assert d.independent_moth_adult_window.eq("no").all()
    assert d.original_postlarval_intact_seeds.eq("no").all()
    assert d.strict_h1_effect.eq("no").all()
    text=Path(
        "docs/SLIMON2026_OLD_MOMPHA_STOCK_FLOW_AUDIT_20261013.md"
    ).read_text(encoding="utf-8").lower()
    normalized=" ".join(text.split())
    for term in (
        "desiccated flower-bud count",
        "field gall count",
        "trivial zero records",
        "not an exact cumulative",
        "strict h1 unchanged",
    ):
        assert term in normalized
    correction=Path(
        "docs/SLIMON2026_NEW_OLD_STAGE_PROVENANCE_20261011.md"
    ).read_text(encoding="utf-8").lower()
    assert "correction after original-r-code review" in correction
    effects=pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.study_id.astype(str).str.contains(
        "SLIMON",case=False
    ).any()
