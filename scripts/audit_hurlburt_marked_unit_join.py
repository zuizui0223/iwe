"""Hurlburt (2004) non-promoting source-unit join preflight.

Inputs are analyst-transcribed ORIGINAL records (not COSEWIC annual summaries):
  marked_units.csv, adult_census.csv, mature_fruits.csv, provenance.json.
The TSV/CSV column labels are a normalization contract, NOT a claim that
the thesis has been shown to contain these tables or original row IDs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.hurlburt_join import audit_marked_unit_join


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("marked_units", type=Path)
    ap.add_argument("adult_census", type=Path)
    ap.add_argument("mature_fruits", type=Path)
    ap.add_argument("provenance", type=Path)
    ap.add_argument("output_dir", type=Path)
    args = ap.parse_args()
    result = audit_marked_unit_join(
        pd.read_csv(args.marked_units, dtype={"clone_id": str, "inflorescence_id": str}),
        pd.read_csv(args.adult_census),
        pd.read_csv(args.mature_fruits, dtype={"clone_id": str, "inflorescence_id": str, "fruit_id": str}),
        json.loads(args.provenance.read_text(encoding="utf-8")),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outfile = args.output_dir / "marked_unit_join_audit.json"
    outfile.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print(f"Hurlburt source-unit join status: {result['status']}")
    print(f"Matched mature fruits: {result['mature_fruits_with_exact_marked_unit_join']}"
          f"/{result['total_mature_fruits']}; admitted SMD effects: 0.")
    print(f"Wrote {outfile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
