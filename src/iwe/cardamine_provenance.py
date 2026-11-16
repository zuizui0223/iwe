from __future__ import annotations

from collections.abc import Mapping
from calendar import isleap

import pandas as pd


CARDAMINE_CANDIDATE_ID = "ANT002_CARDAMINE_ANTHOCHARIS_2024"
CARDAMINE_SITE = "Dibbinsdale Nature Reserve"
CARDAMINE_REAL_YEARS = {2012, 2013, 2014}
CARDAMINE_RECORD_BASIS = "female_capture_recapture_events"


def _integer_year_set(values: object, label: str) -> tuple[set[int], list[str]]:
    if not isinstance(values, (list, tuple, pd.Series)) or len(values) == 0:
        return set(), [f"{label} must be a non-empty sequence of integer years"]

    years: set[int] = set()
    errors: list[str] = []
    for value in values:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            errors.append(f"{label} values must be integer years")
            continue
        if not numeric.is_integer():
            errors.append(f"{label} values must be integer years")
            continue
        years.add(int(numeric))
    return years, errors


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

    declared_years, year_errors = _integer_year_set(
        provenance["years"], "adult provenance years"
    )
    errors.extend(year_errors)

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

        # Figures 2 and 4 in Davies & Saccheri (2024) reset Day 1 to
        # the first observed early-ecotype flowering date *separately*
        # for each year. The raw Dryad transect Date is calendar DOY.
        # Both may contain numbers between 1 and 366; range validation
        # alone cannot detect a biologically disastrous origin mismatch.
        for field in ("adult_event_doy_basis", "plant_observation_doy_basis"):
            if provenance.get(field) != "calendar_day_of_year":
                errors.append(
                    f"real Cardamine {field} must explicitly be "
                    "calendar_day_of_year; Figure-4 relative Day 1 is "
                    "not an absolute DOY"
                )
        locator = provenance.get("adult_calendar_origin_source_locator")
        if not isinstance(locator, str) or len(locator.strip()) < 12:
            errors.append(
                "real adult events require a specific original capture/recapture "
                "calendar-date column or reviewed year-specific origin locator"
            )
        if provenance.get("figure_digitization_performed") is not False:
            errors.append(
                "real adult events must declare figure_digitization_performed=false; "
                "Figure 4 graphical values are not raw event dates"
            )

    if "year" not in adult_events.columns or "event_doy" not in adult_events.columns:
        errors.append("adult_events must contain year and event_doy")
        return errors

    event_years, event_year_errors = _integer_year_set(
        adult_events["year"].dropna().tolist(), "adult_events year"
    )
    errors.extend(event_year_errors)

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
        # A non-leap-year day 366 can be numerically plausible in a
        # graph but never an actual calendar date.
        if "year" in adult_events:
            for y, d in zip(adult_events["year"], doys):
                try:
                    yy = int(y)
                    if float(y) != yy:
                        continue  # independently flagged as non-integer
                except (ValueError, TypeError, OverflowError):
                    continue
                if pd.notna(d) and float(d) > (366 if isleap(yy) else 365):
                    errors.append(
                        f"calendar DOY exceeds year={yy} day limit"
                    )
                    break

    return errors


def require_cardamine_adult_provenance(
    provenance: Mapping[str, object],
    adult_events: pd.DataFrame,
) -> None:
    errors = validate_cardamine_adult_provenance(provenance, adult_events)
    if errors:
        raise ValueError("; ".join(errors))
