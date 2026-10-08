"""One-time public FULL-ARCHIVE Dryad fallback for IWE015 (non-promoting).

The documented API dataset ZIP endpoint is not the same as the individual
file_stream/file-ID API endpoints that returned HTTP 403/401. Inspect the
entire public deposit archive without guessing plant outcome columns.
Only six source-pinned exact basenames may be written. No Hedges g or SMD.
Run from repository root:
  python -m scripts.probe_iwe015_dataset_zip --output-dir /tmp/iwe015-archive --strict

OPTIONAL: DRYAD_ACCESS_TOKEN is read only from an environment secret; it is
never included in logs or manifests, and is stripped on off-Dryad redirects.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
import os
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import quote
import urllib.request
import zipfile

from scripts.recover_iwe015_dryad import (
    DOI, SOURCE_FILES, ScopeBearerRedirect, inspect_payload, source_headers
)

MAX_ARCHIVE_BYTES = 75_000_000
SOURCE_MAX_BYTES = 2_000_000
DATASET_URL = (
    "https://datadryad.org/api/v2/datasets/"
    + quote("doi:" + DOI, safe="")
    + "/download"
)


def audit_archive(payload: bytes) -> tuple[dict[str, object], dict[str, bytes]]:
    """Audit zip and return source bytes for exact six basenames; no extraction.

    The complete dataset ZIP may include other files, but we never retain
    non-required source files or infer how their columns relate to fitness.
    """
    if not payload or len(payload) > MAX_ARCHIVE_BYTES:
        raise ValueError("archive missing or exceeds byte cap")
    if not zipfile.is_zipfile(BytesIO(payload)):
        raise ValueError("dataset response is not a ZIP archive")

    found: dict[str, bytes] = {}
    rows: list[dict[str, object]] = []
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            name = PurePosixPath(info.filename).name
            if name not in SOURCE_FILES:
                continue
            if name in found:
                raise ValueError(f"duplicate pinned archive basename: {name}")
            if info.file_size > SOURCE_MAX_BYTES:
                raise ValueError(f"pinned archive member exceeds size cap: {name}")
            with archive.open(info, "r") as fh:
                content = fh.read(SOURCE_MAX_BYTES + 1)
            entry = inspect_payload(name, content)
            found[name] = content
            rows.append({"name": name, "file_id": SOURCE_FILES[name],
                         "zip_entry": info.filename, **entry})

    missing = sorted(set(SOURCE_FILES) - set(found))
    state = "complete" if not missing else "incomplete"
    return {
        "schema": "iwe015_full_dryad_dataset_archive_probe_v1",
        "doi": DOI,
        "source_url": DATASET_URL,
        "n_expected": len(SOURCE_FILES),
        "n_matched": len(found),
        "status": state,
        "missing": missing,
        "source_file_manifest": sorted(rows, key=lambda x: x["name"]),
        "evidence_promoted": False,
        "source_analysis_executed": False,
        "table1_variance_verified": False,
        "flower_fruit_lineage_verified": False,
    }, found


def probe(output_dir: Path, *, token: str | None = None,
          timeout: float = 20) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    status: dict[str, object] = {
        "schema": "iwe015_full_dryad_dataset_archive_probe_v1",
        "doi": DOI,
        "source_url": DATASET_URL,
        "status": "blocked",
        "n_expected": len(SOURCE_FILES),
        "n_matched": 0,
        "bearer_auth_configured": bool(token),
        "evidence_promoted": False,
        "source_analysis_executed": False,
        "table1_variance_verified": False,
        "flower_fruit_lineage_verified": False,
    }
    try:
        request = urllib.request.Request(
            DATASET_URL, headers=source_headers(token)
        )
        opener = urllib.request.build_opener(ScopeBearerRedirect())
        with opener.open(request, timeout=timeout) as response:
            ct = response.headers.get("Content-Type", "")
            status["http_status"] = response.status
            status["response_content_type"] = ct
            payload = response.read(MAX_ARCHIVE_BYTES + 1)
        audit, files = audit_archive(payload)
        status.update(audit)
        # Unreviewed raw bytes are output only if all six pinned basenames
        # are in one verified ZIP. Never write arbitrary zip paths.
        if status["status"] == "complete":
            dest = output_dir / "source_files"
            dest.mkdir(exist_ok=True)
            for name, raw in files.items():
                (dest / name).write_bytes(raw)
    except HTTPError as exc:
        status["error"] = f"HTTP {exc.code}"
    except (URLError, TimeoutError, ConnectionError, OSError) as exc:
        status["error"] = type(exc).__name__
    except (ValueError, zipfile.BadZipFile, RuntimeError) as exc:
        status["error"] = str(exc)[:200]

    (output_dir / "archive_manifest.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    token = os.environ.get("DRYAD_ACCESS_TOKEN", "").strip() or None
    result = probe(args.output_dir, token=token, timeout=args.timeout)
    print(f"Dryad full-dataset archive: {result['status']}; "
          f"{result['n_matched']}/{result['n_expected']} source files.")
    if result.get("error"):
        print(f"Archive retrieval blocker: {result['error']}")
    print("No effect size or source-fitness identity was inferred.")
    return 2 if args.strict and result["status"] != "complete" else 0


if __name__ == "__main__":
    raise SystemExit(main())
