from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from iwe.diel_reserve_meta import KEY


def module():
    from iwe import diel_matched_asymmetry
    return diel_matched_asymmetry


def fixture(tmp_path, *, no_precision=False, missing_trait=False):
    records=[]
    for study,plant in [('one','Plant alpha'),('two','Plant beta')]:
        for arm,value in [('open pollination',10),('day pollination',4),('night pollination',6)]:
            r={k:'NA' for k in KEY}
            r.update(study_ID=study,plant_species=plant,locality='site',Site_period='period',
                     treatment_effectiveness_metric='seed set',effectiveness_units='seeds/fruit',
                     treatment_condition=arm,effectiveness_value=str(value),sample_size='10',
                     effect_error='NA' if no_precision else '1',effect_error_units='SE',
                     exclude='n',plant_native_status='native',day_pollination_hrs='12',night_pollination_hrs='12')
            records.append(r)
    a=tmp_path/'author.csv';pd.DataFrame(records).to_csv(a,index=False)
    tr=[{'old_name':'Plant alpha','plant_family':'Fam1','bloom_period_simple':'night'},
        {'old_name':'Plant beta','plant_family':'Fam2','bloom_period_simple':'day'}]
    if missing_trait:tr=tr[:1]
    b=tmp_path/'traits.csv';pd.DataFrame(tr).to_csv(b,index=False)
    return a,b


def test_paired_difference_matches_algebra_with_shared_open():
    r=module().matched_contrast([10,4,6],[1,2,3])
    assert r['effect']==pytest.approx((10-4)/14-(10-6)/16)
    assert r['effect']==pytest.approx(2*10*(6-4)/(14*16))
    assert abs(r['effect'])<=2
    assert r['variance_bound']>=r['variance_independent']


def test_gradient_is_numerically_correct_and_uses_open_only_once():
    m=np.array([10.,4.,6.]);s=np.array([1.,2.,3.])
    r=module().matched_contrast(m,s)
    def f(x):return (x[0]-x[1])/(x[0]+x[1])-(x[0]-x[2])/(x[0]+x[2])
    g=np.array([(f(m+np.eye(3)[i]*1e-5)-f(m-np.eye(3)[i]*1e-5))/2e-5 for i in range(3)])
    assert r['gradient']==pytest.approx(g,abs=1e-10)
    assert r['variance_independent']==pytest.approx(np.sum((g*s)**2))
    assert r['variance_bound']==pytest.approx(np.sum(np.abs(g*s))**2)
    assert r['gradient'][0]==pytest.approx(2*4/14**2-2*6/16**2)


def test_variance_bound_encloses_arbitrary_correlations():
    rng=np.random.default_rng(56);s=np.array([.3,.6,.2]);r=module().matched_contrast([.8,.6,.2],s);g=np.array(r['gradient'])
    for _ in range(100):
        x=rng.normal(size=(3,3));v=x@x.T;rho=v/np.sqrt(np.outer(v.diagonal(),v.diagonal()));cov=rho*np.outer(s,s)
        assert g@cov@g<=r['variance_bound']+1e-12


def test_swap_day_night_flips_sign_and_preserves_variance():
    a=module().matched_contrast([10,4,6],[1,2,3]);b=module().matched_contrast([10,6,4],[1,3,2])
    assert b['effect']==pytest.approx(-a['effect'])
    assert b['variance_bound']==pytest.approx(a['variance_bound'])
    eq=module().matched_contrast([10,5,5],[100,1,1]);assert eq['gradient'][0]==0


def test_zero_arms_are_not_replaced_by_pseudocounts():
    assert module().matched_contrast([0,0,1],[0,0,.1]) is None
    z=module().matched_contrast([10,0,0],[1,0,0]);assert z['effect']==0;assert z['variance_bound']==0
    with pytest.raises(ValueError):module().matched_contrast([10,-1,2],[1,1,1])
    with pytest.raises(ValueError):module().matched_contrast([10,1,2],[1,np.nan,1])


def test_three_arm_data_and_missing_traits_remain_eligible(tmp_path):
    a,b=fixture(tmp_path,missing_trait=True);data,audit=module().extract_matched(a,b,verify=False)
    assert len(data)==2
    assert data.precision_status.eq('source_precision_available').all()
    assert data.bloom.tolist()==['night','unknown']
    assert not data.complete_fourarm_means.any()
    assert audit['trait_complete_case_filter_applied'] is False


def test_missing_precision_retains_mean_not_fake_zero_uncertainty(tmp_path):
    a,b=fixture(tmp_path,no_precision=True);data,_=module().extract_matched(a,b,verify=False)
    assert len(data)==2;assert data.variance_bound.isna().all()
    assert data.effect.notna().all()


def test_duplicate_source_arm_or_cross_site_not_silently_averaged(tmp_path):
    a,b=fixture(tmp_path);d=pd.read_csv(a,dtype=str,keep_default_na=False)
    pd.concat([d,d.iloc[[0]]]).to_csv(a,index=False)
    data,audit=module().extract_matched(a,b,verify=False)
    assert len(data)==1;assert audit['flow']['ambiguous_duplicate_arm']==1
    a,b=fixture(tmp_path);d=pd.read_csv(a,dtype=str,keep_default_na=False)
    d.loc[0,'locality']='other';d.to_csv(a,index=False)
    data,audit=module().extract_matched(a,b,verify=False)
    assert len(data)==1


def test_trait_name_duplication_or_unsupported_bloom_code_fails(tmp_path):
    a,b=fixture(tmp_path);t=pd.read_csv(b);pd.concat([t,t.iloc[[0]]]).to_csv(b,index=False)
    with pytest.raises(ValueError,match='duplicate'):module().extract_matched(a,b,verify=False)
    a,b=fixture(tmp_path);t=pd.read_csv(b);t.loc[0,'bloom_period_simple']='moth';t.to_csv(b,index=False)
    with pytest.raises(ValueError,match='bloom'):module().extract_matched(a,b,verify=False)


def test_source_hash_is_verified_before_modeling(tmp_path):
    a,b=fixture(tmp_path)
    with pytest.raises(ValueError,match='Git blob'):module().extract_matched(a,b,verify=True)


def test_paired_trait_study_bootstrap_preserves_common_studies():
    d=pd.DataFrame([{'study':str(i),'bloom':b,'effect':v,'family':'one'} for i in range(5) for b,v in [('day',-.2),('night',.3)]])
    r=module().trait_bootstrap(d,nboot=300,seed=13)
    assert r['night_minus_day']==pytest.approx(.5)
    assert r['ci_low']==pytest.approx(.5)
    assert r['within_publication_comparisons']==5
    assert r['within_publication_mean']==pytest.approx(.5)
    assert r['n_publications_day']==r['n_publications_night']==5


def test_trait_absence_returns_explicit_unestimable_not_zero():
    d=pd.DataFrame([{'study':str(i),'bloom':'night','effect':.3,'family':'one'} for i in range(5)])
    r=module().trait_bootstrap(d,nboot=100,seed=13)
    assert r['status']=='missing_day_or_night_group'
    assert r['night_minus_day'] is None
