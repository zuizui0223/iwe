"""IWE Slimon original weekly Mompha detections: persistence versus stage lag.

The original Mompha count is a *newly observed host-associated stage*,
not an adult flight curve or an oviposition timestamp. On the exact
same original plant × 2023 date sample, evaluate whether t-7 floral
status tracks newly visible Mompha after also conditioning on t-7
visible Mompha. An additional log1p count-scale diagnostic checks
whether the binary-incidence signal is entirely a threshold artefact.
Retrospective association; no source-native measured intact seeds.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path

import numpy as np
import pandas as pd
from zipfile import ZipFile

from scripts.analyze_slimon2026_date_plant_controls import (
    _pinned_zip_bytes, extract_original_panel,
)
from scripts.analyze_slimon2026_joint_fe_weeklag import (
    TEMPORAL_AXES, match_exact_flower_neighbours, _weighted_fe_fit,
)
from scripts.analyze_slimon2026_window_edges import EXPECTED_ZIP_MD5
from scripts.probe_slimon2026_zenodo_source import DOI

SEED = 20261011
N_BOOT = 120
EXTENDED_AXES = ["prior_mompha_positive_7d"] + TEMPORAL_AXES


def original_complete_stage_panel(raw_panel: pd.DataFrame) -> pd.DataFrame:
    """Only original exactly matched t−7/t/t+7 visits, no imputed zero."""
    required = {
        "source_plant_id", "doy", "open_flower_snapshot",
        "mompha_positive", "source_visible_mompha_count",
    }
    if not required.issubset(raw_panel):
        raise ValueError("source original Mompha counts or plant dates missing")
    if raw_panel.duplicated(["source_plant_id","doy"]).any():
        raise ValueError("duplicate original plant and survey day")
    source = raw_panel[list(required)].copy()
    if source["source_visible_mompha_count"].isna().any():
        raise ValueError("source visible counts missing; do not zero fill")
    count = source["source_visible_mompha_count"].to_numpy(dtype=float)
    if not np.isfinite(count).all() or np.any(count < 0) or np.any(count % 1):
        raise ValueError("visible Mompha counts must be nonnegative integer")
    if (source["mompha_positive"].to_numpy(dtype=int) != (count > 0)).any():
        raise ValueError("original count does not match source positive stage")
    matched = match_exact_flower_neighbours(raw_panel)
    prior = source[["source_plant_id", "doy", "mompha_positive",
                    "source_visible_mompha_count"]].copy()
    prior["doy"] += 7
    prior = prior.rename(columns={
        "mompha_positive": "prior_mompha_positive_7d",
        "source_visible_mompha_count": "prior_mompha_count_7d",
    })
    matched = matched.merge(
        prior, on=["source_plant_id", "doy"], validate="one_to_one",
        how="inner",
    )
    matched = matched.merge(
        source[["source_plant_id","doy","source_visible_mompha_count"]],
        on=["source_plant_id","doy"],validate="one_to_one",how="inner"
    )
    if matched.empty:
        raise ValueError("original date and prior outcome data do not align")
    if not matched["prior_mompha_positive_7d"].isin([0,1]).all():
        raise ValueError("unrecognized original prior Mompha stage")
    return matched.sort_values(
        ["source_plant_id","doy"]
    ).reset_index(drop=True)


def source_stage_persistence_diagnostic(
    raw_panel: pd.DataFrame, n_boot: int = N_BOOT, seed: int = SEED
) -> dict:
    if not isinstance(n_boot, int) or not 0 <= n_boot <= 500:
        raise ValueError("n_boot must be an integer 0..500")
    df = original_complete_stage_panel(raw_panel)
    original_count = df["source_visible_mompha_count"].to_numpy(dtype=float)
    if not np.any(original_count > 0):
        raise ValueError("original Mompha stage has no nonzero observations")
    baseline = _weighted_fe_fit(df, [])
    if baseline["rss"] <= 1e-9:
        raise ValueError("source stage binary outcome has no within-FE variation")
    same_source_models = {
        "flowering_three_axes": TEMPORAL_AXES,
        "prior_mompha_only": ["prior_mompha_positive_7d"],
        "past_flower_and_past_mompha": [
            "prior_open_7d", "prior_mompha_positive_7d"
        ],
        "both_stage_and_all_flower_axes": EXTENDED_AXES,
    }
    fits = {
        name: _weighted_fe_fit(df, cols)
        for name, cols in same_source_models.items()
    }
    summary = {}
    for name, fit in fits.items():
        summary[name] = {
            "coefficients": {
                key: round(float(val),6)
                for key,val in fit["coefficients"].items()
            },
            "incremental_in_sample_fe_r2": round(
                float(1-fit["rss"]/baseline["rss"]),6
            ),
        }

    # Secondary count-scale sensitivity on exactly the same visits;
    # log1p(sum of *visible new observations*) does NOT identify
    # actual number of independent individuals/oviposition events.
    log_df = df.copy()
    log_df["mompha_positive"] = np.log1p(original_count)
    count_base = _weighted_fe_fit(log_df, [])
    count_fit = _weighted_fe_fit(log_df, EXTENDED_AXES)
    total_counts = int(original_count.sum())
    plant_names, plant_idx = np.unique(
        df.source_plant_id.to_numpy(),return_inverse=True
    )
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        weights = np.bincount(
            rng.integers(0,len(plant_names),size=len(plant_names)),
            minlength=len(plant_names)
        ).astype(float)
        try:
            fit = _weighted_fe_fit(df, EXTENDED_AXES, weights)
        except RuntimeError:
            continue
        boot.append(fit["coefficients"])
    intervals = {}
    for variable in EXTENDED_AXES:
        vals = [record[variable] for record in boot]
        if len(vals) >= max(20,int(.8*n_boot)):
            intervals[variable] = [
                round(float(x),6) for x in np.quantile(vals,[.025,.975])
            ]
        else:
            intervals[variable] = None
    return {
        "n_unique_original_plants":len(plant_names),
        "n_original_complete_case_plant_visits":len(df),
        "n_original_calendar_survey_dates":int(df.doy.nunique()),
        "n_mompha_positive_current":int(df.mompha_positive.sum()),
        "n_mompha_positive_prior_7d":int(df.prior_mompha_positive_7d.sum()),
        "sum_source_visible_new_mompha_counts":total_counts,
        "candidate_models_same_source_records":summary,
        "extended_model_plant_bootstrap_95pct_descriptive":intervals,
        "valid_plant_bootstrap_replicates":len(boot),
        "n_bootstrap_requested":n_boot,
        "log1p_visible_count_model": {
            "joint_coefficients": {
                key:round(float(val),6)
                for key,val in count_fit["coefficients"].items()
            },
            "joint_additional_in_sample_fe_r2": round(
                float(1-count_fit["rss"]/count_base["rss"]),6
            ) if count_base["rss"]>1e-9 else None,
        },
        "lagged_Mompha_is_previous_detection_not_prior_oviposition":True,
        "conditioning_on_prior_detection_may_control_prior_mediators":True,
        "same_2023_field_year_experiments_not_independent":True,
        "source_bud_counts_known":False,
        "source_mature_intact_seeds_measured":False,
        "independent_adult_partner_activity_known":False,
        "out_of_sample_predictive_validation":False,
        "strict_h1_effects_added":0,
    }


def run(outdir:Path, bootstrap:int=N_BOOT)->dict:
    raw = _pinned_zip_bytes()  # official original Zenodo checksum checked
    with ZipFile(BytesIO(raw)) as source:
        results={
            cohort:source_stage_persistence_diagnostic(
                extract_original_panel(source,cohort),n_boot=bootstrap
            )
            for cohort in ("exp1","exp2")
        }
    report={
        "source_doi":DOI,
        "original_zip_md5":EXPECTED_ZIP_MD5,
        "flowering_calendar_year":2023,
        "experiment_results":results,
        "work_type":"source_authenticated_exploratory_not_h1",
        "observed_oviposition_timing":False,
        "strict_h1_effects_added":0,
    }
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"original_mompha_prior_stage_control.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    for cohort,result in results.items():
        print("MOMPHA_PERSISTENCE",cohort,json.dumps(result))
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--outdir",required=True,type=Path)
    parser.add_argument("--boot",type=int,default=N_BOOT)
    args=parser.parse_args()
    run(args.outdir,bootstrap=args.boot)


if __name__=="__main__":
    main()
