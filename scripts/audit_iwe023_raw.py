#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from iwe.iwe023_raw import audit_iwe023_raw, workbook_inventory


def _parse_week_order(value: str | None):
    if value is None:
        return None
    items = [item.strip() for item in value.split(",")]
    if len(items) != 4 or any(not item for item in items):
        raise ValueError("--week-order must be four comma-separated values")
    return items


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect or audit the public IWE023 phenology workbook and reconstruct "
            "the week-1 versus week-4 SMD from plant-level seed set."
        )
    )
    parser.add_argument("input")
    parser.add_argument("output_dir")
    parser.add_argument("--sheet")
    parser.add_argument("--week-col")
    parser.add_argument("--plant-col")
    parser.add_argument("--seed-set-col")
    parser.add_argument("--mature-seeds-col")
    parser.add_argument("--flowers-col")
    parser.add_argument("--week-order")
    parser.add_argument("--mean-tolerance", type=float, default=0.02)
    parser.add_argument("--f-tolerance", type=float, default=0.03)
    parser.add_argument(
        "--inventory-only",
        action="store_true",
        help="write sheet/column inventory without reading any response semantics",
    )
    args = parser.parse_args()

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    inventory = workbook_inventory(args.input)
    inventory.to_csv(outdir / "workbook_inventory.csv", index=False)

    if args.inventory_only:
        print(f"Wrote IWE023 workbook inventory to {outdir}.")
        return 0

    if not args.week_col or not args.plant_col:
        parser.error("--week-col and --plant-col are required unless --inventory-only")

    summary, anova, effect = audit_iwe023_raw(
        args.input,
        sheet=args.sheet,
        week_col=args.week_col,
        plant_col=args.plant_col,
        seed_set_col=args.seed_set_col,
        mature_seeds_col=args.mature_seeds_col,
        flowers_col=args.flowers_col,
        week_order=_parse_week_order(args.week_order),
        mean_tolerance=args.mean_tolerance,
        f_tolerance=args.f_tolerance,
    )
    summary.to_csv(outdir / "week_summary.csv", index=False)
    anova.to_csv(outdir / "anova_audit.csv", index=False)
    effect.to_csv(outdir / "raw_effect_candidate.csv", index=False)

    row = effect.iloc[0]
    status = {
        "schema": "iwe023_raw_reconstruction_v1",
        "raw_effect_ready": bool(row["raw_effect_ready"]),
        "effect_native": float(row["effect_native"]),
        "variance_native": float(row["variance_native"]),
        "all_group_n_match": bool(row["all_group_n_match"]),
        "all_relative_means_match": bool(row["all_relative_means_match"]),
        "f_matches": bool(row["f_matches"]),
        "direct_registry_mutation_performed": False,
    }
    (outdir / "audit_status.json").write_text(
        json.dumps(status, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote IWE023 raw reconstruction to {outdir}; "
        f"ready={status['raw_effect_ready']}, "
        f"g={status['effect_native']:.10f}, "
        f"var={status['variance_native']:.10f}. "
        "No evidence registry row was changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
