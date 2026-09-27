#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from iwe.cardamine_raw import normalize_cardamine_workbooks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize audited Cardamine Dryad XLSX transects for the frozen preflight."
    )
    parser.add_argument("output_dir")
    parser.add_argument(
        "--workbook",
        action="append",
        nargs=3,
        metavar=("YEAR", "ECOTYPE", "PATH"),
        required=True,
        help="Repeat for each Dryad workbook, e.g. --workbook 2012 early file.xlsx",
    )
    args = parser.parse_args()

    specs = [(int(year), ecotype, path) for year, ecotype, path in args.workbook]
    timing, summaries, audit = normalize_cardamine_workbooks(specs)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    timing.to_csv(outdir / "plant_timing.csv", index=False)
    summaries.to_csv(outdir / "plant_summaries.csv", index=False)
    audit.to_csv(outdir / "raw_normalization_audit.csv", index=False)

    ready = int((audit["outcome_status"] == "ready").sum())
    excluded = int((audit["outcome_status"] != "ready").sum())
    print(
        f"Wrote Cardamine raw normalization to {outdir}; "
        f"source-backed outcomes={ready}, excluded/audited={excluded}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
