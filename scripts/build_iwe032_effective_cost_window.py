from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_CURVES = {
    "total_egg_load",
    "active_egg_load",
    "active_high_fecundity",
    "active_medium_fecundity",
}


def build_effective_window_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(REQUIRED_CURVES - set(df["curve"]))
    if missing:
        raise ValueError(f"missing source curves: {', '.join(missing)}")

    indexed = df.set_index("curve")
    total = indexed.loc["total_egg_load"]
    active = indexed.loc["active_egg_load"]

    shift = float(active["center_z"] - total["center_z"])
    width_ratio = float(active["sigma"] / total["sigma"])
    narrowing = float(1.0 - width_ratio)
    amplitude_ratio = float(active["amplitude"] / total["amplitude"])

    return pd.DataFrame(
        [
            {
                "study_id": "IWE032",
                "dependence_id": "DEP_IWE032_CARDAMINE_DIBBINSDALE",
                "comparison": "active_vs_total_egg_load",
                "total_peak_z": float(total["center_z"]),
                "effective_peak_z": float(active["center_z"]),
                "peak_shift_z": shift,
                "total_sigma": float(total["sigma"]),
                "effective_sigma": float(active["sigma"]),
                "sigma_ratio": width_ratio,
                "relative_narrowing": narrowing,
                "amplitude_ratio": amplitude_ratio,
                "interpretation": (
                    "Host-stage filtering shifts the effective antagonist window "
                    "later and narrows it relative to all oviposition events."
                ),
            }
        ]
    )


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
        default=Path(
            "data/source_reconstructions/iwe032_cost_window_parameters.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/iwe032_effective_cost_window.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    summary = build_effective_window_summary(pd.read_csv(args.source))
    rendered = render_csv(summary)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing IWE032 output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale IWE032 output: {args.output}")
            return 1
        print(f"IWE032 effective cost window is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote IWE032 effective cost window to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
