#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


FAMILIES = [
    "access",
    "access_alignment",
    "uncertainty",
    "dependence",
    "effect_recovery",
    "source_eligibility",
    "source_eligibility_net_outcome",
    "shape_uncertainty",
]


def build_summary(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "study_id",
        "interaction_type",
        "primary_gate_gain_if_closed",
        "source_eligible",
        "blocker_family",
        "priority",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing blocker-summary columns: {sorted(missing)}")

    unknown = sorted(set(df["blocker_family"].dropna()) - set(FAMILIES))
    if unknown:
        raise ValueError(f"unknown blocker_family: {unknown}")

    rows: list[dict] = []
    for (interaction_type, blocker_family), part in df.groupby(
        ["interaction_type", "blocker_family"], dropna=False
    ):
        rows.append(
            {
                "interaction_type": interaction_type,
                "blocker_family": blocker_family,
                "n_open_blockers": int(len(part)),
                "n_source_eligible": int(
                    part["source_eligible"].astype(str).str.lower().eq("true").sum()
                ),
                "n_gate_changing_if_closed": int(
                    pd.to_numeric(
                        part["primary_gate_gain_if_closed"], errors="raise"
                    ).sum()
                ),
                "n_priority1": int(
                    pd.to_numeric(part["priority"], errors="raise").eq(1).sum()
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            ["interaction_type", "n_open_blockers", "blocker_family"],
            ascending=[True, False, True],
        )
        .reset_index(drop=True)
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize the current IWE strict-evidence blocker families."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/registry/strict_blockers.csv",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="data/derived/strict_blocker_summary_current.csv",
    )
    args = parser.parse_args()

    out = build_summary(Path(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(out.to_string(index=False))
    print(
        "\nCurrent execution bottlenecks only: these counts summarize unresolved "
        "strict candidates and are not final systematic-review failure rates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
