from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED = {
    "fecundity_class",
    "R",
    "I_minus",
    "I_plus",
    "active_amplitude",
    "active_center_z",
    "active_sigma",
    "L",
}


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    rows = []
    for _, r in df.iterrows():
        if not (0 <= r["I_plus"] <= r["I_minus"] <= 1):
            raise ValueError(
                f"{r['fecundity_class']}: require 0 <= I_plus <= I_minus <= 1"
            )
        if not (0 <= r["L"] <= 1):
            raise ValueError(f"{r['fecundity_class']}: L must be a proportion")
        if r["active_amplitude"] < 0 or r["active_sigma"] <= 0 or r["R"] <= 0:
            raise ValueError(f"{r['fecundity_class']}: invalid positive parameter")

        baseline = float(r["R"] * r["I_minus"])
        trough = float(
            r["R"]
            * (
                r["I_minus"]
                - r["active_amplitude"]
                * r["L"]
                * (r["I_minus"] - r["I_plus"])
            )
        )
        absolute_loss = baseline - trough
        relative_loss = absolute_loss / baseline

        rows.append(
            {
                "study_id": "IWE032",
                "dependence_id": "DEP_IWE032_CARDAMINE_DIBBINSDALE",
                "fecundity_class": r["fecundity_class"],
                "effective_cost_center_z": float(r["active_center_z"]),
                "effective_cost_sigma": float(r["active_sigma"]),
                "baseline_predicted_intact_ru": baseline,
                "trough_predicted_intact_ru": trough,
                "absolute_predicted_loss": absolute_loss,
                "relative_predicted_loss": relative_loss,
                "interpretation": (
                    "Source-model fitness minimum occurs at the active-egg Gaussian "
                    "center because final intact reproduction declines monotonically "
                    "with active egg load under Equation 1."
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
        default=Path(
            "data/source_reconstructions/iwe032_effective_fitness_parameters.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/iwe032_effective_fitness_surface.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    out = build_summary(pd.read_csv(args.source))
    rendered = render_csv(out)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing IWE032 effective-fitness output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale IWE032 effective-fitness output: {args.output}")
            return 1
        print(f"IWE032 effective fitness surface is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote IWE032 effective fitness surface to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
