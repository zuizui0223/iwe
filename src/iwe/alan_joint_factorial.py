"""ALAN × diel reproductive-access identifiability (method, not new field data).

Observed ecological results cannot be inferred from a synthetic null or
unstratified original paper percentages. In particular, moderator V and
lighting log-RR y sharing the same dark/open O create negative sampling
covariance even when the true light effect is zero.
"""
from __future__ import annotations

import math
from typing import Mapping

import numpy as np

SLOTS = ("dark_day", "dark_open", "lit_day", "lit_open")


def _validated(means: Mapping[str, float], covariance):
    if set(means) != set(SLOTS):
        raise ValueError("An authentic factorial interaction requires all four treatment cells")
    m = np.asarray([means[key] for key in SLOTS], dtype=float)
    if not np.isfinite(m).all() or (m <= 0).any():
        raise ValueError("Four source arm means must be finite strictly positive on the log scale")
    if covariance is None:
        raise ValueError("Full source covariance of arm means is required; do not impute independent clusters")
    cov = np.asarray(covariance, dtype=float)
    if cov.shape != (4,4) or not np.isfinite(cov).all():
        raise ValueError("Expected source covariance matrix for all four original arm means")
    if not np.allclose(cov, cov.T, rtol=0, atol=1e-12):
        raise ValueError("Source covariance matrix must be symmetric")
    if (np.diag(cov) < 0).any() or np.linalg.eigvalsh(cov).min() < -1e-10:
        raise ValueError("Source covariance must be positive semi-definite")
    return m,cov


def _jacobian(m):
    d,o,ld,lo=m
    grad_v=np.array([-1/o,d/o**2,0,0])
    grad_y=np.array([0,-1/o,0,1/lo])
    grad_delta=np.array([1/d,-1/o,-1/ld,1/lo])
    return np.vstack([grad_v,grad_y,grad_delta])


def moderator_response_covariance(means: Mapping[str,float], covariance):
    """First-order covariance of V=1-D/O and y=log(LitOpen/DarkOpen).

    Covariance between original treatment means is required; zero
    off-diagonal values must not be assumed for shared blocks unless
    justified by their source design.
    """
    m,cov=_validated(means,covariance)
    J=_jacobian(m)
    out=J@cov@J.T
    if not np.allclose(out,out.T,atol=1e-11):
        raise ValueError("Derived covariance not symmetric")
    return {"variance_V":float(out[0,0]),"variance_y":float(out[1,1]),
            "covariance_V_y":float(out[0,1]),
            "derived_covariance_matrix":out.tolist(),
            "first_order_delta_only":True}


def factorial_log_interaction(means: Mapping[str,float], covariance):
    """Return a published-source-estimable four-cell DID, only with covariance.

    Delta = log(litOpen/darkOpen) - log(litDay/darkDay). Negative Delta
    means more negative lighting response when day+night access remains,
    rather than when access is restricted to daytime. A mechanism from
    moths/daytime compensation is NOT identified by this DID alone.
    """
    m,cov=_validated(means,covariance)
    d,o,ld,lo=m
    J=_jacobian(m)
    derived=J@cov@J.T
    return {"night_dependence_dark":float(1-d/o),
            "light_open_log_rr":float(np.log(lo/o)),
            "light_day_only_log_rr":float(np.log(ld/d)),
            "delta_light_x_access":float(np.log(lo/o)-np.log(ld/d)),
            "delta_variance":float(derived[2,2]),
            "night_dependence_and_light_error_covariance":float(derived[0,1]),
            "delta_standard_error":float(np.sqrt(max(derived[2,2],0))),
            "gradient_V":J[0].tolist(),"gradient_delta":J[2].tolist(),
            "source_covariance_required":True,
            "effect_is_not_proof_of_nocturnal_insect_causation":True,
            "source_is_assumed_validated_elsewhere":True}


def shared_denominator_null(*, seed=20261115,n_per_arm=40,repetitions=20000):
    """Monte Carlo under zero ALAN effect; synthetic, not a scientific effect.

    Eight hypothetical plant taxa differ ONLY in true night-dependence V,
    with O_dark=O_lit=0.60. Independent dark-day, dark-open, and lit-open
    binomial observations are simulated. The comparator separately samples
    the open measurement used in V, leaving y's actual dark-open value intact.
    This estimates synthetic beta artefacts and is not a corrected meta beta.
    """
    if n_per_arm<20 or repetitions<1000:
        raise ValueError("Enough synthetic replications/positive controls required")
    rng=np.random.default_rng(seed)
    true_v=np.linspace(.15,.75,8)
    shape=(repetitions,8)
    dark_day=rng.binomial(n_per_arm,.60*(1-true_v),size=shape)/n_per_arm
    dark_open=rng.binomial(n_per_arm,.60,size=shape)/n_per_arm
    dark_open_split=rng.binomial(n_per_arm,.60,size=shape)/n_per_arm
    lit_open=rng.binomial(n_per_arm,.60,size=shape)/n_per_arm
    valid=(dark_open>0).all(axis=1)&(lit_open>0).all(axis=1)&(dark_open_split>0).all(axis=1)
    dark_day,dark_open,dark_open_split,lit_open=[x[valid] for x in (dark_day,dark_open,dark_open_split,lit_open)]
    if len(dark_day)<.99*repetitions:
        raise ValueError("Too many invalid source denominators in synthetic experiment")
    y=np.log(lit_open/dark_open)
    x_shared=1-dark_day/dark_open
    x_split=1-dark_day/dark_open_split
    def slopes(x):
        dx=x-x.mean(axis=1,keepdims=True)
        dy=y-y.mean(axis=1,keepdims=True)
        return np.sum(dx*dy,axis=1)/np.sum(dx*dx,axis=1)
    shared=slopes(x_shared);split=slopes(x_split)
    return {"schema":"iwe_shared_dark_open_synthetic_null_v01",
            "true_ALAN_effect":0,"independent_study_count":8,
            "synthetic_taxa_count":8,"replications_requested":repetitions,
            "replications_analyzed":len(shared),"flowers_per_treatment":n_per_arm,
            "shared_control_mean_beta":float(np.mean(shared)),
            "shared_control_fraction_negative":float(np.mean(shared<0)),
            "split_control_mean_beta":float(np.mean(split)),
            "split_control_fraction_negative":float(np.mean(split<0)),
            "split_control_measures_need_independent_assignment_clusters_in_real_data":True,
            "true_night_dependence_range":[float(true_v.min()),float(true_v.max())],
            "synthetic_not_ecological_evidence":True,
            "beta_V_from_original_ALAN_studies_estimated":False}


def macgregor_pooled_caging_check():
    """Original-source paper pooled cage-condition proportions, NOT dark only.

    Macgregor et al. (2019), Ecosphere 10:e02550 DOI 10.1002/ecs2.2550.
    The paper itself mentions the simple independent-guild expected union.
    Published percent values lack per-light/access cell successes and SE.
    """
    d,n,o=.376,.528,.720
    pred=1-(1-d)*(1-n)
    return {"source_doi":"10.1002/ecs2.2550",
            "caging_open_all_light_pooled":o,
            "caging_day_all_light_pooled":d,
            "caging_night_all_light_pooled":n,
            "independent_guild_union_prediction":pred,
            "observed_minus_independent_guild_union":o-pred,
            "night_marginal_index_pooled":(o-d)/(o+d),
            "night_vs_day_index_pooled":(n-d)/(n+d),
            "can_be_used_as_dark_open_moderator":False,
            "can_be_used_to_estimate_light_x_access_interaction":False,
            "reported_light_x_access_interaction_significant":False,
            "published_interaction_numeric_beta_SE_available":False,
            "original_lighting_sites":5,"light_rotation_dates":4,
            "flowers_sampled":417,"individual_female_plants":169,
            "flowers_successfully_seeded":194,
            "damaged_seed_capsule_flowers":46,
            "non_damaged_successful_flowers_for_seed_count":148,
            "reared_seed_capsule_larva_taxon":"Lacanobia oleracea",
            "reared_larva_proves_hadena_bicruris":False,
            "no_reliable_study_specific_Hadena_seed_predation_effect":True}


def validate_published_factorial_gate(rows):
    """Conservative source-audited two-paper completeness receipt.

    Data may be promoted only with actual four treatment means and the
    correct source covariance. Paper-level yes/no cannot replace these.
    """
    expected={
       "MACGREGOR2019":("10.1002/ecs2.2550","nonsignificant","seed_present_per_original_flower"),
       "LU2026_JPE":("10.1093/jpe/rtag160","not_source_reconstructed","seed_per_ovule_in_formed_fruit"),
    }
    if len(rows)!=2 or set(x.get("study_id") for x in rows)!=set(expected):
        raise ValueError("Exactly two named original factorial papers are required")
    for row in rows:
        doi,interaction,outcome=expected[row["study_id"]]
        if row["doi"]!=doi or row["published_interaction_test"]!=interaction or row["outcome"]!=outcome:
            raise ValueError("Source DOI, test result, or denominator changed")
        if any(row[c]!="yes" for c in ("four_arm_design","same_experiment_nightly_access","genuine_lighting_assignment")):
            raise ValueError("Original light by access factorial design cannot be inferred")
        if row["original_joint_means_available"]!="no" or row["original_joint_covariance_available"]!="no":
            raise ValueError("Do not upgrade without original underlying data and covariance")
    return {"schema":"iwe_alan_joint_factorial_evidence_gate_v01",
            "papers_with_factorial_design":2,
            "papers_with_published_non_significant_interaction":1,
            "individually_source_recomputable_delta_interactions":0,
            "meta_analysable_papers":0,
            "night_dependence_beta_V_estimated":False,
            "original_papers_are_not_all_numerically_reestimated":True,
            "Lu_night_only_seed_change_is_not_open_access_loss":True,
            "Macgregor_pooled_caging_rates_not_dark_only":True,
            "light_x_access_interaction_non_significant_is_not_equivalence":True,
            "source_CI_for_beta_V":None,
            "new_strict_iwe_H1_effects":0}
