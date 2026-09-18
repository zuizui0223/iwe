#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.feasibility import common_scale_gate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        default="data/extraction/common_scale_fisher_z.csv",
    )
    parser.add_argument("output", nargs="?", default="-")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    gate = common_scale_gate(df)

    payload = {
        "status": gate.status,
        "programme_counts": gate.programme_counts,
        "coverage_complete": gate.coverage_complete,
        "cross_class_fit_allowed": gate.cross_class_fit_allowed,
        "primary_claim_gate": gate.primary_claim_gate,
        "rules": {
            "min_independent_programmes_per_class_for_cross_class_fit": 2,
            "min_independent_programmes_per_class_for_primary_claim_gate": 5,
            "note": "IWE execution rules; passing a gate does not guarantee adequate power.",
        },
        "row_count": int(len(df)),
        "independent_programme_count": int(df["dependence_id"].nunique()),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        print(rendered, end="")
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())