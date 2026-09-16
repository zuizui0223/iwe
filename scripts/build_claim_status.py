#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

from iwe.schema import INTERACTION_TYPES
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description="Build IWE machine-readable hypothesis status from the current corpus.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    classes = set(primary["interaction_type"].dropna())
    real_rows = primary.loc[~primary["source_id"].astype(str).str.startswith("synthetic:")]

    h1_structure = INTERACTION_TYPES.issubset(classes)
    payload = {
        "schema": "iwe_claim_status_v1",
        "biological_evidence_rows": int(len(real_rows)),
        "synthetic_rows_excluded_from_biological_claims": int(len(primary) - len(real_rows)),
        "H1": {
            "status": "unresolved" if real_rows.empty else ("evaluable" if h1_structure else "not_evaluable"),
            "reason": "no real extracted Tier-A evidence" if real_rows.empty else ("all three interaction classes represented" if h1_structure else "one or more preregistered interaction classes absent"),
        },
        "H2": {
            "status": "unresolved",
            "reason": "curvature requires dedicated mixed-system within-study synchrony information beyond the first-release effect table",
        },
        "H3": {
            "status": "unresolved",
            "reason": "redundancy buffering is secondary and requires independently measured redundancy effects",
        },
        "claim_support_declared": False,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote claim status to {output}; no support state is inferred by this utility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
