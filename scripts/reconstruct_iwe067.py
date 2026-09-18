#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd

from iwe.iwe067 import reconstruct_iwe067


def read_table(path: str) -> pd.DataFrame:
    return pd.read_csv(
        Path(path),
        sep=None,
        engine="python",
        na_values=["."],
        keep_default_na=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen IWE067 reconstruction on canonicalized source tables. "
            "See docs/EXTRACTION_IWE067.md for the biological contract."
        )
    )
    parser.add_argument("--phenology", required=True)
    parser.add_argument("--fruit", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--plants")
    args = parser.parse_args()

    phenology = read_table(args.phenology)
    fruit = read_table(args.fruit)
    plants, effects = reconstruct_iwe067(phenology, fruit)

    payload = {
        "study_id": "IWE067",
        "dependence_id": "DEP_IWE067_IPOMOPSIS_HYLEMYA",
        "effect_family": "fisher_z",
        "exposure_direction": "synchrony",
        "years": [asdict(effect) for effect in effects],
    }

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.plants:
        plant_path = Path(args.plants)
        plant_path.parent.mkdir(parents=True, exist_ok=True)
        plants.to_csv(plant_path, index=False)

    print(
        "Wrote frozen IWE067 reconstruction. "
        "Input files must already use the canonical columns documented in iwe.iwe067."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
