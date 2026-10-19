from __future__ import annotations

"""Outcome-exposed, exploratory single-predictor ablation.

Models were added after inspecting the seven final seed-predation outcomes.
LOORO here is a descriptive stress test, not a nested model-selection CV,
independent validation set, or prospective forecast.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE = Path("data/source_reconstructions/vanklinken2008_paired_stage_diagnostic.csv")
OUTPUT = Path("data/derived/vanklinken2008_conversion_ablation_metrics.csv")

# These are numerical checksums, not prior predictions or selection rules.
EXPECTED_RMSE = {
    "annual_eggs": 20.5841932718,
    "stage_eggs": 19.9286407547,
    "nonparasitized_fraction": 4.7194997141,
    "hatch_fraction": 15.8299035679,
    "joint_survival_fraction": 4.1079791112,
    "annual_nonparasitized": 10.9241032570,
    "stage_nonparasitized": 7.6575682328,
    "stage_hatched": 6.9843637109,
    "annual_joint_survival": 8.1766460327,
    "stage_joint_survival": 4.9243281848,
}


def _held_region_out_predictions(
    x: np.ndarray, y: np.ndarray, region: np.ndarray
) -> np.ndarray:
    """Same unbounded one-predictor OLS and same region folds as original audit."""
    pred = np.empty_like(y, dtype=float)
    for held in np.unique(region):
        test = region == held
        train = ~test
        X = np.column_stack([np.ones(train.sum()), x[train]])
        beta, *_ = np.linalg.lstsq(X, y[train], rcond=None)
        pred[test] = beta[0] + beta[1] * x[test]
    return pred


def conversion_ablation(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "region",
        "region_season",
        "annual_ground_egg_density",
        "stage_matched_egg_density",
        "egg_parasitism_pct",
        "egg_hatch_pct",
        "observed_seed_predation_pct",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    if len(df) != 7 or df["region"].nunique() != 4:
        raise ValueError("expected 7 region-season records from 4 regions")
    if df["region_season"].duplicated().any():
        raise ValueError("region-season IDs must be unique")
    if df[list(required - {"region", "region_season"})].isna().any().any():
        raise ValueError("source columns may not contain missing values")
    for pct in ("egg_parasitism_pct", "egg_hatch_pct", "observed_seed_predation_pct"):
        if not df[pct].between(0, 100).all():
            raise ValueError(f"{pct} must be between 0 and 100")

    annual = df["annual_ground_egg_density"].to_numpy(dtype=float)
    stage = df["stage_matched_egg_density"].to_numpy(dtype=float)
    nonpar = 1 - df["egg_parasitism_pct"].to_numpy(dtype=float) / 100
    hatch = df["egg_hatch_pct"].to_numpy(dtype=float) / 100
    survival = nonpar * hatch

    # Full exploration set: do not retain only the winning comparator.
    models = {
        "annual_eggs": annual,
        "stage_eggs": stage,
        "nonparasitized_fraction": nonpar,
        "hatch_fraction": hatch,
        "joint_survival_fraction": survival,
        "annual_nonparasitized": annual * nonpar,
        "stage_nonparasitized": stage * nonpar,
        "stage_hatched": stage * hatch,
        "annual_joint_survival": annual * survival,
        "stage_joint_survival": stage * survival,
    }
    y = df["observed_seed_predation_pct"].to_numpy(dtype=float)
    region = df["region"].to_numpy(dtype=str)

    records = []
    for name, x in models.items():
        pearson = float(pd.Series(x).corr(pd.Series(y)))
        predicted = _held_region_out_predictions(x, y, region)
        rmse = float(np.sqrt(np.mean((predicted - y) ** 2)))
        mae = float(np.mean(np.abs(predicted - y)))
        if not np.isclose(rmse, EXPECTED_RMSE[name], atol=1e-8, rtol=0):
            raise ValueError(f"{name}: source checksum changed, RMSE={rmse}")
        records.append(
            {
                "coordinate": name,
                "n_region_seasons": int(len(df)),
                "n_regions": int(df["region"].nunique()),
                "pearson_r": pearson,
                "leave_one_region_out_rmse_pp": rmse,
                "leave_one_region_out_mae_pp": mae,
                "analysis_status": "exploratory_outcome_exposed",
            }
        )
    return pd.DataFrame(records)


def render_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, lineterminator="\n", float_format="%.10f")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render_csv(conversion_ablation(pd.read_csv(args.source)))
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: missing or stale ablation: {args.output}")
            return 1
        print(f"Conversion ablation is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote outcome-exposed conversion ablation: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
