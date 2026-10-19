"""Original-data, non-confirmatory 3-plant-species pollination-window diagnostic.

de Manincor, Fisogni & Rafferty (2023), Ecology Letters, DOI 10.1111/ele.14158.
Frozen source: Zenodo 10.5281/zenodo.7264150 (2021 eight-arenas experiment).

Unlike the maple annual audit, both flower counts and independently recorded
arena-level bee density have dated observations, linked to sampled-fruit seed
set on a single plant identifier. The strict data contract uses all original
byte-level MD5 hashes, drops incomplete original sampled fruits and excludes
any derived seed-summary/raw-seed disagreement. Warming is randomized among
8 arenas, NOT among 181 plants.

This is NOT final lifetime viable seeds, not a causal test of flower stage
synchrony, and not strict IWE H1. It is a targeted, outcome-exposed pilot
comparing a calendar predictor with an adult-density-by-bloom predictor on
the same plant sample, leaving entire arenas out of fit/validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from math import isfinite, log1p, sqrt
from pathlib import Path
from statistics import mean, median
from urllib.parse import quote
from urllib.request import Request, urlopen

RECORD = "7264150"
DOI = "10.5281/zenodo.7264150"
PINNED_MD5 = {
    "seeds.txt": "2a5edcf8fd3b8c6453311689e61c988b",
    "seedset_flowervisit.txt": "67d397770a759cfb3f80738cbe14b080",
    "flower_count.txt": "8b97c1cb2ae12b5d141f1e5d44120f10",
    "bee_density.txt": "ca630dc9ff10e55b28b4edc026243a25",
    "flower_onset.txt": "9a15baeefc087e0dfe9fb574b422336f",
}
SOURCE_ROWS = {
    "seeds.txt": 600,
    "seedset_flowervisit.txt": 234,
    "flower_count.txt": 9266,
    "bee_density.txt": 184,
    "flower_onset.txt": 318,
}
ARENAS = ("C1", "C2", "C3", "C4", "W5", "W6", "W7", "W8")
SPECIES = ("CH", "NM", "PC")
# Bounded, training-standardized least squares with fixed regularization.
RIDGE = 0.05
MODELS = {
    "M0_host_context": ("treatment", "species", "logFlowers"),
    "M1_host_calendar": ("treatment", "species", "logFlowers", "onset"),
    "M2_adult_mean": ("treatment", "species", "logFlowers", "adultMean"),
    "M3_flower_bee_overlap": (
        "treatment", "species", "logFlowers", "flowerBeeOverlap"
    ),
    "M4_calendar_and_overlap": (
        "treatment", "species", "logFlowers", "onset", "flowerBeeOverlap"
    ),
    "M5_realized_visits": ("treatment", "species", "logFlowers", "visrates"),
}


def read_original(name: str) -> bytes:
    if name not in PINNED_MD5:
        raise ValueError("source not in frozen Zenodo manifest")
    url = (
        "https://zenodo.org/records/" + RECORD + "/files/"
        + quote(name, safe="") + "?download=1"
    )
    with urlopen(Request(url, headers={
        "User-Agent": "IWE-original-interaction-window-audit/1.0",
        "Accept": "text/plain,*/*",
    }), timeout=40) as response:
        raw = response.read(600_000)
    if len(raw) >= 600_000:
        raise ValueError("unexpected oversized source")
    if hashlib.md5(raw).hexdigest() != PINNED_MD5[name]:
        raise ValueError("source checksum mismatch: " + name)
    return raw


def source_rows(raw: bytes, name: str) -> list[list[str]]:
    lines = [x.strip() for x in raw.decode("utf-8-sig").splitlines()
             if x.strip()]
    if not lines:
        raise ValueError("empty original file: " + name)
    head = lines.pop(0).split()
    # Original author header has TWO words "plant sp" for one field;
    # rows themselves have eight fields. Never silently shift the columns.
    if name == "seedset_flowervisit.txt":
        if head != ["sp_id", "trtm", "cage", "plant", "sp", "ID",
                    "visrates", "seeds", "ovules"]:
            raise ValueError("unexpected original source header")
        expected_width = 8
    else:
        expected_width = len(head)
    rows = [line.split() for line in lines]
    if any(len(x) != expected_width for x in rows):
        raise ValueError("malformed original source row width: " + name)
    if name in SOURCE_ROWS and len(rows) != SOURCE_ROWS[name]:
        raise ValueError("original source file row count drift: " + name)
    return rows


def positive_number(token: str, label: str, allow_zero: bool = True) -> float:
    try:
        x = float(token)
    except ValueError as exc:
        raise ValueError("invalid " + label) from exc
    if not isfinite(x) or x < 0 or (not allow_zero and x == 0):
        raise ValueError("non-finite / negative " + label)
    return x


def _assert_arena(cage: str, treatment: str) -> None:
    if cage not in ARENAS or cage[0] != treatment:
        raise ValueError("unknown, duplicated or mismatched experimental arena")


def build_plants(sources: dict[str, list[list[str]]]):
    """Return validated original plant records and explicit exclusion funnel."""
    orig = {}
    for a in sources["seeds.txt"]:
        cage, trt, sp, ident = a[:4]
        _assert_arena(cage, trt)
        key = "_".join((cage, sp, ident))
        z = orig.setdefault(key, {
            "n": 0, "missing": 0, "seeds": 0, "ovules": 0
        })
        z["n"] += 1
        if a[8] == "NA" or a[9] == "NA":
            z["missing"] += 1
            continue
        z["seeds"] += positive_number(a[8], "seeds")
        z["ovules"] += positive_number(a[9], "ovules")

    onset = {}
    for a in sources["flower_onset.txt"]:
        trt, number, sp, ident, day, event = a
        cage = trt + number
        _assert_arena(cage, trt)
        if event != "1":
            continue
        key = "_".join((cage, sp, ident))
        if key in onset:
            raise ValueError("duplicated plant-onset date")
        onset[key] = positive_number(day, "first flowering day")

    bee = {}
    means = defaultdict(list)
    for a in sources["bee_density.txt"]:
        date, day, trt, number, density = a
        cage = trt + number
        _assert_arena(cage, trt)
        key = (cage, int(day))
        if key in bee:
            raise ValueError("duplicate independent arena-day bee census")
        value = positive_number(density, "bee density")
        bee[key] = value
        means[cage].append(value)
    if set(means) != set(ARENAS):
        raise ValueError("incomplete arena adult census")
    adult_mean = {c: mean(x) for c, x in means.items()}

    flowers = defaultdict(lambda: {
        "n_days": 0, "total": 0.0, "sumDay": 0.0,
        "matchedBlooms": 0.0, "matchedBeeBlooms": 0.0,
    })
    unique_plant_day = set()
    for a in sources["flower_count.txt"]:
        cage, trt, sp, ident = a[:4]
        if trt not in ("ambient", "warmed") or cage[0] != trt[0].upper():
            raise ValueError("flower treatment source mismatch")
        _assert_arena(cage, cage[0])
        day = int(a[7])
        count = positive_number(a[8], "open flower count")
        key = "_".join((cage, sp, ident))
        if (key, day) in unique_plant_day:
            raise ValueError("duplicate flower date in original individual")
        unique_plant_day.add((key, day))
        z = flowers[key]
        z["n_days"] += 1
        z["total"] += count
        z["sumDay"] += count * day
        bd = bee.get((cage, day))
        if bd is not None:
            z["matchedBlooms"] += count
            z["matchedBeeBlooms"] += count * bd

    excluded = defaultdict(int)
    plants = []
    summary_ids = set()
    for a in sources["seedset_flowervisit.txt"]:
        key, trt, cage, sp, ident, vr, sf, ov = a
        if key in summary_ids:
            raise ValueError("duplicate source summary plant ID")
        summary_ids.add(key)
        _assert_arena(cage, trt)
        if sp not in SPECIES or key != "_".join((cage, sp, ident)):
            raise ValueError("original source summary key does not match columns")
        original = orig.get(key)
        if original is None:
            excluded["no_individual_raw_source"] += 1
            continue
        final_seed = positive_number(sf, "summary seeds")
        final_ovule = positive_number(ov, "summary ovules")
        if original["seeds"] != final_seed or original["ovules"] != final_ovule:
            excluded["raw_vs_summary_disagreement"] += 1
            continue
        if original["missing"] > 0:
            excluded["uncounted_original_fruit"] += 1
            continue
        day = onset.get(key)
        if day is None:
            excluded["no_first_flowering_date"] += 1
            continue
        f = flowers.get(key)
        if f is None or f["total"] <= 0:
            excluded["no_observed_open_flower_days"] += 1
            continue
        if f["matchedBlooms"] <= 0:
            excluded["no_same_date_bee_census_during_flowering"] += 1
            continue
        denom = final_seed + final_ovule
        if denom <= 0:
            excluded["no_sampled_seed_or_ovule"] += 1
            continue
        plants.append({
            "source_id": key, "arena": cage, "treatment": trt, "species": sp,
            "seed_set": final_seed / denom,
            "sampled_seed_count": final_seed,
            "sampled_ovule_count": final_ovule,
            "n_fruit_records": original["n"],
            "onset": day,
            "logFlowers": log1p(f["total"]),
            "flowerBeeOverlap": f["matchedBeeBlooms"] / f["matchedBlooms"],
            "adultMean": adult_mean[cage],
            "beeCoverage": f["matchedBlooms"] / f["total"],
            "visrates": positive_number(vr, "individual visit-rate"),
        })
    if set(x["arena"] for x in plants) != set(ARENAS):
        raise ValueError("not all randomized arenas have eligible plants")
    return plants, dict(excluded)


def design(train, test, spec):
    columns = []
    for k in spec:
        if k == "species":
            columns.extend(("species_NM", "species_PC"))
        else:
            columns.append(k)
    continuous = [x for x in spec if x not in ("treatment", "species")]
    center = {k: mean(row[k] for row in train) for k in continuous}
    stdev = {
        k: sqrt(mean((row[k] - center[k]) ** 2 for row in train)) or 1.0
        for k in continuous
    }
    def encode(rows):
        out = []
        for z in rows:
            row = [1.0]
            for k in spec:
                if k == "species":
                    row.extend((float(z["species"] == "NM"),
                                float(z["species"] == "PC")))
                elif k == "treatment":
                    row.append(float(z["treatment"] == "W"))
                else:
                    row.append((z[k] - center[k]) / stdev[k])
            out.append(row)
        return out
    return encode(train), encode(test)


def solve_linear(a, b):
    size = len(b)
    rows = [list(a[i]) + [b[i]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        denom = rows[col][col]
        if abs(denom) < 1e-10:
            raise ValueError("singular fixed model")
        for k in range(col, size + 1):
            rows[col][k] /= denom
        for r in range(size):
            if r != col:
                mult = rows[r][col]
                for k in range(col, size + 1):
                    rows[r][k] -= mult * rows[col][k]
    return [r[-1] for r in rows]


def fit_ols(X, y, ridge=RIDGE):
    p = len(X[0])
    a = [[0.0] * p for _ in range(p)]
    b = [0.0] * p
    for row, outcome in zip(X, y):
        for i in range(p):
            b[i] += row[i] * outcome
            for j in range(p):
                a[i][j] += row[i] * row[j]
    for i in range(1, p):
        a[i][i] += ridge
    return solve_linear(a, b)


def predict_row(features, beta):
    value = sum(x * b for x, b in zip(features, beta))
    return min(1.0, max(0.0, value))


def evaluate(plants, specs=MODELS):
    arenas = tuple(sorted(set(x["arena"] for x in plants)))
    if arenas != ARENAS:
        raise ValueError("minimum support: eight complete independent arenas")
    predictions = {}
    for name, spec in specs.items():
        rows = []
        for held in arenas:
            training = [x for x in plants if x["arena"] != held]
            testing = [x for x in plants if x["arena"] == held]
            X, T = design(training, testing, spec)
            beta = fit_ols(X, [x["seed_set"] for x in training])
            for x, features in zip(testing, T):
                rows.append({
                    "arena": held, "species": x["species"],
                    "observed": x["seed_set"],
                    "predicted": predict_row(features, beta),
                })
        per_arena = {}
        for arena in arenas:
            a = [r for r in rows if r["arena"] == arena]
            per_arena[arena] = mean(
                (r["observed"] - r["predicted"]) ** 2 for r in a
            )
        predictions[name] = {
            "n_plants": len(rows), "n_arenas": len(arenas),
            "predictors": list(spec),
            "plant_rmse": sqrt(mean(
                (r["observed"] - r["predicted"]) ** 2 for r in rows
            )),
            "equal_arena_rmse": sqrt(mean(per_arena.values())),
            "per_arena_mse": per_arena,
            "per_species_rmse": {
                sp: sqrt(mean(
                    (r["observed"] - r["predicted"]) ** 2
                    for r in rows if r["species"] == sp
                )) for sp in SPECIES
            },
        }
    return predictions


def source_audit(sources, plants, excluded):
    counts = {name: len(rows) for name, rows in sources.items()}
    if counts != SOURCE_ROWS:
        raise ValueError("source row counts drift")
    return {
        "schema": "iwe_demanincor2023_service_window_original_v1",
        "source_doi": DOI,
        "article_doi": "10.1111/ele.14158",
        "source_md5_verified": True,
        "source_rows": counts,
        "plant_summary_records": counts["seedset_flowervisit.txt"],
        "matched_source_complete_plant_records": len(plants),
        "excluded_original_summary_records": excluded,
        "n_excluded": sum(excluded.values()),
        "arena_count_independent_treatment_units": len(ARENAS),
        "species": {
            sp: {"n_plants": sum(z["species"] == sp for z in plants),
                 "mean_sampled_fruit_seed_set":
                     mean(z["seed_set"] for z in plants if z["species"] == sp)}
            for sp in SPECIES
        },
        "flower_observation_coverage_on_bee_census_days":
            mean(z["beeCoverage"] for z in plants),
        "flower_observation_min_coverage": min(z["beeCoverage"] for z in plants),
        "outcome_type": "sampled_fruit_seed_formation_not_maternal_lifetime_fitness",
        "partner_metric": "independently_recorded_arena_day_bee_density_weighted_by_observed_open_flowers_on_exact_common_dates",
        "no_interpolation_of_missing_bee_days": True,
        "study_programme_count": 1,
        "strict_iwe_h1_promotion": False,
        "claim_ceiling": "exploratory_8_arena_blocked_within_programme_prediction_only",
        "hyperparameters_and_models_selected_after_discovery":
            "exploratory_fixed_ridge_0.05; no confirmatory test",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    sources = {
        name: source_rows(read_original(name), name)
        for name in PINNED_MD5
    }
    plants, excluded = build_plants(sources)
    audit = source_audit(sources, plants, excluded)
    # Main comparison uses the identical original source-complete individuals
    # and unchanged eight arena holdouts for every model.
    audit["models"] = evaluate(plants)
    # Sparse common observation days are a genuine temporal measurement
    # limitation, not missing-zero bee abundance. Exclude, do not impute.
    high_cov = [x for x in plants if x["beeCoverage"] >= 0.50]
    audit["coverage_at_least_half"] = {
        "n": len(high_cov),
        "arenas": sorted(set(x["arena"] for x in high_cov)),
        "model_comparison": evaluate(high_cov)
        if set(x["arena"] for x in high_cov) == set(ARENAS)
        else None
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # Only 24 derived species×arena summaries; never redistribute 600
    # original sampled fruit records or any source individual raw table.
    summary = {}
    for z in plants:
        k = (z["arena"], z["species"])
        summary.setdefault(k, []).append(z)
    with (args.outdir / "arena_species_derived.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "arena", "species", "n_eligible_plants", "mean_sampled_seed_set",
            "mean_flowering_onset_doy", "mean_bloom_weighted_bee_density",
            "mean_cage_bee_density",
        ])
        for (arena, sp), rows in sorted(summary.items()):
            writer.writerow([
                arena, sp, len(rows),
                round(mean(z["seed_set"] for z in rows), 7),
                round(mean(z["onset"] for z in rows), 5),
                round(mean(z["flowerBeeOverlap"] for z in rows), 6),
                round(mean(z["adultMean"] for z in rows), 6),
            ])
    print("DEMANINCOR_SOURCE_COMPLETE_PLANTS", len(plants))
    print("DEMANINCOR_SOURCE_EXCLUSIONS", json.dumps(excluded, sort_keys=True))
    print("DEMANINCOR_ARENAS", ",".join(ARENAS))
    print("DEMANINCOR_MEAN_BEE_DENSITY_COVERAGE",
          audit["flower_observation_coverage_on_bee_census_days"])
    print("DEMANINCOR_MODELS", json.dumps({
        k: {"equal_arena_rmse": v["equal_arena_rmse"],
            "plant_rmse": v["plant_rmse"]}
        for k, v in audit["models"].items()
    }, sort_keys=True))
    print("Never promote single-programme sampled-fruit seed set into strict H1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
