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
        print("DEMANINCOR2022_R_METHOD_REFERENCES",
              json.dumps(report["analysis_script"]["source_stage_or_join_expressions"],
                         ensure_ascii=False)[:13000])
    print("Do not infer direct causal phenology benefit from temperature-room means")
    return 0 if report["source_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
