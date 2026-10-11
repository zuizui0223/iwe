from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.propagation import render_propagation_audit, validate_propagation_registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/registry/temporal_signal_components.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/TEMPORAL_SIGNAL_PROPAGATION_AUDIT.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.registry)
    errors = validate_propagation_registry(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    rendered = render_propagation_audit(df)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing propagation audit: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale propagation audit: {args.output}")
            return 1
        print(f"Temporal signal-propagation audit is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote temporal signal-propagation audit to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
