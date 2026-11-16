from __future__ import annotations

import argparse
from pathlib import Path

from iwe.riemer_paired_bounds import render_bounds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--output", type=Path,
        default=Path("docs/RIEMER2024_PAIRED_CLASSIFICATION_BOUNDS.md"),
    )
    args = parser.parse_args()
    rendered = render_bounds()
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            print("ERROR: stale published-margins audit: " + str(args.output))
            return 1
        print("Riemer published-margins audit current.")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print("Wrote " + str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
