#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from iwe.meta import fixed_effect_summary
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Run leave-one-study IWE reference sensitivity summaries.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    rows: list[pd.DataFrame] = []
    for study_id in sorted(primary["study_id"].unique()):
        reduced = primary.loc[primary["study_id"] != study_id]
        if reduced.empty:
            continue
        summary = fixed_effect_summary(reduced)
        summary.insert(0, "omitted_study_id", study_id)
        rows.append(summary)
    out = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(f"Wrote {len(out)} leave-one-study reference rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
