#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


def canonical_doi(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text if text.startswith("10.") else ""


def normalize_title(value: object) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def read_csv(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(encoding="utf-8", newline="")))


def build_known(studies_path: Path, prospective_path: Path) -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    by_doi: dict[str, list[dict]] = defaultdict(list)
    by_title: dict[str, list[dict]] = defaultdict(list)

    for row in read_csv(studies_path):
        item = {
            "study_id": row["study_id"],
            "screening_status": row["screening_status"],
            "source_id": row["source_id"],
            "title": row["title"],
        }
        doi = canonical_doi(row["source_id"])
        if doi:
            by_doi[doi].append(item)
        title_key = normalize_title(row["title"])
        if title_key:
            by_title[title_key].append(item)

    for row in read_csv(prospective_path):
        item = {
            "study_id": row["study_id"],
            "screening_status": row["screening_status"],
            "source_id": row["source_id"],
            "title": "",
        }
        doi = canonical_doi(row["source_id"])
        if doi:
            # Avoid duplicate study ids when a prospective record has already
            # been promoted into studies.csv.
            if not any(x["study_id"] == item["study_id"] for x in by_doi[doi]):
                by_doi[doi].append(item)

    return by_doi, by_title


def title_priority(title: str, families: str, record_type: str) -> tuple[int, list[str]]:
    text = normalize_title(title)
    reasons: list[str] = []
    score = 0

    strong_timing = [
        "phenological mismatch",
        "phenological synchrony",
        "phenological asynchrony",
        "pollinator mismatch",
        "flowering pollinator asynchrony",
    ]
    timing = [
        "phenolog",
        "synchron",
        "asynchron",
        "mismatch",
        "overlap",
        "flowering time",
        "flowering date",
        "emergence",
    ]
    partner = [
        "pollinat",
        "pollinator",
        "bee",
        "wasp",
        "seed predat",
        "seed predator",
        "oviposition",
        "herbivor",
        "florivor",
        "moth",
        "butterfl",
        "hadena",
        "epicephala",
        "tegeticula",
        "chiastocheta",
        "greya",
    ]
    final_fitness = [
        "seed set",
        "fruit set",
        "fecund",
        "fitness",
        "reproductive success",
        "seed production",
        "fruit production",
        "seed output",
        "reproduction",
    ]

    has_strong = any(term in text for term in strong_timing)
    has_timing = any(term in text for term in timing)
    has_partner = any(term in text for term in partner)
    has_fitness = any(term in text for term in final_fitness)

    if has_strong:
        score += 4
        reasons.append("explicit_matching_title")
    elif has_timing:
        score += 2
        reasons.append("timing_title")

    if has_partner:
        score += 2
        reasons.append("identified_partner_title")

    if has_fitness:
        score += 3
        reasons.append("final_reproduction_title")

    if has_timing and has_partner and has_fitness:
        score += 4
        reasons.append("full_H1_chain_in_title")

    family_set = set(str(families or "").split(";"))
    if "mixed_pollinating_seed_predator" in family_set:
        score += 1
        reasons.append("mixed_family_sparse_lane")

    rtype = str(record_type or "").lower()
    if "article" in rtype or "journal article" in rtype:
        score += 1
        reasons.append("published_article_type")
    elif any(x in rtype for x in ["dissertation", "thesis", "book", "paratext"]):
        score -= 1
        reasons.append("nonprimary_source_type")

    return score, reasons


OUTPUT_FIELDS = [
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
    "already_screened",
    "existing_study_ids",
    "existing_screening_statuses",
    "title_priority_score",
    "screening_priority",
    "priority_reasons",
    "screening_decision",
    "screening_reason",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a high-recall screening ledger from the frozen database "
            "inventory. Priority is triage only; no record is auto-excluded."
        )
    )
    parser.add_argument(
        "--inventory",
        default="data/registry/frozen_database_inventory_unique.csv",
    )
    parser.add_argument("--studies", default="data/registry/studies.csv")
    parser.add_argument(
        "--prospective",
        default="data/registry/prospective_search_log.csv",
    )
    parser.add_argument(
        "--output",
        default="data/registry/frozen_database_screening_ledger.csv",
    )
    parser.add_argument(
        "--summary",
        default="data/registry/frozen_database_screening_summary.json",
    )
    args = parser.parse_args()

    inventory = read_csv(Path(args.inventory))
    by_doi, by_title = build_known(Path(args.studies), Path(args.prospective))

    rows: list[dict] = []
    for rec in inventory:
        doi = canonical_doi(rec.get("doi"))
        title_key = normalize_title(rec.get("title"))
        known: list[dict] = []
        if doi:
            known.extend(by_doi.get(doi, []))
        if not known and title_key:
            known.extend(by_title.get(title_key, []))

        # Deduplicate known matches by IWE study id.
        known_by_id = {x["study_id"]: x for x in known}
        known = [known_by_id[k] for k in sorted(known_by_id)]

        score, reasons = title_priority(
            rec.get("title", ""),
            rec.get("families", ""),
            rec.get("record_type", ""),
        )

        if known:
            priority = "already_screened"
            decision = ";".join(
                sorted({x["screening_status"] for x in known})
            )
            screening_reason = "matched existing IWE registry by DOI/title"
        elif score >= 9:
            priority = "P1"
            decision = ""
            screening_reason = ""
        elif score >= 5:
            priority = "P2"
            decision = ""
            screening_reason = ""
        else:
            priority = "P3"
            decision = ""
            screening_reason = ""

        rows.append(
            {
                **{k: rec.get(k, "") for k in OUTPUT_FIELDS if k in rec},
                "already_screened": str(bool(known)).lower(),
                "existing_study_ids": ";".join(x["study_id"] for x in known),
                "existing_screening_statuses": ";".join(
                    sorted({x["screening_status"] for x in known})
                ),
                "title_priority_score": score,
                "screening_priority": priority,
                "priority_reasons": ";".join(reasons),
                "screening_decision": decision,
                "screening_reason": screening_reason,
            }
        )

    order = {"already_screened": 0, "P1": 1, "P2": 2, "P3": 3}
    rows.sort(
        key=lambda r: (
            order[r["screening_priority"]],
            -int(r["title_priority_score"]),
            str(r["publication_year"]),
            str(r["title"]).lower(),
            str(r["record_key"]),
        )
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    priority_counts = Counter(r["screening_priority"] for r in rows)
    family_counts: dict[str, int] = Counter()
    unscreened_family_counts: dict[str, int] = Counter()
    for r in rows:
        for family in filter(None, str(r["families"]).split(";")):
            family_counts[family] += 1
            if r["screening_priority"] != "already_screened":
                unscreened_family_counts[family] += 1

    summary = {
        "schema": "iwe_frozen_database_screening_v1",
        "inventory_records": len(rows),
        "already_screened_records": priority_counts["already_screened"],
        "unscreened_records": (
            priority_counts["P1"] + priority_counts["P2"] + priority_counts["P3"]
        ),
        "priority_counts": dict(sorted(priority_counts.items())),
        "family_memberships_all": dict(sorted(family_counts.items())),
        "family_memberships_unscreened": dict(sorted(unscreened_family_counts.items())),
        "note": (
            "Priority is triage only. P2/P3 are not exclusions; every unscreened "
            "record requires a final screening decision for search completion."
        ),
    }
    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, sort_keys=True))
    print("\nTop unscreened P1 records:")
    shown = 0
    for r in rows:
        if r["screening_priority"] != "P1":
            continue
        print(
            f"{r['doi'] or r['record_key']} | {r['families']} | "
            f"score={r['title_priority_score']} | {r['title']}"
        )
        shown += 1
        if shown >= 40:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
