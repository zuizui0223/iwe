#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.meta import cluster_robust_summary
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run leave-one-dependence-cluster IWE reference sensitivity summaries."
    )
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    rows: list[pd.DataFrame] = []

    dependence_ids = sorted(primary["dependence_id"].dropna().astype(str).unique())
    for dependence_id in dependence_ids:
        reduced = primary.loc[primary["dependence_id"].astype(str) != dependence_id]
        if reduced.empty:
            continue
        summary = cluster_robust_summary(reduced)
        summary.insert(0, "omitted_dependence_id", dependence_id)
        rows.append(summary)

    if rows:
        out = pd.concat(rows, ignore_index=True)
    else:
        out = pd.DataFrame(
            columns=[
                "omitted_dependence_id",
                "interaction_type",
                "estimate",
                "se",
                "ci_low",
                "ci_high",
                "k_effects",
                "m_dependence",
                "df",
                "method",
                "inferential_status",
            ]
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(
        f"Wrote {len(out)} leave-one-dependence reference rows to {output}; "
        f"starting from {len(dependence_ids)} dependence clusters."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
