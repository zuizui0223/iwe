import pandas as pd
import pytest

from iwe.cardamine_raw import (
    normalize_cardamine_transect,
    normalize_cardamine_workbooks,
    read_cardamine_workbook,
)


def _raw():
    return pd.DataFrame(
        [
            {"Plant Number": "1", "Date": 100, "Height": 10, "Flowers": 0, "Buds": 5, "Seed-pods": 0},
            {"Plant Number": "1", "Date": 106, "Height": 12, "Flowers": 2, "Buds": 3, "Seed-pods": 0},
            {"Plant Number": "1", "Date": 112, "Height": 12, "Flowers": 0, "Buds": 0, "Seed-pods": 4},
            {"Plant Number": "1", "Date": 118, "Height": "d", "Flowers": 0, "Buds": 0, "Seed-pods": 3},
            {"Plant Number": "2", "Date": 101, "Height": 9, "Flowers": 1, "Buds": 2, "Seed-pods": 0},
            {"Plant Number": "2", "Date": 108, "Height": "d", "Flowers": None, "Buds": 0, "Seed-pods": 1},
        ]
    )


def test_normalize_cardamine_transect_is_conservative_at_dehiscence():
    timing, summaries, audit = normalize_cardamine_transect(
        _raw(), year=2012, ecotype="early"
    )
    one = summaries.set_index("plant_id").loc["1"]
    assert one["max_ru"] == pytest.approx(5)
    assert one["final_intact_ru"] == pytest.approx(3)
    assert timing.loc[
        (timing["plant_id"] == "1") & (timing["flowers"] > 0), "doy"
    ].min() == pytest.approx(106)

    audit = audit.set_index("plant_id")
    assert audit.loc["1", "outcome_status"] == "ready"
    assert audit.loc["2", "outcome_status"] == "excluded"
    assert audit.loc["2", "exclusion_reason"] == "dehiscence_ru_missing"


def test_parser_never_uses_previous_row_as_missing_final_outcome():
    raw = _raw()
    raw.loc[3, ["Flowers", "Buds", "Seed-pods"]] = None
    _, summaries, audit = normalize_cardamine_transect(
        raw, year=2012, ecotype="early"
    )
    assert "1" not in set(summaries["plant_id"])
    row = audit.set_index("plant_id").loc["1"]
    assert row["exclusion_reason"] == "dehiscence_ru_missing"


def test_multiple_dehiscence_markers_fail_closed():
    raw = _raw()
    raw.loc[len(raw)] = {
        "Plant Number": "1",
        "Date": 119,
        "Height": "d",
        "Flowers": 0,
        "Buds": 0,
        "Seed-pods": 2,
    }
    _, summaries, audit = normalize_cardamine_transect(
        raw, year=2012, ecotype="early"
    )
    assert "1" not in set(summaries["plant_id"])
    assert (
        audit.set_index("plant_id").loc["1", "exclusion_reason"]
        == "multiple_dehiscence_markers"
    )


def test_dehiscence_ru_cannot_exceed_predehiscence_max():
    raw = _raw()
    raw.loc[3, "Seed-pods"] = 6
    _, summaries, audit = normalize_cardamine_transect(
        raw, year=2012, ecotype="early"
    )
    assert "1" not in set(summaries["plant_id"])
    assert (
        audit.set_index("plant_id").loc["1", "exclusion_reason"]
        == "dehiscence_ru_exceeds_predehiscence_max"
    )


def test_workbook_reader_uses_second_row_as_header(tmp_path):
    path = tmp_path / "cardamine.xlsx"
    raw = _raw()
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame([["CpE", 2012]]).to_excel(
            writer, index=False, header=False, sheet_name="Sheet1"
        )
        raw.to_excel(writer, index=False, startrow=1, sheet_name="Sheet1")
    timing, summaries, audit = read_cardamine_workbook(
        path, year=2012, ecotype="early"
    )
    assert not timing.empty
    assert "1" in set(summaries["plant_id"])
    assert len(audit) == 2


def test_duplicate_workbook_specification_fails(tmp_path):
    path = tmp_path / "cardamine.xlsx"
    raw = _raw()
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame([["CpE", 2012]]).to_excel(
            writer, index=False, header=False, sheet_name="Sheet1"
        )
        raw.to_excel(writer, index=False, startrow=1, sheet_name="Sheet1")
    with pytest.raises(ValueError, match="duplicate"):
        normalize_cardamine_workbooks(
            [(2012, "early", path), (2012, "early", path)]
        )
