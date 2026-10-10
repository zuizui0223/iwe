"""Source grain and falsifiable current/prior/future fluorescence timing."""
import numpy as np
import pandas as pd
import pytest

from scripts.analyze_slimon2026_joint_fe_weeklag import (
    match_exact_flower_neighbours, audit_twfe,
)


def _panel(seed=20261010, n_plants=28):
    rng=np.random.default_rng(seed)
    rows=[]
    for i in range(n_plants):
        days=[193,200,207,214,221,228]
        flowers=rng.binomial(1, .42, size=len(days))
        for j,d in enumerate(days):
            # An exact source-lag design where prior open flowers
            # explain every Mompha-positive visit; concurrent and
            # future blooms add no independent information.
            outcome=int(flowers[j-1]) if j else 0
            rows.append({
                "source_plant_id":f"synthetic_{i}",
                "doy":d,
                "open_flower_snapshot":int(flowers[j]),
                "mompha_positive":outcome,
            })
    return pd.DataFrame(rows)


def test_exact_adjacent_source_week_only_and_two_way_fe_recovers_lag():
    panel=_panel()
    subset=match_exact_flower_neighbours(panel)
    assert len(subset)==28*4
    assert set(subset.doy)=={200,207,214,221}
    assert subset.prior_open_7d.isin([0,1]).all()
    result=audit_twfe(subset,n_boot=36)
    assert result["n_matched_plant_visits"]==112
    assert result["n_original_plants"]==28
    assert result["n_original_survey_days"]==4
    assert result["joint_twfe_slopes"]["prior_open_7d"]==pytest.approx(1.,abs=1e-5)
    assert abs(result["joint_twfe_slopes"]["current_open"])<1e-5
    assert abs(result["joint_twfe_slopes"]["future_open_7d"])<1e-5
    assert result["joint_twfe_plant_bootstrap_percentile_95pct"]["prior_open_7d"] is not None
    assert result["strict_h1_admitted"] is False
    assert not result["oviposition_date_measured"]


def test_no_borrowed_nonsequential_doy_or_fake_zero():
    panel=_panel(n_plants=6)
    panel=panel[panel.doy.isin([193,207,221])]
    with pytest.raises(ValueError,match="exact 7-day neighbours"):
        match_exact_flower_neighbours(panel)
    panel=_panel(n_plants=6)
    with pytest.raises(ValueError,match="repeated"):
        match_exact_flower_neighbours(pd.concat([panel,panel.iloc[[0]]]))
    with pytest.raises(ValueError,match="7"):
        match_exact_flower_neighbours(panel,lag_days=10)


def test_time_varying_plant_and_date_confounder_does_not_become_h1():
    rows=[]
    for plant in range(16):
        for d in [193,200,207,214,221,228]:
            open_now=int((plant+d//7)%3==0)
            mompha=int((plant%4==0) or d in [207,214])
            rows.append({"source_plant_id":f"p{plant}","doy":d,
                         "open_flower_snapshot":open_now,
                         "mompha_positive":mompha})
    subset=match_exact_flower_neighbours(pd.DataFrame(rows))
    out=audit_twfe(subset,n_boot=0)
    assert out["n_plant_boot_resamples_used"]==0
    assert out["n_original_survey_days"]==4
    assert out["not_predictive_out_of_sample"] is True
    assert out["observed_final_intact_seeds_measured"] is False
