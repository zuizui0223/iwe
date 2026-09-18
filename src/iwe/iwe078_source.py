from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np
import pandas as pd


_NA_VALUES = ["NA", "na", "NaN", ""]
_EXP1_VALID_GENOTYPES = {"80", "6", "64", "2"}
_EXP1_EXCLUDED_IDS = {"2.05", "2.39", "64.2"}
_EXP2_EXCLUDED_IDS = {"81.12", "28.37", "81.06"}
_EXP2_MISSING_FITNESS_IDS = {"63.15", "28.26", "2.89", "10.73", "2.77", "112.05"}


@dataclass(frozen=True)
class IWE078CanonicalSource:
    flowering: pd.DataFrame
    attacks: pd.DataFrame
    fitness: pd.DataFrame
    eligible_ids: dict[str, frozenset[str]]


def _read_source_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        dtype=str,
        na_values=_NA_VALUES,
        keep_default_na=True,
    )


def _clean_id(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    return text


def _parse_source_date(value: object) -> pd.Timestamp:
    """Parse the mixed date formats present in the archived IWE078 files.

    Experiment-1 momphaCALC writes 2023 dates as 0023-MM-DD; the raw date
    lists and Experiment-2 files use M/D/YY. This parser repairs only that
    explicit archival formatting artifact.
    """
    if pd.isna(value):
        return pd.NaT
    text = str(value).strip()
    if not text:
        return pd.NaT
    match = re.fullmatch(r"00(\d{2})-(\d{2})-(\d{2})", text)
    if match:
        text = f"20{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return pd.to_datetime(text, errors="coerce")


def _r_week_start(values: pd.Series) -> pd.Series:
    """Mirror cut.Date(..., breaks='week') with Monday-start weekly bins."""
    dates = pd.to_datetime(values, errors="coerce")
    return dates - pd.to_timedelta(dates.dt.weekday, unit="D")


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _source_dates(root: Path, file_name: str) -> list[pd.Timestamp]:
    df = _read_source_csv(root / file_name)
    if "date" not in df.columns:
        raise ValueError(f"{file_name} must contain a date column")
    dates = [_parse_source_date(v) for v in df["date"]]
    if any(pd.isna(v) for v in dates):
        raise ValueError(f"{file_name} contains an unparseable date")
    return dates


def _wide_flower_long(
    root: Path,
    *,
    data_file: str,
    date_file: str,
    experiment: str,
) -> pd.DataFrame:
    wide = _read_source_csv(root / data_file)
    required = {"ID", "TRT", "geno"}
    missing = required - set(wide.columns)
    if missing:
        raise ValueError(f"{data_file} missing columns: {sorted(missing)}")

    count_columns = [c for c in wide.columns if c not in required]
    dates = _source_dates(root, date_file)
    if len(count_columns) != len(dates):
        raise ValueError(
            f"{data_file}: {len(count_columns)} count columns != "
            f"{len(dates)} source dates"
        )

    rows: list[dict] = []
    for _, row in wide.iterrows():
        plant_id = _clean_id(row["ID"])
        if plant_id is None:
            continue
        for column, date in zip(count_columns, dates, strict=True):
            rows.append(
                {
                    "experiment": str(experiment),
                    "plant_id": plant_id,
                    "raw_treatment": row["TRT"],
                    "genotype": row["geno"],
                    "date": date,
                    "open_flowers": pd.to_numeric(row[column], errors="coerce"),
                }
            )
    return pd.DataFrame(rows)


def _mompha_long(
    root: Path,
    *,
    file_name: str,
    experiment: str,
) -> pd.DataFrame:
    df = _read_source_csv(root / file_name)
    required = {"ID", "date", "mompha", "positive mompha"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} missing columns: {sorted(missing)}")

    out = pd.DataFrame(
        {
            "experiment": str(experiment),
            "plant_id": df["ID"].map(_clean_id),
            "date": df["date"].map(_parse_source_date),
            "fresh_mompha": _numeric(df["mompha"]),
            "positive_mompha": _numeric(df["positive mompha"]),
        }
    )
    return out.loc[out["plant_id"].notna() & out["date"].notna()].copy()


def _extra_potential_rows(
    root: Path,
    *,
    file_name: str,
    experiment: str,
    flower_survey_dates: set[pd.Timestamp],
) -> pd.DataFrame:
    """Recover source first-potential-flower rows outside regular flower surveys."""
    df = _read_source_csv(root / file_name)
    required = {"ID", "date", "potential"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{file_name} missing columns: {sorted(missing)}")

    out = pd.DataFrame(
        {
            "experiment": str(experiment),
            "plant_id": df["ID"].map(_clean_id),
            "date": df["date"].map(_parse_source_date),
            "potential_flowers": _numeric(df["potential"]),
        }
    )
    out = out.loc[
        out["plant_id"].notna()
        & out["date"].notna()
        & ~out["date"].isin(flower_survey_dates)
    ].copy()
    return out


def _eligible_exp1(root: Path) -> tuple[pd.DataFrame, frozenset[str]]:
    main = _read_source_csv(root / "main_exp1.csv")
    fit = _read_source_csv(root / "fitness_exp1.csv")
    main["plant_id"] = main["ID"].map(_clean_id)
    fit["plant_id"] = fit["ID"].map(_clean_id)

    keep = main["plant_id"].notna()
    keep &= main["TRT"].astype(str).str.strip().eq("C")
    keep &= ~main["CHOP_1FLR"].astype(str).str.upper().eq("Y")
    keep &= main["first_flr"].notna()
    keep &= main["first_flr"].astype(str).str.strip().str.lower().ne("na")
    keep &= main["geno"].notna()
    keep &= main["geno"].astype(str).str.strip().isin(_EXP1_VALID_GENOTYPES)
    keep &= ~main["plant_id"].isin(_EXP1_EXCLUDED_IDS)
    meta = main.loc[keep, ["plant_id"]].drop_duplicates()

    merged = meta.merge(fit, on="plant_id", how="left", validate="one_to_one")
    lg = _numeric(merged["lg frt"])
    sm = _numeric(merged["sm frt"])
    schinia = _numeric(merged["schinia"])
    sm_brev = _numeric(merged["sm brev"])
    lg_brev_fit = _numeric(merged["lg brev FIT"])
    merged["final_reproduction"] = (
        lg + sm - (schinia + 0.2 * sm_brev + 0.2 * lg_brev_fit)
    )
    merged = merged.loc[merged["final_reproduction"].notna()].copy()
    if (merged["final_reproduction"] < 0).any():
        raise ValueError("Experiment 1 source reconstruction produced negative fitness")

    eligible = frozenset(merged["plant_id"].astype(str))
    fitness = pd.DataFrame(
        {
            "experiment": "1",
            "plant_id": merged["plant_id"].astype(str),
            "treatment": "control",
            "final_reproduction": merged["final_reproduction"].astype(float),
        }
    )
    return fitness.reset_index(drop=True), eligible


def _eligible_exp2(root: Path) -> tuple[pd.DataFrame, frozenset[str]]:
    main = _read_source_csv(root / "main_exp2.csv")
    fit = _read_source_csv(root / "Exp 2 fitness.csv")
    main["plant_id"] = main["ID"].map(_clean_id)
    fit["plant_id"] = fit["ID"].map(_clean_id)

    keep = main["plant_id"].notna()
    keep &= main["Treatment"].astype(str).str.strip().str.lower().eq("c")
    keep &= ~main["CHOP_1FLR"].astype(str).str.upper().eq("Y")
    keep &= main["first_flr_mom"].notna()
    keep &= main["first_flr_mom"].astype(str).str.strip().str.lower().ne("na")
    keep &= main["geno"].notna()
    keep &= main["geno"].astype(str).str.strip().str.lower().ne("na")
    keep &= ~main["plant_id"].isin(_EXP2_EXCLUDED_IDS)
    keep &= ~main["plant_id"].isin(_EXP2_MISSING_FITNESS_IDS)
    meta = main.loc[keep, ["plant_id"]].drop_duplicates()

    merged = meta.merge(fit, on="plant_id", how="left", validate="one_to_one")
    lg = _numeric(merged["lg frt"])
    sm = _numeric(merged["sm frt"])
    schinia = _numeric(merged["schinia"])
    sm_brev = _numeric(merged["sm brev"])
    lg_brev = _numeric(merged["lg brev"])
    merged["final_reproduction"] = (
        lg + sm - (schinia + 0.2 * sm_brev + 0.2 * lg_brev)
    )
    merged = merged.loc[merged["final_reproduction"].notna()].copy()
    if (merged["final_reproduction"] < 0).any():
        raise ValueError("Experiment 2 source reconstruction produced negative fitness")

    eligible = frozenset(merged["plant_id"].astype(str))
    fitness = pd.DataFrame(
        {
            "experiment": "2",
            "plant_id": merged["plant_id"].astype(str),
            "treatment": "control",
            "final_reproduction": merged["final_reproduction"].astype(float),
        }
    )
    return fitness.reset_index(drop=True), eligible


def _canonical_experiment(
    root: Path,
    *,
    experiment: str,
    flower_file: str,
    flower_date_file: str,
    mompha_file: str,
    extra_potential_file: str,
    eligible_ids: frozenset[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    flowers = _wide_flower_long(
        root,
        data_file=flower_file,
        date_file=flower_date_file,
        experiment=experiment,
    )
    mompha = _mompha_long(root, file_name=mompha_file, experiment=experiment)

    # Source final_all is an outer merge of flower surveys and fresh Mompha
    # surveys. potential = flower + mompha/9, with a missing component treated
    # as zero only when the other component is observed.
    merged = flowers[["plant_id", "date", "open_flowers"]].merge(
        mompha[["plant_id", "date", "fresh_mompha"]],
        on=["plant_id", "date"],
        how="outer",
        validate="one_to_one",
    )
    both_missing = merged["open_flowers"].isna() & merged["fresh_mompha"].isna()
    merged["potential_flowers"] = (
        merged["open_flowers"].fillna(0.0)
        + merged["fresh_mompha"].fillna(0.0) / 9.0
    )
    merged.loc[both_missing, "potential_flowers"] = np.nan

    flower_dates = set(pd.to_datetime(flowers["date"].dropna().unique()))
    extra = _extra_potential_rows(
        root,
        file_name=extra_potential_file,
        experiment=experiment,
        flower_survey_dates=flower_dates,
    )
    potential = pd.concat(
        [
            merged[["plant_id", "date", "potential_flowers"]],
            extra[["plant_id", "date", "potential_flowers"]],
        ],
        ignore_index=True,
    )
    potential = potential.loc[potential["plant_id"].isin(eligible_ids)].copy()
    potential["week"] = _r_week_start(potential["date"])
    potential = (
        potential.groupby(["plant_id", "week"], as_index=False, dropna=False)
        .agg(
            potential_flowers=(
                "potential_flowers",
                lambda s: s.sum(min_count=1),
            )
        )
    )
    flowering = potential.rename(columns={"week": "date"})
    flowering.insert(0, "experiment", str(experiment))
    flowering["treatment"] = "control"
    flowering = flowering[
        ["experiment", "plant_id", "treatment", "date", "potential_flowers"]
    ]

    attack = mompha.loc[mompha["plant_id"].isin(eligible_ids)].copy()
    attack["week"] = _r_week_start(attack["date"])
    attack = (
        attack.groupby(["plant_id", "week"], as_index=False, dropna=False)
        .agg(
            mompha_acquired=(
                "positive_mompha",
                lambda s: s.sum(min_count=1),
            )
        )
    )
    attack = attack.rename(columns={"week": "date"})
    attack.insert(0, "experiment", str(experiment))
    attack["treatment"] = "control"
    attack = attack[
        ["experiment", "plant_id", "treatment", "date", "mompha_acquired"]
    ]

    return flowering.reset_index(drop=True), attack.reset_index(drop=True)


def load_iwe078_source(source_dir: str | Path) -> IWE078CanonicalSource:
    """Canonicalize the archived Zenodo IWE078 source package.

    The returned date column is a Monday-start weekly bin, matching the source
    R analysis' cut.Date(..., breaks="week") convention.
    """
    root = Path(source_dir)
    required_files = [
        "main_exp1.csv",
        "fitness_exp1.csv",
        "df2_exp1.csv",
        "test.csv",
        "momphaCALC_exp1.csv",
        "fflr_overlap_ex1.csv",
        "main_exp2.csv",
        "Exp 2 fitness.csv",
        "df2_exp2.csv",
        "test_exp2.csv",
        "momphaCALC_exp2.csv",
        "fflr_overlap_ex2.csv",
    ]
    missing = [name for name in required_files if not (root / name).exists()]
    if missing:
        raise FileNotFoundError(f"IWE078 source package missing files: {missing}")

    fit1, ids1 = _eligible_exp1(root)
    fit2, ids2 = _eligible_exp2(root)

    flower1, attack1 = _canonical_experiment(
        root,
        experiment="1",
        flower_file="df2_exp1.csv",
        flower_date_file="test.csv",
        mompha_file="momphaCALC_exp1.csv",
        extra_potential_file="fflr_overlap_ex1.csv",
        eligible_ids=ids1,
    )
    flower2, attack2 = _canonical_experiment(
        root,
        experiment="2",
        flower_file="df2_exp2.csv",
        flower_date_file="test_exp2.csv",
        mompha_file="momphaCALC_exp2.csv",
        extra_potential_file="fflr_overlap_ex2.csv",
        eligible_ids=ids2,
    )

    return IWE078CanonicalSource(
        flowering=pd.concat([flower1, flower2], ignore_index=True),
        attacks=pd.concat([attack1, attack2], ignore_index=True),
        fitness=pd.concat([fit1, fit2], ignore_index=True),
        eligible_ids={"1": ids1, "2": ids2},
    )
