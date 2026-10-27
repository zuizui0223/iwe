"""Execute the real CLI with a small, intentionally unpinned pilot fixture."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_chocho_bridge.py"
FIXTURE = ROOT / "examples" / "chocho_pilot_species_metrics.csv"
RECEIPT = ROOT / "docs" / "CHOCHO_EXACT_MATCH_SOURCE_AUDIT_v0.1.json"


def _run(output_dir: Path, *options: str):
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--iwe-candidates",
            str(ROOT / "data" / "registry" / "replication_candidates.csv"),
            "--chocho-metrics",
            str(FIXTURE),
            "--out-dir",
            str(output_dir),
            *options,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_smoke_has_one_exact_candidate_and_no_fitness_effect(tmp_path):
    result = _run(tmp_path, "--expected-chocho-blob", "none")
    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "bridge_status.json").read_text())
    assert report["registry_candidate_rows"] == 50
    assert report["chocho_metric_species"] == 1
    assert report["exact_butterfly_candidate_matches"] == 1
    assert report["sidecar_pair_confirmed_rows"] == 0
    assert report["regional_temporal_proxy_rows"] == 0
    assert report["chocho_metrics_pinned"] is False
    assert report["iwe_strict_h1_effects_created"] == 0
    assert report["claim_support_declared"] is False
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "bridge_status.json",
        "candidate_resource_crosswalk.csv",
    ]


def test_cli_rejects_pretending_fixture_is_pinned_chocho(tmp_path):
    result = _run(tmp_path)
    assert result.returncode != 0
    assert "chocho blob mismatch" in result.stderr
    assert not (tmp_path / "bridge_status.json").exists()


def test_pinned_cross_repository_receipt_preserves_evidence_boundary():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["source_git_blobs"]["chocho"] == (
        "9f83d2d9ac8e46f1cfd4ded572c7a023273503dd"
    )
    assert receipt["candidate_rows"] == 50
    assert receipt["chocho_species_rows"] == 239
    assert receipt["exact_candidate_species_matches"] == 1
    row = receipt["matches"][0]
    assert row["animal_taxon"] == "Anthocharis cardamines"
    assert row["resource_metrics"]["native_resource_units"] == 162
    assert row["resource_metrics"]["contemporary_resource_units"] == 272
    assert row["resource_metrics"]["introduced_added_units"] == 110
    assert receipt["host_pair_confirmation"].startswith("not_checked")
    assert receipt["temporal_phenophase_rows"] == 0
    assert receipt["strict_h1_effects_created"] == 0
    assert not receipt["claim_support_declared"]
