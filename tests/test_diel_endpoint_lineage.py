"""Guard source endpoint definitions, true phylogeny and publication dependence."""
import numpy as np
import pandas as pd
import pytest
from iwe.diel_endpoint_lineage import (classify_endpoint, tree_correlation,
    species_kernels, covariance_reml, asymmetry_identity, map_source_taxa)
from iwe.diel_reserve_meta import reml_meta


def test_endpoint_denominators_not_one_undifferentiated_seed_result():
    assert classify_endpoint('seed set','seeds/fruit')=='seeds_per_fruit'
    assert classify_endpoint('seed set','seeds/capsule')=='seeds_per_fruit'
    assert classify_endpoint('seed set','seeds/plant')=='seeds_per_plant'
    assert classify_endpoint('seed set','seeds/flower')=='seeds_per_flower'
    assert classify_endpoint('seed set','seeds/ovule')=='seeds_per_ovule'
    assert classify_endpoint('seed set','viable seeds per fruit')=='viable_seeds_per_fruit'
    assert classify_endpoint('fruit set','fruit/flower')=='fruits_per_flower'
    assert classify_endpoint('fruit set','proportion')=='fruit_proportion_unspecified'
    assert classify_endpoint('seed set','NA')=='denominator_unknown'
    assert classify_endpoint('seed set','new nonaudited unit')=='denominator_unknown'
    with pytest.raises(ValueError):classify_endpoint('fruit mass','mg')


def simple_tree():
    return {'tip.label':['A','B','C'],'edge':[[5,4],[4,1],[4,2],[5,3]],
            'edge.length':[1.,1.,1.,2.],'Nnode':[2]}


def test_actual_shared_ancestry_not_family_identity():
    labels,r=tree_correlation(simple_tree())
    assert labels==['A','B','C']
    np.testing.assert_allclose(r,[[1,.5,0],[.5,1,0],[0,0,1]])
    assert np.linalg.eigvalsh(r).min()>0


@pytest.mark.parametrize('change',['negative','duplicate_tip','cycle','missing_tip'])
def test_invalid_tree_fails_instead_of_grafting_taxa(change):
    tr=simple_tree()
    if change=='negative':tr['edge.length'][0]=-1
    if change=='duplicate_tip':tr['tip.label'][1]='A'
    if change=='cycle':tr['edge'][0]=[4,5];tr['edge'][1]=[5,4]
    if change=='missing_tip':tr['edge'][-1]=[5,6]
    with pytest.raises(ValueError):tree_correlation(tr)


def test_equal_cell_species_memberships_and_shared_species():
    f=pd.DataFrame({'study':['x','x','y','z'],'phylo':['A','B','A','C']})
    pub,z,ks,kp=species_kernels(f,['A','B','C'],np.array([[1,.5,0],[.5,1,0],[0,0,1]]))
    assert pub==['x','y','z']
    np.testing.assert_allclose(z,[[.5,.5,0],[1,0,0],[0,0,1]])
    np.testing.assert_allclose(ks, z@z.T)
    assert ks[0,0]==.5 and kp[0,0]==.75
    assert kp[0,1]==.75
    assert np.linalg.eigvalsh(kp).min()>-1e-10
    f.loc[0,'phylo']='absent'
    with pytest.raises(ValueError,match='absent'):species_kernels(f,['A','B','C'],np.eye(3))


def test_source_crosswalk_no_fuzzy_or_silent_merges():
    frame=pd.DataFrame({'plant':['old A','old B','missing']})
    orig=pd.DataFrame({'plant_species':[' old A ','old A','old B'], 'phylo':['A','A','B']})
    result,receipt=map_source_taxa(frame,orig,['A','B'])
    assert result.phylo.tolist()[:2]==['A','B']
    assert pd.isna(result.phylo.iloc[2])
    assert receipt['unmapped_original_names']==['missing']
    conflict=pd.concat([orig,pd.DataFrame({'plant_species':['old A'],'phylo':['B']})])
    with pytest.raises(ValueError,match='conflict'):map_source_taxa(frame,conflict,['A','B'])


def test_same_signal_algebra_and_zero_open():
    for o,d,n in [(1,2,3),(5,1,8),(.1,.4,.5),(2,0,3),(0,2,3)]:
        r=asymmetry_identity(o,d,n)
        assert r['A']==pytest.approx(r['direct_NminusD']*r['open_weight'])
        assert r['open_weight']>=0
    assert asymmetry_identity(0,2,3)['A']==0
    with pytest.raises(ValueError):asymmetry_identity(1,-1,2)


def test_one_covariance_component_reproduces_parent_REML():
    y=np.array([-.2,.1,.5,.7,-.4,.2]);v=np.array([.02,.06,.01,.05,.08,.03])
    old=reml_meta(y,v);new=covariance_reml(y,v,{'publication':np.eye(len(y))})
    for field in ['mean','se_mean','ci_low','ci_high']:
        assert new[field]==pytest.approx(old[field],abs=3e-6)
    assert new['tau_publication']==pytest.approx(old['tau2'],abs=3e-6)


def test_two_component_fit_is_permutation_invariant():
    y=np.array([-.2,.1,.5,.7,-.4,.2]);v=np.array([.02,.06,.01,.05,.08,.03])
    labels=np.array([0,0,1,1,2,2]);s=(labels[:,None]==labels[None,:]).astype(float)
    k={'publication':np.eye(6),'species':s};a=covariance_reml(y,v,k)
    perm=np.array([5,2,0,3,1,4]);b=covariance_reml(y[perm],v[perm],{n:q[np.ix_(perm,perm)] for n,q in k.items()})
    assert a['mean']==pytest.approx(b['mean'],abs=1e-6)
    assert a['restricted_objective']==pytest.approx(b['restricted_objective'],abs=1e-7)
    assert a['conditional_interval_not_full_original_model']


def test_invalid_variance_or_kernel_rejected():
    y=np.array([1.,2,3,4]);v=np.ones(4)*.1
    with pytest.raises(ValueError):covariance_reml(y,[-1,.1,.1,.1],{'publication':np.eye(4)})
    k=np.eye(4);k[0,1]=2
    with pytest.raises(ValueError):covariance_reml(y,v,{'bad':k})
    with pytest.raises(ValueError):covariance_reml(y,v,{'bad':-np.eye(4)})
