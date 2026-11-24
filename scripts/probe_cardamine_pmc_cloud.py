"""Non-promoting PMC Cloud source-availability audit for IWE032 Cardamine.

Official, public NLM dataset API (post-August 2026). Does not ingest
published figure geometry, fabricate female capture dates, or promote effects.
All source files are kept in memory; only a compact provenance receipt is saved.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
import zipfile

PMCID = "PMC11056787"
DOI = "10.1002/ece3.11330"
S3 = "https://pmc-oa-opendata.s3.amazonaws.com"
ALLOWED = {("ECE3-14-e11330-s001.docx").lower(),
           ("ECE3-14-e11330-s002.docx").lower()}
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def fetch(url: str, *, max_bytes: int = 3_000_000) -> bytes:
    p = urlparse(url)
    if p.scheme != "https" or p.hostname != "pmc-oa-opendata.s3.amazonaws.com":
        raise ValueError("only official PMC Cloud S3 file URLs are allowed")
    req = Request(url, headers={"User-Agent": "IWE-IWE032-source-audit/1.0"})
    with urlopen(req, timeout=25) as response:
        raw = response.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError("source exceeds byte cap")
    return raw


def metadata_is_source(m: dict) -> bool:
    return (str(m.get("pmcid", "")).upper() == PMCID
            and str(m.get("doi", "")).lower() == DOI
            and str(m.get("license_code", "")).strip() != "")


def media_urls(meta: dict) -> list[str]:
    output = []
    for item in meta.get("media_urls", []):
        u = item if isinstance(item, str) else item.get("url", "") if isinstance(item, dict) else ""
        if isinstance(u, str) and urlparse(u).hostname == "pmc-oa-opendata.s3.amazonaws.com":
            output.append(u)
    return output


def docx_source_signals(raw: bytes) -> dict:
    """Diagnostic only: tokens are NOT sufficient evidence for the missing events."""
    with zipfile.ZipFile(io.BytesIO(raw)) as arc:
        member = arc.getinfo("word/document.xml")
        if member.file_size > 2_000_000:
            raise ValueError("oversized Word document XML")
        xml = arc.read("word/document.xml")
    root = ET.fromstring(xml)
    para = [" ".join(t.text or "" for t in p.findall(".//w:t", NS))
            for p in root.findall(".//w:p", NS)]
    normalized = "\n".join(para).casefold()
    return {
        "paragraphs": len(para),
        "has_all_2012_2014_tokens": all(str(y) in normalized for y in (2012, 2013, 2014)),
        "has_female_token": any(w in normalized for w in ("female", "females")),
        "has_captured_event_token": any(w in normalized for w in ("capture", "recapture")),
        "has_doy_token": any(w in normalized for w in ("day of year", "doy")),
    }


def run() -> dict:
    versions = []
    seen = set()
    for n in (1, 2, 3):
        uri = f"{S3}/metadata/{PMCID}.{n}.json"
        try:
            blob = fetch(uri, max_bytes=200_000)
            meta = json.loads(blob.decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as e:
            versions.append({"version": n, "metadata": "unavailable", "error_type": type(e).__name__})
            continue
        if not isinstance(meta, dict) or not metadata_is_source(meta):
            versions.append({"version": n, "metadata": "identity_or_license_not_verified"})
            continue
        urls = media_urls(meta)
        v = {
            "version": n,
            "metadata": "source_identity_and_license_present",
            "license_code": str(meta.get("license_code")),
            "media_count": len(urls),
            "candidate_files": [],
        }
        for u in urls:
            filename = unquote(urlparse(u).path.split("/")[-1])
            if filename.lower() not in ALLOWED or filename.lower() in seen:
                continue
            seen.add(filename.lower())
            rec = {"filename": filename, "url": u.split("?")[0]}
            try:
                raw = fetch(u)
                rec["sha256"] = hashlib.sha256(raw).hexdigest()
                rec["bytes"] = len(raw)
                rec["signals"] = docx_source_signals(raw)
                rec["adjudication"] = "requires_human_source_verification"
            except (HTTPError, URLError, TimeoutError, ValueError, zipfile.BadZipFile,
                    KeyError, ET.ParseError) as e:
                rec["adjudication"] = "access_or_parse_failed"
                rec["error_type"] = type(e).__name__
            v["candidate_files"].append(rec)
        versions.append(v)
    available = [r for v in versions for r in v.get("candidate_files", [])
                 if r.get("adjudication") == "requires_human_source_verification"]
    return {
        "primary_article": DOI,
        "source_pmcid": PMCID,
        "source_route": "NLM_PMC_Cloud_post_2026_08",
        "versions": versions,
        "downloaded_docx_count": len(available),
        "source_verified_2012_2014_female_capture_recapture": False,
        "strict_h1_promotion": False,
        "decision": "await_numeric_female_events_or_exact_annual_quantiles",
        "interpretation": "A document with year/female/capture tokens is not a female event series. No graphical digitization.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("outputs/cardamine_pmc_cloud_receipt.json"))
    args = parser.parse_args()
    result = run()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"downloaded_docx_count": result["downloaded_docx_count"],
                      "versions": [v["metadata"] for v in result["versions"]],
                      "source_verified": False,
                      "receipt": str(args.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
