#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.search_coverage import (
    render_search_coverage_status,
    validate_search_runs,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and render the IWE systematic-search coverage registry."
    )
    parser.add_argument("--registry", default="data/registry/search_runs.csv")
    parser.add_argument("--document", default="docs/SEARCH_COVERAGE_STATUS.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.registry)
    errors = validate_search_runs(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    rendered = render_search_coverage_status(df).rstrip() + "\n"
    document = Path(args.document)
    if args.check:
        if not document.exists():
            print(f"ERROR: search coverage document is missing: {document}")
            return 1
        if document.read_text(encoding="utf-8") != rendered:
            print(
                "ERROR: search coverage status is stale. "
                "Run scripts/render_search_coverage_status.py and commit the result."
            )
            return 1
        print(f"OK: search coverage registry valid; {len(df)} runs registered.")
        return 0

    document.write_text(rendered, encoding="utf-8")
    print(f"Wrote search coverage status for {len(df)} runs to {document}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
