#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.cardamine_promotion import build_cardamine_promotion_packet


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a transactionally validated, non-mutating Cardamine promotion packet."
    )
    parser.add_argument("plant_timing_csv")
    parser.add_argument("adult_events_csv")
    parser.add_argument("adult_provenance_json")
    parser.add_argument("plant_summaries_csv")
    parser.add_argument("output_dir")
    parser.add_argument("--studies", default="data/registry/studies.csv")
    parser.add_argument("--effects", default="data/extraction/direct_effects.csv")
    parser.add_argument("--adjudications", default="data/registry/strict_h1_adjudications.csv")
    parser.add_argument("--candidates", default="data/registry/replication_candidates.csv")
    parser.add_argument("--routes", default="data/registry/replication_completion_routes.csv")
    args = parser.parse_args()

    provenance = json.loads(
        Path(args.adult_provenance_json).read_text(encoding="utf-8")
    )
    packet = build_cardamine_promotion_packet(
        pd.read_csv(args.plant_timing_csv),
        pd.read_csv(args.adult_events_csv),
        provenance,
        pd.read_csv(args.plant_summaries_csv),
        pd.read_csv(args.studies),
        pd.read_csv(args.effects),
        pd.read_csv(args.adjudications),
        pd.read_csv(args.candidates),
        pd.read_csv(args.routes),
    )

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    packet["exposure"].to_csv(outdir / "timing_exposure.csv", index=False)
    packet["audit"].to_csv(outdir / "outcome_smd_audit.csv", index=False)
    packet["effects_append"].to_csv(outdir / "draft_direct_effects_append.csv", index=False)
    packet["adjudications_append"].to_csv(
        outdir / "draft_strict_adjudications_append.csv", index=False
    )
    packet["candidate_ready_row"].to_csv(
        outdir / "draft_candidate_ready_row.csv", index=False
    )
    packet["completion_routes_after"].to_csv(
        outdir / "draft_completion_routes_after.csv", index=False
    )
    (outdir / "promotion_manifest.json").write_text(
        json.dumps(packet["manifest"], indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote validated Cardamine promotion packet to {outdir}; "
        f"draft effects={len(packet['effects_append'])}. No repository files were changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
