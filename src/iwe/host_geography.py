"""Rebuild focal-host contributions to chocho's WCVP level-3 resource regions.

Potential region-level larval-resource availability only; never inferred adult
activity, egg laying, occupied range, colonization, or plant fitness.
"""
from __future__ import annotations

from collections import defaultdict
import math
import pandas as pd


PAIR_COLS = {"insect_species", "accepted_plant_name_id", "accepted_name"}
REGION_COLS = {"accepted_plant_name_id", "area_code_l3"}
METRIC_COLS = {
    "species", "native_resource_units", "contemporary_resource_units",
    "introduced_added_units", "resolved_host_species",
}


def _require(df: pd.DataFrame, columns: set[str], label: str) -> None:
    missing = sorted(columns - set(df.columns))
    if missing:
        raise ValueError(f"{label}: missing columns {missing}")


def _text(value: object) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _region_sets(df: pd.DataFrame, label: str) -> dict[str, set[str]]:
    _require(df, REGION_COLS, label)
    result: dict[str, set[str]] = defaultdict(set)
    for _, row in df.iterrows():
        plant, unit = _text(row["accepted_plant_name_id"]), _text(row["area_code_l3"])
        if not plant or not unit:
            raise ValueError(f"{label}: empty plant ID or region code")
        result[plant].add(unit)
    return result


def _count(value: object, name: str) -> int:
    try:
        v = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}: not numeric") from exc
    if not math.isfinite(v) or v < 0 or not v.is_integer():
        raise ValueError(f"{name}: count must be nonnegative integer")
    return int(v)


def analyze_focal_host_geography(
    *, pairs: pd.DataFrame, native_units: pd.DataFrame,
    contemporary_units: pd.DataFrame, species_metrics: pd.DataFrame,
    butterfly: str = "Anthocharis cardamines",
    focal_host: str = "Cardamine pratensis",
) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    _require(pairs, PAIR_COLS, "HOSTS pairs")
    _require(species_metrics, METRIC_COLS, "chocho metrics")
    native = _region_sets(native_units, "native")
    contemporary = _region_sets(contemporary_units, "contemporary")
    filtered = pairs.loc[pairs["insect_species"].map(_text) == butterfly]
    if filtered.empty:
        raise ValueError("no source-backed HOSTS pairs for focal butterfly")

    hosts: dict[str, str] = {}
    for _, row in filtered.iterrows():
        ident, name = _text(row["accepted_plant_name_id"]), _text(row["accepted_name"])
        if not ident or not name:
            raise ValueError("unresolved name/ID for a focal butterfly host")
        if ident in hosts and hosts[ident] != name:
            raise ValueError("inconsistent accepted name for plant ID " + ident)
        hosts[ident] = name

    ms = species_metrics.loc[species_metrics["species"].map(_text) == butterfly]
    if len(ms) != 1:
        raise ValueError("expected one pinned chocho metrics row")
    met = ms.iloc[0]
    if len(hosts) != _count(met["resolved_host_species"], "resolved_host_species"):
        raise ValueError("frozen resolved host count drift")

    for ident in hosts:
        if not native[ident].issubset(contemporary[ident]):
            raise ValueError("native not subset of contemporary for host " + ident)

    native_total = set().union(*(native[i] for i in hosts))
    contemporary_total = set().union(*(contemporary[i] for i in hosts))
    if not native_total.issubset(contemporary_total):
        raise ValueError("native butterfly geography not subset of contemporary")
    added = contemporary_total - native_total
    for field, actual in (
        ("native_resource_units", len(native_total)),
        ("contemporary_resource_units", len(contemporary_total)),
        ("introduced_added_units", len(added)),
    ):
        if actual != _count(met[field], field):
            raise ValueError(f"chocho frozen {field} drift: rebuild={actual}")

    matches = [ident for ident, name in hosts.items() if name == focal_host]
    if len(matches) > 1:
        raise ValueError("ambiguous focal host accepted ID")
    focal_id = matches[0] if matches else None
    cover = {
        unit: [ident for ident in sorted(hosts) if unit in contemporary[ident]]
        for unit in sorted(added)
    }
    if any(not ids for ids in cover.values()):
        raise ValueError("added butterfly unit without host")

    covered = defaultdict(int)
    exclusive = defaultdict(int)
    fractional = defaultdict(float)
    for ids in cover.values():
        for ident in ids:
            covered[ident] += 1
            fractional[ident] += 1 / len(ids)
        if len(ids) == 1:
            exclusive[ids[0]] += 1
    if not math.isclose(sum(fractional.values()), len(added), abs_tol=1e-9):
        raise ValueError("fractional credit does not sum to added units")

    host_records = [{
        "accepted_plant_name_id": ident,
        "accepted_name": hosts[ident],
        "native_host_units": len(native[ident]),
        "contemporary_host_units": len(contemporary[ident]),
        "introduced_only_host_units": len(contemporary[ident] - native[ident]),
        "butterfly_added_units_covered": covered[ident],
        "butterfly_added_units_exclusively_covered": exclusive[ident],
        "fractional_added_unit_credit": fractional[ident],
        "is_focal_host": bool(ident == focal_id),
    } for ident in sorted(hosts)]
    region_records = [{
        "wgsrpd3_unit": unit,
        "is_new_resource_unit": True,
        "n_available_hosts": len(ids),
        "focal_host_status": (
            "not_verified_in_HOSTS_source" if focal_id is None
            else "available" if focal_id in ids else "not_in_this_host_union"
        ),
        "focal_exclusively_supplies_unit": (
            None if focal_id is None
            else bool(focal_id in ids and len(ids) == 1)
        ),
    } for unit, ids in cover.items()]
    result = {
        "schema": "iwe_chocho_focal_host_geography_v0.1",
        "butterfly": butterfly,
        "focal_host": focal_host,
        "source_pair_status": (
            "confirmed_exact_in_chocho_HOSTS_sidecar" if focal_id
            else "not_found_exact_in_this_HOSTS_sidecar"
        ),
        "focal_accepted_plant_id": focal_id,
        "resolved_hosts": len(hosts),
        "native_butterfly_units": len(native_total),
        "contemporary_butterfly_units": len(contemporary_total),
        "added_butterfly_units": len(added),
        "focal_native_units": len(native[focal_id]) if focal_id else None,
        "focal_contemporary_units": len(contemporary[focal_id]) if focal_id else None,
        "focal_introduced_only_units": (
            len(contemporary[focal_id] - native[focal_id]) if focal_id else None
        ),
        "added_units_covered_by_focal": covered[focal_id] if focal_id else None,
        "added_units_exclusively_covered_by_focal": exclusive[focal_id] if focal_id else None,
        "fractional_added_units_focal": fractional[focal_id] if focal_id else None,
        "fractional_credit_sum": sum(fractional.values()),
        "regional_pheno_observed": False,
        "regional_host_use_observed": False,
        "strict_h1_effects_created": 0,
        "interpretation": "Potential host-region union only; not occupancy, interaction timing, seed fitness, or invasion causation.",
    }
    return (
        result,
        pd.DataFrame(host_records).sort_values("accepted_name", kind="stable").reset_index(drop=True),
        pd.DataFrame(region_records).sort_values("wgsrpd3_unit", kind="stable").reset_index(drop=True),
    )
