"""Published-margins-only bounds for Riemer et al. 2024 field classification.

The underlying field-level predictions are NOT public in IWE. This module
only enumerates possible 2x2 correctness tables compatible with the original
Table 4 marginal error counts. It does not reconstruct unseen field rows and
the exact McNemar tail areas are conditional diagnostics, not an unbiased
post-selection significance test of generalizable forecast skill.
"""
from __future__ import annotations

import csv
from math import comb
from pathlib import Path

SOURCE = Path("data/source_reconstructions/riemer2024_pea_moth_prediction.csv")


def reconstruct_counts(row: dict[str, str]) -> dict[str, int]:
    """Uniquely recover integers from 2-d.p. published percentages or fail."""
    n = int(row["n_fields"])
    if n < 1:
        raise ValueError("n_fields must be positive")
    count_keys = {
        "correct": "correct_pct",
        "overestimated": "overestimated_pct",
        "underestimated": "underestimated_pct",
    }
    counts: dict[str, int] = {}
    for label, key in count_keys.items():
        percent = float(row[key])
        possible = [
            count for count in range(n + 1)
            if abs(round(100 * count / n, 2) - percent) < 1e-8
        ]
        if len(possible) != 1:
            raise ValueError(f"{row['model']} {key} is not an unambiguous 2-d.p. count")
        counts[label] = possible[0]
    if sum(counts.values()) != n:
        raise ValueError("Table 4 marginal categories do not sum to number of fields")
    return counts


def exact_conditional_mcnemar_p(better: int, worse: int) -> float:
    """Two-sided binomial McNemar exact tail conditional on discordance.

    This is mathematically valid for a *fixed paired classification*; however,
    it is NOT treated here as a calibrated publication-level p-value because
    original predictions, model-selection uncertainty and year grouping are
    unavailable.
    """
    if min(better, worse) < 0:
        raise ValueError("negative discordance")
    n = better + worse
    if n == 0:
        return 1.0
    small = min(better, worse)
    return min(1.0, 2 * sum(comb(n, i) for i in range(small + 1)) / 2**n)


def published_margins_bounds(source: Path = SOURCE) -> dict:
    with source.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_name = {row["model"]: row for row in rows if row["model"].startswith("M")}
    if set(by_name) != {"M1", "M2", "M3", "M4"}:
        raise ValueError("Riemer source reconstruction must have M1-M4 exactly once")
    left, right = by_name["M1"], by_name["M3"]
    if left["predictors"] != "flowering_onset_only" or right["predictors"] != "first_moth_arrival_x_flowering":
        raise ValueError("unexpected published predictor comparison")
    if left["source"] != "Riemer_et_al_2024_Table3_4" or right["source"] != "Riemer_et_al_2024_Table3_4":
        raise ValueError("unverified source for published Table 4 marginals")
    if left["n_fields"] != right["n_fields"] or int(left["n_fields"]) != 88:
        raise ValueError("source did not measure same 88 fields")
    a, b = reconstruct_counts(left), reconstruct_counts(right)
    n = int(left["n_fields"])
    a_error = n - a["correct"]
    b_error = n - b["correct"]
    if a_error != a["overestimated"] + a["underestimated"] or b_error != b["overestimated"] + b["underestimated"]:
        raise ValueError("error decompositions do not agree")

    possibilities = []
    for shared_wrong in range(max(0, a_error + b_error - n), min(a_error, b_error) + 1):
        fixed_only_wrong = a_error - shared_wrong
        new_only_wrong = b_error - shared_wrong
        both_correct = n - shared_wrong - fixed_only_wrong - new_only_wrong
        if min(fixed_only_wrong, new_only_wrong, both_correct) < 0:
            raise AssertionError("invalid overlap")
        possibilities.append({
            "both_wrong": shared_wrong,
            "m1_wrong_m3_right": fixed_only_wrong,
            "m1_right_m3_wrong": new_only_wrong,
            "both_right": both_correct,
            "conditional_exact_two_sided_p": exact_conditional_mcnemar_p(
                fixed_only_wrong, new_only_wrong),
        })
    return {
        "n_fields": n,
        "M1": a,
        "M3": b,
        "m3_minus_m1_correct": b["correct"] - a["correct"],
        "m3_minus_m1_underestimated": b["underestimated"] - a["underestimated"],
        "rmse_reduction_pct": 100 * (
            1 - float(right["loocv_rmse_pct"]) / float(left["loocv_rmse_pct"])
        ),
        "all_compatible_2x2_correctness_tables": possibilities,
        "conditional_p_min": min(x["conditional_exact_two_sided_p"] for x in possibilities),
        "conditional_p_max": max(x["conditional_exact_two_sided_p"] for x in possibilities),
        "source_only_no_field_level_join": True,
        "forecast_significance_identified": False,
        "year_blocked_validation_available": False,
        "effective_stage_test": False,
    }


def render_bounds(source: Path = SOURCE) -> str:
    a = published_margins_bounds(source)
    lines = [
        "# Riemer 2024: paired classification margins, not identified transitions",
        "",
        "_Generated from the 2024 article Tables 3–4 via "
        "data/source_reconstructions/riemer2024_pea_moth_prediction.csv._",
        "",
        "## Published source totals",
        "",
        f"- 88 fields; flowering-only M1: **{a['M1']['correct']} correct, "
        f"{a['M1']['overestimated']} overestimated, "
        f"{a['M1']['underestimated']} underestimated**.",
        f"- First-moth-arrival × flowering M3: **{a['M3']['correct']} correct, "
        f"{a['M3']['overestimated']} overestimated, "
        f"{a['M3']['underestimated']} underestimated**.",
        f"- Net correct-classification gain: **{a['m3_minus_m1_correct']} fields**; "
        f"underestimation difference: **{a['m3_minus_m1_underestimated']} fields**.",
        f"- Field-wise LOOCV RMSE reduction: **{a['rmse_reduction_pct']:.1f}%** "
        "(published model summaries; no newly fit model).",
        "",
        "## Every mathematically compatible field correctness table",
        "",
        "The source has not released an exact 88-field paired prediction table. "
        "The intersection of the M1 and M3 wrong-field sets is therefore unknown. "
        "With 13 M1 mistakes and four M3 mistakes, the intersection can have "
        "**0 through 4** fields; all five possibilities are listed, with no "
        "synthetic field records or inferred overlap.",
        "",
        "| Wrong under both | M1 wrong / M3 right | M1 right / M3 wrong | "
        "Right under both | Conditional exact McNemar two-sided tail |",
        "|---:|---:|---:|---:|---:|",
    ]
    for x in a["all_compatible_2x2_correctness_tables"]:
        lines.append(
            f"| {x['both_wrong']} | {x['m1_wrong_m3_right']} | "
            f"{x['m1_right_m3_wrong']} | {x['both_right']} | "
            f"{x['conditional_exact_two_sided_p']:.6f} |"
        )
    lines.extend([
        "",
        f"The conditional two-sided tail area ranges **"
        f"{a['conditional_p_min']:.6f}–{a['conditional_p_max']:.6f}** "
        "over every algebraically compatible overlap. These numbers are "
        "**not a new reported inferential p-value**: original models were "
        "compared/selected using the same data; outcomes and field-year "
        "correlations are unavailable, and no independent-year validation "
        "has been performed. Do not label the improvement confirmed in "
        "a fresh year or use McNemar significance to promote it.",
        "",
        "## Scientific boundary",
        "",
        "- The **nine-field net classification advantage** is supported by "
        "source marginals and does not require knowing which fields changed.",
        "- The identity of improved vs worsened fields, error covariance, "
        "year-by-year performance, false-negative rate and generalization "
        "to unseen seasons remain unidentifiable from these totals.",
        "- First *male* trap occurrence is an independently measured adult "
        "proxy, not direct female oviposition or a delayed larval survival filter.",
        "- M3 adds an adult-arrival × flowering statistical interaction; "
        "there is no adult-only or truly host-filtered stage-specific "
        "comparator in Tables 3–4.",
        "- There is also a textual inconsistency in the original article: "
        "Table 3 lists M4 LOOCV MAE as **4.85**, whereas the paragraph "
        "below Table 3 cites **4.70**. Use the printed Table 3 value, "
        "flag the discrepancy, and do not invent revised field predictions.",
        "",
        "**Decision:** Retain Riemer as a strong within-corpus "
        "adult-plus-host-timing diagnostic, not a confirmatory "
        "effective-consumer-window superiority or strict-H1 SMD.",
        "",
        "Source: Riemer, Schieler & Saucke (2024), "
        "https://doi.org/10.1111/eea.13430 (Tables 3–4 and data availability).",
        "",
    ])
    return "\n".join(lines)
