import pytest

from iwe.effects import (\n    hedges_g_from_balanced_anova_means,\n    hedges_g_from_mean_se,\n    hedges_g_from_summary,\n    orient_effect,\n)


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



def test_hedges_g_from_mean_se_reconstructs_iwe015_2012():
    g, variance = hedges_g_from_mean_se(
        mean_high=2.66,
        se_high=2.95,
        n_high=59,
        mean_low=3.91,
        se_low=4.13,
        n_low=58,
    )
    assert g == pytest.approx(-0.0453662495)
    assert variance == pytest.approx(0.0337540056)


def test_hedges_g_from_mean_se_reconstructs_iwe015_2013():
    g, variance = hedges_g_from_mean_se(
        mean_high=9.77,
        se_high=6.91,
        n_high=55,
        mean_low=8.60,
        se_low=7.01,
        n_low=55,
    )
    assert g == pytest.approx(0.0225087081)
    assert variance == pytest.approx(0.0358615214)


def test_hedges_g_from_mean_se_rejects_nonpositive_se():
    with pytest.raises(ValueError):
        hedges_g_from_mean_se(1.0, 0.0, 10, 2.0, 0.2, 10)



def test_hedges_g_from_mean_se_reconstructs_iwe027_his_2007():
    g, variance = hedges_g_from_mean_se(
        mean_high=0.77,
        se_high=0.03,
        n_high=24,
        mean_low=0.62,
        se_low=0.04,
        n_low=24,
    )
    assert g == pytest.approx(0.8518282660)
    assert variance == pytest.approx(0.0885105687)


def test_hedges_g_from_mean_se_reconstructs_iwe027_gos_2007():
    g, variance = hedges_g_from_mean_se(
        mean_high=0.65,
        se_high=0.05,
        n_high=24,
        mean_low=0.40,
        se_low=0.05,
        n_low=24,
    )
    assert g == pytest.approx(1.0038892388)
    assert variance == pytest.approx(0.0915777666)



def test_balanced_anova_reconstructs_iwe023_week1_vs_week4():
    g, variance = hedges_g_from_balanced_anova_means(
        group_means=[0.85, 1.00, 0.91, 0.69],
        n_per_group=10,
        f_statistic=1.01,
        high_index=0,
        low_index=3,
    )
    assert g == pytest.approx(0.3732395638)
    assert variance == pytest.approx(0.1873253239)


def test_balanced_anova_reconstruction_fails_closed_on_invalid_inputs():
    with pytest.raises(ValueError):
        hedges_g_from_balanced_anova_means([0.8, 0.7], 10, 0.0, 0, 1)
    with pytest.raises(ValueError):
        hedges_g_from_balanced_anova_means([0.8, 0.7], 1, 1.2, 0, 1)
    with pytest.raises(ValueError):
        hedges_g_from_balanced_anova_means([0.8, 0.7], 10, 1.2, 0, 0)
    with pytest.raises(ValueError):
        hedges_g_from_balanced_anova_means([0.8, 0.7], 10, 1.2, 0, 2)
