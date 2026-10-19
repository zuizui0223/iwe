"""Explore where floral visitor information appears in a reproductive chain.

Original Höfer et al. 2022 Sinapis arvensis dataset, Zenodo
DOI 10.5281/zenodo.7335086. This is an independent resource/visitation
study, NOT a temporal partner synchrony study. One plant per row, 15
plots nested in five experimental water shelters, one source programme.

Use original observed/estimated:
  - recorded season flower index (NOT a confirmed complete opportunity denominator),
  - source counted pods per plant,
  - average seeds per pod,
  - author-estimated seeds per plant (a deterministic pod x average-seed product).

The original data show 47/50 plants with pods > the recorded sumflower
index. The invalid pods/sumflower and seeds/sumflower ratios are never
fitted as reproductive conversion probabilities. Only individual
pods and mean seeds/pod are biological component outcomes.

Question: conditional on the recorded flower index and water allocation,
does observed visitor intensity add out-of-shelter information about
pod numbers or per-pod seeds, without fabricating a followed-flower chain?

No invented phenology, plant-by-plant actual viable seeds, mediation
causality, treatment×visit randomization, or strict IWE H1 promotion.
No pooled effects between partly algebraically dependent responses.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from math import log1p, isfinite
from pathlib import Path
from statistics import mean, median

from scripts.analyze_hofer2022_resource_limits import (
    _finite, link_plants, load_sources, validate, MODELS,
)

SOURCE_DOI = "10.5281/zenodo.7335086"
STAGE_NAMES = {
    "pods_total": "log1p_recorded_pods_per_plant",
    "seeds_per_pod": "log1p_source_average_seeds_per_pod",
    "seed_total": "log1p_source_estimated_total_seeds",
}
# Source sumflower and pods are NOT demonstrated to be congruent
# reproductive-unit counts: 47/50 observed source plants have pods
# exceeding sumflower. Therefore pods/sumflower and seeds/sumflower
# are strictly diagnostics of measurement mismatch, NOT stage outcomes.
COMPARISON_MODELS = {
    "flowers": MODELS["M1_water_and_flowers"],
    "add_visits_per_flower_day": MODELS["M3_water_flowers_visitors"],
    "add_visits_per_day": MODELS["M6_water_flowers_visitor_rate_per_day"],
    "flowers_plus_SWP": (
        "treatment", "logFlowers", "waterPotential"
    ),
    "flowers_SWP_visits_per_day": (
        "treatment", "logFlowers", "waterPotential", "logVisitorsPerDay"
    ),
    "flowers_plus_duration": MODELS["M5_water_flowers_flowering_duration"],
}


def stage_plants(sources: dict) -> tuple[list[dict], dict]:
    """Link original plant rows without treating taxon-group visits as n."""
    base, source_missing, repeated = link_plants(sources)
    by_id = {}
    for r in sources["Floral_traits.csv"]:
        identifier = r["plantID"]
        if identifier in by_id:
            raise ValueError("original plant duplicated in floral traits")
        by_id[identifier] = r
    if len(by_id) != 53:
        raise ValueError("original total focal plants changed")
    records = []
    reject = Counter()
    for x in base:
        r = by_id[x["plant"]]
        if r.get("treatment") != x["treatment"]:
            raise ValueError("source treatment identity drift")
        pods = _finite(r, "pods")
        seeds_per_pod = _finite(r, "avgseed")
        if pods is None or seeds_per_pod is None:
            reject["missing_pod_or_seed_per_pod"] += 1
            continue
        if pods <= 0:
            reject["zero_source_pod_cannot_define_seeds_per_pod"] += 1
            continue
        flowers = x["flowerCount"]
        if flowers <= 0:
            raise ValueError("zero total observed flowers")
        if not isfinite(pods / flowers):
            raise ValueError("invalid original fruit/flower ratio")
        # Source separately estimates seeds per plant: DO NOT assume
        # pods*avgseed is exactly identical in the source, and DO NOT
        # use this identity as an independent biological confirmation.
        outcome = {
            "pods_total": log1p(pods),
            "seeds_per_pod": log1p(seeds_per_pod),
            "seed_total": x["outcome"],
        }
        records.append({
            **x,
            "sourcePods": pods,
            "sourceAvgSeedsPerPod": seeds_per_pod,
            "podsPerFlower": pods / flowers,
            "sourceSeedsPerFlower": x["estimatedTotalSeeds"] / flowers,
            "derivedExpectedSeedsFromPodAndAvg": pods * seeds_per_pod,
            "expectedFromPodRatio":
                (pods * seeds_per_pod) / x["estimatedTotalSeeds"]
                if x["estimatedTotalSeeds"] > 0 else None,
            "stages": outcome,
        })
    if len(set(x["shelter"] for x in records)) != 5:
        raise ValueError("stage source has fewer than five shelters")
    return records, {
        "source_n_raw_plants": len(by_id),
        "initial_visitor_seed_link_n": len(base),
        "initial_source_excluded": source_missing,
        "duplicate_visitor_taxon_plant_count": repeated,
        "stage_n": len(records),
        "stage_excluded": dict(reject),
        "n_plots": len(set(x["plot"] for x in records)),
        "n_shelters": len(set(x["shelter"] for x in records)),
        "shelter_counts": dict(Counter(x["shelter"] for x in records)),
        "water_treatments": dict(Counter(x["treatment"] for x in records)),
    }


def stage_validate(records: list[dict]) -> dict:
    """Fit each stage on EXACTLY the same biological units and shelters."""
    if len(records) < 25:
        raise ValueError("too few complete reproductive stage plants")
    result = {}
    for stage in STAGE_NAMES:
        scoped = [{**x, "outcome": x["stages"][stage]} for x in records]
        fit = validate(scoped, models=COMPARISON_MODELS)
        ref = fit["flowers"]
        comparisons = {}
        for key in COMPARISON_MODELS:
            if key == "flowers":
                continue
            m = fit[key]
            comparisons[key] = {
                "relative_rmse_reduction_vs_flower_only":
                    1 - m["mean_shelter_rmse"] / ref["mean_shelter_rmse"]
                    if ref["mean_shelter_rmse"] else None,
                "shelter_wins_over_flower_only": sum(
                    m["by_shelter_mse"][s] < ref["by_shelter_mse"][s]
                    for s in ref["by_shelter_mse"]
                ),
            }
        # Fair within-stage comparison of *continuous water potential*
        # baseline + visitor/day: not claiming SWP was assigned as random.
        water = fit["flowers_plus_SWP"]
        visit_after_water = fit["flowers_SWP_visits_per_day"]
        comparisons["visitor_day_after_measured_SWP"] = {
            "relative_rmse_reduction":
                1 - visit_after_water["mean_shelter_rmse"] /
                water["mean_shelter_rmse"]
                if water["mean_shelter_rmse"] else None,
            "shelter_wins": sum(
                visit_after_water["by_shelter_mse"][s] <
                water["by_shelter_mse"][s]
                for s in water["by_shelter_mse"]
            ),
        }
        result[stage] = {
            "response_name": STAGE_NAMES[stage],
            "n_plants": len(records),
            "n_shelters": 5,
            "source_response_years": 1,
            "model_rmse": {
                k: value["mean_shelter_rmse"] for k, value in fit.items()
            },
            "per_shelter_errors": {
                k: value["by_shelter_mse"] for k, value in fit.items()
            },
            "paired_comparisons": comparisons,
        }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    raw = load_sources()  # every underlying CSV source byte is MD5 guarded
    plants, admissibility = stage_plants(raw)
    ratios = [
        x["expectedFromPodRatio"] for x in plants
        if x["expectedFromPodRatio"] is not None
    ]
    out = {
        "schema": "iwe_hofer2022_original_reproductive_conversion_v1",
        "source_doi": SOURCE_DOI,
        "source_md5_verified": True,
        "timing_partner_window_observed": False,
        "strict_h1_effect_admitted": False,
        "single_programme": True,
        "original_source_grain": "plant_nested_plot_nested_shelter",
        "admission": admissibility,
        "source_component_consistency": {
            "median_pods_per_recorded_flower":
                median(x["podsPerFlower"] for x in plants),
            "n_pods_exceed_source_total_flower": sum(
                x["sourcePods"] > x["flowerCount"] for x in plants
            ),
            "number_compared_with_pod_flower_counts": len(plants),
            "pod_per_flower_not_admitted_as_conversion_endpoint": True,
            "reason":
                "most plants have more counted pods than sumflower; "
                "the source flower count and total pods are not an "
                "identified matching unit/complete opportunity denominator",
            "median_pods_x_avgseed_to_estimated_total_seed_ratio":
                median(ratios) if ratios else None,
            "n_exact_pods_x_avgseed_equals_estimated_total": sum(
                abs(x["derivedExpectedSeedsFromPodAndAvg"] -
                    x["estimatedTotalSeeds"]) <=
                1e-6 * max(1.0, x["estimatedTotalSeeds"])
                for x in plants
            ),
            "ratio_is_not_independent_source_measurement": True,
        },
        "models": stage_validate(plants),
        "interpretation_contract": {
            "estimated_seeds_not_viable_recruits": True,
            "pods_per_source_sumflower_invalid_fruit_conversion_ratio": True,
            "reported_flower_variable_may_be_incomplete_observation_index":
                True,
            "stage_outcomes_share_algebraic_inputs_not_independent_effects":
                True,
            "season_aggregated_visitor_rows_not_partner_phenology": True,
            "visitation_rates_observational_not_randomized": True,
            "same_five_shelters_held_out_for_every_comparison": True,
            "selection_of_question_after_original_published_results": True,
            "no_statistically_identified_resource_by_service_causality":
                True,
        }
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "stage_conversion_audit.json").write_text(
        json.dumps(out, indent=2)+"\n", encoding="utf-8"
    )
    print("HOFER_CONVERSION_ADMISSION", json.dumps(
        admissibility, sort_keys=True
    ))
    print("HOFER_CONVERSION_SOURCE_CONSISTENCY", json.dumps(
        out["source_component_consistency"], sort_keys=True
    ))
    for stage, model in out["models"].items():
        print("HOFER_CONVERSION_STAGE", stage, json.dumps({
            "n_plants": model["n_plants"],
            "model_rmse": model["model_rmse"],
            "paired_comparisons": model["paired_comparisons"],
        }, sort_keys=True))
    print("No animal flight dates, no confirmed within-flower biological chain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
