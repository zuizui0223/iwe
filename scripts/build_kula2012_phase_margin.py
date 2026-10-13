from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def derive_phase_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Describe maturation relative to *detection*, never damage onset.

    The first observed H. ectypa larvae were typically already moving between
    flowers (ca. 10-15 mm). Observations were every 2-4 days. Therefore a
    positive margin to the first observed larva cannot establish that a fruit
    matured before feeding began.

    The +/-2 SE range below covers only uncertainty in the reported mean fruit
    maturation interval, not larval-detection error or plant-specific timing.
    """
    required = {
        "year",
        "synchrony_predation_sign",
        "first_flower_to_first_larva_days",
        "fruit_maturation_days",
        "fruit_maturation_se_days",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    if df["year"].duplicated().any():
        raise ValueError("years must be unique")
    if df["fruit_maturation_se_days"].isna().any() or (
        df["fruit_maturation_se_days"] < 0
    ).any():
        raise ValueError("fruit maturation SE must be finite and nonnegative")

    out = df[
        [
            "year",
            "synchrony_predation_sign",
            "first_flower_to_first_larva_days",
            "fruit_maturation_days",
            "fruit_maturation_se_days",
        ]
    ].copy()
    out["phase_detection_margin_days"] = (
        out["first_flower_to_first_larva_days"]
        - out["fruit_maturation_days"]
    )
    out["margin_lower_two_se_maturation_only"] = (
        out["phase_detection_margin_days"]
        - 2 * out["fruit_maturation_se_days"]
    )
    out["margin_upper_two_se_maturation_only"] = (
        out["phase_detection_margin_days"]
        + 2 * out["fruit_maturation_se_days"]
    )

    def classify(row: pd.Series) -> str:
        if row["margin_upper_two_se_maturation_only"] < 0:
            return "negative"
        if row["margin_lower_two_se_maturation_only"] > 0:
            return "positive_maturation_only"
        return "unresolved"

    out["margin_sign_maturation_only"] = out.apply(classify, axis=1)
    # Earliest larval feeding cannot be inferred from first detected mobile larva.
    out["damaging_onset_directly_observed"] = False

    expected = {
        2008: (-11.3, "positive", "negative"),
        2009: (0.3, "negative", "unresolved"),
    }
    if set(out["year"]) != set(expected):
        raise ValueError("expected exactly the source years 2008 and 2009")
    for year, (margin, sign, status) in expected.items():
        row = out.loc[out["year"].eq(year)].iloc[0]
        if abs(float(row["phase_detection_margin_days"]) - margin) > 1e-9:
            raise ValueError(f"{year}: unexpected source detection margin")
        if str(row["synchrony_predation_sign"]) != sign:
            raise ValueError(f"{year}: unexpected synchrony-predation sign")
        if str(row["margin_sign_maturation_only"]) != status:
            raise ValueError(f"{year}: unexpected uncertainty status")
    return out


def render_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, lineterminator="\n", float_format="%.2f")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/source_reconstructions/kula2012_silene_phase_lag.csv"),
    )
    # Retain the historical filename for downstream compatibility.
    # The file now explicitly labels margins as relative to first detection.
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/kula2012_phase_safety_margin.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = pd.read_csv(args.source)
    rendered = render_csv(derive_phase_margin(source))

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing phase-detection output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale phase-detection output: {args.output}")
            return 1
        print(f"Kula phase-detection margin is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote Kula phase-detection margin to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
