from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED_WHOLE_SITE_R = {
    "NFP": -0.6823367403,
    "TOEF": -0.9041525384,
    "JOZ": -0.8184761715,
}

EXPECTED_WHOLE_SITE_N = {
    "NFP": 13,
    "TOEF": 9,
    "JOZ": 7,
}

DEPENDENCE_ID = "DEP_CORYDALIS_KUDO_LONGTERM"
SOURCE_ID = "E094-213-A1"


def build_directional_effects(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "site",
        "year",
        "natural_seed_set",
        "natural_seed_n",
        "mismatch_day",
        "source_id",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    for site, expected_r in EXPECTED_WHOLE_SITE_R.items():
        site_df = df[df["site"].eq(site)]
        if len(site_df) != EXPECTED_WHOLE_SITE_N[site]:
            raise ValueError(
                f"{site}: expected {EXPECTED_WHOLE_SITE_N[site]} complete rows, "
                f"found {len(site_df)}"
            )
        observed_r = float(
            site_df["mismatch_day"].corr(site_df["natural_seed_set"])
        )
        if not np.isclose(observed_r, expected_r, rtol=0.0, atol=1e-10):
            raise ValueError(
                f"{site}: reconstructed whole-site r={observed_r:.10f} "
                f"does not reproduce registered r={expected_r:.10f}"
            )

    rows: list[dict[str, object]] = []
    domains = [
        (
            "plant_earlier_only",
            lambda x: x > 0,
            "mismatch",
            "positive partner_minus_plant means the plant flowers before bee detection",
        ),
        (
            "partner_earlier_only",
            lambda x: x < 0,
            "synchrony",
            "negative partner_minus_plant means bees are detected before flowering",
        ),
    ]

    for site in sorted(EXPECTED_WHOLE_SITE_R):
        site_df = df[df["site"].eq(site)].copy()
        for domain, selector, exposure_direction, domain_note in domains:
            subset = site_df[selector(site_df["mismatch_day"])].copy()
            n = int(len(subset))
            status = "estimable" if n >= 4 else "insufficient_n"
            pearson_r = np.nan
            fisher_z = np.nan
            variance = np.nan

            if status == "estimable":
                pearson_r = float(
                    subset["mismatch_day"].corr(subset["natural_seed_set"])
                )
                fisher_z = float(np.arctanh(pearson_r))
                variance = float(1.0 / (n - 3))

            rows.append(
                {
                    "effect_id": f"IWE001_{site}_{domain.upper()}_FZ",
                    "study_id": "IWE001",
                    "dependence_id": DEPENDENCE_ID,
                    "site_id": site,
                    "timing_metric_type": "partner_minus_plant",
                    "timing_analysis_class": "directional_mismatch",
                    "timing_domain": domain,
                    "exposure_direction": exposure_direction,
                    "effect_family": "fisher_z",
                    "sample_size": n,
                    "pearson_r": pearson_r,
                    "effect_native": fisher_z,
                    "variance_native": variance,
                    "status": status,
                    "source_id": SOURCE_ID,
                    "notes": domain_note,
                }
            )

    return pd.DataFrame(rows)


def render_csv(df: pd.DataFrame) -> str:
    return df.to_csv(
        index=False,
        lineterminator="\n",
        float_format="%.10f",
        na_rep="",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(
            "data/source_reconstructions/iwe001_appendix_a_complete_rows.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/iwe001_directional_landscape.csv"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = pd.read_csv(args.source)
    effects = build_directional_effects(source)
    rendered = render_csv(effects)

    if args.check:
        if not args.output.exists():
            print(f"ERROR: missing directional output: {args.output}")
            return 1
        if args.output.read_text(encoding="utf-8") != rendered:
            print(f"ERROR: stale directional output: {args.output}")
            return 1
        print(f"IWE001 directional landscape is current: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Wrote IWE001 directional landscape to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
