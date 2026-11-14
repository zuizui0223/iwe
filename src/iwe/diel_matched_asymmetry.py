"""Matched O/D/N reproductive asymmetry and source anthesis association.

Source exploratory reanalysis, not independent replication or an ALAN effect.
The shared open arm is differentiated ONCE before bounding unknown covariance.
Species anthesis class is not measured local floral receptivity or a moth guild.
"""
from __future__ import annotations
import hashlib
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from .diel_reserve_meta import KEY, AUTHOR_BLOB, collapse_studies, reml_meta, _holm

TRAIT_BLOB='18381e550a7e405fe4f198909f0bb381bbecf1e0'
ARMS=('open pollination','day pollination','night pollination')
METRICS=('fruit set','seed set')


def matched_contrast(means, sem):
    """A=night marginal minus day marginal, O/D/N order; range [-2,2]."""
    m=np.asarray(means,float);s=np.asarray(sem,float)
    if m.shape!=(3,) or s.shape!=(3,) or not np.isfinite(m).all() or not np.isfinite(s).all() or (m<0).any() or (s<0).any():
        raise ValueError('O,D,N means and SEM must be finite and nonnegative')
    o,d,n=m
    if o+d==0 or o+n==0:return None
    night=(o-d)/(o+d);day=(o-n)/(o+n)
    g=np.array([2*d/(o+d)**2-2*n/(o+n)**2,-2*o/(o+d)**2,2*o/(o+n)**2])
    return {'effect':float(night-day),'night_marginal':float(night),'day_marginal':float(day),
            'gradient':g.tolist(),'variance_bound':float(np.abs(g*s).sum()**2),
            'variance_independent':float(np.sum((g*s)**2))}


def gitblob(path):
    raw=Path(path).read_bytes()
    return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()


def extract_matched(author:Path, traits:Path, verify=True):
    if verify and (gitblob(author)!=AUTHOR_BLOB or gitblob(traits)!=TRAIT_BLOB):
        raise ValueError('Source author/trait Git blob changed')
    raw=pd.read_csv(author,dtype=str,keep_default_na=False)
    tx=pd.read_csv(traits,dtype=str,keep_default_na=False)
    needed=set(KEY+['treatment_condition','effectiveness_value','effect_error','effect_error_units','sample_size','exclude','plant_native_status','day_pollination_hrs','night_pollination_hrs'])
    if not needed<=set(raw):raise ValueError('Original source fields absent')
    if not {'old_name','plant_family','bloom_period_simple'}<=set(tx):raise ValueError('Original trait columns absent')
    if tx.old_name.duplicated().any():raise ValueError('Source trait names duplicate')
    if not tx.bloom_period_simple.isin(['night','day','both','NA','']).all():raise ValueError('Unknown source bloom class')
    if verify and (len(raw)!=1652 or raw.study_ID.nunique()!=140 or not raw.exclude.eq('n').all()):
        raise ValueError('Original source roster/exclusion flags drift')
    if not raw.exclude.eq('n').all():raise ValueError('Source excluded rows must not enter')
    tx=tx.set_index('old_name')
    r=raw[raw.treatment_effectiveness_metric.isin(METRICS)]
    flow=Counter();out=[]
    for key,group in r.groupby(KEY,sort=True,dropna=False):
        z=group[group.treatment_condition.isin(ARMS)]
        if z.treatment_condition.nunique()!=3:flow['missing_required_arm']+=1;continue
        if len(z)!=3:flow['ambiguous_duplicate_arm']+=1;continue
        z=z.set_index('treatment_condition').loc[list(ARMS)]
        m=pd.to_numeric(z.effectiveness_value,errors='coerce').to_numpy(float)
        if not np.isfinite(m).all() or (m<0).any():flow['invalid_source_mean']+=1;continue
        if m[0]+m[1]==0 or m[0]+m[2]==0:flow['zero_required_denominator']+=1;continue
        sample=pd.to_numeric(z.sample_size,errors='coerce').to_numpy(float)
        err=pd.to_numeric(z.effect_error,errors='coerce').to_numpy(float)
        typ=z.effect_error_units.to_numpy()
        status='source_precision_available'
        if not (np.isfinite(sample)&(sample>=2)&np.isclose(sample,np.round(sample),atol=1e-7,rtol=0)).all():
            status='insufficient_or_noninteger_source_n'
        elif not (np.isfinite(err)&(err>=0)&np.isin(typ,['SE','SD'])).all():status='no_supported_source_SE_or_SD'
        se=np.where(typ=='SD',err/np.sqrt(sample),err) if status=='source_precision_available' else np.zeros(3)
        effect=matched_contrast(m,se);effect.pop('gradient')
        if status!='source_precision_available':effect['variance_bound']=effect['variance_independent']=np.nan
        elif effect['variance_bound']<=0:status='zero_delta_variance'
        info=dict(zip(KEY,key));name=info['plant_species']
        bloom=tx.loc[name,'bloom_period_simple'] if name in tx.index else ''
        family=tx.loc[name,'plant_family'] if name in tx.index else ''
        bloom=bloom if bloom in ('day','night','both') else 'unknown'
        family=family if family not in ('','NA') else None
        dh=pd.to_numeric(pd.Series([z.loc['day pollination','day_pollination_hrs']]),errors='coerce').iloc[0]
        nh=pd.to_numeric(pd.Series([z.loc['night pollination','night_pollination_hrs']]),errors='coerce').iloc[0]
        complete=group[group.treatment_condition.isin(ARMS+('complete exclusion',))]
        cm=pd.to_numeric(complete.effectiveness_value,errors='coerce')
        four=bool(len(complete)==4 and complete.treatment_condition.nunique()==4 and cm.notna().all() and np.isfinite(cm).all() and (cm>=0).all())
        out.append({'cell_id':hashlib.sha256(repr(key).encode()).hexdigest()[:16],
                    'study':info['study_ID'],'plant':name,'metric':info['treatment_effectiveness_metric'],
                    'units':info['effectiveness_units'],'native_only':bool(z.plant_native_status.eq('native').all()),
                    'balanced_reported_hours':bool(np.isfinite(dh) and np.isfinite(nh) and dh>0 and nh>0 and .9<=dh/nh<=1.1),
                    'positive_open_mean':bool(m[0]>0),'complete_fourarm_means':four,
                    'precision_status':status,'bloom':bloom,'family':family,**effect})
        flow[status]+=1
    df=pd.DataFrame(out)
    return df,{'source_doi':'10.1111/ele.70036','author_blob':gitblob(author),'trait_blob':gitblob(traits),
               'source_rows':len(raw),'source_publication_ids':int(raw.study_ID.nunique()),
               'matched_mean_cells':len(df),'matched_mean_publication_ids':int(df.study.nunique()),
               'matched_mean_species':int(df.plant.nunique()),'flow':dict(flow),'key_columns':KEY,
               'trait_complete_case_filter_applied':False,'closed_arm_required':False,
               'same_endpoint_open_day_night_matched':True,
               'breeding_system_column_not_self_compatibility':True,
               'trait_is_species_annotated_anthesis_not_local_availability':True}


def _draw_differences(matrix,nboot,seed):
    rng=np.random.default_rng(seed);idx=rng.integers(0,len(matrix),size=(nboot,len(matrix)))
    values=matrix[idx];counts=np.isfinite(values).sum(axis=1)
    sums=np.nansum(values,axis=1)
    good=(counts>0).all(axis=1)
    means=sums[good]/counts[good]
    return means,int((~good).sum())


def trait_bootstrap(frame,nboot=10000,seed=20261114,unit='publication'):
    """Difference of equal-publication bloom means; joint study resampling.

    An observational comparison of anthesis classes, not an intervention.
    Both/unknown bloom remain in main models but do not become day or night.
    """
    q=frame[frame.bloom.isin(['day','night'])]
    pub=q.groupby(['study','bloom']).effect.mean().unstack('bloom').reindex(columns=['day','night'])
    both=pub.dropna();base={
        'resampling_unit':unit,'n_publications_day':int(pub.day.notna().sum()),
        'n_publications_night':int(pub.night.notna().sum()),
        'within_publication_comparisons':len(both),
        'within_publication_mean':float((both.night-both.day).mean()) if len(both) else None,
        'within_publication_min':float((both.night-both.day).min()) if len(both) else None,
        'within_publication_max':float((both.night-both.day).max()) if len(both) else None,
        'missing_family_cells':int(q.family.isna().sum()),'night_minus_day':None,
        'causal_anthesis_effect':False,'bootstrap_repetitions':nboot}
    if unit=='family':
        p=q.dropna(subset=['family']).groupby(['family','study','bloom']).effect.mean().reset_index()
        matrix=p.groupby(['family','bloom']).effect.mean().unstack('bloom').reindex(columns=['day','night'])
    elif unit=='publication':matrix=pub
    else:raise ValueError('Resampling unit must be publication or family')
    base.update(groups_day=int(matrix.day.notna().sum()),groups_night=int(matrix.night.notna().sum()))
    if matrix.day.notna().sum()<2 or matrix.night.notna().sum()<2:
        return {**base,'status':'missing_day_or_night_group'}
    drawmeans,invalid=_draw_differences(matrix.to_numpy(),nboot,seed)
    draws=drawmeans[:,1]-drawmeans[:,0]
    if len(draws)<.95*nboot:return {**base,'status':'insufficient_valid_bootstrap_draws'}
    lo,hi=np.quantile(draws,[.025,.975]);slo,shi=np.quantile(draws,[.0125,.9875])
    balanced=(drawmeans[:,0]+drawmeans[:,1])/2
    blo,bhi=np.quantile(balanced,[.025,.975])
    base.update(hypothetical_equal_day_night_class_mean=float((matrix.day.mean()+matrix.night.mean())/2),
                hypothetical_balanced_ci_low=float(blo),hypothetical_balanced_ci_high=float(bhi),
                hypothetical_class_balancing_is_not_estimated_population_composition=True,
                status='estimable_observational_association',day_class_mean=float(matrix.day.mean()),
                night_class_mean=float(matrix.night.mean()),night_minus_day=float(matrix.night.mean()-matrix.day.mean()),
                ci_low=float(lo),ci_high=float(hi),ci_low_bonferroni_two=float(slo),ci_high_bonferroni_two=float(shi),
                invalid_resamples=invalid,nominal_interval=.95,simultaneous_two_endpoint_marginal_interval=.975)
    return base


def analyse_matched(frame,nboot=10000):
    precision=frame[frame.precision_status.eq('source_precision_available')]
    models=[];coverage=[];influence=[];traits=[];within=[]
    for metric in METRICS:
        allm=frame[frame.metric==metric];prim=precision[precision.metric==metric]
        for panel,q in [('all_means',allm),('source_precision',prim)]:
            for bloom in ['all','day','night','both','unknown']:
                v=q if bloom=='all' else q[q.bloom==bloom]
                coverage.append({'metric':metric,'panel':panel,'bloom':bloom,'cells':len(v),
                                 'publications':int(v.study.nunique()),'species':int(v.plant.nunique()),
                                 'study_mean_unweighted':float(v.groupby('study').effect.mean().mean()) if len(v) else np.nan})
            for unit in ('publication','family'):
                traits.append({'metric':metric,'panel':panel,**trait_bootstrap(q,nboot=nboot,unit=unit)})
            # Within-publication trait difference with source-precision upper bound.
            rows=[]
            for sid,g in q[q.bloom.isin(['night','day'])].groupby('study'):
                if set(g.bloom)!=set(['night','day']):continue
                nd=g[g.bloom=='night'];dd=g[g.bloom=='day'];delta=float(nd.effect.mean()-dd.effect.mean())
                vb=(np.sqrt(nd.variance_bound).sum()/len(nd)+np.sqrt(dd.variance_bound).sum()/len(dd))**2 if panel=='source_precision' else np.nan
                rows.append({'study':sid,'effect':delta,'variance_bound':vb})
            if panel=='source_precision' and len(rows)>=3:
                st=pd.DataFrame(rows);good=st[st.variance_bound>0]
                fit=reml_meta(good.effect,good.variance_bound) if len(good)>=3 else {}
                within.append({'metric':metric,'panel':panel,'candidate_publications':len(rows),**fit,
                               'status':'within_publication_trait_contrast' if fit else 'insufficient_positive_precision'})
            else:within.append({'metric':metric,'panel':panel,'candidate_publications':len(rows),
                                'mean':float(np.mean([x['effect'] for x in rows])) if rows else None,
                                'status':'descriptive_only_no_variance_or_too_few_publications'})
        for panel in ('primary','native_only','balanced_hours','explicit_unit','fourarm_means','positive_open'):
            q=prim
            if panel=='native_only':q=q[q.native_only]
            if panel=='balanced_hours':q=q[q.balanced_reported_hours]
            if panel=='explicit_unit':q=q[~q.units.isin(['','NA'])]
            if panel=='fourarm_means':q=q[q.complete_fourarm_means]
            if panel=='positive_open':q=q[q.positive_open_mean]
            if q.study.nunique()<3:continue
            st=collapse_studies(q)
            for variance in ('bound','independent'):
                valid=st[st['variance_'+variance]>0]
                if len(valid)<3:continue
                fit=reml_meta(valid.effect,valid['variance_'+variance])
                models.append({'metric':metric,'panel':panel,'covariance':variance,
                               'cells':len(q),'species':int(q.plant.nunique()),**fit})
            if panel=='primary':
                for study in st.study:
                    rest=st[st.study!=study];fit=reml_meta(rest.effect,rest.variance_bound)
                    influence.append({'metric':metric,'omitted_publication_id':study,**fit})
    models=pd.DataFrame(models);main=(models.panel=='primary')&(models.covariance=='bound')
    if main.sum()!=2:raise ValueError('Both predeclared primary endpoints must be estimable')
    models['p_holm_primary_two']=np.nan
    models.loc[main,'p_holm_primary_two']=_holm(models.loc[main,'p_nominal'])
    report={'primary_test_family':['fruit set matched asymmetry','seed set matched asymmetry'],
            'primary_models':models[main].to_dict('records'),'matched_precision_cells':len(precision),
            'matched_precision_publications':int(precision.study.nunique()),'matched_precision_species':int(precision.plant.nunique()),
            'one_publication_effect_per_primary_model':True,
            'shared_open_covariance_handled_via_joint_gradient':True,
            'study_dependence_unresolved_beyond_publication_ID':True,
            'source_SE_delta_bounds_not_guaranteed_final_CI_bounds':True,
            'subgroup_association_is_exploratory_not_new_independent_replication':True,
            'species_phylogeny_not_modelled':True,'ALAN_manipulation_effect_estimated':False,
            'day_and_night_effects_subtracted_after_separate_meta_analyses':False,
            'fractional_seed_loss_or_percentage_conversion_allowed':False,
            'within_publication_trait_checks':within,
            'new_iwe_strict_H1_effects':0,'new_chocho_host_geography_results':False}
    return models,pd.DataFrame(coverage),pd.DataFrame(traits),pd.DataFrame(influence),report
