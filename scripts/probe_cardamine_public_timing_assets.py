"""One-time, NON-PROMOTING publisher-asset access probe for IWE032.

These are source-pinned official Wiley assets, not images to be digitized.
Fetching bytes never establishes female adult event dates or q10/q90 windows.
Record only format, SHA256, size, and whether editable charts MAY exist.
No H1 effect or exposure definition is generated. No user credentials.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from io import BytesIO
import zipfile

TARGETS = {
    "davies2024_figure4.ppt": (
        "https://onlinelibrary.wiley.com/action/downloadFigures"
        "?doi=10.1002%2Fece3.11330&id=ece311330-fig-0004&partId=",
        "ppt",
    ),
    "davies2019_appendixS1.pdf": (
        "https://esajournals.onlinelibrary.wiley.com/action/downloadSupplement"
        "?doi=10.1002%2Fecy.2612&file=ecy2612-sup-0001-AppendixS1.pdf",
        "pdf",
    ),
    "davies2019_appendixS2.pdf": (
        "https://esajournals.onlinelibrary.wiley.com/action/downloadSupplement"
        "?doi=10.1002%2Fecy.2612&file=ecy2612-sup-0002-AppendixS2.pdf",
        "pdf",
    ),
    "davies2019_appendixS3.pdf": (
        "https://esajournals.onlinelibrary.wiley.com/action/downloadSupplement"
        "?doi=10.1002%2Fecy.2612&file=ecy2612-sup-0003-AppendixS3.pdf",
        "pdf",
    ),
}
MAX_FILE_BYTES = 9_000_000
OLE_MAGIC = bytes.fromhex("D0 CF 11 E0 A1 B1 1A E1")
ZIP_MAGIC = b"PK\x03\x04"
PDF_MAGIC = b"%PDF-"


def validate_asset(name: str, data: bytes, asset_type: str) -> dict[str, object]:
    """Validate binary signature but never infer biological event values."""
    if not data or len(data) > MAX_FILE_BYTES:
        raise ValueError("empty or oversized publisher asset")
    first = data[:64].lstrip().lower()
    if first.startswith((b"<html", b"<!doctype", b"<?xml")):
        raise ValueError("HTML/XML error payload cannot substitute for source file")
    if asset_type == "pdf":
        if not data.startswith(PDF_MAGIC):
            raise ValueError("expected PDF magic")
        form = "pdf"
        possible_charts: list[str] = []
    elif asset_type == "ppt":
        if data.startswith(OLE_MAGIC):
            form = "legacy_ole_ppt"
            possible_charts = []  # Unknown, not evidence that no data exist.
        elif data.startswith(ZIP_MAGIC):
            form = "office_open_xml"
            try:
                with zipfile.ZipFile(BytesIO(data)) as zf:
                    if zf.testzip() is not None:
                        raise ValueError("corrupted Office archive")
                    names = zf.namelist()
            except (zipfile.BadZipFile, RuntimeError) as exc:
                raise ValueError("invalid Office archive") from exc
            if "[Content_Types].xml" not in names:
                raise ValueError("not a complete Office archive")
            # Presence of an embedded workbook is only a lead for audit.
            possible_charts = [
                n for n in names
                if n.startswith(("ppt/embeddings/", "ppt/charts/"))
            ]
        else:
            raise ValueError("expected legacy PPT or OOXML signature")
    else:
        raise ValueError("unknown publisher asset type")
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "format": form,
        "potential_editable_chart_parts": sorted(possible_charts),
        "source_adult_flight_numeric_verified": False,
        "figure_digitization_performed": False,
    }


def download_assets(outdir: Path, timeout: float = 15.0) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, (url, asset_type) in TARGETS.items():
        record: dict[str, object] = {"filename": filename, "url": url}
        try:
            req = urllib.request.Request(
                url, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; IWE-source-audit/1.0)",
                    "Accept": "application/pdf,application/vnd.ms-powerpoint,"
                              "application/vnd.openxmlformats-officedocument."
                              "presentationml.presentation,*/*",
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                response_url = resp.geturl()
                if urlsplit(response_url).scheme != "https":
                    raise ValueError("publisher redirected to non-HTTPS URL")
                content = resp.read(MAX_FILE_BYTES + 1)
            record.update(validate_asset(filename, content, asset_type))
            (outdir / filename).write_bytes(content)
            record["access_status"] = "downloaded_unreviewed"
        except urllib.error.HTTPError as exc:
            record["access_status"] = "blocked"
            record["error"] = f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError,
                OSError) as exc:
            record["access_status"] = "blocked"
            record["error"] = type(exc).__name__
        except ValueError as exc:
            record["access_status"] = "invalid_asset"
            record["error"] = str(exc)
        records.append(record)
    status = {
        "schema": "cardamine_pinned_publisher_timing_assets_v1",
        "source_doi_2024": "10.1002/ece3.11330",
        "source_doi_2019": "10.1002/ecy.2612",
        "expected_assets": len(TARGETS),
        "downloaded_assets": sum(
            r["access_status"] == "downloaded_unreviewed" for r in records
        ),
        "female_capture_recap_data_verified": False,
        "exact_q10_q90_verified": False,
        "strict_h1_effect_admitted": False,
        "source_files": records,
    }
    (outdir / "manifest.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    result = download_assets(args.outdir, timeout=args.timeout)
    print(f"Pinned Cardamine publisher assets: "
          f"{result['downloaded_assets']}/{result['expected_assets']} downloaded")
    for entry in result["source_files"]:
        print(f"- {entry['filename']}: {entry['access_status']} "
              f"{entry.get('error','')}")
    print("Numeric female flight is NOT verified by downloading a figure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
