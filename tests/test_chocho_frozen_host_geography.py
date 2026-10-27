"""Verify fixed biological-source geography without rebuilding large upstream inputs."""
from pathlib import Path
import csv
import hashlib
import json
import math

BASE = Path(__file__).resolve().parents[1] / "data/frozen/chocho_cardamine_host_geography_v0.1"
BLOBS = {
    "new_resource_units.csv": "6fd55a3261268f4ef4a083538446a48ea083a4ed",
    "host_contributions.csv": "f5e82d5b5992344af9882a2b8f1c7959a340df73",
    "focal_host_geography_receipt.json": "d403cd7ac90ec783fec9b05ba7b1ad2aaac17613",
}


def rows(name):
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_frozen_outputs_equal_original_full_source_artifact_bytes():
    for name, expected in BLOBS.items():
        raw = (BASE / name).read_bytes()
        git_hash = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert git_hash == expected


def test_confirmed_focal_host_is_not_overcredited():
    summary = json.loads((BASE / "focal_host_geography_receipt.json").read_text())
    hosts = rows("host_contributions.csv")
    units = rows("new_resource_units.csv")
    assert len(hosts) == summary["resolved_hosts"] == 11
    assert len(units) == summary["added_butterfly_units"] == 110
    assert (summary["native_butterfly_units"], summary["contemporary_butterfly_units"]) == (162, 272)
    assert summary["source_pair_status"] == "confirmed_exact_in_chocho_HOSTS_sidecar"
    assert summary["strict_h1_effects_created"] == 0
    assert not summary["regional_pheno_observed"]
    assert not summary["regional_host_use_observed"]
    assert math.isclose(sum(float(x["fractional_added_unit_credit"]) for x in hosts), 110, abs_tol=1e-8)
    focal = next(x for x in hosts if x["accepted_name"] == "Cardamine pratensis")
    assert (focal["native_host_units"], focal["contemporary_host_units"]) == ("75", "78")
    assert (focal["butterfly_added_units_covered"], focal["butterfly_added_units_exclusively_covered"]) == ("2", "0")
    assert float(focal["fractional_added_unit_credit"]) == 0.4
    assert {x["wgsrpd3_unit"] for x in units if x["focal_host_status"] == "available"} == {"NZN", "NZS"}
    assert all(x["focal_exclusively_supplies_unit"] == "False" for x in units)


def test_other_hosts_dominate_added_resource_credit():
    hosts = {x["accepted_name"]: x for x in rows("host_contributions.csv")}
    b, c = hosts["Brassica rapa"], hosts["Capsella bursa-pastoris"]
    assert (b["butterfly_added_units_covered"], b["butterfly_added_units_exclusively_covered"]) == ("82", "30")
    assert (c["butterfly_added_units_covered"], c["butterfly_added_units_exclusively_covered"]) == ("78", "21")
    assert math.isclose(float(b["fractional_added_unit_credit"]) + float(c["fractional_added_unit_credit"]), 92.2, abs_tol=1e-9)
