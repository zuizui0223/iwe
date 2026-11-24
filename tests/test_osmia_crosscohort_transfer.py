"""Synthetic software-only tests. Do not describe these as source results."""
from __future__ import annotations
import math
import pytest

import scripts.analyze_osmia_crosscohort_transfer_2021_2022 as cross


def fake_both_cohorts():
    records=[]
    for cohort,arenas in (
        ("2021", ["C1","C2","C3","C4","W5","W6","W7","W8"]),
        ("2022", [f"{r}_{i}" for r in ("A","W2","W4","W6")
                  for i in range(1,6)]),
    ):
        for i,arena in enumerate(arenas):
            for j,sp in enumerate(cross.SPECIES):
                base=.5+0.065*j-.01*i+(.03 if cohort=="2021" else 0)
                records.append({
                    "cohort":cohort, "arena":arena,"species":sp,
                    "seed_fraction":max(0,min(1,base)),
                    "seeds_measured":20, "ovules_sampled":30,
                    "n_original_outcome_plants":2,
                    "flowerTotal":100+i*3+j*15,
                    "bloomDOY":(110 if cohort=="2021" else 68)+i*1.7+j*3,
                    "bloomBeeDensity":2+j*.2+i*.1,
                    "adultMean":3+i*.02,
                    "matchedFlowerCoverage":.6 if cohort=="2021" else .97,
                })
    return records


def test_source_harmonization_uses_true_arena_species_once():
    sample=fake_both_cohorts()
    result=cross.harmonize(sample)
    assert len(result)==84
    assert len(sample)==84
    assert "flowerShare" not in sample[0]  # no source mutation
    assert {r["cohort"] for r in result}=={"2021","2022"}
    assert {r["species"] for r in result}==set(cross.SPECIES)
    for year in ("2021","2022"):
        cohort=[r for r in result if r["cohort"]==year]
        assert min(r["relativeBloomCalendar"] for r in cohort)==0
        assert max(r["relativeBloomCalendar"] for r in cohort)==1
        assert all(math.isfinite(r["relativeBloomBeeDensity"]) for r in cohort)
    for year,arena in {("2021","C1"),("2022","W6_5")}:
        a=[z for z in result if z["cohort"]==year and z["arena"]==arena]
        assert len(a)==3
        assert sum(z["flowerShare"] for z in a)==pytest.approx(1)


def test_year_transfer_does_not_learn_from_heldout_year_seed_fates():
    a=cross.harmonize(fake_both_cohorts())
    tr=[z for z in a if z["cohort"]=="2021"]
    te=[z for z in a if z["cohort"]=="2022"]
    original=cross.fit_and_predict(tr,te,cross.MODELS["M3_real_bee_window"])
    changed=[{**z,"seed_fraction":1-z["seed_fraction"]} for z in te]
    recomputed=cross.fit_and_predict(tr,changed,cross.MODELS["M3_real_bee_window"])
    assert original==recomputed
    assert len(original)==60
    assert all(0<=z<=1 for z in original)


def test_same_response_cohort_sensitivity_is_not_independent_taxa_replication():
    a=cross.harmonize(fake_both_cohorts())
    out=cross.compare(a)
    assert set(out)=={
        "other_year_trains_test_2021",
        "other_year_trains_test_2022",
        "within_2021_leave_arena_out",
        "within_2022_leave_arena_out",
    }
    for k,record in out.items():
        assert set(record["models"])==set(cross.MODELS)
        required=8 if "2021" in k.split("test_")[-1] else 20
        if k.endswith("_2021"):
            required=8
        if k.endswith("_2022"):
            required=20
        assert record["models"]["M3_real_bee_window"][
            "n_holdout_arenas"
        ]==required if k.startswith("other_year") else True
        assert 0<=record["window_wins_vs_calendar"]<=required
        assert math.isfinite(
            record["models"]["M3_real_bee_window"]["equal_arena_rmse"]
        )


def test_harmonization_rejects_duplicate_or_missing_source_species():
    data=fake_both_cohorts()
    with pytest.raises(ValueError,match="duplicated"):
        cross.harmonize(data+[dict(data[0])])
    with pytest.raises(ValueError,match="missing one"):
        cross.harmonize(data[1:])


def test_outcome_balance_is_recomputed_from_primitive_counts_not_per_plant_mean(
    monkeypatch,
):
    # A tiny fixture for the source join adapter, not the real biological
    # 181-plant / 234-summary original cohort.
    from scripts.analyze_osmia_crosscohort_transfer_2021_2022 import (
        aggregate_2021,
    )
    plants=[]
    flower=[]
    bee=[]
    for i,arena in enumerate(["C1","C2","C3","C4","W5","W6","W7","W8"]):
        trt=arena[0]
        for sp in cross.SPECIES:
            flower.extend([
                [arena,"ambient" if trt=="C" else "warmed",sp,"PLANT",
                 "0","0","0","109","2"],
                [arena,"ambient" if trt=="C" else "warmed",sp,"PLANT",
                 "0","0","0","110","3"],
            ])
            plants.append({
                "arena":arena,"species":sp,
                "sampled_seed_count":10,"sampled_ovule_count":2,
            })
        bee.extend([
            ["4/19/2021","109",trt,arena[1:],"3"],
            ["4/20/2021","110",trt,arena[1:],"5"],
        ])
    monkeypatch.setattr(cross,"build_2021_plants",
                        lambda data, allow_incomplete_fruit:
                        (plants,{"synthetic":1}))
    units, meta=aggregate_2021({
        "flower_count.txt":flower, "bee_density.txt":bee
    })
    assert len(units)==24
    assert meta["n_plants_with_original_seed_outcome"]==24
    assert all(z["seed_fraction"]==pytest.approx(10/12) for z in units)
    assert all(z["bloomBeeDensity"]==pytest.approx(4.2) for z in units)
    assert all(z["matchedFlowerCoverage"]==1 for z in units)


def test_nonpositive_source_seed_denominator_is_fatal():
    a=fake_both_cohorts()
    a[0]["flowerTotal"]=-1
    with pytest.raises(ValueError,match="invalid source flowering"):
        cross.harmonize(a)
    a=fake_both_cohorts()
    a[0]["seed_fraction"]=2
    with pytest.raises(ValueError,match="invalid sampled seed"):
        cross.harmonize(a)
