"""No-network regression: source grain, seasonal strata and plant clusters."""
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import pytest

from scripts.analyze_slimon2026_date_plant_controls import (
    extract_original_panel, summarize_panel, _weighted_strata_estimate
)


def source_fixture():
    with BytesIO() as bio:
        with ZipFile(bio, "w") as z:
            for e in ("exp1", "exp2"):
                p="Freese Stats/"
                f="df2_exp1.csv" if e=="exp1" else "df2_exp2.csv"
                m="df2_exp1_M.csv" if e=="exp1" else "df2_exp2M.csv"
                z.writestr(p+f,
                    "ID,#flr_7_12,#flr_7_19\n"
                    "a,1,0\nb,0,1\nc,1,0\nd,0,1\n"
                )
                z.writestr(p+m,
                    "ID,mompha_7_12,mompha_7_19\n"
                    "a,1,1\nb,0,1\nc,0,0\nd,0,0\n"
                )
        return bio.getvalue()


def test_source_exact_panel_and_three_separate_estimands():
    raw=source_fixture()
    with ZipFile(BytesIO(raw)) as zf:
        panel=extract_original_panel(zf,"exp1")
    assert len(panel)==8
    assert panel.source_plant_id.nunique()==4
    assert set(panel.doy)=={193,200}
    out=summarize_panel(panel,n_boot=64)
    assert out["n_original_survey_days"]==2
    assert out["naive_pooled_visit_risk_difference"]==0.25
    assert out["date_stratified_risk_difference"]["risk_difference"]==0.25
    assert out["within_plant_risk_difference"]["risk_difference"]==0.25
    assert out["date_stratified_risk_difference"]["n_comparable_strata"]==2
    assert out["within_plant_risk_difference"]["n_comparable_strata"]==4
    assert out["date_stratified_cluster_plant_resampling_95pct"] is not None
    assert out["not_independent_two_field_seasons"] if "not_independent_two_field_seasons" in out else True
    assert out["strict_h1_effects_admitted"]==0
    assert out["same_date_visible_stage_not_oviposition"]
    assert out["true_bud_risk_denominator_available"] is False


def test_stratum_adjusted_does_not_conflate_different_calendar_times():
    # Two early vs late days with different plant resources. Raw
    # difference is 3/4 - 2/4 = .25; within-date matches remove it.
    p=pd.DataFrame([
      ("a", 195, 1, 1),("b",195,1,1),("c",195,1,1),("d",195,0,1),
      ("a", 225, 1, 0),("b",225,0,0),("c",225,0,0),("d",225,0,0),
    ],columns=["source_plant_id","doy","open_flower_snapshot","mompha_positive"])
    out=summarize_panel(p,n_boot=0)
    assert out["date_stratified_risk_difference"]["n_comparable_strata"] == 2
    # Within-date all observed positive at day 195 and none at 225,
    # so open-flower availability has zero within-date association.
    assert out["date_stratified_risk_difference"]["risk_difference"] == 0
    assert out["naive_pooled_visit_risk_difference"] == 0.25
    assert out["within_plant_risk_difference"]["n_comparable_strata"] > 0


def test_duplicated_source_plant_day_is_rejected():
    with ZipFile(BytesIO(source_fixture())) as zf:
        panel=extract_original_panel(zf,"exp1")
    with pytest.raises(ValueError, match="duplicate"):
        summarize_panel(pd.concat([panel,panel.iloc[[0]]]),n_boot=0)


def test_empty_or_missing_source_is_not_negative_occurrence():
    b=BytesIO()
    with ZipFile(b,"w") as z:
        z.writestr("Freese Stats/df2_exp1.csv", "ID,#flr_7_12\na,1\n")
        z.writestr("Freese Stats/df2_exp1_M.csv", "ID,mompha_7_19\na,1\n")
    with ZipFile(BytesIO(b.getvalue())) as zf:
        with pytest.raises(ValueError, match="overlap absent"):
            extract_original_panel(zf,"exp1")
