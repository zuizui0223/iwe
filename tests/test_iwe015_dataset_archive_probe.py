"""No-network, fail-closed checks of IWE015 whole-dataset archive fallback."""
from io import BytesIO
import zipfile

import pytest

from scripts.probe_iwe015_dataset_zip import (
    DATASET_URL, SOURCE_FILES, audit_archive, probe
)


def _source_zip(names: list[str], *, duplicate: bool = False) -> bytes:
    out = BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            if name.endswith(".csv"):
                payload = "plant,flowers,fruits\n1,12,3\n2,10,4\n"
            elif name.endswith(".R"):
                payload = "\n".join(["x <- 1"] * 12)
            else:
                payload = "Documented public archive source file " * 4
            z.writestr(f"source/v1/{name}", payload)
            if duplicate and name == names[0]:
                z.writestr(f"source/v2/{name}", payload)
    return out.getvalue()


def test_archive_route_is_documented_dataset_endpoint():
    assert DATASET_URL.startswith("https://datadryad.org/api/v2/datasets/")
    assert DATASET_URL.endswith("/download")
    assert "doi%3A10.5061%2Fdryad.6q573n5w1" in DATASET_URL


def test_complete_six_source_archive_has_checksum_and_no_effect():
    payload = _source_zip(list(SOURCE_FILES))
    report, files = audit_archive(payload)
    assert report["status"] == "complete"
    assert report["n_matched"] == 6
    assert report["n_expected"] == 6
    assert report["missing"] == []
    assert len(files) == 6
    assert set(files) == set(SOURCE_FILES)
    assert not report["evidence_promoted"]
    assert not report["table1_variance_verified"]
    assert not report["flower_fruit_lineage_verified"]
    for entry in report["source_file_manifest"]:
        assert len(entry["sha256"]) == 64


def test_incomplete_archive_is_not_declared_recovered():
    payload = _source_zip(list(SOURCE_FILES)[:-1])
    report, files = audit_archive(payload)
    assert report["status"] == "incomplete"
    assert report["n_matched"] == 5
    assert list(SOURCE_FILES)[-1] in report["missing"]
    assert len(files) == 5


def test_duplicate_basename_fail_closed():
    with pytest.raises(ValueError, match="duplicate pinned archive basename"):
        audit_archive(_source_zip(list(SOURCE_FILES), duplicate=True))


def test_no_html_or_bogus_zip_accepted():
    with pytest.raises(ValueError, match="not a ZIP"):
        audit_archive(b"<html>403 Forbidden</html>")


def test_archived_untrusted_paths_are_not_extracted():
    out = BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("../../not-an-IWE-source.txt", "inert")
        for name in SOURCE_FILES:
            if name.endswith(".csv"):
                v = "plant,flowers,fruits\n1,12,3\n2,10,4\n"
            elif name.endswith(".R"):
                v = "\n".join(["x<-1"] * 12)
            else:
                v = "Documented public archive source file " * 4
            z.writestr(f"nested/{name}", v)
    report, files = audit_archive(out.getvalue())
    assert report["status"] == "complete"
    assert all("/" not in k for k in files)
    assert set(files) == set(SOURCE_FILES)
