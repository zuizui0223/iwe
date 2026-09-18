#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


VALID_STATUS = {"not_started", "in_progress", "complete", "blocked"}
REQUIRED_COMPONENTS = {"A", "B", "C", "D", "E", "F"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and summarize the frozen IWE systematic-search completion state."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/registry/search_completion_status.csv",
    )
    parser.add_argument("output", nargs="?", default="-")
    args = parser.parse_args()

    df = pd.read_csv(Path(args.input), dtype=str, keep_default_na=False)
    required = {
        "component_id",
        "component",
        "status",
        "completion_evidence",
        "next_action",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    if df["component_id"].duplicated().any():
        raise ValueError("duplicate component_id")
    if set(df["component_id"]) != REQUIRED_COMPONENTS:
        raise ValueError(
            f"component ids must be exactly {sorted(REQUIRED_COMPONENTS)}"
        )
    bad = sorted(set(df["status"]) - VALID_STATUS)
    if bad:
        raise ValueError(f"invalid search completion status: {bad}")
    if (df["completion_evidence"].str.strip() == "").any():
        raise ValueError("completion_evidence cannot be blank")
    if (df["next_action"].str.strip() == "").any():
        raise ValueError("next_action cannot be blank")

    search_closed = bool((df["status"] == "complete").all())
    payload = {
        "schema": "iwe_search_completion_v1",
        "search_closed": search_closed,
        "component_status": dict(zip(df["component_id"], df["status"], strict=True)),
        "complete_components": int((df["status"] == "complete").sum()),
        "total_components": int(len(df)),
        "remaining_components": df.loc[
            df["status"] != "complete", "component_id"
        ].tolist(),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output == "-":
        print(rendered, end="")
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")

    if search_closed:
        print("IWE systematic-search completion gate is CLOSED.")
    else:
        print(
            "IWE systematic-search completion gate is OPEN: "
            + ",".join(payload["remaining_components"])
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
