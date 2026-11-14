"""Four-arm source reproductive contrasts with covariance-upper uncertainty.

Exploratory reanalysis of Kendall & Nicholson (2025), NOT an ALAN experiment.
The upper bounds protect against unknown correlations only to first order;
they do not fix incorrect source sampling units or biased exclusion treatments.
"""
from __future__ import annotations
import hashlib
import math
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import t

AUTHOR_BLOB = '39a82d966afcdde670603add1c881ace8791ffe9'
ARM_NAMES = ('open pollination','complete exclusion','day pollination','night pollination')
CONTRASTS = ('nonadditivity','night_marginal','day_marginal')
KEY = ['study_ID','plant_species','plant_cultivar','locality','Site_period',
       'coordinates_lat','coordinates_lon','year_start','year_end','month_start',
       'month_end','treatment_effectiveness_metric','effectiveness_units','additional_treatment']


def contrast(means, sem, kind: str) -> dict | None:
    """A ratio of linear contrasts plus first-order independent/upper variances."""
    m=np.asarray(means,dtype=float); s=np.asarray(sem,dtype=float)
    if m.shape!=(4,) or s.shape!=(4,):
        raise ValueError('Use O,C,D,N slots; unused arms may remain missing')
    if kind=='nonadditivity': a=np.array([1,1,-1,-1]); b=np.ones(4)
    elif kind=='night_marginal': a=np.array([1,0,-1,0]); b=np.array([1,0,1,0])
    elif kind=='day_marginal': a=np.array([1,0,0,-1]); b=np.array([1,0,0,1])
    else: raise ValueError('Unknown four-arm contrast')
    required=b!=0; m=m[required];s=s[required];a=a[required];b=b[required]
    if not np.isfinite(m).all() or not np.isfinite(s).all() or (m<0).any() or (s<0).any():
        raise ValueError('Required means and SEMs must be finite and nonnegative')
    denominator=float(b@m)
    if denominator==0: return None
    effect=float(a@m/denominator); gradient=(a-effect*b)/denominator
    return {'effect':effect,'variance_bound':float(np.abs(gradient*s).sum()**2),
            'variance_independent':float(np.sum((gradient*s)**2))}


def collapse_studies(frame: pd.DataFrame) -> pd.DataFrame:
    """Equal cell means within publication; unknown cross-cell covariance bounded."""
    out=[]
    for study,g in frame.groupby('study',sort=True):
        if not np.isfinite(g[['effect','variance_bound','variance_independent']].to_numpy(float)).all() or (g[['variance_bound','variance_independent']]<0).any().any():
            raise ValueError('Invalid cell estimate/precision')
        n=len(g)
        out.append({'study':study,'effect':float(g.effect.mean()),'cells':n,
                    'variance_bound':float(np.sqrt(g.variance_bound).sum()**2/n**2),
                    'variance_independent':float(g.variance_independent.sum()/n**2)})
    return pd.DataFrame(out)


def reml_meta(effects, variances) -> dict:
    """Intercept-only REML with modified Hartung-Knapp, at publication grain."""
    y=np.asarray(effects,float); v=np.asarray(variances,float); k=len(y)
    if y.shape!=v.shape or k<2 or not np.isfinite(y).all() or not np.isfinite(v).all() or (v<=0).any():
        raise ValueError('At least two valid publication effects with positive variances required')
    def obj(tau2):
        w=1/(v+tau2); mean=np.dot(w,y)/w.sum()
        return .5*(np.log(v+tau2).sum()+np.log(w.sum())+np.dot(w,(y-mean)**2))
    fit=minimize_scalar(obj,bounds=(0,max(1.,10*np.var(y),10*v.max())),method='bounded',options={'xatol':1e-12})
    if not fit.success: raise ValueError('REML optimization did not converge')
    tau2=float(fit.x) if obj(fit.x)<obj(0) else 0.
    w=1/(v+tau2); mean=float(np.dot(w,y)/w.sum())
    q=float(np.dot(w,(y-mean)**2)/(k-1)); se=float(np.sqrt(max(1.,q)/w.sum()))
    critical=float(t.ppf(.975,k-1)); p=float(2*t.sf(abs(mean/se),k-1))
    pi=critical*np.sqrt(tau2+se**2)
    return {'k_publications':k,'mean':mean,'se_mean':se,'ci_low':mean-critical*se,
            'ci_high':mean+critical*se,'p_nominal':p,'tau2':tau2,'hk_scale':max(1.,q),
            'prediction_low':float(mean-pi),'prediction_high':float(mean+pi),
            'max_study_weight_share':float(w.max()/w.sum())}


def _number(value):
    try: return float(value)
    except (TypeError,ValueError): return float('nan')


def extract(path: Path, verify: bool=True) -> tuple[pd.DataFrame,dict]:
    raw=path.read_bytes(); blob=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if verify and blob!=AUTHOR_BLOB: raise ValueError('Original source Git blob mismatch')
    d=pd.read_csv(path,dtype=str,keep_default_na=False)
    if not set(KEY+['treatment_condition','sample_size','effectiveness_value','effect_error','effect_error_units','exclude'])<=set(d):
        raise ValueError('Missing original author source columns')
    if verify and (len(d)!=1652 or d.study_ID.nunique()!=140 or not d.exclude.eq('n').all()):
        raise ValueError('Original author source row/study inclusion drift')
    r=d[d.treatment_effectiveness_metric.isin(['fruit set','seed set'])].copy()
    counts=Counter(); allcells=[]; flow=Counter()
    needed={'nonadditivity':(0,1,2,3),'night_marginal':(0,2),'day_marginal':(0,3)}
    def precision(rows):
        n=np.array([_number(x) for x in rows.sample_size])
        error=np.array([_number(x) for x in rows.effect_error]); types=rows.effect_error_units.to_numpy()
        if not (np.isfinite(n)&(n>=2)&np.isclose(n,np.round(n),atol=1e-7,rtol=0)).all():
            return 'insufficient_or_noninteger_source_n',None
        if not (np.isfinite(error)&(error>=0)&np.isin(types,['SE','SD'])).all():
            return 'no_supported_source_SE_or_SD',None
        return 'source_precision_available',np.where(types=='SD',error/np.sqrt(n),error)
    for key,g in r.groupby(KEY,dropna=False,sort=True):
        arms=g[g.treatment_condition.isin(ARM_NAMES)]
        complete=len(arms)==4 and arms.treatment_condition.nunique()==4
        complete_precision=False
        if complete:
            vals=pd.to_numeric(arms.effectiveness_value,errors='coerce').to_numpy()
            complete=bool(np.isfinite(vals).all() and (vals>=0).all() and vals.sum()>0)
            complete_precision=complete and precision(arms)[0]=='source_precision_available'
        if complete:counts['complete_valid_fourarm_cells']+=1
        for kind,indices in needed.items():
            wanted=[ARM_NAMES[i] for i in indices];selected=arms[arms.treatment_condition.isin(wanted)]
            tag=key[-3]+'|'+kind+'|'
            if selected.treatment_condition.nunique()!=len(wanted):
                flow[tag+'missing_required_arm']+=1;continue
            if len(selected)!=len(wanted):
                flow[tag+'ambiguous_duplicate_arm']+=1;continue
            rows=selected.set_index('treatment_condition').loc[wanted]
            vals=np.array([_number(x) for x in rows.effectiveness_value])
            if not np.isfinite(vals).all() or (vals<0).any():
                flow[tag+'invalid_mean']+=1;continue
            if vals.sum()==0:
                flow[tag+'zero_required_denominator']+=1;continue
            status,errors=precision(rows)
            means=np.full(4,np.nan);sem=np.full(4,np.nan)
            means[list(indices)]=vals
            sem[list(indices)]=errors if errors is not None else 0
            result=contrast(means,sem,kind)
            info=dict(zip(KEY,key));native=rows.plant_native_status.eq('native').all()
            day=g[g.treatment_condition.eq('day pollination')]
            night=g[g.treatment_condition.eq('night pollination')]
            dh=_number(day.iloc[0].get('day_pollination_hrs')) if len(day)==1 else np.nan
            nh=_number(night.iloc[0].get('night_pollination_hrs')) if len(night)==1 else np.nan
            balanced=bool(np.isfinite(dh) and np.isfinite(nh) and dh>0 and nh>0 and .9<=dh/nh<=1.1)
            row={'cell_id':hashlib.sha256(repr(key).encode()).hexdigest()[:16],
                 'study':info['study_ID'],'plant':info['plant_species'],
                 'metric':info['treatment_effectiveness_metric'],'units':info['effectiveness_units'],
                 'contrast':kind,'native_only':bool(native),'balanced_reported_hours':balanced,
                 'complete_fourarm_means':complete,'complete_fourarm_precision':complete_precision,
                 'precision_status':status,**result}
            if errors is None:row['variance_bound']=None;row['variance_independent']=None
            elif result['variance_bound']<=0:row['precision_status']='zero_delta_variance'
            flow[tag+row['precision_status']]+=1;allcells.append(row)
    frame=pd.DataFrame(allcells)
    audit={'source_doi':'10.1111/ele.70036','git_blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),
           'original_rows':len(d),'original_study_ids':int(d.study_ID.nunique()),
           'fruit_seed_source_rows':len(r),'candidate_exact_source_cells':int(r.groupby(KEY,dropna=False).ngroups),
           'source_cell_flow':dict(counts),'endpoint_contrast_flow':dict(flow),
           'key_columns':KEY,'no_PCNL_date_or_geography_filter':True,
           'mean_arms_never_averaged_across_site_period_cultivar_additional_treatment':True,
           'original_author_dataset_not_new_independent_experiments':True,
           'precision_only_required_for_mathematically_used_arms':True}
    return frame,audit


def _holm(values):
    p=np.asarray(values,float); order=np.argsort(p); out=np.empty(len(p));running=0.
    for rank,i in enumerate(order):
        running=max(running,min(1.,(len(p)-rank)*p[i]));out[i]=running
    return out


def analyse(frame:pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame,dict]:
    eligible=frame[frame.precision_status.eq('source_precision_available')].copy()
    model=[];counts=[]; selection=[]
    for metric in ('fruit set','seed set'):
      for kind in CONTRASTS:
        full=frame[(frame.metric==metric)&(frame.contrast==kind)]
        for label,base in [('full_mean_panel',full),('precision_panel',full[full.precision_status.eq('source_precision_available')])]:
            means=base.groupby('study').effect.mean()
            selection.append({'metric':metric,'contrast':kind,'panel':label,'cells':len(base),
                              'publication_ids':len(means),'study_mean_unweighted':float(means.mean()),
                              'study_median':float(means.median()),'studies_positive':int((means>1e-12).sum()),
                              'studies_negative':int((means < -1e-12).sum())})
        for panel in ('primary','native_only','explicit_unit','balanced_hours','fourarm_precision'):
            z=eligible[(eligible.metric==metric)&(eligible.contrast==kind)]
            if panel=='fourarm_precision':z=z[z.complete_fourarm_precision]
            if panel=='native_only':z=z[z.native_only]
            if panel=='explicit_unit':z=z[~z.units.isin(['','NA'])]
            if panel=='balanced_hours':z=z[z.balanced_reported_hours]
            st=collapse_studies(z)
            if len(st)<3:continue
            for variance in ('bound','independent'):
                good=st[st['variance_'+variance]>0]
                if len(good)<3:continue
                result=reml_meta(good.effect,good['variance_'+variance])
                model.append({'metric':metric,'contrast':kind,'panel':panel,
                              'covariance':('upper_bound_both_arm_and_within_publication' if variance=='bound' else 'assumed_independent_sensitivity'),
                              'cells':len(z),'species':int(z.plant.nunique()),**result})
            if panel=='primary':
                counts.append({'metric':metric,'contrast':kind,'study_estimates':st.to_dict('records')})
    models=pd.DataFrame(model)
    models['p_holm_primary_six']=np.nan
    primary=(models.panel=='primary')&models.covariance.str.startswith('upper_bound')
    if primary.sum()!=6: raise ValueError('Six planned primary models not estimable; do not shrink test family')
    models.loc[primary,'p_holm_primary_six']=_holm(models.loc[primary,'p_nominal'].to_numpy())
    receipt={'primary_models':models.loc[primary].where(pd.notna(models.loc[primary]),None).to_dict('records'),
             'all_precision_cells':int(eligible.cell_id.nunique()),'publication_ids_with_precision':int(eligible.study.nunique()),
             'species_with_precision':int(eligible.plant.nunique()),'source_selection_summary':selection,
             'publication_effects_internal':counts,
             'variance_meaning':'first_order_delta_upper_bound_given_source_SEs_and_SD_n; within-publication covariance also bounded',
             'unknown_covariance_imputed_zero_in_primary':False,'random_effects':'intercept_REML_modified_Hartung_Knapp_t',
             'outcomes_pooled_together':False,'new_ALAN_causal_effect':False,'new_iwe_strict_H1_effects':0,
             'nonadditivity_proves_dynamic_pollinator_compensation':False,
             'studies_are_publication_ids_not_verified_independent_field_programmes':True,
             'shared_species_phylogeny_not_modelled':True,
             'new_publication_findings':'exploratory_reanalysis_not_independent_replication'}
    return models,pd.DataFrame(selection),receipt


def robustness(frame: pd.DataFrame, trait_path: Path) -> tuple[pd.DataFrame,pd.DataFrame,dict]:
    """Leave-one-publication-out and unweighted study/family bootstrap sensitivity."""
    raw=trait_path.read_bytes();blob=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if blob!='18381e550a7e405fe4f198909f0bb381bbecf1e0':
        raise ValueError('Original author family source changed')
    traits=pd.read_csv(trait_path,dtype=str,keep_default_na=False)
    if traits.old_name.duplicated().any(): raise ValueError('Nonunique source trait names')
    f=frame.copy();f['family']=f.plant.map(traits.set_index('old_name').plant_family)
    f.loc[f.family.isin(['','NA']),'family']=None
    rng=np.random.default_rng(20261114); boot=[]; leave=[]
    for metric in ('fruit set','seed set'):
      for kind in CONTRASTS:
        full=f[(f.metric==metric)&(f.contrast==kind)]
        z=full[full.precision_status.eq('source_precision_available')];st=collapse_studies(z)
        fits=[]
        for i in st.index:
            t0=st.drop(i);fits.append(reml_meta(t0.effect,t0.variance_bound))
        leave.append({'metric':metric,'contrast':kind,'publications_removed_one_at_a_time':len(st),
                      'minimum_mean':min(x['mean'] for x in fits),'maximum_mean':max(x['mean'] for x in fits),
                      'maximum_nominal_p':max(x['p_nominal'] for x in fits),
                      'deletions_with_nominal_CI_including_zero':sum(x['ci_low']<=0<=x['ci_high'] for x in fits)})
        for panel,q in [('all_available_means',full),('source_precision',z)]:
          for unit in ('publication','family'):
            vals=(q.groupby('study').effect.mean() if unit=='publication' else
                  q.groupby(['family','study']).effect.mean().groupby('family').mean()).to_numpy()
            draws=vals[rng.integers(0,len(vals),size=(10000,len(vals)))].mean(axis=1)
            lo,hi=np.quantile(draws,[.025,.975])
            boot.append({'metric':metric,'contrast':kind,'panel':panel,'resampling_unit':unit,
                         'groups':len(vals),'mean':float(vals.mean()),'ci_low':float(lo),'ci_high':float(hi),
                         'cells_without_source_family':int(q.family.isna().sum()),
                         'simultaneous_multiplicity_adjusted':False})
    return pd.DataFrame(leave),pd.DataFrame(boot),{'source_trait_git_blob':blob,
            'bootstrap_repetitions':10000,'seed':20261114,
            'family_bootstrap_is_not_a_phylogenetic_meta_model':True}
