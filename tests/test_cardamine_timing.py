import pandas as pd
import pytest

from iwe.cardamine_timing import (
    adult_flight_windows,
    cardamine_timing_only_exposure,
    first_flowering_dates,
)


def _plants():
    return pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 100, "flowers": 0, "intact_ru": 999},
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 106, "flowers": 3, "intact_ru": 0},
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 112, "flowers": 1, "intact_ru": 500},
            {"year": 2012, "ecotype": "late", "plant_id": "L1", "doy": 120, "flowers": 2, "intact_ru": -100},
            {"year": 2012, "ecotype": "late", "plant_id": "L2", "doy": 145, "flowers": 4, "intact_ru": 10000},
        ]
    )


def _adults():
    return pd.DataFrame(
        {
            "year": [2012] * 11,
            "event_doy": [110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130],
        }
    )


def test_first_flowering_uses_first_positive_flower_observation():
    out = first_flowering_dates(_plants())
    e1 = out.loc[out["plant_id"] == "E1"].iloc[0]
    assert e1["first_flowering_doy"] == 106


def test_adult_window_uses_source_compatible_tenth_to_ninetieth_percentiles():
    out = adult_flight_windows(_adults()).iloc[0]
    assert out["adult_q10_doy"] == pytest.approx(112)
    assert out["adult_q90_doy"] == pytest.approx(128)
    assert out["n_adult_events"] == 11


def test_timing_group_preserves_early_core_and_late_positions():
    out = cardamine_timing_only_exposure(_plants(), _adults()).set_index("plant_id")
    assert out.loc["L1", "timing_group"] == "core_flight"
    assert out.loc["E1", "timing_group"] == "early_refugium"
    assert out.loc["L2", "timing_group"] == "late_refugium"


def test_timing_exposure_ignores_response_columns():
    plants = _plants()
    out1 = cardamine_timing_only_exposure(plants, _adults())
    plants["intact_ru"] = list(reversed(plants["intact_ru"].tolist()))
    plants["eggs"] = [1000, 0, 500, 0, 900]
    out2 = cardamine_timing_only_exposure(plants, _adults())
    pd.testing.assert_frame_equal(out1, out2)


def test_ecotype_is_retained_and_not_pooled():
    out = cardamine_timing_only_exposure(_plants(), _adults())
    assert set(out["ecotype"]) == {"early", "late"}


def test_missing_adult_year_fails_closed():
    plants = _plants().copy()
    plants.loc[len(plants)] = {
        "year": 2013,
        "ecotype": "early",
        "plant_id": "E2",
        "doy": 101,
        "flowers": 2,
        "intact_ru": 1,
    }
    with pytest.raises(ValueError, match="missing adult timing window"):
        cardamine_timing_only_exposure(plants, _adults())


def test_invalid_quantiles_fail():
    with pytest.raises(ValueError, match="quantiles"):
        adult_flight_windows(_adults(), 0.9, 0.1)
