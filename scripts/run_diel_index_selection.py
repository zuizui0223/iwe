#!/usr/bin/env python3
"""Source-pinned index/selection sensitivity; exports only aggregate results."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from iwe.diel_index_selection import extract_direct, analyse_selection
from iwe.diel_matched_asymmetry import extract_matched
from iwe.diel_reserve_meta import collapse_studies


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author',type=Path,required=True);p.add_argument('--traits',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--bootstrap',type=int,default=10000)
    a=p.parse_args()
    frame,source=extract_direct(a.author,a.traits)
    models,coverage,boot,influence,studies,report=analyse_selection(frame,nboot=a.bootstrap)
    # Independent source alignment and numerical REML score-root verification.
    prior,_=extract_matched(a.author,a.traits)
    join=prior.merge(frame,on='cell_id',suffixes=('_prior','_direct'),validate='one_to_one')
    discrepancy=float(np.max(np.abs(join.effect_prior-join.old_effect)))
    if discrepancy>1e-12:raise ValueError('Prior exact-cell effects failed source replay')
    root_checks=[]
    primary=models[(models.panel=='all_DN')&(models['index']=='E')&(models.covariance=='bound')]
    for _,m in primary.iterrows():
        q=studies[studies.metric==m.metric];y=q.effect.to_numpy();v=q.variance_bound.to_numpy()
        def score(tau):
            w=1/(v+tau);mu=w@y/w.sum()
            return float(np.sum(w*w*(y-mu)**2)-np.sum(w)+np.sum(w*w)/np.sum(w))
        upper=max(1.,10*np.var(y),10*v.max())
        if score(0)<=0:tau=0.
        else:
            while score(upper)>0:upper*=2
            tau=brentq(score,0,upper,xtol=1e-14)
        w=1/(v+tau);mu=w@y/w.sum()
        if abs(mu-m['mean'])>1e-7 or abs(tau-m.tau2)>1e-7:raise ValueError('Independent REML score mismatch')
        root_checks.append({'metric':m.metric,'score_root_tau2':tau,'mean_abs_error':abs(mu-m['mean'])})
    boundary=join[(join.precision_status_prior=='source_precision_available') &
                  (join.precision_status_direct=='zero_delta_variance')]
    boundary_summary=[]
    for metric,g in boundary.groupby('metric_direct'):
        boundary_summary.append({'metric':metric,'cells':len(g),'publication_ids':int(g.study_direct.nunique()),
            'night_positive_cells':int((g.effect_direct>0).sum()),'day_positive_cells':int((g.effect_direct<0).sum())})
    report['prior_precision_now_zero_delta_variance']=boundary_summary
    report['zero_delta_variance_is_not_no_effect']=True
    report.update(source=source,previous_source_comparisons={'previous_mean_cells':len(prior),
        'common_mean_cells':len(join),'prior_not_direct_due_both_zero_DN':len(prior)-len(join),
        'max_abs_previous_A_effect_error':discrepancy},independent_REML_checks=root_checks,
        bootstrap_repetitions=a.bootstrap)
    a.out.mkdir(parents=True,exist_ok=True)
    for name,df in [('index_selection_models',models),('source_coverage',coverage),
                    ('unweighted_source_diagnostics',boot),('leave_one_publication',influence),
                    ('primary_publication_summaries',studies),('primary_two_models',primary)]:
        df.to_csv(a.out/(name+'.csv'),index=False)
    (a.out/'index_selection_receipt.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    print(primary[['metric','k_publications','cells','mean','ci_low','ci_high','p_holm_primary_two','prediction_low','prediction_high']].to_string(index=False))
    print(json.dumps({k:report[k] for k in ['mean_cells','mean_publication_ids','mean_taxa','precision_cells','precision_publication_ids','precision_taxa']},indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
