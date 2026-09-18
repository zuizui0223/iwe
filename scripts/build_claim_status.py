#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.feasibility import common_scale_gate
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build IWE machine-readable hypothesis status from the current corpus."
    )
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument(
        "--common-scale",
        default="data/extraction/common_scale_fisher_z.csv",
        help="Common-scale effect table used to gate cross-class H1 inference.",
    )
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    real_rows = primary.loc[
        ~primary["source_id"].astype(str).str.startswith("synthetic:")
    ]

    common_scale_path = Path(args.common_scale)
    common_scale = pd.read_csv(common_scale_path)
    gate = common_scale_gate(common_scale)

    if real_rows.empty:
        h1_status = "unresolved"
        h1_reason = "no real extracted Tier-A evidence"
    elif gate.primary_claim_gate:
        h1_status = "evaluable"
        h1_reason = (
            "common-scale independent-programme gate is open for the primary "
            "cross-class H1 model"
        )
    elif gate.cross_class_fit_allowed:
        h1_status = "not_evaluable"
        h1_reason = (
            "common-scale replication permits exploratory cross-class fitting "
            "only; the primary H1 claim gate remains closed"
        )
    elif gate.coverage_complete:
        h1_status = "not_evaluable"
        h1_reason = (
            "all three interaction classes have common-scale coverage, but "
            "independent-programme replication is still coverage-only"
        )
    else:
        h1_status = "not_evaluable"
        h1_reason = (
            "one or more preregistered interaction classes lack common-scale "
            "independent-programme coverage"
        )

    payload = {
        "schema": "iwe_claim_status_v2",
        "biological_evidence_rows": int(len(real_rows)),
        "synthetic_rows_excluded_from_biological_claims": int(
            len(primary) - len(real_rows)
        ),
        "H1": {
            "status": h1_status,
            "reason": h1_reason,
            "common_scale_gate_status": gate.status,
            "programme_counts": gate.programme_counts,
            "cross_class_fit_allowed": gate.cross_class_fit_allowed,
            "primary_claim_gate": gate.primary_claim_gate,
        },
        "H2": {
            "status": "unresolved",
            "reason": (
                "mixed-system shape evidence exists, but quantitative curvature "
                "requires dedicated within-study synchrony information with "
                "recoverable uncertainty"
            ),
        },
        "H3": {
            "status": "unresolved",
            "reason": (
                "redundancy buffering is secondary and requires independently "
                "measured redundancy effects"
            ),
        },
        "claim_support_declared": False,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"Wrote claim status to {output}; H1 gate={gate.status}; "
        "no support state is inferred by this utility."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
