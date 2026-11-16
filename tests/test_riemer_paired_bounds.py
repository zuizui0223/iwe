from copy import deepcopy
from pathlib import Path

import pandas as pd
import pytest

from iwe.riemer_paired_bounds import (
    exact_conditional_mcnemar_p, published_margins_bounds,
    reconstruct_counts, render_bounds,
)


def test_published_source_margins_are_unambiguously_eighty_eight_fields():
    df = pd.read_csv("data/source_reconstructions/riemer2024_pea_moth_prediction.csv")
    rows = {r["model"]: r for r in df.to_dict("records") if r["model"] in {"M1", "M3"}}
    m1 = reconstruct_counts(rows["M1"])
    m3 = reconstruct_counts(rows["M3"])
    assert m1 == {"correct": 75, "overestimated": 2, "underestimated": 11}
    assert m3 == {"correct": 84, "overestimated": 1, "underestimated": 3}


def test_enumerates_all_and_only_paired_correctness_tables_consistent_with_source():
    s = published_margins_bounds()
    assert s["n_fields"] == 88
    assert s["m3_minus_m1_correct"] == 9
    assert s["m3_minus_m1_underestimated"] == -8
    assert s["rmse_reduction_pct"] == pytest.approx(20.0)
    pairs = s["all_compatible_2x2_correctness_tables"]
    assert len(pairs) == 5
    assert [r["both_wrong"] for r in pairs] == list(range(5))
    for row in pairs:
        assert sum(row[k] for k in (
            "both_wrong", "m1_wrong_m3_right", "m1_right_m3_wrong", "both_right"
        )) == 88
        assert row["both_wrong"] + row["m1_wrong_m3_right"] == 13
        assert row["both_wrong"] + row["m1_right_m3_wrong"] == 4
        assert row["m1_wrong_m3_right"] - row["m1_right_m3_wrong"] == 9
    assert s["conditional_p_min"] == pytest.approx(0.00390625)
    assert s["conditional_p_max"] == pytest.approx(0.049041748046875)
    assert s["forecast_significance_identified"] is False
    assert s["year_blocked_validation_available"] is False
    assert s["effective_stage_test"] is False


def test_exact_conditional_tail_is_two_sided():
    assert exact_conditional_mcnemar_p(9, 0) == pytest.approx(0.00390625)
    assert exact_conditional_mcnemar_p(13, 4) == pytest.approx(0.049041748046875)
    assert exact_conditional_mcnemar_p(0, 0) == 1.0
    with pytest.raises(ValueError):
        exact_conditional_mcnemar_p(-1, 4)


def test_tampered_published_margins_fail_closed():
    source = pd.read_csv("data/source_reconstructions/riemer2024_pea_moth_prediction.csv")
    row = source[source["model"].eq("M1")].iloc[0].to_dict()
    row["correct_pct"] = 86.5
    with pytest.raises(ValueError, match="unambiguous"):
        reconstruct_counts(row)
    row = source[source["model"].eq("M1")].iloc[0].to_dict()
    row["underestimated_pct"] = 11.36
    with pytest.raises(ValueError, match="do not sum"):
        reconstruct_counts(row)


def test_render_has_unidentifiable_field_join_warning_and_is_fresh():
    txt = render_bounds()
    assert "no synthetic field records" in txt
    assert "not a new reported inferential p-value" in txt
    assert "4.85" in txt and "4.70" in txt
    assert Path("docs/RIEMER2024_PAIRED_CLASSIFICATION_BOUNDS.md").read_text(encoding="utf-8") == txt
