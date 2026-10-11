from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr


EXPECTED_PLOTS = ["HA", "HL", "HC", "KD", "HD"]
OUTCOMES = {
    "initial_fruit_set": "initial_fruit_set_mean",
    "final_fruit_set": "final_fruit_set_mean",
    "intact_fruit_number": "intact_fruit_number_mean",
}


def build_plot_rank_landscape(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "plot",
        "phenology_rank_early_to_late",
        "initial_fruit_set_mean",
        "final_fruit_set_mean",
        "intact_fruit_number_mean",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    ordered = df.sort_values("phenology_rank_early_to_late").reset_index(drop=True)
    if ordered["plot"].tolist() != EXPECTED_PLOTS:
        raise ValueError(
            "plot phenology order must reproduce Figure 1: "
            + " < ".join(EXPECTED_PLOTS)
        )
    if ordered["phenology_rank_early_to_late"].tolist() != [1, 2, 3, 4, 5]:
        raise ValueError("phenology ranks must be exactly 1..5")

    rows = []
    for outcome, column in OUTCOMES.items():
        rho, p_value = spearmanr(
            ordered["phenology_rank_early_to_late"],
            ordered[column],
        )
        rows.append(
            {
                "study_id": "IWE011",
                "dependence_id": "DEP_PEUCEDANUM_KUDO_PROGRAM",
                "analysis": "plot_rank_spearman",
                "timing_axis": "earlier_to_later_population_flowering",
                "outcome": outcome,
                "n_plots": len(ordered),
                "spearman_rho": float(rho),
                "p_value_two_sided": float(p_value),
                "inferential_status": "descriptive_five_plot_association",
                "notes": (
                    "Plot is the analysis unit. Plant observation counts are not "
                    "used as timing-exposure replication."
                ),
            }
        )
    return pd.DataFrame(rows)


def render_csv(df: pd.DataFrame) -> str:
    return df.to_csv(
        index=False,
        lineterminator="\n",
        float_format="%.10f",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/source_reconstructions/iwe011_plot_table1.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/iwe011_plot_rank_landscape.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    effects = build_plot_rank_landscape(pd.read_csv(args.source))
    rendered = render_csv(effects)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing IWE011 output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale IWE011 output: {args.output}")
            return 1
        print(f"IWE011 plot-rank landscape is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote IWE011 plot-rank landscape to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
