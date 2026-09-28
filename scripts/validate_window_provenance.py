#!/usr/bin/env python3
from __future__ import annotations

import argparse

import pandas as pd

from iwe.window_provenance import validate_strict_window_provenance


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate provenance of every current real strict partner window."
    )
    parser.add_argument("--effects", default="data/extraction/direct_effects.csv")
    parser.add_argument(
        "--provenance", default="data/registry/strict_window_provenance.csv"
    )
    args = parser.parse_args()

    errors = validate_strict_window_provenance(
        pd.read_csv(args.effects),
        pd.read_csv(args.provenance),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    provenance = pd.read_csv(args.provenance)
    print(
        f"OK: {len(provenance)} current real strict-window effects have "
        "same-season admissible partner-window provenance."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
