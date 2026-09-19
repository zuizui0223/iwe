#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen


USER_AGENT = "iwe-systematic-search/1.0 (https://github.com/zuizui0223/iwe)"


def get_json(url: str, *, retries: int = 5) -> dict:
    """Fetch JSON without turning rate-limit/network failures into zero hits."""
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            )
            with urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except HTTPError as exc:  # pragma: no cover - network execution
            last = exc
            if exc.code == 429 and attempt + 1 < retries:
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2.0 ** (attempt + 1)
                time.sleep(max(delay, 1.0))
                continue
            if attempt + 1 < retries and 500 <= exc.code < 600:
                time.sleep(2.0 ** attempt)
                continue
            raise
        except Exception as exc:  # pragma: no cover - network execution
            last = exc
            if attempt + 1 < retries:
                time.sleep(2.0 ** attempt)
                continue
            raise
    assert last is not None
    raise last


def pubmed_count(query: str, cutoff: str) -> int:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "0",
        "datetype": "pdat",
        "mindate": "1800/01/01",
        "maxdate": cutoff.replace("-", "/"),
        "tool": "iwe_systematic_search",
    }
    data = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        + urlencode(params)
    )
    result = data["esearchresult"]
    if result.get("errorlist"):
        raise RuntimeError(f"PubMed query error: {result['errorlist']}")
    return int(result["count"])


def openalex_count(query: str, cutoff: str) -> int:
    params = {
        "search": query,
        "filter": f"to_publication_date:{cutoff}",
        "per-page": "1",
        "select": "id",
    }
    data = get_json("https://api.openalex.org/works?" + urlencode(params))
    return int(data["meta"]["count"])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count hits for the frozen IWE PubMed/OpenAlex query registry."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/registry/frozen_database_queries.csv",
    )
    parser.add_argument("output")
    args = parser.parse_args()

    rows = list(csv.DictReader(Path(args.input).open(encoding="utf-8", newline="")))
    if not rows:
        raise ValueError("query registry is empty")

    out: list[dict] = []
    for row in rows:
        engine = row["engine"]
        if engine == "pubmed":
            count = pubmed_count(row["query"], row["cutoff_date"])
        elif engine == "openalex":
            count = openalex_count(row["query"], row["cutoff_date"])
        else:
            raise ValueError(f"unknown engine: {engine}")

        record = {
            "query_id": row["query_id"],
            "engine": engine,
            "family": row["family"],
            "cutoff_date": row["cutoff_date"],
            "hit_count": count,
        }
        out.append(record)
        print(json.dumps(record, sort_keys=True))
        # NCBI's unauthenticated E-utilities limit is 3 requests/second.
        # A small universal pause also keeps the multi-engine audit reproducible.
        time.sleep(0.5)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["query_id", "engine", "family", "cutoff_date", "hit_count"],
        )
        writer.writeheader()
        writer.writerows(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
