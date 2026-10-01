#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from iwe.iwe023_raw import audit_iwe023_workbook


def _sheet(value: str) -> str | int:
    try:
        return int(value)
    except ValueError:
        return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the IWE023 Gallagher-Campbell phenology workbook and reconstruct "
            "the frozen week-1 minus week-4 SMD directly from plant-level seed set."
        )
    )
    parser.add_argument("workbook")
    parser.add_argument("output_dir")
    parser.add_argument("--week-col", required=True)
    parser.add_argument("--seed-set-col", required=True)
    parser.add_argument("--plant-id-col")
    parser.add_argument("--sheet", default="0")
    parser.add_argument("--relative-mean-tolerance", type=float, default=0.015)
    parser.add_argument("--f-tolerance", type=float, default=0.08)
    args = parser.parse_args()

    summary, effects = audit_iwe023_workbook(
        args.workbook,
        week_col=args.week_col,
        seed_set_col=args.seed_set_col,
        plant_id_col=args.plant_id_col,
        sheet_name=_sheet(args.sheet),
        relative_mean_tolerance=args.relative_mean_tolerance,
        f_tolerance=args.f_tolerance,
    )

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(outdir / "week_audit.csv", index=False)
    effects.to_csv(outdir / "raw_effect_candidate.csv", index=False)

    effect = effects.iloc[0]
    status = {
        "schema": "iwe023_raw_audit_v1",
        "dataset_doi": "10.7280/D19X0D",
        "dryad_file_id": 341732,
        "source_file": "gallagher&campbell_phenologyExperimentData.xlsx",
        "raw_effect_ready": bool(effect["raw_effect_ready"]),
        "effect_native": (
            float(effect["effect_native"]) if bool(effect["raw_effect_ready"]) else None
        ),
        "variance_native": (
            float(effect["variance_native"]) if bool(effect["raw_effect_ready"]) else None
        ),
        "direct_registry_mutation_performed": False,
    }
    (outdir / "audit_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote IWE023 raw audit to {outdir}; "
        f"raw_effect_ready={status['raw_effect_ready']}. "
        "No extraction registry row was changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
