#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse-check every CSV in the IWE data registry."
    )
    parser.add_argument("directory", nargs="?", default="data/registry")
    args = parser.parse_args()

    root = Path(args.directory)
    errors: list[str] = []
    parsed = 0

    for path in sorted(root.glob("*.csv")):
        try:
            df = pd.read_csv(path)
        except Exception as exc:
            errors.append(
                f"{path}: {type(exc).__name__}: {exc}"
            )
            continue

        parsed += 1
        if len(df.columns) != len(set(df.columns)):
            errors.append(f"{path}: duplicate column names")

        if "study_id" in df.columns:
            ids = df["study_id"].dropna().astype(str)
            if (ids.str.strip() == "").any():
                errors.append(f"{path}: blank study_id")
            if ids.duplicated().any():
                dupes = sorted(ids.loc[ids.duplicated(keep=False)].unique())
                errors.append(f"{path}: duplicate study_id {dupes}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: parsed {parsed} registry CSV files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
