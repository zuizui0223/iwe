#!/usr/bin/env python3
"""Review original ALAN-study outcome support; optionally replay Li author raw data.

Outputs are original study *aggregates* only; no 79-row original file is
redistributed. Does not add strict IWE synchrony SMDs or causal meta claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from iwe.alan_li_source import audit_li_original, fetch_original_author_bytes
from iwe.alan_reproductive_gate import build_crossstudy_readiness

PROG = Path("data/registry/alan_reproduction_programmes_v01.csv")
CLAIMS = Path("data/registry/alan_reproduction_claims_v01.csv")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--programmes", type=Path, default=PROG)
    parser.add_argument("--claims", type=Path, default=CLAIMS)
    parser.add_argument("--out-dir", type=Path, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--download-li-author-original",
        action="store_true",
        help="Fetch only the published author's 79-row seed source with SHA guard; save aggregates only",
    )
    source.add_argument(
        "--li-original-file", type=Path,
        help="Original author's local seedset.csv; must pass the same Git blob SHA guard",
    )
    args = parser.parse_args()

    p = pd.read_csv(args.programmes, dtype=str, keep_default_na=False)
    c = pd.read_csv(args.claims, dtype=str, keep_default_na=False)
    valid_programmes, validated_claims, ledger = build_crossstudy_readiness(p, c)
    original_bytes = (
        fetch_original_author_bytes()
        if args.download_li_author_original else args.li_original_file.read_bytes()
    )
    arm, field, plant, li = audit_li_original(
        original_bytes, original_source_verified=True
    )
    if not li["source_verified_original_git_blob"] or li["original_field_blocks"] != 3:
        raise ValueError("Li original seedset source/provenance not verified")
    frozen_path = Path("data/frozen/alan_li2026_original_aggregate_v01.json")
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if (li["original_source_git_blob_sha1"] != frozen["source_git_blob_sha1"]
            or li["original_source_sha256"] != frozen["source_sha256"]
            or li["observed_total_seed_count"] != frozen["source_observed_seeds_total"]
            or li["observed_total_fruits_count"] != frozen["source_observed_fruits_total"]
            or li["source_original_rows"] != frozen["original_author_plant_records"]
            or li["seed_outcome_known_plant_rows"] != frozen["records_with_known_seeds"]):
        raise ValueError("Frozen source snapshot and original author Li data do not reconcile")
    by_arm = {x["treatment"]: x for x in arm}
    for item in frozen["treatments"]:
        original = by_arm[item["treatment"]]
        if (original["seed_outcome_known_plant_rows"] != item["nonmissing"]
                or original["seed_present_plant_rows"] != item["seed_present"]
                or original["actual_seed_count_from_known_plants"] != item["seeds"]
                or original["actual_fruit_count_from_known_plants"] != item["fruits"]):
            raise ValueError("Frozen Li arm snapshot differs from authentic replay")
    ledger["frozen_author_aggregate_snapshot_sha256"] = _sha(frozen_path)
    li["not_an_independent_replication_of_network_or_spectrum_experiments"] = True
    li["observed_moth_pollinator_or_substitution_evidence_in_this_dataset"] = False
    ledger["li_2026_source_verified"] = {
        "author_source_git_blob_sha1": li["original_source_git_blob_sha1"],
        "three_field_reproduction": True,
        "original_seed_formation_fields": 3,
        "linear_array_over_dark_seed_presence_risk_difference":
            li["linear_array_minus_control_pooled_plant_risk_difference"],
        "point_over_dark_seed_presence_risk_difference":
            li["point_minus_control_pooled_plant_risk_difference"],
        "independent_pollinator_visitation_measured": False,
        "separate_light_geometry_from_total_lamp_count": False,
    }
    ledger["source_input_sha256"] = {
        "programme_ledger": _sha(args.programmes),
        "published_claim_ledger": _sha(args.claims),
        "author_original_li_csv": li["original_source_sha256"],
    }
    ledger["original_author_Li_records_redistributed"] = False
    ledger["observational_PCNLand_manipulated_ground_lux_are_not_exchangeable"] = True
    ledger["different_response_types_can_be_pooled_into_one_effect"] = False

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    valid_programmes.to_csv(out / "source_programme_endpoint_eligibility.csv", index=False)
    validated_claims.to_csv(out / "reported_original_source_endpoint_values.csv", index=False)
    pd.DataFrame(arm).to_csv(out / "li_original_seed_arm_summary.csv", index=False)
    pd.DataFrame(field).to_csv(out / "li_three_hayfield_reproductive_contrasts.csv", index=False)
    pd.DataFrame(plant).to_csv(out / "li_species_treatment_seed_aggregates.csv", index=False)
    (out / "reproductive_source_grain_receipt.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (out / "li_original_author_source_receipt.json").write_text(
        json.dumps(li, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "study_rows_including_secondary_meta": ledger[
            "n_source_rows_including_secondary_literature_synthesis"
        ],
        "original_light_experiment_paper_rows": ledger[
            "n_original_ALAN_manipulation_paper_rows"
        ],
        "co_reported_visit_pollen_seed_original_studies": ledger[
            "n_original_papers_with_reported_visit_pollen_reproduction"
        ],
        "complete_light_time_pollen_viable_seed_chains": ledger[
            "n_complete_independent_seasonal_or_diel_phenophase_fitness_chains"
        ],
        "actual_author_Li_seed_source_verified": li["source_verified_original_git_blob"],
        "Li_three_field_risk_difference_mean": li[
            "linear_array_minus_control_equal_field_mean_risk_difference"
        ],
        "strict_H1_new_effects": ledger["new_strict_iwe_h1_effects"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
