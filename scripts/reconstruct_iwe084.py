#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd

from iwe.iwe084 import reconstruct_iwe084


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct the frozen IWE084 Solidago-Apis SMD."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/extraction/source_rows/IWE084_table5.csv",
    )
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    source = pd.read_csv(args.input)
    effect = reconstruct_iwe084(source)

    payload = {
        "study_id": "IWE084",
        "dataset_id": "GrossWerner1983_Sgraminifolia_1980",
        "dependence_id": "DEP_IWE084_SOLIDAGO_APIS",
        "interaction_type": "mutualist",
        "plant_taxon": "Solidago graminifolia",
        "animal_taxon": "Apis mellifera",
        "phenology_source": "direct_activity",
        "exposure_direction": "synchrony",
        "outcome_family": "seed_set",
        "effect_family": "standardized_mean_difference",
        "sample_size": effect.n_low + effect.n_high,
        "source_id": "10.2307/1942589",
        **asdict(effect),
    }

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
