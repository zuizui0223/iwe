"""Cross-cohort, source-verified flower × Osmia season transport diagnostic.

Two independent experimental seasons, 2021/2022, in the same research
programme and with the same three hosts and Osmia lignaria. Biological
unit is an *arena × species* sampled-fruit seed fraction in each cohort,
never 181 individual plants vs 60 group responses as if exchangeable
independent trials.

2021 original: 181 complete fruit-source-matched individuals in eight
experimental arenas (or 228 with partly missing other sampled fruits);
aggregate actual fruit seed and undeveloped ovule counts for each of
24 arena × species groups. All source flower census records, including
those without a measured later seed fate, supply the season bloom
reference. Only same-day independently observed bee census is used.

2022 original: 208 source flower/fruit rows, nested in 60 original
arena × species group responses in 20 physical arenas; raw seeds/total
ovules close, 31 exported seed-set fractions do not and are ignored.
No 208 independent F1 germination units are fabricated.

Use an identically derived source response:
    seed fraction = sum(sampled mature seeds)/sum(total sampled ovules)

Calendar and adult exposure are normalized *without outcome information*
within the target cohort (available after flower season); modelling is
retrospective diagnostic, NOT prospective model deployment. Predictors
are differentially sampled across years; positive/negative comparisons
do not demonstrate effect reversals, random room causal effects, or
independent replicated programmes.

Compare 2021->2022 and 2022->2021 whole-cohort transfers, in addition
to held-arena within-cohort performance. Fit only training outcomes;
all numeric model centering/scaling is fitted on training data.
Original data stay at the DOI sources (both records MD5 checked).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from math import isfinite, log1p, sqrt
from pathlib import Path
from statistics import mean
from io import BytesIO
from zipfile import ZipFile

from scripts.analyze_demanincor2023_service_window import (
    PINNED_MD5 as MD5_2021, read_original as get_2021,
    source_rows as rows_2021, build_plants as build_2021_plants,
    SPECIES as SPECIES_2021,
)
from scripts.analyze_demanincor2022_grouped_stage_windows import (
    make_records as build_2022_groups,
    ROOMS as ROOMS_2022,
)
from scripts.audit_demanincor2022_reproduction_units import (
    NAMES as NAMES_2022, original_table as table_2022,
)
from scripts.probe_demanincor2022_stage_zip import (
    fetch_original as get_2022,
)

SPECIES = ("CH", "NM", "PC")
RIDGE = 0.05
COHORT_2021 = "2021"
COHORT_2022 = "2022"
MODELS = {
    "M0_species_and_flower_share": ("flowerShare",),
    "M1_calendar": ("flowerShare", "relativeBloomCalendar"),
    "M2_mean_bee_density": ("flowerShare", "scaledMeanBeeDensity"),
    "M3_real_bee_window": ("flowerShare", "scaledBloomBeeDensity"),
    "M4_window_relative_to_mean_bees": (
        "flowerShare", "relativeBloomBeeDensity"
    ),
    "M5_calendar_and_window": (
        "flowerShare", "relativeBloomCalendar",
        "scaledBloomBeeDensity"
    ),
    "M6_calendar_and_relative_window": (
        "flowerShare", "relativeBloomCalendar",
        "relativeBloomBeeDensity"
    ),
    # Critical ablation: does timing have value after seasonal mean
    # adult availability is already observed? M3 vs M2 alone is not a
    # nested test, but M7 vs M2 uses the same additional timing input.
    "M7_adult_mean_plus_bee_window": (
        "flowerShare", "scaledMeanBeeDensity",
        "scaledBloomBeeDensity"
    ),
    "M8_adult_mean_plus_relative_window": (
        "flowerShare", "scaledMeanBeeDensity",
        "relativeBloomBeeDensity"
    ),
    "M9_adult_mean_and_calendar": (
        "flowerShare", "scaledMeanBeeDensity",
        "relativeBloomCalendar"
    ),
}


def _nonnegative(value, label):
    try:
        n = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("non-numeric original " + label) from exc
    if not isfinite(n) or n < 0:
        raise ValueError("negative / non-finite original " + label)
    return n


def aggregate_2021(sources, allow_partly_missing=False):
    """Genuine original plant outcomes, grouped to 2022-comparable units."""
    plants, excluded = build_2021_plants(
        sources, allow_incomplete_fruit=allow_partly_missing
    )
    outcomes = defaultdict(lambda: {"seeds":0.0, "total":0.0,"n":0})
    for p in plants:
        key=(p["arena"],p["species"])
        seed=p["sampled_seed_count"]
        ov=p["sampled_ovule_count"]
        outcomes[key]["seeds"] += seed
        outcomes[key]["total"] += seed + ov
        outcomes[key]["n"] += 1

    bee = {}
    means = defaultdict(list)
    for row in sources["bee_density.txt"]:
        date, day, treatment, number, density = row
        arena=treatment+number
        key=(arena,int(day))
        if key in bee:
            raise ValueError("repeated bee day in 2021 source")
        b=_nonnegative(density,"2021 independently observed bees")
        bee[key]=b
        means[arena].append(b)

    bloom = defaultdict(lambda: defaultdict(float))
    for row in sources["flower_count.txt"]:
        cage,treatment,sp,identity = row[:4]
        if cage not in means or sp not in SPECIES:
            raise ValueError("unknown original plant/arena")
        day=int(row[7])
        b=_nonnegative(row[8],"2021 source flower census")
        bloom[(cage,sp)][day]+=b
    units=[]
    for (arena,sp), y in sorted(outcomes.items()):
        if not y["total"]>0 or not y["n"]:
            raise ValueError("original 2021 sampled fruit outcome has no denominator")
        curve=bloom[(arena,sp)]
        if not curve:
            raise ValueError("source 2021 did not monitor flowering")
        full=sum(curve.values())
        common=[(day,count,bee[(arena,day)])
                for day,count in curve.items() if (arena,day) in bee]
        paired=sum(n for _,n,_ in common)
        if full<=0 or paired<=0:
            raise ValueError("no exact source flower/bee date overlap")
        units.append({
            "cohort":COHORT_2021, "arena":arena, "species":sp,
            "seed_fraction":y["seeds"]/y["total"],
            "seeds_measured":y["seeds"],"ovules_sampled":y["total"],
            "n_original_outcome_plants":y["n"],
            "flowerTotal":full,
            "bloomDOY":sum(day*n for day,n in curve.items())/full,
            "bloomBeeDensity":sum(n*b for _,n,b in common)/paired,
            "adultMean":mean(means[arena]),
            "matchedFlowerCoverage":paired/full,
        })
    if set(p["species"] for p in units)!=set(SPECIES):
        raise ValueError("2021 source lacks plant species")
    return units,{
        "n_plants_with_original_seed_outcome":len(plants),
        "excluded_original_source":excluded,
        "n_source_arena_species_groups":len(units),
        "n_original_arenas":len({x["arena"] for x in units}),
        "original_census_plant_ids":
            len({(row[0],row[2],row[3])
                 for row in sources["flower_count.txt"]}),
        "n_original_daily_bee_censuses":len(bee),
        "partial_fruit_sensitivity":allow_partly_missing,
    }


def aggregate_2022(sources):
    groups, gate = build_2022_groups(sources)
    units=[]
    for g in groups:
        total=g["raw_fruit_ovules"]
        seed=g["raw_fruit_numerator"]
        if total<=0 or seed>total:
            raise ValueError("invalid 2022 raw seed source group")
        units.append({
            "cohort":COHORT_2022,
            "arena":g["arena"],
            "species":g["sp"],
            "seed_fraction":seed/total,
            "seeds_measured":seed,
            "ovules_sampled":total,
            "n_original_outcome_plants":g["n_source_fruit_rows"],
            "flowerTotal":__import__("math").expm1(g["logFlowers"]),
            "bloomDOY":g["bloomDOY"],
            "bloomBeeDensity":g["bloomBeeDensity"],
            "adultMean":g["adultMean"],
            "matchedFlowerCoverage":g["flowerBeeCensusCoverage"],
        })
    return units,{
        "n_original_fruit_rows":gate["n_grouped_parent_flower_rows"],
        "n_source_arena_species_groups":len(units),
        "n_original_arenas":len({x["arena"] for x in units}),
        "n_unreliable_published_seedset_fraction_rows":
            gate["n_original_fruit_seed_set_column_disagreements"],
        "original_seed_fraction_recomputed_from_seed_and_ovule_counts":True,
    }


def harmonize(units):
    """Source-dependent units, outcome-free cohort-relative calendar scales.

    Counts are from different plant sampling frames, so use the
    three-species composition share within each arena, NOT absolute
    number of open flowers as if protocols were identical.
    """
    if len(units)==0:
        raise ValueError("no groups")
    if any(r["cohort"] not in (COHORT_2021,COHORT_2022) for r in units):
        raise ValueError("unknown original 2021/2022 cohort")
    out=[dict(x) for x in units]
    bycohort=defaultdict(list)
    byarena=defaultdict(list)
    for x in out:
        for k in ("seed_fraction","flowerTotal","bloomDOY",
                  "bloomBeeDensity","adultMean","matchedFlowerCoverage"):
            if not isfinite(float(x[k])):
                raise ValueError("nonfinite original "+k)
        if x["seed_fraction"]<0 or x["seed_fraction"]>1:
            raise ValueError("invalid sampled seed fraction")
        if x["flowerTotal"]<=0 or x["adultMean"]<0:
            raise ValueError("invalid source flowering/bee index")
        bycohort[x["cohort"]].append(x)
        byarena[(x["cohort"],x["arena"])].append(x)
    for key, rows in byarena.items():
        if {z["species"] for z in rows}!=set(SPECIES):
            raise ValueError("source group missing one of three species")
        if len(rows)!=3:
            raise ValueError("source group duplicated")
        denom=sum(z["flowerTotal"] for z in rows)
        for z in rows:
            z["flowerShare"]=z["flowerTotal"]/denom
    for cohort, rows in bycohort.items():
        calendar_min=min(z["bloomDOY"] for z in rows)
        calendar_max=max(z["bloomDOY"] for z in rows)
        span=calendar_max-calendar_min
        if span<=0:
            raise ValueError("no flowering calendar variation in cohort")
        mean_annual_bees=mean(z["adultMean"] for z in rows)
        if mean_annual_bees<=0:
            raise ValueError("no independent adult bee abundance recorded")
        for z in rows:
            z["relativeBloomCalendar"]=(z["bloomDOY"]-calendar_min)/span
            z["scaledMeanBeeDensity"]=z["adultMean"]/mean_annual_bees
            z["scaledBloomBeeDensity"]=z["bloomBeeDensity"]/mean_annual_bees
            z["relativeBloomBeeDensity"]=(z["bloomBeeDensity"]-z["adultMean"])/mean_annual_bees
            z["cohort_context_uses_only_source_predictors"]=True
    return out


def solve_linear(a,b):
    n=len(b)
    w=[list(a[i])+[b[i]] for i in range(n)]
    for i in range(n):
        pivot=max(range(i,n),key=lambda j:abs(w[j][i]))
        w[i],w[pivot]=w[pivot],w[i]
        d=w[i][i]
        if abs(d)<1e-10:
            raise ValueError("singular cross-cohort model")
        for col in range(i,n+1):
            w[i][col]/=d
        for j in range(n):
            if j==i:
                continue
            mult=w[j][i]
            for col in range(i,n+1):
                w[j][col]-=mult*w[i][col]
    return [z[-1] for z in w]


def fit_and_predict(train,test,spec):
    """Same model, outcome-blind test cohort and train-only standardization."""
    if not train or not test:
        raise ValueError("missing train/test source cohort")
    mu={k:mean(x[k] for x in train) for k in spec}
    sigma={k:sqrt(mean((x[k]-mu[k])**2 for x in train)) or 1.
           for k in spec}
    def encode(rows):
        return [
            [1.,float(x["species"]=="NM"),float(x["species"]=="PC")]+
            [(x[k]-mu[k])/sigma[k] for k in spec]
            for x in rows
        ]
    X=encode(train)
    T=encode(test)
    p=len(X[0])
    matrix=[[0.]*p for _ in range(p)]
    rhs=[0.]*p
    for x,r in zip(X,train):
        target=r["seed_fraction"]
        for i in range(p):
            rhs[i]+=x[i]*target
            for j in range(p):
                matrix[i][j]+=x[i]*x[j]
    for j in range(1,p):
        matrix[j][j]+=RIDGE
    beta=solve_linear(matrix,rhs)
    return [
        max(0.,min(1.,sum(w*b for w,b in zip(x,beta))))
        for x in T
    ]


def _score(test,predictions):
    if len(test)!=len(predictions):
        raise ValueError("nonmatching predicted original source groups")
    errors=defaultdict(list)
    for z,p in zip(test,predictions):
        errors[z["arena"]].append((z["seed_fraction"]-p)**2)
    if any(len(errors[k])!=3 for k in errors):
        raise ValueError("sample unit is not exactly three plant species/arena")
    arena_mse={k:mean(v) for k,v in sorted(errors.items())}
    return {
        "equal_arena_rmse":sqrt(mean(arena_mse.values())),
        "n_groups":len(test),
        "n_holdout_arenas":len(errors),
        "per_arena_mse":arena_mse,
    }


def compare(records):
    if {x["cohort"] for x in records}!={COHORT_2021,COHORT_2022}:
        raise ValueError("both original cohorts needed")
    outputs={}
    for year in (COHORT_2021,COHORT_2022):
        testing=[r for r in records if r["cohort"]==year]
        training=[r for r in records if r["cohort"]!=year]
        contrasts={}
        for name,spec in MODELS.items():
            predictions=fit_and_predict(training,testing,spec)
            contrasts[name]=_score(testing,predictions)
        reference=contrasts["M1_calendar"]["per_arena_mse"]
        outputs[f"other_year_trains_test_{year}"]={
            "trained_on":COHORT_2022 if year==COHORT_2021 else COHORT_2021,
            "tested_on":year,
            "models":contrasts,
            "window_wins_vs_calendar":sum(
                contrasts["M3_real_bee_window"]["per_arena_mse"][a]
                < reference[a] for a in reference
            ),
            "incremental_bee_window_after_season_mean": {
                "rmse_delta_M7_minus_M2":
                    contrasts["M7_adult_mean_plus_bee_window"]["equal_arena_rmse"]
                    - contrasts["M2_mean_bee_density"]["equal_arena_rmse"],
                "n_arenas_M7_better_than_M2":sum(
                    contrasts["M7_adult_mean_plus_bee_window"]["per_arena_mse"][a]
                    < contrasts["M2_mean_bee_density"]["per_arena_mse"][a]
                    for a in reference
                ),
            },
        }
    # Identical source-level output and predictors with within-cohort
    # held-out experimental ARENAS, not plants inside those arenas.
    for cohort in (COHORT_2021,COHORT_2022):
        y=[r for r in records if r["cohort"]==cohort]
        arenas=sorted({r["arena"] for r in y})
        scores={}
        for name,spec in MODELS.items():
            all_error={}
            for held in arenas:
                train=[z for z in y if z["arena"]!=held]
                test=[z for z in y if z["arena"]==held]
                pred=fit_and_predict(train,test,spec)
                all_error[held]=_score(test,pred)["per_arena_mse"][held]
            scores[name]={
                "equal_arena_rmse":sqrt(mean(all_error.values())),
                "per_arena_mse":all_error,
            }
        outputs[f"within_{cohort}_leave_arena_out"]={
            "tested_on":cohort,
            "models":scores,
            "window_wins_vs_calendar":sum(
                scores["M3_real_bee_window"]["per_arena_mse"][a]
                < scores["M1_calendar"]["per_arena_mse"][a]
                for a in arenas
            ),
        }
    return outputs


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--outdir",type=Path,required=True)
    args=parser.parse_args()

    source21={name:rows_2021(get_2021(name),name)
              for name in MD5_2021}
    y21,metadata21=aggregate_2021(source21)
    y21_partial,metadata21_partial=aggregate_2021(
        source21,allow_partly_missing=True
    )
    with ZipFile(BytesIO(get_2022(
        "deManincor-et-al.2025_data_pSEM.zip"
    ))) as z:
        source22={name:table_2022(z,name) for name in NAMES_2022}
    y22,metadata22=aggregate_2022(source22)
    if len(y21)!=24 or metadata21["n_plants_with_original_seed_outcome"]!=181:
        raise ValueError("2021 source complete-case original support drift")
    if len(y21_partial)!=24 or metadata21_partial[
        "n_plants_with_original_seed_outcome"]!=228:
        raise ValueError("2021 original partial fruit support drift")
    if len(y22)!=60 or metadata22["n_original_fruit_rows"]!=208:
        raise ValueError("2022 source group/fate support drift")

    units=harmonize(y21+y22)
    partial_units=harmonize(y21_partial+y22)
    main_results=compare(units)
    partial_results=compare(partial_units)
    metadata={
        COHORT_2021:metadata21, COHORT_2022:metadata22,
        "2021_partial_original_fruits":metadata21_partial,
        "n_crossyear_arena_species_groups":len(units),
        "n_source_cohorts":2,
        "source_year_specific_plant_fate_sampling_not_identical":True,
        "year_predictor_normalization_uses_only_pre_seed_flowering_bees":True,
        "germination_not_compared_across_cohorts":True,
        "one_research_programme_not_new_taxon_meta_replication":True,
        "temperature_designs_are_not_cross_year_identical":True,
    }
    audit={
        "schema":"iwe_osmia_crosscohort_harmonized_seed_fractions_v1",
        "sources":["10.5281/zenodo.7264150",
                   "10.5281/zenodo.17830772"],
        "original_md5_verified_both":True,
        "experimental_years":[2021,2022],
        "biological_unit":"arena_species_sampled_fruit_seed_fraction",
        "n_source_years":2,
        "n_independent_taxonomic_programmes":1,
        "causal_warming_effect_identified":False,
        "confirmatory_cross_year_model_selection":False,
        "strict_h1_new_effect_clusters":0,
        "source_metadata":metadata,
        "primary_models":main_results,
        "2021_partial_fruit_outcome_sensitivity":partial_results,
        "claims_not_supported":[
            "effect_size_meta_comparison_between_paper-specific_rmse",
            "cross_cohort_regime_selection_independently_replicated",
            "reproductive_germination_outcome_common_across_years",
            "a_2022_room_is_randomized_treatment_replication",
            "2021_individuals_are_independent_of_8_original_arenas",
        ]
    }
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"crosscohort_transport_audit.json").write_text(
        json.dumps(audit,indent=2)+"\n",encoding="utf-8"
    )
    print("OSMIA_COHORT_JOIN",json.dumps(metadata,sort_keys=True))
    for title,results in (
        ("OSMIA_PRIMARY",main_results),
        ("OSMIA_PARTIAL_2021_FRUIT",partial_results),
    ):
        print(title,json.dumps({
            k:{
                "train":v.get("trained_on"),
                "test":v.get("tested_on"),
                "n_arena_window_better_than_calendar":
                    v["window_wins_vs_calendar"],
                "rmse":{m:round(z["equal_arena_rmse"],6)
                        for m,z in v["models"].items()}
            } for k,v in results.items()
        },sort_keys=True))
    print("No confirmed carryover or independent treatment effect from two source cohorts")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
