#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from iwe.iwe078 import reconstruct_iwe078
from iwe.iwe078_source import load_iwe078_source


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the frozen IWE078 reconstruction on the archived Zenodo source package."
    )
    parser.add_argument("source_dir")
    parser.add_argument("--json", required=True)
    parser.add_argument("--plants")
    parser.add_argument("--canonical-dir")
    args = parser.parse_args()

    source = load_iwe078_source(args.source_dir)
    plants, effects = reconstruct_iwe078(
        source.flowering,
        source.attacks,
        source.fitness,
    )

    payload = {
        "study_id": "IWE078",
        "source_id": "10.5281/zenodo.19488509",
        "dependence_id": "DEP_IWE078_OENOTHERA_MOMPHA",
        "interaction_type": "antagonist",
        "effect_family": "fisher_z",
        "exposure_direction": "synchrony",
        "source_status": "provisional_pending_publication_eligibility",
        "eligible_source_plants": {
            key: len(value) for key, value in source.eligible_ids.items()
        },
        "effects": [asdict(effect) for effect in effects],
    }

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.plants:
        p = Path(args.plants)
        p.parent.mkdir(parents=True, exist_ok=True)
        plants.to_csv(p, index=False)

    if args.canonical_dir:
        cdir = Path(args.canonical_dir)
        cdir.mkdir(parents=True, exist_ok=True)
        source.flowering.to_csv(cdir / "flowering.csv", index=False)
        source.attacks.to_csv(cdir / "attacks.csv", index=False)
        source.fitness.to_csv(cdir / "fitness.csv", index=False)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
