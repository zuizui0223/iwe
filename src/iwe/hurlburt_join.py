"""Fail-closed marked-unit provenance audit for Hurlburt 2004 (Onefour).

This audit deliberately DOES NOT calculate overlap, timing contrasts, Hedges g,
variance, or final plant fitness. It tests the *possibility* of joining one
source-marked flowering unit to a recorded mature-fruit fate and the presence of
an independently measured, same-season adult-census series.

Rows supplied by an analyst MUST be checked against the original thesis.
The public government annual summaries do not contain these join keys.
"""
from __future__ import annotations

from datetime import date

import pandas as pd

THESIS_DOI = "10.7939/r3-fe1d-kj80"
SITE = "Onefour"
YEARS = frozenset(range(1999, 2004))
UNIT_KEY = ("year", "clone_id", "inflorescence_id")
REQUIRED = {
    "flowering": set(UNIT_KEY) | {"first_flower_date", "last_flower_date"},
    "adult": {"year", "census_date", "adult_moth_count"},
    "mature_fruits": set(UNIT_KEY) | {"fruit_id", "viable_seeds"},
}
EVIDENCE_FIELDS = (
    "adult_census_source_locator",
    "flowering_unit_source_locator",
    "mature_fruit_source_locator",
    "fruit_to_marked_unit_link_source_locator",
)


def _nonblank(frame: pd.DataFrame, fields: tuple[str, ...], source: str) -> None:
    for field in fields:
        if frame[field].isna().any() or frame[field].astype(str).str.strip().eq("").any():
            raise ValueError(f"{source} lacks a source-backed {field}; no identifier imputation")


def _year(frame: pd.DataFrame, source: str) -> None:
    values = pd.to_numeric(frame["year"], errors="coerce")
    if values.isna().any() or (~values.isin(YEARS)).any():
        raise ValueError(f"{source}: only original Onefour 1999-2003 seasons allowed")
    frame["year"] = values.astype(int)


def _calendar(frame: pd.DataFrame, name: str, source: str) -> None:
    # ISO dates are required; no day-of-year reconstruction from annual counts.
    for value in frame[name]:
        try:
            parsed = date.fromisoformat(str(value))
        except (ValueError, TypeError):
            raise ValueError(f"{source}: {name} needs original full ISO dates") from None
        if parsed.year not in YEARS:
            raise ValueError(f"{source}: date is outside 1999-2003")
    _year(frame, source)
    if any(date.fromisoformat(str(v)).year != int(y)
           for v, y in zip(frame[name], frame["year"])):
        raise ValueError(f"{source}: {name} and year do not agree")


def _source_manifest(manifest: dict) -> str:
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    mode = manifest.get("mode")
    if mode not in {"original_source_review", "synthetic_fixture"}:
        raise ValueError("mode must be original_source_review or synthetic_fixture")
    if mode == "original_source_review":
        if manifest.get("thesis_doi") != THESIS_DOI or manifest.get("site") != SITE:
            raise ValueError("source manifest does not name Hurlburt thesis/Onefour")
        if manifest.get("original_pdf_inspected") is not True:
            raise ValueError("original thesis PDF review is required, not derivative summaries")
        for field in EVIDENCE_FIELDS:
            locator = manifest.get(field)
            if not isinstance(locator, str) or len(locator.strip()) < 8:
                raise ValueError("missing original-thesis page/table locator for " + field)
    return mode


def audit_marked_unit_join(
    flowering: pd.DataFrame, adult: pd.DataFrame,
    mature_fruits: pd.DataFrame, manifest: dict,
) -> dict:
    """Coverage/lineage gate only; never silently infer a fitness effect.

    Repeated fruits nested within one inflorescence do not become independent
    timing exposure units. Missing fruits are NOT assumed aborted or zero seed.
    """
    mode = _source_manifest(manifest)
    datasets = {
        "flowering": flowering.copy(),
        "adult": adult.copy(),
        "mature_fruits": mature_fruits.copy(),
    }
    for label, df in datasets.items():
        missing = REQUIRED[label] - set(df.columns)
        if missing:
            raise ValueError(f"{label}: missing {sorted(missing)}")
        if df.empty:
            raise ValueError(f"{label}: empty records cannot establish lineage")
        _year(df, label)

    f, a, m = (datasets[key] for key in ("flowering", "adult", "mature_fruits"))
    _nonblank(f, ("clone_id", "inflorescence_id"), "flowering")
    _nonblank(m, ("clone_id", "inflorescence_id", "fruit_id"), "mature_fruits")
    if f.duplicated(list(UNIT_KEY)).any():
        raise ValueError("duplicate source flowering inflorescence keys")
    if m.duplicated(list(UNIT_KEY) + ["fruit_id"]).any():
        raise ValueError("duplicate source fruit within marked inflorescence")
    _calendar(f, "first_flower_date", "flowering")
    _calendar(f, "last_flower_date", "flowering")
    if any(str(lo) > str(hi) for lo, hi in
           zip(f["first_flower_date"], f["last_flower_date"])):
        raise ValueError("flowering interval ends before it starts")
    _calendar(a, "census_date", "adult")
    adult_count = pd.to_numeric(a["adult_moth_count"], errors="coerce")
    if adult_count.isna().any() or (adult_count < 0).any():
        raise ValueError("adult counts must be measured non-negative values")
    if a.duplicated(["year", "census_date"]).any():
        raise ValueError("adult census duplicates a day; aggregate only with source support")
    # Moths were searched for *inside freshly open Yucca flowers*. These
    # observations are independent of egg/larva counts, but detection is
    # conditioned on availability of sampled host flowers. Never infer zeros
    # on unsampled days or an unconstrained external moth flight season.
    effort_recorded = "flowers_examined" in a.columns
    if effort_recorded:
        effort = pd.to_numeric(a["flowers_examined"], errors="coerce")
        if effort.isna().any() or (effort <= 0).any() or (effort % 1 != 0).any():
            raise ValueError("flowers_examined must be explicit positive integer effort")
    seeds = pd.to_numeric(m["viable_seeds"], errors="coerce")
    if seeds.isna().any() or (seeds < 0).any() or (seeds % 1 != 0).any():
        raise ValueError("mature viable seeds must be explicit non-negative integer counts")

    # Coverage must be evaluated by year and the full source-marked key.
    fkeys = set(map(tuple, f[list(UNIT_KEY)].itertuples(index=False, name=None)))
    mkeys = list(map(tuple, m[list(UNIT_KEY)].itertuples(index=False, name=None)))
    joined = [k in fkeys for k in mkeys]
    with_mature = set(k for k, ok in zip(mkeys, joined) if ok)
    years = sorted(set(f["year"]) | set(a["year"]) | set(m["year"]))
    period = {}
    for y in years:
        f_this = f[f["year"].eq(y)]
        a_this = a[a["year"].eq(y)]
        m_this = m[m["year"].eq(y)]
        unit_keys = set(map(tuple, f_this[list(UNIT_KEY)].itertuples(index=False, name=None)))
        matched = [
            tuple(k) in unit_keys
            for k in m_this[list(UNIT_KEY)].itertuples(index=False, name=None)
        ]
        period[str(y)] = {
            "marked_inflorescences": int(len(f_this)),
            "adult_census_days": int(len(a_this)),
            "recorded_mature_fruits": int(len(m_this)),
            "source_unit_joined_mature_fruits": int(sum(matched)),
            "unmatched_mature_fruits": int(len(m_this) - sum(matched)),
            "matched_inflorescences_with_mature_fruits": int(
                len({tuple(k) for k, ok in zip(
                    m_this[list(UNIT_KEY)].itertuples(index=False, name=None),
                    matched) if ok})
            ),
        }

    independent_adult_series = any(
        v["adult_census_days"] >= 2
        and v["matched_inflorescences_with_mature_fruits"] >= 2
        for v in period.values()
    )
    if not any(joined):
        status = "blocked_no_mature_fruit_to_marked_flowering_unit_join"
    elif any(not x for x in joined):
        status = "blocked_partial_matched_subset_selection_risk"
    elif not independent_adult_series:
        status = "blocked_insufficient_same_season_adult_and_linked_units"
    else:
        status = "source_unit_lineage_structurally_present_not_an_effect"

    return {
        "schema": "iwe_hurlburt2004_marked_unit_join_audit_v1",
        "source": THESIS_DOI,
        "site": SITE,
        "mode": mode,
        "status": status,
        "year_breakdown": period,
        "total_marked_inflorescences": len(f),
        "total_mature_fruits": len(m),
        "mature_fruits_with_exact_marked_unit_join": sum(joined),
        "unmatched_mature_fruits": len(joined) - sum(joined),
        "linked_marked_inflorescences": len(with_mature),
        "date_resolved_adult_and_mature_fruit_join_present": bool(
            mode == "original_source_review"
            and status == "source_unit_lineage_structurally_present_not_an_effect"
        ),
        "original_source_verification_required": True,
        "unobserved_aborted_fruits_imputed": False,
        "annual_partner_abundance_as_synchrony": False,
        "adult_census_detection_context": "moths_counted_within_fresh_host_flowers",
        "flowers_examined_per_census_recorded": effort_recorded,
        "unsampled_adult_activity_imputed_zero": False,
        "independent_unconditional_adult_flight_window_verified": False,
        "source_defined_timing_contrast_frozen": False,
        "plant_fitness_effect_estimated": False,
        "strict_h1_effect_promoted": False,
        "confirmatory_stage_prediction_supported": False,
        "limits": (
            "This checks exact marked IDs and within-year adult census support, "
            "not original identifier authenticity or biological exposure alignment; "
            "multiple fruits share one marked inflorescence. Absence from the mature "
            "fruit file is not zero reproductive fitness. Timing grouping, net plant "
            "output/abortion, sampling variance, and independent adult-to-stage "
            "prediction require separately preregistered source auditing. Adult "
            "moths were surveyed inside fresh flowers; a non-surveyed day cannot "
            "be classified as true adult absence."
        ),
    }
