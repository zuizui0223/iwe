"""Original-day and stage control contracts, using synthetic data only."""
import numpy as np
import pandas as pd
import pytest

from scripts.analyze_slimon2026_mompha_persistence import (
    source_stage_persistence_diagnostic,
    original_complete_stage_panel,
)


def synthetic_source_panel(seed=119, n_plants=28):
    rng=np.random.default_rng(seed)
    rows=[]
    for i in range(n_plants):
        prior=0
        for day in [193,200,207,214,221,228,235]:
            flower=int(rng.uniform()<.5)
            # Both lagged visible insect state and earlier flowering
            # influence *observed stage* incidence in this synthetic
            # fixture, not real data or an oviposition mechanism.
            positive=int(rng.uniform()<(.06+.53*prior+.27*flower))
            count=int(positive*(1+(i+day)%3))
            rows.append({
                "source_plant_id":f"synthetic_{i}",
                "doy":day,"open_flower_snapshot":flower,
                "mompha_positive":positive,
                "source_visible_mompha_count":count,
            })
            prior=positive
    return pd.DataFrame(rows)


def test_prior_stage_is_same_original_plant_and_exact_prior_seven_days():
    x=original_complete_stage_panel(synthetic_source_panel())
    assert set(x.doy)=={200,207,214,221,228}
    assert len(x)==28*5
    assert set(x.prior_mompha_positive_7d)=={0,1}
    for plant, sub in x.groupby("source_plant_id"):
        assert sub.doy.is_monotonic_increasing
        assert (sub.mompha_positive.astype(int) ==
                sub.source_visible_mompha_count.gt(0).astype(int)).all()
    assert x.prior_open_7d.isin([0,1]).all()


def test_stage_persistence_fe_comparison_and_logcount_are_not_strict_h1():
    x=source_stage_persistence_diagnostic(synthetic_source_panel(),n_boot=25)
    assert x["n_unique_original_plants"]==28
    assert x["n_original_complete_case_plant_visits"]==140
    assert x["valid_plant_bootstrap_replicates"]>=20
    assert x["strict_h1_effects_added"]==0
    assert x["lagged_Mompha_is_previous_detection_not_prior_oviposition"]
    assert "prior_mompha_only" in x["candidate_models_same_source_records"]
    assert "past_flower_and_past_mompha" in x["candidate_models_same_source_records"]
    assert x["candidate_models_same_source_records"][
        "both_stage_and_all_flower_axes"
    ]["coefficients"]["prior_mompha_positive_7d"]>0
    assert x["log1p_visible_count_model"]["joint_coefficients"]
    assert not x["out_of_sample_predictive_validation"]


def test_source_mompha_count_missing_mismatch_or_duplicate_fails():
    original=synthetic_source_panel()
    corrupted=original.copy()
    corrupted.loc[0,"source_visible_mompha_count"]=np.nan
    with pytest.raises(ValueError,match="missing"):
        original_complete_stage_panel(corrupted)
    corrupted=original.copy()
    corrupted.loc[0,"mompha_positive"] = 1-int(
        corrupted.loc[0,"mompha_positive"]
    )
    with pytest.raises(ValueError,match="count does not match"):
        original_complete_stage_panel(corrupted)
    with pytest.raises(ValueError,match="duplicate"):
        original_complete_stage_panel(pd.concat([original,original.iloc[[0]]]))


def test_source_week_missing_never_becomes_zero_stage():
    x=synthetic_source_panel()
    x=x.loc[~((x.source_plant_id=="synthetic_0")&(x.doy==207))]
    matched=original_complete_stage_panel(x)
    assert not matched[
        (matched.source_plant_id=="synthetic_0")&
        (matched.doy.isin([200,207,214]))
    ].shape[0]
    assert matched.source_plant_id.nunique()==28
