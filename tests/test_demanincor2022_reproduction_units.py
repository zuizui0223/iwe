"""Synthetic software tests only; ecological counts require original source CI."""
from io import BytesIO
from zipfile import ZipFile
import pytest
from scripts.audit_demanincor2022_reproduction_units import (
    original_table, numeric, _constant_report, audit_source_tables,
)


def source_zip(named):
    b = BytesIO()
    with ZipFile(b, "w") as z:
        for n, data in named.items():
            z.writestr(n, data)
    return ZipFile(BytesIO(b.getvalue()))


def test_R_source_unheaded_integer_rows_align_tagged_flower_and_fate():
    z = source_zip({
        "data_seeds_germ_pSEM.txt":
            "trtmt\tarena\tsp\tplant_flwr_ID\tseeds\tovules_tot\tgerm\n"
            "1\tA\t1\tCH\t39_a\t13\t15\t3\n"
            "2\tA\t1\tCH\t39_b\t18\t19\t3\n",
    })
    rows=original_table(z,"data_seeds_germ_pSEM.txt")
    assert len(rows)==2
    assert rows[0]["trtmt"]=="A"
    assert rows[0]["arena"]=="1"
    assert rows[0]["sp"]=="CH"
    assert rows[0]["plant_flwr_ID"]=="39_a"
    assert numeric(rows[0],"seeds")==13
    assert numeric(rows[0],"ovules_tot")==15
    assert numeric(rows[0],"germ")==3


def test_source_reject_nonsequential_index_instead_of_shifting_fate_columns():
    z = source_zip({
        "data_seeds_germ_pSEM.txt":
            "trtmt\tarena\tsp\n13\tA\t1\tCH\n",
    })
    with pytest.raises(ValueError,match="columns not aligned"):
        original_table(z,"data_seeds_germ_pSEM.txt")


def test_group_shared_germ_is_not_one_independent_seed_trial_per_fruit():
    group = {
        ("A","1","CH"): [
            {"germ":"3"},{"germ":"3"},{"germ":"3"}
        ],
        ("A","1","NM"): [
            {"germ":"2"}
        ],
    }
    r=_constant_report(group,"germ")
    assert r["n_groups"]==2
    assert r["groups_with_repeated_identical_value"]==1
    assert r["n_source_rows_repeated_on_same_group_value"]==2
    assert r["groups_with_multiple_values"]==0


def test_source_missing_is_not_observed_zero():
    with pytest.raises(ValueError,match="missing"):
        numeric({"germ":"NA"},"germ")
    assert numeric({"germ":"NA"},"germ",allow_na=True) is None
    assert numeric({"germ":"0"},"germ")==0


def test_never_promote_synthetic_short_table_as_real_208_fate_records():
    with pytest.raises(ValueError,match="unexpected original source row counts"):
        audit_source_tables({
            "data_seeds_germ_pSEM.txt":[{
                "trtmt":"A","arena":"1","sp":"CH","plant_flwr_ID":"39_a",
                "seeds":"13","ovules":"2","ovules_tot":"15",
                "seed_set":"0.866666667","seeds_sown":"6",
                "germ":"3","germ_prop":"0.5","cotyl":"2",
                "cotyl_prop":"0.333333333"
            }],
            "data_bee_nest_pSEM.txt":[{
                "trtmt":"A","arena":"1","sp":"CH","plant_flwr_ID":"39_a"
            }],
            "bee_abund_2022.txt":[],
            "flwrcount_temp2022.txt":[],
        })
