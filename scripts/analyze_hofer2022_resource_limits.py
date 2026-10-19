"""Five-shelter, 53-plant resource-vs-service diagnostic, NOT temporal synchrony.

Original Höfer et al. (2022) public Zenodo 10.5281/zenodo.7335086.
The original source has plant-level flowering, estimated seed output and
visitor-group counts/rates *aggregated over monitoring days*. It does not
provide independently dated partner activity: no daily-overlap clock is
constructed, no strict IWE H1 effect is admitted, and models are
retrospective, not forecasts.

Test the limiting-stage boundary: after holding out an entire shelter,
does visitor rate per flower-day add information on final *estimated total
seeds per plant* beyond plant flower count and assigned water treatment?
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from io import StringIO
import json
from math import isfinite, log1p, sqrt
from pathlib import Path
from statistics import mean

from scripts.probe_hofer2022_resource_gate import _reader, get_original

DOC_DOI = "10.5281/zenodo.7335086"
REQUIRED = ("Int_data.csv", "Plantlist.csv", "Floral_traits.csv")
TREATMENTS = ("Control", "PrecipRed", "Drought")
MODELS = {
    "M0_water_treatment": ("treatment",),
    "M1_water_and_flowers": ("treatment", "logFlowers"),
    "M2_water_and_visitors": ("treatment", "logVisitation"),
    "M3_water_flowers_visitors": (
        "treatment", "logFlowers", "logVisitation"
    ),
    "M4_flowers_only": ("logFlowers",),
    "M5_water_flowers_flowering_duration": (
        "treatment", "logFlowers", "floweringDuration"
    ),
    # Essential falsifier: visitors per observation day, not divided by
    # number of flowers. If only a ratio-containing predictor improves
    # prediction, a source denominator artifact remains plausible.
    "M6_water_flowers_visitor_rate_per_day": (
        "treatment", "logFlowers", "logVisitorsPerDay"
    ),
}
POLLEN_MODELS = {
    "P0_water_and_flowers": ("treatment", "logFlowers"),
    "P1_add_visitor_per_flower_day": (
        "treatment", "logFlowers", "logVisitation"
    ),
    "P2_add_actual_pollen_grains_on_stigma": (
        "treatment", "logFlowers", "logPollenStigma"
    ),
    "P3_add_both_visitor_and_pollen": (
        "treatment", "logFlowers", "logVisitation", "logPollenStigma"
    ),
}
RIDGE = 0.05


def _finite(raw, field, allow_zero=True, allow_negative=False):
    s = str(raw.get(field, "")).strip()
    if s.upper() in ("", "NA", "NAN"):
        return None
    try:
        x = float(s)
    except ValueError as exc:
        raise ValueError("nonnumeric original value: " + field) from exc
    if not isfinite(x) or (x < 0 and not allow_negative) or (x == 0 and not allow_zero):
        raise ValueError("invalid negative/nonfinite: " + field)
    return x


def load_sources():
    return {
        name: _reader(get_original(name))[1]
        for name in REQUIRED
    }


def _unique(rows, keyfield):
    index = {}
    for r in rows:
        k = str(r.get(keyfield, "")).strip()
        if not k or k in index:
            raise ValueError("missing/repeated original plant ID: " + k)
        index[k] = r
    return index


def link_plants(sources):
    traits = _unique(sources["Floral_traits.csv"], "plantID")
    plants = _unique(sources["Plantlist.csv"], "plantID")
    if len(traits) != 53 or len(plants) != 53:
        raise ValueError("original focal plant support changed")
    if set(traits) != set(plants):
        raise ValueError("plant list and final source trait IDs differ")

    groups = defaultdict(list)
    for row in sources["Int_data.csv"]:
        pid = str(row.get("plantID", "")).strip()
        if pid not in traits:
            raise ValueError("visitor row references unobserved focal plant")
        groups[pid].append(row)
    if set(groups) != set(traits):
        raise ValueError("incomplete observed visitor-group plant IDs")
    if len(sources["Int_data.csv"]) != 427:
        raise ValueError("visitor source row count changed")

    excluded = Counter()
    result = []
    perplant_visitorgroup_repeats = 0
    for pid in sorted(traits):
        a, listing, visitrows = traits[pid], plants[pid], groups[pid]
        for c1, c2 in (
            ("motherID", "motherID"), ("treatment", "treatment"),
            ("plotID", "plotID"),
        ):
            if a[c1] != listing[c2]:
                raise ValueError("plant list and trait source disagree: " + c1)
        shelter = a["shelterID"]
        if listing["shelter"] != shelter:
            raise ValueError("assigned shelter ID differs across sources")
        if a["treatment"] not in TREATMENTS:
            raise ValueError("unrecognized water intervention")
        for r in visitrows:
            for k, tk in (("motherID", "motherID"),
                          ("treatment", "treatment"),
                          ("plotID", "plotID"), ("shelter", "shelterID")):
                if r[k] != a[tk]:
                    raise ValueError("visitor plant metadata mismatch: " + k)
        if len(set(r["visitorgroup"] for r in visitrows)) < len(visitrows):
            perplant_visitorgroup_repeats += 1
        seeds = _finite(a, "seedsperplant")
        nflower = _finite(a, "sumflower")
        duration = _finite(a, "floweringtime")
        water = _finite(a, "SWP", allow_negative=True)
        visitrates = [_finite(r, "NrInt_day_flower") for r in visitrows]
        dayrates = [_finite(r, "NrInt_day") for r in visitrows]
        pollen_stigma = _finite(a, "pollenstigma")
        # The author report gives a rate by visitor group, normalized by
        # monitoring days and plant flower abundance; summing these
        # visitor-type rates is a plant-level observation aggregate.
        if None in (seeds, nflower, duration, water) or any(
            r is None for r in (*visitrates, *dayrates)
        ):
            excluded["required_plant_or_visit_data_missing"] += 1
            continue
        if nflower <= 0:
            excluded["zero_measured_flowers"] += 1
            continue
        if seeds < 0:
            raise ValueError("negative seed production")
        result.append({
            "plant": pid,
            "shelter": shelter,
            "plot": a["plotID"],
            "mother": a["motherID"],
            "treatment": a["treatment"],
            "flowerCount": nflower,
            "logFlowers": log1p(nflower),
            "waterPotential": water,
            "floweringDuration": duration,
            "visitGroupRows": len(visitrows),
            "visitGroupRepeated": len(set(
                r["visitorgroup"] for r in visitrows
            )) != len(visitrows),
            "visitPerFlowerDay": sum(visitrates),
            "logVisitation": log1p(sum(visitrates)),
            "visitorRatePerDay": sum(dayrates),
            "logVisitorsPerDay": log1p(sum(dayrates)),
            "pollenStigma": pollen_stigma,
            "logPollenStigma":
                log1p(pollen_stigma) if pollen_stigma is not None else None,
            "estimatedTotalSeeds": seeds,
            "outcome": log1p(seeds),
        })
    if len(set(x["shelter"] for x in result)) < 4:
        raise ValueError("insufficient true experimental shelter groups")
    return result, dict(excluded), perplant_visitorgroup_repeats


def solve(A, y):
    n = len(y)
    a = [list(row) + [float(y[i])] for i, row in enumerate(A)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(a[i][col]))
        a[col], a[pivot] = a[pivot], a[col]
        if abs(a[col][col]) < 1e-10:
            raise ValueError("singular ridge model")
        v = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= v
        for i in range(n):
            if i != col:
                v = a[i][col]
                for j in range(col, n + 1):
                    a[i][j] -= v * a[col][j]
    return [row[n] for row in a]


def features(train, test, spec):
    cols = [k for k in spec if k != "treatment"]
    mu = {c: mean(z[c] for z in train) for c in cols}
    sd = {c: sqrt(mean((z[c]-mu[c])**2 for z in train)) or 1 for c in cols}
    def encode(rows):
        return [
            [1, float(x["treatment"]=="PrecipRed"),
             float(x["treatment"]=="Drought")] +
            [(x[k]-mu[k])/sd[k] for k in cols]
            if "treatment" in spec
            else [1]+[(x[k]-mu[k])/sd[k] for k in cols]
            for x in rows
        ]
    return encode(train), encode(test)


def ridge_fit(X, y):
    p = len(X[0])
    A = [[0.0]*p for _ in range(p)]
    b = [0.0]*p
    for row, target in zip(X, y):
        for i in range(p):
            b[i] += row[i]*target
            for j in range(p):
                A[i][j] += row[i]*row[j]
    for i in range(1, p):
        A[i][i] += RIDGE
    return solve(A, b)


def validate(plants, models=MODELS):
    groups = sorted(set(r["shelter"] for r in plants))
    if len(groups) != 5:
        raise ValueError("source must contain five independent shelter blocks")
    output = {}
    for name, variables in models.items():
        rows = []
        for hold in groups:
            train = [x for x in plants if x["shelter"] != hold]
            test = [x for x in plants if x["shelter"] == hold]
            if not test:
                raise ValueError("empty original shelter fold")
            X, T = features(train, test, variables)
            beta = ridge_fit(X, [x["outcome"] for x in train])
            for z, f in zip(test, T):
                pred = sum(b * t for b, t in zip(beta, f))
                rows.append({"shelter": hold,
                             "squared_error": (z["outcome"] - pred)**2})
        block_mse = {
            b: mean(z["squared_error"] for z in rows if z["shelter"]==b)
            for b in groups
        }
        output[name] = {
            "n_plants": len(plants),
            "n_shelters": len(groups),
            "mean_shelter_rmse": sqrt(mean(block_mse.values())),
            "plant_rmse": sqrt(mean(x["squared_error"] for x in rows)),
            "by_shelter_mse": block_mse,
        }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    plants, excluded, repeated = link_plants(load_sources())
    pollen_plants = [x for x in plants
                     if x["logPollenStigma"] is not None]
    pollen_fits = (
        validate(pollen_plants, models=POLLEN_MODELS)
        if len({x["shelter"] for x in pollen_plants}) == 5
        and len(pollen_plants) >= 25 else None
    )
    comparison = validate(plants)
    def shelter_wins(candidate, reference):
        a, b = comparison[candidate]["by_shelter_mse"], (
            comparison[reference]["by_shelter_mse"]
        )
        return sum(a[k] < b[k] for k in a)
    result = {
        "schema": "iwe_hofer2022_resource_v_service_limit_v2",
        "source_doi": DOC_DOI,
        "n_source_matched_plant_trajectories": len(plants),
        "n_independent_shelters": len(set(x["shelter"] for x in plants)),
        "n_visitor_groups_rows": sum(x["visitGroupRows"] for x in plants),
        "plant_level_repeated_visitor_group_labels": repeated,
        "excluded": excluded,
        "outcome": "authors_estimated_total_seeds_per_plant_not_observed_germination",
        "visitation": "summed_observed_visitor_group_rates_per_plant_flower_day_no_daily_partner_window",
        "timestamp_provenance": "visitor_group_rates_aggregated_over_an_original_flowering_season",
        "all_water_treatments": dict(Counter(x["treatment"] for x in plants)),
        "shelter_support": dict(Counter(x["shelter"] for x in plants)),
        "all_variables_measured_in_one_field_season": True,
        "not_prospective_predictive_comparison": True,
        "estimated_effect_strict_h1": False,
        "source_body_md5_guard": True,
        "paired_shelter_win_counts": {
            "flower_plus_perflower_visits_over_flower_only":
                shelter_wins("M3_water_flowers_visitors",
                             "M1_water_and_flowers"),
            "flower_plus_perday_visits_over_flower_only":
                shelter_wins("M6_water_flowers_visitor_rate_per_day",
                             "M1_water_and_flowers"),
        },
        "pollen_receipt_stage_subset": {
            "n_plants_with_source_pollen_stigma": len(pollen_plants),
            "n_shelters": len({x["shelter"] for x in pollen_plants}),
            "measured_stage": "pollen_grains_on_stigma_no_validated_date_before_outcome",
            "models": pollen_fits,
        },
        "claim_ceiling": "single_programme_5_shelters_nonstrict_limiting_stage_diagnostic",
        "models": comparison,
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir/"resource_service_plant_audit.json").write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8"
    )
    print("HOFER_JOIN", json.dumps({
        "n": result["n_source_matched_plant_trajectories"],
        "shelters": result["shelter_support"],
        "treatments": result["all_water_treatments"],
        "n_visitor_group_rows": result["n_visitor_groups_rows"],
        "repeated_groups": repeated,
        "excluded": excluded,
    },sort_keys=True))
    print("HOFER_PREDICTIONS", json.dumps({
        name: {"shelter_rmse": v["mean_shelter_rmse"],
               "n_shelters": v["n_shelters"]}
        for name, v in result["models"].items()
    }, sort_keys=True))
    print("HOFER_POLLEN_STAGE", json.dumps({
        "n": len(pollen_plants),
        "shelters": sorted({x["shelter"] for x in pollen_plants}),
        "shelter_rmse": {
            name: v["mean_shelter_rmse"]
            for name, v in (pollen_fits or {}).items()
        },
    }, sort_keys=True))
    print("HOFER_SHELTER_WINS", json.dumps(
        result["paired_shelter_win_counts"], sort_keys=True
    ))
    print("No date-specific visitor availability or IWE strict-H1 synchrony")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
