from scripts.probe_ostergard2007_meyer2014_archives import (
    FIGSHARE_COLLECTION, FIGSHARE_BASE, DRYAD_DOI, MAX_ARTICLES,
    safe_read_json, source_figshare, source_dryad
)


def test_provider_sources_are_pinned_to_original_paper_links():
    assert FIGSHARE_COLLECTION == 3300059
    assert FIGSHARE_BASE == "https://api.figshare.com/v2"
    assert DRYAD_DOI == "10.5061/dryad.k8m7b"
    assert MAX_ARTICLES == 25


def test_forbid_arbitrary_private_and_http_sources():
    for url in (
        "http://api.figshare.com/v2/collections/3300059",
        "https://example.invalid/v2/collections/3300059",
        "file:///etc/passwd",
        "https://api.figshare.com.evil.net/v2/collections/3300059",
    ):
        obj, err = safe_read_json(url)
        assert obj is None
        assert err == "unapproved_source_endpoint"


def test_bounded_retrieval_does_not_claim_raw_data_recovery(monkeypatch):
    def fake(url, timeout=15):
        if "collections/" in url and "articles" not in url:
            return {"title": "Test original source-linked collection",
                    "doi": "10.6084/m9.figshare.c.3300059"}, None
        if url.endswith("/articles?page_size=25"):
            return [{"id": 42, "title": "Dataset"}], None
        if url.endswith("/articles/42"):
            return {"files": [{"id": 11, "name": "original.csv",
                              "size": 100}]}, None
        if "/datasets/" in url:
            return {"title": "Published source dataset", "id": 100}, None
        raise AssertionError(url)
    monkeypatch.setattr(
        "scripts.probe_ostergard2007_meyer2014_archives.safe_read_json", fake
    )
    f = source_figshare()
    d = source_dryad()
    assert f["status"] == "found_source_linked_records"
    assert f["articles"][0]["listed_files"][0]["name"] == "original.csv"
    assert d["status"] == "dataset_reachable_no_file_link"
    for x in (f, d):
        assert x["raw_data_recovered"] is False
        assert x["source_join_verified"] is False
        assert x["strict_effect_promoted"] is False


def test_source_figshare_appendix_is_not_raw_data():
    from scripts.recover_ostergard2007_figshare_appendix import inspect_html
    original = (
        "<html><body>" + "<p>Fruit abortion and seed oviposition</p>" * 50
        + "</body></html>"
    ).encode()
    result = inspect_html(original)
    assert result["source_article_id"] == 3528548
    assert result["original_file_id"] == 5600258
    assert result["raw_data_recovered"] is False
    assert result["source_egg_to_seed_join_verified"] is False
    assert result["quantitative_smd_promoted"] is False


def test_source_appendix_rejects_json_and_short_html():
    import pytest
    from scripts.recover_ostergard2007_figshare_appendix import inspect_html
    with pytest.raises(ValueError):
        inspect_html(b'{"error":"Rate limit"}')
    with pytest.raises(ValueError):
        inspect_html(b"<html>access denied</html>")
