from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.selection_shift import (
    render_selection_shift_audit,
    validate_selection_shift_registry,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/registry/selection_shift_components.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/SELECTION_SHIFT_PILOT_AUDIT.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.registry)
    errors = validate_selection_shift_registry(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    rendered = render_selection_shift_audit(df)
    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing generated audit: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale generated audit: {args.output}")
            return 1
        print(f"Selection-shift pilot audit is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote selection-shift pilot audit to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
