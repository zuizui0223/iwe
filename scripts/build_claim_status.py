#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.replication import replication_target_status
from iwe.schema import INTERACTION_TYPES
from iwe.validation import build_primary_dataset


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build IWE machine-readable hypothesis status from the current corpus."
    )
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    raw = pd.read_csv(Path(args.input))
    primary = build_primary_dataset(raw)
    real_rows = primary.loc[
        ~primary["source_id"].astype(str).str.startswith("synthetic:")
    ].copy()

    classes = set(real_rows["interaction_type"].dropna())
    cluster_counts = {
        interaction_type: int(
            real_rows.loc[
                real_rows["interaction_type"] == interaction_type, "dependence_id"
            ].nunique()
        )
        for interaction_type in sorted(INTERACTION_TYPES)
    }

    family_cluster_counts: dict[str, dict[str, int]] = {}
    if not real_rows.empty:
        for effect_family, part in real_rows.groupby("effect_family", sort=True):
            family_cluster_counts[str(effect_family)] = {
                interaction_type: int(
                    part.loc[
                        part["interaction_type"] == interaction_type, "dependence_id"
                    ].nunique()
                )
                for interaction_type in sorted(INTERACTION_TYPES)
            }

    evaluable_families = [
        family
        for family, counts in family_cluster_counts.items()
        if all(counts[c] >= 2 for c in INTERACTION_TYPES)
    ]

    if real_rows.empty:
        h1_status = "unresolved"
        h1_reason = "no real extracted strict Tier-A evidence"
    elif evaluable_families:
        h1_status = "evaluable"
        h1_reason = (
            "at least one common effect family spans all three interaction classes "
            "with at least two dependence clusters per class"
        )
    elif not INTERACTION_TYPES.issubset(classes):
        h1_status = "not_evaluable"
        h1_reason = "one or more preregistered interaction classes absent"
    else:
        h1_status = "not_evaluable"
        h1_reason = (
            "no single native effect family spans all three interaction classes "
            "with at least two dependence clusters per class"
        )

    payload = {
        "schema": "iwe_claim_status_v4",
        "biological_evidence_rows": int(len(real_rows)),
        "biological_dependence_clusters": int(real_rows["dependence_id"].nunique()),
        "effect_families_present": sorted(set(real_rows["effect_family"].astype(str))),
        "dependence_clusters_by_interaction_type": cluster_counts,
        "dependence_clusters_by_effect_family_and_interaction_type": family_cluster_counts,
        "h1_evaluable_effect_families": evaluable_families,
        "replication_target": replication_target_status(real_rows),
        "synthetic_rows_excluded_from_biological_claims": int(
            len(primary) - len(real_rows)
        ),
        "H1": {
            "status": h1_status,
            "reason": h1_reason,
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
    print(
        f"Wrote claim status to {output}; dependence clusters and common effect family "
        "are required for H1 evaluability."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
