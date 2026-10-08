import pytest

from scripts.recover_iwe015_dryad import (
    DOI,
    SOURCE_FILES,
    inspect_payload,
    source_urls,
)


def test_source_file_ids_are_pinned_and_complete():
    assert DOI == "10.5061/dryad.6q573n5w1"
    assert SOURCE_FILES == {
        "2012_early_female.csv": 278487,
        "2012_late_female.csv": 278488,
        "2013_early_female.csv": 278490,
        "2013_late_female.csv": 278492,
        "data_analysis.R": 278500,
        "README.txt": 278498,
    }
    for file_id in SOURCE_FILES.values():
        assert all("datadryad.org/" in url and str(file_id) in url
                   for url in source_urls(file_id))


def test_csv_probe_reports_schema_without_inventing_effect_sizes():
    payload = b"plant_id,fruit_count,leaf_area\n1,5,1.5\n2,0,2.0\n"
    record = inspect_payload("2012_early_female.csv", payload)
    assert record["columns"] == ["plant_id", "fruit_count", "leaf_area"]
    assert record["n_data_rows"] == 2
    assert len(record["sha256"]) == 64
    assert "hedges_g" not in record
    assert "dispersion" not in record


@pytest.mark.parametrize("payload", [
    b"",
    b"<html><head>Rate limited</head></html>",
    b"<!DOCTYPE html><html>Forbidden</html>",
    b"Access Denied by CDN",
    b"plant_id,fruit_count\n1,3\n2,2\n",
    b"a,b,c\n1,2,3\n",
    b"a,a,b\n1,2,3\n2,3,4\n",
])
def test_probe_rejects_error_pages_and_incomplete_csv(payload):
    with pytest.raises(ValueError):
        inspect_payload("2012_early_female.csv", payload)


def test_short_script_does_not_masquerade_as_source_code():
    with pytest.raises(ValueError):
        inspect_payload("data_analysis.R", b"no")
