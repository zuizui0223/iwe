from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.propagation_screening import (
    render_propagation_screening,
    validate_propagation_screening,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--screening",
        type=Path,
        default=Path("data/registry/temporal_propagation_screening.csv"),
    )
    parser.add_argument(
        "--studies",
        type=Path,
        default=Path("data/registry/studies.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/TEMPORAL_PROPAGATION_SCREENING_COVERAGE.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    screening = pd.read_csv(args.screening)
    studies = pd.read_csv(args.studies)
    errors = validate_propagation_screening(screening, studies)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    rendered = render_propagation_screening(screening)
    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing generated propagation screening: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale propagation screening: {args.output}")
            return 1
        print(f"Propagation screening is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote propagation screening to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
