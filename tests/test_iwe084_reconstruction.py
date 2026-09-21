import math

import pandas as pd
import pytest

from iwe.iwe084 import angular_transform_percent, reconstruct_iwe084


def source_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "state": "low",
                "partner_availability": "lower",
                "mean_filled_seed_pct": 21.71,
                "ci95_low_pct": 14.97,
                "ci95_high_pct": 29.31,
                "n_clones": 10,
            },
            {
                "state": "high",
                "partner_availability": "higher",
                "mean_filled_seed_pct": 39.56,
                "ci95_low_pct": 32.69,
                "ci95_high_pct": 46.64,
                "n_clones": 27,
            },
        ]
    )


def test_angular_transform_matches_source_definition():
    assert angular_transform_percent(0) == pytest.approx(0.0)
    assert angular_transform_percent(100) == pytest.approx(math.pi / 2)
    assert angular_transform_percent(25) == pytest.approx(math.asin(0.5))


def test_iwe084_reconstructs_positive_higher_availability_effect():
    effect = reconstruct_iwe084(source_rows())

    assert effect.n_low == 10
    assert effect.n_high == 27
    assert effect.theta_high > effect.theta_low
    assert effect.sd_low > 0
    assert effect.sd_high > 0
    assert effect.pooled_sd > 0
    assert effect.cohen_d > 0
    assert 0 < effect.hedges_j < 1
    assert effect.hedges_g > 0
    assert effect.variance_native > 0


def test_iwe084_result_is_locked_to_published_table_values():
    effect = reconstruct_iwe084(source_rows())

    assert effect.theta_low == pytest.approx(0.4846965804176788)
    assert effect.theta_high == pytest.approx(0.6802242871117625)
    assert effect.sd_low == pytest.approx(0.12218158136973015)
    assert effect.sd_high == pytest.approx(0.1809128134060566)
    assert effect.pooled_sd == pytest.approx(0.16778563252392986)
    assert effect.cohen_d == pytest.approx(1.1653423702187207)
    assert effect.hedges_g == pytest.approx(1.140091749239752, abs=2e-4)
    assert effect.variance_native == pytest.approx(0.14973, abs=2e-4)


def test_iwe084_fails_if_ci_inversion_is_not_symmetric():
    df = source_rows()
    df.loc[df["state"] == "low", "ci95_low_pct"] = 2.0
    with pytest.raises(ValueError, match="not symmetric"):
        reconstruct_iwe084(df)


def test_iwe084_requires_exact_low_high_states():
    df = source_rows()
    df.loc[df["state"] == "high", "state"] = "late"
    with pytest.raises(ValueError, match="states must be exactly low/high"):
        reconstruct_iwe084(df)
