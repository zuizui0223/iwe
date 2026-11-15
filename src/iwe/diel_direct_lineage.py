"""Original-tree and repeated-species robustness of direct D/N reproduction E.

Reanalyse author-authenticated Kendall & Nicholson 2025 studies, not new
field experiments or any manipulated nighttime-light exposure. Conditional
REML intervals do not propagate uncertain tree or variance components.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from iwe.diel_reserve_meta import collapse_studies, reml_meta, _holm
from iwe.diel_endpoint_lineage import (
    tree_correlation, map_source_taxa, species_kernels,
    covariance_reml, classify_endpoint,
)


def analyse_direct_lineage(frame: pd.DataFrame, tree: dict,
                           original: pd.DataFrame):
    """Model the SAME direct E source under nested dependence structures.

    Input frame already comes from exact day/night original source matching;
    samples with zero or missing delta variance are never imputed as precise.
    """
    required = {'study', 'plant', 'metric', 'effect', 'variance_bound',
                'variance_independent', 'precision_status', 'units'}
    if not required <= set(frame):
        raise ValueError('Missing direct E source and precision columns')
    if not set(frame.metric) <= {'fruit set', 'seed set'}:
        raise ValueError('Only distinct source fruit set and seed set metrics')
    labels, r = tree_correlation(tree)
    source, mapping = map_source_taxa(frame, original, labels)
    source['denominator'] = [classify_endpoint(metric,unit)
                             for metric,unit in zip(source.metric,source.units)]
    eligible = source[source.precision_status.eq('source_precision_available')].copy()
    if eligible.empty:
        raise ValueError('No original-source positive-error comparisons')
    values = eligible[['effect','variance_bound','variance_independent']].to_numpy(float)
    if (not np.isfinite(values).all() or (eligible[['variance_bound','variance_independent']] <= 0).any().any()):
        raise ValueError('All admitted source precision variances must be positive source variance')
    models=[];coverage=[];repeat=[]
    for metric in ('fruit set','seed set'):
        q=eligible[eligible.metric.eq(metric)]
        common=q[q.phylo.notna()].copy()
        if q.study.nunique()<3 or common.study.nunique()<3:
            raise ValueError(f'Insufficient independent publication identifiers: {metric}')
        full=collapse_studies(q)
        models.append({'metric':metric,'panel':'full_source','model':'publication_only',
                       'cells':len(q),'tree_tip_species':None,
                       **reml_meta(full.effect,full.variance_bound)})
        st=collapse_studies(common)
        pubs,z,species_kernel,phylo_kernel=species_kernels(common,labels,r)
        if pubs!=st.study.tolist():
            raise ValueError('Publication membership order differs between kernels and source averages')
        kernels=[
            ('publication_only',{'publication':np.eye(len(st))}),
            ('publication_plus_species',{
                'publication':np.eye(len(st)),'species':species_kernel,
            }),
            ('publication_species_phylogeny',{
                'publication':np.eye(len(st)),'species':species_kernel,
                'phylogeny':phylo_kernel,
            }),
        ]
        for model,mats in kernels:
            result=covariance_reml(st.effect.to_numpy(),st.variance_bound.to_numpy(),mats)
            models.append({'metric':metric,'panel':'tree_common','model':model,
                           'cells':len(common),'tree_tip_species':common.phylo.nunique(),
                           **result})
        counts=common.groupby('phylo').study.nunique()
        repeat.append({'metric':metric,'cells':len(common),'publications':len(st),
                       'tree_tip_species':common.phylo.nunique(),
                       'species_in_multiple_publications':int((counts>1).sum()),
                       'publication_pairs_sharing_species':int(np.triu(species_kernel>0,1).sum())})
        for denom,g in source[source.metric.eq(metric)].groupby('denominator'):
            correct=g[g.precision_status.eq('source_precision_available')]
            coverage.append({'metric':metric,'denominator':denom,
                             'all_mean_cells':len(g),'precision_cells':len(correct),
                             'precision_publications':correct.study.nunique(),
                             'mapped_precision_cells':int(correct.phylo.notna().sum())})
    model_frame=pd.DataFrame(models)
    focus=(model_frame.panel.eq('tree_common')&
           model_frame.model.eq('publication_species_phylogeny'))
    if len(model_frame)!=8 or focus.sum()!=2:
        raise ValueError('Two outcomes × one full-source plus three tree-common models expected')
    model_frame['holm_two_exploratory_full_phylogeny']=np.nan
    model_frame.loc[focus,'holm_two_exploratory_full_phylogeny']=_holm(
        model_frame.loc[focus,'p_nominal'].to_numpy(float))
    report={
        'schema':'iwe_diel_direct_original_phylogeny_v0.1',
        'source_doi':'10.1111/ele.70036',
        'source_mapping':mapping,
        'original_tree_tips':len(labels),
        'original_study_source_rows_in_final_author_analysis':len(original),
        'full_precision_cells':len(eligible),
        'full_precision_publication_ids':int(eligible.study.nunique()),
        'tree_mapped_precision_cells':int(eligible.phylo.notna().sum()),
        'tree_mapped_precision_publication_ids':int(
            eligible.loc[eligible.phylo.notna(),'study'].nunique()),
        'repeated_species_dependency':repeat,
        'two_primary_tree_models_are_post_hoc_exploratory':True,
        'unknown_within_study_covariance_first_order_bounded':True,
        'unmapped_names_are_invented_grafts':False,
        'individual_source_rows_are_independent_studies':False,
        'manipulated_ALAN_exposure_observed':False,
        'autonomous_selfing_observed':False,
        'comparisons_independent_of_original_diel_literature':False,
        'new_iwe_strict_H1_effects':0,
        'same_as_original_author_SMD_model':False,
        'conditional_CI_guarantees_population_coverage':False,
        'phylogenetic_causation_identified':False,
    }
    return model_frame,pd.DataFrame(coverage),report
