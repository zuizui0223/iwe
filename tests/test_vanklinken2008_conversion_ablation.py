from pathlib import Path

import pandas as pd
import pytest

from scripts.build_vanklinken2008_conversion_ablation import (
    conversion_ablation,
    render_csv,
)


SOURCE = Path("data/source_reconstructions/vanklinken2008_paired_stage_diagnostic.csv")
SNAPSHOT = Path("data/derived/vanklinken2008_conversion_ablation_metrics.csv")


def test_ablation_snapshot_and_complete_candidate_space():
    output = conversion_ablation(pd.read_csv(SOURCE))
    assert len(output) == 10
    assert output["coordinate"].nunique() == 10
    assert (output["analysis_status"] == "exploratory_outcome_exposed").all()
    assert render_csv(output) == SNAPSHOT.read_text(encoding="utf-8")


def test_conversion_fraction_alone_beats_stage_times_fraction_in_this_sample():
    output = conversion_ablation(pd.read_csv(SOURCE)).set_index("coordinate")
    survival = output.loc["joint_survival_fraction", "leave_one_region_out_rmse_pp"]
    stage_filtered = output.loc["stage_joint_survival", "leave_one_region_out_rmse_pp"]
    annual = output.loc["annual_eggs", "leave_one_region_out_rmse_pp"]
    stage = output.loc["stage_eggs", "leave_one_region_out_rmse_pp"]
    assert survival < stage_filtered
    assert stage_filtered < stage < annual
    assert survival == pytest.approx(4.1079791112, abs=1e-8)
    assert stage_filtered == pytest.approx(4.9243281848, abs=1e-8)


def test_original_three_model_comparison_is_not_changed():
    output = conversion_ablation(pd.read_csv(SOURCE)).set_index("coordinate")
    old = pd.read_csv("data/derived/vanklinken2008_paired_stage_metrics.csv").set_index(
        "coordinate"
    )
    pairs = {
        "annual_ground_egg_density": "annual_eggs",
        "stage_matched_egg_density": "stage_eggs",
        "filtered_stage_exposure": "stage_joint_survival",
    }
    for old_key, new_key in pairs.items():
        for col in ("pearson_r", "leave_one_region_out_rmse_pp", "leave_one_region_out_mae_pp"):
            assert output.loc[new_key, col] == pytest.approx(old.loc[old_key, col], abs=1e-8)


def test_invalid_source_domain_fails_closed():
    df = pd.read_csv(SOURCE)
    df.loc[0, "egg_hatch_pct"] = 110
    with pytest.raises(ValueError, match="egg_hatch_pct"):
        conversion_ablation(df)
    df = pd.read_csv(SOURCE)
    df.loc[0, "region_season"] = df.loc[1, "region_season"]
    with pytest.raises(ValueError, match="unique"):
        conversion_ablation(df)
