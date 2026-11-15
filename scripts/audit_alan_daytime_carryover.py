#!/usr/bin/env python3
"""Pin ALAN PR78 Table S3 block means; audit next-day reproduction only.

An author ResearchGate PREPRINT contains 28 choice rounds × 4 ALAN/slug
treatments, with four target-flower seed measurements per treatment.
This code parses only the upstream already-transcribed four-cell
per-round source summary, not the original author 448 flower records.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from iwe.alan_daytime_carryover import (
    ALAN_PINNED_COMMIT, ALAN_SOURCE_GIT_BLOB,
    read_alan_derived_source, summarize_daytime_carryover,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--alan-derived-block-source", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = p.parse_args()
    raw = a.alan_derived_block_source.read_bytes()
    study = read_alan_derived_source(raw, verify=True)
    summaries, receipt = summarize_daytime_carryover(study, verified=True)
    receipt["transcribed_block_file_sha256"] = hashlib.sha256(raw).hexdigest()
    receipt["upstream_alan_derived_ref_id"] = ALAN_SOURCE_GIT_BLOB
    receipt["upstream_git_commit_used"] = ALAN_PINNED_COMMIT
    receipt["source_comparison"] = (
        "Nightly ALAN versus dark crossed with slug treatment; all target "
        "flowers protected prior to 90-minute daytime pollinator choice"
    )
    a.out_dir.mkdir(parents=True,exist_ok=True)
    for item in summaries:
        if item["source_choice_rounds_are_independent_lamp_installations"] or item["valid_new_lighting_study_effect_SE"]:
            raise ValueError("Do not promote 28 repeated daytime rounds to independent lamp samples")
    names = [k for k in summaries[0] if not isinstance(summaries[0][k], (dict,list))]
    with (a.out_dir / "daytime_only_seed_stage_summary.csv").open(
        "w", encoding="utf-8", newline=""
    ) as out:
        writer=csv.DictWriter(out,fieldnames=names)
        writer.writeheader()
        for x in summaries:
            writer.writerow({k:x[k] for k in names})
    with (a.out_dir / "daytime_only_seed_function_receipt.json").open(
        "w",encoding="utf-8"
    ) as out:
        json.dump({"study":receipt, "species":summaries}, out,
                  ensure_ascii=False,indent=2,allow_nan=False)
        out.write("\n")
    print(json.dumps({
        "n_original_daytime_choice_rounds":receipt["original_n_daytime_choice_rounds"],
        "n_original_observed_seed_pots":receipt["original_n_observed_seed_outcomes"],
        "independent_lamp_light_effects_estimated":0,
        "species_summary":[{
            "species":r["species"],"night_exposed_daytime_seed_ratio":r["equal_choice_round_lit_dark_ratio"],
            "no_slug_lit_dark_ratio":r["no_slug_lit_dark_ratio"],
            "slug_lit_dark_ratio":r["slug_lit_dark_ratio"],
            "slug_x_light_additive_diff":r["slug_x_light_additive_difference_of_differences"],
        } for r in summaries]
    },ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
