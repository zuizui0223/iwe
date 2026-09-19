#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


USER_AGENT = "iwe-systematic-search/1.0 (https://github.com/zuizui0223/iwe)"


def get_json(url: str, *, retries: int = 6) -> dict:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            )
            with urlopen(req, timeout=90) as resp:
                return json.load(resp)
        except HTTPError as exc:
            last = exc
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if retryable and attempt + 1 < retries:
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else min(30.0, 2.0 ** (attempt + 1))
                time.sleep(max(delay, 1.0))
                continue
            raise
        except Exception as exc:
            last = exc
            if attempt + 1 < retries:
                time.sleep(min(30.0, 2.0 ** attempt))
                continue
            raise
    assert last is not None
    raise last


def canonical_doi(value: object) -> str:
    if value is None:
        return ""
    doi = str(value).strip().lower()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.strip()


def normalize_title(value: object) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def read_queries(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    if not rows:
        raise ValueError("query registry is empty")
    for row in rows:
        query = row["query"]
        if '\\"' in query:
            raise ValueError(f"{row['query_id']}: malformed backslash quote")
        if query.count('"') % 2:
            raise ValueError(f"{row['query_id']}: unbalanced quote")
        if row["engine"] == "openalex" and (
            " OR " not in query or " AND " not in query
        ):
            raise ValueError(
                f"{row['query_id']}: OpenAlex Boolean groups not preserved"
            )
    return rows


def pubmed_search(row: dict) -> list[dict]:
    params = {
        "db": "pubmed",
        "term": row["query"],
        "retmode": "json",
        "retmax": "10000",
        "datetype": "pdat",
        "mindate": "1800/01/01",
        "maxdate": row["cutoff_date"].replace("-", "/"),
        "tool": "iwe_systematic_search",
    }
    search = get_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        + urlencode(params)
    )["esearchresult"]
    if search.get("errorlist"):
        raise RuntimeError(f"{row['query_id']}: PubMed error {search['errorlist']}")
    pmids = list(search.get("idlist", []))
    expected = int(search["count"])
    if expected != len(pmids):
        raise RuntimeError(
            f"{row['query_id']}: PubMed returned {len(pmids)} IDs for count {expected}"
        )

    out: list[dict] = []
    for start in range(0, len(pmids), 200):
        batch = pmids[start : start + 200]
        params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "json",
            "tool": "iwe_systematic_search",
        }
        data = get_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            + urlencode(params)
        )["result"]
        for pmid in batch:
            item = data[str(pmid)]
            doi = ""
            for article_id in item.get("articleids", []):
                if str(article_id.get("idtype", "")).lower() == "doi":
                    doi = canonical_doi(article_id.get("value"))
                    break
            pubdate = str(item.get("pubdate", "") or "")
            year_match = re.search(r"\b(18|19|20)\d{2}\b", pubdate)
            year = year_match.group(0) if year_match else ""
            out.append(
                {
                    "query_id": row["query_id"],
                    "engine": "pubmed",
                    "family": row["family"],
                    "record_id": str(pmid),
                    "doi": doi,
                    "title": str(item.get("title", "") or "").strip(),
                    "publication_date": pubdate,
                    "publication_year": year,
                    "record_type": ",".join(map(str, item.get("pubtype", []) or [])),
                }
            )
        time.sleep(0.45)
    return out


def openalex_search(row: dict) -> list[dict]:
    cursor = "*"
    by_id: dict[str, dict] = {}
    expected_start: int | None = None
    search_filter = (
        f"title_and_abstract.search:{row['query']},"
        f"to_publication_date:{row['cutoff_date']}"
    )

    while cursor:
        params = {
            "filter": search_filter,
            "per-page": "200",
            "cursor": cursor,
            "select": "id,doi,display_name,publication_date,publication_year,type",
        }
        data = get_json("https://api.openalex.org/works?" + urlencode(params))
        if expected_start is None:
            expected_start = int(data["meta"]["count"])
        for item in data["results"]:
            record_id = str(item.get("id", "")).replace(
                "https://openalex.org/", ""
            )
            if not record_id:
                raise RuntimeError(f"{row['query_id']}: OpenAlex row missing id")
            by_id[record_id] = {
                "query_id": row["query_id"],
                "engine": "openalex",
                "family": row["family"],
                "record_id": record_id,
                "doi": canonical_doi(item.get("doi")),
                "title": str(item.get("display_name", "") or "").strip(),
                "publication_date": str(item.get("publication_date", "") or ""),
                "publication_year": str(item.get("publication_year", "") or ""),
                "record_type": str(item.get("type", "") or ""),
            }
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
        time.sleep(0.15)

    # OpenAlex is a live index. A few records can be indexed while a cursor
    # pagination is running. Re-count after the final page and accept only a
    # snapshot size bracketed by the start/end counts; larger discrepancies
    # still fail closed.
    end_params = {
        "filter": search_filter,
        "per-page": "1",
        "select": "id",
    }
    expected_end = int(
        get_json("https://api.openalex.org/works?" + urlencode(end_params))["meta"]["count"]
    )
    expected_start = 0 if expected_start is None else expected_start
    observed = len(by_id)
    low, high = sorted((expected_start, expected_end))
    if not (low <= observed <= high):
        raise RuntimeError(
            f"{row['query_id']}: OpenAlex snapshot has {observed} unique IDs; "
            f"start count={expected_start}, end count={expected_end}"
        )
    if expected_start != expected_end:
        print(
            json.dumps(
                {
                    "query_id": row["query_id"],
                    "openalex_index_drift": {
                        "start_count": expected_start,
                        "end_count": expected_end,
                        "snapshot_unique_ids": observed,
                    },
                },
                sort_keys=True,
            )
        )
    return [by_id[key] for key in sorted(by_id)]


RAW_FIELDS = [
    "query_id",
    "engine",
    "family",
    "record_id",
    "doi",
    "title",
    "publication_date",
    "publication_year",
    "record_type",
]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def deduplicate(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        doi = canonical_doi(row["doi"])
        title_key = normalize_title(row["title"])
        year = str(row["publication_year"] or "")
        if doi:
            key = f"doi:{doi}"
        elif title_key:
            key = f"titleyear:{title_key}|{year}"
        else:
            key = f"{row['engine']}:{row['record_id']}"
        groups[key].append(row)

    out: list[dict] = []
    for key in sorted(groups):
        part = groups[key]
        # Deterministic representative: DOI-bearing first, then longest title,
        # then lexical engine/id.
        rep = sorted(
            part,
            key=lambda r: (
                0 if canonical_doi(r["doi"]) else 1,
                -len(str(r["title"])),
                r["engine"],
                r["record_id"],
            ),
        )[0]
        out.append(
            {
                "record_key": key,
                "doi": canonical_doi(rep["doi"]),
                "title": rep["title"],
                "publication_date": rep["publication_date"],
                "publication_year": rep["publication_year"],
                "record_type": rep["record_type"],
                "engines": ";".join(sorted({r["engine"] for r in part})),
                "families": ";".join(sorted({r["family"] for r in part})),
                "query_ids": ";".join(sorted({r["query_id"] for r in part})),
                "source_record_ids": ";".join(
                    sorted({f"{r['engine']}:{r['record_id']}" for r in part})
                ),
            }
        )
    return out


UNIQUE_FIELDS = [
    "record_key",
    "doi",
    "title",
    "publication_date",
    "publication_year",
    "record_type",
    "engines",
    "families",
    "query_ids",
    "source_record_ids",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch immutable IWE PubMed/OpenAlex frozen-query inventories."
    )
    parser.add_argument(
        "queries",
        nargs="?",
        default="data/registry/frozen_database_queries.csv",
    )
    parser.add_argument("--raw", required=True)
    parser.add_argument("--unique", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    query_rows = read_queries(Path(args.queries))
    raw: list[dict] = []
    per_query: dict[str, int] = {}

    for row in query_rows:
        if row["engine"] == "pubmed":
            found = pubmed_search(row)
        elif row["engine"] == "openalex":
            found = openalex_search(row)
        else:
            raise ValueError(f"unknown engine: {row['engine']}")
        raw.extend(found)
        per_query[row["query_id"]] = len(found)
        print(
            json.dumps(
                {
                    "query_id": row["query_id"],
                    "engine": row["engine"],
                    "n": len(found),
                },
                sort_keys=True,
            )
        )

    raw = sorted(
        raw,
        key=lambda r: (r["query_id"], r["engine"], r["record_id"]),
    )
    unique = deduplicate(raw)

    write_csv(Path(args.raw), raw, RAW_FIELDS)
    write_csv(Path(args.unique), unique, UNIQUE_FIELDS)

    multi_engine = sum(1 for r in unique if ";" in r["engines"])
    multi_family = sum(1 for r in unique if ";" in r["families"])
    summary = {
        "schema": "iwe_frozen_database_inventory_v1",
        "cutoff_date": sorted({r["cutoff_date"] for r in query_rows}),
        "query_counts": per_query,
        "raw_query_memberships": len(raw),
        "unique_records": len(unique),
        "unique_records_in_multiple_engines": multi_engine,
        "unique_records_in_multiple_families": multi_family,
    }
    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
