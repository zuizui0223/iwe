#!/usr/bin/env python3
"""Produce an auditable source sampling-panel receipt; NOT a phenology effect."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd
from iwe.oikos_sampling_bridge import build_oikos_sampling_crosswalk

DEFAULT_TABLE = Path("data/registry/oikos_2018_table_a1_sampling.csv")
DEFAULT_TAXON = Path("data/registry/oikos_2018_to_chocho_taxonomy.csv")
DEFAULT_HOSTS = Path("data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", type=Path, default=DEFAULT_TABLE)
    ap.add_argument("--taxa", type=Path, default=DEFAULT_TAXON)
    ap.add_argument("--host-geography", type=Path, default=DEFAULT_HOSTS)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    strata, species, result = build_oikos_sampling_crosswalk(
        pd.read_csv(args.table, dtype=str, keep_default_na=False),
        pd.read_csv(args.taxa, dtype=str, keep_default_na=False),
        pd.read_csv(args.host_geography, dtype=str, keep_default_na=False),
    )
    result["input_sha256"] = {
        "oikos_appendix_table_a1_transcription": _sha(args.table),
        "name_crosswalk": _sha(args.taxa),
        "chocho_frozen_host_geography": _sha(args.host_geography),
    }
    strata.to_csv(args.output_dir / "oikos_region_species_year_strata.csv", index=False)
    species.to_csv(args.output_dir / "oikos_species_to_chocho_hosts.csv", index=False)
    (args.output_dir / "source_crosswalk_receipt.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
