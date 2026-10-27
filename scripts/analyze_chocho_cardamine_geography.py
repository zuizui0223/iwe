#!/usr/bin/env python3
"""Run the IWE × chocho pinned Cardamine host-region decomposition."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd
from iwe.host_geography import analyze_focal_host_geography

PINS = {
    "chocho": "df6f920a37c7e86a878d9f6375bb4454128b5d66",
    "HOSTS": "808e0b869f9ec1adf8efff87cf6a395adda103e0",
    "WCVP": "65bed76bae9d644ccb6ad200c05f9f5071d89e05",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-pairs", type=Path, required=True)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--contemporary", type=Path, required=True)
    parser.add_argument("--chocho-metrics", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    files = {
        "HOSTS_resolved_pairs": args.host_pairs,
        "WCVP_native": args.native,
        "WCVP_contemporary": args.contemporary,
        "chocho_frozen_metrics": args.chocho_metrics,
    }
    dfs = {name: pd.read_csv(path, dtype=str, keep_default_na=False)
           for name, path in files.items()}
    receipt, hosts, units = analyze_focal_host_geography(
        pairs=dfs["HOSTS_resolved_pairs"],
        native_units=dfs["WCVP_native"],
        contemporary_units=dfs["WCVP_contemporary"],
        species_metrics=dfs["chocho_frozen_metrics"],
    )
    receipt["sources_pinned_to_commits"] = PINS
    receipt["input_sha256"] = {key: sha256(value) for key, value in files.items()}
    receipt["analysis_status"] = "pair_resolved_potential_geography_only"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "focal_host_geography_receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    hosts.to_csv(args.output_dir / "host_contributions.csv", index=False)
    units.to_csv(args.output_dir / "new_resource_units.csv", index=False)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
