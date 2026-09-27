import pandas as pd

from iwe.cardamine_pipeline import run_cardamine_preflight


def test_cardamine_preflight_runs_frozen_stages_in_order():
    plant_timing = pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 110, "flowers": 0},
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "doy": 114, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "doy": 120, "flowers": 3},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "doy": 106, "flowers": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "doy": 135, "flowers": 2},
            {"year": 2012, "ecotype": "late", "plant_id": "L1", "doy": 116, "flowers": 2},
            {"year": 2012, "ecotype": "late", "plant_id": "L2", "doy": 126, "flowers": 2},
            {"year": 2012, "ecotype": "late", "plant_id": "L3", "doy": 108, "flowers": 2},
            {"year": 2012, "ecotype": "late", "plant_id": "L4", "doy": 140, "flowers": 2},
        ]
    )
    adult_events = pd.DataFrame(
        {
            "year": [2012] * 11,
            "event_doy": [110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130],
        }
    )
    summaries = pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "max_ru": 10, "final_intact_ru": 8},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "max_ru": 10, "final_intact_ru": 6},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "max_ru": 10, "final_intact_ru": 2},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "max_ru": 10, "final_intact_ru": 0},
            {"year": 2012, "ecotype": "late", "plant_id": "L1", "max_ru": 20, "final_intact_ru": 10},
            {"year": 2012, "ecotype": "late", "plant_id": "L2", "max_ru": 20, "final_intact_ru": 4},
            {"year": 2012, "ecotype": "late", "plant_id": "L3", "max_ru": 20, "final_intact_ru": 16},
            {"year": 2012, "ecotype": "late", "plant_id": "L4", "max_ru": 20, "final_intact_ru": 12},
        ]
    )

    exposure, audit, effects = run_cardamine_preflight(
        plant_timing,
        adult_events,
        summaries,
    )

    assert set(exposure["synchrony_group"]) == {"higher_synchrony", "lower_synchrony"}
    assert len(audit) == 2
    assert audit["eligible_smd"].all()
    assert len(effects) == 2
    assert set(effects["ecotype"]) == {"early", "late"}
