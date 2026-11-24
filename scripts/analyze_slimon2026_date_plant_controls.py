"""Nonpromoting matched-visit open-flower/Mompha diagnostic.

The original positive 'new Mompha' weekly tally is a detection of a
host-associated stage, NOT adult availability, attack/oviposition date,
or post-larval intact seed fitness. Three descriptive contrasts answer
different questions: pooled plant-visits, within-date comparisons
(control seasonal sampling), and within-plant comparisons (control
stable plant propensity). No causal estimand, repeated-visit n inflation,
or strict IWE H1 outcome is claimed.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
from io import BytesIO
import json
from pathlib import Path
import time
from zipfile import ZipFile

import numpy as np
import pandas as pd

from scripts.analyze_slimon2026_window_edges import (
    EXPECTED_ZIP_MD5, _load_rows, _num
)
from scripts.analyze_slimon2026_plant_visit_stage_lag import (
    SOURCE, survey_dates, original_id_map,
)
from scripts.probe_slimon2026_zenodo_source import API, DOI, file_info, read_public

N_BOOT = 400
SEED = 20261010


def extract_original_panel(zf: ZipFile, experiment: str) -> pd.DataFrame:
    """Never approximate dates or interpret missing cells as zero."""
    mapping = SOURCE[experiment]
    flowers = _load_rows(zf, mapping["flowers"])
    mompha = _load_rows(zf, mapping["mompha_new"])
    flower_days = survey_dates(flowers, "flowers")
    mompha_days = survey_dates(mompha, "mompha_new")
    by_flower = original_id_map(flowers, "flowers")
    by_mompha = original_id_map(mompha, "new Mompha")
    shared_ids = sorted(set(by_flower) & set(by_mompha))
    dates = sorted(set(flower_days) & set(mompha_days))
    if not shared_ids or not dates:
        raise ValueError("original same plant and date overlap absent")
    rows = []
    for id_ in shared_ids:
        for doy in dates:
            a = _num(by_flower[id_][flower_days[doy]])
            b = _num(by_mompha[id_][mompha_days[doy]])
            if not np.isfinite(a) or not np.isfinite(b):
                continue
            if a < 0 or b < 0 or a % 1 or b % 1:
                raise ValueError("original plant-day cell is not a nonnegative count")
            rows.append({
                "source_plant_id": id_, "doy": doy,
                "open_flower_snapshot": int(a > 0),
                "mompha_positive": int(b > 0),
                "source_visible_mompha_count": int(b),
            })
    panel = pd.DataFrame(rows)
    if panel.empty or panel.duplicated(["source_plant_id", "doy"]).any():
        raise ValueError("missing or duplicate source plant-day panel")
    return panel


def _weighted_strata_estimate(
    groups: np.ndarray,
    plant_indices: np.ndarray,
    exposure: np.ndarray,
    response: np.ndarray,
    plant_weights: np.ndarray,
    min_group: int = 1,
) -> dict:
    """Harmonic balance-weighted within-stratum positive-rate contrast.

    Plant weights are bootstrap resampling multiplicities. Report RD,
    not an odds ratio. The comparison stays descriptive.
    """
    w = plant_weights[plant_indices].astype(float)
    n_strata = int(groups.max()) + 1
    pos_e = np.bincount(groups, weights=w * exposure, minlength=n_strata)
    neg_e = np.bincount(groups, weights=w * (1 - exposure), minlength=n_strata)
    hits_e = np.bincount(groups, weights=w * exposure * response, minlength=n_strata)
    hits_n = np.bincount(groups, weights=w * (1 - exposure) * response, minlength=n_strata)
    eligible = (pos_e >= min_group) & (neg_e >= min_group)
    if not eligible.any():
        return {"risk_difference": None, "n_comparable_strata": 0,
                "effective_weight": 0}
    p1 = np.divide(hits_e, pos_e, out=np.zeros_like(hits_e), where=pos_e > 0)
    p0 = np.divide(hits_n, neg_e, out=np.zeros_like(hits_n), where=neg_e > 0)
    balance = np.divide(pos_e * neg_e, pos_e + neg_e,
                        out=np.zeros_like(pos_e), where=(pos_e + neg_e) > 0)
    balance[~eligible] = 0.
    value = float(np.dot(balance, p1 - p0) / balance.sum())
    return {
        "risk_difference": round(value, 7),
        "n_comparable_strata": int(eligible.sum()),
        "effective_weight": round(float(balance.sum()), 4),
    }


def summarize_panel(panel: pd.DataFrame, n_boot: int = N_BOOT,
                    seed: int = SEED) -> dict:
    if n_boot < 0:
        raise ValueError("n_boot must be >= 0")
    data = panel.sort_values(["source_plant_id", "doy"]).copy()
    if data.duplicated(["source_plant_id", "doy"]).any():
        raise ValueError("cannot count duplicate same-plant visits")
    plants, plant_i = np.unique(data.source_plant_id.to_numpy(), return_inverse=True)
    days, day_i = np.unique(data.doy.to_numpy(dtype=int), return_inverse=True)
    exp = data.open_flower_snapshot.to_numpy(dtype=float)
    outcome = data.mompha_positive.to_numpy(dtype=float)
    if not (np.isin(exp, [0, 1]).all() and np.isin(outcome, [0, 1]).all()):
        raise ValueError("source open-flower and stage positivity must be binary")
    w = np.ones(len(plants), dtype=float)
    n1 = int(exp.sum())
    n0 = len(exp) - n1
    y1 = int(np.dot(exp, outcome))
    y0 = int(np.dot(1 - exp, outcome))
    raw = ((y1 / n1) - (y0 / n0)) if n1 and n0 else None
    adjusted_date = _weighted_strata_estimate(
        day_i, plant_i, exp, outcome, w
    )
    adjusted_plant = _weighted_strata_estimate(
        plant_i, plant_i, exp, outcome, w
    )
    def interval(mode: str):
        if n_boot == 0:
            return None, 0
        rng = np.random.default_rng(seed)
        kept = []
        for _ in range(n_boot):
            sample = rng.integers(0, len(plants), size=len(plants))
            replicate_weights = np.bincount(
                sample, minlength=len(plants)
            ).astype(float)
            grouping = day_i if mode == "date" else plant_i
            z = _weighted_strata_estimate(
                grouping, plant_i, exp, outcome, replicate_weights
            )
            if z["risk_difference"] is not None:
                kept.append(z["risk_difference"])
        if len(kept) < max(20, int(n_boot * .8)):
            return None, len(kept)
        # Cluster resample addresses repeated plants only; date effects,
        # block layout, observation effort and sampling confounding
        # remain unaddressed. This is NOT a causal confidence interval.
        a, b = np.quantile(kept, [.025, .975])
        return [round(float(a), 6), round(float(b), 6)], len(kept)

    date_interval, date_boot_used = interval("date")
    plant_interval, plant_boot_used = interval("plant")
    date_records = []
    for day in days:
        subset = data.loc[data.doy == day]
        a = subset.loc[subset.open_flower_snapshot == 1]
        b = subset.loc[subset.open_flower_snapshot == 0]
        date_records.append({
            "doy": int(day),
            "n_open": len(a),
            "n_without_open": len(b),
            "positive_with_open": int(a.mompha_positive.sum()),
            "positive_without_open": int(b.mompha_positive.sum()),
            "date_difference_eligible": bool(len(a) > 0 and len(b) > 0)
        })
    return {
        "n_unique_source_plants": len(plants),
        "n_exact_date_survey_visits": len(data),
        "n_original_survey_days": len(days),
        "denominator": {
            "no_open_flower": {"n": n0, "mompha_positive": y0,
                               "fraction": round(y0 / n0, 7) if n0 else None},
            "open_flower": {"n": n1, "mompha_positive": y1,
                            "fraction": round(y1 / n1, 7) if n1 else None}
        },
        "naive_pooled_visit_risk_difference": (
            round(raw, 7) if raw is not None else None
        ),
        "date_stratified_risk_difference": adjusted_date,
        "date_stratified_cluster_plant_resampling_95pct": date_interval,
        "date_stratified_boot_valid": date_boot_used,
        "within_plant_risk_difference": adjusted_plant,
        "within_plant_cluster_resampling_95pct": plant_interval,
        "within_plant_boot_valid": plant_boot_used,
        "n_plant_cluster_bootstraps_attempted": n_boot,
        "bootstrap_seed": seed,
        "date_strata": date_records,
        "all_claims_descriptive": True,
        "true_bud_risk_denominator_available": False,
        "same_date_visible_stage_not_oviposition": True,
        "stage_detection_not_adult_partner_activity": True,
        "observed_net_plant_intact_seeds": False,
        "strict_h1_effects_admitted": 0,
    }


def _pinned_zip_bytes():
    error = None
    for trial in range(3):
        try:
            meta = json.loads(read_public(API, timeout=60).decode("utf-8"))
            candidates = [x for x in file_info(meta) if x["name"] == "Freese Stats.zip"]
            if len(candidates) != 1:
                raise ValueError("original Zenodo record ZIP listing ambiguous")
            raw = read_public(candidates[0]["url"], timeout=75)
            digest = hashlib.md5(raw).hexdigest()
            if digest != EXPECTED_ZIP_MD5:
                raise ValueError("original deposited ZIP MD5 mismatch")
            return raw
        except (OSError, TimeoutError, ValueError) as exc:
            error = exc
            if trial < 2:
                time.sleep(2)
    raise RuntimeError(
        "source not verified; do not publish biological estimates"
    ) from error


def run(outdir: Path, n_boot: int = N_BOOT) -> dict:
    raw = _pinned_zip_bytes()
    outdir.mkdir(parents=True, exist_ok=True)
    with ZipFile(BytesIO(raw)) as zf:
        data = {
            e: summarize_panel(extract_original_panel(zf, e), n_boot=n_boot)
            for e in ("exp1", "exp2")
        }
    doc = {
        "schema": "slimon2026_within_date_and_within_plant_stage_v1",
        "source_doi": DOI,
        "source_md5": EXPECTED_ZIP_MD5,
        "flowering_calendar_year": 2023,
        "results": data,
        "not_independent_two_field_seasons": True,
        "selection_status": "outcome_exposed_exploratory_analysis",
        "not_causal_or_h1": True,
    }
    (outdir / "source_panel_stage_controls.json").write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    for experiment, summary in data.items():
        print("ORIGINAL_EXPERIMENT", experiment,
              "N_PLANTS", summary["n_unique_source_plants"],
              "N_VISITS", summary["n_exact_date_survey_visits"])
        print("SOURCE_POOLED", experiment,
              json.dumps(summary["denominator"]))
        print("ADJUSTED", experiment, json.dumps({
            "naive": summary["naive_pooled_visit_risk_difference"],
            "within_same_date": summary["date_stratified_risk_difference"],
            "date_boot": summary["date_stratified_cluster_plant_resampling_95pct"],
            "within_same_plant": summary["within_plant_risk_difference"],
            "plant_boot": summary["within_plant_cluster_resampling_95pct"],
        }))
        print("SURVEYS", experiment, json.dumps(summary["date_strata"]))
    return doc


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", type=Path, required=True)
    p.add_argument("--boot", type=int, default=N_BOOT)
    args = p.parse_args()
    run(args.outdir, n_boot=args.boot)


if __name__ == "__main__":
    main()
