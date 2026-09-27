import pandas as pd
import pytest

from iwe.cardamine_outcome import (
    DEPENDENCE_ID,
    cardamine_realized_fraction,
    cardamine_smd_audit,
    cardamine_smd_effects,
)


def _summaries():
    return pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "max_ru": 10, "final_intact_ru": 8, "eggs": 99},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "max_ru": 10, "final_intact_ru": 6, "eggs": 0},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "max_ru": 10, "final_intact_ru": 2, "eggs": 10},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "max_ru": 10, "final_intact_ru": 0, "eggs": 10},
            {"year": 2012, "ecotype": "late", "plant_id": "L1", "max_ru": 20, "final_intact_ru": 10, "eggs": 0},
            {"year": 2012, "ecotype": "late", "plant_id": "L2", "max_ru": 20, "final_intact_ru": 4, "eggs": 0},
            {"year": 2012, "ecotype": "late", "plant_id": "L3", "max_ru": 20, "final_intact_ru": 16, "eggs": 0},
            {"year": 2012, "ecotype": "late", "plant_id": "L4", "max_ru": 20, "final_intact_ru": 12, "eggs": 0},
        ]
    )


def _exposure():
    return pd.DataFrame(
        [
            {"year": 2012, "ecotype": "early", "plant_id": "E1", "synchrony_group": "higher_synchrony"},
            {"year": 2012, "ecotype": "early", "plant_id": "E2", "synchrony_group": "higher_synchrony"},
            {"year": 2012, "ecotype": "early", "plant_id": "E3", "synchrony_group": "lower_synchrony"},
            {"year": 2012, "ecotype": "early", "plant_id": "E4", "synchrony_group": "lower_synchrony"},
            {"year": 2012, "ecotype": "late", "plant_id": "L1", "synchrony_group": "higher_synchrony"},
            {"year": 2012, "ecotype": "late", "plant_id": "L2", "synchrony_group": "higher_synchrony"},
            {"year": 2012, "ecotype": "late", "plant_id": "L3", "synchrony_group": "lower_synchrony"},
            {"year": 2012, "ecotype": "late", "plant_id": "L4", "synchrony_group": "lower_synchrony"},
        ]
    )


def test_realized_fraction_is_final_intact_over_max_ru():
    out = cardamine_realized_fraction(_summaries()).set_index("plant_id")
    assert out.loc["E1", "realized_fraction"] == pytest.approx(0.8)
    assert out.loc["E4", "realized_fraction"] == pytest.approx(0.0)


def test_outcome_ignores_egg_and_timing_columns():
    x = _summaries()
    out1 = cardamine_realized_fraction(x)
    x["eggs"] = list(reversed(x["eggs"].tolist()))
    x["first_flowering_doy"] = range(100, 108)
    out2 = cardamine_realized_fraction(x)
    pd.testing.assert_frame_equal(out1, out2)


def test_invalid_outcome_bounds_fail_closed():
    x = _summaries()
    x.loc[0, "final_intact_ru"] = 11
    with pytest.raises(ValueError, match="cannot exceed"):
        cardamine_realized_fraction(x)


def test_smd_audit_keeps_ecotypes_separate():
    audit = cardamine_smd_audit(_exposure(), _summaries())
    assert set(audit["ecotype"]) == {"early", "late"}
    assert len(audit) == 2
    assert audit["eligible_smd"].all()


def test_all_estimable_strata_share_one_dependence_cluster():
    effects = cardamine_smd_effects(_exposure(), _summaries())
    assert len(effects) == 2
    assert set(effects["dependence_id"]) == {DEPENDENCE_ID}
    assert set(effects["effect_family"]) == {"standardized_mean_difference"}


def test_contrast_is_higher_minus_lower_synchrony():
    effects = cardamine_smd_effects(_exposure(), _summaries()).set_index("ecotype")
    assert effects.loc["early", "effect_native"] > 0
    assert effects.loc["late", "effect_native"] < 0


def test_small_group_is_reported_not_replaced_by_another_stratum():
    exposure = _exposure().query("plant_id != 'E4'").copy()
    audit = cardamine_smd_audit(exposure, _summaries()).set_index("ecotype")
    assert not bool(audit.loc["early", "eligible_smd"])
    assert "at least two" in audit.loc["early", "blocker"]
    effects = cardamine_smd_effects(exposure, _summaries())
    assert set(effects["ecotype"]) == {"late"}
