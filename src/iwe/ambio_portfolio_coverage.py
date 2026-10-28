"""Coverage of published egg-count host taxa by chocho's frozen host portfolio.

These are egg-count accounting diagnostics, NOT host suitability, the
butterfly's occupancy, independent oviposition events, or time-window effects.
C. paludosa is a separately sampled octoploid in the source; a hypothetical
species-complex grouping is reported only as a sensitivity upper bound.
"""
from __future__ import annotations

import pandas as pd
from iwe.ambio_host_use import build_ambio_host_use, REGIONS


def summarize_ambio_portfolio_coverage(
    source: pd.DataFrame,
    taxonomy: pd.DataFrame,
    geography: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    table, _, prior = build_ambio_host_use(source, taxonomy, geography)
    frame = table.loc[table["sampling_status"] == "sampled"].copy()
    frame["n_eggs"] = pd.to_numeric(frame["n_eggs"], errors="raise")
    if frame["n_eggs"].isna().any() or (frame["n_eggs"] < 0).any():
        raise ValueError("unexpected invalid egg count")
    frame["portfolio_bucket"] = "other_taxon_not_in_frozen_portfolio"
    frame.loc[
        frame["portfolio_match"] == "matched", "portfolio_bucket"
    ] = "exact_accepted_host_in_portfolio"
    frame.loc[
        frame["species_as_published"] == "Cardamine paludosa",
        "portfolio_bucket"
    ] = "separately_reported_octoploid_cardamine"
    # The published paper identifies C. paludosa as an octoploid
    # C. pratensis ssp. paludosa, but keeps it separate from tetraploid
    # C. pratensis ssp. pratensis. No geographic ID is reassigned.
    if len(frame.loc[
        frame["portfolio_bucket"] == "separately_reported_octoploid_cardamine"
    ]) != 3:
        raise ValueError("octoploid cytotype sampling strata drift")
    results: list[dict] = []
    for region in REGIONS:
        group = frame.loc[frame["region"] == region]
        sums = group.groupby("portfolio_bucket")["n_eggs"].sum().to_dict()
        total = int(group["n_eggs"].sum())
        confirmed = int(sums.get("exact_accepted_host_in_portfolio", 0))
        octoploid = int(sums.get("separately_reported_octoploid_cardamine", 0))
        other = int(sums.get("other_taxon_not_in_frozen_portfolio", 0))
        if confirmed + octoploid + other != total:
            raise ValueError("regional egg reconciliation drift")
        results.append({
            "region": region,
            "year": 2010,
            "total_published_eggs": total,
            "eggs_on_exact_frozen_portfolio_taxa": confirmed,
            "eggs_on_separate_octoploid_cardamine": octoploid,
            "eggs_on_other_unmatched_host_taxa": other,
            "strict_exact_portfolio_egg_share": confirmed / total,
            "hypothetical_share_if_octoploid_grouped": (
                confirmed + octoploid
            ) / total,
            "independent_programmes": "NOT_IDENTIFIED",
        })
    regions = pd.DataFrame(results)
    by_taxon = frame.groupby(
        ["species_as_published", "portfolio_bucket"],
        as_index=False, sort=True
    )["n_eggs"].sum().rename(columns={"n_eggs": "source_egg_total"})
    total = int(regions["total_published_eggs"].sum())
    confirmed = int(regions["eggs_on_exact_frozen_portfolio_taxa"].sum())
    octoploid = int(regions["eggs_on_separate_octoploid_cardamine"].sum())
    other = int(regions["eggs_on_other_unmatched_host_taxa"].sum())
    if (total, confirmed, octoploid, other) != (547, 200, 245, 102):
        raise ValueError("published 2010 egg totals / portfolio class drift")
    receipt = {
        "schema": "iwe_chocho_ambio2010_portfolio_coverage_v0.1",
        "source_doi": prior["source_doi"],
        "source_table": "Table 1",
        "total_eggs": total,
        "exact_frozen_portfolio_eggs": confirmed,
        "separate_octoploid_cardamine_eggs": octoploid,
        "other_documented_host_taxa_eggs": other,
        "exact_portfolio_coverage_fraction_of_eggs": confirmed / total,
        "hypothetical_with_octoploid_grouped_fraction": (
            confirmed + octoploid
        ) / total,
        "reported_host_taxa": 7,
        "strict_accepted_portfolio_host_taxa": 3,
        "octoploid_is_currently_mapped_to_species": False,
        "hypothetical_grouping_changes_actual_geography": False,
        "other_unmatched_taxa_are_true_nonhosts": False,
        "source_overlap_with_oikos2018": "possible_same_programme_not_independent",
        "regional_phenology_extracted": False,
        "independent_female_flight_observed": False,
        "plant_reproductive_fitness_observed": False,
        "strict_h1_effects_created": 0,
        "conclusion_ceiling": (
            "Reported host eggs are incompletely represented by the exact "
            "species-level chocho frozen accepted host portfolio; this is "
            "a source-coverage and taxonomic-grain diagnostic only."
        ),
    }
    return regions, by_taxon, receipt
