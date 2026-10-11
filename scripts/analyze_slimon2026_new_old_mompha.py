"""Original 2023 Oenothera new/old Mompha stage audit, no fitness inference.

The Zenodo source has 159 exp1 "old Mompha" rows but 951 exp2
rows, compared with 123 exp2 "new Mompha" rows. Do not assume
repeated old rows are independent plant units or average them.
If old stage is uniquely keyed by the *original source plant ID*,
test whether new observed Mompha at t is associated with old observed
Mompha at t+7, with exact date and plant identity controls.

"New" and "old" are the author's recorded stage labels; this
does not track an individual moth or prove stage maturation.
"""
from __future__ import annotations

import argparse
from datetime import date
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile

import numpy as np
import pandas as pd

from scripts.analyze_slimon2026_date_plant_controls import _pinned_zip_bytes
from scripts.analyze_slimon2026_window_edges import _load_rows, _num, EXPECTED_ZIP_MD5
from scripts.analyze_slimon2026_joint_fe_weeklag import _weighted_fe_fit
from scripts.probe_slimon2026_zenodo_source import DOI

YEAR = 2023
SOURCE = {
    "exp1": {
        "new": "Freese Stats/df2_exp1_M.csv",
        "old": "Freese Stats/df2_exp1OM.csv",
    },
    "exp2": {
        "new": "Freese Stats/df2_exp2M.csv",
        "old": "Freese Stats/df2_exp2OM.csv",
    },
}
PREFIX = {"new": "mompha", "old": "OLDmompha"}


def _dated_columns(rows: list[dict], stage: str) -> dict[int, str]:
    if not rows:
        raise ValueError("no original stage records")
    prefix = PREFIX[stage]
    matcher = re.compile(r"^" + re.escape(prefix) + r"_(\d{1,2})_(\d{1,2})$",re.I)
    out = {}
    for column in rows[0]:
        matched = matcher.match(column)
        if matched is None:
            continue
        try:
            day = date(YEAR,int(matched.group(1)),int(matched.group(2))).timetuple().tm_yday
        except ValueError as exc:
            raise ValueError(f"invalid original {stage} survey date {column}") from exc
        if day in out:
            raise ValueError(f"duplicate original survey date {stage}: {day}")
        out[day] = column
    if not out:
        raise ValueError(f"no source-dated {stage} Mompha measurements")
    return out


def stage_grain(rows: list[dict], stage: str) -> dict:
    day_fields = _dated_columns(rows,stage)
    keyed = [row for row in rows
             if str(row.get("ID") or "").strip() not in ("","NA","NaN")]
    if not keyed:
        raise ValueError("original stage has no source plant IDs")
    # A large export may contain rows with no original plant key.
    # These are NEVER added as independent plants or silently mapped
    # to another plant. Determine whether they contain observed stage
    # values before any coverage claim about the original population.
    unkeyed = [row for row in rows
               if str(row.get("ID") or "").strip() in ("", "NA", "NaN")]
    stage_cells_present = 0
    unkeyed_positive_rows = 0
    unkeyed_nonmissing_stage_rows = 0
    unkeyed_nonempty_auxiliary_rows = 0
    for row in unkeyed:
        present = False
        positive = False
        for col in day_fields.values():
            val = _num(row.get(col))
            if np.isfinite(val):
                present = True
                stage_cells_present += 1
                if val > 0:
                    positive = True
        if present:
            unkeyed_nonmissing_stage_rows += 1
        if positive:
            unkeyed_positive_rows += 1
        if any(str(val or "").strip() not in ("","NA","NaN")
               for col,val in row.items()
               if col not in day_fields.values() and col != "ID"):
            unkeyed_nonempty_auxiliary_rows += 1
    by_id: dict[str,list[dict]] = {}
    for row in keyed:
        by_id.setdefault(str(row["ID"]).strip(), []).append(row)
    duplicates = {id_: len(g) for id_,g in by_id.items() if len(g)>1}
    variable_repeats = 0
    repeated_identical = 0
    for group in by_id.values():
        if len(group) < 2:
            continue
        patterns = {
            tuple(str(row.get(k,"")).strip() for k in day_fields.values())
            for row in group
        }
        if len(patterns)>1:
            variable_repeats += 1
        else:
            repeated_identical += 1
    return {
        "original_row_count":len(rows),
        "source_rows_with_plant_id":len(keyed),
        "unique_original_plant_ids":len(by_id),
        "source_rows_without_original_plant_id":len(unkeyed),
        "unkeyed_rows_with_any_numeric_stage_value":unkeyed_nonmissing_stage_rows,
        "unkeyed_rows_with_positive_stage_value":unkeyed_positive_rows,
        "unkeyed_numeric_stage_cells":stage_cells_present,
        "unkeyed_rows_with_nonempty_auxiliary_fields":unkeyed_nonempty_auxiliary_rows,
        "repeated_id_count":len(duplicates),
        "repeated_id_rows":sum(n-1 for n in duplicates.values()),
        "max_original_rows_per_plant":max(len(v) for v in by_id.values()),
        "repeated_ids_with_different_stage_profiles":variable_repeats,
        "repeated_ids_with_identical_stage_profiles":repeated_identical,
        "source_dated_stage_columns":len(day_fields),
        "original_stage_calendar_days":sorted(day_fields),
        "safe_unique_plant_grain_for_exact_join":not duplicates,
        "do_not_arbitrarily_average_or_sum_duplicate_old_rows":True,
    }


def _safe_unique_map(rows: list[dict], stage: str) -> dict[str,dict]:
    by_id={}
    for row in rows:
        key=str(row.get("ID") or "").strip()
        if not key or key.upper() in {"NA","NAN","NULL"}:
            continue
        if key in by_id:
            raise ValueError(f"duplicate source plant ID for {stage}; cannot infer unit")
        by_id[key]=row
    return by_id


def paired_source_stage_panel(new: list[dict], old: list[dict]) -> pd.DataFrame:
    if not stage_grain(old,"old")["safe_unique_plant_grain_for_exact_join"]:
        raise ValueError("old stage has duplicated plant IDs; require original biological grain")
    if not stage_grain(new,"new")["safe_unique_plant_grain_for_exact_join"]:
        raise ValueError("new stage has duplicated plant IDs; require original biological grain")
    day_new=_dated_columns(new,"new")
    day_old=_dated_columns(old,"old")
    common=sorted(set(day_new)&set(day_old))
    day_pair=sorted(d for d in common if (d+7) in common)
    if not day_pair:
        raise ValueError("no exact weekly observations of both source stages")
    by_new=_safe_unique_map(new,"new")
    by_old=_safe_unique_map(old,"old")
    overlap=sorted(set(by_new)&set(by_old))
    if not overlap:
        raise ValueError("no identical original plant IDs shared across stages")
    output=[]
    for id_ in overlap:
        for day in day_pair:
            nv=_num(by_new[id_].get(day_new[day]))
            ov=_num(by_old[id_].get(day_old[day]))
            nf=_num(by_new[id_].get(day_new[day+7]))
            of=_num(by_old[id_].get(day_old[day+7]))
            if not all(np.isfinite(x) for x in (nv,ov,nf,of)):
                continue
            if any(x<0 or x%1!=0 for x in (nv,ov,nf,of)):
                raise ValueError("source original Mompha stage count is invalid")
            output.append({
                "source_plant_id":id_,
                "doy":day,
                "mompha_positive":int(of>0),  # old at t+7
                "new_today":int(nv>0),
                "old_today":int(ov>0),
                "new_following_week":int(nf>0),
                "new_count_today":float(nv),
                "old_count_following_week":float(of),
            })
    data=pd.DataFrame(output)
    if data.empty or data.duplicated(["source_plant_id","doy"]).any():
        raise ValueError("original stage panel has no unique plant/date unit")
    return data


def diagnostic(new: list[dict],old: list[dict]) -> dict:
    gn=stage_grain(new,"new")
    go=stage_grain(old,"old")
    result={
        "new_source_grain":gn,
        "old_source_grain":go,
        "source_new_old_stage_labels_not_individual_moth_tracking":True,
        "stage_estimates_source_scope":"original_plant_id_keyed_complete_case_only",
        "real_oviposition_date_identified":False,
        "source_bud_abundance_identified":False,
        "strict_h1_effects_admitted":0,
    }
    if not gn["safe_unique_plant_grain_for_exact_join"] or not go[
        "safe_unique_plant_grain_for_exact_join"
    ]:
        result["stage_transition_status"]="blocked_nonunique_original_stage_grain"
        result["biological_stage_coefficients"]=None
        return result
    data=paired_source_stage_panel(new,old)
    result.update({
        "stage_transition_status":"plant_and_exact_calendar_day_matched",
        "n_source_plants":int(data.source_plant_id.nunique()),
        "n_original_matched_plant_date_pairs":len(data),
        "n_original_survey_days":int(data.doy.nunique()),
        "new_today_positive":int(data.new_today.sum()),
        "old_today_positive":int(data.old_today.sum()),
        "old_following_week_positive":int(data.mompha_positive.sum()),
        "new_following_week_positive":int(data.new_following_week.sum()),
    })
    basic=data.groupby("new_today").agg(
        n=("mompha_positive","size"),
        old_following_positive=("mompha_positive","sum")
    )
    result["observed_old_following_week_by_prior_new"]={
        str(idx):{"plant_visits":int(row["n"]),
                  "old_positive_next_week":int(row["old_following_positive"])}
        for idx,row in basic.iterrows()
    }
    if (data.mompha_positive.nunique()>1 and
        data.new_today.nunique()>1 and
        data.source_plant_id.nunique()>=8 and
        data.doy.nunique()>=3):
        models={
            "new_today_only":["new_today"],
            "old_today_only":["old_today"],
            "current_new_and_old":["new_today","old_today"],
            "joint_with_next_week_new":["new_today","old_today","new_following_week"],
        }
        baseline=_weighted_fe_fit(data,[])
        fitted={}
        for key,axes in models.items():
            z=_weighted_fe_fit(data,axes)
            fitted[key]={
                "source_coefficients":{
                    k:round(float(v),6) for k,v in z["coefficients"].items()
                },
                "additional_in_sample_twfe_r2":(
                    round(1-z["rss"]/baseline["rss"],6)
                    if baseline["rss"]>1e-8 else None
                )
            }
        result["biological_stage_coefficients"]=fitted
    else:
        result["biological_stage_coefficients"]=None
        result["stage_fit_hold"]="too_little_outcome_or_source_stage_variation"
    return result


def run(outdir:Path):
    original=_pinned_zip_bytes()
    outdir.mkdir(parents=True,exist_ok=True)
    with ZipFile(BytesIO(original)) as z:
        outputs={
            experiment:diagnostic(
                _load_rows(z,files["new"]),
                _load_rows(z,files["old"])
            )
            for experiment,files in SOURCE.items()
        }
    report={
        "schema":"slimon_2026_original_new_old_mompha_grain_v1",
        "source_doi":DOI,
        "source_original_zip_md5":EXPECTED_ZIP_MD5,
        "year_of_original_stage_surveys":YEAR,
        "experiment_results":outputs,
        "not_an_oviposition_to_mature_seed_experiment":True,
        "strict_h1_effects_added":0,
    }
    (outdir/"original_new_old_stage_grain.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    for key, value in outputs.items():
        print("STAGE_ORIGINAL_SOURCE",key,json.dumps(value))
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    args=p.parse_args()
    run(args.outdir)


if __name__=="__main__":
    main()
