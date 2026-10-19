"""No-network source rules for Jadera mixed pollination/seed-cost Dryad."""
import csv
from io import BytesIO
from zipfile import ZipFile
import pytest

from scripts.probe_jadera2025_dryad_source import (
    _allowed_url,_inspect_zip,_parse_csv_field_info,_safe_name,_source_lines,
    ROOT,ZIP_URL
)


def test_exact_dryad_source_rejects_other_do_is_or_external_hosts():
    assert _allowed_url(ROOT)
    assert _allowed_url(ZIP_URL)
    assert not _allowed_url(
        "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.other/download"
    )
    assert not _allowed_url(
        "https://unrelated.example/api/v2/datasets/doi%3A10.5061%2Fdryad.2bvq83c2b/download"
    )
    assert not _allowed_url("http://datadryad.org/api/v2/datasets")
    assert not _allowed_url("https://datadryad.org/api/v2/datasets")


def test_nested_original_separate_experiment_files_not_imputed_as_h1():
    inner=BytesIO()
    with ZipFile(inner,"w") as z:
        z.writestr("pollination.csv",
                   "PlantID,host_species,field_date,pollen_deposited\n"
                   "A,Cardiospermum,2018-05-01,1\n")
        z.writestr("seed_cost.csv",
                   "PlantID,host_species,seed_viability,progeny\n"
                   "B,Koelreuteria,0.6,2\n")
    archive=BytesIO()
    with ZipFile(archive,"w") as z:
        z.writestr("GREENHOUSE.zip",inner.getvalue())
        z.writestr("README.md",
                   "Study date and host seed viability: separate experiments.\n")
    items=_inspect_zip(archive.getvalue(),"source",0)
    assert len(items)==3
    names=[x["name"] for x in items]
    assert any("pollination.csv" in x for x in names)
    assert any("seed_cost.csv" in x for x in names)
    assert any("README.md" in x for x in names)
    assert items[0]["rows"]==1
    assert "field_date" in items[0]["source_stage_field_hints"]
    assert "seed_viability" in items[1]["source_stage_field_hints"]
    assert "source_line_leads" in items[2]


def test_do_not_accept_path_traversal_or_invalid_members():
    assert not _safe_name("../../host_secrets.csv")
    assert not _safe_name("/absolute.csv")
    payload=BytesIO()
    with ZipFile(payload,"w") as z:
        z.writestr("../other.csv","ID\n1\n")
    with pytest.raises(ValueError,match="source archive path"):
        _inspect_zip(payload.getvalue(),"root",0)


def test_source_code_leads_and_field_names_never_authenticate_adult_activity():
    csv_bytes=(b"ID,flowering_day,adult_flight_date,final_viable_seed\n"
               b"123,200,198,6\n")
    result=_parse_csv_field_info(csv_bytes,"example.csv")
    assert result["rows"]==1
    assert "adult_flight_date" in result["source_stage_field_hints"]
    lines=_source_lines(b"Adult flight date is an UNKNOWN stage.\n",
                        "readme.txt")
    assert lines[0]["line_number"]==1
    assert "UNKNOWN" in lines[0]["source_text_short"]
