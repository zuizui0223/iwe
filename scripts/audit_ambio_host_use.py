#!/usr/bin/env python3
"""Build 2010 published egg-rate/chocho resource crosswalk (descriptive)."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd
from iwe.ambio_host_use import build_ambio_host_use

INPUT_TABLE = Path("data/registry/ambio_2015_table1_2010_host_use.csv")
TAXA = Path("data/registry/oikos_2018_to_chocho_taxonomy.csv")
GEO = Path("data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=INPUT_TABLE)
    parser.add_argument("--taxonomy", type=Path, default=TAXA)
    parser.add_argument("--host-geography", type=Path, default=GEO)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    table, contrasts, receipt = build_ambio_host_use(
        pd.read_csv(args.source, dtype=str, keep_default_na=False),
        pd.read_csv(args.taxonomy, dtype=str, keep_default_na=False),
        pd.read_csv(args.host_geography, dtype=str, keep_default_na=False),
    )
    receipt["source_input_sha256"] = {
        "Ambio_2015_Table1_transcription": digest(args.source),
        "Oikos_taxon_crosswalk": digest(args.taxonomy),
        "chocho_frozen_11_host_geography": digest(args.host_geography),
    }
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "ambio_region_host_2010_egg_rates.csv", index=False)
    contrasts.to_csv(out / "cardamine_vs_capsella_2010_descriptive.csv", index=False)
    (out / "ambio_source_audit.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
