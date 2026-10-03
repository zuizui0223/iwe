from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def derive_phase_margin(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "year",
        "synchrony_predation_sign",
        "first_flower_to_first_larva_days",
        "fruit_maturation_days",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    out = df[
        [
            "year",
            "synchrony_predation_sign",
            "first_flower_to_first_larva_days",
            "fruit_maturation_days",
        ]
    ].copy()

    out["phase_safety_margin_days"] = (
        out["first_flower_to_first_larva_days"]
        - out["fruit_maturation_days"]
    )
    out["host_can_mature_before_first_larva"] = (
        out["phase_safety_margin_days"] >= 0
    )

    expected = {
        2008: (-11.3, "positive", False),
        2009: (0.3, "negative", True),
    }
    for year, (margin, sign, mature_first) in expected.items():
        row = out.loc[out["year"].eq(year)]
        if len(row) != 1:
            raise ValueError(f"expected one row for year {year}, found {len(row)}")
        observed_margin = float(row.iloc[0]["phase_safety_margin_days"])
        if abs(observed_margin - margin) > 1e-9:
            raise ValueError(
                f"{year}: phase margin {observed_margin} != expected {margin}"
            )
        if str(row.iloc[0]["synchrony_predation_sign"]) != sign:
            raise ValueError(f"{year}: unexpected synchrony-predation sign")
        if bool(row.iloc[0]["host_can_mature_before_first_larva"]) != mature_first:
            raise ValueError(f"{year}: unexpected phase-margin classification")

    return out


def render_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, lineterminator="\n", float_format="%.1f")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/source_reconstructions/kula2012_silene_phase_lag.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/kula2012_phase_safety_margin.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.source)
    rendered = render_csv(derive_phase_margin(df))

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing phase-margin output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale phase-margin output: {args.output}")
            return 1
        print(f"Kula phase-safety margin is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote Kula phase-safety margin to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
