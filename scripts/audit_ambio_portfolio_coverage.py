#!/usr/bin/env python3
"""Published 2010 host-use edge coverage audit; no ecological model."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd
from iwe.ambio_portfolio_coverage import summarize_ambio_portfolio_coverage

A = Path("data/registry/ambio_2015_table1_2010_host_use.csv")
B = Path("data/registry/oikos_2018_to_chocho_taxonomy.csv")
C = Path("data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    inputs = [A, B, C]
    dfs = [pd.read_csv(p, dtype=str, keep_default_na=False) for p in inputs]
    regions, taxa, receipt = summarize_ambio_portfolio_coverage(*dfs)
    receipt["input_sha256"] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in inputs
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    regions.to_csv(args.out_dir / "region_portfolio_coverage.csv", index=False)
    taxa.to_csv(args.out_dir / "reported_host_taxon_egg_coverage.csv", index=False)
    (args.out_dir / "portfolio_coverage_receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
