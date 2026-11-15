#!/usr/bin/env python3
"""Source-preserving endpoint and original-phylogeny sensitivity of paired A."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from iwe.diel_matched_asymmetry import extract_matched
from iwe.diel_reserve_meta import collapse_studies,reml_meta,_holm
from iwe.diel_endpoint_lineage import (classify_endpoint,tree_correlation,
    map_source_taxa,species_kernels,covariance_reml)


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('author','traits','tree','original-analysis','out'):p.add_argument('--'+name,required=True,type=Path)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for path,expected in [(a.tree,'34324b8e97b87abdca53a6d578187d0bc239f2cab58974c48b58933398c84a7f'),
                          (a.original_analysis,'3be56ba387a338795037f0fcee3e41ae2d9c5bcf26434f3421565ea10f18b07b')]:
        if digest(path)!=expected:raise ValueError('Source-derived tree or final-data conversion changed; re-audit original RData')
    f,source=extract_matched(a.author,a.traits)
    tree=json.loads(a.tree.read_text());labels,r=tree_correlation(tree)
    original=pd.read_csv(a.original_analysis,dtype=str,keep_default_na=False)
    f,mapping=map_source_taxa(f,original,labels)
    f['denominator']=[classify_endpoint(m,u) for m,u in zip(f.metric,f.units)]
    eligible=f[f.precision_status.eq('source_precision_available')].copy()
    models=[];coverage=[];denom=[];membership=[];influence=[]
    for metric in ('fruit set','seed set'):
        q=eligible[eligible.metric.eq(metric)];common=q[q.phylo.notna()]
        for panel,base in [('previous_full_precision',q),('author_tree_common_panel',common)]:
            st=collapse_studies(base)
            if panel=='previous_full_precision':
                result=reml_meta(st.effect,st.variance_bound)
                models.append(dict(metric=metric,panel=panel,model='publication_only',cells=len(base),species=base.plant.nunique(),**result));continue
            pubs,z,ks,kp=species_kernels(base,labels,r)
            assert pubs==st.study.tolist()
            covariances={'publication_only':{'publication':np.eye(len(st))},
                         'publication_plus_species':{'publication':np.eye(len(st)),'species':ks},
                         'publication_species_phylogeny':{'publication':np.eye(len(st)),'species':ks,'phylogeny':kp}}
            for model,kernels in covariances.items():
                fit=covariance_reml(st.effect.to_numpy(),st.variance_bound.to_numpy(),kernels)
                models.append(dict(metric=metric,panel=panel,model=model,cells=len(base),species=base.phylo.nunique(),**fit))
            counts=base.groupby('phylo').study.nunique()
            pairs=int(np.sum(np.triu(ks>0,1)))
            membership.append(dict(metric=metric,publications=len(st),species=int(base.phylo.nunique()),
                              species_in_multiple_publications=int((counts>1).sum()),
                              max_publications_for_one_species=int(counts.max()),
                              publication_pairs_sharing_any_species=pairs,
                              multi_species_publications=int((base.groupby('study').phylo.nunique()>1).sum()),
                              min_species_kernel_eigenvalue=float(np.linalg.eigvalsh(ks).min()),
                              min_phylogeny_kernel_eigenvalue=float(np.linalg.eigvalsh(kp).min())))
        for denominator,g in f[f.metric.eq(metric)].groupby('denominator'):
            precision=g[g.precision_status.eq('source_precision_available')]
            co=dict(metric=metric,denominator=denominator,all_mean_cells=len(g),all_mean_publications=g.study.nunique(),
                    precision_cells=len(precision),precision_publications=precision.study.nunique(),
                    precision_species=precision.plant.nunique(),original_unit_labels=' | '.join(sorted(g.units.unique())))
            coverage.append(co)
            st=collapse_studies(precision)
            if len(st)>=3:
                result=reml_meta(st.effect,st.variance_bound)
                denom.append(dict(metric=metric,denominator=denominator,status='exploratory_nominal_interval',**result))
            else:denom.append(dict(metric=metric,denominator=denominator,status='fewer_than_three_publications',k_publications=len(st)))
        # Leave all publications involving one accepted species out; this is
        # not the preceding leave-one-publication sensitivity.
        fits=[]
        for tip in sorted(common.phylo.unique()):
            st=collapse_studies(common[~common.study.isin(common.loc[common.phylo.eq(tip),'study'])])
            if len(st)>=3:
                fit=reml_meta(st.effect,st.variance_bound);fits.append(fit)
        influence.append(dict(metric=metric,removed_species_groups=len(fits),
            min_mean=min(x['mean'] for x in fits),max_mean=max(x['mean'] for x in fits),
            removals_with_interval_spanning_zero=sum(x['ci_low']<=0<=x['ci_high'] for x in fits),
            max_publications_removed=int(common.groupby('phylo').study.nunique().max())))
    model_frame=pd.DataFrame(models);commonmask=model_frame.panel.eq('author_tree_common_panel')
    if commonmask.sum()!=6:raise ValueError('Expected six declared covariance sensitivities')
    model_frame['p_holm_six_covariance_sensitivities']=np.nan
    model_frame.loc[commonmask,'p_holm_six_covariance_sensitivities']=_holm(model_frame.loc[commonmask,'p_nominal'].to_numpy())
    unitmap=f[['metric','units','denominator']].drop_duplicates().sort_values(['metric','units'])
    for name,table in [('lineage_models',model_frame),('denominator_coverage',pd.DataFrame(coverage)),
                       ('denominator_models',pd.DataFrame(denom)),('species_dependency',pd.DataFrame(membership)),
                       ('leave_species_publications_out',pd.DataFrame(influence)),('literal_source_unit_map',unitmap)]:
        table.to_csv(a.out/(name+'.csv'),index=False)
    report={'schema':'iwe_diel_endpoint_lineage_v1','source_doi':'10.1111/ele.70036',
            'parent_source_extraction':source,'source_taxon_mapping':mapping,
            'full_precision_publications':int(eligible.study.nunique()),'full_precision_cells':len(eligible),
            'phylogeny_common_precision_publications':int(eligible[eligible.phylo.notna()].study.nunique()),
            'phylogeny_common_precision_cells':int(eligible.phylo.notna().sum()),
            'source_tree_tips':len(labels),'author_final_published_analysis_rows':len(original),
            'author_final_publication_ids':int(original.study_ID.nunique()),
            'source_roster_ids_absent_from_author_final':sorted(set(f.study)-set(original.study_ID)),
            'source_files_sha256':{k:digest(getattr(a,k)) for k in ['author','traits','tree','original_analysis']},
            'interval_method':'generalized_modified_KH_t_publication_df_plugin_variance_components',
            'interval_limit':'conditional_sensitivity_not_guaranteed_conservative_not_full_original_multilevel_SMD_reproduction',
            'same_publication_sampling_bounds_unchanged':True,'unmapped_taxa_retained_in_full_reference_models':True,
            'phylogeny_branch_uncertainty_propagated':False,'new_phylogenetic_grafts_or_fuzzy_matches':False,
            'same_species_in_multiple_publications_accounted':True,'cross_publication_raw_sample_overlap_verified':False,
            'denominator_subgroups_are_exploratory_not_primary_discoveries':True,
            'seed_per_fruit_equals_whole_plant_viable_seed_output':False,'new_ALAN_causal_estimate':False,
            'strict_iwe_H1_effects_added':0,'original_paper_overturned':False}
    (a.out/'endpoint_lineage_receipt.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(model_frame[['metric','panel','model','k_publications','mean','ci_low','ci_high','p_nominal']].to_string(index=False))
    print(pd.DataFrame(denom)[['metric','denominator','k_publications','mean','ci_low','ci_high']].to_string(index=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
