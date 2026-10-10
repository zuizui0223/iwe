"""Source-authenticated IWE Slimon (2026): plant/date FE and ±7-day floral status.

Exploratory ecological question: Do *newly observed* Mompha counts
co-occur more with current or the prior census's open flowers once
both source plant identity and survey date are controlled? A +7d
future flower status is included as a deliberately imperfect
negative-control timing comparator. A new Mompha count is *not* the
date of oviposition and open flowers do not measure susceptible buds.

This is descriptive two-way fixed-effect LPM and cannot supply the
original strict-H1 direct plant fitness effect.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, diags, hstack
from scipy.sparse.linalg import lsqr
from zipfile import ZipFile

from scripts.analyze_slimon2026_date_plant_controls import (
    _pinned_zip_bytes, extract_original_panel,
)
from scripts.probe_slimon2026_zenodo_source import DOI
from scripts.analyze_slimon2026_window_edges import EXPECTED_ZIP_MD5

SEED = 20261010
REPLICATIONS = 160
TEMPORAL_AXES = ["prior_open_7d", "current_open", "future_open_7d"]


def match_exact_flower_neighbours(
    original: pd.DataFrame, lag_days: int = 7,
) -> pd.DataFrame:
    """No adjacent-row shifts: require exact original dated ±7d visits."""
    if lag_days != 7:
        raise ValueError("source review covers exact one-week gaps only")
    required = {"source_plant_id", "doy", "open_flower_snapshot", "mompha_positive"}
    if not required.issubset(original):
        raise ValueError("missing original timestamp and plant fields")
    if original.duplicated(["source_plant_id", "doy"]).any():
        raise ValueError("repeated source plant-day rows not admissible")
    original = original.copy()
    base = original[["source_plant_id", "doy",
                     "open_flower_snapshot", "mompha_positive"]]
    prior = base[["source_plant_id", "doy", "open_flower_snapshot"]].copy()
    prior["doy"] = prior["doy"] + lag_days
    prior = prior.rename(columns={"open_flower_snapshot": "prior_open_7d"})
    future = base[["source_plant_id", "doy", "open_flower_snapshot"]].copy()
    future["doy"] = future["doy"] - lag_days
    future = future.rename(columns={"open_flower_snapshot": "future_open_7d"})
    joined = base.merge(prior, on=["source_plant_id", "doy"],
                        how="inner", validate="one_to_one")
    joined = joined.merge(future, on=["source_plant_id", "doy"],
                          how="inner", validate="one_to_one")
    joined = joined.rename(columns={"open_flower_snapshot": "current_open"})
    if joined.empty:
        raise ValueError("no original plant dates with both exact 7-day neighbours")
    for axis in TEMPORAL_AXES:
        if not joined[axis].isin([0, 1]).all():
            raise ValueError("unrecognized original binary flower status")
    return joined.sort_values(["source_plant_id", "doy"]).reset_index(drop=True)


def _original_twfe_design(panel: pd.DataFrame, temporal_axes: list[str]):
    """Separate calendar-day and stable source plant dummy columns."""
    labels, plant_idx = np.unique(panel["source_plant_id"].to_numpy(),
                                  return_inverse=True)
    days, date_idx = np.unique(panel["doy"].to_numpy(), return_inverse=True)
    n = len(panel)
    row = np.arange(n)
    plant = coo_matrix((np.ones(n), (row, plant_idx)),
                       shape=(n, len(labels))).tocsr()
    time = coo_matrix((np.ones(n), (row, date_idx)),
                      shape=(n, len(days))).tocsr()
    # Factor columns and temporal covariates. Full plant and date
    # intercepts are deliberately rank-deficient; min-norm LSQR
    # still identifies the slopes provided their residual variation.
    if temporal_axes:
        additional = coo_matrix(
            panel[temporal_axes].to_numpy(dtype=float)
        ).tocsr()
        design = hstack([plant, time, additional], format="csr")
    else:
        design = hstack([plant, time], format="csr")
    return design, len(labels), len(days), plant_idx


def _weighted_fe_fit(
    panel: pd.DataFrame, axes: list[str],
    cluster_weights: np.ndarray | None = None,
) -> dict:
    design, n_plants, n_dates, plant_idx = _original_twfe_design(panel, axes)
    y = panel["mompha_positive"].to_numpy(dtype=float)
    if cluster_weights is None:
        w = np.ones(len(y), dtype=float)
    else:
        if len(cluster_weights) != n_plants:
            raise ValueError("must bootstrap entire original plants")
        w = cluster_weights[plant_idx]
    root = np.sqrt(w)
    weighted_design = diags(root) @ design
    weighted_y = root * y
    result = lsqr(weighted_design, weighted_y, atol=1e-10,
                  btol=1e-10, iter_lim=2000)
    params = result[0]
    resid = weighted_y - weighted_design @ params
    # Do not interpret rank-deficient fixed effect identities as
    # biological traits or convert these coefficients to odds ratios.
    if result[1] not in {1, 2}:
        raise RuntimeError(f"two-way fixed-effect source fit failed: {result[1]}")
    return {
        "rss": float(resid @ resid),
        "coefficients": dict(zip(axes, params[-len(axes):]))
                        if axes else {},
        "n_plant_ids": n_plants,
        "n_survey_dates": n_dates,
    }


def audit_twfe(panel: pd.DataFrame, n_boot: int = REPLICATIONS,
               seed: int = SEED) -> dict:
    if n_boot < 0 or n_boot > 1000:
        raise ValueError("bootstrap count must be 0..1000")
    if panel.duplicated(["source_plant_id", "doy"]).any():
        raise ValueError("source plant/date duplicate")
    n = len(panel)
    base = _weighted_fe_fit(panel, [])
    if base["rss"] <= 1e-9:
        raise ValueError("source stage positivity has no within-plant/date variance")
    # Same biological units and source dates for every model.
    single = {}
    for axis in TEMPORAL_AXES:
        fit = _weighted_fe_fit(panel, [axis])
        single[axis] = {
            "slope_lpm": round(fit["coefficients"][axis], 6),
            "incremental_in_sample_fe_r2": round(1-fit["rss"]/base["rss"], 6),
        }
    full = _weighted_fe_fit(panel, TEMPORAL_AXES)
    coefficients = full["coefficients"]
    fits = []
    if n_boot:
        rng = np.random.default_rng(seed)
        n_plants = base["n_plant_ids"]
        for _ in range(n_boot):
            weight = np.bincount(
                rng.integers(n_plants, size=n_plants),
                minlength=n_plants
            ).astype(float)
            try:
                fit = _weighted_fe_fit(panel, TEMPORAL_AXES, weight)
            except RuntimeError:
                continue
            fits.append(fit["coefficients"])
    boot = {}
    for axis in TEMPORAL_AXES:
        estimates = [q[axis] for q in fits]
        boot[axis] = (
            [round(float(a), 6) for a in np.quantile(estimates,[.025,.975])]
            if len(estimates) >= max(20, .8*n_boot) else None
        )
    exposed = panel
    result = {
        "n_matched_plant_visits": n,
        "n_original_plants": base["n_plant_ids"],
        "n_original_survey_days": base["n_survey_dates"],
        "n_plant_boot_resamples_used": len(fits),
        "joint_source_observation_requirement": "exact_original_7day_before_and_after",
        "observable_positive_visits": int(exposed.mompha_positive.sum()),
        "current_flower_positive_visits": int(exposed.current_open.sum()),
        "prior_flower_positive_visits": int(exposed.prior_open_7d.sum()),
        "future_flower_positive_visits": int(exposed.future_open_7d.sum()),
        "single_axis_same_sample_model": single,
        "joint_twfe_slopes": {
            axis: round(float(coefficients[axis]), 6) for axis in TEMPORAL_AXES
        },
        "joint_twfe_plant_bootstrap_percentile_95pct": boot,
        "joint_in_sample_fe_incremental_r2": round(
            1-full["rss"]/base["rss"], 6
        ),
        "same_year_2023_two_experiments_not_two_independent_years": True,
        "future_flower_status_is_imperfect_negative_control": True,
        "not_predictive_out_of_sample": True,
        "strict_h1_admitted": False,
        "bud_count_measured": False,
        "oviposition_date_measured": False,
        "observed_final_intact_seeds_measured": False,
    }
    return result


def run(outdir: Path, boot: int = REPLICATIONS):
    outdir.mkdir(parents=True, exist_ok=True)
    raw = _pinned_zip_bytes()  # exact source MD5 validated before analysis
    with ZipFile(BytesIO(raw)) as original:
        analysis = {
            experiment: audit_twfe(
                match_exact_flower_neighbours(
                    extract_original_panel(original, experiment)
                ), n_boot=boot
            ) for experiment in ("exp1", "exp2")
        }
    result = {
        "source_doi": DOI, "original_archive_md5": EXPECTED_ZIP_MD5,
        "source_year": 2023, "analysis": analysis,
        "research_status": "outcome_exposed_exploratory",
        "never_treat_visible_Mompha_stage_as_adult_activity_or_oviposition": True,
        "strict_h1_effects_added": 0,
    }
    (outdir/"matched_weeklag_twfe.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    for experiment, details in analysis.items():
        print("WEEKLAG_RESULT", experiment, json.dumps(details))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--boot",type=int,default=REPLICATIONS)
    args = p.parse_args()
    run(args.outdir, args.boot)


if __name__=="__main__":
    main()
