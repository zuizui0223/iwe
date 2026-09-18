#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from iwe.schema import INTERACTION_TYPES


REQUIRED = {
    "study_id",
    "interaction_type",
    "primary_gate_gain_if_closed",
    "source_eligible",
    "blocker_type",
    "reconstruction_state",
    "target_effect_family",
    "priority",
    "next_action",
    "terminal_if_unrecovered",
}


def build_queue(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"missing blocker columns: {sorted(missing)}")
    if df["study_id"].duplicated().any():
        raise ValueError("duplicate study_id in strict blocker queue")

    unknown = sorted(set(df["interaction_type"].dropna()) - INTERACTION_TYPES)
    if unknown:
        raise ValueError(f"unknown interaction_type: {unknown}")

    df["priority"] = pd.to_numeric(df["priority"], errors="raise").astype(int)
    if (~df["priority"].between(1, 3)).any():
        raise ValueError("priority must be 1, 2, or 3")

    df["primary_gate_gain_if_closed"] = pd.to_numeric(
        df["primary_gate_gain_if_closed"], errors="raise"
    ).astype(int)
    if (~df["primary_gate_gain_if_closed"].isin([0, 1])).any():
        raise ValueError("primary_gate_gain_if_closed must be 0 or 1")

    eligible = df["source_eligible"].astype(str).str.lower()
    if (~eligible.isin(["true", "false"])).any():
        raise ValueError("source_eligible must be true/false")
    df["source_eligible"] = eligible.eq("true")

    # Rank source-eligible programme gains first. This rank is execution value,
    # not a biological effect ranking.
    df["gate_value"] = (
        100 * df["primary_gate_gain_if_closed"]
        + 10 * df["source_eligible"].astype(int)
        + (4 - df["priority"])
    )
    return df.sort_values(
        ["gate_value", "priority", "interaction_type", "study_id"],
        ascending=[False, True, True, True],
    ).reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the current IWE strict-evidence blocker queue."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/registry/strict_blockers.csv",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="data/derived/strict_blocker_queue_current.csv",
    )
    args = parser.parse_args()

    queue = build_queue(Path(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    queue.to_csv(output, index=False)

    print(queue[
        [
            "study_id",
            "interaction_type",
            "primary_gate_gain_if_closed",
            "source_eligible",
            "blocker_type",
            "priority",
            "gate_value",
        ]
    ].to_string(index=False))
    print(
        "\nExecution ranking only: gate_value prioritizes source-eligible "
        "independent programmes that can change the current inference gate; "
        "it is not an ecological evidence score."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
