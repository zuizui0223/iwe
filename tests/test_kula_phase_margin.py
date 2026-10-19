from pathlib import Path

import pandas as pd
import pytest

from scripts.build_kula2012_phase_margin import (
    derive_phase_margin,
    render_csv,
)


SOURCE = Path("data/source_reconstructions/kula2012_silene_phase_lag.csv")
DERIVED = Path("data/derived/kula2012_phase_safety_margin.csv")


def test_generated_detection_margin_matches_registry():
    df = pd.read_csv(SOURCE)
    actual = derive_phase_margin(df)
    assert DERIVED.read_text(encoding="utf-8") == render_csv(actual)


def test_zero_crossing_not_promoted_to_safe_hardening_threshold():
    output = derive_phase_margin(pd.read_csv(SOURCE)).set_index("year")
    assert output.loc[2008, "margin_sign_maturation_only"] == "negative"
    assert output.loc[2009, "margin_sign_maturation_only"] == "unresolved"
    assert output.loc[2009, "margin_lower_two_se_maturation_only"] < 0
    assert output.loc[2009, "margin_upper_two_se_maturation_only"] > 0
    assert not output["damaging_onset_directly_observed"].any()
    assert "host_can_mature_before_first_larva" not in output.columns


def test_bad_maturation_se_fails_closed():
    df = pd.read_csv(SOURCE)
    df.loc[df["year"].eq(2009), "fruit_maturation_se_days"] = -0.1
    with pytest.raises(ValueError, match="fruit maturation SE"):
        derive_phase_margin(df)
