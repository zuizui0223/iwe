#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.screening import render_screening_snapshot, replace_screening_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render or check the registry-derived screening snapshot."
    )
    parser.add_argument(
        "--registry",
        default="data/registry/studies.csv",
        help="study registry CSV",
    )
    parser.add_argument(
        "--document",
        default="docs/SCREENING_BATCH_001.md",
        help="screening Markdown document",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the Markdown snapshot differs from the current registry",
    )
    args = parser.parse_args()

    registry = Path(args.registry)
    document = Path(args.document)
    df = pd.read_csv(registry)
    snapshot = render_screening_snapshot(df)
    current = document.read_text(encoding="utf-8")
    rendered = replace_screening_snapshot(current, snapshot)

    if args.check:
        if rendered != current:
            print(
                "ERROR: screening snapshot is stale. "
                "Run scripts/render_screening_batch.py and commit the result."
            )
            return 1
        print(f"OK: screening snapshot matches {len(df)} registry rows.")
        return 0

    document.write_text(rendered, encoding="utf-8")
    print(f"Wrote screening snapshot for {len(df)} registry rows to {document}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
