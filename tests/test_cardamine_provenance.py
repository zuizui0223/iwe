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
