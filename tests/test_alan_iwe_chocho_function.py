import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

from iwe.alan_function_bridge import (
    analyze_lu_night_channels, analyze_boom_spectral_nursery,
    build_three_repo_receipt, check_iwe_taxon_relation,
)

ROOT = Path(__file__).resolve().parents[1]
LU = ROOT / "data/registry/alan_lu2026_night_visits_v01.csv"
BOOM = ROOT / "data/registry/alan_boom2020_spectrum_nursery_v01.csv"
IWE = ROOT / "data/registry/replication_candidates.csv"


def load():
    return [pd.read_csv(p, dtype=str, keep_default_na=False)
            for p in (LU, BOOM, IWE)]


def test_lu_only_visits_and_break_even_pollen_ratio_is_hypothetical():
    lu, _, _ = load()
    rows, scenarios, receipt = analyze_lu_night_channels(lu)
    assert len(rows) == 3
    assert receipt["lepidoptera_visits_lost"] == 481
    assert receipt["diptera_visits_gained"] == 97
    assert receipt["count_only_substitution_share"] == pytest.approx(97 / 481)
    assert receipt["hypothetical_per_visit_fly_effectiveness_break_even"] == pytest.approx(481 / 97)
    one = scenarios.loc[
        scenarios["assumed_fly_over_lepidoptera_pollen_effectiveness_per_visit"] == 1.
    ].iloc[0]
    assert one["lit_over_dark_two_guild_hypothetical_ratio"] == pytest.approx(508 / 892)
    assert not bool(one["is_real_measured_pollen_delivery"])
    assert receipt["other_author_worksheet_can_be_subtracted_from_this_one"] is False
    assert receipt["strict_h1_effects_created"] == 0


def test_boom_all_light_spectra_rounded_seed_formula_and_significance_ceiling():
    _, boom, _ = load()
    table, receipt = analyze_boom_spectral_nursery(boom)
    assert set(table["light_spectrum"]) == {"dark", "green", "red", "white"}
    components = table.set_index("light_spectrum")
    assert components.loc["dark", "fruit_set_fraction"] == pytest.approx(.73)
    assert components.loc["green", "fruit_infestation_fraction"] == pytest.approx(.53)
    assert components.loc["green", "uninfested_ovule_fertilized_fraction"] == pytest.approx(.43)
    assert components.loc["green", "model_seeds_from_rounded_components"] == pytest.approx(
        .75 * .47 * .43 * 404
    )
    assert receipt["green_over_dark_rounded_component_product"] == pytest.approx(
        (.75 * .47 * .43) / (.73 * .72 * .56)
    )
    assert receipt["reported_net_seed_anova_p"] == pytest.approx(.63)
    assert receipt["source_supports_significant_net_seed_reduction"] is False
    assert not table["is_actual_counted_mature_seed_observation"].any()
    assert not table["interpretable_as_causal_mediation"].any()
    assert receipt["strict_h1_effects_created"] == 0


def test_taxonomic_relatedness_does_not_promote_historical_iwe_candidate():
    _, _, candidates = load()
    relation = check_iwe_taxon_relation(candidates)
    assert relation["iwe_candidate_id"] == "MIX002_BIERE_HONDERS_1996"
    assert relation["exact_shared_insect"] == "Hadena bicruris"
    assert "Silene latifolia subsp. alba" in relation["taxonomy"]
    assert relation["same_population_time_exposure_unit"] is False
    assert relation["alan_measures_iwe_strict_seasonal_partner_window"] is False
    assert relation["promote_alan_to_iwe_strict_h1"] is False


def test_no_global_causal_alan_chocho_effect_or_iwe_meta_promotion():
    lu, boom, candidates = load()
    _, _, _, report = build_three_repo_receipt(lu, boom, candidates)
    assert report["source_programmes"] == 2
    assert report["chocho"]["same_species_site_year_alan_experiment"] is False
    assert report["chocho"]["cross_scale_model_evaluable"] is False
    assert report["diel_night_visits_is_not_day_of_year_seasonal_overlap"]
    assert report["satellite_annual_VIIRS_is_not_equivalent_to_ground_lux"]
    assert report["seasonal_flower_and_adult_overlap_measured_same_unit"] is False
    assert report["light_dependent_pollen_transfer_measured_for_substitution"] is False
    assert report["new_iwe_h1_effects"] == 0
    assert report["original_chocho_paper_unchanged"]


def test_unverified_subgroup_and_nonfrozen_spectra_fail_closed():
    lu, boom, candidates = load()
    bad = lu.copy()
    bad.loc[0, "source_sheet"] = "species visitation"
    with pytest.raises(ValueError, match="source_sheet"):
        build_three_repo_receipt(bad, boom, candidates)
    bad = lu.copy()
    bad.loc[bad["guild"] == "Diptera", "lit_visits"] = "1000"
    with pytest.raises(ValueError, match="smaller than recorded subset"):
        analyze_lu_night_channels(bad)
    bad = boom.copy()
    bad.loc[bad["light_spectrum"] == "green", "fruit_infestation_fraction"] = "0.15"
    with pytest.raises(ValueError, match="published spectrum data drift"):
        analyze_boom_spectral_nursery(bad)
    bad = candidates.copy()
    bad.loc[bad["candidate_id"] == "MIX002_BIERE_HONDERS_1996", "status"] = "ready"
    with pytest.raises(ValueError, match="IWE source/partner timing gate"):
        check_iwe_taxon_relation(bad)


def test_cli_copies_only_aggregates_and_audits_input_sha(tmp_path):
    res = subprocess.run(
        [sys.executable, str(ROOT / "scripts/audit_alan_iwe_chocho_function.py"),
         "--output-dir", str(tmp_path)],
        cwd=ROOT, text=True, capture_output=True
    )
    assert res.returncode == 0, res.stderr
    receipt = json.loads((tmp_path / "mechanism_bridge_receipt.json").read_text())
    assert len(receipt["input_sha256"]) == 3
    assert receipt["new_iwe_h1_effects"] == 0
    assert receipt["original_iwe_meta_claim_unchanged"] is True
    assert receipt["pooled_meta_effect_claimed"] is False
    assert len(pd.read_csv(tmp_path / "lu2026_night_visit_composition.csv")) == 3
    assert len(pd.read_csv(tmp_path / "lu2026_hypothetical_fly_effectiveness.csv")) == 7
    assert len(pd.read_csv(tmp_path / "boom2020_spectral_nursery_components.csv")) == 4
