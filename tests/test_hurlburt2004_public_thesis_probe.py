"""No-network checks for Hurlburt original PDF access probe."""
import pytest

from scripts.probe_hurlburt2004_public_thesis import (
    extract_source_file_links, validate_pdf_bytes,
)


def test_only_original_repository_pdf_or_bitstream_links_pass():
    html = """
    <a href="/bitstreams/77a/download">original</a>
    <a href="https://evil.example/bitstreams/77a/download">external</a>
    <a href="/files/NQ95948.pdf">thesis</a>
    <a href="https://another.example/unknown.pdf">other</a>
    """
    urls = extract_source_file_links(html, "https://scholaris.ca/items/abc")
    assert urls == [
        "https://scholaris.ca/bitstreams/77a/download",
        "https://scholaris.ca/files/NQ95948.pdf",
    ]


def test_binary_validation_never_accepts_html_or_tiny_fake_pdf():
    with pytest.raises(ValueError, match="not a PDF"):
        validate_pdf_bytes(b"<!doctype html><body>denied</body>")
    with pytest.raises(ValueError, match="too small"):
        validate_pdf_bytes(b"%PDF-1.7" + b"x" * 10)
    assert len(validate_pdf_bytes(b"%PDF-1.7" + b"x" * 2000)) == 64
