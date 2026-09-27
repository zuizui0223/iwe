from __future__ import annotations

from pathlib import Path

import pandas as pd


SOURCE_YEARS = {2012, 2013, 2014}
SOURCE_ECOTYPES = {"early", "late"}
_CANONICAL = {
    "plant number": "plant_id",
    "date": "doy",
    "height": "height",
    "flowers": "flowers",
    "buds": "buds",
    "seed-pods": "seed_pods",
    "seed pods": "seed_pods",
}
_REQUIRED = {"plant_id", "doy", "height", "flowers", "buds", "seed_pods"}


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename: dict[object, str] = {}
    for column in df.columns:
        key = str(column).strip().lower()
        if key in _CANONICAL:
            rename[column] = _CANONICAL[key]
    out = df.rename(columns=rename).copy()
    missing = sorted(_REQUIRED - set(out.columns))
    if missing:
        raise ValueError(
            "Cardamine workbook missing documented columns: " + ", ".join(missing)
        )
    return out


def _ru_numeric(group: pd.DataFrame) -> pd.DataFrame:
    out = group.copy()
    for column in ("flowers", "buds", "seed_pods"):
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def normalize_cardamine_transect(
    raw: pd.DataFrame,
    *,
    year: int,
    ecotype: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normalize one documented Dryad transect table conservatively.

    Returns timing observations, source-backed plant summaries, and a one-row-per-
    plant audit. Final intact RU is accepted only when the unique dehiscence row
    itself contains numeric buds/flowers/seed-pods. The parser never substitutes
    the previous observation for a missing dehiscence outcome.
    """
    if int(year) not in SOURCE_YEARS or float(year) != int(year):
        raise ValueError("Cardamine transect year must be one of 2012, 2013, 2014")
    ecotype = str(ecotype).strip().lower()
    if ecotype not in SOURCE_ECOTYPES:
        raise ValueError("Cardamine ecotype must be early or late")

    data = _canonicalize_columns(raw)
    data = data.loc[:, list(dict.fromkeys([*data.columns]))].copy()
    data["plant_id"] = data["plant_id"].astype("string").str.strip()
    data["doy"] = pd.to_numeric(data["doy"], errors="coerce")
    data = _ru_numeric(data)
    data["height_text"] = data["height"].astype("string").str.strip().str.lower()
    data["is_dehisced"] = data["height_text"].eq("d")

    valid_key = (
        data["plant_id"].notna()
        & data["plant_id"].ne("")
        & data["doy"].notna()
    )
    keyed = data.loc[valid_key].copy()
    if keyed.empty:
        raise ValueError("Cardamine transect contains no rows with plant_id and DOY")

    timing = keyed.loc[
        keyed["flowers"].notna(), ["plant_id", "doy", "flowers"]
    ].copy()
    timing.insert(0, "ecotype", ecotype)
    timing.insert(0, "year", int(year))
    timing = timing.sort_values(["plant_id", "doy"]).reset_index(drop=True)

    summaries: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []

    for plant_id, group in keyed.groupby("plant_id", sort=True):
        group = group.sort_values("doy").copy()
        flowering = group.loc[group["flowers"].fillna(0) > 0, "doy"]
        first_flowering = (
            float(flowering.min()) if not flowering.empty else float("nan")
        )

        dehisced = group.loc[group["is_dehisced"]]
        n_d = int(len(dehisced))
        status = "ready"
        reason = ""

        pre = group.loc[~group["is_dehisced"]].copy()
        complete_pre = pre.loc[
            pre[["flowers", "buds", "seed_pods"]].notna().all(axis=1)
        ].copy()
        if not complete_pre.empty:
            complete_pre["ru"] = (
                complete_pre["flowers"]
                + complete_pre["buds"]
                + complete_pre["seed_pods"]
            )
            max_ru = float(complete_pre["ru"].max())
        else:
            max_ru = float("nan")

        final_intact = float("nan")
        if pd.isna(first_flowering):
            status = "excluded"
            reason = "no_positive_flower_observation"
        elif not pd.notna(max_ru) or max_ru <= 0:
            status = "excluded"
            reason = "no_positive_source_backed_predehiscence_max_ru"
        elif n_d == 0:
            status = "excluded"
            reason = "no_dehiscence_marker"
        elif n_d > 1:
            status = "excluded"
            reason = "multiple_dehiscence_markers"
        else:
            drow = dehisced.iloc[0]
            if drow[["flowers", "buds", "seed_pods"]].isna().any():
                status = "excluded"
                reason = "dehiscence_ru_missing"
            else:
                final_intact = float(
                    drow["flowers"] + drow["buds"] + drow["seed_pods"]
                )
                if final_intact < 0:
                    status = "excluded"
                    reason = "negative_dehiscence_ru"
                elif final_intact > max_ru:
                    status = "excluded"
                    reason = "dehiscence_ru_exceeds_predehiscence_max"
                else:
                    summaries.append(
                        {
                            "year": int(year),
                            "ecotype": ecotype,
                            "plant_id": str(plant_id),
                            "max_ru": max_ru,
                            "final_intact_ru": final_intact,
                        }
                    )

        audit_rows.append(
            {
                "year": int(year),
                "ecotype": ecotype,
                "plant_id": str(plant_id),
                "first_flowering_doy": first_flowering,
                "max_ru": max_ru,
                "final_intact_ru": final_intact,
                "n_dehiscence_markers": n_d,
                "outcome_status": status,
                "exclusion_reason": reason,
            }
        )

    summary_df = pd.DataFrame(
        summaries,
        columns=["year", "ecotype", "plant_id", "max_ru", "final_intact_ru"],
    )
    audit_df = pd.DataFrame(audit_rows).sort_values(
        ["year", "ecotype", "plant_id"]
    ).reset_index(drop=True)
    return timing, summary_df, audit_df


def read_cardamine_workbook(
    path: str | Path,
    *,
    year: int,
    ecotype: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Read a Dryad XLSX with source metadata on row 1 and headers on row 2."""
    raw = pd.read_excel(Path(path), header=1, engine="openpyxl")
    return normalize_cardamine_transect(raw, year=year, ecotype=ecotype)


def normalize_cardamine_workbooks(
    specs: list[tuple[int, str, str | Path]],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normalize multiple source workbooks and concatenate their audited outputs."""
    if not specs:
        raise ValueError("at least one Cardamine workbook specification is required")
    timing_parts: list[pd.DataFrame] = []
    summary_parts: list[pd.DataFrame] = []
    audit_parts: list[pd.DataFrame] = []
    seen: set[tuple[int, str]] = set()

    for year, ecotype, path in specs:
        key = (int(year), str(ecotype).strip().lower())
        if key in seen:
            raise ValueError(f"duplicate Cardamine workbook specification: {key}")
        seen.add(key)
        timing, summaries, audit = read_cardamine_workbook(
            path, year=year, ecotype=ecotype
        )
        timing_parts.append(timing)
        summary_parts.append(summaries)
        audit_parts.append(audit)

    timing_all = pd.concat(timing_parts, ignore_index=True)
    summaries_all = pd.concat(summary_parts, ignore_index=True)
    audit_all = pd.concat(audit_parts, ignore_index=True)
    if timing_all.duplicated(["year", "ecotype", "plant_id", "doy"]).any():
        raise ValueError("duplicate normalized Cardamine timing observation detected")
    if summaries_all.duplicated(["year", "ecotype", "plant_id"]).any():
        raise ValueError("duplicate normalized Cardamine plant summary detected")
    return (
        timing_all.sort_values(["year", "ecotype", "plant_id", "doy"]).reset_index(drop=True),
        summaries_all.sort_values(["year", "ecotype", "plant_id"]).reset_index(drop=True),
        audit_all.sort_values(["year", "ecotype", "plant_id"]).reset_index(drop=True),
    )
