#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.screening_triage import build_source_type_audit


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit source types among unscreened frozen-query records."
    )
    parser.add_argument(
        "--ledger",
        default="data/registry/frozen_database_screening_ledger.csv",
    )
    parser.add_argument(
        "--summary",
        default="data/derived/frozen_screening_source_type_audit_current.csv",
    )
    parser.add_argument(
        "--queue",
        default="data/derived/frozen_screening_source_type_queue_current.csv",
    )
    parser.add_argument(
        "--json",
        default="data/derived/frozen_screening_source_type_summary_current.json",
    )
    args = parser.parse_args()

    ledger = pd.read_csv(args.ledger)
    summary, queue = build_source_type_audit(ledger)

    summary_path = Path(args.summary)
    queue_path = Path(args.queue)
    json_path = Path(args.json)
    for path in [summary_path, queue_path, json_path]:
        path.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(summary_path, index=False)
    queue.to_csv(queue_path, index=False)

    payload = {
        "schema": "iwe_frozen_screening_source_type_audit_v1",
        "unscreened_records": int(queue["record_key"].nunique()),
        "priority_counts": {
            str(k): int(v)
            for k, v in queue.groupby("screening_priority")["record_key"].nunique().items()
        },
        "source_type_bucket_counts": {
            str(k): int(v)
            for k, v in queue.groupby("source_type_bucket")["record_key"].nunique().items()
        },
        "note": (
            "Source-type triage proposes the next screening action only. "
            "It never writes include/context/exclude decisions."
        ),
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2, sort_keys=True))
    print("\nUnscreened source-type summary:")
    print(summary.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
