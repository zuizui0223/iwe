"""Source-audited 2010 Swedish Anthocharis eggs vs frozen chocho geography.

The published Ambio Table 1 supplies region-by-host *counts* of eggs and
surveyed plants, NOT independent adult flight dates, individual phenophase,
plant reproductive fitness, or sampling-cluster variance. This 2010 data
may overlap Toftegaard et al. (2018) and MUST NOT be counted independently.
"""
from __future__ import annotations

import math
import pandas as pd

SOURCE_DOI = "10.1007/s13280-014-0602-z"
SOURCE_URL = "https://link.springer.com/article/10.1007/s13280-014-0602-z"
REGIONS = ("South", "Central", "North")
SPECIES = (
    "Arabidopsis thaliana", "Thlaspi caerulescens",
    "Capsella bursa-pastoris", "Cardamine pratensis",
    "Cardamine paludosa", "Arabis hirsuta", "Arabis glabra",
)
COUNTS = ("sampled_populations", "n_eggs", "n_plants", "n_trait_plants")
SOURCE_FIELDS = {"region", "species_as_published", "sampling_status",
                 *COUNTS, "published_eggs_per_plant"}
TAXON_FIELDS = {"species_as_published", "normalized_accepted_name",
                "portfolio_match", "accepted_plant_name_id",
                "normalization", "normalization_source"}
GEO_FIELDS = {"accepted_plant_name_id", "accepted_name",
              "fractional_added_unit_credit",
              "butterfly_added_units_covered",
              "butterfly_added_units_exclusively_covered"}


def _require(frame: pd.DataFrame, cols: set[str], label: str) -> None:
    missing = sorted(cols - set(frame.columns))
    if missing:
        raise ValueError(f"{label}: missing {missing}")


def _integer(frame: pd.DataFrame, name: str) -> pd.Series:
    vals = pd.to_numeric(frame[name], errors="coerce")
    if (vals.isna().any() or (vals < 0).any()
            or (~(vals % 1 == 0)).any()):
        raise ValueError(f"invalid nonnegative count: {name}")
    return vals.astype("int64")


def build_ambio_host_use(
    source: pd.DataFrame,
    oikos_taxonomy: pd.DataFrame,
    frozen_chocho_hosts: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Combine exact 2010 source egg counts with source-checked host identities.

    All quantitative contrasts are DESCRIPTIVE. Eggs per plant can exceed one
    and are not binomial incidence. The site/plot IDs are not in Table 1;
    never treat surveyed plants as independent regression observations.
    """
    _require(source, SOURCE_FIELDS, "Ambio Table 1")
    _require(oikos_taxonomy, TAXON_FIELDS, "Oikos taxon crosswalk")
    _require(frozen_chocho_hosts, GEO_FIELDS, "chocho geography")
    data = source.copy()
    for col in ("region", "species_as_published", "sampling_status"):
        data[col] = data[col].astype(str).str.strip()
    if data.duplicated(["region", "species_as_published"]).any():
        raise ValueError("duplicate region-species in Ambio Table 1")
    if len(data) != 21 or set(data["region"]) != set(REGIONS) or set(
            data["species_as_published"]) != set(SPECIES):
        raise ValueError("Ambio Table 1 expected complete 3 by 7 source grid")
    expected = {(r, s) for r in REGIONS for s in SPECIES}
    if set(zip(data["region"], data["species_as_published"])) != expected:
        raise ValueError("Ambio region-species grid incomplete")
    if not data["sampling_status"].isin(["sampled", "host_not_found"]).all():
        raise ValueError("invalid sampling_status: do not infer sampled zeros")
    present = data["sampling_status"].eq("sampled")
    count_fields = (*COUNTS, "published_eggs_per_plant")
    for name in count_fields:
        if data.loc[~present, name].fillna("").astype(str).str.strip().ne("").any():
            raise ValueError("host_not_found must not have invented zero/counts")
    sampled = data.loc[present].copy()
    for col in COUNTS:
        sampled[col] = _integer(sampled, col)
    if ((sampled["sampled_populations"] <= 0)
            | (sampled["n_plants"] <= 0)
            | (sampled["n_trait_plants"] > sampled["n_plants"])).any():
        raise ValueError("invalid sampled population/plant denominators")
    printed = pd.to_numeric(sampled["published_eggs_per_plant"], errors="coerce")
    if printed.isna().any() or (printed < 0).any() or (~printed.map(math.isfinite)).any():
        raise ValueError("invalid printed egg ratio")
    sampled["published_eggs_per_plant"] = printed
    sampled["eggs_per_plant_recomputed"] = (
        sampled["n_eggs"] / sampled["n_plants"]
    )
    sampled["abs_published_rate_discrepancy"] = (
        sampled["published_eggs_per_plant"]
        - sampled["eggs_per_plant_recomputed"]
    ).abs()
    sampled["material_printed_rate_discrepancy"] = (
        sampled["abs_published_rate_discrepancy"] > 0.005
    )
    absent = data.loc[~present].copy()
    for name in (*COUNTS, "published_eggs_per_plant",
                 "eggs_per_plant_recomputed",
                 "abs_published_rate_discrepancy"):
        absent[name] = float("nan")
    absent["material_printed_rate_discrepancy"] = False
    table = pd.concat([sampled, absent], ignore_index=True)

    taxonomy = oikos_taxonomy.copy().fillna("")
    for name in TAXON_FIELDS:
        taxonomy[name] = taxonomy[name].astype(str).str.strip()
    if taxonomy["species_as_published"].duplicated().any():
        raise ValueError("duplicate Oikos taxon entries")
    required_original = set(SPECIES) - {"Cardamine paludosa"}
    if set(taxonomy["species_as_published"]) != required_original:
        raise ValueError("Oikos crosswalk must cover the other six taxa exactly")
    # Ambio 2015 distinguishes a separate octoploid cytotype. It is NOT
    # silently pooled into the tetraploid C. pratensis field sample.
    extra = pd.DataFrame([{
        "species_as_published": "Cardamine paludosa",
        "normalized_accepted_name": "",
        "normalization": "source_separated_octoploid_not_resolved",
        "portfolio_match": "not_in_frozen_11_host_portfolio",
        "accepted_plant_name_id": "",
        "normalization_source": SOURCE_URL,
    }])
    taxonomy = pd.concat([taxonomy, extra], ignore_index=True)
    if taxonomy.loc[
        taxonomy["species_as_published"] == "Cardamine paludosa",
        "portfolio_match",
    ].item() != "not_in_frozen_11_host_portfolio":
        raise ValueError("C. paludosa cannot be silently combined with C. pratensis")

    geo = frozen_chocho_hosts.copy()
    geo["accepted_plant_name_id"] = geo["accepted_plant_name_id"].astype(str)
    if geo["accepted_plant_name_id"].duplicated().any():
        raise ValueError("duplicate chocho host IDs")
    geo["accepted_name"] = geo["accepted_name"].astype(str).str.strip()
    if geo["accepted_name"].duplicated().any():
        raise ValueError("duplicate chocho accepted plant names")
    for f in ("fractional_added_unit_credit",
              "butterfly_added_units_covered",
              "butterfly_added_units_exclusively_covered"):
        geo[f] = pd.to_numeric(geo[f], errors="raise")
    if not math.isclose(float(geo["fractional_added_unit_credit"].sum()),
                        110., abs_tol=1e-8):
        raise ValueError("chocho frozen fractional attribution changed")
    if not set(taxonomy["accepted_plant_name_id"]) - {""} <= set(
            geo["accepted_plant_name_id"]):
        raise ValueError("taxonomy references a missing frozen host ID")
    table = table.merge(
        taxonomy, on="species_as_published", how="left",
        validate="many_to_one",
    )
    if table["portfolio_match"].isna().any():
        raise ValueError("missing taxonomy mapping")
    geo_small = geo[[
        "accepted_plant_name_id", "accepted_name",
        "fractional_added_unit_credit",
        "butterfly_added_units_covered",
        "butterfly_added_units_exclusively_covered",
    ]].rename(columns={"accepted_name": "_geo_name"})
    table = table.merge(
        geo_small, on="accepted_plant_name_id",
        how="left", validate="many_to_one",
    )
    m = table["portfolio_match"].eq("matched")
    if table.loc[m, "_geo_name"].isna().any():
        raise ValueError("matched host not found in chocho")
    if not (table.loc[m, "_geo_name"].tolist() ==
            table.loc[m, "normalized_accepted_name"].tolist()):
        raise ValueError("taxonomic name/accepted ID disagree")
    if table.loc[~m, "_geo_name"].notna().any():
        raise ValueError("unmatched host was silently joined to geography")
    table = table.drop(columns="_geo_name")
    table["year"] = 2010
    table = table.sort_values(
        ["region", "species_as_published"], kind="stable"
    ).reset_index(drop=True)
    # Rebuild the boolean mask after sorting/resetting row indices. Retaining
    # the pre-sort mask would silently mislabel unmatched taxa as matched.
    m = table["portfolio_match"].eq("matched")

    # A deliberately complete three-region comparison. Published
    # rates are NOT used: South C. paludosa printed ratio is inconsistent.
    contrast = []
    for region in REGIONS:
        card = table.loc[
            (table["region"] == region)
            & table["species_as_published"].eq("Cardamine pratensis")
        ].iloc[0]
        caps = table.loc[
            (table["region"] == region)
            & table["species_as_published"].eq("Capsella bursa-pastoris")
        ].iloc[0]
        card_rate = float(card["eggs_per_plant_recomputed"])
        caps_rate = float(caps["eggs_per_plant_recomputed"])
        contrast.append({
            "region": region,
            "year": 2010,
            "cardamine_eggs": int(card["n_eggs"]),
            "cardamine_plants": int(card["n_plants"]),
            "capsella_eggs": int(caps["n_eggs"]),
            "capsella_plants": int(caps["n_plants"]),
            "cardamine_eggs_per_plant": card_rate,
            "capsella_eggs_per_plant": caps_rate,
            "observed_rate_ratio_cardamine_over_capsella": (
                card_rate / caps_rate if caps_rate > 0 else float("nan")
            ),
            "comparison_type": "descriptive_observed_egg_rate_not_causal",
        })
    contrasts = pd.DataFrame(contrast)

    sampled_table = table.loc[table["sampling_status"].eq("sampled")]
    discrepant = sampled_table.loc[
        sampled_table["material_printed_rate_discrepancy"]
    ]
    result = {
        "schema": "iwe_chocho_ambio2010_egg_use_audit_v0.1",
        "source_doi": SOURCE_DOI,
        "source_table": "Table 1",
        "source_type": "published_aggregated_counts",
        "survey_year": 2010,
        "total_source_rows_including_missing": int(len(table)),
        "sampled_region_host_rows": int(len(sampled_table)),
        "host_not_found_rows_not_assigned_zero": int(len(table) - len(sampled_table)),
        "observed_egg_count": int(sampled_table["n_eggs"].sum()),
        "sampled_plant_count": int(sampled_table["n_plants"].sum()),
        "plant_trait_record_count": int(sampled_table["n_trait_plants"].sum()),
        "matched_chocho_host_species": sorted(
            table.loc[m, "normalized_accepted_name"].unique().tolist()
        ),
        "material_published_ratio_discrepancies": [
            {
                "region": row["region"],
                "published_host": row["species_as_published"],
                "reported": float(row["published_eggs_per_plant"]),
                "derived_eggs_div_plants": float(row["eggs_per_plant_recomputed"]),
            }
            for _, row in discrepant.iterrows()
        ],
        "source_overlap_with_oikos2018": "possible_same_programme_not_independent",
        "phenology_stage_observations_extracted": False,
        "female_adult_flight_window_extracted": False,
        "regional_oviposition_causation_identified": False,
        "global_distribution_causation_identified": False,
        "plant_final_fitness_observed": False,
        "strict_h1_effects_created": 0,
        "claim_status": "descriptive_region_host_egg_rates_only",
    }
    return table, contrasts, result
