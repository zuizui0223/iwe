#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.meta import class_contrasts, cluster_robust_summary
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run IWE dependence-aware reference meta summaries."
    )
    parser.add_argument("input")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    summary = cluster_robust_summary(primary)
    contrasts = class_contrasts(summary)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    primary.to_csv(outdir / "primary_tier_a.csv", index=False)
    summary.to_csv(outdir / "class_summary_reference.csv", index=False)
    contrasts.to_csv(outdir / "class_contrasts_reference.csv", index=False)
    print(
        f"Wrote dependence-aware reference outputs to {outdir}. "
        "Uncertainty is CR1-clustered by dependence_id; these remain reference diagnostics, "
        "not the final publication model."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
