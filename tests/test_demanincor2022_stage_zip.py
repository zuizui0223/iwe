"""Synthetic software-only fixtures: never count test records as ecology."""
from __future__ import annotations
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import pytest

from scripts.probe_demanincor2022_stage_zip import (
    DOI, FILES, original_url, fetch_original, sniff_csv_headers,
    validate_member_name, inspect_archive, inspect_analysis_script,
    profile_zip_tables,
)


def zip_fixture(paths: dict[str, bytes]) -> bytes:
    obj = BytesIO()
    with ZipFile(obj, "w", compression=ZIP_DEFLATED) as z:
        for name, data in paths.items():
            z.writestr(name, data)
    return obj.getvalue()


def test_only_exact_immutable_2022_zenodo_record_allowed():
    assert DOI == "10.5281/zenodo.17830772"
    assert original_url("deManincor-et-al.2025_data_pSEM.zip") == (
        "https://zenodo.org/records/17830772/files/"
        "deManincor-et-al.2025_data_pSEM.zip?download=1"
    )
    assert len(FILES) == 2
    with pytest.raises(ValueError, match="off-record"):
        original_url("outcome.csv")


def test_member_path_and_software_gate():
    validate_member_name("Data/seed_germination.csv")
    for name in ("../fake.csv", "/tmp/outcome.csv", "x/../bad.csv",
                 r"Data\evil.csv", "malicious.sh"):
        with pytest.raises(ValueError, match="untrusted|executable"):
            validate_member_name(name)


def test_source_archive_metadata_only_and_missing_cells_not_filled():
    zipped = zip_fixture({
        "Data/bee_abund_2022.csv":
            b"room,arena,day,bee_density\nC1,1,91,2\nC1,1,92,NA\n",
        "Data/data_seed_germ_pSEM.csv":
            b"room,plant_ID,germination,seed_survival\nC1,P2,1,\n",
        "metadata/readme.txt":
            b"plant id room and arena are not matched until checked\n",
    })
    res = inspect_archive(zipped)
    assert res["n_members"] == 3
    assert res["member_formats"][".csv"] == 2
    assert res["expanded_bytes"] > 0
    d = {x["source_member_name"]:x for x in res["members"]}
    assert "bee_density" in d["Data/bee_abund_2022.csv"][
        "table_profile"]["timing_or_unit_columns"]
    assert "seed_survival" in d["Data/data_seed_germ_pSEM.csv"][
        "table_profile"]["headers"]
    assert d["Data/data_seed_germ_pSEM.csv"][
        "table_profile"]["full_source_rows_released"] is False


def test_duplicate_original_column_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        sniff_csv_headers(b"room,room,bee_density\nC1,C1,3\n", "foo.csv")


def test_no_reproduction_claim_before_same_unit_linkage():
    z = inspect_analysis_script(b"""
    dat <- read.csv('fruit.csv')
    flowers <- read.csv('flower_count.csv')
    fitted <- pSEM(dat)
    """)
    assert z["n_lines"] >= 3
    assert z["source_stage_or_join_expressions"]


def test_source_file_bytes_must_match_published_md5(monkeypatch):
    import scripts.probe_demanincor2022_stage_zip as mod
    class Dummy:
        def __enter__(self): return self
        def __exit__(self, *args): return None
        def read(self, n): return b"forged dataset"
    monkeypatch.setattr(mod, "urlopen", lambda *args, **kwargs: Dummy())
    with pytest.raises(ValueError, match="MD5"):
        fetch_original("deManincor-et-al.2025_data_pSEM.zip")


def test_invalid_zip_must_fail_closed_not_just_emit_good_status(monkeypatch):
    import scripts.probe_demanincor2022_stage_zip as m
    monkeypatch.setattr(
        m, "fetch_original",
        lambda name: b"not an archive" if name.endswith(".zip")
        else b"valid-looking R script",
    )
    result = m.audit()
    assert result["source_verified"] is False
    assert result["matched_plant_to_final_seed_germination_verified"] is False
    assert result["status"] == "source_unavailable_or_source_shape_changed"


def test_exact_2022_stage_tables_profile_candidate_grain_and_nulls():
    data = zip_fixture({
        "data_seeds_germ_pSEM.txt":
            b"trtmt\tarena\tsp\tplant_flwr_ID\tseeds\tgerm\tcotyl\n"
            b"C\t1\tCH\tP1_F1\t10\t3\t2\n"
            b"C\t1\tCH\tP1_F2\t20\tNA\tNA\n",
        "data_bee_nest_pSEM.txt":
            b"trtmt\tarena\tsp\tplant_flwr_ID\tcells\nC\t1\tCH\tP1_F1\t2\n",
        "bee_abund_2022.txt":
            b"DOY\ttrtmt\tarena\tbees\n140\tC\t1\t3\n",
        "flwrcount_temp2022.txt":
            b"DOY\ttrtmt_arena\tspecies\tflwr_count\n"
            b"140\tC1\tCH\t10\n",
        "imputed_temporal_vars_T.txt":
            b"doy\ttrtmt\tsp\tarena\tvisits\n140\tC\tCH\t1\t2\n",
    })
    out = profile_zip_tables(data)
    assert len(out) == 5
    seeds = out["data_seeds_germ_pSEM.txt"]
    assert seeds["n_rows"] == 2
    assert seeds["timing_unit_and_fate_column_support"]["germ"][
        "n_nonmissing"] == 1
    assert seeds["candidate_grains"][0]["n_unique_keys"] == 2
    assert seeds["candidate_grains"][1]["n_unique_keys"] == 1
    assert out["bee_abund_2022.txt"]["n_rows"] == 1
    assert out["flwrcount_temp2022.txt"]["candidate_grains"]


def test_2022_stage_profile_does_not_infer_missing_archive_members():
    data = zip_fixture({"only_visits.txt": b"day\tvisits\n1\t2\n"})
    with pytest.raises(ValueError, match="essential original source stage missing"):
        profile_zip_tables(data)
