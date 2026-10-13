from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.provenance_support import render_provenance_support


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path,
                        default=Path('docs/PROPAGATION_REFERENCE_SUPPORT_AUDIT.md'))
    args = parser.parse_args()
    text = render_provenance_support(
        pd.read_csv('data/registry/temporal_signal_components.csv'),
        pd.read_csv('data/registry/propagation_endpoint_audit.csv'),
    )
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding='utf-8') != text:
            print('ERROR: stale timing-reference support audit: ' + str(args.output))
            return 1
        print('Timing-reference support audit current')
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding='utf-8')
    print('Wrote ' + str(args.output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
