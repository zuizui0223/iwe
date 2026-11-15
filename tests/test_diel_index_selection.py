from pathlib import Path
import importlib
import numpy as np
import pandas as pd
import pytest
from iwe.diel_reserve_meta import KEY


def mod():
    return importlib.import_module('iwe.diel_index_selection')


def fixture(tmp_path, with_open=True):
    rows=[]
    for arm,mean in [('day pollination',2.),('night pollination',4.)]+([('open pollination',6.)] if with_open else []):
        r={key:'' for key in KEY}
        r.update(study_ID='paper',plant_species='Plant example',treatment_effectiveness_metric='seed set',effectiveness_units='seeds/fruit',
                 treatment_condition=arm,effectiveness_value=str(mean),effect_error='0.2',effect_error_units='SE',sample_size='10',
                 exclude='n',plant_native_status='native',day_pollination_hrs='12',night_pollination_hrs='12')
        rows.append(r)
    a=tmp_path/'author.csv'; t=tmp_path/'traits.csv'
    pd.DataFrame(rows).to_csv(a,index=False)
    pd.DataFrame([{'old_name':'Plant example','plant_family':'Family','bloom_period_simple':'NA'}]).to_csv(t,index=False)
    return a,t


def test_direct_index_gradient_and_uncertainty():
    x=mod().direct_contrast([2.,4.],[.2,.4])
    assert x['effect']==pytest.approx(1/3)
    assert x['gradient']==pytest.approx([-8/36,4/36])
    assert x['variance_bound']>=x['variance_independent']>0
    for i in range(2):
        p=np.array([2.,4.]);m=p.copy();p[i]+=1e-5;m[i]-=1e-5
        numerical=(mod().direct_contrast(p,[0,0])['effect']-mod().direct_contrast(m,[0,0])['effect'])/2e-5
        assert x['gradient'][i]==pytest.approx(numerical,abs=1e-9)


def test_scale_and_swap_invariance():
    f=mod().direct_contrast
    a=f([2.,5.],[.3,.5]);b=f([20.,50.],[3,5]);s=f([5.,2.],[.5,.3])
    assert a['effect']==pytest.approx(b['effect'])
    assert a['variance_bound']==pytest.approx(b['variance_bound'])
    assert a['effect']==pytest.approx(-s['effect'])


def test_index_identity_and_open_zero_not_positive_direction():
    from iwe.diel_matched_asymmetry import matched_contrast
    rng=np.random.default_rng(1)
    for o,d,n in rng.lognormal(0,3,(50,3)):
        old=matched_contrast([o,d,n],[0,0,0])['effect']
        e=mod().direct_contrast([d,n],[0,0])['effect']
        w=mod().open_multiplier(o,d,n)
        assert old==pytest.approx(w*e,abs=1e-12)
        assert np.sign(old)==np.sign(e)
    assert mod().open_multiplier(0,2,4)==0
    assert mod().direct_contrast([2,4],[.2,.2])['effect']>0
    assert matched_contrast([0,2,4],[.1,.2,.2])['effect']==0


def test_boundary_means_and_invalid_precision():
    f=mod().direct_contrast
    assert f([0,0],[0,0]) is None
    assert f([0,4],[0,.2])['effect']==1
    assert f([0,4],[0,.2])['variance_bound']==0
    with pytest.raises(ValueError): f([-1,2],[.2,.3])
    with pytest.raises(ValueError): f([1,2],[np.nan,.3])


def test_covariance_bound_for_valid_psd_matrices():
    rng=np.random.default_rng(5)
    for _ in range(100):
        se=rng.uniform(.1,2,2);x=mod().direct_contrast(rng.uniform(.1,9,2),se)
        rho=rng.uniform(-1,1);V=np.outer(se,se)*np.array([[1,rho],[rho,1]])
        g=np.array(x['gradient'])
        assert g@V@g<=x['variance_bound']+1e-12


def test_no_open_needed_and_unknown_bloom_retained(tmp_path):
    a,t=fixture(tmp_path,False);df,audit=mod().extract_direct(a,t,verify=False)
    assert len(df)==1 and df.iloc[0]['bloom']=='unknown'
    assert df.iloc[0]['precision_status']=='source_precision_available'
    assert not df.iloc[0]['open_mean_eligible']
    assert audit['open_arm_required'] is False


def test_unrelated_missing_open_error_does_not_remove_pair(tmp_path):
    a,t=fixture(tmp_path);raw=pd.read_csv(a,dtype=str,keep_default_na=False)
    raw.loc[raw.treatment_condition=='open pollination','effect_error']='NA';raw.to_csv(a,index=False)
    df,_=mod().extract_direct(a,t,verify=False)
    assert df.iloc[0]['open_mean_eligible']
    assert not df.iloc[0]['prior_joint_precision']
    assert df.iloc[0]['precision_status']=='source_precision_available'


def test_duplicate_open_is_not_duplicate_day_night(tmp_path):
    a,t=fixture(tmp_path);raw=pd.read_csv(a,dtype=str,keep_default_na=False)
    raw=pd.concat([raw,raw[raw.treatment_condition=='open pollination']],ignore_index=True);raw.to_csv(a,index=False)
    df,_=mod().extract_direct(a,t,verify=False)
    assert len(df)==1 and not df.iloc[0]['open_mean_eligible']
    raw=pd.concat([raw,raw[raw.treatment_condition=='day pollination']],ignore_index=True);raw.to_csv(a,index=False)
    df,audit=mod().extract_direct(a,t,verify=False)
    assert len(df)==0 and audit['flow']['duplicate_DN_arm']==1


def test_unknown_day_precision_not_imputed(tmp_path):
    a,t=fixture(tmp_path);r=pd.read_csv(a,dtype=str,keep_default_na=False)
    r.loc[r.treatment_condition=='day pollination','effect_error']='NA';r.to_csv(a,index=False)
    df,_=mod().extract_direct(a,t,verify=False)
    assert len(df)==1 and df.iloc[0]['precision_status']!='source_precision_available'
    assert pd.isna(df.iloc[0]['variance_bound'])


def test_original_hash_and_denominator_gate(tmp_path):
    a,t=fixture(tmp_path)
    with pytest.raises(ValueError,match='blob'):mod().extract_direct(a,t,verify=True)
    r=pd.read_csv(a,dtype=str,keep_default_na=False)
    r.loc[r.treatment_condition=='night pollination','effectiveness_units']='seeds/plant';r.to_csv(a,index=False)
    df,_=mod().extract_direct(a,t,verify=False)
    assert len(df)==0


def test_source_exclusions_and_unknown_label_fail(tmp_path):
    a,t=fixture(tmp_path);r=pd.read_csv(a,dtype=str,keep_default_na=False);r.loc[0,'exclude']='y';r.to_csv(a,index=False)
    with pytest.raises(ValueError,match='excluded'):mod().extract_direct(a,t,verify=False)


def test_zero_variance_is_not_infinite_weight(tmp_path):
    a,t=fixture(tmp_path);r=pd.read_csv(a,dtype=str,keep_default_na=False)
    r.loc[r.treatment_condition=='day pollination',['effectiveness_value','effect_error']]=['0','0'];r.to_csv(a,index=False)
    df,_=mod().extract_direct(a,t,verify=False)
    assert df.iloc[0]['effect']==1
    assert df.iloc[0]['precision_status']=='zero_delta_variance'


def test_selection_bootstrap_keeps_shared_publication_joint():
    f=pd.DataFrame([{'study':str(i),'effect':i/10,'prior_joint_precision':group}
                    for i in range(6) for group in (True,False)])
    r=mod().selection_bootstrap(f,nboot=1000)
    assert r['shared_publications']==6
    assert r['gained_minus_common']==0
    assert r['ci_low']==0 and r['ci_high']==0
    assert r['randomized_selection_effect'] is False


def test_selection_bootstrap_missing_group_stays_unestimated():
    f=pd.DataFrame([{'study':str(i),'effect':.2,'prior_joint_precision':True} for i in range(4)])
    r=mod().selection_bootstrap(f,nboot=1000)
    assert r['status']=='too_few_publications_per_cohort'
