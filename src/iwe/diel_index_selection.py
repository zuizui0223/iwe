"""Audit open-reference rescaling and minimal two-arm source eligibility.

Reanalysis of Kendall & Nicholson 2025, not independent experiments or ALAN.
A=wE has the same sign for positive O, but magnitudes/precision weights differ.
Unknown correlations are bounded only by first-order delta variances.
"""
from __future__ import annotations
import hashlib
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import binomtest
from .diel_reserve_meta import KEY, AUTHOR_BLOB, collapse_studies, reml_meta, _holm
from .diel_matched_asymmetry import TRAIT_BLOB, gitblob, matched_contrast

METRICS=('fruit set','seed set')
DN=('day pollination','night pollination')


def direct_contrast(means, sem):
    """E=(N-D)/(N+D); D,N order, no continuity constant, undefined if both zero."""
    m=np.asarray(means,float);s=np.asarray(sem,float)
    if m.shape!=(2,) or s.shape!=(2,) or not np.isfinite(m).all() or not np.isfinite(s).all() or (m<0).any() or (s<0).any():
        raise ValueError('D,N means and SEM must be finite and nonnegative')
    d,n=m;total=d+n
    if total==0:return None
    g=np.array([-2*n,2*d])/total**2
    return {'effect':float((n-d)/total),'gradient':g.tolist(),
            'variance_bound':float(np.abs(g*s).sum()**2),
            'variance_independent':float(np.sum((g*s)**2))}


def open_multiplier(o,d,n):
    if not np.isfinite([o,d,n]).all() or min(o,d,n)<0:raise ValueError('Invalid means')
    if o+d==0 or o+n==0 or d+n==0:return None
    return float(2*o*(n+d)/((o+d)*(o+n)))


def _precision(rows):
    ns=pd.to_numeric(rows.sample_size,errors='coerce').to_numpy(float)
    error=pd.to_numeric(rows.effect_error,errors='coerce').to_numpy(float)
    label=rows.effect_error_units.to_numpy()
    if not (np.isfinite(ns)&(ns>=2)&np.isclose(ns,np.round(ns),atol=1e-7,rtol=0)).all():
        return 'insufficient_or_noninteger_source_n',None
    if not (np.isfinite(error)&(error>=0)&np.isin(label,['SE','SD'])).all():
        return 'no_supported_source_SE_or_SD',None
    return 'source_precision_available',np.where(label=='SD',error/np.sqrt(ns),error)


def extract_direct(author:Path,traits:Path,verify=True):
    if verify and (gitblob(author)!=AUTHOR_BLOB or gitblob(traits)!=TRAIT_BLOB):
        raise ValueError('Original source blob mismatch')
    raw=pd.read_csv(author,dtype=str,keep_default_na=False)
    tx=pd.read_csv(traits,dtype=str,keep_default_na=False)
    required=set(KEY+['treatment_condition','effectiveness_value','effect_error','effect_error_units','sample_size','exclude','plant_native_status','day_pollination_hrs','night_pollination_hrs'])
    if not required<=set(raw):raise ValueError('Missing original source fields')
    if not {'old_name','plant_family','bloom_period_simple'}<=set(tx) or tx.old_name.duplicated().any():
        raise ValueError('Original trait mapping absent or ambiguous')
    if not tx.bloom_period_simple.isin(['day','night','both','NA','']).all():raise ValueError('Unknown anthesis label')
    if not raw.exclude.eq('n').all():raise ValueError('Source excluded rows cannot enter')
    if verify and (len(raw)!=1652 or raw.study_ID.nunique()!=140):raise ValueError('Source roster drift')
    tx=tx.set_index('old_name');out=[];flow=Counter()
    for key,g in raw[raw.treatment_effectiveness_metric.isin(METRICS)].groupby(KEY,sort=True,dropna=False):
        z=g[g.treatment_condition.isin(DN)]
        if z.treatment_condition.nunique()!=2:flow['missing_DN_arm']+=1;continue
        if len(z)!=2:flow['duplicate_DN_arm']+=1;continue
        z=z.set_index('treatment_condition').loc[list(DN)]
        means=pd.to_numeric(z.effectiveness_value,errors='coerce').to_numpy(float)
        if not np.isfinite(means).all() or (means<0).any():flow['invalid_DN_mean']+=1;continue
        if means.sum()==0:flow['both_DN_zero']+=1;continue
        status,se=_precision(z)
        result=direct_contrast(means,se if se is not None else [0,0]);result.pop('gradient')
        if se is None:result['variance_bound']=result['variance_independent']=np.nan
        elif result['variance_bound']==0:status='zero_delta_variance'
        op=g[g.treatment_condition=='open pollination']
        oval=pd.to_numeric(op.effectiveness_value,errors='coerce').to_numpy(float)
        open_ok=bool(len(op)==1 and np.isfinite(oval).all() and oval[0]>=0 and (oval[0]+means>0).all())
        old=None;weight=np.nan;old_status='missing_or_invalid_open_mean'
        if open_ok:
            weight=open_multiplier(oval[0],*means)
            three=pd.concat([op.set_index('treatment_condition'),z])
            old_status,old_se=_precision(three)
            old=matched_contrast([oval[0],*means],old_se if old_se is not None else [0,0,0])
            if old_se is None:old['variance_bound']=old['variance_independent']=np.nan
            elif old['variance_bound']==0:old_status='zero_delta_variance'
            if not np.isclose(old['effect'],weight*result['effect'],atol=1e-12,rtol=1e-10):raise ValueError('A=wE identity failed')
        info=dict(zip(KEY,key));name=info['plant_species']
        bloom=tx.loc[name,'bloom_period_simple'] if name in tx.index else 'unknown'
        bloom=bloom if bloom in ('day','night','both') else 'unknown'
        family=tx.loc[name,'plant_family'] if name in tx.index else ''
        family=family if family not in ('','NA') else None
        dh=pd.to_numeric(pd.Series([z.loc[DN[0],'day_pollination_hrs']]),errors='coerce').iloc[0]
        nh=pd.to_numeric(pd.Series([z.loc[DN[1],'night_pollination_hrs']]),errors='coerce').iloc[0]
        out.append({'cell_id':hashlib.sha256(repr(key).encode()).hexdigest()[:16],
            'study':info['study_ID'],'plant':name,'metric':info['treatment_effectiveness_metric'],
            'units':info['effectiveness_units'],'bloom':bloom,'family':family,
            'native_only':bool(z.plant_native_status.eq('native').all()),
            'balanced_reported_hours':bool(np.isfinite(dh) and np.isfinite(nh) and dh>0 and nh>0 and .9<=dh/nh<=1.1),
            'open_mean_eligible':open_ok,'prior_joint_precision':old_status=='source_precision_available',
            'old_precision_status':old_status,'open_multiplier':weight,
            'old_effect':old['effect'] if old else np.nan,
            'old_variance_bound':old['variance_bound'] if old else np.nan,
            'old_variance_independent':old['variance_independent'] if old else np.nan,
            'boundary_DN_zero':bool((means==0).any()),'precision_status':status,**result})
        flow[status]+=1
    f=pd.DataFrame(out)
    return f,{'author_blob':gitblob(author),'trait_blob':gitblob(traits),'original_rows':len(raw),
              'source_doi':'10.1111/ele.70036','flow':dict(flow),'key_columns':KEY,
              'open_arm_required':False,'trait_complete_case_required':False,
              'no_local_light_or_seasonal_phenology_effect':True}


def publication_bootstrap(q,nboot=10000,seed=20261115):
    values=q.groupby('study',sort=True).effect.mean().to_numpy(float)
    if len(values)<3:return {'status':'too_few_publications'}
    rng=np.random.default_rng(seed)
    draw=values[rng.integers(0,len(values),(nboot,len(values)))].mean(axis=1)
    pos=int((values>1e-12).sum());neg=int((values< -1e-12).sum());ties=len(values)-pos-neg
    return {'status':'computed','publication_count':len(values),'unweighted_mean':float(values.mean()),
            'ci_low':float(np.quantile(draw,.025)),'ci_high':float(np.quantile(draw,.975)),
            'positive':pos,'negative':neg,'ties':ties,
            'sign_p_two_sided':float(binomtest(pos,pos+neg).pvalue) if pos+neg else None}


def selection_bootstrap(frame,nboot=10000,seed=20261115):
    """Gained versus common source effects; resample whole publications jointly."""
    q=frame.assign(cohort=np.where(frame.prior_joint_precision,'common','gained'))
    matrix=q.groupby(['study','cohort']).effect.mean().unstack('cohort').reindex(columns=['common','gained'])
    out={'status':'computed','common_publications':int(matrix.common.notna().sum()),
         'gained_publications':int(matrix.gained.notna().sum()),'shared_publications':int(matrix.notna().all(axis=1).sum()),
         'randomized_selection_effect':False}
    if min(out['common_publications'],out['gained_publications'])<3:
        return {**out,'status':'too_few_publications_per_cohort'}
    rng=np.random.default_rng(seed);values=matrix.to_numpy()
    draw=values[rng.integers(0,len(values),(nboot,len(values)))]
    ns=np.isfinite(draw).sum(axis=1);valid=(ns>0).all(axis=1)
    means=np.nansum(draw[valid],axis=1)/ns[valid]
    diff=means[:,1]-means[:,0]
    out.update(gained_minus_common=float(matrix.gained.mean()-matrix.common.mean()),
               ci_low=float(np.quantile(diff,.025)),ci_high=float(np.quantile(diff,.975)),
               valid_resamples=int(valid.sum()),bootstrap_repetitions=nboot)
    return out


def analyse_selection(frame,nboot=10000):
    eligible=frame[frame.precision_status=='source_precision_available']
    models=[];coverage=[];boot=[];influence=[];study_rows=[]
    for metric in METRICS:
        full=frame[frame.metric==metric];q=eligible[eligible.metric==metric]
        panels={'all_DN':q,'open_mean_available':q[q.open_mean_eligible],
                'same_precision_as_A':q[q.prior_joint_precision],
                'gained_over_A':q[~q.prior_joint_precision],
                'native_only':q[q.native_only],'balanced_hours':q[q.balanced_reported_hours],
                'explicit_unit':q[~q.units.isin(['','NA'])]}
        for name in ('day','night','both','unknown'):panels['bloom_'+name]=q[q.bloom==name]
        for panel,v in [('all_DN_means',full),*panels.items()]:
            coverage.append({'metric':metric,'panel':panel,'cells':len(v),'publication_ids':v.study.nunique(),
                             'taxa':v.plant.nunique(),'boundary_mean_cells':int(v.boundary_DN_zero.sum())})
            boot.append({'metric':metric,'panel':panel,**publication_bootstrap(v,nboot=nboot)})
            if panel=='all_DN_means' or v.study.nunique()<3:continue
            contrasts=['E','A'] if panel=='same_precision_as_A' else ['E']
            for index in contrasts:
                x=v.copy()
                if index=='A':
                    x[['effect','variance_bound','variance_independent']]=x[['old_effect','old_variance_bound','old_variance_independent']].to_numpy()
                studies=collapse_studies(x)
                for covariance in ('bound','independent'):
                    fit=reml_meta(studies.effect,studies['variance_'+covariance])
                    models.append({'metric':metric,'panel':panel,'index':index,'covariance':covariance,'cells':len(v),**fit})
                if panel=='all_DN' and index=='E':
                    study_rows.extend(studies.assign(metric=metric).to_dict('records'))
                    for sid in studies.study:
                        rest=studies[studies.study!=sid]
                        influence.append({'metric':metric,'omitted_study':sid,**reml_meta(rest.effect,rest.variance_bound)})
    models=pd.DataFrame(models);main=(models.panel=='all_DN')&(models['index']=='E')&(models.covariance=='bound')
    if main.sum()!=2:raise ValueError('Both prespecified primary endpoints required')
    models['p_holm_primary_two']=np.nan;models.loc[main,'p_holm_primary_two']=_holm(models.loc[main,'p_nominal'])
    paired=frame[frame.open_mean_eligible]
    report={'primary_models':models[main].to_dict('records'),'mean_cells':len(frame),
            'mean_publication_ids':int(frame.study.nunique()),'mean_taxa':int(frame.plant.nunique()),
            'precision_cells':len(eligible),'precision_publication_ids':int(eligible.study.nunique()),
            'precision_taxa':int(eligible.plant.nunique()),'A_equals_open_multiplier_times_E_max_abs_error':
                float(np.max(np.abs(paired.old_effect-paired.open_multiplier*paired.effect))),
            'multiplier_quantiles':paired.open_multiplier.quantile([0,.25,.5,.75,1]).to_dict(),
            'observational_source_selection_not_randomized':True,'independent_validation_dataset':False,
            'replicated_original_phylogenetic_SMD_model':False,'original_article_novelty_claim':False,
            'confidence_interval_is_not_percentage_reproduction_loss':True,
            'new_iwe_strict_H1_effects':0,'ALAN_effect_estimated':False,
            'prediction_intervals_normal_working_scale_may_exceed_natural_bounds':True,
            'selection_cohort_diagnostics':{m:selection_bootstrap(eligible[eligible.metric==m],nboot=nboot) for m in METRICS}}
    return models,pd.DataFrame(coverage),pd.DataFrame(boot),pd.DataFrame(influence),pd.DataFrame(study_rows),report
