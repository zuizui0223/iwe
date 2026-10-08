"""Synthetic (not biological) tests of actual effect-size sensitivity."""
import pandas as pd
import pytest

from iwe.cardamine_onset_sensitivity import cardamine_onset_effect_sensitivity


def _plants():
    ds = [
        ("E1", 100), ("E2", 101),
        ("C1", 118), ("C2", 120), ("C3", 112), ("C4", 119),
        ("L1", 144), ("L2", 145), ("B", 132),
    ]
    return pd.DataFrame([
        {"year": 2012, "ecotype": "late", "plant_id": pid,
         "doy": day, "flowers": 2, "egg_count": 900}
        for pid, day in ds
    ])


def _adults():
    return pd.DataFrame({
        "year": [2012] * 11,
        "event_doy": [100, 110, 112, 114, 116, 118, 120, 122, 125, 130, 150]
    })


def _outcomes():
    fractions = {
        "E1": .2, "E2": .4,
        "C1": .5, "C2": .6, "C3": .8, "C4": .7,
        "L1": .1, "L2": .3, "B": .9,
    }
    return pd.DataFrame([
        {"year": 2012, "ecotype": "late", "plant_id": pid,
         "max_ru": 10, "final_intact_ru": round(frac * 10)}
        for pid, frac in fractions.items()
    ])


def _take(df, mode, lag, contrast):
    rows = df[(df.assignment_method == mode) &
              (df.contrast == contrast)]
    if lag is None:
        rows = rows[rows.assumed_detection_lag_days.isna()]
    else:
        rows = rows[rows.assumed_detection_lag_days.eq(lag)]
    assert len(rows) == 1
    return rows.iloc[0]


def test_synthetic_onset_shift_changes_homologous_smd_not_strict_h1():
    df = cardamine_onset_effect_sensitivity(
        _plants(), _adults(), _outcomes(), scenario_lags=(0, 7)
    )
    assert len(df) == 12  # 2 contrasts x [observed, source, two scenarios x 2]
    baseline = _take(df, "observed_point", None, "core_vs_late")
    lag0 = _take(df, "scenario_stable_only", 0, "core_vs_late")
    lag7 = _take(df, "scenario_stable_only", 7, "core_vs_late")
    shifted = _take(df, "scenario_earliest_all", 7, "core_vs_late")
    source = _take(df, "source_certified_only", None, "core_vs_late")
    assert baseline.eligible_smd
    assert baseline.n_high == 4 and baseline.n_low == 3
    assert lag0.effect_native == pytest.approx(baseline.effect_native)
    assert lag0.n_excluded_uncertain == 0
    assert lag7.eligible_smd
    assert lag7.n_high == 3 and lag7.n_low == 2
    assert lag7.n_excluded_uncertain == 2
    assert lag7.effect_native != pytest.approx(baseline.effect_native)
    assert shifted.eligible_smd
    assert shifted.n_low == 2
    assert not source.eligible_smd
    assert pd.isna(source.effect_native)
    assert not df["source_verified_assumed_lag"].any()
    assert not df["strict_h1_effect_promoted"].any()


def test_source_bounds_can_stabilize_complete_comparison_but_are_not_auto_verified():
    source = pd.DataFrame([
        {"year": 2012, "ecotype": "late", "plant_id": k,
         "earliest_possible_doy": v, "source_locator": "original marked source row " + k}
        for k, v in {
            "C1": 114, "C2": 115, "C3": 111, "C4": 113,
            "L1": 140, "L2": 140, "B": 131,
        }.items()
    ])
    df = cardamine_onset_effect_sensitivity(
        _plants(), _adults(), _outcomes(),
        source_lower_bounds=source, scenario_lags=(7,)
    )
    row = _take(df, "source_certified_only", None, "core_vs_late")
    assert row.eligible_smd
    assert row.n_high == 4 and row.n_low == 3
    assert row.n_excluded_uncertain == 0
    assert not df["source_verified_assumed_lag"].any()
    assert not df["strict_h1_effect_promoted"].any()


def test_output_never_uses_eggs_to_set_exposure_and_only_outcomes_change_g():
    x = _plants()
    a = cardamine_onset_effect_sensitivity(x, _adults(), _outcomes(), scenario_lags=(7,))
    x["egg_count"] = 0
    b = cardamine_onset_effect_sensitivity(x, _adults(), _outcomes(), scenario_lags=(7,))
    pd.testing.assert_frame_equal(a, b)
    y = _outcomes()
    y.loc[y.plant_id == "B", "final_intact_ru"] = 1
    c = cardamine_onset_effect_sensitivity(x, _adults(), y, scenario_lags=(7,))
    assert _take(a, "observed_point", None, "core_vs_late").effect_native != (
        _take(c, "observed_point", None, "core_vs_late").effect_native
    )
    for key in ["n_excluded_uncertain", "n_high", "n_low"]:
        assert (a[key] == c[key]).all()


def test_bad_lags_rejected_without_reclassification():
    for lags in [(), (7, 7), (-1,), (7.5,), (True,)]:
        with pytest.raises(ValueError, match="scenario_lags|scenario lag"):
            cardamine_onset_effect_sensitivity(
                _plants(), _adults(), _outcomes(), scenario_lags=lags
            )
