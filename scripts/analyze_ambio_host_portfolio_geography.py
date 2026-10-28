#!/usr/bin/env python3
"""Build WCVP v13 counterfactual host-portfolios for IWE × chocho."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd
from iwe.host_portfolio_sensitivity import build_portfolio_sensitivity

DEFAULT_BASELINE = Path(
    "data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv"
)
PINS = {
    "chocho": "df6f920a37c7e86a878d9f6375bb4454128b5d66",
    "WCVP": "65bed76bae9d644ccb6ad200c05f9f5071d89e05",
    "observed_egg_reference_DOI": "10.1007/s13280-014-0602-z",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _encode(v):
    if hasattr(v, "item"):
        return v.item()
    raise TypeError(f"Not JSON serializable: {type(v)}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wcvp-presence", type=Path, required=True)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args()
    frame = pd.read_csv(args.wcvp_presence, dtype=str, keep_default_na=False)
    baseline = pd.read_csv(args.baseline, dtype=str, keep_default_na=False)
    scenarios, regions, receipt = build_portfolio_sensitivity(frame, baseline)
    receipt["pinned_upstream"] = PINS
    receipt["input_sha256"] = {
        "WCVP_host_region_presence": _sha(args.wcvp_presence),
        "11_frozen_HOSTS_host_metrics": _sha(args.baseline),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    scenarios.to_csv(args.out_dir / "candidate_portfolio_scenarios.csv", index=False)
    regions.to_csv(args.out_dir / "added_region_transitions.csv", index=False)
    (args.out_dir / "portfolio_sensitivity_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False,
                   default=_encode) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2,
                     allow_nan=False, default=_encode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
