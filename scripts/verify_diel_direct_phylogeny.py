#!/usr/bin/env python3
"""Independent eigenvalue/Nelder-Mead checks for original-tree E covariance fits."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd
from scipy.linalg import eigh
from scipy.optimize import minimize
from iwe.diel_index_selection import extract_direct
from iwe.diel_endpoint_lineage import tree_correlation,map_source_taxa,species_kernels
from iwe.diel_reserve_meta import collapse_studies


def main():
    p=argparse.ArgumentParser()
    for key in ('author','traits','tree','original-analysis','models','out'):
        p.add_argument('--'+key,type=Path,required=True)
    args=p.parse_args();f,_=extract_direct(args.author,args.traits)
    labels,r=tree_correlation(json.loads(args.tree.read_text()))
    original=pd.read_csv(args.original_analysis,dtype=str,keep_default_na=False)
    f,_=map_source_taxa(f,original,labels)
    f=f[f.precision_status.eq('source_precision_available')&f.phylo.notna()]
    models=pd.read_csv(args.models)
    validated=[]
    for metric in ('fruit set','seed set'):
        q=f[f.metric.eq(metric)];st=collapse_studies(q)
        pubs,z,ks,kp=species_kernels(q,labels,r)
        if pubs!=st.study.tolist():raise ValueError('Independent original source key mismatch')
        mats=[np.eye(len(st)),ks,kp];y=st.effect.to_numpy();v=st.variance_bound.to_numpy();one=np.ones(len(st))
        def objective(theta,mean_only=False):
            V=np.diag(v)
            for component,k in zip(theta,mats):V=V+component*k
            eigen,U=eigh(V)
            if (eigen<=0).any():raise ValueError('Invalid original model covariance')
            w=1/eigen
            wy=U@((U.T@y)*w);wu=U@((U.T@one)*w)
            den=one@wu;mean=float(one@wy/den);res=y-mean
            value=.5*(np.log(eigen).sum()+np.log(den)+np.sum((U.T@res)**2*w))
            return mean if mean_only else float(value)
        fit=models[(models.metric==metric)&(models.panel=='tree_common')&
                   (models.model=='publication_species_phylogeny')]
        if len(fit)!=1:raise ValueError('Missing exact original E model')
        row=fit.iloc[0]
        start=np.array([row.tau_publication,row.tau_species,row.tau_phylogeny],float)
        sols=[minimize(objective,x0,method='Nelder-Mead',bounds=[(0,10)]*3,
                       options={'maxiter':12000,'xatol':1e-9,'fatol':1e-10})
              for x0 in (start,np.array([.1,.1,.1]),np.array([.2,0,0]))]
        good=[x for x in sols if x.success]
        if not good:raise ValueError('Independent direct E eigensolver did not converge')
        best=min(good,key=lambda x:x.fun)
        gap=abs(best.fun-row.restricted_objective)
        diff=abs(objective(best.x,True)-row['mean'])
        if gap>1e-7 or diff>1e-5:raise ValueError('Independent E phylogeny REML maximum not reproduced')
        validated.append({'metric':metric,'n_publications':len(st),'objective_gap':gap,
                          'fitted_mean_gap':diff,'independent_solver':'eigendecomposition_NelderMead',
                          'same_source_study_membership':True,'success':True})
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps({'schema':'iwe_direct_phylogeny_optimization_recheck_v01',
                                   'independent_fits':validated,'new_iwe_strict_h1':0},indent=2)+'\n')
    print(json.dumps(validated,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
