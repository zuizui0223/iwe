#!/usr/bin/env python3
"""Independent MRCA and derivative-free likelihood verification, no new test."""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
from scipy.optimize import minimize
from iwe.diel_matched_asymmetry import extract_matched
from iwe.diel_reserve_meta import collapse_studies
from iwe.diel_endpoint_lineage import tree_correlation,map_source_taxa,species_kernels,covariance_reml,asymmetry_identity


def main():
    p=argparse.ArgumentParser()
    for n in ['author','traits','tree','original-analysis','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();tr=json.loads(a.tree.read_text());labels,r=tree_correlation(tr)
    # Independent tree method: sum shared ancestral edges, not incidence products.
    parent={c:(pa,float(le)) for (pa,c),le in zip(tr['edge'],tr['edge.length'])}
    root=next(iter(set(x[0] for x in tr['edge'])-set(parent)))
    paths=[]
    for tip in range(1,len(labels)+1):
        cur=tip;path={}
        while cur!=root:
            pa,length=parent[cur];path[cur]=length;cur=pa
        paths.append(path)
    other=np.zeros_like(r)
    for i,pi in enumerate(paths):
        for j,pj in enumerate(paths):
            other[i,j]=sum(pi[k] for k in set(pi)&set(pj))/np.sqrt(sum(pi.values())*sum(pj.values()))
    assert np.max(np.abs(other-r))<1e-12
    f,_=extract_matched(a.author,a.traits);original=pd.read_csv(a.original_analysis,dtype=str,keep_default_na=False)
    f,_=map_source_taxa(f,original,labels);f=f[f.precision_status.eq('source_precision_available')&f.phylo.notna()]
    checks=[]
    for metric in ['fruit set','seed set']:
        q=f[f.metric.eq(metric)];pubs,z,ks,kp=species_kernels(q,labels,r);st=collapse_studies(q)
        y=st.effect.to_numpy();v=st.variance_bound.to_numpy();one=np.ones(len(y))
        for name,km in [('publication_only',{'publication':np.eye(len(y))}),
                        ('publication_plus_species',{'publication':np.eye(len(y)),'species':ks}),
                        ('publication_species_phylogeny',{'publication':np.eye(len(y)),'species':ks,'phylogeny':kp})]:
            primary=covariance_reml(y,v,km);mats=list(km.values())
            def independent(theta,retmean=False):
                V=np.diag(v)
                for vv,kk in zip(theta,mats):V=V+vv*kk
                e,U=np.linalg.eigh(V);wy=U@((U.T@y)/e);wu=U@((U.T@one)/e)
                mean=float(one@wy/(one@wu));res=y-mean
                obj=.5*(np.log(e).sum()+np.log(one@wu)+np.sum((U.T@res)**2/e))
                return mean if retmean else obj
            start=np.array([primary['tau_'+x] for x in km])
            vals=[]
            # Nelder-Mead independent objective, including boundary parameters.
            for x0 in [start, np.full(len(mats),.05)]:
                fit=minimize(independent,x0,method='Nelder-Mead',bounds=[(0,10)]*len(mats),
                             options={'xatol':1e-10,'fatol':1e-11,'maxiter':10000})
                if fit.success:vals.append(fit)
            assert vals
            val=min(vals,key=lambda x:x.fun);mean=independent(val.x,True)
            assert abs(val.fun-primary['restricted_objective'])<1e-7
            assert abs(mean-primary['mean'])<1e-5
            checks.append({'metric':metric,'model':name,'objective_difference':float(val.fun-primary['restricted_objective']),
                           'mean_difference':mean-primary['mean'],'derivative_free_converged':True})
    rng=np.random.default_rng(20261115);err=0
    for o,d,n in rng.uniform(.001,10,size=(1000,3)):
        item=asymmetry_identity(o,d,n);err=max(err,abs(item['A']-item['direct_NminusD']*item['open_weight']))
    assert err<2e-14
    report={'independent_ancestral_path_correlation_max_error':float(np.max(np.abs(other-r))),
            'independent_eigendecomposition_Nelder_Mead_fits':checks,
            'direct_index_weight_identity_1000_cases_max_error':err,
            'same_estimation_code_was_not_the_only_check':True}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
