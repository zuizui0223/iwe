import numpy as np
import pandas as pd
import pytest
from iwe.diel_reserve_meta import contrast, collapse_studies, reml_meta


def test_nonadditivity_and_exact_additive_controls():
    r=contrast([8,2,6,4],[1,1,1,1],'nonadditivity')
    assert r['effect']==pytest.approx(0)
    assert r['variance_bound']==pytest.approx(.04)
    assert r['variance_independent']==pytest.approx(.01)
    r=contrast([9,1,7,6],[1,1,1,1],'nonadditivity')
    assert r['effect']==pytest.approx(-3/23)


def test_zero_outcomes_and_unit_rescaling():
    a=contrast([10,0,0,10],[2,0,0,2],'night_marginal')
    assert a['effect']==1
    assert a['variance_bound']==0
    assert contrast([0,0,0,0],[1,1,1,1],'nonadditivity') is None
    assert contrast([0,2,0,0],[1,1,1,1],'day_marginal') is None
    a=contrast([8,2,6,4],[1,2,1,2],'nonadditivity')
    b=contrast([800,200,600,400],[100,200,100,200],'nonadditivity')
    assert a==pytest.approx(b)


def test_variance_bound_dominates_any_feasible_correlations():
    mu=np.array([8.,2,6,4]);se=np.array([.2,.5,1.,2.])
    r=contrast(mu,se,'nonadditivity')
    grad=(np.array([1,1,-1,-1])-r['effect'])/mu.sum()
    rng=np.random.default_rng(50)
    for _ in range(30):
        x=rng.normal(size=(4,4));v=x@x.T;den=np.sqrt(np.diag(v));cor=v/den[:,None]/den[None,:]
        assert grad @ (cor*se[:,None]*se[None,:]) @ grad <= r['variance_bound']+1e-12


def test_invalid_means_or_se_fail_instead_of_imputing():
    for means,se in [([1,-1,1,1],[1]*4),([1]*4,[1,np.nan,1,1]),([1]*4,[-1]*4)]:
        with pytest.raises(ValueError):contrast(means,se,'nonadditivity')


def test_study_clusters_not_treated_as_independent_publications():
    d=pd.DataFrame({'study':['A','A','B'],'effect':[.1,.3,-.2], 'variance_bound':[.01,.04,.01], 'variance_independent':[.005,.01,.005]})
    s=collapse_studies(d)
    assert len(s)==2
    a=s.set_index('study').loc['A']
    assert a['effect']==pytest.approx(.2)
    assert a['variance_bound']==pytest.approx((.1+.2)**2/4)
    assert a['variance_independent']==pytest.approx(.015/4)


def test_meta_equal_variance_identical_effects_no_false_precision():
    r=reml_meta(np.repeat(.2,8),np.repeat(.04,8))
    assert r['mean']==pytest.approx(.2)
    assert r['tau2']==pytest.approx(0,abs=1e-6)
    assert r['se_mean']>=np.sqrt(.04/8)-1e-8
    assert r['ci_low']<.2<r['ci_high']
    assert r['k_publications']==8


def test_meta_requires_valid_positive_precision_and_multiple_publications():
    with pytest.raises(ValueError):reml_meta([.1],[.01])
    with pytest.raises(ValueError):reml_meta([.1,.2],[0,.01])


def test_only_required_arms_are_needed_for_marginal_contrast():
    result=contrast([8,np.nan,4,np.nan],[1,np.nan,1,np.nan],'night_marginal')
    assert result['effect']==pytest.approx(1/3)
    with pytest.raises(ValueError):
        contrast([8,np.nan,4,np.nan],[1,np.nan,1,np.nan],'nonadditivity')


def source_fixture(tmp_path,changes=None):
    from iwe.diel_reserve_meta import KEY,ARM_NAMES
    records=[]
    for site in ['A','B']:
        for arm,mean in zip(ARM_NAMES,[8,2,6,4]):
            row=dict.fromkeys(KEY,'NA')
            row.update(study_ID='one_publication',plant_species='Example species',Site_period=site,
                       treatment_effectiveness_metric='seed set',effectiveness_units='seeds/fruit',
                       treatment_condition=arm,sample_size='10',effectiveness_value=str(mean),
                       effect_error='1',effect_error_units='SE',exclude='n',plant_native_status='native',
                       day_pollination_hrs='12',night_pollination_hrs='12')
            if changes:changes(row)
            records.append(row)
    path=tmp_path/'source.csv';pd.DataFrame(records).to_csv(path,index=False)
    return path


def test_site_period_is_preserved_not_averaged_or_cross_joined(tmp_path):
    from iwe.diel_reserve_meta import extract
    frame,audit=extract(source_fixture(tmp_path),verify=False)
    assert len(frame)==6 and frame.cell_id.nunique()==2
    assert frame.study.nunique()==1
    assert frame.complete_fourarm_precision.all()


def test_missing_closed_precision_does_not_remove_usable_marginal_pair(tmp_path):
    from iwe.diel_reserve_meta import extract
    def missing(row):
        if row['treatment_condition']=='complete exclusion':row['effect_error_units']='CI95'
    frame,_=extract(source_fixture(tmp_path,missing),verify=False)
    assert set(frame.loc[frame.precision_status=='source_precision_available','contrast'])=={'night_marginal','day_marginal'}
    assert not frame.complete_fourarm_precision.any()


def test_SE_SD_conversion_and_source_n_not_replication(tmp_path):
    from iwe.diel_reserve_meta import extract
    def sd(row):
        row.update(sample_size='4',effect_error='2',effect_error_units='SD')
    a,_=extract(source_fixture(tmp_path,sd),verify=False)
    expected=contrast([8,2,6,4],[1,1,1,1],'nonadditivity')
    assert a[a.contrast=='nonadditivity'].variance_bound.iloc[0]==pytest.approx(expected['variance_bound'])
    assert len(collapse_studies(a[a.contrast=='nonadditivity']))==1


def test_source_checksum_rejects_nonoriginal_fixture(tmp_path):
    from iwe.diel_reserve_meta import extract
    with pytest.raises(ValueError,match='blob mismatch'):extract(source_fixture(tmp_path))


def test_holm_keeps_six_planned_tests():
    from iwe.diel_reserve_meta import _holm
    p=np.array([.001,.01,.02,.04,.2,.5])
    assert _holm(p)==pytest.approx([.006,.05,.08,.12,.4,.5])
