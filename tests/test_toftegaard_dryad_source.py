import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    import importlib.util
    target = ROOT / "scripts" / "acquire_toftegaard_dryad.py"
    spec = importlib.util.spec_from_file_location("iwe_dryad_acquire", target)
    assert spec is not None and spec.loader is not None
    instance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instance)
    return instance


def test_public_source_gate_rejects_html_binary_and_tiny_payload():
    mod = _load_module()
    assert mod.candidate_file(b"<html>" + b"a" * 80000)[0] is False
    assert mod.candidate_file(b"x" * 99)[0] is False
    assert mod.candidate_file(b"\x00" * 60000)[0] is False


def test_receipt_is_never_promoted_to_fitness_evidence():
    mod = _load_module()
    data = (b"site,year,host,egg\n" + b"X,2012,C,1\n" * 5000)
    report = mod.audit_file(data)
    assert report["doi"] == "10.5061/dryad.jp328r6"
    assert report["line_count"] == 5001
    assert report["sha256"] == hashlib.sha256(data).hexdigest()
    assert report["strict_h1_effects_created"] == 0
    assert report["independent_adult_activity_observed"] is False
    assert report["plant_reproductive_fitness_observed"] is False
