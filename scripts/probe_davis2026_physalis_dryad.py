"""Independent antagonist-induced pollination filtration: original Dryad gate.

Davis, Cintron, Cohen, Tolz & Thaler (2026), Oikos e11650:
"Plant responses to herbivory shift the contributions of different
pollinator taxa to plant reproduction". Source DOI 10.5061/dryad.xpnvx0kvp.

This could test whether a plant's induced defence context changes
conversion of a verified bee visit into fruit set / fruit weight on
the SAME individually observed Physalis flower or plant.
It is not a pollinating seed predator, not a temporal phase model,
and does not provide stage-separated adult/larva availability.

Never synthesize a plant-ID-only join of per-visit fruit set records
with sampled fruit weight unless the source explicitly names a
shared flower/fruit identifier. Distinct 2020/2021 experiments cannot
be collapsed into one life-history cohort. If original source bytes
are inaccessible, report official file receipts and STOP; do not
fabricate original rows from the public README.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

SOURCE_DOI = "10.5061/dryad.xpnvx0kvp"
SOURCE_DATASET_URI = "doi%3A10.5061%2Fdryad.xpnvx0kvp"
ROOT = "https://datadryad.org"
METADATA_URI = ROOT + "/api/v2/datasets/" + SOURCE_DATASET_URI
TARGET_SOURCE_FILES = frozenset({
    "Oikos_2020_bee_behavior_observations.csv",
    "Oikos_2020_cross_season_abundance.csv",
    "Oikos_2020_focal_taxa_abundance.csv",
    "Oikos_2020_total_plant_yield.csv",
    "Oikos_2021_fruit_set_poll_obs.csv",
    "Oikos_2021_fruit_weight_poll_obs.csv",
    "Oikos_2021_nectar_pollen_foraging.csv",
    "Oikos_2021_poll_importance.csv",
})
FIELD_HINTS = (
    "plant", "fruit", "flower", "herbiv", "block", "date",
    "julian", "visit", "treat", "beetle", "bee", "morphospecies",
    "forag", "yield", "weight", "set", "poll", "taxa", "insect",
)
MAX_META_BYTES = 550_000
MAX_SINGLE_SOURCE_BYTES = 350_000


def allow_public_source_url(uri: str) -> bool:
    """Do not permit a guessed third-party download URL."""
    u = urlsplit(uri)
    if u.scheme != "https":
        return False
    host = (u.hostname or "").lower()
    if host == "datadryad.org":
        path = u.path.lower()
        return (
            path.startswith(("/api/v2/datasets/"+SOURCE_DATASET_URI).lower())
            or bool(re.fullmatch(r"/api/v2/versions/[0-9]+/files", path))
            or bool(re.fullmatch(r"/api/v2/files/[0-9]+/download", path))
            or bool(re.fullmatch(r"/stash/downloads/file_stream/[0-9]+", path))
        )
    # Public Dryad original file URLs may redirect to trusted object stores.
    return host == "s3.amazonaws.com" or host.endswith(".s3.amazonaws.com") or (
        host == "storage.googleapis.com"
    )


def fetch_original(uri: str, cap: int) -> bytes:
    if not allow_public_source_url(uri):
        raise ValueError("unapproved original source endpoint")
    req = Request(uri, headers={
        "Accept": "text/csv,application/json,application/zip,*/*;q=0.1",
        "User-Agent": "IWE-public-Physalis-2026-original-source-audit/1.0"
    })
    with urlopen(req, timeout=42) as response:
        if not allow_public_source_url(response.geturl()):
            raise ValueError("download redirected outside trusted Dryad storage")
        payload = response.read(cap + 1)
    if len(payload) > cap:
        raise ValueError("source raw data exceeds source cap")
    return payload


def profile_csv(raw: bytes, name: str) -> dict:
    """Only source-derived schema, never implied herbivore timing effects."""
    text = raw.decode("utf-8-sig")
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("source CSV empty or header only")
    separator = max((",", "\t", ";"), key=lines[0].count)
    if lines[0].count(separator) == 0:
        raise ValueError("original CSV delimiter ambiguous")
    reader = csv.DictReader(StringIO(text), delimiter=separator)
    h = reader.fieldnames or []
    if len(h) != len(set(h)) or not h:
        raise ValueError("original header missing or repeated")
    rows = list(reader)
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise ValueError("inconsistent original CSV row widths")
    def known_value(row,key):
        v = str(row.get(key, "")).strip()
        return bool(v) and v.lower() not in ("na", "nan", "null")
    columns = [
        k for k in h if any(sub in k.lower() for sub in FIELD_HINTS)
    ]
    shape = {
        key: {
            "n_nonmissing": sum(known_value(r,key) for r in rows),
            "n_distinct_nonmissing": len({
                str(r[key]).strip() for r in rows if known_value(r,key)
            }),
        }
        for key in columns
    }
    candidates = [
        ("plant_id", "julian_date", "morphospecies"),
        ("plant_id", "julian_date", "treatment"),
        ("plant_id", "treatment", "block"),
        ("plant_id", "fruit_id"),
        ("plant_id", "flower_id"),
        ("plant_id",),
    ]
    duplicates = []
    for keys in candidates:
        if all(k in h for k in keys):
            val = [tuple(row[k] for k in keys) for row in rows]
            duplicates.append({
                "original_source_key": list(keys),
                "n_distinct_keys": len(set(val)),
                "n_source_rows_with_duplicate_key":
                    len(val) - len(set(val)),
                "n_rows_with_null_key": sum(
                    not all(known_value(r,k) for k in keys) for r in rows
                ),
            })
    return {
        "original_filename":name, "n_rows":len(rows),
        "n_columns":len(h), "original_columns":h,
        "measurement_field_support":shape, "candidate_key_grains":duplicates,
        "original_body_sha256":hashlib.sha256(raw).hexdigest(),
        "source_body_inspected":True,
        "same_flower_set_weight_join_verified":False,
        "conditional_visit_stage_effect_estimated":False,
        "strict_h1_stage_effect_admitted":False,
    }


def original_version_file_listing(metadata: dict) -> tuple[str,list[dict]]:
    reference = metadata.get("_links",{}).get("stash:version",{}).get("href","")
    if re.fullmatch(r"/api/v2/versions/[0-9]+",reference) is None:
        raise ValueError("original published Dryad version missing")
    data=json.loads(fetch_original(ROOT+reference+"/files",MAX_META_BYTES))
    listed=data.get("_embedded",{}).get("stash:files",[])
    if not listed or data.get("total",len(listed)) > len(listed):
        raise ValueError("Dryad original version file inventory is incomplete")
    records=[]
    if len(listed)>20:
        raise ValueError("implausible number of source files in version")
    for item in listed:
        path=item.get("path","")
        uri=item.get("_links",{}).get("stash:download",{}).get("href","")
        # The official Dryad file inventory can exceed files printed in
        # a short public landing-page preview (e.g., source seed/fruit
        # quality endpoints). Permit only provenance-issued, precisely
        # named author Oikos 2020/2021 CSVs, and list each extra file.
        if (path!="README.md" and
                re.fullmatch(r"Oikos_202[01]_[A-Za-z0-9_]+\.csv",path) is None):
            raise ValueError("off-contract non-Oikos original file: " + path)
        if re.fullmatch(r"/api/v2/files/[0-9]+/download",uri) is None:
            raise ValueError("published file direct source link missing")
        records.append({
            "path":path,
            "download_uri":uri,
            "original_size":item.get("size"),
            "original_digest":item.get("digest"),
            "digest_type":item.get("digestType"),
        })
    names={z["path"] for z in records}
    if not TARGET_SOURCE_FILES.issubset(names):
        raise ValueError("previously documented original files missing")
    if len(names)!=len(records):
        raise ValueError("duplicate published original filenames")
    return reference,records


def audit() -> dict:
    report = {
        "schema":"iwe_davis2026_antagonist_context_pollination_source_gate_v1",
        "source_doi":SOURCE_DOI,
        "paper_doi":"10.1002/oik.11650",
        "candidate_type":"experimental_plant_herbivory_modifies_taxon_specific_bee_pollination",
        "original_source_files_retrieved":0,
        "published_original_source_manifest_verified":False,
        "same_flower_date_herbivore_context_and_fruit_identifiers_verified":False,
        "source_treatment_randomization_unit_verified":False,
        "model_estimated":False,
        "strict_iwe_h1_added":False,
        "status":"not_yet_attempted",
    }
    try:
        metadata = json.loads(fetch_original(METADATA_URI,MAX_META_BYTES))
        report["dataset_title"]=metadata.get("title")
        original_version,files=original_version_file_listing(metadata)
        report["published_original_source_manifest_verified"]=True
        report["original_version_link"]=original_version
        report["n_original_version_files"]=len(files)
        report["additional_original_version_files"]=sorted({
            z["path"] for z in files
        }-TARGET_SOURCE_FILES)
        attempts=[]
        profiles=[]
        for item in files:
            file_id=item["download_uri"].split("/")[4]
            routes=[
                ROOT+item["download_uri"],
                ROOT+"/stash/downloads/file_stream/"+file_id,
            ]
            record={k:v for k,v in item.items() if k!="download_uri"}
            original=None
            for route in routes:
                try:
                    original=fetch_original(route,MAX_SINGLE_SOURCE_BYTES)
                    break
                except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc:
                    record.setdefault("blocked_source_routes",[]).append(
                        type(exc).__name__+":"+
                        (str(exc.code) if isinstance(exc,HTTPError)
                         else str(exc)[:75])
                    )
            if original is None:
                record["status"]="original_data_access_blocked"
                attempts.append(record)
                continue
            record["status"]="original_data_retrieved"
            report["original_source_files_retrieved"]+=1
            record["original_body_sha256"]=hashlib.sha256(original).hexdigest()
            digest_type=str(item.get("digest_type") or "").lower()
            digest=str(item.get("original_digest") or "").lower()
            if digest_type in ("sha256", "sha-256") and (
                digest != record["original_body_sha256"].lower()
            ):
                raise ValueError("original Dryad SHA-256 differs from metadata")
            if item["path"].lower().endswith(".csv"):
                profiles.append(profile_csv(original,item["path"]))
            elif item["path"]=="README.md":
                source_text=original.decode("utf-8-sig")
                lines=source_text.splitlines()
                fragments=[
                    {"line":i+1,"short_source_text":line[:180]}
                    for i,line in enumerate(lines)
                    if any(k in line.lower() for k in FIELD_HINTS)
                ]
                profiles.append({
                    "original_filename":item["path"],
                    "n_source_readme_lines":len(lines),
                    "original_body_sha256":hashlib.sha256(original).hexdigest(),
                    "source_unit_and_endpoint_leads":fragments[:65],
                    "same_flower_set_weight_join_verified":False,
                })
            attempts.append(record)
        report["source_attempts"]=attempts
        report["recovered_original_schema"]=profiles
        report["status"]=(
            "original_source_files_recovered_not_yet_eligible"
            if report["original_source_files_retrieved"]==len(TARGET_SOURCE_FILES)
            else "original_file_access_partial_or_blocked"
        )
    except (HTTPError,URLError,TimeoutError,OSError,ValueError,
            json.JSONDecodeError,TypeError) as exc:
        report["status"]="original_dataset_manifest_unavailable"
        report["original_source_error"]=type(exc).__name__+":"+str(exc)[:190]
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--outdir",required=True,type=Path)
    a=parser.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    outcome=audit()
    (a.outdir/"physalis2026_source_admission.json").write_text(
        json.dumps(outcome,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print("PHYSALIS2026_SOURCE_GATE",outcome["status"],
          "original_files",outcome["original_source_files_retrieved"],
          "manifest",outcome["published_original_source_manifest_verified"],
          "error",outcome.get("original_source_error"))
    for v in outcome.get("source_attempts",[]):
        print("PHYSALIS2026_ORIGINAL_FILE",v["path"],v["status"],
              v.get("blocked_source_routes",[]))
    for v in outcome.get("recovered_original_schema",[]):
        print("PHYSALIS2026_SCHEMA",v["original_filename"],
              "N",v.get("n_rows"),"fields",v.get("original_columns"),
              "key_grains",v.get("candidate_key_grains"),
              "README_LEADS",v.get("source_unit_and_endpoint_leads",[])[:30])
    print("Never promote insect source exposure or same plant fruit without source join")
    return 0 if outcome["published_original_source_manifest_verified"] else 2


if __name__=="__main__":
    raise SystemExit(main())
