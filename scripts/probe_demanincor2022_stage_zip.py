"""Source-only gate for 2022 warming, mutualist synchrony and fitness.

Original deposited experiment: de Manincor et al., Global Change Biology
(2026), doi:10.1111/gcb.71074. Original Zenodo v3 record
doi:10.5281/zenodo.17830772.

Aim: can date-specific plant flower abundance and independent Osmia activity
be linked to final seed, germination and seedling survival on the SAME
measured biological units? DO NOT infer individual-level alignment from
treatment-room means; DO NOT promote any effective stage H1 coefficient
without a documented source join and untouched validation.

One ambient and three different warmed greenhouse ROOMS. Even if there
are multiple arenas/plant IDs inside each room, each temperature has one
room. Thus warming effects are NOT replicated independent-room treatment
effects. This probe is metadata only and keeps original bytes outside repo.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from io import BytesIO, StringIO
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

DOI = "10.5281/zenodo.17830772"
RECORD = "17830772"
FILES = {
    "deManincor-et-al.2025_data_pSEM.zip":
        ("33ff77e05c3fb77141ec21226fa3c666", 18_000_000),
    "deManincor-et-al.2025_Warming_RScripts.txt":
        ("9347d7e1733ce4274a7551775ee5a71f", 250_000),
}
MAX_MEMBERS = 150
# Only read small text members, no large scientific binary is loaded.
# A compressed 4.3 MB R dataset can expand to >100 MB legitimately.
MAX_MEMBER_BYTES = 300_000_000
MAX_EXPANDED_BYTES = 500_000_000
MAX_TEXT_READ_BYTES = 2_000_000
HEADERS = (
    "date", "day", "doy", "plant", "flower", "bee", "abund", "visit",
    "seed", "germ", "surviv", "arena", "room", "temperature", "temp",
    "treat", "cohort", "ID", "time", "nest", "fruit",
)
TRUSTED_TEXT_SUFFIXES = (".csv", ".tsv", ".txt", ".md")


def original_url(name: str) -> str:
    if name not in FILES:
        raise ValueError("off-record original file")
    return "https://zenodo.org/records/" + RECORD + "/files/" + (
        quote(name, safe="")
    ) + "?download=1"


def fetch_original(name: str) -> bytes:
    url = original_url(name)
    md5, ceiling = FILES[name]
    with urlopen(Request(url, headers={
        "User-Agent": "IWE-2022-cohort-original-source-audit/1.0",
        "Accept": "application/zip,text/plain,application/octet-stream",
    }), timeout=65) as response:
        raw = response.read(ceiling + 1)
    if len(raw) > ceiling:
        raise ValueError("unexpected source file size")
    if hashlib.md5(raw).hexdigest() != md5:
        raise ValueError("original archive MD5 mismatch: " + name)
    return raw


def validate_member_name(name: str) -> None:
    path = PurePosixPath(name.replace("\\", "/"))
    if (not name or name.startswith("/") or "\\" in name
            or any(x in ("..", "") for x in path.parts)
            or len(name) > 300 or "\x00" in name):
        raise ValueError("untrusted archive file path")
    if path.suffix.lower() in (".exe", ".sh", ".dll", ".pyc"):
        raise ValueError("unexpected executable source file")


def sniff_csv_headers(raw: bytes, filename: str) -> dict:
    """Profile source columns, date/ID candidates and missingness, not effects."""
    sample = raw[: min(len(raw), 200_000)].decode(
        "utf-8-sig", errors="replace"
    )
    lines = [x for x in sample.splitlines() if x.strip()]
    if not lines:
        return {"schema": "empty"}
    head = lines[0]
    delim = max(("\t", ",", ";"), key=head.count)
    if not head.count(delim):
        return {
            "schema": "text_without_delimiter",
            "first_line": head[:160]
        }
    reader = csv.reader(StringIO(sample), delimiter=delim)
    columns = next(reader, [])
    if len(columns) > 300 or len(columns) < 2:
        raise ValueError("implausible source column count")
    if len(set(columns)) < len(columns):
        raise ValueError("duplicate original column header")
    return {
        "schema": "delimited",
        "headers": columns,
        "n_fields": len(columns),
        "delimiter": repr(delim),
        "timing_or_unit_columns": [
            c for c in columns
            if any(k.lower() in c.lower() for k in HEADERS)
        ],
        "data_byte_length": len(raw),
        "preview_lines_only": [
            x[:180] for x in lines[1:3]
        ],
        "full_source_rows_released": False,
    }


def inspect_archive(raw: bytes) -> dict:
    members = []
    total = 0
    counts = Counter()
    with ZipFile(BytesIO(raw)) as z:
        infos = z.infolist()
        if len(infos) > MAX_MEMBERS:
            raise ValueError("too many files in source deposit")
        for inf in infos:
            name = inf.filename
            validate_member_name(name)
            if inf.is_dir():
                continue
            if inf.file_size > MAX_MEMBER_BYTES:
                raise ValueError("implausibly oversized archive member")
            total += inf.file_size
            if total > MAX_EXPANDED_BYTES:
                raise ValueError("original archive uncompressed size cap")
            suffix = PurePosixPath(name).suffix.lower()
            counts[suffix or "no_suffix"] += 1
            item = {
                "source_member_name": name,
                "byte_size": inf.file_size,
                "file_type": suffix or "unknown",
                "member_data_loaded": False,
            }
            # Only metadata of source tables. Never execute archived scripts.
            if suffix in TRUSTED_TEXT_SUFFIXES and inf.file_size < MAX_TEXT_READ_BYTES:
                body = z.read(inf)
                item["member_data_loaded"] = True
                if suffix in (".csv", ".tsv"):
                    item["table_profile"] = sniff_csv_headers(body, name)
                else:
                    text = body.decode("utf-8-sig", errors="replace")
                    lines = text.splitlines()
                    item["n_text_lines"] = len(lines)
                    item["relevant_source_lines"] = [
                        {"line": i + 1, "text": line.strip()[:180]}
                        for i, line in enumerate(lines)
                        if any(k.lower() in line.lower() for k in HEADERS)
                    ][:30]
            members.append(item)
    if not members:
        raise ValueError("no archive members")
    return {
        "source_archive_md5": FILES[
            "deManincor-et-al.2025_data_pSEM.zip"][0],
        "n_members": len(members),
        "expanded_bytes": total,
        "member_formats": dict(counts),
        "members": members,
    }


def inspect_analysis_script(raw: bytes) -> dict:
    body = raw.decode("utf-8-sig", errors="replace")
    lines = body.splitlines()
    probes = ("read.", "load(", "bee_abund", "flwrcount",
              "seed_germ", "germ", "surviv", "nests", "pSEM",
              "mutate(", "filter(", "join(")
    hits = [
        {"line": i + 1, "expression": line.strip()[:225]}
        for i, line in enumerate(lines)
        if any(p.lower() in line.lower() for p in probes)
    ]
    return {
        "source_script_md5": FILES[
            "deManincor-et-al.2025_Warming_RScripts.txt"][0],
        "n_lines": len(lines),
        "source_stage_or_join_expressions": hits[:90],
    }



PROFILED_MEMBERS = (
    "data_seeds_germ_pSEM.txt",
    "data_bee_nest_pSEM.txt",
    "bee_abund_2022.txt",
    "flwrcount_temp2022.txt",
    "imputed_temporal_vars_T.txt",
)


def _nonmissing(value: object) -> bool:
    return str(value if value is not None else "").strip().lower() not in (
        "", "na", "nan", "null", "none", "."
    )


def _profile_rows(rows: list[dict[str, str]], headers: list[str]) -> dict:
    shape = {}
    for name in headers:
        if (any(x in name.lower() for x in HEADERS)
                or name.lower() in ("sp", "germ", "cotyl", "seeds",
                                    "ovules", "ovules_tot", "mort")):
            values = [str(row.get(name, "")).strip() for row in rows]
            actual = [v for v in values if _nonmissing(v)]
            shape[name] = {
                "n_nonmissing": len(actual),
                "n_distinct_nonmissing": len(set(actual)),
                "first_distinct_literals": list(dict.fromkeys(actual))[:10],
            }
            if name.lower() in ("germ", "cotyl", "seeds", "ovules",
                                "ovules_tot", "mort", "doy", "day",
                                "flwr_count", "bees", "seed_set"):
                try:
                    numeric = [float(v) for v in actual]
                    shape[name]["numeric_min_max"] = [
                        min(numeric), max(numeric)
                    ] if numeric else None
                except ValueError:
                    shape[name]["not_uniformly_numeric"] = True
    candidate = (
        ("trtmt", "arena", "sp", "plant_flwr_ID"),
        ("trtmt", "arena", "sp"),
        ("trtmt", "arena", "DOY"),
        ("trtmt_arena", "species", "DOY"),
        ("doy", "trtmt", "sp", "arena"),
    )
    by_key = []
    for keys in candidate:
        if all(k in headers for k in keys):
            values = [tuple(r.get(k, "") for k in keys) for r in rows]
            by_key.append({
                "original_source_key_columns": list(keys),
                "n_unique_keys": len(set(values)),
                "n_repeated_rows_at_key": len(values)-len(set(values)),
                "keys_with_unrecorded_missing": sum(
                    not all(_nonmissing(r.get(k)) for k in keys)
                    for r in rows
                ),
            })
    return {
        "n_rows": len(rows),
        "headers": headers,
        "timing_unit_and_fate_column_support": shape,
        "candidate_grains": by_key,
    }


def profile_zip_tables(raw: bytes) -> dict:
    """Validate and profile original source stage rows without redistributing."""
    out = {}
    with ZipFile(BytesIO(raw)) as z:
        files = set(z.namelist())
        for name in PROFILED_MEMBERS:
            if name not in files:
                raise ValueError("essential original source stage missing: " + name)
            inf = z.getinfo(name)
            if inf.file_size > 2_000_000:
                raise ValueError("unexpected original stage source table size")
            text = z.read(inf).decode("utf-8-sig", errors="strict")
            raw_reader = csv.reader(StringIO(text), delimiter="\t")
            headers = next(raw_reader, [])
            if not headers or len(headers) != len(set(headers)):
                raise ValueError("missing/repeated original source header")
            source_values = list(raw_reader)
            source_values = [r for r in source_values if any(x.strip() for x in r)]
            # read.table() R export frequently writes row.names=TRUE
            # but does NOT label that index in the header. This is a
            # LEADING unheaded row index, not a trailing extra value.
            # Repair only when EVERY index is source-exact 1,2,..,n.
            indexed = (len(source_values) > 0
                       and all(len(row) == len(headers) + 1
                               for row in source_values)
                       and all(row[0].strip() == str(i)
                               for i, row in enumerate(source_values, 1)))
            if indexed:
                aligned = [row[1:] for row in source_values]
            elif all(len(row) == len(headers) for row in source_values):
                aligned = source_values
            else:
                raise ValueError(
                    "unverified original TSV field shift; no automatic key repair"
                )
            rows = [dict(zip(headers, row)) for row in aligned]
            original_profile = _profile_rows(rows, headers)
            original_profile["original_row_index_provenance"] = {
                "had_unheaded_export_row_number": indexed,
                "row_number_verified_source_sequential": indexed,
                "n_original_rows": len(source_values),
            }
            original_profile["source_row_alignment_verified"] = True
            out[name] = original_profile
    return out


def audit() -> dict:
    output = {
        "schema": "iwe_2022_warming_stage_original_source_gate_v1",
        "original_dataset_doi": DOI,
        "article_doi": "10.1111/gcb.71074",
        "experiment_year": 2022,
        "same_research_group_as_2021_zenodo_7264150": True,
        "not_independent_across_research_programmes_without_design_audit": True,
        "temperature_room_treatment_confound": True,
        "study_design": "four temperature rooms, one room per level",
        "strict_iwe_h1_effect_added": False,
        "source_verified": False,
        "matched_plant_to_final_seed_germination_verified": False,
        "biological_result_newly_estimated": False,
    }
    try:
        archive = fetch_original("deManincor-et-al.2025_data_pSEM.zip")
        code = fetch_original("deManincor-et-al.2025_Warming_RScripts.txt")
        output["archive"] = inspect_archive(archive)
        output["source_stage_tables"] = profile_zip_tables(archive)
        output["analysis_script"] = inspect_analysis_script(code)
        output["source_verified"] = True
        output["status"] = "source_manifest_verified_join_unresolved"
    except (OSError, TimeoutError, ValueError, BadZipFile, UnicodeError) as e:
        output["status"] = "source_unavailable_or_source_shape_changed"
        output["error"] = type(e).__name__ + ": " + str(e)[:250]
    return output


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", required=True, type=Path)
    a = p.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    report = audit()
    (a.outdir / "source_archive_profile.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print("DEMANINCOR2022_SOURCE_GATE", report["status"],
          report.get("error", ""))
    if "archive" in report:
        print("DEMANINCOR2022_SOURCE_MEMBERS",
              json.dumps(report["archive"], ensure_ascii=False)[:55000])
        if "source_stage_tables" in report:
            print("DEMANINCOR2022_SOURCE_UNIT_PROFILES",
                  json.dumps(report["source_stage_tables"],
                             ensure_ascii=False)[:60000])
        print("DEMANINCOR2022_R_METHOD_REFERENCES",
              json.dumps(report["analysis_script"]["source_stage_or_join_expressions"],
                         ensure_ascii=False)[:13000])
    print("Do not infer direct causal phenology benefit from temperature-room means")
    return 0 if report["source_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
