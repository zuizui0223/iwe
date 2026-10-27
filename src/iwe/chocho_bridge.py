"""Auditable, non-promoting bridge from IWE candidates to chocho host-resource data.

The chocho metric is a butterfly-level union of *all* known hosts.  It is not
host-pair geography, regional interaction evidence, or a phenological effect.
This module never writes to IWE's strict-H1 extraction or adjudication files.
"""

from __future__ import annotations

import math
import re
from typing import Optional

import pandas as pd

from iwe.overlap import normalized_overlap


CANDIDATE_FIELDS = {"candidate_id", "animal_taxon", "plant_taxon", "target_class", "status"}
RESOURCE_FIELDS = {
    "species",
    "native_resource_units",
    "contemporary_resource_units",
    "introduced_added_units",
    "resolved_host_species",
}
RESOURCE_COUNT_FIELDS = (
    "native_resource_units",
    "contemporary_resource_units",
    "introduced_added_units",
    "resolved_host_species",
)
WINDOW_FIELDS = {
    "candidate_id",
    "host_taxon",
    "wgsrpd3_unit",
    "year",
    "range_origin",
    "host_range_source",
    "host_window_source",
    "partner_window_source",
    "host_window_basis",
    "partner_window_basis",
    "host_start_doy",
    "host_end_doy",
    "partner_start_doy",
    "partner_end_doy",
}
CROSSWALK_COLUMNS = [
    "candidate_id", "animal_taxon", "plant_taxon", "interaction_type",
    "iwe_candidate_status", "chocho_species", "resolved_host_species",
    "native_resource_units", "contemporary_resource_units",
    "introduced_added_units", "geographic_expansion_ratio",
    "geographic_aggregation", "host_pair_status", "temporal_status",
    "strict_h1_effect_admitted",
]
TEMPORAL_COLUMNS = [
    "candidate_id", "animal_taxon", "host_taxon", "wgsrpd3_unit", "year",
    "range_origin", "phenophase_jaccard", "host_window_fraction",
    "source_tier", "strict_h1_effect_admitted",
]


def _require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{label}: missing columns: {', '.join(missing)}")


def _exact_binomial(value: object) -> Optional[str]:
    """No spp., genus-only, abbreviated or composite records are guessed."""
    if not isinstance(value, str):
        return None
    stripped = " ".join(value.split())
    if re.fullmatch(r"[A-Z][a-z]+\s+[a-z][a-z-]+", stripped):
        return stripped
    return None


def _resources(metrics: pd.DataFrame) -> pd.DataFrame:
    _require_columns(metrics, RESOURCE_FIELDS, "chocho metrics")
    result = metrics.copy()
    result["species"] = result["species"].astype("string").str.strip()
    if result["species"].isna().any() or result["species"].eq("").any():
        raise ValueError("chocho metrics: empty species")
    if result["species"].duplicated().any():
        raise ValueError("chocho metrics: duplicate species")
    for field in RESOURCE_COUNT_FIELDS:
        values = pd.to_numeric(result[field], errors="coerce")
        if values.isna().any() or (values < 0).any() or (~(values % 1 == 0)).any():
            raise ValueError(f"chocho metrics: invalid nonnegative count: {field}")
        result[field] = values.astype("int64")
    if (
        result["contemporary_resource_units"] - result["native_resource_units"]
        != result["introduced_added_units"]
    ).any():
        raise ValueError("chocho metrics: geographic increments do not reconcile")
    return result


def build_candidate_resource_crosswalk(
    candidates: pd.DataFrame,
    resource_metrics: pd.DataFrame,
    host_pairs: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Exact species match only; pair identity is audited separately.

    Neither a name match nor a verified HOSTS pair promotes an IWE effect.
    """
    _require_columns(candidates, CANDIDATE_FIELDS, "IWE candidate registry")
    if candidates["candidate_id"].isna().any() or candidates["candidate_id"].duplicated().any():
        raise ValueError("IWE candidate registry: missing/duplicate candidate_id")
    resources = _resources(resource_metrics)
    known_pairs: Optional[set[tuple[str, str]]] = None
    if host_pairs is not None:
        _require_columns(host_pairs, {"insect_species", "accepted_name"}, "HOSTS sidecar")
        known_pairs = set(
            (str(insect).strip(), str(host).strip())
            for insect, host in zip(host_pairs["insect_species"], host_pairs["accepted_name"])
            if pd.notna(insect) and pd.notna(host)
        )
    registry = candidates.copy()
    registry["_exact_animal"] = registry["animal_taxon"].map(_exact_binomial)
    joined = registry.loc[registry["_exact_animal"].notna()].merge(
        resources, left_on="_exact_animal", right_on="species",
        how="inner", validate="many_to_one", sort=False,
    )
    records: list[dict[str, object]] = []
    for _, row in joined.iterrows():
        native = int(row["native_resource_units"])
        contemporary = int(row["contemporary_resource_units"])
        plant = str(row["plant_taxon"]).strip()
        species = str(row["species"])
        pair = (species, plant)
        pair_status = (
            "not_checked" if known_pairs is None
            else "confirmed_in_hosts_sidecar" if pair in known_pairs
            else "not_found_in_supplied_sidecar"
        )
        records.append({
            "candidate_id": str(row["candidate_id"]),
            "animal_taxon": str(row["animal_taxon"]).strip(),
            "plant_taxon": plant,
            "interaction_type": str(row["target_class"]),
            "iwe_candidate_status": str(row["status"]),
            "chocho_species": species,
            "resolved_host_species": int(row["resolved_host_species"]),
            "native_resource_units": native,
            "contemporary_resource_units": contemporary,
            "introduced_added_units": int(row["introduced_added_units"]),
            "geographic_expansion_ratio": contemporary / native if native else float("nan"),
            "geographic_aggregation": "butterfly_union_all_resolved_hosts",
            "host_pair_status": pair_status,
            "temporal_status": "not_evaluated",
            "strict_h1_effect_admitted": False,
        })
    return pd.DataFrame(records, columns=CROSSWALK_COLUMNS).sort_values(
        "candidate_id", kind="stable"
    ).reset_index(drop=True)


def _interval(value_start: object, value_end: object, label: str) -> tuple[float, float]:
    try:
        start, end = float(value_start), float(value_end)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{label}: invalid DOY") from exc
    if not (math.isfinite(start) and math.isfinite(end) and 1 <= start < end <= 367):
        raise ValueError(f"{label}: require 1 <= start < end <= 367 (half-open)")
    return start, end


def screen_spatiotemporal_windows(
    windows: pd.DataFrame,
    crosswalk: pd.DataFrame,
    *,
    allow_synthetic: bool = False,
) -> pd.DataFrame:
    """Potential phenophase screening, never fitness or strict-H1 inference.

    Requires a confirmed *species-level* host pair from a HOSTS sidecar and
    independent adult activity / observed host phenophase inputs at the same
    regional unit and year.  Does not create missing windows or infer zeros.
    """
    _require_columns(windows, WINDOW_FIELDS, "seasonal windows")
    _require_columns(crosswalk, set(CROSSWALK_COLUMNS), "IWE-chocho crosswalk")
    if crosswalk["candidate_id"].duplicated().any():
        raise ValueError("crosswalk: duplicate candidate_id")
    if windows.empty:
        return pd.DataFrame(columns=TEMPORAL_COLUMNS)
    keys = ["candidate_id", "host_taxon", "wgsrpd3_unit", "year"]
    if windows.duplicated(subset=keys).any():
        raise ValueError("seasonal windows: duplicated candidate/host/region/year")
    lookup = crosswalk.set_index("candidate_id")
    output: list[dict[str, object]] = []
    for _, row in windows.iterrows():
        candidate_id = str(row["candidate_id"]).strip()
        if candidate_id not in lookup.index:
            raise ValueError(f"seasonal windows: unknown candidate {candidate_id}")
        match = lookup.loc[candidate_id]
        if match["host_pair_status"] != "confirmed_in_hosts_sidecar":
            raise ValueError(f"{candidate_id}: host pair not confirmed by the supplied sidecar")
        host = str(row["host_taxon"]).strip()
        if host != match["plant_taxon"]:
            raise ValueError(f"{candidate_id}: host taxon differs from IWE candidate")
        if row["range_origin"] not in {"native", "introduced"}:
            raise ValueError(f"{candidate_id}: range_origin requires a sourced native/introduced label")
        if str(row["partner_window_basis"]).strip() != "independent_adult_activity":
            raise ValueError(f"{candidate_id}: partner window must be independent adult activity")
        if str(row["host_window_basis"]).strip() != "observed_host_phenophase":
            raise ValueError(f"{candidate_id}: host window must be observed host phenophase")
        for field in ("wgsrpd3_unit", "host_range_source", "host_window_source", "partner_window_source"):
            value = row[field]
            if pd.isna(value) or not str(value).strip():
                raise ValueError(f"{candidate_id}: missing {field}")
            if not allow_synthetic and str(value).strip().lower().startswith("synthetic:"):
                raise ValueError(f"{candidate_id}: synthetic provenance cannot support a real screening receipt")
        year = pd.to_numeric(row["year"], errors="coerce")
        if pd.isna(year) or not math.isfinite(float(year)) or year % 1 != 0 or year < 1800:
            raise ValueError(f"{candidate_id}: invalid year")
        host_start, host_end = _interval(
            row["host_start_doy"], row["host_end_doy"], "host window"
        )
        partner_start, partner_end = _interval(
            row["partner_start_doy"], row["partner_end_doy"], "partner window"
        )
        intersection = max(
            0.0, min(host_end, partner_end) - max(host_start, partner_start)
        )
        output.append({
            "candidate_id": candidate_id,
            "animal_taxon": match["chocho_species"],
            "host_taxon": host,
            "wgsrpd3_unit": str(row["wgsrpd3_unit"]).strip(),
            "year": int(year),
            "range_origin": row["range_origin"],
            "phenophase_jaccard": normalized_overlap(
                host_start, host_end, partner_start, partner_end
            ),
            "host_window_fraction": intersection / (host_end - host_start),
            "source_tier": "proxy_only",
            "strict_h1_effect_admitted": False,
        })
    return pd.DataFrame(output, columns=TEMPORAL_COLUMNS).sort_values(
        keys, kind="stable"
    ).reset_index(drop=True)
