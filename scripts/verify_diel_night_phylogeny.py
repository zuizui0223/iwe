#!/usr/bin/env python3
"""Independent eigen-decomposition and Nelder–Mead source-fit comparison."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from iwe.diel_reserve_meta import extract, collapse_studies
from iwe.diel_endpoint_lineage import (
    tree_correlation, map_source_taxa, species_kernels, classify_endpoint,
)


def main():
    ap=argparse.ArgumentParser()
    for name in ("author","tree","original-analysis","models","denominators","out"):
        ap.add_argument("--"+name,type=Path,required=True)
    x=ap.parse_args()
    frame,_=extract(x.author)
    frame=frame[frame["contrast"].eq("night_marginal")]
    tree=json.loads(x.tree.read_text())
    labels,r=tree_correlation(tree)
    final=pd.read_csv(x.original_analysis,dtype=str,keep_default_na=False)
    df,_=map_source_taxa(frame,final,labels)
    df["denominator"]=[classify_endpoint(m,u) for m,u in zip(df.metric,df.units)]
    good=df[df.precision_status.eq("source_precision_available")&df.phylo.notna()]
    models=pd.read_csv(x.models)
    denom=pd.read_csv(x.denominators)
    checks=[]
    tests=[
        ("fruit set","all",61),
        ("seed set","all",54),
        ("seed set","seeds_per_fruit",32),
    ]
    for metric,scope,n in tests:
        q=good[good.metric.eq(metric)]
        if scope!="all":q=q[q.denominator.eq(scope)]
        pubs,z,ks,kp=species_kernels(q,labels,r)
        st=collapse_studies(q)
        if len(st)!=n or pubs!=st.study.tolist():
            raise ValueError("Original study count/kernel order changed")
        if scope=="all":
            a=models[(models.metric==metric)&(models.panel=="tree_common")&
                     (models.dependence=="publication_species_phylogeny")]
            if len(a)!=1:raise ValueError("Original full phylogenetic model absent")
            target=float(a.iloc[0]["mean"])
            target_objective=float(a.iloc[0]["restricted_objective"])
            start=np.array([a.iloc[0]["tau_publication"],a.iloc[0]["tau_species"],a.iloc[0]["tau_phylogeny"]])
        else:
            a=denom[(denom.metric==metric)&(denom.denominator==scope)]
            if len(a)!=1:raise ValueError("Original unit denominator absent")
            target=float(a.iloc[0]["conditional_phylogeny_mean"])
            start=np.array([.02,.04,.02])
            target_objective=None
        y=st.effect.to_numpy(float);v=st.variance_bound.to_numpy(float)
        one=np.ones(len(y))
        mats=[np.eye(len(y)),ks,kp]
        def evaluation(theta,return_mean=False):
            V=np.diag(v)
            for theta_k,K in zip(theta,mats):V+=theta_k*K
            values,U=np.linalg.eigh(V)
            if (values<=0).any():raise ValueError("Invalid positive source covariance")
            vy=U@((U.T@y)/values)
            vone=U@((U.T@one)/values)
            denominator=one@vone
            mean=float(one@vy/denominator)
            resid=y-mean
            value=.5*(np.log(values).sum()+np.log(denominator)+np.sum((U.T@resid)**2/values))
            return mean if return_mean else float(value)
        fits=[minimize(evaluation,t,method="Nelder-Mead",bounds=[(0,10)]*3,
                       options={"xatol":1e-10,"fatol":1e-11,"maxiter":12000})
              for t in (start,np.array([.05,.05,.05]),np.array([0,.08,0]))]
        solved=[a for a in fits if a.success]
        if not solved:raise ValueError("Independent optimizer did not converge")
        fit=min(solved,key=lambda f:f.fun)
        diff=abs(evaluation(fit.x,True)-target)
        if diff>1e-5 or (target_objective is not None and abs(fit.fun-target_objective)>1e-6):
            raise ValueError(f"Independent {metric}/{scope} phylogenetic likelihood disagrees: {diff}")
        checks.append({
            "metric":metric,"denominator":scope,
            "original_publications":n,"independent_mean_abs_error":diff,
            "independent_likelihood_gap": (
                abs(fit.fun-target_objective) if target_objective is not None else None
            ),
            "original_source_membership_verified":True,
            "success":True,
        })
    result={
        "schema":"iwe_night_marginal_independent_eigen_validation_v01",
        "original_source_doi":"10.1111/ele.70036",
        "checks":checks,
        "not_new_experimental_replicates":True,
        "new_ALAN_causal_effects":0,
        "new_iwe_strict_h1_effects":0,
    }
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    return 0


if __name__=="__main__":raise SystemExit(main())
