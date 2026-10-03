from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED = {
    "annual_ground_egg_density": {
        "pearson_r": 0.4762529941,
        "spearman_r": 0.5714285714,
        "loo_rmse_pp": 12.3121077849,
        "loo_mae_pp": 10.5200174021,
    },
    "stage_matched_egg_density": {
        "pearson_r": 0.5964140926,
        "spearman_r": 0.5714285714,
        "loo_rmse_pp": 11.0162880546,
        "loo_mae_pp": 9.5542365956,
    },
    "filtered_stage_exposure": {
        "pearson_r": 0.9378943315,
        "spearman_r": 0.9285714286,
        "loo_rmse_pp": 4.5795128833,
        "loo_mae_pp": 3.9095939368,
    },
}


def _loo_predictions(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    predictions = np.empty_like(y, dtype=float)
    for held_out in range(len(y)):
        mask = np.ones(len(y), dtype=bool)
        mask[held_out] = False
        design = np.column_stack([np.ones(mask.sum()), x[mask]])
        beta, *_ = np.linalg.lstsq(design, y[mask], rcond=None)
        predictions[held_out] = beta[0] + beta[1] * x[held_out]
    return predictions


def build_paired_diagnostic(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {
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

    if len(df) != 7:
        raise ValueError(f"expected 7 matched region-season rows, found {len(df)}")

    out = df.copy()
    out["filtered_stage_exposure"] = (
        out["stage_matched_egg_density"]
        * (1.0 - out["egg_parasitism_pct"] / 100.0)
        * (out["egg_hatch_pct"] / 100.0)
    )

    y = out["observed_seed_predation_pct"].to_numpy(dtype=float)
    rows: list[dict[str, float | int | str]] = []

    for coordinate in [
        "annual_ground_egg_density",
        "stage_matched_egg_density",
        "filtered_stage_exposure",
    ]:
        x = out[coordinate].to_numpy(dtype=float)
        pearson = float(pd.Series(x).corr(pd.Series(y), method="pearson"))
        spearman = float(pd.Series(x).corr(pd.Series(y), method="spearman"))
        pred = _loo_predictions(x, y)
        rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
        mae = float(np.mean(np.abs(pred - y)))

        expected = EXPECTED[coordinate]
        observed = {
            "pearson_r": pearson,
            "spearman_r": spearman,
            "loo_rmse_pp": rmse,
            "loo_mae_pp": mae,
        }
        for metric, value in observed.items():
            if not np.isclose(
                value,
                expected[metric],
                rtol=0.0,
                atol=1e-9,
            ):
                raise ValueError(
                    f"{coordinate} {metric}={value:.10f} "
                    f"does not match expected {expected[metric]:.10f}"
                )

        rows.append(
            {
                "coordinate": coordinate,
                "n_region_seasons": int(len(out)),
                "pearson_r": pearson,
                "spearman_r": spearman,
                "loo_rmse_pp": rmse,
                "loo_mae_pp": mae,
            }
        )

    return out, pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "data/source_reconstructions/"
            "vanklinken2008_paired_stage_diagnostic.csv"
        ),
    )
    parser.add_argument(
        "--rows-output",
        type=Path,
        default=Path(
            "data/derived/vanklinken2008_paired_stage_rows.csv"
        ),
    )
    parser.add_argument(
        "--metrics-output",
        type=Path,
        default=Path(
            "data/derived/vanklinken2008_paired_stage_metrics.csv"
        ),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rows, metrics = build_paired_diagnostic(pd.read_csv(args.source))
    rows_rendered = rows.to_csv(
        index=False,
        lineterminator="\n",
        float_format="%.10f",
    )
    metrics_rendered = metrics.to_csv(
        index=False,
        lineterminator="\n",
        float_format="%.10f",
    )

    if args.check:
        failures = []
        for path, rendered in [
            (args.rows_output, rows_rendered),
            (args.metrics_output, metrics_rendered),
        ]:
            if not path.exists():
                failures.append(f"missing {path}")
            elif path.read_text(encoding="utf-8") != rendered:
                failures.append(f"stale {path}")
        if failures:
            for failure in failures:
                print(f"ERROR: {failure}")
            return 1
        print("Parkinsonia paired stage diagnostic is current.")
        return 0

    args.rows_output.parent.mkdir(parents=True, exist_ok=True)
    args.rows_output.write_text(rows_rendered, encoding="utf-8")
    args.metrics_output.write_text(metrics_rendered, encoding="utf-8")
    print(
        "Wrote Parkinsonia paired stage diagnostic: "
        f"{args.rows_output}, {args.metrics_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
