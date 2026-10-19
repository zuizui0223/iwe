"""Original-data year-blocked comparison of IWE temporal scales in sugar maple.

Source: Crone & Rapp (2025) original frozen Zenodo 15090572.
Spring reproductive *effort* is an ordinal tree category, not a timing date.
Outcome: count of seeds recorded during an autumn standardized collection
per tree, not intact viable seeds, offspring fitness or herbivore survival.

All datasets are retrieved afresh and source-MD5 verified. The 2012–2024
panel contains 13 time blocks, not 259 independent research programmes.
Avoid selecting post-outcome "mast years" as a response-blind exposure.

The previous-year autumn seed-count predictor is used ONLY in the
chronological train-through-2017/evaluate-2018–2024 comparison.
It is intentionally excluded from leave-one-year-out cross-validation:
future training years would otherwise contain the held-out year's seed
count in their lagged covariate, leaking the validation response.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from io import StringIO
from math import log1p
from pathlib import Path

import numpy as np

from scripts.probe_crone2025_maple_source import (
    SOURCE_MD5, _get, original_file_url,
)

RECORD = "10.5281/zenodo.15090572"
FLOWER_FILE = "HFmaple.flowering.qual.2011_2024.csv"
SEED_FILE = "HFmaple.seedcounts.2011_2024.csv"
SCORE = {"none": 0, "low": 1, "medium": 2, "high": 3}
YEARS = tuple(range(2012, 2025))
MODEL_FEATURES = {
    "constant": (),
    "focal_spring": ("focal",),
    "calendar_parity": ("parity",),
    "other_tree_spring": ("other",),
    "focal_plus_parity": ("focal", "parity"),
    "focal_plus_other": ("focal", "other"),
    "focal_other_parity": ("focal", "other", "parity"),
}
FORWARD_ADDITIONS = {
    "previous_autumn_seed_mean": ("lag",),
    "focal_plus_previous_seed_mean": ("focal", "lag"),
}


def original_csv(name: str) -> list[dict[str, str]]:
    if name not in (FLOWER_FILE, SEED_FILE):
        raise ValueError("file not frozen for this analysis")
    raw = _get(original_file_url(name))
    if hashlib.md5(raw).hexdigest() != SOURCE_MD5[name]:
        raise ValueError("original archive MD5 mismatch: " + name)
    return list(csv.DictReader(StringIO(raw.decode("utf-8-sig"))))


def _integer(value: str, field: str) -> int:
    try:
        v = int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"invalid source count {field}") from exc
    if v < 0:
        raise ValueError(f"negative original seed count {field}")
    return v


def build_panel(
    flowers: list[dict[str, str]],
    seed_counts: list[dict[str, str]],
    n_trees: int = 20,
) -> tuple[list[dict], dict]:
    """Join exact tree-by-calendar-year records, leaving missing keys missing."""
    flowering: dict[int, dict[str, int]] = defaultdict(dict)
    for row in flowers:
        year = _integer(row["year"], "flower-year")
        if year not in YEARS:
            continue
        tree = row["tree.num"].strip()
        cat = row["flowering.intensity"].strip().lower()
        if not tree or cat not in SCORE:
            raise ValueError("unknown source flowering category or tree")
        if tree in flowering[year]:
            raise ValueError(f"duplicate spring tree-year {year}/{tree}")
        flowering[year][tree] = SCORE[cat]

    if set(flowering) != set(YEARS):
        raise ValueError("required 2012–2024 spring seasons absent")
    for year in YEARS:
        if len(flowering[year]) != n_trees:
            raise ValueError(f"incorrect original flowering coverage {year}")

    harvest: dict[tuple[int, str], int] = {}
    all_autumn: dict[int, list[int]] = defaultdict(list)
    for row in seed_counts:
        date = datetime.strptime(row["date"].strip(), "%m/%d/%Y")
        year = date.year
        tree = row["tree"].strip()
        ec = _integer(row["EC.count"], "EC.count")
        jr = _integer(row["JR.count"], "JR.count")
        total = _integer(row["total.count"], "total.count")
        if ec + jr != total:
            raise ValueError("original two-observer count does not close")
        if (year, tree) in harvest:
            raise ValueError("duplicate autumn tree-year")
        harvest[year, tree] = total
        all_autumn[year].append(total)
    if set(range(2011, 2025)) - set(all_autumn):
        raise ValueError("previous-year autumn seed records incomplete")
    for year in range(2011, 2025):
        if len(all_autumn[year]) != n_trees:
            raise ValueError("wrong original autumn tree coverage")

    panel = []
    unmatched = []
    for year in YEARS:
        year_f = flowering[year]
        year_sum = sum(year_f.values())
        n_active = sum(value > 0 for value in year_f.values())
        previous_mean = sum(all_autumn[year - 1]) / n_trees
        for (yy, tree), seed_number in harvest.items():
            if yy != year:
                continue
            if tree not in year_f:
                unmatched.append({"year": year, "tree": tree,
                                  "autumn_sample_count": seed_number})
                continue
            own = year_f[tree]
            panel.append({
                "year": year,
                "tree": tree,
                "focal": float(own),
                "other": (year_sum - own) / (n_trees - 1),
                "population": year_sum / n_trees,
                "parity": float(year % 2),
                "lag": log1p(previous_mean),
                "sample_count": seed_number,
                "y_log1p": log1p(seed_number),
                "spring_active_tree_n": n_active,
            })
    panel.sort(key=lambda z: (z["year"], z["tree"]))
    for year in YEARS:
        if not any(r["year"] == year for r in panel):
            raise ValueError(f"no spring–autumn comparable trees in {year}")

    return panel, {
        "original_flowering_years": len(YEARS),
        "original_flowering_tree_years": sum(len(x) for x in flowering.values()),
        "original_autumn_tree_years": sum(
            len(v) for y, v in all_autumn.items() if y in YEARS
        ),
        "matched_tree_years": len(panel),
        "unmatched_original_autumn": unmatched,
        "n_source_year_blocks": len(YEARS),
        "source_record": RECORD,
    }


def _fit(train: list[dict], features: tuple[str, ...]) -> np.ndarray:
    x = np.array([[1.0] + [r[name] for name in features]
                  for r in train], dtype=float)
    y = np.array([r["y_log1p"] for r in train])
    if len(train) < max(8, 2 * x.shape[1]):
        raise ValueError("too few training rows")
    coeff, *_ = np.linalg.lstsq(x, y, rcond=None)
    if np.linalg.matrix_rank(x) < x.shape[1]:
        raise ValueError("model columns rank deficient")
    return coeff


def _predict(r: dict, coef: np.ndarray, features: tuple[str, ...]) -> float:
    x = np.array([1.0] + [r[name] for name in features])
    return float(np.dot(x, coef))


def _score(errors: list[float]) -> dict:
    return {
        "rmse_log1p_count": round(float(np.sqrt(np.mean(
            np.square(errors)))), 6),
        "mae_log1p_count": round(float(np.mean(np.abs(errors))), 6),
    }


def evaluate(panel: list[dict], train_through: int = 2017) -> dict:
    """Hold out whole years; never score training samples as validation."""
    if len({r["year"] for r in panel}) < 9:
        raise ValueError("insufficient independent original year blocks")

    scopes = {
        "all_tree_years": panel,
        "spring_active_years": [
            r for r in panel if r["spring_active_tree_n"] >= 5
        ],
        "actually_flowering_trees": [
            r for r in panel
            if r["spring_active_tree_n"] >= 5 and r["focal"] > 0
        ],
    }
    out = {}
    for scope_name, rows in scopes.items():
        ys = sorted({r["year"] for r in rows})
        if len(ys) < 5:
            raise ValueError("insufficient years for pre-outcome scope")

        loo = {}
        for model, feat in MODEL_FEATURES.items():
            e = []
            per_year = {}
            for heldout in ys:
                train = [r for r in rows if r["year"] != heldout]
                test = [r for r in rows if r["year"] == heldout]
                b = _fit(train, feat)
                errors = [
                    r["y_log1p"] - _predict(r, b, feat) for r in test
                ]
                e.extend(errors)
                per_year[str(heldout)] = _score(errors)[
                    "rmse_log1p_count"
                ]
            loo[model] = {
                **_score(e),
                "heldout_year_count": len(ys),
                "per_year_rmse": per_year,
            }

        chronological = {}
        train = [r for r in rows if r["year"] <= train_through]
        test = [r for r in rows if r["year"] > train_through]
        train_ys = {r["year"] for r in train}
        test_ys = {r["year"] for r in test}
        if not test or len(train_ys) < 4 or len(test_ys) < 3:
            raise ValueError("insufficient truly future year cohorts")
        for model, features in {
            **MODEL_FEATURES, **FORWARD_ADDITIONS
        }.items():
            beta = _fit(train, features)
            errors = [
                r["y_log1p"] - _predict(r, beta, features) for r in test
            ]
            chronological[model] = _score(errors)

        out[scope_name] = {
            "row_count": len(rows),
            "year_blocks": ys,
            "n_year_blocks": len(ys),
            "year_loo": loo,
            "fixed_train_2012_to_2017_future_test_2018_to_2024": {
                "train_rows": len(train), "test_rows": len(test),
                "training_years": sorted(train_ys),
                "testing_years": sorted(test_ys),
                "models": chronological,
            },
            "pre_outcome_eligibility": (
                "spring observed; >=5/20 trees flowering in a year"
                + ("; focal flowering >0" if scope_name ==
                   "actually_flowering_trees" else "")
                if scope_name != "all_tree_years" else "none"
            ),
        }
    return out


def annual_summary(panel: list[dict]) -> list[dict]:
    by_year = defaultdict(list)
    for row in panel:
        by_year[row["year"]].append(row)
    out = []
    for year in sorted(by_year):
        a = by_year[year]
        out.append({
            "year": year, "matched_original_trees": len(a),
            "mean_spring_ordinal_score": round(a[0]["population"], 6),
            "spring_flowing_trees": a[0]["spring_active_tree_n"],
            "autumn_sampled_count_mean": round(
                sum(r["sample_count"] for r in a) / len(a), 6
            ),
            "autumn_count_positive_fraction": round(
                sum(r["sample_count"] > 0 for r in a) / len(a), 6
            ),
        })
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    panel, provenance = build_panel(original_csv(FLOWER_FILE),
                                    original_csv(SEED_FILE))
    # Current archive: 20 spring trees for each 2012–2024 year. One autumn
    # tree in 2022 (HF28) has no matching spring census and zero sampled
    # seeds; the unmatched response remains EXCLUDED rather than assigned
    # an invented spring category.
    if not (
        provenance["matched_tree_years"] == 259
        and provenance["unmatched_original_autumn"] ==
        [{"year": 2022, "tree": "HF28", "autumn_sample_count": 0}]
    ):
        raise ValueError("unexpected source unit coverage; review archive")
    scores = evaluate(panel)
    year_rows = annual_summary(panel)
    audit = {
        "schema": "iwe_maple_crossscale_annual_validation_v1",
        "source_integrity": "original_Zenodo_MD5_verified",
        "provenance": provenance,
        "evidence_level": "exploratory_same_original_study_not_strict_H1",
        "outcome": "log1p(autumn 30-second seed sample count per tree)",
        "not_final_fitness": True,
        "no_partner_adult_activity_or_larval_lag": True,
        "no_valid_independent_multi_site_replication": True,
        "year_blocks_not_independent_studies": True,
        "heldout_years_never_used_for_current_year_model_training":
            True,
        "source_phase_coordinate_absent": True,
        "previous_autumn_outcome_never_used_in_year_loo": True,
        "year_loo_not_prequential_forecast": True,
        "fixed_future_split_retrospectively_selected_not_pre_registered":
            True,
        "models": scores,
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    path = args.outdir / "annual_summary.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(year_rows[0]))
        w.writeheader()
        w.writerows(year_rows)
    (args.outdir / "crossscale_summary.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("IWE_MAPLE_13YEAR_SOURCE", json.dumps(provenance))
    for name, o in scores.items():
        print("IWE_MAPLE_SCOPE", name, "n", o["row_count"],
              "years", o["n_year_blocks"])
        for model in (
            "constant", "focal_spring", "calendar_parity",
            "other_tree_spring", "focal_plus_parity",
            "focal_plus_other", "focal_other_parity"
        ):
            print("IWE_MAPLE_YEAR_LOO", name, model,
                  o["year_loo"][model]["rmse_log1p_count"])
        for model in (
            "focal_spring", "focal_plus_other", "calendar_parity",
            "previous_autumn_seed_mean", "focal_plus_previous_seed_mean"
        ):
            print("IWE_MAPLE_FUTURE_2018_2024", name, model,
                  o["fixed_train_2012_to_2017_future_test_2018_to_2024"]
                   ["models"][model]["rmse_log1p_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
