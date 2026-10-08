#!/usr/bin/env python3
"""Source-pinned Figshare supplemental HTML retrieval, nonpromoting.

Appendix A to Östergård et al. Ecology 2007 DOI 10.1890/07-0346.1.
The publisher's collection DOI 10.6084/m9.figshare.c.3300059 yielded
article ID 3528548 and single file ID 5600258, appendix-A.htm.
This file describes measurements and transformations. It is NOT
a linked original fruit-level dataset or a strict-H1 effect.
"""
from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import argparse
import json

FIGSHARE_FILE_ID = 5600258
URL = f"https://ndownloader.figshare.com/files/{FIGSHARE_FILE_ID}"
MAX_FILE_BYTES = 100_000


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden = True

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = False
        if tag in {"p", "br", "tr", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip() + " ")


def inspect_html(payload: bytes) -> dict:
    if not payload or len(payload) > MAX_FILE_BYTES:
        raise ValueError("empty or oversized source appendix")
    raw = payload.decode("utf-8-sig", errors="replace")
    if "<html" not in raw[:2000].lower() and "<body" not in raw[:2000].lower():
        raise ValueError("source not an HTML appendix")
    parser = Text()
    parser.feed(raw)
    text = " ".join(" ".join(parser.parts).split())
    if len(text) < 500 or len(text) > 100_000:
        raise ValueError("implausible source Appendix A content")
    words = ["phenology", "position", "abortion", "oviposition",
             "fruit", "survival", "egg", "seed", "beetle"]
    keywords = {word: text.lower().count(word) for word in words}
    return {
        "original_file_id": FIGSHARE_FILE_ID,
        "source_article_id": 3528548,
        "published_figshare_collection": 3300059,
        "sha256": sha256(payload).hexdigest(),
        "size_bytes": len(payload),
        "approx_normalized_text_chars": len(text),
        "source_variable_keywords": keywords,
        "raw_data_recovered": False,
        "source_egg_to_seed_join_verified": False,
        "quantitative_smd_promoted": False,
    }


def run(outdir: Path, timeout: float = 15) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    report = {"status": "blocked", "source_url": URL, "file_id": FIGSHARE_FILE_ID}
    try:
        req = Request(URL, headers={"User-Agent": "IWE-source-audit/1.0"})
        with urlopen(req, timeout=timeout) as r:
            data = r.read(MAX_FILE_BYTES + 1)
        report.update(inspect_html(data))
        report["status"] = "source_appendix_recovered"
        (outdir / "appendix-A.htm").write_bytes(data)
    except HTTPError as e:
        report["error"] = f"HTTP_{e.code}"
    except (URLError, TimeoutError, ConnectionError, OSError):
        report["error"] = "network_unavailable"
    except ValueError as e:
        report["error"] = str(e)
    (outdir / "appendix_manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    result = run(args.outdir)
    print("Östergård Figshare appendix:", result["status"])
    print("Appendix description is not original fruit/egg timing data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
