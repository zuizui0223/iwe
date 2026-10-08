#!/usr/bin/env python3
"""Source-constrained, NON-PROMOTING retrieval of the public IWE015 Dryad files.

Only use pinned file IDs from dataset DOI 10.5061/dryad.6q573n5w1.
A successful download identifies source files; it does NOT authorize any new
strict-H1 effect, infer column meanings, or relabel printed SE values as SD.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.request

DOI = "10.5061/dryad.6q573n5w1"
SOURCE_FILES = {
    "2012_early_female.csv": 278487,
    "2012_late_female.csv": 278488,
    "2013_early_female.csv": 278490,
    "2013_late_female.csv": 278492,
    "data_analysis.R": 278500,
    "README.txt": 278498,
}

def source_urls(file_id: int) -> tuple[str, ...]:
    return (
        f"https://datadryad.org/downloads/file_stream/{file_id}",
        f"https://datadryad.org/api/v2/files/{file_id}/download",
    )

def inspect_payload(filename: str, payload: bytes) -> dict[str, object]:
    """Reject blocked/error pages and validate file contents before archiving."""
    if not payload or len(payload) > 2_000_000:
        raise ValueError("unexpected payload length for pinned small source file")
    try:
        data = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("source file is not UTF-8 text") from exc
    raw = data.lstrip().lower()
    if (raw.startswith("<!doctype html") or raw.startswith("<html")
            or raw.startswith("<?xml") or "access denied" in raw[:200]):
        raise ValueError("HTML/XML/access-denied payload instead of source data")
    result: dict[str, object] = {
        "size_bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
    if filename.endswith(".csv"):
        table = csv.reader(io.StringIO(data))
        header = next(table, None)
        if not header or len(header) < 3 or len(set(header)) != len(header):
            raise ValueError("CSV header missing, duplicated, or unexpectedly narrow")
        n_rows = sum(1 for row in table if any(x.strip() for x in row))
        if n_rows < 2:
            raise ValueError("CSV lacks data rows")
        result["columns"] = header
        result["n_data_rows"] = n_rows
    elif filename.endswith(".R"):
        if len(data.splitlines()) < 10:
            raise ValueError("R source file unexpectedly short")
        result["lines"] = len(data.splitlines())
    else:
        if len(data.strip()) < 30:
            raise ValueError("README unexpectedly short")
        result["lines"] = len(data.splitlines())
    return result

def retrieve_one(filename: str, file_id: int, dest: Path, *,
                 timeout: float = 15) -> dict[str, object]:
    attempts = []
    for url in source_urls(file_id):
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "IWE-reproducibility-audit/1.0",
                "Accept": "text/csv,text/plain,application/octet-stream,*/*",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read(2_000_001)
            metadata = inspect_payload(filename, payload)
        except urllib.error.HTTPError as exc:
            attempts.append({"url": url, "error": f"HTTP {exc.code}"})
            continue
        except (urllib.error.URLError, TimeoutError, ValueError,
                ConnectionError, OSError) as exc:
            attempts.append({"url": url, "error": str(exc)[:250]})
            continue
        dest.mkdir(parents=True, exist_ok=True)
        (dest / filename).write_bytes(payload)
        return {
            "name": filename, "file_id": file_id, "status": "downloaded",
            "verified_url": url, "attempts": attempts, **metadata,
        }
    return {
        "name": filename, "file_id": file_id, "status": "blocked",
        "attempts": attempts,
    }

def run(output_dir: Path, timeout: float = 15) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [retrieve_one(name, file_id, output_dir / "source_files",
                         timeout=timeout)
            for name, file_id in SOURCE_FILES.items()]
    success = sum(row["status"] == "downloaded" for row in rows)
    manifest: dict[str, object] = {
        "schema": "iwe015_source_download_probe_v1",
        "doi": DOI,
        "source_dataset_url": "https://datadryad.org/dataset/doi:10.5061/dryad.6q573n5w1",
        "files_expected": len(SOURCE_FILES),
        "files_downloaded": success,
        "status": "complete" if success == len(SOURCE_FILES) else "blocked",
        "evidence_promoted": False,
        "source_analysis_executed": False,
        "table1_dispersion_verified": False,
        "files": rows,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--strict", action="store_true",
                        help="Exit nonzero if any source file cannot be retrieved")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    manifest = run(args.output_dir, timeout=args.timeout)
    print(f"IWE015 pinned public source status: {manifest['status']}, "
          f"{manifest['files_downloaded']}/{manifest['files_expected']} files.")
    for f in manifest["files"]:
        columns = f.get("columns")
        msg = f"- {f['name']}: {f['status']}"
        if columns is not None:
            msg += f" ({f['n_data_rows']} data rows, columns={columns})"
        elif f["status"] == "blocked":
            msg += f" ({', '.join(a['error'] for a in f['attempts'])})"
        print(msg)
    print("No effect sizes generated or registry rows changed.")
    return 2 if args.strict and manifest["status"] != "complete" else 0

if __name__ == "__main__":
    raise SystemExit(main())
