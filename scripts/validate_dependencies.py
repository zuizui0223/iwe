#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.dependence import validate_effect_dependency_assignments


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate registered cross-publication dependence assignments."
    )
    parser.add_argument(
        "--effects",
        default="data/extraction/direct_effects.csv",
    )
    parser.add_argument(
        "--registry",
        default="data/registry/study_dependencies.csv",
    )
    args = parser.parse_args()

    effects = pd.read_csv(Path(args.effects))
    registry = pd.read_csv(Path(args.registry))
    errors = validate_effect_dependency_assignments(effects, registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"OK: {len(effects)} effect rows satisfy "
        f"{int((registry['dependency_status'] == 'confirmed').sum())} confirmed "
        "study-level dependence assignments."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
