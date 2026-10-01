#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.iwe015_promotion import build_iwe015_promotion_packet


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a transactionally validated, non-mutating IWE015 strict "
            "re-admission packet from raw-effect audit output."
        )
    )
    parser.add_argument("raw_effect_candidates_csv")
    parser.add_argument("output_dir")
    parser.add_argument("--studies", default="data/registry/studies.csv")
    parser.add_argument("--effects", default="data/extraction/direct_effects.csv")
    parser.add_argument(
        "--adjudications", default="data/registry/strict_h1_adjudications.csv"
    )
    parser.add_argument(
        "--window-provenance", default="data/registry/strict_window_provenance.csv"
    )
    parser.add_argument(
        "--unit-provenance", default="data/registry/strict_effect_unit_provenance.csv"
    )
    args = parser.parse_args()

    packet = build_iwe015_promotion_packet(
        pd.read_csv(args.raw_effect_candidates_csv),
        pd.read_csv(args.studies),
        pd.read_csv(args.effects),
        pd.read_csv(args.adjudications),
        pd.read_csv(args.window_provenance),
        pd.read_csv(args.unit_provenance),
    )

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    packet["effects_append"].to_csv(outdir / "draft_direct_effects_append.csv", index=False)
    packet["adjudications_replacement"].to_csv(
        outdir / "draft_strict_adjudications_replacement.csv", index=False
    )
    packet["window_provenance_append"].to_csv(
        outdir / "draft_window_provenance_append.csv", index=False
    )
    packet["unit_provenance_append"].to_csv(
        outdir / "draft_unit_provenance_append.csv", index=False
    )
    packet["effects_after"].to_csv(outdir / "draft_direct_effects_after.csv", index=False)
    packet["adjudications_after"].to_csv(
        outdir / "draft_strict_adjudications_after.csv", index=False
    )
    packet["window_provenance_after"].to_csv(
        outdir / "draft_window_provenance_after.csv", index=False
    )
    packet["unit_provenance_after"].to_csv(
        outdir / "draft_unit_provenance_after.csv", index=False
    )
    (outdir / "promotion_manifest.json").write_text(
        json.dumps(packet["manifest"], indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote validated IWE015 promotion packet to {outdir}; "
        "no repository files were changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
