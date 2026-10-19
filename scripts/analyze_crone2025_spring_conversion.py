"""Source-verified exploratory annual conversion analysis for IWE.

Crone & Rapp (2025) Harvard Forest original archive: DOI 10.5281/zenodo.15090572.

QUESTION (annual scale only):
Does spring flowering intensity measured *before* seed development predict
the eventual fraction of harvested samaras with intact filled seeds?

No daily plant–adult phase, larval timing, true viable-seed germination,
or same-individual lifetime fecundity is present. The late-year mast.index
is an outcome-proximal seed-count measure and MUST NOT be substituted for
the spring predictor or labelled prospective.

Independent exposure variation is only SIX YEARS (2012–2017), not 159
independent branch-level trials. This is a descriptive pilot, no p-values.
All original bytes are re-fetched and verified against the DOI's MD5.
Original per-branch data are never redistributed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from itertools import permutations
from io import StringIO
import json
from math import isfinite, sqrt
from pathlib import Path
from statistics import mean

from scripts.probe_crone2025_maple_source import (
    SOURCE_MD5, _get, original_file_url,
)

SPRING_NAME = "HFmaple.flowering.qual.2011_2024.csv"
EXCLUSION_NAME = "HFmaple.pollenexclusion.2012_2017.csv"
SCORE = {"none": 0, "low": 1, "medium": 2, "high": 3}
# Authors' descriptive flower-bud category midpoints; not observed flower counts.
BUD_PROXY = {"none": 0, "low": 500, "medium": 5000, "high": 25000}
YEARS = tuple(range(2012, 2018))
TREATMENTS = ("control", "exclusion")
CATS = (
    "num.filled", "num.empty", "num.grub", "num.wrinkle",
    "num.small", "num.moldy", "num.exit",
)
OPTIONAL = {"num.wrinkle", "num.small", "num.moldy", "num.exit"}


def original_rows(name: str) -> list[dict[str, str]]:
    """Read an exact frozen original CSV; reject off-record or changed bytes."""
    if name not in (SPRING_NAME, EXCLUSION_NAME):
        raise ValueError("unregistered analysis source")
    raw = _get(original_file_url(name))
    if hashlib.md5(raw).hexdigest() != SOURCE_MD5[name]:
        raise ValueError("original source checksum mismatch: " + name)
    reader = csv.DictReader(StringIO(raw.decode("utf-8-sig")))
    if not reader.fieldnames:
        raise ValueError("empty CSV header: " + name)
    return list(reader)


def _count(row: dict, col: str, allow_na: bool = False) -> int | None:
    value = str(row.get(col, "")).strip()
    if value in ("", "NA"):
        if allow_na:
            return None
        raise ValueError("required numeric source field missing: " + col)
    try:
        f = float(value)
        n = int(f)
    except (TypeError, ValueError) as err:
        raise ValueError("invalid numeric source field: " + col) from err
    if n != f or n < 0:
        raise ValueError("source field must be a nonnegative count: " + col)
    return n


def _spring_by_year(rows: list[dict], expected_tree_count: int = 20) -> dict:
    by_year = defaultdict(dict)
    for row in rows:
        year = int(row["year"])
        if year not in YEARS:
            continue
        tree = row["tree.num"].strip()
        category = row["flowering.intensity"].strip().lower()
        if category not in SCORE or not tree:
            raise ValueError("unknown original spring flowering category / tree")
        if tree in by_year[year]:
            raise ValueError("duplicated original tree-year spring score")
        by_year[year][tree] = category
    if set(by_year) != set(YEARS):
        raise ValueError("incomplete 2012-2017 early flowering years")
    for year, trees in by_year.items():
        if len(trees) != expected_tree_count:
            raise ValueError(f"incomplete spring tree coverage in {year}")
    return by_year


def _spearman(x: list[float], y: list[float]) -> float:
    def ranks(z):
        ans = [0.0] * len(z)
        for value in sorted(set(z)):
            indexes = [i for i, v in enumerate(z) if v == value]
            average = mean([1 + sum(v < value for v in z)
                            + j for j in range(len(indexes))])
            for i in indexes:
                ans[i] = average
        return ans
    a, b = ranks(x), ranks(y)
    ma, mb = mean(a), mean(b)
    num = sum((u - ma) * (v - mb) for u, v in zip(a, b))
    denom = sqrt(sum((u - ma) ** 2 for u in a)
                 * sum((v - mb) ** 2 for v in b))
    return num / denom if denom else float("nan")


def _exact_permutation_p(x: list[float], y: list[float]) -> float | None:
    """Unadjusted two-sided 6! label-randomization diagnostic.

    This is exploratory (endpoints were selected after inspecting the
    source). Never interpret it as a preregistered discovery threshold.
    """
    if len(x) != 6 or len(y) != 6:
        raise ValueError("exact diagnostic requires exactly six years")
    observed = abs(_spearman(x, y))
    if not isfinite(observed):
        return None
    number = 0
    exceed = 0
    for perm in permutations(y):
        number += 1
        if abs(_spearman(x, list(perm))) >= observed - 1e-12:
            exceed += 1
    assert number == 720
    return exceed / number


def _stage_test(x: list[float], y: list[float]) -> dict:
    baseline = _loo_rmse(x, y, linear=False)
    timed = _loo_rmse(x, y, linear=True)
    rho = _spearman(x, y)
    perm_p = _exact_permutation_p(x, y)
    return {
        "spearman_annual": round(rho, 6) if isfinite(rho) else None,
        "exact_permutation_two_sided_exploratory":
            round(perm_p, 6) if perm_p is not None else None,
        "loo_year_rmse_intercept_only": round(baseline, 6),
        "loo_year_rmse_spring_linear": round(timed, 6),
        "loo_year_relative_rmse_change":
            round((timed / baseline) - 1, 6) if baseline else None,
    }


def _loo_rmse(x: list[float], y: list[float], linear: bool) -> float:
    if len(x) < 4 or len(x) != len(y):
        raise ValueError("need >=4 paired independent year means")
    squared_errors = []
    for held_out in range(len(x)):
        xx = [v for i, v in enumerate(x) if i != held_out]
        yy = [v for i, v in enumerate(y) if i != held_out]
        mx, my = mean(xx), mean(yy)
        var = sum((v - mx) ** 2 for v in xx)
        slope = (
            sum((a - mx) * (b - my) for a, b in zip(xx, yy)) / var
            if linear and var > 0 else 0.0
        )
        prediction = my + slope * (x[held_out] - mx)
        squared_errors.append((y[held_out] - prediction) ** 2)
    return sqrt(mean(squared_errors))


def analyze(
    spring_rows: list[dict],
    exclusion_rows: list[dict],
    expected_tree_count: int = 20,
) -> tuple[list[dict], dict]:
    spring = _spring_by_year(spring_rows, expected_tree_count)
    if not exclusion_rows:
        raise ValueError("no original pollen-exclusion branch records")

    groups = {}
    # Keep repeated branch rows nested in their original tree/year.
    # Tree means and pooled seed fractions answer different questions.
    tree_groups = {}
    unobserved_branches = defaultdict(int)
    for raw in exclusion_rows:
        year = int(raw["year"])
        treatment = raw["treatment"].strip().lower()
        tree = raw["tree"].strip()
        if year not in YEARS or treatment not in TREATMENTS:
            raise ValueError("unexpected source year/treatment")
        if tree not in spring[year]:
            raise ValueError("branch tree lacks observed earlier spring flowering")
        reported_total = _count(raw, "total.seed")
        literal_state = {
            col: str(raw.get(col, "")).strip() for col in CATS
        }
        if all(v in ("", "NA") for v in literal_state.values()):
            # Five original 2016 branch rows have all seed states NA,
            # num.missing=NA and an exported total.seed=0. There is NO
            # measured zero-seed outcome on these branches. The paper
            # explicitly analyzes 154 of the 159 recorded branch rows.
            if reported_total != 0:
                raise ValueError("unobserved branch with positive seed total")
            unobserved_branches[(year, treatment)] += 1
            continue
        observed = {
            col: _count(raw, col, allow_na=(col in OPTIONAL))
            for col in CATS
        }
        non_missing_sum = sum(v for v in observed.values() if v is not None)
        if non_missing_sum != reported_total:
            raise ValueError("original seed-state totals fail closure")
        tk = (year, treatment, tree)
        tg = tree_groups.setdefault(
            tk, {"n_branches": 0, "classified": 0,
                 "filled": 0, "empty": 0}
        )
        tg["n_branches"] += 1
        tg["classified"] += reported_total
        tg["filled"] += observed["num.filled"]
        tg["empty"] += observed["num.empty"]
        reported_missing = _count(raw, "num.missing", allow_na=True)
        mast = float(raw["mast.index"])
        key = (year, treatment)
        if key not in groups:
            groups[key] = {
                "year": year, "treatment": treatment,
                "source_branch_rows": 0, "tree_set": set(),
                "observed_pods": 0, "intact_filled": 0, "empty": 0,
                "recorded_predation": 0, "other_developed": 0,
                "missing_reported_count": 0, "missing_unknown_rows": 0,
                "predation_categories_unknown_rows": 0,
                "mast_indices": set(),
            }
        g = groups[key]
        g["source_branch_rows"] += 1
        g["tree_set"].add(tree)
        g["observed_pods"] += reported_total
        g["intact_filled"] += observed["num.filled"]
        g["empty"] += observed["num.empty"]
        g["recorded_predation"] += observed["num.grub"]
        for col in ("num.moldy", "num.exit"):
            if observed[col] is not None:
                g["recorded_predation"] += observed[col]
        for col in ("num.wrinkle", "num.small"):
            if observed[col] is not None:
                g["other_developed"] += observed[col]
        if observed["num.exit"] is None or observed["num.moldy"] is None:
            g["predation_categories_unknown_rows"] += 1
        if reported_missing is None:
            g["missing_unknown_rows"] += 1
        else:
            g["missing_reported_count"] += reported_missing
        g["mast_indices"].add(mast)

    if set(groups) != {(y, t) for y in YEARS for t in TREATMENTS}:
        raise ValueError("some source year/treatment groups absent")

    annual = []
    for (year, treatment), g in sorted(groups.items()):
        if len(g["mast_indices"]) != 1:
            raise ValueError("late mast index changes within one year")
        count = g["observed_pods"]
        if count == 0:
            raise ValueError("entire year-treatment lacks classified pods")
        nonempty = count - g["empty"]
        missing = g["missing_reported_count"]
        missing_is_complete = g["missing_unknown_rows"] == 0
        row = {
            "year": year,
            "treatment": treatment,
            "spring_intensity_mean_0to3": round(
                mean(SCORE[v] for v in spring[year].values()), 6),
            "spring_author_bud_proxy_mean": round(
                mean(BUD_PROXY[v] for v in spring[year].values()), 6),
            "spring_fraction_high": round(
                mean(v == "high" for v in spring[year].values()), 6),
            "spring_tree_n": len(spring[year]),
            "source_branch_rows": g["source_branch_rows"]
                + unobserved_branches[(year, treatment)],
            "observed_branch_rows": g["source_branch_rows"],
            "unobserved_all_NA_branch_rows":
                unobserved_branches[(year, treatment)],
            "distinct_branch_trees": len(g["tree_set"]),
            "classified_pods": count,
            "intact_filled": g["intact_filled"],
            "empty": g["empty"],
            "recorded_predation": g["recorded_predation"],
            "other_developed": g["other_developed"],
            "optional_predation_unknown_rows": g["predation_categories_unknown_rows"],
            "missing_reported_count": missing,
            "missing_unknown_rows": g["missing_unknown_rows"],
            "p_intact_among_classified": round(g["intact_filled"] / count, 8),
            "p_nonempty_among_classified": round(nonempty / count, 8),
            "p_intact_among_nonempty_classified":
                round(g["intact_filled"] / nonempty, 8)
                if nonempty else None,
            "p_predation_among_nonempty_recorded":
                round(g["recorded_predation"] / nonempty, 8)
                if nonempty else None,
            "p_intact_missing_worst":
                round(g["intact_filled"] / (count + missing), 8)
                if missing_is_complete else None,
            "p_intact_missing_best":
                round((g["intact_filled"] + missing) / (count + missing), 8)
                if missing_is_complete else None,
            # This is a later, outcome-proximal index; never a prospectively
            # available flowering/animal window.
            "late_seed_mast_index_retrospective": next(iter(g["mast_indices"])),
        }
        annual.append(row)

    control = [r for r in annual if r["treatment"] == "control"]
    spring_x = [r["spring_intensity_mean_0to3"] for r in control]
    intact_y = [r["p_intact_among_classified"] for r in control]
    initiated_y = [r["p_nonempty_among_classified"] for r in control]
    converted_y = [r["p_intact_among_nonempty_classified"] for r in control]
    predator_y = [r["p_predation_among_nonempty_recorded"] for r in control]
    if len(control) != len(YEARS) or any(
        v is None for v in (*predator_y, *converted_y)
    ):
        raise ValueError("incomplete annual control timing/response comparison")
    endpoint_y = {
        "initial_nonempty_proxy": initiated_y,
        "postinit_intact_conditional": converted_y,
        "intact_fraction_all_classified": intact_y,
    }
    alt_x = {
        "original_author_category_bud_proxy":
            [r["spring_author_bud_proxy_mean"] for r in control],
        "fraction_high_flowering_trees":
            [r["spring_fraction_high"] for r in control],
    }
    # Audit whether the conclusion changes when the unit is a typical
    # sampled tree, rather than a typical *classified samara*. Tree-year
    # ratios with only 2 seeds are intrinsically unstable; repeat after
    # a transparent 10-classified-samara eligibility sensitivity.
    tree_sensitivity = {}
    for minimum in (1, 10):
        stage_year_means = {name: [] for name in endpoint_y}
        included_trees = {}
        zero_classified_trees = {}
        for year in YEARS:
            tx = [v for (y, tr, _), v in tree_groups.items()
                  if y == year and tr == "control"]
            zero_classified_trees[year] = sum(
                v["classified"] == 0 for v in tx
            )
            eligible = [v for v in tx if v["classified"] >= minimum]
            included_trees[year] = len(eligible)
            if not eligible:
                raise ValueError(f"no tree-year seed fraction in {year}")
            stage_year_means["initial_nonempty_proxy"].append(
                mean((v["classified"] - v["empty"])/v["classified"]
                     for v in eligible)
            )
            positive = [v for v in eligible
                        if v["classified"] > v["empty"]]
            if not positive:
                raise ValueError(f"no nonempty original samaras in {year}")
            stage_year_means["postinit_intact_conditional"].append(
                mean(v["filled"]/(v["classified"] - v["empty"])
                     for v in positive)
            )
            stage_year_means["intact_fraction_all_classified"].append(
                mean(v["filled"]/v["classified"] for v in eligible)
            )
        tree_sensitivity[f"minimum_classified_samaras_{minimum}"] = {
            "tree_sample_count_by_year": included_trees,
            "trees_with_zero_classified_samaras_by_year":
                zero_classified_trees,
            "yearwise_tree_mean_stages": {
                key: {
                    str(year): round(value, 8)
                    for year, value in zip(YEARS, values)
                }
                for key, values in stage_year_means.items()
            },
            "stage_comparisons": {
                key: _stage_test(spring_x, values)
                for key, values in stage_year_means.items()
            },
        }

    # The >=2 exploratory split represents >=medium mean flowering, not
    # a preregistered threshold or a randomized exposure.
    high = [r for r in control if r["spring_intensity_mean_0to3"] >= 2]
    low = [r for r in control if r["spring_intensity_mean_0to3"] < 2]

    summary = {
        "schema": "iwe_crone_spring_to_seed_annual_descriptive_v1",
        "source_doi": "10.5281/zenodo.15090572",
        "source_checksum_verified": True,
        "claim": "exploratory_annual_seed_conversion_not_stage_window_or_strict_H1",
        "experimental_years": list(YEARS),
        "independent_year_clusters": len(control),
        "total_original_exclusion_rows": len(exclusion_rows),
        "total_evaluated_branch_rows": sum(
            g["source_branch_rows"] for g in groups.values()
        ),
        "total_unobserved_all_NA_branch_rows": sum(
            unobserved_branches.values()
        ),
        "unobserved_branch_years": sorted({
            year for (year, _), n in unobserved_branches.items() if n
        }),
        "spring_trees_per_year": expected_tree_count,
        "raw_rows_not_independent_exposure_replicates": True,
        "true_partner_adult_window_measured": False,
        "true_larval_stage_lag_measured": False,
        "final_fitness_definition":
            "intact filled samaras / classified harvested samaras, not total viable seeds per plant",
        "late_seed_mast_index_only_retrospective": True,
        "endpoint_comparisons": {
            key: _stage_test(spring_x, y)
            for key, y in endpoint_y.items()
        },
        "spring_scale_sensitivity": {
            scale_name: {
                endpoint: _stage_test(xs, y)
                for endpoint, y in endpoint_y.items()
            }
            for scale_name, xs in alt_x.items()
        },
        "tree_vs_samara_unit_sensitivity": tree_sensitivity,
        "tree_balanced_estimate_is_typical_sampled_tree_not_typical_seed": True,
        "spring_proxy_is_ordinal_flowering_effort_not_phase": True,
        "initial_nonempty_is_pollen_or_seed_initiation_proxy": True,
        "postinit_conversion_is_not_direct_predator_survival": True,
        "spearman_spring_vs_classified_intact_year_means":
            round(_spearman(spring_x, intact_y), 6),
        "spearman_spring_vs_recorded_predation_year_means":
            round(_spearman(spring_x, predator_y), 6),
        "loo_year_rmse_intercept_only": round(
            _loo_rmse(spring_x, intact_y, linear=False), 6
        ),
        "loo_year_rmse_spring_linear": round(
            _loo_rmse(spring_x, intact_y, linear=True), 6
        ),
        "exploratory_mean_flowering_threshold": 2.0,
        "exploratory_high_years": [r["year"] for r in high],
        "exploratory_low_years": [r["year"] for r in low],
        "high_mean_classified_intact": round(mean(
            r["p_intact_among_classified"] for r in high
        ), 6) if high else None,
        "low_mean_classified_intact": round(mean(
            r["p_intact_among_classified"] for r in low
        ), 6) if low else None,
        "high_mean_recorded_predation": round(mean(
            r["p_predation_among_nonempty_recorded"] for r in high
        ), 6) if high else None,
        "low_mean_recorded_predation": round(mean(
            r["p_predation_among_nonempty_recorded"] for r in low
        ), 6) if low else None,
        "no_statistical_significance_claim": True,
        "year_confounded_with_mast_intensity_and_other_ecology": True,
        "incomplete_missing_status_years": sorted({
            r["year"] for r in annual if r["missing_unknown_rows"]
        }),
        "incomparable_predation_category_years": sorted({
            r["year"] for r in annual
            if r["optional_predation_unknown_rows"]
        }),
    }
    return annual, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    annual, summary = analyze(
        original_rows(SPRING_NAME), original_rows(EXCLUSION_NAME)
    )
    args.outdir.mkdir(parents=True, exist_ok=True)
    with (args.outdir / "annual_plant_conversion.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=list(annual[0]))
        writer.writeheader()
        writer.writerows(annual)
    (args.outdir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for row in annual:
        print("SPRING_CONVERSION", row["year"], row["treatment"],
              "spring", row["spring_intensity_mean_0to3"],
              "branches_observed", row["observed_branch_rows"],
              "branches_all_NA", row["unobserved_all_NA_branch_rows"],
              "pods", row["classified_pods"],
              "intact", row["p_intact_among_classified"],
              "pred", row["p_predation_among_nonempty_recorded"],
              "missing_unknown", row["missing_unknown_rows"])
    print("SPRING_PILOT_SUMMARY", json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
