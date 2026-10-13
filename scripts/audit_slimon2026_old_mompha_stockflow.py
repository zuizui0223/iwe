"""Is weekly 'old Mompha' a bookkeeping carry-forward of 'new Mompha'?

A lag correlation among source new and old Mompha must not be presented
as independent developmental evidence if older observed stages are
computed partly from earlier newly observed stage counts.

Inspect exact original Zenodo ZIP, source scripts/README and old/new
source observations at identical original plant/date. Test *literal
arithmetic identities* (not significance) on numeric complete cases.
An identity is a measurement-definition warning, not a biological
maturation parameter. No personal data, raw file redistribution, H1.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile

import numpy as np

from scripts.analyze_slimon2026_date_plant_controls import _pinned_zip_bytes
from scripts.analyze_slimon2026_new_old_mompha import (
    SOURCE, _dated_columns, _safe_unique_map, stage_grain
)
from scripts.analyze_slimon2026_window_edges import (
    _load_rows, _num, EXPECTED_ZIP_MD5
)
from scripts.probe_slimon2026_zenodo_source import DOI

MAX_SOURCE_LINE_HITS = 26
CODE_PAT = re.compile(
    r"(?i)oldmompha|momphacalc|cumsum|cum.?mompha|new.?mompha|"
    r"(?<!\w)lag\(|(?<!\w)lead\("
)


def source_program_leads(zf: ZipFile) -> dict:
    """Bounded provenance locators only, never claim code is validated biology."""
    result = {}
    for member in zf.namelist():
        low = member.lower()
        if not (low.endswith((".r", ".rmd")) and
                ("__macosx" not in low) and
                not Path(low).name.startswith("._")):
            continue
        if zf.getinfo(member).file_size > 2_000_000:
            continue
        lines = zf.read(member).decode("utf-8-sig", errors="replace").splitlines()
        hits = []
        for i, line in enumerate(lines, 1):
            if CODE_PAT.search(line):
                hits.append({
                    "original_line": i,
                    "source_excerpt_short": line.strip()[:145],
                    "bookkeeping_formula_manually_verified": False,
                })
            if len(hits) >= MAX_SOURCE_LINE_HITS:
                break
        if hits:
            result[member] = hits
    return result


def cumulative_input_metadata(zf: ZipFile, experiment: str) -> dict:
    name = "Freese Stats/momphaCALC_" + experiment + ".csv"
    if name not in zf.namelist():
        return {"file": name, "status": "file_missing"}
    rows = _load_rows(zf, name)
    headers = list(rows[0]) if rows else []
    keyed = [
        str(row.get("ID", "")).strip()
        for row in rows if str(row.get("ID", "")).strip()
        and str(row.get("ID", "")).strip().upper() not in {"NA","NULL","NAN"}
    ]
    return {
        "file":name,
        "status":"original_cumulative_helper_file_present",
        "source_rows":len(rows),
        "source_headers":headers[:60],
        "source_ids":len(set(keyed)),
        "source_rows_with_original_id":len(keyed),
        "no_assumption_about_original_bud_or_larva_tracking":True
    }


def audit_stock_flow(new_rows: list[dict], old_rows: list[dict]) -> dict:
    g_new = stage_grain(new_rows, "new")
    g_old = stage_grain(old_rows, "old")
    info = {
        "source_new_rows":g_new["original_row_count"],
        "source_old_rows":g_old["original_row_count"],
        "source_old_unkeyed_rows":g_old["source_rows_without_original_plant_id"],
        "matched_exact_source_dates":0,
        "source_plants_keyed_in_both_stages":0,
        "numeric_consecutive_original_plant_weeks":0,
        "arithmetic_identity_checks":{},
        "original_insect_individuals_tracked":False,
        "strict_h1_effects_admitted":0,
    }
    if not g_new["safe_unique_plant_grain_for_exact_join"] or not g_old[
        "safe_unique_plant_grain_for_exact_join"
    ]:
        info["status"]="blocked_duplicate_biological_plant_ids"
        return info
    dn = _dated_columns(new_rows, "new")
    do = _dated_columns(old_rows, "old")
    pair_dates = sorted(x for x in (set(dn)&set(do))
                        if (x+7) in dn and (x+7) in do)
    info["matched_exact_source_dates"]=len(pair_dates)
    if not pair_dates:
        info["status"]="no_exact_week_pairs"
        return info
    mnew = _safe_unique_map(new_rows, "new")
    mold = _safe_unique_map(old_rows, "old")
    ids = sorted(set(mnew)&set(mold))
    info["source_plants_keyed_in_both_stages"]=len(ids)
    if not ids:
        info["status"]="no_source_plant_overlap"
        return info
    formula_counts = {
        "old_following_equals_old_current_plus_new_current":0,
        "old_following_equals_old_current_plus_new_following":0,
        "old_following_equals_new_current":0,
        "old_following_equals_old_current":0,
        "old_following_at_least_old_current":0,
        "old_following_nonincreasing":0,
        "old_following_equals_zero":0,
        "old_current_positive":0,
        "new_current_positive":0,
        "old_following_positive":0,
    }
    valid = 0
    delta_sum = 0.0
    new_sum = 0.0
    for plant in ids:
        for d in pair_dates:
            a = _num(mnew[plant].get(dn[d]))
            b = _num(mnew[plant].get(dn[d+7]))
            c = _num(mold[plant].get(do[d]))
            e = _num(mold[plant].get(do[d+7]))
            if not all(np.isfinite(x) for x in (a,b,c,e)):
                continue
            if any(x<0 or x%1 for x in (a,b,c,e)):
                raise ValueError("original counted stages must be nonnegative integers")
            valid += 1
            delta_sum += e-c
            new_sum += a
            conditions = {
                "old_following_equals_old_current_plus_new_current": e == c+a,
                "old_following_equals_old_current_plus_new_following": e == c+b,
                "old_following_equals_new_current":e == a,
                "old_following_equals_old_current":e == c,
                "old_following_at_least_old_current":e >= c,
                "old_following_nonincreasing":e <= c,
                "old_following_equals_zero":e == 0,
                "old_current_positive":c > 0,
                "new_current_positive":a > 0,
                "old_following_positive":e > 0,
            }
            for key, match in conditions.items():
                formula_counts[key] += int(match)
    info["numeric_consecutive_original_plant_weeks"]=valid
    info["sum_delta_old_stage_counts"]=round(delta_sum,4)
    info["sum_same_week_new_stage_counts"]=round(new_sum,4)
    info["arithmetic_identity_checks"]={
        key: {
            "matching_original_plant_weeks":n,
            "fraction_of_numeric_week_pairs":round(n/valid,6) if valid else None,
        } for key,n in formula_counts.items()
    }
    # The diagnostic is *not* enough to certify independence even
    # when the simple identities are not exact: cleaning in R or
    # original field accounting could connect the original series.
    info["status"]="numeric_stock_flow_compared" if valid else "no_complete_numeric_pairs"
    info["original_new_old_measurement_independence_verified"]=False
    info["stock_flow_identity_is_developmental_tracking_evidence"]=False
    return info


def audit_archive(zf: ZipFile) -> dict:
    audit={}
    for exp,paths in SOURCE.items():
        audit[exp]=audit_stock_flow(
            _load_rows(zf,paths["new"]),_load_rows(zf,paths["old"])
        )
        audit[exp]["cumulative_helper"]=cumulative_input_metadata(zf,exp)
    script_sources = source_program_leads(zf)
    return {
        "schema":"iwe_slimon2026_new_old_stock_flow_dependency_v1",
        "source_doi":DOI,
        "source_zip_md5":EXPECTED_ZIP_MD5,
        "experiment_results":audit,
        "source_R_code_locators":script_sources,
        "empirical_biological_maturation_claim_admitted":False,
        "source_stage_count_derivation_authenticated":False,
        "direct_source_seeds_or_adults_recovered":False,
        "strict_h1_effects_added":0,
    }


def run(outdir: Path) -> dict:
    raw = _pinned_zip_bytes()
    with ZipFile(BytesIO(raw)) as archive:
        result = audit_archive(archive)
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"source_new_old_stock_flow_audit.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )
    for exp, out in result["experiment_results"].items():
        print("SOURCE_STOCK_FLOW",exp,json.dumps(out,ensure_ascii=False))
    for filename,hits in result["source_R_code_locators"].items():
        print("ORIGINAL_R_SOURCE_LOCATOR",filename,
              json.dumps(hits[:10],ensure_ascii=False))
    print("No untracked biological transition, original ova or seed outputs inferred")
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    args=p.parse_args()
    run(args.outdir)


if __name__=="__main__":
    main()
