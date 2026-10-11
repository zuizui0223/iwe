"""No-network source grain checks for original new/old Mompha observations."""
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import pytest

from scripts.analyze_slimon2026_new_old_mompha import (
    _dated_columns, paired_source_stage_panel, stage_grain, diagnostic
)


def fixture_rows(duplicate_old=False):
    new, old = [], []
    for i in range(25):
        id_=str(i)
        # Include original dates and observable stage variation;
        # planted "old next week" follows prior "new", not an
        # invented literal larval development timing claim.
        new_values=[int((i*3+j*5)%11<5) for j in range(5)]
        old_values=[int((i*3+(j-1)*5)%11<5) if j>0 else 0
                    for j in range(5)]
        nr={"ID":id_}
        orow={"ID":id_}
        for (mm,dd), n, o in zip(
            [(7,12),(7,19),(7,26),(8,2),(8,9)],new_values,old_values
        ):
            nr[f"mompha_{mm}_{dd}"]=str(n)
            orow[f"OLDmompha_{mm}_{dd}"]=str(o)
        new.append(nr)
        old.append(orow)
    if duplicate_old:
        # Repeated source ID is biologically ambiguous; it cannot
        # be averaged or silently treated as independent plants.
        extra=old[0].copy()
        extra["OLDmompha_7_12"]="5"
        old.append(extra)
    return new, old


def test_source_old_and_new_match_only_exact_plant_id_and_date():
    new,old=fixture_rows()
    a,b=stage_grain(new,"new"),stage_grain(old,"old")
    assert a["original_row_count"]==25
    assert b["unique_original_plant_ids"]==25
    assert not b["repeated_id_count"]
    assert len(_dated_columns(old,"old"))==5
    panel=paired_source_stage_panel(new,old)
    assert panel.source_plant_id.nunique()==25
    assert len(panel)==25*4
    assert set(panel.doy)=={193,200,207,214}
    assert panel.old_count_following_week.ge(0).all()
    assert set(panel.mompha_positive).issubset({0,1})


def test_nonunique_old_source_grain_is_explicitly_blocked():
    new,old=fixture_rows(duplicate_old=True)
    x=diagnostic(new,old)
    assert x["old_source_grain"]["original_row_count"]==26
    assert x["old_source_grain"]["unique_original_plant_ids"]==25
    assert x["old_source_grain"]["repeated_ids_with_different_stage_profiles"]==1
    assert x["stage_transition_status"]=="blocked_nonunique_original_stage_grain"
    assert x["biological_stage_coefficients"] is None
    with pytest.raises(ValueError,match="duplicated plant IDs"):
        paired_source_stage_panel(new,old)
    assert x["strict_h1_effects_admitted"]==0


def test_only_source_observed_days_and_no_fake_weekly_zero():
    new,old=fixture_rows()
    for r in new:
        r["mompha_7_19"]=""  # missing is not zero
    panel=paired_source_stage_panel(new,old)
    assert set(panel.doy)=={207,214}
    assert panel.source_plant_id.nunique()==25
    for r in old:
        r.pop("OLDmompha_8_2")
    with pytest.raises(ValueError,match="no exact weekly"):
        # two-stage overlap still 7/12,7/19,7/26,8/9
        # therefore there are still two earlier exact pairs; to
        # exercise the fail gate, retain only disconnected days.
        paired_source_stage_panel(
            [{"ID":"1","mompha_7_12":"1","mompha_7_26":"0"}],
            [{"ID":"1","OLDmompha_7_12":"0","OLDmompha_7_26":"1"}]
        )


def test_source_stage_descriptive_fit_is_not_oviposition():
    new,old=fixture_rows()
    x=diagnostic(new,old)
    assert x["stage_transition_status"]=="plant_and_exact_calendar_day_matched"
    assert x["n_original_matched_plant_date_pairs"]==100
    assert x["biological_stage_coefficients"] is not None
    assert "new_today_only" in x["biological_stage_coefficients"]
    assert "joint_with_next_week_new" in x["biological_stage_coefficients"]
    assert x["real_oviposition_date_identified"] is False
    assert x["source_bud_abundance_identified"] is False
