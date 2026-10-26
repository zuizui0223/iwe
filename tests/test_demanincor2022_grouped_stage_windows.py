"""Software fixture only, no fake values admitted to original ecological claims."""
import math
from collections import Counter
import pytest
from scripts.analyze_demanincor2022_grouped_stage_windows import (
    ROOMS, SPECIES, ARENAS, make_records, evaluate,
    room_holdout_sensitivity, MODEL_SPECS, OUTCOMES,
)


def source_fixture():
    d = {
        "data_seeds_germ_pSEM.txt": [],
        "data_bee_nest_pSEM.txt": [],
        "bee_abund_2022.txt": [],
        "flwrcount_temp2022.txt": [],
    }
    for room in ROOMS:
        for n in range(1,6):
            for doy in range(100,128):
                d["bee_abund_2022.txt"].append({
                    "DOY":str(doy), "trtmt":room, "arena":str(n),
                    "bees":str(n + doy % 3)
                })
            for sp in SPECIES:
                for letter in ("a","b"):
                    original = {
                        "trtmt":room, "arena":str(n), "sp":sp,
                        "plant_flwr_ID":f"{n}_{letter}",
                        "seeds":"3", "ovules":"1", "ovules_tot":"4",
                        # Deliberately wrong derived source column:
                        "seed_set":"0.5",
                        "visits_avg":str(n), "germ":"3", "cotyl":"2",
                        "seeds_sown":"6"
                    }
                    d["data_seeds_germ_pSEM.txt"].append(original)
                for doy in (100,110,120):
                    d["flwrcount_temp2022.txt"].append({
                        "DOY":str(doy),
                        "trtmt_arena":f"{room}_{n}",
                        "species":sp,
                        "flwr_count":str(2 if doy==100 else 1)
                    })
    return d


def test_60_original_group_stage_fates_not_120_fruit_replicated_germination(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod, "audit_source_tables", lambda _: {
        "status": "synthetic_fixture_not_empirical_evidence"
    })
    d=source_fixture()
    rows,source=make_records(d)
    assert len(rows)==60
    assert len(set(x["arena"] for x in rows))==20
    assert source["n_grouped_parent_flower_rows"]==120
    assert source["source_unique_F1_seeds_sown"]==360
    assert source["n_original_fruit_seed_set_column_disagreements"]==120
    z=rows[0]
    assert z["fruit_seed_fraction"]==.75
    assert z["F1_germination"]==.5
    assert z["F1_cotyl_survival"]==pytest.approx(1/3)
    assert z["flowerBeeCensusCoverage"]==1


def test_20_arena_exact_holdouts_preserved_with_3_host_species_each(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod, "audit_source_tables",lambda _: {})
    rows,_=make_records(source_fixture())
    output=evaluate(rows)
    assert set(output)==set(OUTCOMES)
    for stage,report in output.items():
        assert set(report["models"])==set(MODEL_SPECS)
        for model,fit in report["models"].items():
            assert fit["n_group_outcomes"]==60
            assert fit["n_arena_folds"]==20
            assert set(fit["per_arena_mse"])==set(ARENAS)
            assert math.isfinite(fit["equal_arena_rmse"])


def test_any_unverified_group_germination_disagreement_fails(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod, "audit_source_tables",lambda _: {})
    d=source_fixture()
    d["data_seeds_germ_pSEM.txt"][0]["germ"]="1"
    with pytest.raises(ValueError,match="seedling outcomes varied"):
        make_records(d)


def test_source_seed_ovule_closure_strict(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod, "audit_source_tables",lambda _: {})
    d=source_fixture()
    d["data_seeds_germ_pSEM.txt"][0]["ovules_tot"]="5"
    with pytest.raises(ValueError,match="source fruit count denominator invalid"):
        make_records(d)


def test_observed_bee_census_must_overlap_flowering_day(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod, "audit_source_tables",lambda _: {})
    d=source_fixture()
    for row in d["flwrcount_temp2022.txt"]:
        row["DOY"]="200" if row["DOY"]=="100" else row["DOY"]
        row["DOY"]="201" if row["DOY"]=="110" else row["DOY"]
        row["DOY"]="202" if row["DOY"]=="120" else row["DOY"]
    with pytest.raises(ValueError,match="unobserved matched flower"):
        make_records(d)


def test_unseen_room_holdout_is_not_room_dummy_replicated_20_times(monkeypatch):
    import scripts.analyze_demanincor2022_grouped_stage_windows as mod
    monkeypatch.setattr(mod,"audit_source_tables",lambda _: {})
    grouped,_=make_records(source_fixture())
    outer=room_holdout_sensitivity(grouped)
    assert set(outer)==set(OUTCOMES)
    for y, spec in outer.items():
        assert set(spec["models"])==set(MODEL_SPECS)
        assert spec["interpretation"].endswith("not_causal")
        for model,score in spec["models"].items():
            assert score["n_held_out_rooms"]==4
            assert set(score["per_room_mse"])==set(ROOMS)
            assert math.isfinite(score["equal_room_rmse"])
