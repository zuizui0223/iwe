#!/usr/bin/env python3
"""Response-blind, source-preserving HOSTS prefilter for a single butterfly."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def filter_focal_hosts(
    source: Path, destination: Path, *,
    insect_genus: str = "Anthocharis", insect_species: str = "cardamines",
) -> dict:
    raw_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        if not {"Insect Genus", "Insect Species", "Hostplant Genus", "Hostplant Species"} <= set(fields):
            raise ValueError("Pinned HOSTS resource missing expected native columns")
        rows = [row for row in reader if
                (row.get("Insect Genus") or "").strip() == insect_genus and
                (row.get("Insect Species") or "").strip() == insect_species]
    if not rows:
        raise ValueError("No exact genus-species rows in source; never infer host records")
    with destination.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return {
        "source": str(source),
        "source_sha256": raw_hash,
        "focal_insect": insect_genus + " " + insect_species,
        "focal_source_rows": len(rows),
        "distinct_nonblank_species_level_host_names": len({
            (row["Hostplant Genus"].strip(), row["Hostplant Species"].strip())
            for row in rows if row["Hostplant Genus"].strip()
            and row["Hostplant Species"].strip()
        }),
        "unfiltered_source_replaced": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    receipt = filter_focal_hosts(
        args.source, args.output_directory / "resource.csv"
    )
    (args.output_directory / "source_filter_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
