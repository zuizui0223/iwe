import pytest

from iwe.effects import orient_effect


def test_synchrony_effect_keeps_sign():
    assert orient_effect(0.4, "synchrony") == pytest.approx(0.4)


def test_mismatch_effect_reverses_sign():
    assert orient_effect(0.4, "mismatch") == pytest.approx(-0.4)


def test_unknown_exposure_direction_fails_closed():
    with pytest.raises(ValueError):
        orient_effect(0.4, "timing")
