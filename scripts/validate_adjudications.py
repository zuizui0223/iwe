#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.adjudication import validate_effect_adjudications


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate strict-H1 adjudications against extracted real effects."
    )
    parser.add_argument(
        "--effects",
        default="data/extraction/direct_effects.csv",
    )
    parser.add_argument(
        "--registry",
        default="data/registry/strict_h1_adjudications.csv",
    )
    args = parser.parse_args()

    effects = pd.read_csv(Path(args.effects))
    adjudications = pd.read_csv(Path(args.registry))
    errors = validate_effect_adjudications(effects, adjudications)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    strict_n = int((effects["timing_analysis_class"] == "strict_window").sum())
    print(
        f"OK: {len(effects)} real effect rows are covered by strict-H1 adjudication; "
        f"{strict_n} strict-window rows have exact eligible gates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
