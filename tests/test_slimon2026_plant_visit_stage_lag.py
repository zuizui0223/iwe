"""Never infer oviposition from matched flower and new Mompha observations."""
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts.analyze_slimon2026_plant_visit_stage_lag import (
    audit_experiment, original_id_map, survey_dates
)


def _source_zip(*, duplicate_id=False):
    b=BytesIO()
    with ZipFile(b,"w") as z:
        root="Freese Stats/"
        flower_header="ID,#flr_7_12,#flr_7_19,#_flr_7_26\n"
        flower_rows="a,3,0,0\nb,0,4,0\n"
        if duplicate_id:
            flower_rows+="a,2,0,0\n"
        mompha_header="ID,mompha_7_12,mompha_7_19,mompha_7_26\n"
        mompha_rows="a,0,1,2\nb,1,2,0\n"
        for exp in ("exp1","exp2"):
            z.writestr(root+("df2_exp1.csv" if exp=="exp1" else "df2_exp2.csv"),
                       flower_header+flower_rows)
            z.writestr(root+("df2_exp1_M.csv" if exp=="exp1" else "df2_exp2M.csv"),
                       mompha_header+mompha_rows)
            z.writestr(root+("main_exp1.csv" if exp=="exp1" else "main_exp2.csv"),
                       "ID,first_flr\na,7/12/23\nb,7/19/23\n")
            z.writestr(root+("d_pheno.csv" if exp=="exp1" else "d_pheno_exp2.csv"),
                       "ID,last_flower\na,7/20/23\nb,7/26/23\n")
    return b.getvalue()


def test_exact_same_plant_date_stage_detects_mompha_without_open_flower():
    with ZipFile(BytesIO(_source_zip())) as zf:
        first=audit_experiment(zf,"exp1")
        second=audit_experiment(zf,"exp2")
    for x in (first,second):
        assert x["source_shared_plant_ids"]==2
        assert x["n_exact_same_dates"]==3
        assert x["n_matched_plant_visits"]==6
        assert x["strict_h1_effects_admitted"]==0
        assert x["mompha_new_visible_stage_is_not_oviposition_or_adult_flight"]
        visits={v["survey_date"]:v for v in x["exact_date_survey_results"]}
        assert visits["2023-07-12"]["n_mompha_positive_without_open_flower"]==1
        assert visits["2023-07-26"]["n_mompha_positive_without_open_flower"]==1
        assert visits["2023-07-26"]["n_mompha_positive_events_outside_recorded_window"]==2
        assert sum(v["n_paired_plants"] for v in x["exact_date_survey_results"])==6
        assert x["per_plant_flower_mompha_spearman"] if "per_plant_flower_mompha_spearman" in x else True


def test_duplicate_ids_and_ambiguous_date_fields_are_not_merged():
    with ZipFile(BytesIO(_source_zip(duplicate_id=True))) as zf:
        with pytest.raises(ValueError,match="duplicate original plant ID"):
            audit_experiment(zf,"exp1")
    with pytest.raises(ValueError,match="duplicate source survey day"):
        survey_dates([{"ID":"a","#flr_7_12":"1","flr_7_12":"1"}],"flowers")
    assert survey_dates([{"ID":"b","#_flr_7_26":"5"}],"flowers")


def test_2023_only_date_labels_no_2022_annual_replication():
    with ZipFile(BytesIO(_source_zip())) as zf:
        data=audit_experiment(zf,"exp1")
    assert data["flowering_calendar_year"]==2023
    assert data["mompha_new_visible_stage_is_not_oviposition_or_adult_flight"]
    assert data["mature_intact_seed_n_not_measured"]
