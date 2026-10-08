"""One-shot, source-only retrieval of Hurlburt's *public* thesis PDF.

No extraction, figures, OCR, animal counts, flower dates, or effect sizes.
A downloaded PDF signature is not evidence of a marked-unit linkage.
Only DOI-resolved, institutional-hosted NQ95948.pdf/bitstream routes are tried.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

THESIS_DOI = "10.7939/r3-fe1d-kj80"
DOI_URL = "https://doi.org/" + THESIS_DOI
FILENAME = "NQ95948.pdf"
ALLOWED_HOSTS = frozenset({
    "doi.org", "scholaris.ca", "www.scholaris.ca",
    "era.library.ualberta.ca", "era-av.library.ualberta.ca",
})
MAX_BYTES = 12_000_000
MAX_ATTEMPTS = 6


class _Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag.lower() == "a":
            for k, v in attrs:
                if k.lower() == "href" and v:
                    self.links.append(v)


def _allowed(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme == "https" and (parts.hostname or "").lower() in ALLOWED_HOSTS


def extract_source_file_links(page: str, landing: str) -> list[str]:
    """Recognize repository file/bitstream hrefs, not unrelated PDFs."""
    links = _Anchors()
    links.feed(page)
    candidates: list[str] = []
    for href in links.links:
        if not ("NQ95948" in href or "/bitstreams/" in href or
                "/download" in href and "pdf" in href.lower()):
            continue
        absolute = urljoin(landing, href)
        if _allowed(absolute) and absolute not in candidates:
            candidates.append(absolute)
    return candidates[:MAX_ATTEMPTS]


def validate_pdf_bytes(raw: bytes) -> str:
    if not raw.startswith(b"%PDF-"):
        raise ValueError("not a PDF binary; HTML or access-denial is not a thesis")
    if len(raw) <= 1000 or len(raw) > MAX_BYTES:
        raise ValueError("PDF payload too small or too large")
    return hashlib.sha256(raw).hexdigest()


def _get(url: str, timeout: float):
    if not _allowed(url):
        raise ValueError("source URL not an allowed institution/DOI domain")
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; IWE-source-access-check/1.0)",
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.2"
    })
    with urlopen(req, timeout=timeout) as response:
        landing = response.geturl()
        if not _allowed(landing):
            raise ValueError("redirected off allowed institution/DOI hosts")
        body = response.read(MAX_BYTES + 1)
        return landing, body, response.headers.get("Content-Type", "")


def probe_thesis(output_dir: Path, timeout: float = 15.) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "iwe_hurlburt2004_public_thesis_access_v1",
        "source_doi": THESIS_DOI,
        "expected_filename": FILENAME,
        "endpoint": DOI_URL,
        "status": "not_recovered",
        "source_pdf_inspected": False,
        "source_marked_unit_join_verified": False,
        "adult_timing_verified_from_thesis": False,
        "strict_h1_promoted": False,
        "attempts": [],
    }
    try:
        landing, raw, typ = _get(DOI_URL, timeout)
        report["landing_url"] = landing
        report["landing_type"] = typ
        if raw.startswith(b"%PDF-"):
            candidates = [(landing, raw)]
        else:
            candidates = [(url, None) for url in extract_source_file_links(
                raw.decode("utf-8", errors="replace"), landing
            )]
            report["source_file_candidates"] = len(candidates)
        for url, body in candidates:
            item = {"url": url}
            try:
                if body is None:
                    destination, body, typ = _get(url, timeout)
                    item["resolved_url"] = destination
                    item["content_type"] = typ
                digest = validate_pdf_bytes(body)
                (output_dir / FILENAME).write_bytes(body)
                item.update({"status": "pdf_binary_recovered",
                             "bytes": len(body), "sha256": digest})
                report.update({"status": "pdf_binary_recovered",
                               "pdf_sha256": digest,
                               "pdf_bytes": len(body)})
                report["attempts"].append(item)
                break
            except (HTTPError, URLError, OSError, ValueError, TimeoutError) as exc:
                item["status"] = "blocked_or_invalid"
                item["reason"] = ("HTTP_" + str(exc.code)
                                  if isinstance(exc, HTTPError)
                                  else type(exc).__name__)
                report["attempts"].append(item)
    except (HTTPError, URLError, OSError, ValueError, TimeoutError) as exc:
        report["landing_error"] = ("HTTP_" + str(exc.code)
                                   if isinstance(exc, HTTPError)
                                   else type(exc).__name__)
    (output_dir / "manifest.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--timeout", type=float, default=15.)
    args = ap.parse_args()
    if args.timeout <= 0:
        ap.error("timeout must be positive")
    record = probe_thesis(args.outdir, args.timeout)
    print("Hurlburt public thesis access:", record["status"])
    print("DOI landing:", record.get("landing_url", record.get("landing_error")))
    print("Institutional PDF candidates:", record.get("source_file_candidates", 0))
    for a in record["attempts"]:
        print(a["status"], a["url"], a.get("reason", ""), a.get("bytes", ""))
    print("Marked-unit join/source date data not verified; no H1 promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
