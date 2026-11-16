"""Never promote a public source label into a same-plant causal stage estimate."""
import pytest

from scripts.probe_hofer2022_resource_gate import (
    PINNED, _reader, exact_url, inspect_original, get_original,
)


def test_pinned_record_only():
    assert len(PINNED) == 5
    assert exact_url("Int_data.csv") == (
        "https://zenodo.org/records/7335086/files/Int_data.csv?download=1"
    )
    with pytest.raises(ValueError, match="off-record"):
        exact_url("private_or_unverified.xlsx")


def test_source_csv_fields_and_true_missingness_not_zeros():
    raw = (
        b"Plant_ID,Date,Visits,Seeds,Water\n"
        b"A,2022-05-10,5,10,wet\n"
        b"B,2022-05-10,NA,,dry\n"
    )
    names, rows, delim = _reader(raw)
    assert names == ["Plant_ID", "Date", "Visits", "Seeds", "Water"]
    assert delim == ","
    res = inspect_original("Int_data.csv", raw)
    assert res["n_original_rows"] == 2
    assert res["missing_by_header"]["Seeds"] == 1
    assert res["missing_by_header"]["Visits"] == 1
    assert res["timing_id_endpoint_header_candidates"]
    assert res["one_plant_multi_stage_join_verified"] is False
    assert res["interaction_time_predictive_effect_estimated"] is False


def test_alternate_delimiter_and_malformed_rows():
    cols, rows, sep = _reader(
        b"plant;visit;seed\nA;3;10\nB;4;12\n"
    )
    assert sep == ";"
    assert rows[0]["seed"] == "10"
    with pytest.raises(ValueError, match="extra source CSV cells"):
        _reader(b"plant,seed\nA,1,extra\n")


def test_source_bytes_verified_before_either_readme_or_results(monkeypatch):
    import scripts.probe_hofer2022_resource_gate as mod
    class Res:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self, n): return b"unverified original"
    monkeypatch.setattr(mod, "urlopen", lambda *a, **k: Res())
    with pytest.raises(ValueError, match="MD5 mismatch"):
        get_original("Plantlist.csv")


def test_readme_returns_leads_not_unverified_join():
    result = inspect_original("README.md", (
        b"plant id counts\n"
        b"visitation measured at date\n"
        b"seed set measured at harvest\n"
    ))
    assert len(result["likely_unit_or_endpoint_definitions"]) == 3
    assert result["outcome_join_verified"] is False
