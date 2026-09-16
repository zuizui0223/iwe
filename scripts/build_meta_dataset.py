#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Tier-A IWE primary meta-analysis dataset.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    df = pd.read_csv(Path(args.input))
    out = build_primary_dataset(df)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(f"Wrote {len(out)} Tier-A rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
