"""No-network source arithmetic audit: stage stocks are not maturation tracking."""
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts.audit_slimon2026_old_mompha_stockflow import (
    audit_stock_flow, cumulative_input_metadata, audit_archive
)


DATES=[(7,12),(7,19),(7,26),(8,2),(8,9)]


def _stages(mode="carryover",n_plants=14):
    new_rows,old_rows=[],[]
    for i in range(n_plants):
        counts=[int((i+3*j)%5==0) + int((i+2*j)%7==0)
                for j in range(len(DATES))]
        nr={"ID":str(i)}
        old={"ID":str(i)}
        tally=0
        for j,(month,day) in enumerate(DATES):
            nr[f"mompha_{month}_{day}"]=str(counts[j])
            if mode=="carryover":
                old[f"OLDmompha_{month}_{day}"]=str(tally)
            else:
                old[f"OLDmompha_{month}_{day}"]=str((i+2*j)%4)
            tally+=counts[j]
        new_rows.append(nr)
        old_rows.append(old)
    return new_rows,old_rows


def test_literal_old_next_week_equals_old_now_plus_new_now_when_constructed():
    new,old=_stages("carryover")
    x=audit_stock_flow(new,old)
    assert x["status"]=="numeric_stock_flow_compared"
    assert x["source_plants_keyed_in_both_stages"]==14
    assert x["numeric_consecutive_original_plant_weeks"]==14*4
    formula=x["arithmetic_identity_checks"][
        "old_following_equals_old_current_plus_new_current"
    ]
    assert formula["fraction_of_numeric_week_pairs"]==1.0
    assert x["nontrivial_old_next_equals_old_now_plus_new_now"]["share"] == 1.0
    assert x["nontrivial_stage_plant_weeks"] > 0
    assert not x["original_new_old_measurement_independence_verified"]
    assert not x["stock_flow_identity_is_developmental_tracking_evidence"]
    assert x["strict_h1_effects_admitted"]==0


def test_nonstock_old_stage_does_not_force_arithmetic_identity():
    new,old=_stages("independent")
    x=audit_stock_flow(new,old)
    assert x["arithmetic_identity_checks"][
        "old_following_equals_old_current_plus_new_current"
    ]["fraction_of_numeric_week_pairs"]<0.5
    assert x["original_new_old_measurement_independence_verified"] is False


def test_missing_source_count_is_not_automatically_zero():
    new,old=_stages("carryover")
    new[0]["mompha_7_19"]=""
    x=audit_stock_flow(new,old)
    assert x["numeric_consecutive_original_plant_weeks"]==14*4-2
    assert x["arithmetic_identity_checks"][
        "old_following_equals_old_current_plus_new_current"
    ]["fraction_of_numeric_week_pairs"]==1.0


def test_duplicate_source_id_fails_closed_and_original_unkeyed_is_ignored():
    new,old=_stages("carryover")
    old.append(old[0].copy())
    x=audit_stock_flow(new,old)
    assert x["status"]=="blocked_duplicate_biological_plant_ids"
    assert x["numeric_consecutive_original_plant_weeks"]==0
    new,old=_stages("carryover")
    old.append({"ID":"","OLDmompha_7_12":"8"})
    x=audit_stock_flow(new,old)
    assert x["source_old_unkeyed_rows"]==1
    assert x["source_plants_keyed_in_both_stages"]==14
    assert x["strict_h1_effects_admitted"]==0


def test_helper_grain_is_not_assumed_to_be_plant_id():
    b=BytesIO()
    with ZipFile(b,"w") as z:
        z.writestr("Freese Stats/momphaCALC_exp1.csv",
                   "jday,aggregate_mompha\n193,1\n200,3\n")
    with ZipFile(BytesIO(b.getvalue())) as z:
        x=cumulative_input_metadata(z,"exp1")
    assert x["source_rows"]==2
    assert x["source_ids"]==0
    assert x["source_headers"]==["jday","aggregate_mompha"]
    assert x["no_assumption_about_original_bud_or_larva_tracking"]



def test_original_R_comments_support_tissue_stage_not_marked_moth_age():
    from scripts.audit_slimon2026_old_mompha_stockflow import (
        original_R_stage_semantics
    )
    b=BytesIO()
    with ZipFile(b,"w") as z:
        for experiment in ("exp1","exp2"):
            z.writestr(
                f"Freese Stats/{experiment}_time_series.R",
                "# field gall count (mompha) and the desiccated bud count (OLDmompha), then\n"
            )
    with ZipFile(BytesIO(b.getvalue())) as source:
        result=original_R_stage_semantics(source)
    for item in result.values():
        assert item[
            "original_R_calls_mompha_field_gall_and_oldmompha_desiccated_bud"
        ]
        assert item["stage_definition_comment_source_line_numbers"] == [1]
        assert item["authoritative_individual_moth_age_observed"] is False
