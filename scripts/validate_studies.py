#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "study_id",
    "source_id",
    "title",
    "system_id",
    "screening_status",
    "screening_reason",
    "interaction_type_candidate",
    "notes",
]

ALLOWED_SCREENING_STATUS = {
    "include",
    "include_shape",
    "context_only",
    "exclude",
    "unresolved",
    "unresolved_strict",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the IWE study-level screening registry."
    )
    parser.add_argument("path", nargs="?", default="data/registry/studies.csv")
    args = parser.parse_args()

    path = Path(args.path)
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"ERROR: failed to parse {path}: {type(exc).__name__}: {exc}")
        return 1

    errors: list[str] = []
    if list(df.columns) != REQUIRED_COLUMNS:
        errors.append(
            "unexpected columns/order: "
            f"expected {REQUIRED_COLUMNS}, got {list(df.columns)}"
        )

    if "study_id" in df.columns:
        if df["study_id"].isna().any() or (df["study_id"].astype(str).str.strip() == "").any():
            errors.append("missing study_id")
        if df["study_id"].duplicated().any():
            dupes = sorted(df.loc[df["study_id"].duplicated(keep=False), "study_id"].astype(str).unique())
            errors.append(f"duplicate study_id: {dupes}")

    if "screening_status" in df.columns:
        unknown = sorted(
            set(df["screening_status"].dropna().astype(str))
            - ALLOWED_SCREENING_STATUS
        )
        if unknown:
            errors.append(f"unknown screening_status: {unknown}")

    for column in ["source_id", "title", "system_id", "screening_reason", "interaction_type_candidate"]:
        if column in df.columns:
            missing = df[column].isna() | (df[column].astype(str).str.strip() == "")
            if missing.any():
                ids = df.loc[missing, "study_id"].astype(str).tolist()
                errors.append(f"missing {column} for study_id: {ids}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {len(df)} study screening records validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
