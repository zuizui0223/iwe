#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from iwe.iwe015_raw import audit_iwe015_raw_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the four IWE015 Dryad female CSVs against published Table 1 "
            "and reconstruct raw early-minus-late Hedges g without using the "
            "published SE/SD label."
        )
    )
    parser.add_argument("female_2012_early")
    parser.add_argument("female_2012_late")
    parser.add_argument("female_2013_early")
    parser.add_argument("female_2013_late")
    parser.add_argument("output_dir")
    parser.add_argument("--successful-fruits-col", required=True)
    parser.add_argument("--fruit-initiation-col")
    parser.add_argument("--predation-rate-col")
    parser.add_argument("--rounding-tolerance", type=float, default=0.0051)
    args = parser.parse_args()

    files = {
        "2012_early": args.female_2012_early,
        "2012_late": args.female_2012_late,
        "2013_early": args.female_2013_early,
        "2013_late": args.female_2013_late,
    }
    audit, components, effects = audit_iwe015_raw_files(
        files,
        successful_fruits_col=args.successful_fruits_col,
        fruit_initiation_col=args.fruit_initiation_col,
        predation_rate_col=args.predation_rate_col,
        rounding_tolerance=args.rounding_tolerance,
    )

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    audit.to_csv(outdir / "group_audit.csv", index=False)
    components.to_csv(outdir / "bounded_component_audit.csv", index=False)
    effects.to_csv(outdir / "raw_effect_candidates.csv", index=False)

    status = {
        "schema": "iwe015_raw_variance_audit_v1",
        "all_group_rows_reproduced": bool(audit["raw_group_ready"].all()),
        "raw_effects_ready": int(effects["raw_effect_ready"].sum()),
        "printed_successful_fruit_dispersion_classification": {
            str(row["group"]): str(row["printed_dispersion_matches"])
            for _, row in audit.iterrows()
        },
        "direct_registry_mutation_performed": False,
    }
    (outdir / "audit_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote IWE015 raw variance audit to {outdir}; "
        f"groups reproduced={int(audit['raw_group_ready'].sum())}/4, "
        f"raw effects ready={int(effects['raw_effect_ready'].sum())}/2. "
        "No primary registry row was changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
