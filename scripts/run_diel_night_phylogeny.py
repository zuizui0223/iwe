#!/usr/bin/env python3
"""Replay source night marginal without importing ALAN treated observations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from iwe.diel_reserve_meta import extract
from iwe.diel_matched_asymmetry import gitblob, TRAIT_BLOB
from iwe.diel_night_phylogeny import analyse_night_loss

TREE_SHA256 = "34324b8e97b87abdca53a6d578187d0bc239f2cab58974c48b58933398c84a7f"
AUTHOR_FINAL_SHA256 = "3be56ba387a338795037f0fcee3e41ae2d9c5bcf26434f3421565ea10f18b07b"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    args = argparse.ArgumentParser()
    for label in ("author", "traits", "tree", "original-analysis", "out"):
        args.add_argument("--" + label, required=True, type=Path)
    x = args.parse_args()
    if gitblob(x.traits) != TRAIT_BLOB:
        raise ValueError("Original trait Git blob does not match published source")
    if sha(x.tree) != TREE_SHA256 or sha(x.original_analysis) != AUTHOR_FINAL_SHA256:
        raise ValueError("Original RData-derived tree or taxon mapping checksum drift")
    all_cells, extraction = extract(x.author)
    frame = all_cells[all_cells["contrast"].eq("night_marginal")].copy()
    tree = json.loads(x.tree.read_text(encoding="utf-8"))
    final = pd.read_csv(x.original_analysis, dtype=str, keep_default_na=False)
    models, denominators, repeated, receipt = analyse_night_loss(frame, tree, final)
    if (
        len(frame) != 344 or len(final) != 1094
        or receipt["precision_cells"] != 246
        or receipt["tree_mapped_precision_cells"] != 244
        or receipt["original_tree_tips"] != 139
    ):
        raise ValueError("Original selected source coverage no longer matches frozen audit")
    counts = models.loc[models["panel"].eq("tree_common")
                        & models["dependence"].eq("publication_species_phylogeny")
                        ].set_index("metric")["k_publications"].to_dict()
    if counts != {"fruit set": 61, "seed set": 54}:
        raise ValueError("Full original-tree matched publication counts drift")
    seed_fruit = denominators.loc[
        denominators["metric"].eq("seed set")
        & denominators["denominator"].eq("seeds_per_fruit")
    ]
    if len(seed_fruit) != 1 or seed_fruit.iloc[0]["precision_publications"] != 32:
        raise ValueError("Explicit seed-per-fruit denominator source count changed")
    x.out.mkdir(parents=True, exist_ok=True)
    models.to_csv(x.out / "night_marginal_phylogeny_models.csv", index=False)
    denominators.to_csv(x.out / "night_marginal_denominator_coverage.csv", index=False)
    repeated.to_csv(x.out / "night_marginal_shared_species.csv", index=False)
    receipt["original_source"] = extraction
    receipt["inputs_sha256"] = {
        k: sha(getattr(x, k)) for k in ("author", "traits", "tree", "original_analysis")
    }
    (x.out / "night_marginal_phylogeny_receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(models[["metric", "panel", "dependence", "k_publications",
                  "mean", "ci_low", "ci_high"]].to_string(index=False))
    print(denominators.loc[
        denominators["denominator"].eq("seeds_per_fruit"),
        ["metric", "precision_publications", "conditional_phylogeny_mean",
         "conditional_phylogeny_ci_low", "conditional_phylogeny_ci_high"]
    ].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
