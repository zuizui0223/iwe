#!/usr/bin/env python3
"""Reproduce three-repo ALAN × IWE × chocho evidence boundaries from pinned sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd
from iwe.alan_function_bridge import build_three_repo_receipt


DEFAULT_LU = Path("data/registry/alan_lu2026_night_visits_v01.csv")
DEFAULT_BOOM = Path("data/registry/alan_boom2020_spectrum_nursery_v01.csv")
DEFAULT_IWE = Path("data/registry/replication_candidates.csv")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Source-audited mechanism accounting, NOT an IWE strict H1 or global ALAN estimate."
    )
    p.add_argument("--lu", type=Path, default=DEFAULT_LU)
    p.add_argument("--boom", type=Path, default=DEFAULT_BOOM)
    p.add_argument("--iwe-candidates", type=Path, default=DEFAULT_IWE)
    p.add_argument("--output-dir", type=Path, required=True)
    a = p.parse_args()
    paths = {"lu_original_all_surveys": a.lu,
             "boom_original_spectral_table": a.boom,
             "iwe_registry_read_only": a.iwe_candidates}
    lu = pd.read_csv(a.lu, dtype=str, keep_default_na=False)
    boom = pd.read_csv(a.boom, dtype=str, keep_default_na=False)
    iwe = pd.read_csv(a.iwe_candidates, dtype=str, keep_default_na=False)
    lu_counts, efficacy, boom_spectra, receipt = build_three_repo_receipt(
        lu, boom, iwe
    )
    receipt["input_sha256"] = {key: digest(path) for key, path in paths.items()}
    a.output_dir.mkdir(parents=True, exist_ok=True)
    lu_counts.to_csv(a.output_dir / "lu2026_night_visit_composition.csv", index=False)
    efficacy.to_csv(a.output_dir / "lu2026_hypothetical_fly_effectiveness.csv", index=False)
    boom_spectra.to_csv(a.output_dir / "boom2020_spectral_nursery_components.csv", index=False)
    (a.output_dir / "mechanism_bridge_receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "lu_night_lepidoptera_visits_lost": receipt["lu"]["lepidoptera_visits_lost"],
        "lu_night_diptera_visits_gained": receipt["lu"]["diptera_visits_gained"],
        "fly_effectiveness_break_even_is_hypothetical": receipt["lu"]["hypothetical_per_visit_fly_effectiveness_break_even"],
        "boom_green_over_dark_rounded_model_seed_ratio": receipt["boom"]["green_over_dark_rounded_component_product"],
        "boom_net_seed_effect_significant": receipt["boom"]["source_supports_significant_net_seed_reduction"],
        "strict_iwe_effects_created": receipt["new_iwe_h1_effects"],
        "global_alan_chocho_site_year_effect_evaluable": receipt["chocho"]["cross_scale_model_evaluable"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
