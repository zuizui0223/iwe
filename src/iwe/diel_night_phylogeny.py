"""Source-audited nighttime marginal access; NOT a manipulated ALAN effect.

A nighttime-exclusive outcome is not needed: this estimates the change in
reproduction with night access available in addition to daytime access.
Underlying studies are Kendall & Nicholson (2025), not new field evidence.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .diel_reserve_meta import collapse_studies, reml_meta, _holm
from .diel_endpoint_lineage import (
    tree_correlation, map_source_taxa, species_kernels,
    covariance_reml, classify_endpoint,
)

METRICS = ("fruit set", "seed set")
CONTRAST = "night_marginal"


def analyse_night_loss(
    frame: pd.DataFrame, tree: dict, final_author: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Eight original-source models and literal reproductive denominator coverage.

    Open and day-only reproductive values must already be source matched.
    Each source publication contributes one mean; source standard errors
    and within-publication correlation have only first-order upper bounds.
    """
    required = {
        "study", "plant", "metric", "units", "effect",
        "variance_bound", "variance_independent", "precision_status", "contrast",
    }
    if not required <= set(frame):
        raise ValueError("Missing night-marginal source fields")
    if frame.empty or not frame["contrast"].eq(CONTRAST).all():
        raise ValueError("Do not combine night marginal and day/night dominance")
    if not set(frame["metric"]).issubset(METRICS):
        raise ValueError("Mixed or unrecognized plant reproductive response type")
    labels, phylo = tree_correlation(tree)
    source, mapping = map_source_taxa(frame, final_author, labels)
    source["denominator"] = [
        classify_endpoint(m, u) for m, u in zip(source["metric"], source["units"])
    ]
    eligible = source[source["precision_status"].eq("source_precision_available")].copy()
    if eligible.empty:
        raise ValueError("Missing original observation standard errors")
    values = eligible[["effect", "variance_bound", "variance_independent"]].to_numpy(float)
    if not np.isfinite(values).all() or (
        eligible[["variance_bound", "variance_independent"]] <= 0
    ).any().any():
        raise ValueError("Zero or unknown source variance cannot receive infinite weight")

    model_rows, denominator_rows, repeated_species = [], [], []
    for metric in METRICS:
        q = eligible[eligible["metric"].eq(metric)]
        mapped = q[q["phylo"].notna()].copy()
        for panel, part in (("full_source", q), ("tree_common", mapped)):
            pub = collapse_studies(part)
            if len(pub) < 3:
                raise ValueError("Insufficient publications: " + metric + " " + panel)
            if panel == "full_source":
                model_rows.append({
                    "metric": metric, "panel": panel, "dependence": "publication_only",
                    "cells": len(part), "species": part["plant"].nunique(),
                    **reml_meta(pub["effect"], pub["variance_bound"]),
                })
                continue
            pubs, z, species_kernel, phylo_kernel = species_kernels(part, labels, phylo)
            if pubs != pub["study"].tolist():
                raise ValueError("Publication membership differs from original tree kernel")
            for model, kernels in (
                ("publication_only", {"publication": np.eye(len(pub))}),
                ("publication_plus_species", {
                    "publication": np.eye(len(pub)), "species": species_kernel,
                }),
                ("publication_species_phylogeny", {
                    "publication": np.eye(len(pub)),
                    "species": species_kernel, "phylogeny": phylo_kernel,
                }),
            ):
                fit = covariance_reml(
                    pub["effect"].to_numpy(), pub["variance_bound"].to_numpy(), kernels,
                )
                model_rows.append({
                    "metric": metric, "panel": panel, "dependence": model,
                    "cells": len(part), "species": part["phylo"].nunique(), **fit,
                })
            counts = part.groupby("phylo")["study"].nunique()
            repeated_species.append({
                "metric": metric,
                "source_publications": len(pub),
                "source_species": int(part["phylo"].nunique()),
                "species_in_more_than_one_paper": int((counts > 1).sum()),
                "publication_pairs_sharing_a_species": int(np.triu(species_kernel > 0, 1).sum()),
            })
        for unit, group in source[source["metric"].eq(metric)].groupby("denominator"):
            precision = group[group["precision_status"].eq("source_precision_available")]
            count = int(precision["study"].nunique())
            row = {
                "metric": metric, "denominator": unit,
                "source_cells": len(group), "source_publications": int(group["study"].nunique()),
                "precision_cells": len(precision), "precision_publications": count,
                "tree_mapped_precision_cells": int(precision["phylo"].notna().sum()),
                "reproduction_scope": (
                    "conditional_on_fruit_formed" if unit == "seeds_per_fruit"
                    else "source_literal_denominator"
                ),
                "is_whole_plant_viable_seed_output": False,
            }
            # Underpowered strata are listed but are NOT described as having
            # a resolved treatment effect.
            if count >= 10:
                study = collapse_studies(precision)
                fit = reml_meta(study["effect"], study["variance_bound"])
                row.update({
                    "publication_mean": fit["mean"],
                    "publication_ci_low": fit["ci_low"],
                    "publication_ci_high": fit["ci_high"],
                })
                if precision["phylo"].notna().all():
                    pubs, z, sk, pk = species_kernels(precision, labels, phylo)
                    if pubs != study["study"].tolist():
                        raise ValueError("Denominator-specific publication kernel mismatch")
                    full = covariance_reml(
                        study["effect"].to_numpy(), study["variance_bound"].to_numpy(),
                        {"publication": np.eye(len(study)), "species": sk, "phylogeny": pk},
                    )
                    row.update({
                        "conditional_phylogeny_mean": full["mean"],
                        "conditional_phylogeny_ci_low": full["ci_low"],
                        "conditional_phylogeny_ci_high": full["ci_high"],
                    })
            denominator_rows.append(row)

    models = pd.DataFrame(model_rows)
    primary = models[
        models["panel"].eq("tree_common")
        & models["dependence"].eq("publication_species_phylogeny")
    ]
    if len(models) != 8 or len(primary) != 2:
        raise ValueError("Two endpoints × four source/dependence panels required")
    models["holm_two_posthoc_phylogenetic_tests"] = np.nan
    models.loc[primary.index, "holm_two_posthoc_phylogenetic_tests"] = _holm(
        primary["p_nominal"].to_numpy(float)
    )
    receipt = {
        "schema": "iwe_original_night_marginal_phylogeny_v01",
        "original_source_doi": "10.1111/ele.70036",
        "original_experiments_are_not_ALAN_manipulations": True,
        "source_definition": "(open_pollination-day_only)/(open_pollination+day_only)",
        "is_percentage_reproductive_loss": False,
        "nighttime_pollinator_taxon_identity_measured": False,
        "autonomous_selfing_measured_in_source": False,
        "night_marginal_equivalent_to_day_vs_night_dominance": False,
        "full_source_mean_cells": len(source),
        "full_source_publication_ids": int(source["study"].nunique()),
        "precision_cells": len(eligible),
        "precision_publication_ids": int(eligible["study"].nunique()),
        "tree_mapped_precision_cells": int(eligible["phylo"].notna().sum()),
        "tree_mapped_precision_publications": int(
            eligible.loc[eligible["phylo"].notna(), "study"].nunique()
        ),
        "original_tree_tips": len(labels),
        "source_mapping": mapping,
        "same_original_publications_as_prior_IWE_diel_analysis": True,
        "seed_per_fruit_is_total_whole_plant_fitness": False,
        "conditional_interval_propagates_tree_and_variance_component_uncertainty": False,
        "ALAN_x_night_marginal_effect_estimable": False,
        "independent_confirmation_of_original_biological_claim": False,
        "new_strict_iwe_h1_effects": 0,
    }
    return models, pd.DataFrame(denominator_rows), pd.DataFrame(repeated_species), receipt
