"""Two-sided flowering-window *raw source* diagnostic, not strict IWE H1.

Read only original Zenodo files pinned by DOI, examine plant-ID joins,
first/last-flower source coordinates, raw Schinia/Mompha cost channels,
and published R model definitions. Compute only exploratory cohortwise
associations when original source date columns are genuinely numeric
calendar-day or ISO dates. Do NOT derive novel final seed fitness.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from scripts.probe_slimon2026_zenodo_source import (
    API, DOI, file_info, read_public,
)

EXPECTED_ZIP_MD5 = "151bbd516fc0032af2a2598cb5529c78"
SOURCE_PATHS = {
    "exp1": {
        "host": "Freese Stats/main_exp1.csv",
        "last": "Freese Stats/d_pheno.csv",
        "fitness": "Freese Stats/fitness_exp1.csv",
        "mompha": "Freese Stats/comp_final_sum_exp1.csv",
        "schinia_stage": "Freese Stats/df2_exp1F.csv",
    },
    "exp2": {
        "host": "Freese Stats/main_exp2.csv",
        "last": "Freese Stats/d_pheno_exp2.csv",
        "fitness": "Freese Stats/Exp 2 fitness.csv",
        "mompha": "Freese Stats/comp_final_sum_exp2.csv",
        "schinia_stage": "Freese Stats/df2_exp2F.csv",
    },
}
SCALAR_COLUMNS = {
    "host": ["first_flr", "num_flr", "geno"],
    "last": ["last_flower"],
    "fitness": ["schinia", "lg frt", "sm frt", "abort"],
    "mompha": ["FINAL_Mompha"],
}
MISSING_TOKENS = {"", "NA", "N/A", "NULL", "NAN", "NONE"}


def _load_rows(zf: ZipFile, filename: str) -> list[dict[str, str]]:
    if filename not in zf.namelist():
        raise ValueError(f"pinned original member unavailable: {filename}")
    payload = zf.read(filename).decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(StringIO(payload, newline=""))
    if reader.fieldnames is None or not ({"ID", "ID #"} & set(reader.fieldnames)):
        raise ValueError(f"missing original ID column in: {filename}")
    rows = list(reader)
    if "ID" not in reader.fieldnames and "ID #" in reader.fieldnames:
        for row in rows:
            row["ID"] = row.get("ID #", "")
    return rows


def _id_table(rows: list[dict], wanted: list[str], label: str) -> pd.DataFrame:
    data = []
    for row in rows:
        rid = str(row.get("ID") or "").strip()
        if not rid or rid.upper() in MISSING_TOKENS:
            continue
        item = {"source_plant_id": rid}
        for col in wanted:
            item[col] = row.get(col)
        data.append(item)
    table = pd.DataFrame(data)
    if table.empty:
        raise ValueError(f"no original plant-keyed rows: {label}")
    if table["source_plant_id"].duplicated().any():
        raise ValueError(f"duplicate plant ID in original {label} table; no arbitrary merge")
    return table


def _date_doy(value, year: int) -> float:
    """No dates guessed from figure axes or experimental labels."""
    if value is None or pd.isna(value):
        return np.nan
    original = str(value).strip()
    if not original or original.upper() in MISSING_TOKENS:
        return np.nan
    try:
        v = float(original)
    except ValueError:
        v = None
    if v is not None:
        return v if v.is_integer() and 1 <= v <= 366 else np.nan
    try:
        date = pd.to_datetime(original, errors="coerce", dayfirst=False)
    except (ValueError, TypeError, OverflowError):
        return np.nan
    if pd.isna(date) or date.year != year:
        return np.nan
    return float(date.dayofyear)


def _source_full_date_year(value) -> int | None:
    """Return explicit input calendar year, never cohort/experiment number."""
    if value is None or pd.isna(value):
        return None
    raw = str(value).strip()
    if not raw or raw.upper() in MISSING_TOKENS:
        return None
    if re.fullmatch(r"\d+(?:\.0+)?", raw):
        # A bare DOY does not identify a calendar year.
        return None
    parsed = pd.to_datetime(raw, errors="coerce", dayfirst=False)
    if pd.isna(parsed):
        return None
    return int(parsed.year)


def _num(value) -> float:
    try:
        if value is None or str(value).strip().upper() in MISSING_TOKENS:
            return np.nan
        x = float(value)
        return x if np.isfinite(x) else np.nan
    except (TypeError, ValueError, OverflowError):
        return np.nan


def _safe_spearman(frame: pd.DataFrame, x: str, y: str):
    sub = frame[[x, y]].dropna()
    n = len(sub)
    if n < 8 or sub[x].nunique() < 3 or sub[y].nunique() < 3:
        return {"n": n, "rho": None, "p_exploratory": None,
                "reason": "insufficient_n_or_distinct_values"}
    result = spearmanr(sub[x].to_numpy(), sub[y].to_numpy())
    return {"n": n, "rho": round(float(result.statistic), 5),
            "p_exploratory": round(float(result.pvalue), 7),
            "reason": "noncausal_outcome_exposed_exploratory_only"}


def audit_experiment(zf: ZipFile, label: str, year: int = 2023) -> dict:
    """Experiment 1/2 are source components, NOT different flowering years."""
    mapping = SOURCE_PATHS[label]
    tables = {}
    original_meta = {}
    for kind, filename in mapping.items():
        rows = _load_rows(zf, filename)
        cols = SCALAR_COLUMNS.get(kind, [])
        if kind == "schinia_stage":
            stage_ids = [str(x.get("ID", "")).strip() for x in rows
                         if str(x.get("ID", "")).strip()]
            original_meta[kind] = {
                "raw_rows": len(rows),
                "unique_keyed_plants": len(set(stage_ids)),
                "repeated_measurement_rows": len(stage_ids) - len(set(stage_ids)),
                "original_stage_columns": (
                    [c for c in rows[0].keys() if c.startswith("sf_")]
                    if rows else []
                ),
                "source_path": filename,
                "not_adult_availability_series": True,
            }
            continue
        table = _id_table(rows, cols, f"{label} {kind}")
        original_meta[kind] = {
            "raw_rows": len(rows), "unique_keyed_plants": len(table),
            "columns_used": cols, "source_path": filename,
        }
        tables[kind] = table
    combined = tables["host"].copy()
    for kind in ("last", "fitness", "mompha"):
        combined = combined.merge(
            tables[kind], on="source_plant_id", how="inner",
            validate="one_to_one",
        )
    if combined.empty:
        return {"flowering_calendar_year": year, "experiment": label,
                "status": "no_four_file_plant_join",
                "original_tables": original_meta}

    # Original exp1/exp2 are distinct experimental components, not
    # mutually exclusive 2022/2023 reproductive calendar years.
    source_date_years = {}
    for col in ("first_flr", "last_flower"):
        observed = combined[col].map(_source_full_date_year).dropna()
        source_date_years[col] = {
            str(int(y)): int(n) for y, n in observed.value_counts().items()
        }
        if any(int(y) != year for y in observed):
            raise ValueError(
                f"Original {label} {col} contains source dates outside "
                f"flowering calendar year {year}; cannot force experiment=year"
            )
    combined["first_doy"] = combined["first_flr"].map(lambda x: _date_doy(x, year))
    combined["last_doy"] = combined["last_flower"].map(lambda x: _date_doy(x, year))
    for old, new in (("num_flr", "flowers_reported"),
                     ("schinia", "schinia_fruit_count"),
                     ("FINAL_Mompha", "mompha_final_count"),
                     ("lg frt", "raw_large_fruit_count"),
                     ("sm frt", "raw_small_fruit_count"),
                     ("abort", "aborted_units_source_count")):
        combined[new] = combined[old].map(_num)

    nonnegative = ["schinia_fruit_count", "mompha_final_count",
                   "raw_large_fruit_count", "raw_small_fruit_count",
                   "flowers_reported"]
    if any((combined[c].dropna() < 0).any() for c in nonnegative):
        raise ValueError(f"source counts have negative values in {year}")
    both = combined[["first_doy", "last_doy"]].dropna()
    backwards = int((both["last_doy"] < both["first_doy"]).sum())
    correlations = []
    for date_var in ("first_doy", "last_doy"):
        for outcome in ("schinia_fruit_count", "mompha_final_count",
                        "raw_large_fruit_count", "raw_small_fruit_count"):
            m = _safe_spearman(combined, date_var, outcome)
            correlations.append({"phenology_axis": date_var,
                                 "response_component": outcome, **m})

    source_data = {}
    for x in ("first_doy", "last_doy", "schinia_fruit_count",
              "mompha_final_count", "raw_large_fruit_count",
              "raw_small_fruit_count", "flowers_reported"):
        v = combined[x]
        source_data[x] = {
            "n_nonmissing": int(v.notna().sum()),
            "n_unique": int(v.dropna().nunique()),
            "range": ([round(float(v.min()), 5), round(float(v.max()), 5)]
                      if v.notna().any() else None),
            "n_positive": int(v.gt(0).sum()),
        }
    return {
        "flowering_calendar_year": year, "experiment": label,
        "status": "exploratory_join_and_component_audit",
        "original_tables": original_meta,
        "joint_plant_ids_n": len(combined),
        "source_explicit_date_year_counts": source_date_years,
        "source_date_fields": {
            "first_flr": {"examples": combined["first_flr"].dropna().astype(str).head(3).tolist()},
            "last_flower": {"examples": combined["last_flower"].dropna().astype(str).head(3).tolist()},
        },
        "source_date_scale_crosscheck": {
            "n_both_date_values": len(both),
            "n_last_before_first": backwards,
            "day_of_year_inferred_only_from_valid_calendar_input": True,
        },
        "variable_coverage": source_data,
        "exploratory_correlations": correlations,
        "strict_h1_effect_eligible": False,
        "external_adult_partner_curve_obtained": False,
        "direct_final_seed_counts_obtained": False,
        "pooled_cross_cohort_model_performed": False,
    }


def run(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    source = json.loads(read_public(API).decode("utf-8"))
    matches = [x for x in file_info(source) if x["name"] == "Freese Stats.zip"]
    if len(matches) != 1:
        raise ValueError("original Zenodo archive metadata is not unambiguous")
    raw = read_public(matches[0]["url"])
    checksum = hashlib.md5(raw).hexdigest()
    if checksum != EXPECTED_ZIP_MD5:
        raise ValueError("original source archive MD5 changed; stop rather than analyze")
    with ZipFile(BytesIO(raw)) as zf:
        results = [audit_experiment(zf, cohort) for cohort in ("exp1", "exp2")]
    summary = {
        "schema": "iwe_slimon2026_window_edges_exploratory_v1",
        "source_doi": DOI,
        "source_archive_md5": checksum,
        "study_interaction_type": "antagonist",
        "experiment_results": results,
        "phenology_calendar_year_provenance": "both experiments have original 2023-dated first/last flowering columns",
        "confirmatory_inference_authorized": False,
        "observed_intact_mature_seed_response": False,
        "independent_adult_partner_activity": False,
        "strict_h1_effects_admitted": 0,
        "reproduction": "original individual raw fruit components, not observed intact seeds",
        "selection_warning": "outcome-exposed source and targeted hypothesis, do not interpret p-values as confirmatory",
    }
    (outdir / "raw_window_edge_diagnostic.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for year in results:
        print("EXPERIMENT", year["experiment"], "flowering_year", year["flowering_calendar_year"],
              "joined_plants", year.get("joint_plant_ids_n"),
              "date_crosscheck", year.get("source_date_scale_crosscheck"))
        print("SOURCE_DATE_FORMS", year["experiment"], json.dumps(
            year.get("source_date_fields", {}), ensure_ascii=False
        ))
        print("COVERAGE", json.dumps(year.get("variable_coverage", {})))
        for row in year.get("exploratory_correlations", []):
            print("CORRELATION", json.dumps({
                "experiment": year["experiment"],
                "flowering_calendar_year": year["flowering_calendar_year"], **row
            }))
    print("Strict-H1: zero newly admitted, observed final seed counts: none")
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", type=Path, required=True)
    args = p.parse_args()
    run(args.outdir)


if __name__ == "__main__":
    main()
