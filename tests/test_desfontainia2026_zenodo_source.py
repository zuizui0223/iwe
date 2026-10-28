"""Synthetic OOXML source-gate tests, not original flower or seed evidence."""
from io import BytesIO
from zipfile import ZipFile
import pytest
import scripts.probe_desfontainia2026_zenodo_source as m

W="<workbook xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'><sheets><sheet name='Robbery_Seed_Output' sheetId='1' r:id='rId1'/></sheets></workbook>"
REL="<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'><Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet' Target='worksheets/sheet1.xml'/></Relationships>"
SHEET="<worksheet xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>shrub_id</t></is></c><c r='B1' t='inlineStr'><is><t>seed_count</t></is></c></row><row r='2'><c r='A2' t='inlineStr'><is><t>S1</t></is></c><c r='B2'><v>12</v></c></row></sheetData></worksheet>"

def as_xlsx(files):
    b=BytesIO()
    with ZipFile(b,"w") as z:
        for name,raw in files.items():
            z.writestr(name,raw)
    return b.getvalue()


def fixture():
    return as_xlsx({
        "xl/workbook.xml":W,
        "xl/_rels/workbook.xml.rels":REL,
        "xl/worksheets/sheet1.xml":SHEET,
    })


def test_frozen_public_record_and_original_md5_target_not_fake_filename():
    name="Raw Data Desfontainia fulgens.xlsx"
    assert m.original_url(name)==(
        "https://zenodo.org/records/18895003/files/"
        "Raw%20Data%20Desfontainia%20fulgens.xlsx?download=1")
    with pytest.raises(ValueError,match="frozen"):
        m.original_url("secret_other_data.xlsx")


def test_unpacked_ooxml_source_keys_read_only():
    r=m.workbook_inventory(fixture())
    assert r["n_original_sheets"]==1
    s=r["sheets"][0]
    assert s["sheet"]=="Robbery_Seed_Output"
    assert s["n_nonempty_excel_rows"]==2
    assert s["n_observed_columns"]==2
    assert s["header_candidates_first_nonempty_row"]==[
        "shrub_id","seed_count"]
    assert s["source_shrub_treatment_join_verified"] is False
    assert r["paired_shrub_reproduction_effect_admitted"] is False


def test_unsafe_ooxml_file_path_and_missing_worksheet_fail():
    z=as_xlsx({
        "../metadata":b"x",
        "xl/workbook.xml":W,
        "xl/_rels/workbook.xml.rels":REL,
        "xl/worksheets/sheet1.xml":SHEET
    })
    with pytest.raises(ValueError,match="unsafe"):
        m.workbook_inventory(z)
    z=as_xlsx({
        "xl/workbook.xml":W,
        "xl/_rels/workbook.xml.rels":REL,
    })
    with pytest.raises(ValueError,match="untrusted original sheet"):
        m.workbook_inventory(z)


def test_source_md5_is_hard_requirement(monkeypatch):
    class R:
        def __enter__(self):return self
        def __exit__(self,*a):return None
        def read(self,n):return b"synthetic unverified xlsx"
    monkeypatch.setattr(m,"urlopen",lambda *args,**kwargs:R())
    with pytest.raises(ValueError,match="MD5 mismatch"):
        m.original_bytes("Raw Data Desfontainia fulgens.xlsx")


def test_method_script_snippets_are_context_not_plant_effect():
    q=m.script_hints(b"foo <- read_excel('Raw Data.xlsx')\n"
                     b"fit <- gee(seed_count~treatment, data=foo)\n")
    assert q["n_lines"]==2
    assert q["source_code_leads"]
