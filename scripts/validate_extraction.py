#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from iwe.validation import validate_effect_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an IWE effect extraction table.")
    parser.add_argument("path")
    args = parser.parse_args()

    df = pd.read_csv(Path(args.path))
    errors = validate_effect_rows(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(df)} effect rows validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
