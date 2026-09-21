import pytest

from iwe.effects import hedges_g_from_summary, orient_effect


def test_synchrony_effect_keeps_sign():
    assert orient_effect(0.4, "synchrony") == pytest.approx(0.4)


def test_mismatch_effect_reverses_sign():
    assert orient_effect(0.4, "mismatch") == pytest.approx(-0.4)


def test_unknown_exposure_direction_fails_closed():
    with pytest.raises(ValueError):
        orient_effect(0.4, "timing")


def test_hedges_g_reconstructs_iwe011_extreme_timing_contrast():
    g, variance = hedges_g_from_summary(
        mean_high=0.13,
        sd_high=0.19,
        n_high=177,
        mean_low=0.40,
        sd_low=0.29,
        n_low=127,
    )
    assert g == pytest.approx(-1.1368391965)
    assert variance == pytest.approx(0.0155963310)


def test_hedges_g_rejects_invalid_group_summary():
    with pytest.raises(ValueError):
        hedges_g_from_summary(0.1, 0.2, 1, 0.3, 0.4, 10)
    with pytest.raises(ValueError):
        hedges_g_from_summary(0.1, 0.0, 10, 0.3, 0.4, 10)
