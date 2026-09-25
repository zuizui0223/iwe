#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.replication_routes import (
    active_completion_routes,
    validate_replication_completion_routes,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ranked IWE replication-completion routes."
    )
    parser.add_argument(
        "--routes",
        default="data/registry/replication_completion_routes.csv",
    )
    parser.add_argument(
        "--candidates",
        default="data/registry/replication_candidates.csv",
    )
    args = parser.parse_args()

    routes = pd.read_csv(Path(args.routes))
    candidates = pd.read_csv(Path(args.candidates))
    errors = validate_replication_completion_routes(routes, candidates)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    ranked = active_completion_routes(routes, candidates)
    counts = ranked.groupby("target_class").size().to_dict()
    print(
        f"OK: {len(ranked)} completion routes validated; "
        f"ranked routes by class={counts}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
