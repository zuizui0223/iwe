"""Targeted ALAN × daytime-only seed controls; source audit not field study."""
import json
from pathlib import Path
import subprocess
import sys

import pytest
from iwe.alan_daytime_carryover import (
    read_alan_derived_source, summarize_daytime_carryover,
    _gitblob, ALAN_SOURCE_GIT_BLOB,
)

HEADER = (
    "block_id,mean_dark_no_slug,mean_dark_slug,"
    "mean_lit_no_slug,mean_lit_slug,n_dark_no_slug,n_dark_slug,"
    "n_lit_no_slug,n_lit_slug\n"
)
SAMPLE = (
    HEADER +
    "T01,4,2,2,1,4,4,4,4\n"
    "C01,2,4,1,4,4,4,4,4\n"
)


def test_synthetic_original_stage_means_are_kept_separate():
    rows=read_alan_derived_source(SAMPLE.encode(),verify=False)
    result,gate=summarize_daytime_carryover(rows,verified=False)
    assert len(result)==2
    t,c=result
    assert t["species"]=="Trifolium pratense"
    assert t["no_slug_lit_dark_ratio"]==pytest.approx(.5)
    assert t["slug_lit_dark_ratio"]==pytest.approx(.5)
    assert t["equal_choice_round_lit_dark_ratio"]==pytest.approx(.5)
    assert t["slug_x_light_additive_difference_of_differences"]==pytest.approx(1)
    assert c["species"]=="Centaurea jacea"
    assert c["no_slug_lit_dark_ratio"]==pytest.approx(.5)
    assert c["slug_lit_dark_ratio"]==pytest.approx(1)
    assert c["slug_x_light_additive_difference_of_differences"]==pytest.approx(1)
    assert gate["original_n_missing_seed_outcomes"]==23
    assert gate["all_pot_level_original_observations_recovered"] is False
    assert gate["original_fully_bagged_control_flower_total"]==39


def test_wrong_source_sha_and_unknown_block_are_rejected():
    with pytest.raises(ValueError,match="pinned ALAN-derived"):
        read_alan_derived_source(SAMPLE.encode(),verify=True)
    with pytest.raises(ValueError,match="No evidence"):
        read_alan_derived_source(SAMPLE.replace("C01,","X01,").encode(),verify=False)
    with pytest.raises(ValueError,match="duplicate"):
        read_alan_derived_source((SAMPLE+"T01,4,2,2,1,4,4,4,4\n").encode(),verify=False)
    assert _gitblob(SAMPLE.encode())!=ALAN_SOURCE_GIT_BLOB


def test_zero_or_unreported_seed_pots_are_not_fabricated():
    with pytest.raises(ValueError,match="Impossible original seed"):
        read_alan_derived_source(
            SAMPLE.replace("T01,4,2,2,1,4,4,4,4","T01,4,2,2,1,0,4,4,4").encode(),
            verify=False,
        )
    with pytest.raises(ValueError,match="Impossible original seed"):
        read_alan_derived_source(
            SAMPLE.replace("C01,2,4,1,4,4,4,4,4","C01,-2,4,1,4,4,4,4,4").encode(),
            verify=False,
        )
    with pytest.raises(ValueError,match="Unrecoverable"):
        read_alan_derived_source(
            SAMPLE.replace("T01,4,2,2,1,4,4,4,4","T01,NA,2,2,1,4,4,4,4").encode(),
            verify=False,
        )


def test_the_study_does_not_identify_fly_moth_or_night_access_moderator():
    rows=read_alan_derived_source(SAMPLE.encode(),verify=False)
    result,gate=summarize_daytime_carryover(rows,verified=False)
    assert not gate["pollination_exclusively_daytime_verified_without_exception"]
    assert gate["Trifolium_bagged_control_seed_positive"]==0
    assert gate["Centaurea_bagged_control_seed_positive"]==3
    assert not gate["daylight_carryover_mechanism_identified"]
    assert not gate["focal_species_original_nocturnal_dependence_measured"]
    assert gate["strict_h1_effects_created"]==0
    assert not result[0]["source_choice_rounds_are_independent_lamp_installations"]


def test_published_group_means_cannot_be_inferred_from_one_synthetic_round():
    rows=read_alan_derived_source(SAMPLE.encode(),verify=False)
    with pytest.raises(ValueError,match="Original source has wrong choice-round"):
        summarize_daytime_carryover(rows,verified=True)


def test_run_on_pinned_original_source_when_supplied(tmp_path):
    path=tmp_path/"synthetic.csv";path.write_text(SAMPLE,encoding="utf-8")
    # Even a neatly formatted alternative source must be rejected by CLI.
    cmd=[sys.executable,"scripts/audit_alan_daytime_carryover.py",
         "--alan-derived-block-source",str(path),
         "--out-dir",str(tmp_path/"out")]
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    assert result.returncode!=0
    assert not (tmp_path/"out"/"daytime_only_seed_function_receipt.json").exists()
