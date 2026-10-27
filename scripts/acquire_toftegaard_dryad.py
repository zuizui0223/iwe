#!/usr/bin/env python3
"""Acquire a public Dryad field dataset for an *independent* phenology audit.

The file is not part of IWE strict H1 and cannot replace Dibbinsdale 2012-14
independently observed adult female flight dates or any plant fitness outcome.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

DOI = "10.5061/dryad.jp328r6"
FILE_NAME = "Plant phenology in the field.txt"
PUBLIC_ENDPOINTS = (
    "https://datadryad.org/api/v2/files/79537/download",
    "https://datadryad.org/downloads/file_stream/79537",
)
MAX_BYTES = 15_000_000
MIN_BYTES = 50_000


def candidate_file(raw: bytes) -> tuple[bool, str]:
    if not (MIN_BYTES <= len(raw) <= MAX_BYTES):
        return False, "size_outside_published_text_expectation"
    preview = raw[:8192].lstrip().lower()
    if any(x in preview for x in (b"<!doctype html", b"<html", b"<body", b"<error>")):
        return False, "html_or_error_response"
    if raw.count(b"\x00") > len(raw) // 200:
        return False, "binary_like_response"
    return True, "plausible_text_data_not_yet_schema_validated"


def fetch_text_publicly(url: str) -> tuple[bytes, dict]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "IWE-public-research-data-audit/0.1 (GitHub Actions; Dryad DOI 10.5061/dryad.jp328r6)",
            "Accept": "text/plain,application/octet-stream,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        status = response.status
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        payload = response.read(MAX_BYTES + 1)
    return payload, {"status_code": status, "content_type": content_type, "resolved_url": final_url}


def audit_file(raw: bytes) -> dict:
    ok, condition = candidate_file(raw)
    if not ok:
        raise ValueError(condition)
    encoding = next(
        (e for e in ("utf-8-sig", "utf-16", "latin-1") if _decodable(raw, e)),
        "unresolved",
    )
    return {
        "schema": "iwe_toftegaard_dryad_source_audit_v0.1",
        "doi": DOI,
        "original_file_name": FILE_NAME,
        "source_scope": "Sweden 2010-2013 plant phenophase and A. cardamines egg/larval observations",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "line_count": len(raw.splitlines()),
        "encoding_candidate": encoding,
        "content_gate": condition,
        "observation_fields_validated": False,
        "butterfly_presence_observed": "not_yet_audited",
        "plant_reproductive_fitness_observed": False,
        "independent_adult_activity_observed": False,
        "strict_h1_effects_created": 0,
    }


def _decodable(raw: bytes, name: str) -> bool:
    try:
        raw.decode(name)
        return True
    except UnicodeError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[dict] = []
    for uri in PUBLIC_ENDPOINTS:
        try:
            raw, http = fetch_text_publicly(uri)
            report = audit_file(raw)
            (args.output_dir / "toftegaard_2018_plant_phenology.txt").write_bytes(raw)
            report["http"] = http
            report["retrieval_status"] = "source_downloaded_schema_pending"
            report["endpoint"] = uri
            report["failed_other_endpoints"] = errors
            (args.output_dir / "dryad_retrieval_audit.json").write_text(
                json.dumps(report, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps(report, indent=2))
            return 0
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            errors.append({
                "endpoint": uri,
                "error_type": type(exc).__name__,
                "error_summary": str(exc)[:250],
            })
    receipt = {
        "schema": "iwe_toftegaard_dryad_source_audit_v0.1",
        "doi": DOI,
        "retrieval_status": "blocked_external_download",
        "errors": errors,
        "source_data_rows": 0,
        "strict_h1_effects_created": 0,
    }
    (args.output_dir / "dryad_retrieval_audit.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
