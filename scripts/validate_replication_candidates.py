#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.replication_candidates import (
    ready_replication_candidates,
    validate_replication_candidates,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate IWE replication-candidate readiness gates."
    )
    parser.add_argument(
        "--registry",
        default="data/registry/replication_candidates.csv",
    )
    args = parser.parse_args()

    df = pd.read_csv(Path(args.registry))
    errors = validate_replication_candidates(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    ready = ready_replication_candidates(df)
    blocked = len(df) - len(ready)
    print(
        f"OK: {len(df)} replication candidates validated; "
        f"{len(ready)} ready, {blocked} blocked/rejected."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
