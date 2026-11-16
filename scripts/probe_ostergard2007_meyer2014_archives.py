#!/usr/bin/env python3
"""Non-promoting targeted public-archive provenance probe.

Östergård et al. 2007 Ecology 10.1890/07-0346.1:
  Publisher-linked Figshare collection 10.6084/m9.figshare.c.3300059.
Meyer et al. 2014 Am Nat 10.1086/675063:
  Dryad dataset 10.5061/dryad.k8m7b.

Only manifests/listings for exact source-linked records are read.
Never infer source row values or claim opposite evolutionary mechanisms
from a metadata hit; no effect sizes or source datasets are altered.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen


FIGSHARE_COLLECTION = 3300059
FIGSHARE_BASE = "https://api.figshare.com/v2"
DRYAD_DOI = "10.5061/dryad.k8m7b"
DRYAD_API = "https://datadryad.org/api/v2"
MAX_BODY = 1_000_000
MAX_ARTICLES = 25
ALLOW_HOSTS = {"api.figshare.com", "datadryad.org"}
USER_AGENT = "IWE-archive-provenance/1.0"


def safe_read_json(url: str, timeout: float = 15) -> tuple[dict | list | None, str | None]:
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in ALLOW_HOSTS:
        return None, "unapproved_source_endpoint"
    try:
        request = Request(url, headers={"Accept": "application/json",
                                        "User-Agent": USER_AGENT})
        with urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return None, f"HTTP_{response.status}"
            if urlsplit(response.geturl()).hostname not in ALLOW_HOSTS:
                return None, "source_redirect_outside_allowlist"
            payload = response.read(MAX_BODY + 1)
        if len(payload) > MAX_BODY:
            return None, "JSON_payload_too_large"
        data = json.loads(payload.decode("utf-8"))
        if not isinstance(data, (list, dict)):
            return None, "unexpected_response_shape"
        return data, None
    except HTTPError as err:
        return None, f"HTTP_{err.code}"
    except (URLError, TimeoutError, ConnectionError, OSError):
        return None, "network_unavailable"
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return None, "invalid_json"


def source_figshare(timeout: float = 15) -> dict:
    base = f"{FIGSHARE_BASE}/collections/{FIGSHARE_COLLECTION}"
    record: dict = {
        "provenance": "10.6084/m9.figshare.c.3300059",
        "source_paper": "10.1890/07-0346.1",
        "collection_id": FIGSHARE_COLLECTION,
        "articles": [],
        "raw_data_recovered": False,
        "source_join_verified": False,
        "strict_effect_promoted": False,
    }
    col, err = safe_read_json(base, timeout)
    if err:
        record["status"] = "blocked"
        record["collection_error"] = err
        return record
    if not isinstance(col, dict):
        record["status"] = "unexpected_response"
        return record
    record["collection_title"] = str(col.get("title") or "")[:180]
    record["collection_doi"] = str(col.get("doi") or "")[:160]
    items, err = safe_read_json(f"{base}/articles?page_size=25", timeout)
    if err:
        record["status"] = "collection_readable_articles_unavailable"
        record["articles_error"] = err
        return record
    if not isinstance(items, list):
        record["status"] = "unexpected_articles_response"
        return record
    for item in items[:MAX_ARTICLES]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), int):
            continue
        ident = item["id"]
        detail, d_err = safe_read_json(f"{FIGSHARE_BASE}/articles/{ident}", timeout)
        art = {
            "id": ident,
            "title": str(item.get("title") or "")[:180],
            "doi": str(item.get("doi") or "")[:140],
            "detail_error": d_err,
            "listed_files": [],
        }
        if isinstance(detail, dict):
            for file in (detail.get("files") or [])[:30]:
                if isinstance(file, dict):
                    art["listed_files"].append({
                        "id": file.get("id"),
                        "name": str(file.get("name") or "")[:180],
                        "size": file.get("size"),
                        "is_link_only": bool(file.get("is_link_only", False)),
                    })
        record["articles"].append(art)
    record["status"] = ("found_source_linked_records" if record["articles"]
                        else "collection_reachable_no_articles")
    return record


def source_dryad(timeout: float = 15) -> dict:
    path = f"{DRYAD_API}/datasets/{quote('doi:' + DRYAD_DOI, safe='')}"
    record: dict = {
        "source_paper": "10.1086/675063",
        "dataset_doi": DRYAD_DOI,
        "dataset_api": path,
        "source_files": [],
        "raw_data_recovered": False,
        "source_join_verified": False,
        "strict_effect_promoted": False,
    }
    data, err = safe_read_json(path, timeout)
    if err:
        record["status"] = "blocked"
        record["metadata_error"] = err
        return record
    if not isinstance(data, dict):
        record["status"] = "unexpected_response"
        return record
    record["title"] = str(data.get("title") or "")[:180]
    record["id"] = data.get("id")
    record["version"] = data.get("versionNumber")
    url = data.get("_links", {}).get("stash:files", {}).get("href")
    if url:
        if url.startswith("/"):
            url = "https://datadryad.org" + url
        files, ferr = safe_read_json(url, timeout)
        if ferr:
            record["status"] = "dataset_reachable_files_unavailable"
            record["files_error"] = ferr
        elif isinstance(files, dict):
            for f in (files.get("_embedded", {}).get("stash:files") or [])[:30]:
                if isinstance(f, dict):
                    record["source_files"].append({
                        "id": f.get("id"),
                        "filename": str(f.get("path") or "")[:180],
                        "size": f.get("size"),
                    })
            record["status"] = "dataset_reachable"
        else:
            record["status"] = "files_not_listed"
    else:
        record["status"] = "dataset_reachable_no_file_link"
    return record


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--timeout", type=float, default=15)
    args = ap.parse_args()
    if args.timeout <= 0:
        ap.error("timeout must be >0")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    status = {
        "schema": "iwe_opposing_host_filter_public_archive_probe_v1",
        "figshare": source_figshare(timeout=args.timeout),
        "dryad": source_dryad(timeout=args.timeout),
        "causal_claim_validated": False,
        "raw_fitness_contrast_estimated": False,
        "strict_h1_count_changed": False,
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for key in ("figshare", "dryad"):
        a = status[key]
        count = len(a.get("articles", a.get("source_files", [])))
        print(f"{key}: {a['status']}; listed={count}; "
              f"reason={a.get('collection_error', a.get('metadata_error', 'none'))}")
    print("No raw observations or effect sizes promoted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
