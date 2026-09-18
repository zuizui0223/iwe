#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

CLASSES = [
    "mutualist",
    "antagonist",
    "mixed_pollinating_seed_predator",
]

# Records that currently exist only in the prospective log rather than a
# screening-batch table. Keep this intentionally tiny; move records into a
# normal screening batch when a batch is created.
PROSPECTIVE_CLASS = {
    "IWE078": "antagonist",
    "IWE079": "antagonist",
    "IWE080": "antagonist",
}


def read_if_exists(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def collect_screening_rows(root: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    studies = pd.read_csv(root / "data/registry/studies.csv")
    frames.append(
        studies[
            [
                "study_id",
                "screening_status",
                "interaction_type_candidate",
            ]
        ].copy()
    )

    for path in sorted((root / "data/registry").glob("screening_batch_*.csv")):
        df = pd.read_csv(path)
        required = {
            "study_id",
            "screening_status",
            "interaction_type_candidate",
        }
        if not required.issubset(df.columns):
            continue
        frames.append(df[list(required)].copy())

    all_rows = pd.concat(frames, ignore_index=True)
    # Later batch entries supersede earlier registry snapshots for the same id.
    all_rows = all_rows.drop_duplicates("study_id", keep="last")

    prospective = pd.read_csv(root / "data/registry/prospective_search_log.csv")
    missing = prospective.loc[
        ~prospective["study_id"].isin(all_rows["study_id"])
        & prospective["study_id"].isin(PROSPECTIVE_CLASS)
    ].copy()
    if not missing.empty:
        missing["interaction_type_candidate"] = missing["study_id"].map(PROSPECTIVE_CLASS)
        missing = missing[
            ["study_id", "screening_status", "interaction_type_candidate"]
        ]
        all_rows = pd.concat([all_rows, missing], ignore_index=True)

    overrides = pd.read_csv(root / "data/registry/adjudication_overrides.csv")
    override_status = dict(
        zip(overrides["study_id"], overrides["current_status"], strict=True)
    )
    all_rows["screening_status"] = [
        override_status.get(study_id, status)
        for study_id, status in zip(
            all_rows["study_id"],
            all_rows["screening_status"],
            strict=True,
        )
    ]

    # Multi-agent records are retained in the project but are not assigned to
    # one of the three preregistered H1 classes and therefore do not enter the
    # class architecture denominator.
    return all_rows.loc[
        all_rows["interaction_type_candidate"].isin(CLASSES)
    ].reset_index(drop=True)


def programme_counts(
    path: Path,
    *,
    id_col: str = "dependence_id",
) -> dict[str, int]:
    df = pd.read_csv(path)
    return {
        cls: int(
            df.loc[df["interaction_type"] == cls, id_col]
            .dropna()
            .astype(str)
            .nunique()
        )
        for cls in CLASSES
    }


def build_architecture(root: Path) -> pd.DataFrame:
    rows = collect_screening_rows(root)

    direct_programmes = programme_counts(root / "data/extraction/direct_effects.csv")
    common_programmes = programme_counts(
        root / "data/extraction/common_scale_fisher_z.csv"
    )

    out: list[dict] = []
    for cls in CLASSES:
        part = rows.loc[rows["interaction_type_candidate"] == cls]
        statuses = part["screening_status"].fillna("").astype(str)

        strict_admitted = int((statuses == "include").sum())
        unresolved_strict = int(
            statuses.isin(["unresolved_strict", "unresolved"]).sum()
        )
        shape = int((statuses == "include_shape").sum())
        context = int((statuses == "context_only").sum())
        excluded = int((statuses == "exclude").sum())

        out.append(
            {
                "interaction_type": cls,
                "n_screened_current": int(len(part)),
                "strict_admitted_records": strict_admitted,
                "strict_quantitative_programmes_closed": direct_programmes[cls],
                "common_scale_fisher_z_programmes_closed": common_programmes[cls],
                "unresolved_possible_strict": unresolved_strict,
                "shape_lane_records": shape,
                "context_only_records": context,
                "excluded_records": excluded,
                "strict_admitted_fraction": (
                    strict_admitted / len(part) if len(part) else float("nan")
                ),
                "quantitative_closed_fraction": (
                    direct_programmes[cls] / len(part) if len(part) else float("nan")
                ),
            }
        )

    return pd.DataFrame(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the current IWE evidence-architecture summary."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default="data/derived/evidence_architecture_current.csv",
    )
    args = parser.parse_args()

    root = Path(args.root)
    out = build_architecture(root)
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(out.to_string(index=False))
    print(
        "\nCurrent-corpus diagnostic only: systematic search closure is not yet "
        "complete, so these proportions are descriptive rather than final review estimates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
