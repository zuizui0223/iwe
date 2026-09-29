#!/usr/bin/env python3
from __future__ import annotations

import argparse

import pandas as pd

from iwe.unit_provenance import validate_strict_unit_provenance


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate exposure/response unit semantics for current real strict effects."
    )
    parser.add_argument("--effects", default="data/extraction/direct_effects.csv")
    parser.add_argument(
        "--units", default="data/registry/strict_effect_unit_provenance.csv"
    )
    args = parser.parse_args()

    errors = validate_strict_unit_provenance(
        pd.read_csv(args.effects),
        pd.read_csv(args.units),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    units = pd.read_csv(args.units)
    print(
        f"OK: {len(units)} current real strict-window effects have explicit "
        "exposure/response unit semantics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
