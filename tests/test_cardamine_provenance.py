import pandas as pd
import pytest

from iwe.cardamine_provenance import (
    CARDAMINE_CANDIDATE_ID,
    CARDAMINE_SITE,
    validate_cardamine_adult_provenance,
    require_cardamine_adult_provenance,
)


def _events(years=(2012, 2013, 2014)):
    rows = []
    for year in years:
        rows.extend(
            [
                {"year": year, "event_doy": 110},
                {"year": year, "event_doy": 120},
            ]
        )
    return pd.DataFrame(rows)


def _provenance(**overrides):
    item = {
        "candidate_id": CARDAMINE_CANDIDATE_ID,
        "site": CARDAMINE_SITE,
        "sex": "female",
        "record_basis": "female_capture_recapture_events",
        "years": [2012, 2013, 2014],
        "source_id": "author_archive:cardamine_2012_2014_female_mrr",
        "source_backed": True,
        "synthetic_fixture": False,
        "adult_event_doy_basis": "calendar_day_of_year",
        "plant_observation_doy_basis": "calendar_day_of_year",
        "adult_calendar_origin_source_locator": "original 2012-2014 female capture/recapture calendar-date records",
        "figure_digitization_performed": False,
    }
    item.update(overrides)
    return item


def test_real_cardamine_provenance_passes():
    assert validate_cardamine_adult_provenance(_provenance(), _events()) == []


def test_old_mrr_years_cannot_substitute():
    errors = validate_cardamine_adult_provenance(
        _provenance(years=[2005, 2006]),
        _events((2005, 2006)),
    )
    assert any("exactly 2012, 2013, 2014" in error for error in errors)


def test_male_or_egg_records_fail():
    errors = validate_cardamine_adult_provenance(
        _provenance(sex="male", record_basis="egg_dates"),
        _events(),
    )
    assert any("female records only" in error for error in errors)
    assert any("capture/recapture" in error for error in errors)


def test_manifest_years_must_equal_event_years():
    errors = validate_cardamine_adult_provenance(
        _provenance(),
        _events((2012, 2013)),
    )
    assert any("do not match provenance years" in error for error in errors)


def test_invalid_doy_fails():
    events = _events()
    events.loc[0, "event_doy"] = 400
    with pytest.raises(ValueError, match="1..366"):
        require_cardamine_adult_provenance(_provenance(), events)


def test_synthetic_fixture_can_use_subset_years_but_is_labeled():
    provenance = _provenance(
        years=[2012],
        source_id="synthetic:cardamine_preflight",
        source_backed=False,
        synthetic_fixture=True,
    )
    assert validate_cardamine_adult_provenance(provenance, _events((2012,))) == []



def test_fractional_years_do_not_truncate_to_focal_year():
    provenance = _provenance(years=[2012.5, 2013, 2014])
    errors = validate_cardamine_adult_provenance(provenance, _events())
    assert any("integer years" in error for error in errors)

    events = _events()
    events["year"] = events["year"].astype(float)
    events.loc[0, "year"] = 2012.5
    errors = validate_cardamine_adult_provenance(_provenance(), events)
    assert any("integer years" in error for error in errors)


def test_figure_day1_relative_records_are_not_calendar_DOY_even_if_numeric():
    # All nominal days are 110 or 120 and hence pass basic numeric bounds.
    errors = validate_cardamine_adult_provenance(
        _provenance(adult_event_doy_basis="figure4_day1_relative"),
        _events(),
    )
    assert any("Figure-4 relative Day 1" in e for e in errors)


def test_undocumented_calendar_origin_fails_closed():
    for override in (
        {"adult_event_doy_basis": None},
        {"plant_observation_doy_basis": "first_plant_flower_day1"},
        {"adult_calendar_origin_source_locator": ""},
        {"figure_digitization_performed": True},
    ):
        errors = validate_cardamine_adult_provenance(
            _provenance(**override), _events()
        )
        assert errors


def test_non_leap_calendar_day_366_is_not_admissible():
    events = _events()
    events.loc[events["year"].eq(2013), "event_doy"] = 366
    errors = validate_cardamine_adult_provenance(_provenance(), events)
    assert any("exceeds year=2013" in e for e in errors)


def test_leap_year_2012_day_366_is_permitted_as_a_calendar_day():
    events = _events()
    events.loc[events["year"].eq(2012), "event_doy"] = 366
    assert validate_cardamine_adult_provenance(_provenance(), events) == []
