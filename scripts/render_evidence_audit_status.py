#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.evidence_audit import render_evidence_audit_status


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render or check the registry-derived IWE evidence audit status."
    )
    parser.add_argument("--studies", default="data/registry/studies.csv")
    parser.add_argument("--effects", default="data/extraction/direct_effects.csv")
    parser.add_argument(
        "--adjudications", default="data/registry/strict_h1_adjudications.csv"
    )
    parser.add_argument(
        "--candidates", default="data/registry/replication_candidates.csv"
    )
    parser.add_argument(
        "--routes", default="data/registry/replication_completion_routes.csv"
    )
    parser.add_argument("--document", default="docs/EVIDENCE_AUDIT_STATUS.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render_evidence_audit_status(
        pd.read_csv(args.studies),
        pd.read_csv(args.effects),
        pd.read_csv(args.adjudications),
        pd.read_csv(args.candidates),
        pd.read_csv(args.routes),
    ).rstrip() + "\n"
    document = Path(args.document)

    if args.check:
        if not document.exists():
            print(f"ERROR: evidence audit document is missing: {document}")
            return 1
        if document.read_text(encoding="utf-8") != rendered:
            print(
                "ERROR: evidence audit status is stale. "
                "Run scripts/render_evidence_audit_status.py and commit the result."
            )
            return 1
        print("OK: evidence audit status matches current registries.")
        return 0

    document.write_text(rendered, encoding="utf-8")
    print(f"Wrote evidence audit status to {document}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
