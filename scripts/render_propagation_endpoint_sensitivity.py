from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.endpoint_audit import (
    render_endpoint_sensitivity,
    validate_endpoint_audit,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--propagation",
        type=Path,
        default=Path("data/registry/temporal_signal_components.csv"),
    )
    parser.add_argument(
        "--endpoints",
        type=Path,
        default=Path("data/registry/propagation_endpoint_audit.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/PROPAGATION_ENDPOINT_STRICT_SENSITIVITY.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    propagation = pd.read_csv(args.propagation)
    endpoints = pd.read_csv(args.endpoints)
    errors = validate_endpoint_audit(propagation, endpoints)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    content = render_endpoint_sensitivity(propagation, endpoints)
    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing endpoint sensitivity document: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != content:
            print(f"ERROR: stale endpoint sensitivity document: {args.output}")
            return 1
        print(f"Endpoint sensitivity current: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Rendered endpoint sensitivity to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
