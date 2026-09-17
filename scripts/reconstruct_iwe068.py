#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd

from iwe.reconstruction import (
    leave_one_out_overlaps,
    prepare_maxfield_phenology,
    prepare_maxfield_seeds,
)

SOURCE_REPO = "jmpowers/ipomopsis-temp"
SOURCE_COMMIT = "9f4ceff87f5eb68c5a09f5e89ea457432e452542"
RAW_BASE = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/"

PHENOLOGY_PATH = "data/traits/2021 Maxfield Phenology - 2021.csv"
SEEDS_PATH = "data/traits/2021 Maxfield Seeds - 2021.csv"
METADATA_PATH = "data/2021 Maxfield Rosettes - 2021OTCs.csv"


def raw_url(path: str) -> str:
    return RAW_BASE + quote(path, safe="/")


def reconstruct() -> tuple[dict[str, object], pd.DataFrame]:
    metadata = pd.read_csv(raw_url(METADATA_PATH))
    phen_raw = pd.read_csv(raw_url(PHENOLOGY_PATH))
    # The first line in the source seed file is a code legend; line 2 is the header.
    seed_raw = pd.read_csv(raw_url(SEEDS_PATH), skiprows=1)

    phen = prepare_maxfield_phenology(phen_raw, metadata)
    seeds = prepare_maxfield_seeds(seed_raw, metadata)

    phen_primary = phen.loc[(phen["temp"] == "control") & (phen["snow"] == "normal")].copy()
    seed_primary = seeds.loc[(seeds["temp"] == "control") & (seeds["snow"] == "normal")].copy()

    overlaps = leave_one_out_overlaps(
        phen_primary,
        plant_col="plantid",
        time_col="census",
        floral_col="floral",
        egg_col="eggs",
    )
    analysis = overlaps.merge(
        seed_primary[["plantid", "seeds_per_flower"]],
        on="plantid",
        how="inner",
        validate="1:1",
    )
    analysis = analysis.loc[
        np.isfinite(analysis["overlap"]) & np.isfinite(analysis["seeds_per_flower"])
    ].sort_values("plantid").reset_index(drop=True)

    n = int(len(analysis))
    if n < 4:
        raise RuntimeError(f"IWE068 requires n >= 4 complete plants; recovered n={n}")
    if analysis["overlap"].nunique() < 2 or analysis["seeds_per_flower"].nunique() < 2:
        raise RuntimeError("IWE068 correlation is not estimable because one analysis variable is constant")

    r = float(np.corrcoef(analysis["overlap"], analysis["seeds_per_flower"])[0, 1])
    if not np.isfinite(r) or abs(r) >= 1:
        raise RuntimeError(f"invalid Pearson r for Fisher transform: {r}")
    fisher_z = float(np.arctanh(r))
    variance = float(1.0 / (n - 3))

    result: dict[str, object] = {
        "study_id": "IWE068",
        "source_repository": SOURCE_REPO,
        "source_commit": SOURCE_COMMIT,
        "primary_subset": "Maxfield 2021; temp=control; snow=normal",
        "timing_metric": "leave-one-out histogram intersection of focal floral curve with Hylemya egg activity",
        "outcome": "source-defined seeds_per_flower",
        "n": n,
        "pearson_r": r,
        "fisher_z_native": fisher_z,
        "variance_native": variance,
        "exposure_direction": "synchrony",
        "interpretation": "negative values mean greater antagonist overlap is associated with lower plant reproductive performance",
    }
    return result, analysis


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconstruct the frozen IWE068 strict antagonist effect.")
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--plants", dest="plants_path", type=Path)
    args = parser.parse_args()

    result, analysis = reconstruct()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)

    if args.json_path is not None:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(text + "\n", encoding="utf-8")
    if args.plants_path is not None:
        args.plants_path.parent.mkdir(parents=True, exist_ok=True)
        analysis.to_csv(args.plants_path, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
