"""Endpoint- and lineage-aware sensitivity of PR123's paired reproductive index.

Source reanalysis, NOT independent biological replication or ALAN causation.
Publication mean sampling bounds remain unchanged. The mixed covariance
intervals are plug-in generalized modified-KH sensitivities, not a literal
replication of the authors' multilevel SMD analysis or guaranteed coverage.
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize
from scipy.stats import t


def classify_endpoint(metric: str, units: str) -> str:
    """Literal original units, never infer selfing/viability from 'seed set'."""
    u=str(units).strip().lower()
    if metric=='fruit set':
        if u in {'fruit/flower','proportion fruit/flowers','proportion fruits/flowers',
                 'proportion of flowers that set fruit','capsule/flowers/plant',
                 'proportion converted (orig: percent fruit/flowers)'}:
            return 'fruits_per_flower'
        if u in {'capsule/plant','fruit per plant','number of pods per stalk'}:
            return 'fruit_count_per_plant_or_stalk'
        if u in {'# fruits','number of fruit'}:return 'fruit_count_denominator_unknown'
        if u=='proportion' or u.startswith('proportion converted'):return 'fruit_proportion_unspecified'
    elif metric=='seed set':
        if u in {'seeds/fruit','seeds per fruit','seed per fruit','mean seeds/fruit',
                 'seeds/capsule','seeds/pod'}:return 'seeds_per_fruit'
        if u in {'seeds/plant','count per plant'}:return 'seeds_per_plant'
        if u=='seeds/flower':return 'seeds_per_flower'
        if u in {'seed/ovule','seed:ovule','seeds/ovule','seeds per ovule',
                 'proportion converted (orig: seeds/ovule as percent)'} or 'fertilized and unfertilized' in u:
            return 'seeds_per_ovule'
        if u=='viable seeds per fruit':return 'viable_seeds_per_fruit'
        if u=='proportion converted (orig: percent viable seeds per fruit)':return 'viable_seed_fraction'
        if u=='proportion of flowers that produced seed':return 'seed_producing_flower_fraction'
        if u=='# seeds':return 'seed_count_denominator_unknown'
        if u=='number of viable seeds':return 'viable_seed_count_denominator_unknown'
    else:raise ValueError('Only separate source fruit set and seed set outcomes are supported')
    return 'denominator_unknown'


def tree_correlation(tree: dict) -> tuple[list[str],np.ndarray]:
    """Brownian correlation from original phylo edges; no pruning/grafting edits."""
    labels=list(map(str,tree['tip.label']));edge=np.asarray(tree['edge'],int)
    lengths=np.asarray(tree['edge.length'],float)
    n=len(labels)
    if len(set(labels))!=n or n<2 or edge.ndim!=2 or edge.shape[1]!=2 or len(edge)!=len(lengths):
        raise ValueError('Invalid tree labels or edge dimensions')
    if not np.isfinite(lengths).all() or (lengths<0).any() or (edge<=0).any():
        raise ValueError('Invalid branch length or node index')
    if len(set(edge[:,1]))!=len(edge):raise ValueError('Tree nodes have multiple parents')
    roots=set(edge[:,0])-set(edge[:,1])
    if len(roots)!=1:raise ValueError('Tree must have exactly one root')
    root=next(iter(roots));parent={int(child):(int(par),i) for i,(par,child) in enumerate(edge)}
    if root<=n or set(range(1,n+1)) & set(edge[:,0]):raise ValueError('Tips cannot be internal nodes')
    design=np.zeros((n,len(edge)))
    for tip in range(1,n+1):
        node=tip;seen=set()
        while node!=root:
            if node in seen or node not in parent:raise ValueError('Cycle, missing tip or disconnected tree')
            seen.add(node);node,j=parent[node];design[tip-1,j]=np.sqrt(lengths[j])
    covariance=design@design.T;depth=np.sqrt(np.diag(covariance))
    if (depth<=0).any():raise ValueError('Zero root-to-tip distance')
    correlation=covariance/np.outer(depth,depth)
    if np.linalg.eigvalsh(correlation).min() < -1e-8:raise ValueError('Phylogeny correlation not PSD')
    return labels,correlation


def map_source_taxa(frame, original, labels):
    """Use the original authors' final-name->tree-tip mapping, never fuzzy match."""
    if not {'plant_species','phylo'}<=set(original):raise ValueError('Original source name columns absent')
    m=original[['plant_species','phylo']].copy()
    for col in m:m[col]=m[col].astype(str).str.strip()
    m=m.drop_duplicates()
    if m.plant_species.duplicated().any():raise ValueError('Original species-to-tip mapping conflict')
    if not set(m.phylo)<=set(labels):raise ValueError('Source phylogenetic tip absent from author tree')
    f=frame.copy();f['phylo']=f.plant.str.strip().map(m.set_index('plant_species').phylo)
    return f,{'unmapped_original_names':sorted(f.loc[f.phylo.isna(),'plant'].unique().tolist()),
              'mapped_cells':int(f.phylo.notna().sum()),'unmapped_cells':int(f.phylo.isna().sum()),
              'mapped_source_names':int(f.loc[f.phylo.notna(),'plant'].nunique()),
              'mapped_accepted_tree_tips':int(f.phylo.nunique()),'fuzzy_names_or_new_grafts':False}


def species_kernels(frame,labels,correlation):
    """Publication means have equal-cell multiple membership, not one species guess."""
    if frame.phylo.isna().any() or not set(frame.phylo)<=set(labels):
        raise ValueError('Missing or absent original tree species')
    pubs=sorted(frame.study.unique().tolist());pi={p:i for i,p in enumerate(pubs)};si={s:i for i,s in enumerate(labels)}
    z=np.zeros((len(pubs),len(labels)))
    for study,g in frame.groupby('study'):
        for name,count in g.phylo.value_counts().items():z[pi[study],si[name]]=count/len(g)
    if not np.allclose(z.sum(axis=1),1):raise ValueError('Publication species shares must sum to one')
    r=np.asarray(correlation,float)
    if r.shape!=(len(labels),len(labels)) or not np.isfinite(r).all() or not np.allclose(r,r.T):
        raise ValueError('Invalid original phylogenetic correlation')
    return pubs,z,z@z.T,z@r@z.T


def asymmetry_identity(o,d,n):
    m=np.asarray([o,d,n],float)
    if not np.isfinite(m).all() or (m<0).any():raise ValueError('Nonnegative finite means required')
    if o+d==0 or o+n==0 or d+n==0:raise ValueError('Undefined ratio; no continuity constant')
    direct=(n-d)/(n+d);weight=2*o*(n+d)/((o+d)*(o+n))
    a=(o-d)/(o+d)-(o-n)/(o+n)
    return {'A':a,'direct_NminusD':direct,'open_weight':weight}


def covariance_reml(effects,variances,kernels):
    """Publication-mean REML with multiple covariance kernels and plug-in t CI.

    Unknown cell covariance bounded before input. Additional heterogeneity
    kernels describe shared species/phylogeny, not extra sampling replicates.
    Variance-component and tree uncertainty are not fully propagated in CI.
    """
    y=np.asarray(effects,float);v=np.asarray(variances,float);n=len(y)
    if y.shape!=v.shape or y.ndim!=1 or n<3 or not np.isfinite(y).all() or not np.isfinite(v).all() or (v<=0).any():
        raise ValueError('At least three finite publication effects with positive sampling bounds')
    names=list(kernels);ks=np.asarray([kernels[k] for k in names],float)
    if not len(names):raise ValueError('At least one covariance kernel required')
    for k in ks:
        if k.shape!=(n,n) or not np.isfinite(k).all() or not np.allclose(k,k.T,atol=1e-10) or np.linalg.eigvalsh(k).min() < -1e-8:
            raise ValueError('Covariance kernels must be finite symmetric PSD')
    one=np.ones(n);eye=np.eye(n)
    def calculate(theta,gradient=True):
        cov=np.diag(v)+np.einsum('j,jkl->kl',theta,ks)
        fact=cho_factor(cov,lower=True,check_finite=False)
        w=cho_solve(fact,eye,check_finite=False);u=w@one;den=float(one@u)
        mean=float(u@y/den);r=y-mean;wr=w@r
        value=.5*(2*np.log(np.diag(fact[0])).sum()+np.log(den)+r@wr)
        if not gradient:return value,mean,den,float(r@wr)
        P=w-np.outer(u,u)/den
        grad=.5*(np.einsum('ab,jab->j',P,ks)-np.einsum('a,jab,b->j',wr,ks,wr))
        return float(value),grad
    upper=max(10.,100*float(np.var(y)));base=max(float(np.var(y)),.01)
    starts=[np.zeros(len(ks)),np.repeat(base/len(ks),len(ks))]
    for j in range(len(ks)):
        start=np.zeros(len(ks));start[j]=base;starts.append(start)
    fits=[minimize(calculate,x,jac=True,method='L-BFGS-B',bounds=[(0.,upper)]*len(ks),
                   options={'ftol':1e-12,'gtol':1e-8,'maxiter':1000,'maxls':50}) for x in starts]
    good=[f for f in fits if f.success and np.isfinite(f.fun)]
    if not good:raise ValueError('No successful REML multistart optimization')
    fit=min(good,key=lambda f:f.fun);val,mean,den,rss=calculate(fit.x,False)
    gradient=calculate(fit.x)[1];projected=gradient.copy()
    projected[(fit.x<1e-8)&(gradient>0)]=0
    projected[(fit.x>upper-1e-8)&(gradient<0)]=0
    if np.max(np.abs(projected))>5e-4:raise ValueError('REML projected score not stationary')
    scale=max(1.,rss/(n-1));se=np.sqrt(scale/den);crit=t.ppf(.975,n-1)
    result={'k_publications':n,'mean':mean,'se_mean':float(se),'ci_low':float(mean-crit*se),
            'ci_high':float(mean+crit*se),'p_nominal':float(2*t.sf(abs(mean/se),n-1)),
            'conditional_t_df':n-1,'hk_scale':float(scale),'restricted_objective':float(val),
            'optimizer_successful_starts':len(good),'optimizer_total_starts':len(fits),
            'largest_projected_score':float(np.max(np.abs(projected))),
            'variance_component_upper_boundary_hit':bool(np.any(fit.x>.999*upper)),
            'conditional_interval_not_full_original_model':True}
    result.update({'tau_'+name:float(value) for name,value in zip(names,fit.x)})
    return result
