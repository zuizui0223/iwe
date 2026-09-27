from __future__ import annotations

from collections.abc import Mapping

import pandas as pd


CARDAMINE_CANDIDATE_ID = "ANT002_CARDAMINE_ANTHOCHARIS_2024"
CARDAMINE_SITE = "Dibbinsdale Nature Reserve"
CARDAMINE_REAL_YEARS = {2012, 2013, 2014}
CARDAMINE_RECORD_BASIS = "female_capture_recapture_events"


def validate_cardamine_adult_provenance(
    provenance: Mapping[str, object],
    adult_events: pd.DataFrame,
) -> list[str]:
    """Validate that an adult timing object has the frozen Cardamine provenance.

    A manifest cannot prove provenance by itself, but it prevents accidental use
    of known-inadmissible substitutes such as male records, old 2005-2010 MRR
    seasons, egg dates, or a different site.
    """
    required = {
        "candidate_id",
        "site",
        "sex",
        "record_basis",
        "years",
        "source_id",
        "source_backed",
        "synthetic_fixture",
    }
    missing = sorted(required - set(provenance))
    if missing:
        return [f"adult provenance missing fields: {', '.join(missing)}"]

    errors: list[str] = []
    if provenance["candidate_id"] != CARDAMINE_CANDIDATE_ID:
        errors.append("adult provenance candidate_id does not match Cardamine candidate")
    if provenance["site"] != CARDAMINE_SITE:
        errors.append("adult provenance site must be Dibbinsdale Nature Reserve")
    if str(provenance["sex"]).lower() != "female":
        errors.append("adult provenance must contain female records only")
    if provenance["record_basis"] != CARDAMINE_RECORD_BASIS:
        errors.append("adult provenance must use female capture/recapture events")

    source_id = str(provenance["source_id"]).strip()
    if not source_id:
        errors.append("adult provenance source_id must be non-empty")

    raw_years = provenance["years"]
    if not isinstance(raw_years, list) or not raw_years:
        errors.append("adult provenance years must be a non-empty list")
        declared_years: set[int] = set()
    else:
        try:
            declared_years = {int(year) for year in raw_years}
        except (TypeError, ValueError):
            declared_years = set()
            errors.append("adult provenance years must be integers")

    synthetic = provenance["synthetic_fixture"] is True
    source_backed = provenance["source_backed"] is True
    if synthetic:
        if not source_id.startswith("synthetic:"):
            errors.append("synthetic adult provenance source_id must start with synthetic:")
    else:
        if not source_backed:
            errors.append("real adult provenance must be explicitly source_backed")
        if declared_years != CARDAMINE_REAL_YEARS:
            errors.append("real adult provenance years must be exactly 2012, 2013, 2014")

    if "year" not in adult_events.columns or "event_doy" not in adult_events.columns:
        errors.append("adult_events must contain year and event_doy")
        return errors

    try:
        event_years = {int(year) for year in adult_events["year"].dropna().tolist()}
    except (TypeError, ValueError):
        event_years = set()
        errors.append("adult_events year values must be integers")

    if declared_years and event_years != declared_years:
        errors.append(
            f"adult event years {sorted(event_years)} do not match provenance years "
            f"{sorted(declared_years)}"
        )

    try:
        doys = pd.to_numeric(adult_events["event_doy"], errors="raise")
    except (TypeError, ValueError):
        errors.append("adult event_doy values must be numeric")
    else:
        if doys.isna().any() or ((doys < 1) | (doys > 366)).any():
            errors.append("adult event_doy values must lie within 1..366")

    return errors


def require_cardamine_adult_provenance(
    provenance: Mapping[str, object],
    adult_events: pd.DataFrame,
) -> None:
    errors = validate_cardamine_adult_provenance(provenance, adult_events)
    if errors:
        raise ValueError("; ".join(errors))
