"""No-network, source-provenance checks for official Cardamine binary assets."""
from io import BytesIO
import zipfile

import pytest

from scripts.probe_cardamine_public_timing_assets import (
    TARGETS, OLE_MAGIC, validate_asset
)


def test_only_four_source_pinned_publisher_assets():
    assert set(TARGETS) == {
        "davies2024_figure4.ppt",
        "davies2019_appendixS1.pdf",
        "davies2019_appendixS2.pdf",
        "davies2019_appendixS3.pdf",
    }
    assert "ece311330-fig-0004" in TARGETS["davies2024_figure4.ppt"][0]
    assert all("onlinelibrary.wiley.com" in val[0] for val in TARGETS.values())


def test_official_pdf_mime_signature_only_reports_access():
    obj = validate_asset("davies2019_appendixS1.pdf", b"%PDF-1.6\n%test", "pdf")
    assert obj["format"] == "pdf"
    assert len(obj["sha256"]) == 64
    assert obj["source_adult_flight_numeric_verified"] is False
    assert obj["figure_digitization_performed"] is False


def test_legacy_powerpoint_is_not_mistaken_for_source_numerical_data():
    obj = validate_asset("davies2024_figure4.ppt", OLE_MAGIC + b"\x00" * 100, "ppt")
    assert obj["format"] == "legacy_ole_ppt"
    assert obj["source_adult_flight_numeric_verified"] is False
    assert obj["potential_editable_chart_parts"] == []


def test_ooxml_embedded_parts_are_only_review_candidates():
    s = BytesIO()
    with zipfile.ZipFile(s, "w") as z:
        z.writestr("[Content_Types].xml", '<Types></Types>')
        z.writestr("ppt/embeddings/fake.xlsx", b"not-a-workbook")
        z.writestr("ppt/charts/chart1.xml", b"<chart/>")
    obj = validate_asset("davies2024_figure4.ppt", s.getvalue(), "ppt")
    assert obj["format"] == "office_open_xml"
    assert sorted(obj["potential_editable_chart_parts"]) == [
        "ppt/charts/chart1.xml", "ppt/embeddings/fake.xlsx"
    ]
    assert obj["source_adult_flight_numeric_verified"] is False


@pytest.mark.parametrize("kind,content", [
    ("pdf", b"<html>403 Forbidden</html>"),
    ("ppt", b"<html>Blocked</html>"),
    ("pdf", b"Not a PDF"),
    ("ppt", b"Not a PPT"),
    ("ppt", b"PK\x03\x04not a complete ZIP"),
])
def test_fake_binaries_fail_closed(kind, content):
    with pytest.raises(ValueError):
        validate_asset("source." + kind, content, kind)
