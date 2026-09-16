import pandas as pd
import pytest

from iwe.meta import class_contrasts, fixed_effect_summary


def test_fixed_effect_summary_uses_inverse_variance_weights():
    df = pd.DataFrame(
        [
            {"interaction_type": "mutualist", "effect_oriented": 0.2, "variance_native": 0.04},
            {"interaction_type": "mutualist", "effect_oriented": 0.4, "variance_native": 0.01},
        ]
    )
    out = fixed_effect_summary(df)
    row = out.iloc[0]
    assert row["estimate"] == pytest.approx(0.36)
    assert row["se"] == pytest.approx((1 / 125) ** 0.5)
    assert row["k"] == 2


def test_class_contrasts_return_preregistered_pairs():
    summary = pd.DataFrame(
        [
            {"interaction_type": "mutualist", "estimate": 0.3, "se": 0.1, "k": 4},
            {"interaction_type": "antagonist", "estimate": -0.2, "se": 0.1, "k": 4},
            {"interaction_type": "mixed_pollinating_seed_predator", "estimate": 0.05, "se": 0.1, "k": 4},
        ]
    )
    out = class_contrasts(summary)
    assert set(out["contrast"]) == {
        "mutualist - antagonist",
        "mutualist - mixed_pollinating_seed_predator",
        "antagonist - mixed_pollinating_seed_predator",
    }
    ma = out.loc[out["contrast"] == "mutualist - antagonist"].iloc[0]
    assert ma["estimate"] == pytest.approx(0.5)
