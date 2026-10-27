"""Audit published sampling denominators against pinned chocho host portfolios.

Rows from Oikos Appendix 1, Table A1 are *counts of plants with
phenophase and oviposition incidence recorded*, NOT egg counts,
butterfly counts, independent adult windows, or fitness effect sizes.
"""
from __future__ import annotations

import math
import pandas as pd

YEARS = (2010, 2011, 2012, 2013)
SOURCE_FIELDS = {"region", "species_as_published", *(f"n_{y}" for y in YEARS)}
TAXON_FIELDS = {
    "species_as_published", "normalized_accepted_name", "normalization",
    "portfolio_match", "accepted_plant_name_id", "normalization_source",
}
GEO_FIELDS = {
    "accepted_plant_name_id", "accepted_name",
    "fractional_added_unit_credit", "butterfly_added_units_covered",
    "butterfly_added_units_exclusively_covered",
}


def _required(df: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ValueError(f"{name}: missing {missing}")


def _name(x: object) -> str:
    return "" if pd.isna(x) else str(x).strip()


def _counts(s: pd.Series, label: str) -> pd.Series:
    vals = pd.to_numeric(s, errors="coerce")
    if vals.isna().any() or (vals < 0).any() or (~(vals % 1 == 0)).any():
        raise ValueError(f"{label}: nonnegative integer count required")
    return vals.astype("int64")


def build_oikos_sampling_crosswalk(
    table_a1: pd.DataFrame, taxonomy: pd.DataFrame,
    host_geography: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Return 60 source strata, six species summaries, and noninferential audit.

    A referenced synonym is admitted as an identity match, but only an exact
    accepted plant ID and accepted name may join the frozen host portfolio.
    Sampling counts are never multiplied by regional portfolio totals.
    """
    _required(table_a1, SOURCE_FIELDS, "Oikos Table A1")
    _required(taxonomy, TAXON_FIELDS, "curated taxon names")
    _required(host_geography, GEO_FIELDS, "chocho host geography")

    raw = table_a1.copy()
    if raw[["region", "species_as_published"]].isna().any().any():
        raise ValueError("Oikos Table A1: blank region/species")
    raw["region"] = raw["region"].map(_name)
    raw["species_as_published"] = raw["species_as_published"].map(_name)
    if raw["region"].eq("").any() or raw["species_as_published"].eq("").any():
        raise ValueError("Oikos Table A1: blank region/species")
    if raw.duplicated(["region", "species_as_published"]).any():
        raise ValueError("Oikos Table A1: duplicated region-species cohort")
    for year in YEARS:
        raw[f"n_{year}"] = _counts(raw[f"n_{year}"], f"year {year}")

    tx = taxonomy.copy().fillna("")
    for col in TAXON_FIELDS:
        tx[col] = tx[col].map(_name)
    if tx["species_as_published"].eq("").any() or tx["species_as_published"].duplicated().any():
        raise ValueError("curated taxonomy: missing/duplicate published species")
    if set(raw["species_as_published"]) != set(tx["species_as_published"]):
        raise ValueError("curated taxonomy: must cover exactly all Table A1 species")
    if (~tx["normalization"].isin(
        ["as_published", "homotypic_synonym", "verified_synonym"]
    )).any():
        raise ValueError("taxonomy: unknown normalization")
    if (~tx["portfolio_match"].isin(
        ["matched", "not_in_frozen_11_host_portfolio"]
    )).any():
        raise ValueError("taxonomy: unknown frozen portfolio status")
    for _, row in tx.iterrows():
        if row["normalization"] != "as_published" and not row["normalization_source"]:
            raise ValueError("synonym requires a verifiable independent name source")
        if row["normalization"] == "as_published" and (
            row["species_as_published"] != row["normalized_accepted_name"]
        ):
            raise ValueError("as_published cannot silently change accepted name")

    geo = host_geography.copy()
    for col in ["accepted_name", "accepted_plant_name_id"]:
        geo[col] = geo[col].map(_name)
    if geo["accepted_name"].duplicated().any() or geo["accepted_plant_name_id"].duplicated().any():
        raise ValueError("chocho geography: duplicate accepted names or IDs")
    geo_index = geo.set_index("accepted_name")
    for _, row in tx.iterrows():
        matched = row["portfolio_match"] == "matched"
        in_geo = row["normalized_accepted_name"] in geo_index.index
        if matched != in_geo:
            raise ValueError("taxonomy/geo portfolio match disagreement: "
                             + row["species_as_published"])
        if matched:
            correct_id = geo_index.loc[row["normalized_accepted_name"], "accepted_plant_name_id"]
            if correct_id != row["accepted_plant_name_id"]:
                raise ValueError("accepted plant ID mismatch: " + row["species_as_published"])
        elif row["accepted_plant_name_id"]:
            raise ValueError("unmatched species cannot invent a frozen portfolio plant ID")

    strata = raw.melt(
        id_vars=["region", "species_as_published"],
        value_vars=[f"n_{y}" for y in YEARS],
        var_name="year", value_name="n_plants",
    )
    strata["year"] = strata["year"].str.removeprefix("n_").astype("int64")
    strata = strata.merge(
        tx, on="species_as_published", how="left", validate="many_to_one"
    ).sort_values(["species_as_published", "region", "year"], kind="stable").reset_index(drop=True)

    grouped = strata.groupby(
        ["species_as_published", "normalized_accepted_name",
         "normalization", "portfolio_match", "accepted_plant_name_id"],
        dropna=False, as_index=False
    )["n_plants"].sum().rename(columns={"n_plants": "n_plants_all_strata"})
    geovals = geo[[
        "accepted_plant_name_id", "accepted_name", "fractional_added_unit_credit",
        "butterfly_added_units_covered",
        "butterfly_added_units_exclusively_covered",
    ]].rename(columns={"accepted_name": "_geographic_accepted_name"})
    for field in ["fractional_added_unit_credit", "butterfly_added_units_covered",
                  "butterfly_added_units_exclusively_covered"]:
        geovals[field] = pd.to_numeric(geovals[field], errors="raise")
    species = grouped.merge(
        geovals, on="accepted_plant_name_id", how="left", validate="many_to_one"
    )
    if species.loc[
        species["portfolio_match"] == "matched", "_geographic_accepted_name"
    ].isna().any():
        raise ValueError("matched species lacks geographic source after merge")
    if species.loc[
        species["portfolio_match"] == "matched", "normalized_accepted_name"
    ].tolist() != species.loc[
        species["portfolio_match"] == "matched", "_geographic_accepted_name"
    ].tolist():
        raise ValueError("accepted name mismatch after geographic join")
    species = species.drop(columns="_geographic_accepted_name").sort_values(
        "species_as_published", kind="stable"
    ).reset_index(drop=True)

    matched = species.loc[species["portfolio_match"] == "matched"]
    whole_credit = pd.to_numeric(geo["fractional_added_unit_credit"], errors="raise").sum()
    if not math.isclose(float(whole_credit), 110.0, abs_tol=1e-8):
        raise ValueError("chocho frozen total fractional credit drift from 110")
    sampled_matched_credit = float(matched["fractional_added_unit_credit"].sum())
    audit = {
        "schema": "iwe_chocho_oikos_sampling_audit_v0.1",
        "source": "Toftegaard et al. Oikos DOI 10.1111/oik.05720 Appendix 1 Table A1",
        "source_type": "manually transcribed published table of sampling denominators",
        "years": list(YEARS),
        "regions": sorted(raw["region"].unique().tolist()),
        "published_plant_species": int(len(species)),
        "unique_region_species_cohorts": int(len(raw)),
        "year_region_species_strata": int(len(strata)),
        "plant_records_sum_across_strata": int(strata["n_plants"].sum()),
        "host_species_in_frozen_chocho_portfolio": int(len(matched)),
        "matched_plant_records_sum": int(matched["n_plants_all_strata"].sum()),
        "matched_hosts_fractional_geographic_credit": sampled_matched_credit,
        "all_hosts_fractional_geographic_credit": float(whole_credit),
        "matched_share_of_added_resource_credit": sampled_matched_credit / float(whole_credit),
        "individual_phenophase_values_extracted": False,
        "individual_oviposition_incidence_values_extracted": False,
        "independent_adult_activity_observed": False,
        "geographic_regions_joined_to_swedish_sites": False,
        "strict_h1_effects_created": 0,
        "ecological_claim_permitted": False,
    }
    return strata, species, audit
