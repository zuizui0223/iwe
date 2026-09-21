#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.meta import class_contrasts, cluster_robust_summary
from iwe.validation import build_primary_dataset


def _stratified_reference_outputs(primary: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if primary.empty:
        summary = cluster_robust_summary(primary)
        contrasts = class_contrasts(summary)
        return summary, contrasts

    summaries: list[pd.DataFrame] = []
    contrasts: list[pd.DataFrame] = []
    for _, part in primary.groupby("effect_family", sort=True):
        family_summary = cluster_robust_summary(part)
        summaries.append(family_summary)
        family_contrasts = class_contrasts(family_summary)
        if not family_contrasts.empty:
            contrasts.append(family_contrasts)

    summary = pd.concat(summaries, ignore_index=True)
    if contrasts:
        contrast_df = pd.concat(contrasts, ignore_index=True)
    else:
        contrast_df = pd.DataFrame(
            columns=[
                "effect_family",
                "contrast",
                "estimate",
                "se",
                "ci_low",
                "ci_high",
                "df",
                "inferential_status",
            ]
        )
    return summary, contrast_df


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run IWE dependence-aware reference meta summaries."
    )
    parser.add_argument("input")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    summary, contrasts = _stratified_reference_outputs(primary)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    primary.to_csv(outdir / "primary_tier_a.csv", index=False)
    summary.to_csv(outdir / "class_summary_reference.csv", index=False)
    contrasts.to_csv(outdir / "class_contrasts_reference.csv", index=False)
    print(
        f"Wrote effect-family-stratified dependence-aware reference outputs to {outdir}. "
        "No native effect families are pooled without a registered conversion; "
        "uncertainty is CR1-clustered by dependence_id."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
