"""Original same-plant, same-visit flowering versus new Mompha counts.

Tests a missing ecological link in IWE: can records of *newly observed*
Mompha (the source's wide field names) appear without simultaneous open
flowers, or outside each focal plant's recorded flowering interval?

Archive: Zenodo doi 10.5281/zenodo.19488509, exact MD5 pinned upstream.
No raw distribution, imputation, new seed counts or strict-H1 promotion.
Newly observed Mompha counts are NOT oviposition or adult flight dates.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import hashlib
from io import BytesIO
import json
from pathlib import Path
import time
import re
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from scripts.analyze_slimon2026_window_edges import (
    EXPECTED_ZIP_MD5, _date_doy, _load_rows, _num
)
from scripts.probe_slimon2026_zenodo_source import API, DOI, file_info, read_public

SOURCE = {
    "exp1": {
        "flowers": "Freese Stats/df2_exp1.csv",
        "mompha_new": "Freese Stats/df2_exp1_M.csv",
        "first": "Freese Stats/main_exp1.csv",
        "last": "Freese Stats/d_pheno.csv",
    },
    "exp2": {
        "flowers": "Freese Stats/df2_exp2.csv",
        "mompha_new": "Freese Stats/df2_exp2M.csv",
        "first": "Freese Stats/main_exp2.csv",
        "last": "Freese Stats/d_pheno_exp2.csv",
    }
}
# A date must appear in the original wide header; never assign another
# date from neighbouring surveys or absence from one sheet.
DATE_SUFFIX = re.compile(r"_(\d{1,2})_(\d{1,2})$", re.I)
YEAR = 2023


def survey_dates(rows: list[dict], signal: str) -> dict[int, str]:
    """Parse source mm_dd suffix ONLY with the expected stage prefix."""
    if not rows:
        raise ValueError("empty original wide time-series sheet")
    mapping: dict[int, str] = {}
    for original in rows[0]:
        normalized = original.lower().replace("#", "").replace("_", "")
        if not normalized.startswith("flr" if signal == "flowers" else "mompha"):
            continue
        m = DATE_SUFFIX.search(original)
        if m is None:
            continue
        try:
            doy = date(YEAR, int(m.group(1)), int(m.group(2))).timetuple().tm_yday
        except ValueError as exc:
            raise ValueError(f"Invalid date suffix: {original}") from exc
        if doy in mapping:
            raise ValueError(
                f"duplicate source survey day for {signal}: {doy} "
                f"({mapping[doy]}, {original})"
            )
        mapping[doy] = original
    if not mapping:
        raise ValueError(f"no source-dated {signal} columns")
    return mapping


def original_id_map(rows: list[dict], signal: str) -> dict[str, dict]:
    mapping = {}
    for row in rows:
        key = str(row.get("ID", "")).strip()
        if not key or key.upper() in {"NA", "NAN", "NULL"}:
            continue
        if key in mapping:
            raise ValueError(f"duplicate original plant ID in {signal}: {key}")
        mapping[key] = row
    if not mapping:
        raise ValueError(f"no original plant IDs for {signal}")
    return mapping


def audit_experiment(zf: ZipFile, name: str) -> dict:
    if name not in SOURCE:
        raise ValueError("unrecognized original experiment")
    original = SOURCE[name]
    rows = {label: _load_rows(zf, path) for label, path in original.items()}
    dates_flower = survey_dates(rows["flowers"], "flowers")
    dates_mompha = survey_dates(rows["mompha_new"], "mompha_new")
    same_date = sorted(set(dates_flower) & set(dates_mompha))

    by_id = {label: original_id_map(data, label)
             for label, data in rows.items()}
    common_ids = sorted(set.intersection(*(set(v) for v in by_id.values())))
    if not common_ids:
        raise ValueError("no four-source shared plant IDs")

    per_survey = []
    matched = []
    abnormal_values = 0
    for doy in same_date:
        matched_rows = 0
        n_zero_flower = 0
        n_event_positive = 0
        n_event_zero_flower = 0
        n_event_flowering = 0
        flower_sum = 0.
        mompha_sum = 0.
        event_counts_outside = 0.
        for pid in common_ids:
            flower_n = _num(by_id["flowers"][pid][dates_flower[doy]])
            mompha_n = _num(by_id["mompha_new"][pid][dates_mompha[doy]])
            if not np.isfinite(flower_n) or not np.isfinite(mompha_n):
                continue
            if flower_n < 0 or mompha_n < 0:
                abnormal_values += 1
                continue
            if flower_n % 1 != 0 or mompha_n % 1 != 0:
                abnormal_values += 1
                continue
            start = _date_doy(by_id["first"][pid].get("first_flr"), YEAR)
            end = _date_doy(by_id["last"][pid].get("last_flower"), YEAR)
            if not np.isfinite(start) or not np.isfinite(end) or end < start:
                phase = "missing_or_invalid_window"
            elif doy < start:
                phase = "before_first_recorded_flower"
            elif doy > end:
                phase = "after_last_recorded_flower"
            else:
                phase = "within_recorded_flower_window"
            matched_rows += 1
            flower_sum += flower_n
            mompha_sum += mompha_n
            if flower_n == 0:
                n_zero_flower += 1
            if mompha_n > 0:
                n_event_positive += 1
                if flower_n == 0:
                    n_event_zero_flower += 1
                else:
                    n_event_flowering += 1
                if phase != "within_recorded_flower_window":
                    event_counts_outside += mompha_n
            matched.append({
                "source_plant_id": pid,
                "survey_doy": doy,
                "flowers": flower_n,
                "new_mompha_observation": mompha_n,
                "phase": phase,
            })
        per_survey.append({
            "doy": doy,
            "survey_date": date(YEAR, 1, 1).fromordinal(
                date(YEAR, 1, 1).toordinal() + doy - 1
            ).isoformat(),
            "n_paired_plants": matched_rows,
            "n_plants_no_open_flower": n_zero_flower,
            "n_mompha_positive_plants": n_event_positive,
            "n_mompha_positive_without_open_flower": n_event_zero_flower,
            "n_mompha_positive_with_open_flower": n_event_flowering,
            "total_open_flower_count": int(flower_sum),
            "total_new_mompha_observations": int(mompha_sum),
            "n_mompha_positive_events_outside_recorded_window": int(
                event_counts_outside
            ),
        })

    data = pd.DataFrame(matched)
    stage = []
    if not data.empty:
        for phase, sub in data.groupby("phase", sort=True):
            stage.append({
                "phase": phase,
                "plant_visits": len(sub),
                "unique_plants": sub["source_plant_id"].nunique(),
                "n_mompha_positive_plant_visits": int(
                    sub["new_mompha_observation"].gt(0).sum()
                ),
                "sum_new_mompha_observations": int(
                    sub["new_mompha_observation"].sum()
                ),
                "n_positive_with_zero_open_flower": int((
                    sub["new_mompha_observation"].gt(0) &
                    sub["flowers"].eq(0)
                ).sum()),
            })

    date_summary = {
        "experiment": name,
        "flowering_calendar_year": YEAR,
        "source_dates_flower": len(dates_flower),
        "source_dates_mompha": len(dates_mompha),
        "n_exact_same_dates": len(same_date),
        "flower_dates_only": [date.fromordinal(date(YEAR, 1, 1).toordinal()+d-1).isoformat()
                              for d in sorted(set(dates_flower)-set(dates_mompha))],
        "mompha_dates_only": [date.fromordinal(date(YEAR, 1, 1).toordinal()+d-1).isoformat()
                              for d in sorted(set(dates_mompha)-set(dates_flower))],
        "source_shared_plant_ids": len(common_ids),
        "n_matched_plant_visits": len(data),
        "n_negative_or_fractional_source_counts_rejected": abnormal_values,
        "exact_date_survey_results": per_survey,
        "recorded_window_stage_counts": stage,
        "plant_visits_are_not_independent_replicate_experiments": True,
        "mompha_new_visible_stage_is_not_oviposition_or_adult_flight": True,
        "zero_open_flower_plant_visits_do_not_imply_plant_no_ovules": True,
        "all_detected_Mompha_not_all_lifelong_attack_records": True,
        "mature_intact_seed_n_not_measured": True,
        "strict_h1_effects_admitted": 0,
    }
    if not data.empty:
        sums = data.groupby("source_plant_id").agg(
            n_visits=("survey_doy", "size"),
            total_flower=("flowers", "sum"),
            total_new_mompha=("new_mompha_observation", "sum")
        )
        if (len(sums) >= 8 and sums["total_flower"].nunique() >= 3
                and sums["total_new_mompha"].nunique() >= 3):
            rho = spearmanr(sums.total_flower, sums.total_new_mompha)
            date_summary["per_plant_flower_mompha_spearman"] = {
                "n_plant_ids": len(sums),
                "rho_descriptive": round(float(rho.statistic), 5),
                "not_an_attack_hazard": True,
            }
    return date_summary


def run(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    # Source service can transiently time out. Retries never widen
    # search to another dataset. The original deposited byte MD5 is
    # always verified before a biological value can be interpreted.
    last_error = None
    record = None
    for attempt in range(3):
        try:
            record = json.loads(read_public(API, timeout=60).decode("utf-8"))
            break
        except (OSError, TimeoutError, ValueError) as exc:
            last_error = exc
            if attempt < 2:
                print("Zenodo official metadata transient failure; retry", attempt + 1)
                time.sleep(2)
    if record is None:
        raise RuntimeError("official metadata inaccessible; no data result") from last_error
    x = [v for v in file_info(record) if v["name"] == "Freese Stats.zip"]
    if len(x) != 1:
        raise ValueError("original source zip metadata missing")
    raw = None
    for attempt in range(3):
        try:
            raw = read_public(x[0]["url"], timeout=75)
            break
        except (OSError, TimeoutError, ValueError) as exc:
            last_error = exc
            if attempt < 2:
                print("Zenodo pinned ZIP transient failure; retry", attempt + 1)
                time.sleep(2)
    if raw is None:
        raise RuntimeError("original ZIP inaccessible; no reconstructed observation") from last_error
    md5 = hashlib.md5(raw).hexdigest()
    print("SOURCE_BYTES", len(raw), "SOURCE_MD5", md5,
          "METADATA_CHECKSUM", x[0].get("checksum"),
          "HAS_ZIP_SIGNATURE", raw[:2] == b"PK")
    if md5 != EXPECTED_ZIP_MD5:
        # Retry only this exact source-pinned archive: a network/CDN
        # error page may be binary-sized. No biological computation
        # is made from any mismatching bytes.
        print("Pinned source checksum mismatch; one exact-source retry")
        try:
            fresh = read_public(x[0]["url"], timeout=75)
        except (OSError, TimeoutError, ValueError) as exc:
            raise RuntimeError("checksum failed and exact-source retry unavailable") from exc
        raw, md5 = fresh, hashlib.md5(fresh).hexdigest()
        print("RETRY_SOURCE_BYTES", len(raw), "RETRY_MD5", md5,
              "RETRY_ZIP_SIGNATURE", raw[:2] == b"PK")
    if md5 != EXPECTED_ZIP_MD5:
        raise ValueError("original ZIP MD5 differs from frozen Zenodo source; analysis blocked")
    with ZipFile(BytesIO(raw)) as zf:
        results = [audit_experiment(zf, name) for name in ("exp1", "exp2")]
    answer = {
        "schema": "iwe_slimon2026_exact_plant_visit_stage_lag_v1",
        "source_doi": DOI, "source_md5": md5,
        "results": results,
        "causal_hazard_identified": False,
        "recorded_new_mompha_is_not_true_oviposition_date": True,
        "strict_h1_effects_admitted": 0,
    }
    (outdir / "plant_visit_stage_diagnostic.json").write_text(
        json.dumps(answer, ensure_ascii=False, indent=2)+"\n", encoding="utf-8"
    )
    for x in results:
        print("EXPERIMENT", x["experiment"], "SHARED_PLANTS",
              x["source_shared_plant_ids"], "JOINT_DATES",
              x["n_exact_same_dates"], "PAIRED_VISITS",
              x["n_matched_plant_visits"],
              "REJECTED", x["n_negative_or_fractional_source_counts_rejected"])
        print("STAGE", x["experiment"],
              json.dumps(x["recorded_window_stage_counts"], ensure_ascii=False))
        for entry in x["exact_date_survey_results"]:
            print("VISIT", x["experiment"], json.dumps(entry))
        print("CORRELATION", x["experiment"],
              json.dumps(x.get("per_plant_flower_mompha_spearman")))
    print("No H1 promotion; this is a source-observed stage/detection timing audit.")
    return answer


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", type=Path, required=True)
    args = p.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
