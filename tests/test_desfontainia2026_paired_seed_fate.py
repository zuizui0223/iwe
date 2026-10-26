"""Synthetic software-only verification of paired-shrub inference, not field data."""
import pytest
from io import BytesIO
from zipfile import ZipFile
import scripts.analyze_desfontainia2026_paired_seed_fate as m


def synthetic_shrubs():
    return [
        {
            "Plant":str(i),
            "Seed (-P-R)":str(1 if i<=2 else 0),
            "Seeds (+P-R)":str(10 if i<=32 else 0),
            "Seeds (+P+R)":str(9 if i<=28 else 0),
        } for i in range(1,41)
    ]


def test_40_exact_paired_source_shrubs_and_three_seed_statuses():
    src=m.paired_shrub_records(synthetic_shrubs())
    assert len(src)==40
    assert len({r["plant"] for r in src})==40
    a=[r["bagged"] for r in src]
    b=[r["pollination_no_robbery"] for r in src]
    c=[r["pollination_with_robbery"] for r in src]
    assert (sum(x>0 for x in a),sum(x>0 for x in b),sum(x>0 for x in c))==(2,32,28)
    d=m.paired_binary_discordance(c,b)
    assert d["only_first_positive"]==0
    assert d["only_second_positive"]==4
    assert d["both_positive"]==28
    assert d["both_zero"]==8
    assert d["exact_two_sided_p_mcnemar"]==pytest.approx(.125)


def test_bootstrap_shrub_pairing_not_independent_treatments():
    x=[5]*40
    y=[4]*40
    assert m.bootstrap_difference(x,y,200,20261026)==[1.,1.]
    assert m.mean_difference(x,y)==1
    s=m.summarize_contrast(x,y)
    assert s["p_seeds_first"]==1
    assert s["p_seeds_second"]==1
    assert s["paired_seed_presence_difference"]==0


def test_wrong_shrub_ID_and_seed_count_fail_before_prediction():
    with pytest.raises(ValueError,match="exactly 40"):
        m.paired_shrub_records(synthetic_shrubs()[:39])
    s=synthetic_shrubs()
    s[0]["Plant"]=s[1]["Plant"]
    with pytest.raises(ValueError,match="duplicate original"):
        m.paired_shrub_records(s)
    s=synthetic_shrubs()
    s[0]["Seeds (+P-R)"]="-1"
    with pytest.raises(ValueError,match="nonnegative integer"):
        m.paired_shrub_records(s)


def test_true_source_nectar_status_not_generated_from_assumed_robbery():
    rows=[
        {"Plant":"1","Flower":"1","Status":"Robada",
         "Nectar volumen (microliter)":"0",
         "Nectar concentration (% w/w)":"0"},
        {"Plant":"1","Flower":"2","Status":"Intact",
         "Nectar volumen (microliter)":"2.5",
         "Nectar concentration (% w/w)":"10"},
    ]
    out=m.nectar_schema_statuses(rows)
    assert out["n_original_nectar_flower_measurements"]==2
    assert out["source_literal_nectar_status_levels"]=={
        "Robada":1,"Intact":1}
    assert out["nectar_and_seed_source_shrubs_linked_by_ID"] is False
    assert out["nectar_effect_computed"] is False


def source_zip_example():
    wb="<workbook xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'><sheets><sheet name='Seeds per pollination treatment' sheetId='1' r:id='rId1'/></sheets></workbook>"
    rel="<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'><Relationship Id='rId1' Target='worksheets/sheet1.xml'/></Relationships>"
    sheet="<worksheet xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'><sheetData><row r='1'><c r='A1' t='inlineStr'><is><t>Plant</t></is></c><c r='B1' t='inlineStr'><is><t>Seed (-P-R)</t></is></c><c r='C1' t='inlineStr'><is><t>Seeds (+P-R)</t></is></c><c r='D1' t='inlineStr'><is><t>Seeds (+P+R)</t></is></c></row><row r='2'><c r='A2'><v>1</v></c><c r='B2'><v>0</v></c><c r='C2'><v>18</v></c><c r='D2'><v>20</v></c></row></sheetData></worksheet>"
    data=BytesIO()
    with ZipFile(data,"w") as z:
        z.writestr("xl/workbook.xml",wb)
        z.writestr("xl/_rels/workbook.xml.rels",rel)
        z.writestr("xl/worksheets/sheet1.xml",sheet)
    return data.getvalue()


def test_author_headers_and_source_row_remain_unaltered():
    header,rows=m.source_sheet_rows(
        source_zip_example(),m.SOURCE_SHEET)
    assert tuple(header)==m.EXPECTED_HEADERS
    assert rows[0]["Plant"]=="1"
    assert rows[0]["Seed (-P-R)"]=="0"
    assert rows[0]["Seeds (+P-R)"]=="18"
    assert rows[0]["Seeds (+P+R)"]=="20"


def test_400_independent_nectar_flower_records_remain_40_paired_shrubs():
    seeds=m.paired_shrub_records(synthetic_shrubs())
    raw=[]
    for shrub in range(1,41):
        for flower in range(1,11):
            status="Robada" if flower<=5 else "No dañada"
            raw.append({
                "Plant":str(shrub),"Flower":str(flower),
                "Status":status,
                "Nectar volumen (microliter)":
                    str(0.1 if status=="Robada" else 2),
                "Nectar concentration (% w/w)":"NA",
            })
    res=m.paired_nectar_volume(raw,seeds)
    assert res["paired_shrubs_with_nectar_and_seed_outcomes"]==40
    assert res["original_flower_status_counts"]=={
        "Robada":200,"No dañada":200}
    assert res["healthy_divided_by_pierced_nectar_volume"]==pytest.approx(20)
    assert res["mean_pierced_minus_healthy_nectar_difference_uL"]==pytest.approx(-1.9)
    assert res["n_pierced_with_numeric_nectar"]==200
    assert res["n_healthy_with_numeric_nectar"]==200
    assert res["no_individual_flower_nectar_to_seed_fate_join"] is True


def test_missing_nectar_is_not_assumed_zero_and_unknown_shrub_rejected():
    seeds=m.paired_shrub_records(synthetic_shrubs())
    raw=[]
    for shrub in range(1,41):
        for flower in range(1,11):
            raw.append({
                "Plant":str(shrub),"Flower":str(flower),
                "Status":"Robada" if flower<=5 else "No dañada",
                "Nectar volumen (microliter)": (
                    "NA" if shrub==1 and flower==1 else "1.0"
                ),
                "Nectar concentration (% w/w)":"NA",
            })
    out=m.paired_nectar_volume(raw,seeds)
    assert out["unrecorded_flower_nectar_volumes"]=={"Robada":1}
    assert out["n_pierced_with_numeric_nectar"]==199
    raw[0]["Plant"]="40000"
    with pytest.raises(ValueError,match="unknown seed shrub"):
        m.paired_nectar_volume(raw,seeds)


def test_rank_correlation_uses_same_original_shrub_order():
    assert m.spearman_paired_shrubs([0,2,5,7],[7,5,2,0])==-1
    assert m.spearman_paired_shrubs([1,1,1,1],[0,3,2,4]) is None
