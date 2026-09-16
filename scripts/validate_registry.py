#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from iwe.schema import INTERACTION_TYPES


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the IWE candidate-system registry.")
    parser.add_argument("path", nargs="?", default="data/registry/systems.csv")
    args = parser.parse_args()

    path = Path(args.path)
    df = pd.read_csv(path)
    required = {"system_id", "plant_group", "animal_group", "interaction_type", "candidate_status"}
    missing = required - set(df.columns)
    errors: list[str] = []
    if missing:
        errors.append(f"missing columns: {sorted(missing)}")
    if "system_id" in df and df["system_id"].duplicated().any():
        errors.append("duplicate system_id")
    if "interaction_type" in df:
        unknown = sorted(set(df["interaction_type"].dropna()) - INTERACTION_TYPES)
        if unknown:
            errors.append(f"unknown interaction_type: {unknown}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(df)} candidate systems validated; candidate status does not imply admission.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
