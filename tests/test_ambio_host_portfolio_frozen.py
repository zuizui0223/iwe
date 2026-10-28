"""Frozen verified WCVP source audit for the Anthocharis portfolio sensitivity.

Receipts were generated from pinned WCVP 65bed76 and the frozen
11-host chocho dataset on GitHub Actions run 40612290047.
This verifies source output, not successful larval host use.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/frozen/ambio_host_portfolio_wcvp_v01"
GIT_BLOBS = {
    "candidate_portfolio_scenarios.csv": "f1835ae4ac24bb3a345dec45147a12190b3bfad0",
    "source_taxon_resolution.csv": "eb15a3d1b4fe1e72d2116b6e6dcece29b920a9ce",
    "portfolio_sensitivity_receipt.json": "092ac71153d9e63fcea82432520e1efda760a4fc",
}


def _csv(name):
    with (OUT / name).open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))


def test_source_receipts_match_actual_github_action_bytes():
    for name, sha in GIT_BLOBS.items():
        b = (OUT / name).read_bytes()
        got = hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()
        assert got == sha


def test_source_pin_and_taxon_resolution_are_exact():
    receipt = json.loads((OUT / "portfolio_sensitivity_receipt.json").read_text())
    assert receipt["scenarios_tested"] == 8
    assert receipt["pinned_upstream"]["WCVP"] == "65bed76bae9d644ccb6ad200c05f9f5071d89e05"
    assert receipt["input_sha256"]["WCVP_host_region_presence"] == "9c59036831be320740b27337cf845e24db88a650d9ac3c725844125efd2cf3dc"
    assert receipt["egg_receipt_confirms_larval_suitability"] is False
    assert receipt["octoploid_cardamine_added_as_new_species"] is False
    assert receipt["new_iwe_strict_h1_effects"] == 0
    taxa = _csv("source_taxon_resolution.csv")
    assert len(taxa) == 14
    added = {x["accepted_name"]: x["accepted_plant_name_id"]
             for x in taxa if x["source_role"].startswith("observed_egg")}
    assert added == {
        "Arabis hirsuta": "2645681",
        "Arabidopsis thaliana": "2645262",
        "Noccaea caerulescens": "2381293",
    }


def test_three_candidate_sensitivity_is_entirely_due_to_arabidopsis_thaliana():
    rows = _csv("candidate_portfolio_scenarios.csv")
    assert len(rows) == 8
    original = next(x for x in rows if x["candidate_count"] == "0")
    assert (original["native_units"], original["contemporary_units"],
            original["introduced_added_units"]) == ("162", "272", "110")
    for x in rows:
        has_thaliana = "Arabidopsis thaliana" in x["added_candidate_species"]
        expected = ("168", "274", "106", "-4") if has_thaliana else ("162", "272", "110", "0")
        assert (x["native_units"], x["contemporary_units"],
                x["introduced_added_units"], x["delta_added_vs_frozen"]) == expected
        assert x["strict_h1_effects_created"] == "0"
    full = next(x for x in rows if x["candidate_count"] == "3")
    assert (full["baseline_added_now_native"], full["newly_added_after_host_extension"]) == ("4", "0")


def test_old_source_keys_include_all_four_reclassified_areas():
    rows = ROOT / "data/frozen/chocho_cardamine_host_geography_v0.1/new_resource_units.csv"
    with rows.open(newline="", encoding="utf-8") as f:
        baseline_added = {r["wgsrpd3_unit"] for r in csv.DictReader(f)}
    assert len(baseline_added) == 110
    assert {"CNY", "DJI", "MDR", "SUD"} <= baseline_added
    assert not {"CVI", "SOM"} & baseline_added
