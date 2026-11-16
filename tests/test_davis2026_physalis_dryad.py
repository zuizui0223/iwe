"""Dryad original access and source schema *software tests*, not source results."""
import json
import pytest
from urllib.error import HTTPError

import scripts.probe_davis2026_physalis_dryad as davis


def fake_manifest(include_seed_quality=False):
    files=[]
    names=sorted(davis.TARGET_SOURCE_FILES)
    if include_seed_quality:
        names.append("Oikos_2021_seeds_fruit_sugar.csv")
    for idx,name in enumerate(names,1):
        files.append({
            "path":name,"size":100,"digestType":"sha-256",
            "digest":None,
            "_links":{
                "stash:download":{
                    "href":f"/api/v2/files/{250000+idx}/download"
                }
            }
        })
    return {
        "total":len(files),
        "_embedded":{"stash:files":files}
    }


def test_original_Dryad_DOI_and_untrusted_redirect_routes_rejected():
    assert davis.SOURCE_DOI=="10.5061/dryad.xpnvx0kvp"
    assert davis.allow_public_source_url(davis.METADATA_URI)
    assert davis.allow_public_source_url(
        "https://datadryad.org/api/v2/files/987654/download"
    )
    assert not davis.allow_public_source_url(
        "https://example.com/fake_pollinator_records.csv"
    )
    assert not davis.allow_public_source_url("http://datadryad.org")
    with pytest.raises(ValueError,match="unapproved original"):
        davis.fetch_original("https://malicious.example/files/unsafe.csv",100)


def test_published_version_issued_file_IDs_only(monkeypatch):
    monkeypatch.setattr(
        davis,"fetch_original",
        lambda uri,cap: json.dumps(fake_manifest()).encode()
    )
    ref,files=davis.original_version_file_listing({
        "_links":{"stash:version":{"href":"/api/v2/versions/925384"}}
    })
    assert ref=="/api/v2/versions/925384"
    assert len(files)==8
    assert all(z["download_uri"].startswith("/api/v2/files/")
               for z in files)
    assert set(z["path"] for z in files)==davis.TARGET_SOURCE_FILES
    with pytest.raises(ValueError,match="original published Dryad version"):
        davis.original_version_file_listing({
            "_links":{"stash:version":{"href":"https://evil.site/10"}}
        })


def test_original_fruit_date_morphospecies_and_plant_are_not_unique_flower():
    raw=(
        b"fruit_set,treatment,morphospecies,julian_date,"
        b"plant_id,block,flower_id\n"
        b"1,c,Apis,185,P1,B1,\n"
        b"0,h,Apis,185,P1,B1,\n"
        b"1,h,Bombus,190,P2,B1,FX2\n"
    )
    r=davis.profile_csv(raw,"Oikos_2021_fruit_set_poll_obs.csv")
    assert r["n_rows"]==3
    assert r["source_body_inspected"] is True
    assert r["same_flower_set_weight_join_verified"] is False
    by={tuple(k["original_source_key"]):k
        for k in r["candidate_key_grains"]}
    assert by[("plant_id","julian_date","morphospecies")][
        "n_source_rows_with_duplicate_key"]==1
    assert by[("plant_id","flower_id")]["n_rows_with_null_key"]==2
    assert r["measurement_field_support"]["flower_id"][
        "n_nonmissing"]==1


def test_malformed_original_fruit_row_does_not_infer_herbivore_effect():
    with pytest.raises(ValueError,match="row widths"):
        davis.profile_csv(
            b"fruit_set,plant_id\n1,P1,unexpected\n",
            "Oikos_2021_fruit_set_poll_obs.csv"
        )


def test_public_metadata_without_original_bytes_is_not_source_fit(monkeypatch):
    def mock(uri,cap):
        if uri==davis.METADATA_URI:
            return json.dumps({
                "title":"Synthetic Dryad integration receipt",
                "_links":{
                    "stash:version":{"href":"/api/v2/versions/925384"}
                }
            }).encode()
        if uri.endswith("/versions/925384/files"):
            return json.dumps(fake_manifest()).encode()
        raise HTTPError(uri,401,"Source Not Authorised",{},None)
    monkeypatch.setattr(davis,"fetch_original",mock)
    r=davis.audit()
    assert r["published_original_source_manifest_verified"] is True
    assert r["original_source_files_retrieved"]==0
    assert r["status"]=="original_file_access_partial_or_blocked"
    assert r["same_flower_date_herbivore_context_and_fruit_identifiers_verified"] is False
    assert r["model_estimated"] is False
    assert r["strict_iwe_h1_added"] is False
    assert len(r["source_attempts"])==8


def test_author_source_version_can_contain_additional_seed_quality_file(
    monkeypatch,
):
    monkeypatch.setattr(
        davis,"fetch_original",
        lambda uri,cap: json.dumps(
            fake_manifest(include_seed_quality=True)
        ).encode()
    )
    ref,files=davis.original_version_file_listing({
        "_links":{"stash:version":{"href":"/api/v2/versions/925384"}}
    })
    assert len(files)==9
    assert len({f["path"] for f in files})==9
    assert "Oikos_2021_seeds_fruit_sugar.csv" in {
        f["path"] for f in files
    }
