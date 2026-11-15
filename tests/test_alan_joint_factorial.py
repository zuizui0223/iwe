import math
import numpy as np
import pytest

from iwe.alan_joint_factorial import (
    factorial_log_interaction, moderator_response_covariance,
    shared_denominator_null, macgregor_pooled_caging_check,
    validate_published_factorial_gate,
)


def test_true_factorial_interaction_uses_actual_four_cells():
    means = {"dark_day": 0.4, "dark_open": 0.7,
             "lit_day": 0.4, "lit_open": 0.56}
    cov = np.diag([0.0008, 0.0012, 0.0007, 0.0010])
    q = factorial_log_interaction(means, cov)
    assert q['delta_light_x_access'] == pytest.approx(math.log(.56/.7) - math.log(.4/.4))
    assert q['night_dependence_dark'] == pytest.approx(1-.4/.7)
    assert q['light_open_log_rr'] == pytest.approx(math.log(.56/.7))
    assert q['delta_variance'] > 0
    assert q['night_dependence_and_light_error_covariance'] < 0
    assert q['effect_is_not_proof_of_nocturnal_insect_causation']


def test_cross_arm_covariances_can_override_negative_shared_control_term():
    means={'dark_day':.4,'dark_open':.7,'lit_day':.4,'lit_open':.56}
    independent = np.diag([.001,.002,.001,.002])
    a = moderator_response_covariance(means, independent)
    assert a['covariance_V_y'] == pytest.approx(-.4*.002/(.7**3))
    assert a['variance_V']>0 and a['variance_y']>0
    # Modifying a genuine cross-arm covariance must be respected,
    # not silently erased by a naive independent-controls assumption.
    correlated=independent.copy()
    correlated[0,3]=correlated[3,0]=0.0001
    b=moderator_response_covariance(means, correlated)
    assert b['covariance_V_y'] != pytest.approx(a['covariance_V_y'])


def test_wrong_covariance_and_missing_cell_are_rejected():
    good={'dark_day':.3,'dark_open':.7,'lit_day':.3,'lit_open':.7}
    with pytest.raises(ValueError,match='all four'):
        factorial_log_interaction({'dark_day':.3,'dark_open':.7,'lit_open':.7},np.eye(4))
    with pytest.raises(ValueError,match='source covariance'):
        factorial_log_interaction(good,None)
    with pytest.raises(ValueError,match='symmetric'):
        v=np.eye(4);v[1,0]=.1
        factorial_log_interaction(good,v)
    with pytest.raises(ValueError,match='positive semi-definite'):
        v=np.eye(4);v[0,1]=v[1,0]=2.
        factorial_log_interaction(good,v)
    with pytest.raises(ValueError,match='strictly positive'):
        factorial_log_interaction({**good,'lit_day':0},np.eye(4))


def test_null_simulations_recover_artificial_negative_slope_and_independent_control():
    x=shared_denominator_null(seed=20261115,n_per_arm=40,repetitions=20000)
    assert x['true_ALAN_effect']==0
    assert x['independent_study_count']==8
    assert x['shared_control_mean_beta']<-.07
    assert x['shared_control_fraction_negative']>.62
    assert abs(x['split_control_mean_beta'])<.025
    assert .47<x['split_control_fraction_negative']<.53
    assert x['synthetic_not_ecological_evidence'] is True


def test_published_macgregor_rates_are_not_lighting_specific():
    r=macgregor_pooled_caging_check()
    assert r['caging_open_all_light_pooled']==pytest.approx(.72)
    assert r['caging_day_all_light_pooled']==pytest.approx(.376)
    assert r['caging_night_all_light_pooled']==pytest.approx(.528)
    assert r['independent_guild_union_prediction']==pytest.approx(1-(1-.376)*(1-.528))
    assert r['observed_minus_independent_guild_union']==pytest.approx(.72-(1-(1-.376)*(1-.528)))
    assert r['can_be_used_as_dark_open_moderator'] is False
    assert r['reported_light_x_access_interaction_significant'] is False
    assert r['reared_seed_capsule_larva_taxon']=='Lacanobia oleracea'
    assert r['reared_larva_proves_hadena_bicruris'] is False


def test_published_studies_cannot_be_promoted_to_joint_beta_without_original_cells():
    rows=[
      {'study_id':'MACGREGOR2019','doi':'10.1002/ecs2.2550','four_arm_design':'yes',
       'original_joint_means_available':'no','original_joint_covariance_available':'no',
       'published_interaction_test':'nonsignificant','outcome':'seed_present_per_original_flower',
       'same_experiment_nightly_access':'yes','genuine_lighting_assignment':'yes'},
      {'study_id':'LU2026_JPE','doi':'10.1093/jpe/rtag160','four_arm_design':'yes',
       'original_joint_means_available':'no','original_joint_covariance_available':'no',
       'published_interaction_test':'not_source_reconstructed','outcome':'seed_per_ovule_in_formed_fruit',
       'same_experiment_nightly_access':'yes','genuine_lighting_assignment':'yes'},
    ]
    s=validate_published_factorial_gate(rows)
    assert s['papers_with_factorial_design']==2
    assert s['papers_with_published_non_significant_interaction']==1
    assert s['individually_source_recomputable_delta_interactions']==0
    assert s['meta_analysable_papers']==0
    assert s['night_dependence_beta_V_estimated'] is False
    rows[0]['original_joint_means_available']='yes'
    with pytest.raises(ValueError,match='without original underlying data'):
        validate_published_factorial_gate(rows)
