"""Fail-closed tests for official PMC Cloud supplementary-source probe."""
import io
import sys
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import probe_cardamine_pmc_cloud as m


def make_docx(txt):
    out = io.BytesIO()
    content = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>' + txt + '</w:t></w:r></w:p></w:body></w:document>'
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("word/document.xml", content)
    return out.getvalue()


class TestCloudProbe(unittest.TestCase):
    def test_wrong_identity_rejected(self):
        self.assertFalse(m.metadata_is_source({"pmcid": m.PMCID, "doi": "10.fake", "license_code": "CC BY"}))
        self.assertFalse(m.metadata_is_source({"pmcid": m.PMCID, "doi": m.DOI}))
        self.assertTrue(m.metadata_is_source({"pmcid": m.PMCID, "doi": m.DOI, "license_code": "CC BY"}))

    def test_exact_allowlist_excludes_unknown_supplement(self):
        self.assertNotIn("fake.pdf", m.ALLOWED)
        self.assertIn("ece3-14-e11330-s001.docx", m.ALLOWED)

    def test_media_only_official_url(self):
        inp = {"media_urls": ["https://example.com/ECE3-14-e11330-s001.docx",
                              "https://pmc-oa-opendata.s3.amazonaws.com/PMC11056787.1/ECE3-14-e11330-s001.docx"]}
        self.assertEqual(len(m.media_urls(inp)), 1)

    def test_docx_tokens_are_only_signals(self):
        v = m.docx_source_signals(make_docx("2012 2013 2014 female recapture DOY"))
        self.assertTrue(v["has_all_2012_2014_tokens"])
        self.assertTrue(v["has_female_token"])
        self.assertTrue(v["has_captured_event_token"])
        self.assertTrue(v["has_doy_token"])

    def test_nonyear_source_cannot_count_as_event_candidate(self):
        v = m.docx_source_signals(make_docx("female recapture 2010 only"))
        self.assertFalse(v["has_all_2012_2014_tokens"])

    def test_fetch_rejects_official_looking_other_host_before_network(self):
        with self.assertRaises(ValueError):
            m.fetch("https://pmc-oa-opendata.s3.amazonaws.com.evil.net/metadata/PMC11056787.1.json")

    @patch.object(m, "fetch")
    def test_missing_access_never_promotes(self, fake):
        from urllib.error import URLError
        fake.side_effect = URLError("offline")
        report = m.run()
        self.assertEqual(report["downloaded_docx_count"], 0)
        self.assertFalse(report["source_verified_2012_2014_female_capture_recapture"])
        self.assertFalse(report["strict_h1_promotion"])


if __name__ == "__main__":
    unittest.main()
