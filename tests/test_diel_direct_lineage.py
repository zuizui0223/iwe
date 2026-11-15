import numpy as np
import pandas as pd
import pytest

from iwe.diel_direct_lineage import analyse_direct_lineage


def toy():
    tree = {
        'tip.label': ['Taxon_A', 'Taxon_B', 'Taxon_C'],
        'edge': [[4, 1], [4, 2], [4, 3]],
        'edge.length': [1., 1., 1.],
    }
    original = pd.DataFrame({
        'plant_species': ['Plant A', 'Plant B', 'Plant C'],
        'phylo': ['Taxon_A', 'Taxon_B', 'Taxon_C'],
    })
    frame = pd.DataFrame([
        {'study': sid, 'plant': plant, 'metric': metric,
         'units': ('fruit/flower' if metric == 'fruit set' else 'seeds/fruit'),
         'effect': effect, 'variance_bound': .025, 'variance_independent': .015,
         'precision_status': 'source_precision_available'}
        for metric in ('fruit set', 'seed set')
        for sid, plant, effect in [
            ('paper1', 'Plant A', .3), ('paper2', 'Plant B', -.1),
            ('paper3', 'Plant C', .2), ('paper4', 'Missing plant', .5),
        ]
    ])
    return frame, tree, original


def test_exact_author_phylo_mapping_keeps_unmapped_in_full_reference():
    frame, tree, original = toy()
    models, units, receipt = analyse_direct_lineage(frame, tree, original)
    assert len(models) == 8
    assert set(models['metric']) == {'fruit set', 'seed set'}
    assert receipt['source_mapping']['unmapped_cells'] == 2
    assert receipt['full_precision_publication_ids'] == 4
    assert receipt['tree_mapped_precision_publication_ids'] == 3
    assert receipt['unmapped_names_are_invented_grafts'] is False
    for metric in ('fruit set', 'seed set'):
        q = models[(models['metric'] == metric) & (models['panel'] == 'tree_common')]
        assert q['k_publications'].eq(3).all()
        assert set(q['model']) == {
            'publication_only', 'publication_plus_species', 'publication_species_phylogeny'
        }
        assert (q['ci_low'] <= q['mean']).all()
        assert (q['mean'] <= q['ci_high']).all()
        assert set(units.loc[units.metric == metric, 'denominator']) == {
            ('fruits_per_flower' if metric == 'fruit set' else 'seeds_per_fruit')
        }


def test_no_light_causation_or_strict_h1_effects_promoted():
    model, units, report = analyse_direct_lineage(*toy())
    assert not report['manipulated_ALAN_exposure_observed']
    assert not report['autonomous_selfing_observed']
    assert not report['comparisons_independent_of_original_diel_literature']
    assert report['new_iwe_strict_H1_effects'] == 0
    assert not report['same_as_original_author_SMD_model']
    assert not report['conditional_CI_guarantees_population_coverage']
    assert len(model[model['model'] == 'publication_species_phylogeny']) == 2


def test_no_false_accepted_tree_name_or_fuzzy_grafting():
    frame, tree, original = toy()
    original.loc[0, 'phylo'] = 'Fake_tip'
    with pytest.raises(ValueError, match='Source phylogenetic tip'):
        analyse_direct_lineage(frame, tree, original)


def test_nonpositive_or_missing_source_variance_fails_closed():
    frame, tree, original = toy()
    frame.loc[0, 'variance_bound'] = 0
    with pytest.raises(ValueError, match='positive source variance'):
        analyse_direct_lineage(frame, tree, original)


def test_duplicate_study_plant_cell_does_not_create_new_publication():
    frame, tree, original = toy()
    frame2 = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    models, units, report = analyse_direct_lineage(frame2, tree, original)
    assert report['full_precision_publication_ids'] == 4
    assert not report['individual_source_rows_are_independent_studies']
    assert models.loc[(models.metric=='fruit set')&(models.panel=='full_source'),'k_publications'].iloc[0] == 4
