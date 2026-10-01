import math

import pandas as pd
import pytest

from iwe.iwe023_raw import audit_iwe023_dataframe


def _balanced_fixture(scale=1.0):
    # Four balanced groups with n=10 each and a common within-group pattern.
    offsets = [-1.5, -1.0, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1.0, 1.5]
    means = {1: 0.85, 2: 1.00, 3: 0.91, 4: 0.69}
    rows = []
    for week, mean in means.items():
        for plant, offset in enumerate(offsets, start=1):
            rows.append(
                {
                    "plant": f"W{week}_{plant}",
                    "week": week,
                    "seed": scale * (mean + 0.20 * offset),
                }
            )
    return pd.DataFrame(rows)


def test_raw_audit_preserves_balanced_design_and_returns_both_standardizers():
    df = _balanced_fixture()
    summary, effects = audit_iwe023_dataframe(
        df,
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        # Synthetic fixture is not intended to reproduce F=1.01 exactly.
        f_tolerance=100.0,
    )
    assert list(summary["n"]) == [10, 10, 10, 10]
    assert summary["raw_design_ready"].all()
    row = effects.iloc[0]
    assert bool(row["raw_effect_ready"])
    assert math.isfinite(row["effect_native"])
    assert math.isfinite(row["variance_native"])
    assert math.isfinite(row["contrast_only_g_sensitivity"])
    assert row["residual_df"] == 36



def _published_reconstruction_fixture(scale=1.0):
    """Exact synthetic four-week data matching the frozen published summaries."""
    means = {1: 0.85, 2: 1.00, 3: 0.91, 4: 0.69}
    # Published relative means imply MS_between = 0.17025 for n=10/group.
    # F=1.01 therefore implies MS_within below. Ten symmetric observations
    # with five at -a and five at +a have sample variance (10/9)*a^2,
    # so a^2 = 0.9*MS_within reproduces the source residual variance exactly.
    ms_within = 0.17025 / 1.01
    amplitude = math.sqrt(0.9 * ms_within)
    rows = []
    for week, mean in means.items():
        for plant in range(1, 11):
            offset = -amplitude if plant <= 5 else amplitude
            rows.append(
                {
                    "plant": f"W{week}_{plant}",
                    "week": week,
                    "seed": scale * (mean + offset),
                }
            )
    return pd.DataFrame(rows)


def test_raw_audit_exactly_reproduces_frozen_iwe023_effect():
    summary, effects = audit_iwe023_dataframe(
        _published_reconstruction_fixture(),
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
    )
    assert list(summary["n"]) == [10, 10, 10, 10]
    assert summary["raw_design_ready"].all()
    assert summary["raw_f"].iloc[0] == pytest.approx(1.01, rel=1e-12)
    row = effects.iloc[0]
    assert bool(row["raw_effect_ready"])
    assert row["effect_native"] == pytest.approx(0.3815303645, rel=1e-9)
    assert row["variance_native"] == pytest.approx(0.1937181574, rel=1e-9)
    assert row["residual_df"] == 36

def test_raw_smd_is_invariant_to_common_positive_scaling():
    _, effects1 = audit_iwe023_dataframe(
        _balanced_fixture(scale=1.0),
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        f_tolerance=100.0,
    )
    _, effects2 = audit_iwe023_dataframe(
        _balanced_fixture(scale=7.0),
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        f_tolerance=100.0,
    )
    assert effects1.iloc[0]["effect_native"] == pytest.approx(
        effects2.iloc[0]["effect_native"]
    )
    assert effects1.iloc[0]["variance_native"] == pytest.approx(
        effects2.iloc[0]["variance_native"]
    )


def test_wrong_group_size_fails_closed():
    df = _balanced_fixture().query("plant != 'W4_10'").copy()
    summary, effects = audit_iwe023_dataframe(
        df,
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        f_tolerance=100.0,
    )
    assert not bool(effects.iloc[0]["raw_effect_ready"])
    assert "n != 10" in effects.iloc[0]["reason"]
    assert not summary["raw_design_ready"].any()


def test_duplicate_plant_id_within_week_fails_closed():
    df = _balanced_fixture()
    df.loc[1, "plant"] = df.loc[0, "plant"]
    with pytest.raises(ValueError, match="unique"):
        audit_iwe023_dataframe(
            df,
            week_col="week",
            seed_set_col="seed",
            plant_id_col="plant",
            f_tolerance=100.0,
        )


def test_week_labels_can_be_source_style_strings():
    df = _balanced_fixture()
    df["week"] = df["week"].map(lambda value: f"week {value}")
    summary, _ = audit_iwe023_dataframe(
        df,
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        f_tolerance=100.0,
    )
    assert list(summary["week"]) == [1, 2, 3, 4]


def test_plant_ids_may_restart_across_weeks():
    df = _balanced_fixture()
    df["plant"] = df.groupby("week").cumcount() + 1
    summary, effects = audit_iwe023_dataframe(
        df,
        week_col="week",
        seed_set_col="seed",
        plant_id_col="plant",
        f_tolerance=100.0,
    )
    assert summary["raw_design_ready"].all()
    assert bool(effects.iloc[0]["raw_effect_ready"])
