import pytest
import urllib.request

from scripts.recover_iwe015_dryad import (
    DOI,
    SOURCE_FILES,
    ScopeBearerRedirect,
    inspect_payload,
    source_headers,
    source_urls,
    resolve_bearer_from_environment,
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


def test_bearer_token_only_in_header_not_in_manifest_fields():
    token = "example-secret-NOT-REAL"
    assert "Authorization" not in source_headers()
    with_auth = source_headers(token)
    assert with_auth["Authorization"] == "Bearer " + token
    assert not any(token in str(x) for x in source_urls(278487))


def test_bearer_is_removed_on_redirect_outside_dryad():
    url = source_urls(278487)[0]
    req = urllib.request.Request(url, headers=source_headers("test-only"))
    handler = ScopeBearerRedirect()
    external = handler.redirect_request(
        req, None, 302, "Found", {},
        "https://storage.example.org/dryad/signed-object"
    )
    assert external is not None
    assert not external.has_header("Authorization")

    same_origin = handler.redirect_request(
        req, None, 302, "Found", {},
        "https://datadryad.org/downloads/temporary"
    )
    assert same_origin is not None
    assert same_origin.has_header("Authorization")


def test_bearer_resolution_prefers_fresh_client_credentials(monkeypatch):
    import json
    from urllib.parse import parse_qs
    monkeypatch.setenv("DRYAD_CLIENT_ID", "fake-id-for-unit-test")
    monkeypatch.setenv("DRYAD_CLIENT_SECRET", "fake-secret-for-unit-test")
    monkeypatch.setenv("DRYAD_ACCESS_TOKEN", "old-direct-token")
    called = {}

    class FakeResponse:
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False
        def read(self, n):
            return json.dumps({"access_token": "new-fake-token"}).encode()

    def urlopen(req, timeout):
        called["method"] = req.get_method()
        called["url"] = req.full_url
        called["body"] = parse_qs(req.data.decode())
        return FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    token = resolve_bearer_from_environment()
    assert token == "new-fake-token"
    assert called["method"] == "POST"
    assert called["url"] == "https://datadryad.org/oauth/token"
    assert called["body"]["grant_type"] == ["client_credentials"]


def test_expired_or_partial_credentials_fail_closed_without_secret(monkeypatch):
    monkeypatch.setenv("DRYAD_CLIENT_ID", "fake-id")
    monkeypatch.delenv("DRYAD_CLIENT_SECRET", raising=False)
    with pytest.raises(ValueError, match="credentials incomplete"):
        resolve_bearer_from_environment()


def test_existing_short_lived_token_is_accepted_only_as_fallback(monkeypatch):
    monkeypatch.delenv("DRYAD_CLIENT_ID", raising=False)
    monkeypatch.delenv("DRYAD_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("DRYAD_ACCESS_TOKEN", "fake-short-lived-bearer")
    assert resolve_bearer_from_environment() == "fake-short-lived-bearer"
