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


def test_missing_original_file_fails_without_anonymous_network_calls(tmp_path):
    import json
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/acquire_toftegaard_dryad.py"),
         "--output-dir", str(tmp_path)],
        cwd=ROOT, text=True, capture_output=True,
    )
    assert result.returncode == 2
    receipt = json.loads((tmp_path / "dryad_retrieval_audit.json").read_text())
    assert receipt["retrieval_status"] == "auth_required_no_input"
    assert receipt["source_data_rows"] == 0
    assert receipt["strict_h1_effects_created"] == 0
    assert not (tmp_path / "toftegaard_2018_plant_phenology.txt").exists()


def test_local_original_source_is_hashed_without_claiming_real_field_data(tmp_path):
    import json
    original = tmp_path / "provided-source.txt"
    content = b"region,year,stage,egg\n" + (b"site_a,2012,2,0\n" * 5000)
    original.write_bytes(content)
    destination = tmp_path / "audit"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/acquire_toftegaard_dryad.py"),
         "--source-file", str(original), "--output-dir", str(destination)],
        cwd=ROOT, text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    receipt = json.loads((destination / "dryad_retrieval_audit.json").read_text())
    assert receipt["retrieval_status"] == "supplied_input_schema_pending"
    assert receipt["sha256"] == hashlib.sha256(content).hexdigest()
    assert receipt["observation_fields_validated"] is False
    assert receipt["strict_h1_effects_created"] == 0
    assert (destination / "toftegaard_2018_plant_phenology.txt").read_bytes() == content
