"""Source-grain and claim-ceiling tests for real nighttime marginal response."""
from __future__ import annotations
import numpy as np
import pandas as pd
import pytest
from iwe.diel_night_phylogeny import analyse_night_loss


def synthetic():
    # Four originals, three author-tree taxa; fourth remains in the full
    # publication-only panel, not fabricated by grafting a species.
    tree = {
        "tip.label": ["Taxon_A", "Taxon_B", "Taxon_C"],
        "edge": [[4,1], [4,2], [4,3]],
        "edge.length": [1.0, 1.0, 1.0],
    }
    mapping = pd.DataFrame({
        "plant_species": ["Plant A", "Plant B", "Plant C"],
        "phylo": ["Taxon_A", "Taxon_B", "Taxon_C"],
    })
    rows = []
    for metric in ("fruit set", "seed set"):
        for pub, name, effect in (
            ("p1","Plant A",.3), ("p2","Plant B",.1),
            ("p3","Plant C",-.2), ("p4","Unmapped Plant",.2),
        ):
            rows.append({
                "study": pub, "plant": name, "metric": metric,
                "contrast": "night_marginal",
                "units": "fruit/flower" if metric=="fruit set" else "seeds/fruit",
                "effect": effect, "variance_bound": .03,
                "variance_independent": .02,
                "precision_status": "source_precision_available",
            })
    return pd.DataFrame(rows), tree, mapping


def test_authentic_tree_mapping_does_not_impute_unmapped_species():
    models, denominations, shared, receipt = analyse_night_loss(*synthetic())
    assert len(models) == 8
    assert receipt["full_source_mean_cells"] == 8
    assert receipt["precision_cells"] == 8
    assert receipt["tree_mapped_precision_cells"] == 6
    assert receipt["source_mapping"]["unmapped_cells"] == 2
    assert not receipt["ALAN_x_night_marginal_effect_estimable"]
    for metric in ("fruit set","seed set"):
        full = models[(models.metric==metric)&(models.panel=="full_source")]
        common = models[(models.metric==metric)&(models.panel=="tree_common")]
        assert full.iloc[0].k_publications==4
        assert len(common)==3 and common.k_publications.eq(3).all()
        assert set(common.dependence)=={
            "publication_only", "publication_plus_species",
            "publication_species_phylogeny",
        }
        assert (common.ci_low<=common["mean"]).all()
        assert (common["mean"]<=common.ci_high).all()
    assert set(denominations.denominator)=={"fruits_per_flower","seeds_per_fruit"}
    assert not denominations.is_whole_plant_viable_seed_output.any()


def test_wrong_contrast_cannot_be_used_as_night_loss():
    frame,tree,original=synthetic()
    frame.loc[0,"contrast"]="day_marginal"
    with pytest.raises(ValueError,match="Do not combine"):
        analyse_night_loss(frame,tree,original)


def test_missing_original_variance_is_not_infinite_precision():
    frame,tree,original=synthetic()
    frame.loc[0,"variance_bound"]=0.
    with pytest.raises(ValueError,match="Zero or unknown source variance"):
        analyse_night_loss(frame,tree,original)


def test_unrecognized_original_phylogeny_taxon_is_rejected():
    frame,tree,original=synthetic()
    original.loc[0,"phylo"]="Wrong_tip"
    with pytest.raises(ValueError,match="phylogenetic tip"):
        analyse_night_loss(frame,tree,original)


def test_unobserved_light_selfing_and_moth_mechanisms_stay_false():
    _,denominators,_,receipt=analyse_night_loss(*synthetic())
    assert not receipt["original_experiments_are_not_ALAN_manipulations"] is False
    assert receipt["night_marginal_equivalent_to_day_vs_night_dominance"] is False
    assert receipt["nighttime_pollinator_taxon_identity_measured"] is False
    assert receipt["autonomous_selfing_measured_in_source"] is False
    assert receipt["new_strict_iwe_h1_effects"]==0
    assert not denominators["is_whole_plant_viable_seed_output"].any()


def test_denominator_subsets_below_ten_publications_are_not_fitted():
    _,denoms,_,_=analyse_night_loss(*synthetic())
    assert denoms.precision_publications.max()<=4
    assert "conditional_phylogeny_mean" not in denoms.columns
