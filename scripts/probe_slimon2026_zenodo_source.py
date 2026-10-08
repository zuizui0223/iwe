"""Source-limited inventory of Slimon & Agrawal 2026's public Zenodo archive.

Non-promoting: tests whether a contemporaneous *independent adult*
seed-predator activity series is present alongside the original flowering,
predation and lifetime seed data. Only metadata, file paths, field names
and short README search contexts are logged. Never invent DOY or effects.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from io import BytesIO, StringIO, TextIOWrapper
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

RECORD = "19488509"
DOI = "10.5281/zenodo.19488509"
API = f"https://zenodo.org/api/records/{RECORD}"
FILES = frozenset(("Freese Stats.zip", "READ_ME_Phenological_plasticity.txt"))
MAX_REMOTE = 22_000_000
MAX_ZIP_FILES = 2000
MAX_MEMBER = 12_000_000
KEYWORDS = ("adult", "flight", "trap", "catch", "moth", "schinia",
            "seed predator", "predation", "flowering", "fitness",
            "total seed", "reproductive", "date", "phenolog")


def safe_source_link(link: str) -> bool:
    parsed = urlsplit(link)
    return (parsed.scheme == "https" and parsed.hostname == "zenodo.org"
            and parsed.path.startswith(("/api/records/19488509",
                                        "/records/19488509/files/")))


def read_public(url: str, max_bytes: int = MAX_REMOTE, timeout: int = 25) -> bytes:
    if not safe_source_link(url):
        raise ValueError("source link outside exact public Zenodo record")
    request = Request(url, headers={
        "User-Agent": "IWE-source-audit/1.0",
        "Accept": "application/json,application/zip,text/plain,*/*"
    })
    with urlopen(request, timeout=timeout) as response:
        if not safe_source_link(response.geturl()):
            raise ValueError("archive redirects outside the original record")
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("source file exceeds audit cap")
    return data


def file_info(json_obj: dict) -> list[dict]:
    """Zenodo InvenioRDM records list files as entries[*] (dict or list)."""
    obj = json_obj.get("files", {})
    entries = obj.get("entries", obj) if isinstance(obj, dict) else obj
    if isinstance(entries, dict):
        files = list(entries.values())
    elif isinstance(entries, list):
        files = entries
    else:
        raise ValueError("unknown Zenodo file listing schema")
    result = []
    for entry in files:
        key = entry.get("key", entry.get("filename", ""))
        if key not in FILES:
            continue
        links = entry.get("links", {})
        url = links.get("content") or links.get("self")
        if not url or not safe_source_link(url):
            raise ValueError("Zenodo file link missing or untrusted")
        result.append({"name": key, "url": url,
                       "bytes_expected": entry.get("size"),
                       "checksum": entry.get("checksum", "")})
    return result


def contexts(readme: str, max_matches: int = 22) -> list[dict]:
    """Short source quotations to guide original read, not proof of data."""
    lines = readme.splitlines()
    out = []
    for i, line in enumerate(lines):
        hit = [k for k in KEYWORDS if k in line.lower()]
        if hit:
            out.append({
                "readme_line": i + 1,
                "keywords": hit,
                "short_context": line.strip()[:180],
                "source_verified_method_claim": False,
            })
        if len(out) >= max_matches:
            break
    return out


def archive_inventory(raw: bytes) -> list[dict]:
    result = []
    try:
        zf = ZipFile(BytesIO(raw))
    except BadZipFile as exc:
        raise ValueError("not a valid ZIP archive") from exc
    with zf:
        members = zf.infolist()
        if len(members) > MAX_ZIP_FILES:
            raise ValueError("too many files")
        for member in members:
            if member.is_dir():
                continue
            name = member.filename
            if (name.startswith("/") or ".." in name.split("/")
                    or member.file_size > MAX_MEMBER):
                raise ValueError("unsafe or oversized member")
            record = {"member": name, "byte_size": member.file_size,
                      "ext": Path(name).suffix.lower(),
                      "headers": [], "rows": None}
            if record["ext"] in {".csv", ".tsv"} and member.file_size < 3_000_000:
                content = zf.read(member).decode("utf-8-sig", errors="replace")
                sep = "\t" if record["ext"] == ".tsv" else ","
                reader = csv.reader(StringIO(content), delimiter=sep)
                record["headers"] = next(reader, [])[:120]
                record["rows"] = sum(1 for _ in reader)
            elif record["ext"] in {".r", ".rmd"}:
                script = zf.read(member).decode("utf-8-sig", errors="replace")
                record["candidate_timing_lines"] = contexts(script, 12)
            result.append(record)
    return result


def audit(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "iwe_slimon2026_archive_source_inventory_v1",
        "doi": DOI,
        "study_class": "antagonist",
        "status": "not_checked",
        "adult_partner_window_verified": False,
        "same_unit_final_seeds_verified": False,
        "strict_h1_eligible": False,
        "promoted": False,
        "source_claim": "two cohorts; flowering broadened by induced herbivory; opposing early/late predation consequences",
    }
    try:
        metadata = json.loads(read_public(API).decode("utf-8"))
        files = file_info(metadata)
        report["listed_targets"] = [f["name"] for f in files]
        for entry in files:
            raw = read_public(entry["url"])
            label = entry["name"]
            report[label + "_sha256"] = hashlib.sha256(raw).hexdigest()
            if label.endswith(".txt"):
                report["readme_contexts"] = contexts(raw.decode("utf-8", errors="replace"))
                report["readme_line_count"] = len(raw.splitlines())
            elif label.endswith(".zip"):
                report["archive_members"] = archive_inventory(raw)
        report["status"] = "inventory_recovered" if files else "targets_not_listed"
    except (ValueError, OSError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
        report["status"] = "source_access_or_format_blocked"
        report["error"] = str(exc)[:250]
    (outdir / "source_only_inventory.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("Source archive:", report["status"], "; listed targets:", report.get("listed_targets"))
    print("README source leads:", report.get("readme_contexts", []))
    for f in report.get("archive_members", []):
        print("ARCHIVE MEMBER", f["member"], "size", f["byte_size"],
              "headers", f["headers"][:35], "rows", f["rows"])
        for lead in f.get("candidate_timing_lines", [])[:5]:
            print("SCRIPT KEYWORD", lead["short_context"])
    print("No independent adult flight or H1 effect verified by automated inventory.")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    audit(args.outdir)


if __name__ == "__main__":
    main()
