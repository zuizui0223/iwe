from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.phase_alignment import (
    render_phase_alignment_gate,
    validate_phase_alignment_registry,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/registry/phase_alignment_candidates.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/PHASE_ALIGNMENT_CONFIRMATORY_GATE.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.registry)
    errors = validate_phase_alignment_registry(df)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    rendered = render_phase_alignment_gate(df)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing generated phase-alignment gate: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale phase-alignment gate: {args.output}")
            return 1
        print(f"Phase-alignment gate is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote phase-alignment gate to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
