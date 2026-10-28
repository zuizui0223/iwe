"""Exploratory 2022 three-species bee-window vs reproductive-stage analysis.

Zenodo 10.5281/zenodo.17830772, exact original MD5.
This is a SECOND cohort (2022) of the same lab/3 species/Osmia as IWE's
2021 source, not taxonomically independent replication.

Fate units: original 208 sampled flower/fruit rows nested inside 120
source parent IDs and 60 species x arena experimental seed-sowing groups.
Germ/cotyl (6 seeds per group) are repeated within 208 fruit rows.
NEVER treat them as 208 independent F1 observations.

Room levels: A, W2, W4, W6; 1 room per temperature, with 5 arenas
per room. Hold out 1 physical arena and its 3 plant species at a time.
This is 20 arena-block internal evaluation, NOT an independently randomized
temperature-effect experiment nor an independent year/site forecast.
The reported seed_set summary disagrees with exact seed/ovule arithmetic
on 31 individual rows. ALWAYS recompute the sampled-fruit fraction from
the original source's self-consistent seeds + undeveloped ovules counts.

All models/weights chosen after original results; exploratory only.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, Counter
from io import BytesIO
import json
from math import isfinite, log1p, sqrt
from pathlib import Path
from statistics import mean
from zipfile import ZipFile

from scripts.probe_demanincor2022_stage_zip import fetch_original
from scripts.audit_demanincor2022_reproduction_units import (
    NAMES, audit_source_tables, numeric, original_table,
)

DOI = "10.5281/zenodo.17830772"
ROOMS = ("A", "W2", "W4", "W6")
SPECIES = ("CH", "NM", "PC")
ARENAS = tuple(f"{r}_{a}" for r in ROOMS for a in range(1, 6))
RIDGE = .05
MODEL_SPECS = {
    "M0_context_flowering": ("logFlowers",),
    "M1_flowering_calendar": ("logFlowers", "bloomDOY"),
    "M2_time_averaged_bees": ("logFlowers", "adultMean"),
    "M3_date_matched_bee_window": ("logFlowers", "bloomBeeDensity"),
    "M4_calendar_and_bee_window": (
        "logFlowers", "bloomDOY", "bloomBeeDensity"
    ),
    "M5_source_realized_visit_rate": ("logFlowers", "visitRate"),
    "M6_adult_mean_and_window": (
        "logFlowers", "adultMean", "bloomBeeDensity"
    ),
}
OUTCOMES = ("fruit_seed_fraction", "F1_germination", "F1_cotyl_survival")


def group_key(r):
    return (r["trtmt"], r["arena"], r["sp"])


def make_records(sources):
    gate = audit_source_tables(sources)
    raw = sources["data_seeds_germ_pSEM.txt"]
    sgroups = defaultdict(list)
    for r in raw:
        k = group_key(r)
        if k[0] not in ROOMS or k[2] not in SPECIES or k[1] not in "12345":
            raise ValueError("unrecognized original room/arena/species")
        sgroups[k].append(r)
    if len(sgroups) != 60:
        raise ValueError("expected 60 original source units")

    bees = {}
    by_arena = defaultdict(list)
    for r in sources["bee_abund_2022.txt"]:
        room, area = r["trtmt"], r["arena"]
        arena = f"{room}_{area}"
        if arena not in ARENAS:
            raise ValueError("original independent bee census area not mapped")
        doy = int(numeric(r, "DOY"))
        key=(arena,doy)
        if key in bees:
            raise ValueError("duplicated arena census date")
        v=numeric(r,"bees")
        if v<0:
            raise ValueError("negative source bee density")
        bees[key]=v
        by_arena[arena].append(v)
    if len(bees)!=560 or set(by_arena)!=set(ARENAS):
        raise ValueError("incomplete independent original bee census")
    if {len(v) for v in by_arena.values()} != {28}:
        raise ValueError("unequal original arena bee-census day support")

    flowers = defaultdict(list)
    for r in sources["flwrcount_temp2022.txt"]:
        tag = r["trtmt_arena"]
        if "_" not in tag:
            raise ValueError("unexpected original flower census arena key")
        room, area = tag.rsplit("_",1)
        if area == "TR":
            continue  # aggregate treatment series, not a real arena
        arena=f"{room}_{area}"
        sp = r["species"]
        if arena not in ARENAS or sp not in SPECIES:
            raise ValueError("source flower census group invalid")
        n=numeric(r,"flwr_count")
        if n<0:
            raise ValueError("negative observed flower count")
        flowers[(room,area,sp)].append(
            (int(numeric(r,"DOY")),n)
        )
    if len(flowers)!=60:
        raise ValueError("missing independent flower time groups")

    records=[]
    arithmetic_mismatches=0
    for key, group in sorted(sgroups.items()):
        room,area,sp=key
        arena=f"{room}_{area}"
        full=flowers[key]
        if len({day for day,_ in full})!=len(full):
            raise ValueError("duplicate original group flowering day")
        bloom_total=sum(n for _,n in full)
        common=[(day,n,bees[(arena,day)])
                for day,n in full if (arena,day) in bees]
        matched_total=sum(n for _,n,_ in common)
        if not bloom_total or not matched_total:
            raise ValueError("unobserved matched flower x bee exposure")
        raw_seed=0
        raw_ovule=0
        source_visits=[]
        germ_vals=set()
        cotyl_vals=set()
        sow_vals=set()
        for row in group:
            seeds=numeric(row,"seeds")
            undeveloped=numeric(row,"ovules")
            total=numeric(row,"ovules_tot")
            if abs(seeds+undeveloped-total)>1e-6 or total<=0:
                raise ValueError("source fruit count denominator invalid")
            source_fraction=numeric(row,"seed_set")
            if abs(source_fraction-seeds/total)>1e-5:
                arithmetic_mismatches+=1
            raw_seed+=seeds
            raw_ovule+=total
            source_visits.append(numeric(row,"visits_avg"))
            germ_vals.add(numeric(row,"germ"))
            cotyl_vals.add(numeric(row,"cotyl"))
            sow_vals.add(numeric(row,"seeds_sown"))
        if any(len(v)!=1 for v in (germ_vals,cotyl_vals,sow_vals)):
            raise ValueError("seedling outcomes varied within one original group")
        sown=next(iter(sow_vals))
        germ=next(iter(germ_vals))
        cotyl=next(iter(cotyl_vals))
        if not sown or germ>sown or cotyl>germ:
            raise ValueError("impossible original 6-seed germination trial")
        records.append({
            "arena":arena, "room":room,"sp":sp,
            "n_source_fruit_rows":len(group),
            "logFlowers":log1p(bloom_total),
            "bloomDOY":sum(day*n for day,n in full)/bloom_total,
            "bloomBeeDensity":sum(n*b for _,n,b in common)/matched_total,
            "adultMean":mean(by_arena[arena]),
            "visitRate":mean(source_visits),
            "flowerBeeCensusCoverage":matched_total/bloom_total,
            "fruit_seed_fraction":raw_seed/raw_ovule,
            "F1_germination":germ/sown,
            "F1_cotyl_survival":cotyl/sown,
            "n_sown_seeds":sown,
            "raw_fruit_numerator":raw_seed,
            "raw_fruit_ovules":raw_ovule,
        })
    if {z["arena"] for z in records}!=set(ARENAS):
        raise ValueError("some arena missing any component")
    if len(records)!=60:
        raise ValueError("unexpected 60 group-record count")
    return records,{
        "source_unit_gate":gate,
        "n_original_fruit_seed_set_column_disagreements":arithmetic_mismatches,
        "seed_fraction_recomputed_using_seeds_and_ovules_tot":True,
        "source_2022_seed_sowing_group_count":len(records),
        "source_unique_F1_seeds_sown":sum(x["n_sown_seeds"] for x in records),
        "n_grouped_parent_flower_rows":sum(
            x["n_source_fruit_rows"] for x in records
        ),
        "n_original_independent_arena_holdouts":len(ARENAS),
        "mean_matched_source_bee_census_flower_coverage":
            mean(x["flowerBeeCensusCoverage"] for x in records),
    }


def solve_linear(A,b):
    n=len(b); aug=[list(A[i])+[b[i]] for i in range(n)]
    for i in range(n):
        p=max(range(i,n),key=lambda j:abs(aug[j][i]))
        aug[i],aug[p]=aug[p],aug[i]
        d=aug[i][i]
        if abs(d)<1e-10:
            raise ValueError("singular source ridge model")
        for k in range(i,n+1):
            aug[i][k]/=d
        for j in range(n):
            if j!=i:
                f=aug[j][i]
                for k in range(i,n+1):
                    aug[j][k]-=f*aug[i][k]
    return [row[-1] for row in aug]


def design(train,test,variables,include_room=True):
    means={k:mean(x[k] for x in train) for k in variables}
    std={k:sqrt(mean((x[k]-means[k])**2 for x in train)) or 1
         for k in variables}
    def encode(rows):
        return [
            [1.0]+
            [float(x["sp"]==sp) for sp in SPECIES[1:]]+
            ([float(x["room"]==room) for room in ROOMS[1:]]
             if include_room else [])+
            [(x[k]-means[k])/std[k] for k in variables]
            for x in rows
        ]
    return encode(train),encode(test)


def ridge_fit(X,y):
    p=len(X[0])
    A=[[0.0]*p for _ in range(p)];b=[0.0]*p
    for row,target in zip(X,y):
        for j in range(p):
            b[j]+=row[j]*target
            for k in range(p):
                A[j][k]+=row[j]*row[k]
    for j in range(1,p):
        A[j][j]+=RIDGE
    return solve_linear(A,b)


def evaluate(records,models=MODEL_SPECS):
    assert {x["arena"] for x in records}==set(ARENAS)
    outputs={}
    for outcome in OUTCOMES:
        comparisons={}
        for model,spec in models.items():
            per_arena={}
            for held in ARENAS:
                train=[x for x in records if x["arena"]!=held]
                test=[x for x in records if x["arena"]==held]
                if len(test)!=3:
                    raise ValueError("expected exactly three species/held-out arena")
                X,T=design(train,test,spec)
                b=ridge_fit(X,[x[outcome] for x in train])
                per_arena[held]=mean(
                    (x[outcome]-max(0.,min(1.,sum(v*w for v,w in zip(features,b)))))**2
                    for x,features in zip(test,T)
                )
            comparisons[model]={
                "equal_arena_rmse":sqrt(mean(per_arena.values())),
                "n_arena_folds":len(per_arena),
                "n_group_outcomes":len(records),
                "per_arena_mse":per_arena,
                "fixed_predictors":list(spec),
            }
        ref=comparisons["M1_flowering_calendar"]
        adult=comparisons["M2_time_averaged_bees"]
        win=comparisons["M3_date_matched_bee_window"]
        outputs[outcome]={
            "models":comparisons,
            "window_minus_calendar_rmse":
                win["equal_arena_rmse"]-ref["equal_arena_rmse"],
            "window_minus_adult_mean_rmse":
                win["equal_arena_rmse"]-adult["equal_arena_rmse"],
            "n_arena_folds_bee_window_better_than_calendar":sum(
                win["per_arena_mse"][k]<ref["per_arena_mse"][k]
                for k in ARENAS
            ),
            "n_arena_folds_bee_window_better_than_mean_adult":sum(
                win["per_arena_mse"][k]<adult["per_arena_mse"][k]
                for k in ARENAS
            ),
        }
    return outputs



def room_holdout_sensitivity(records,models=MODEL_SPECS):
    """Deliberately difficult extrapolation: one entire original room out.

    Room and temperature treatment are one-to-one, thus room categorical
    indicators are NOT estimable on an unseen fourth room. Remove room
    dummies from all models symmetrically. Four folds are NOT causal
    treatment replicates or independent experimental years.
    """
    if {x["room"] for x in records} != set(ROOMS):
        raise ValueError("four original temperature rooms required")
    outputs={}
    for outcome in OUTCOMES:
        results={}
        for model,spec in models.items():
            errors={}
            for held in ROOMS:
                train=[x for x in records if x["room"]!=held]
                test=[x for x in records if x["room"]==held]
                if len(test)!=15:
                    raise ValueError("room must contain 5 arenas × 3 species")
                X,T=design(train,test,spec,include_room=False)
                beta=ridge_fit(X,[x[outcome] for x in train])
                errors[held]=mean(
                    (x[outcome]-max(0.,min(1.,sum(v*b for v,b in zip(feat,beta)))))**2
                    for x,feat in zip(test,T)
                )
            results[model]={
                "equal_room_rmse":sqrt(mean(errors.values())),
                "n_held_out_rooms":4,
                "per_room_mse":errors,
            }
        outputs[outcome]={
            "models":results,
            "window_minus_calendar_rmse":
                results["M3_date_matched_bee_window"]["equal_room_rmse"]-
                results["M1_flowering_calendar"]["equal_room_rmse"],
            "window_minus_adult_mean_rmse":
                results["M3_date_matched_bee_window"]["equal_room_rmse"]-
                results["M2_time_averaged_bees"]["equal_room_rmse"],
            "interpretation":
                "out_of_temperature_room_domain_extrapolation_not_causal"
        }
    return outputs


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    args=p.parse_args()
    with ZipFile(BytesIO(fetch_original(
        "deManincor-et-al.2025_data_pSEM.zip"
    ))) as z:
        data={name:original_table(z,name) for name in NAMES}
    records,source=make_records(data)
    models=evaluate(records)
    room_validation=room_holdout_sensitivity(records)
    report={
        "schema":"iwe_2022_grouped_stage_vs_overlap_exploratory_v1",
        "doi":DOI,
        "original_source_md5_verified":True,
        "study_year":2022,
        "not_independent_temperature_treatment_replication":True,
        "n_temperature_rooms":4,
        "temperature_rooms_each_have_one_treatment":True,
        "n_source_arena_groups":20,
        "n_independently_tracked_seed_germination_units":60,
        "n_original_sampled_flower_fruit_rows":208,
        "original_F1_seed_germination_has_no_verified_maternal_plant_join":True,
        "all_models_exploratory_post_outcome_comparison":True,
        "original_data_quality":source,
        "model_comparisons":models,
        "leave_one_room_out_extrapolation_sensitivity":room_validation,
        "room_holdout_omits_room_fixed_effects_by_design":True,
        "strict_H1_cluster_promotion":False,
    }
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"grouped_stage_prediction_audit.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print("DEMANINCOR2022_GROUPED_STAGE_SOURCE",json.dumps({
        k:v for k,v in source.items() if k!="source_unit_gate"
    },sort_keys=True))
    print("DEMANINCOR2022_GROUPED_STAGE_RMSE",json.dumps({
        stage:{
            model:round(row["equal_arena_rmse"],6)
            for model,row in spec["models"].items()
        } for stage,spec in models.items()
    },sort_keys=True))
    print("DEMANINCOR2022_ROOM_HOLDOUT_RMSE",json.dumps({
        stage:{
            model:round(item["equal_room_rmse"],6)
            for model,item in val["models"].items()
        } for stage,val in room_validation.items()
    },sort_keys=True))
    print("DEMANINCOR2022_GROUPED_STAGE_WINS",json.dumps({
        stage:{
            "window_better_than_calendar":
              obj["n_arena_folds_bee_window_better_than_calendar"],
            "window_better_than_mean_bee":
              obj["n_arena_folds_bee_window_better_than_mean_adult"],
            "delta_vs_calendar":obj["window_minus_calendar_rmse"],
            "delta_vs_adult_mean":obj["window_minus_adult_mean_rmse"],
        } for stage,obj in models.items()
    },sort_keys=True))
    print("Room temperature treatments are not independently replicated")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
