#!/usr/bin/env python3
"""Build an auditable candidate crosswalk with chocho's frozen resource metrics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from iwe.chocho_bridge import (
    build_candidate_resource_crosswalk,
    screen_spatiotemporal_windows,
)

CHOCHO_PINNED_COMMIT = "df6f920a37c7e86a878d9f6375bb4454128b5d66"
CHOCHO_METRICS_BLOB_SHA1 = "9f83d2d9ac8e46f1cfd4ded572c7a023273503dd"


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-match exact butterfly names; no promotion into strict H1."
    )
    parser.add_argument(
        "--iwe-candidates", type=Path,
        default=Path("data/registry/replication_candidates.csv")
    )
    parser.add_argument("--chocho-metrics", type=Path, required=True)
    parser.add_argument(
        "--expected-chocho-blob", default=CHOCHO_METRICS_BLOB_SHA1,
        help="Git blob SHA-1 of exact chocho metrics; use 'none' only for explicitly nonfrozen diagnostics"
    )
    parser.add_argument("--hosts-sidecar", type=Path)
    parser.add_argument("--seasonal-windows", type=Path)
    parser.add_argument("--allow-synthetic-windows", action="store_true")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.seasonal_windows is not None and args.hosts_sidecar is None:
        parser.error("--seasonal-windows requires --hosts-sidecar to confirm the focal host pair")

    data = args.chocho_metrics.read_bytes()
    blob_sha = _git_blob_sha1(data)
    expected = args.expected_chocho_blob.strip().lower()
    if expected != "none" and blob_sha != expected:
        parser.error(
            f"chocho blob mismatch: expected {expected}, found {blob_sha}; "
            "do not silently substitute a different dataset"
        )

    candidate_data = args.iwe_candidates.read_bytes()
    candidates = pd.read_csv(args.iwe_candidates)
    metrics = pd.read_csv(args.chocho_metrics)
    sidecar = pd.read_csv(args.hosts_sidecar) if args.hosts_sidecar else None
    crosswalk = build_candidate_resource_crosswalk(candidates, metrics, sidecar)
    windows = None
    if args.seasonal_windows:
        windows = screen_spatiotemporal_windows(
            pd.read_csv(args.seasonal_windows),
            crosswalk,
            allow_synthetic=args.allow_synthetic_windows,
        )

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    crosswalk.to_csv(out / "candidate_resource_crosswalk.csv", index=False)
    if windows is not None:
        windows.to_csv(out / "potential_phenophase_overlap.csv", index=False)

    payload = {
        "schema": "iwe_chocho_bridge_v0.1",
        "status": "potential_window_screening_only" if windows is not None else "geography_only",
        "iwe_registry_sha256": hashlib.sha256(candidate_data).hexdigest(),
        "chocho_metrics_sha256": hashlib.sha256(data).hexdigest(),
        "chocho_metrics_git_blob_sha1": blob_sha,
        "chocho_reference_commit_if_pinned": (
            CHOCHO_PINNED_COMMIT if blob_sha == CHOCHO_METRICS_BLOB_SHA1 else None
        ),
        "chocho_metrics_pinned": blob_sha == CHOCHO_METRICS_BLOB_SHA1,
        "registry_candidate_rows": int(len(candidates)),
        "chocho_metric_species": int(len(metrics)),
        "exact_butterfly_candidate_matches": int(len(crosswalk)),
        "sidecar_pair_confirmed_rows": int(
            (crosswalk["host_pair_status"] == "confirmed_in_hosts_sidecar").sum()
        ),
        "regional_temporal_proxy_rows": int(len(windows)) if windows is not None else 0,
        "potential_overlap_is_not_realized_interaction": True,
        "species_geography_is_all_hosts_not_focal_host": True,
        "iwe_strict_h1_effects_created": 0,
        "claim_support_declared": False,
    }
    (out / "bridge_status.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"Crosswalk: {len(crosswalk)} exact matches; "
        f"{payload['sidecar_pair_confirmed_rows']} confirmed source host pairs; "
        f"{payload['regional_temporal_proxy_rows']} seasonal proxy rows; "
        "no strict-H1 effects created."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
