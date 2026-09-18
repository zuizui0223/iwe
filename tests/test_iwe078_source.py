from pathlib import Path

import pandas as pd
import pytest

from iwe.iwe078_source import load_iwe078_source


def write_csv(root: Path, name: str, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_csv(root / name, index=False)


def build_source_package(root: Path) -> None:
    # Experiment 1 metadata: four valid controls, one treatment, one chopped.
    main1 = []
    for plant_id in ["80.1", "6.1", "64.1", "2.1"]:
        main1.append(
            {
                "ID": plant_id,
                "TRT": "C",
                "geno": plant_id.split(".")[0],
                "CHOP_1FLR": "N",
                "first_flr": "7/10/23",
            }
        )
    main1 += [
        {
            "ID": "80.2",
            "TRT": "H1",
            "geno": "80",
            "CHOP_1FLR": "N",
            "first_flr": "7/10/23",
        },
        {
            "ID": "80.3",
            "TRT": "C",
            "geno": "80",
            "CHOP_1FLR": "Y",
            "first_flr": "7/10/23",
        },
    ]
    write_csv(root, "main_exp1.csv", main1)

    fit1 = []
    for plant_id in ["80.1", "6.1", "64.1", "2.1", "80.2", "80.3"]:
        fit1.append(
            {
                "ID": plant_id,
                "lg frt": 10,
                "sm frt": 5,
                "schinia": 1,
                "sm brev": 5,
                "lg brev FIT": 5,
            }
        )
    write_csv(root, "fitness_exp1.csv", fit1)

    flower1 = []
    for i, plant_id in enumerate(["80.1", "6.1", "64.1", "2.1", "80.2", "80.3"]):
        flower1.append(
            {
                "ID": plant_id,
                "TRT": "C" if plant_id not in {"80.2"} else "H1",
                "geno": plant_id.split(".")[0],
                "f1": 9 + i,
                "f2": 0,
            }
        )
    write_csv(root, "df2_exp1.csv", flower1)
    write_csv(root, "test.csv", [{"date": "7/12/23"}, {"date": "7/19/23"}])

    mompha1 = []
    for i, plant_id in enumerate(["80.1", "6.1", "64.1", "2.1", "80.2", "80.3"]):
        mompha1 += [
            {
                "ID": plant_id,
                "date": "0023-07-12",
                "mompha": 9 if plant_id == "80.1" else 0,
                "positive mompha": i + 1,
            },
            {
                "ID": plant_id,
                "date": "0023-07-19",
                "mompha": 0,
                "positive mompha": 0,
            },
        ]
    write_csv(root, "momphaCALC_exp1.csv", mompha1)

    # Extra first-potential-flower rows: 7/10 is outside the regular flower
    # survey dates and falls in the same Monday-start week as 7/12.
    write_csv(
        root,
        "fflr_overlap_ex1.csv",
        [
            {
                "ID": plant_id,
                "date": "7/10/23",
                "potential": 1,
                "flower": 1,
                "mompha": 0,
            }
            for plant_id in ["80.1", "6.1", "64.1", "2.1", "80.2", "80.3"]
        ],
    )

    # Experiment 2: c is control, h is treatment.
    main2 = []
    for plant_id, geno in [
        ("10.1", "10"),
        ("112.1", "112"),
        ("2.2", "2"),
        ("64.2", "64"),
    ]:
        main2.append(
            {
                "ID": plant_id,
                "Treatment": "c",
                "geno": geno,
                "CHOP_1FLR": "N",
                "first_flr_mom": "7/17/23",
            }
        )
    main2.append(
        {
            "ID": "10.2",
            "Treatment": "h",
            "geno": "10",
            "CHOP_1FLR": "N",
            "first_flr_mom": "7/17/23",
        }
    )
    write_csv(root, "main_exp2.csv", main2)

    fit2 = []
    for plant_id in ["10.1", "112.1", "2.2", "64.2", "10.2"]:
        fit2.append(
            {
                "ID": plant_id,
                "lg frt": 8,
                "sm frt": 4,
                "schinia": 1,
                "sm brev": 5,
                "lg brev": 5,
            }
        )
    write_csv(root, "Exp 2 fitness.csv", fit2)

    flower2 = []
    for i, (plant_id, geno) in enumerate(
        [("10.1", "10"), ("112.1", "112"), ("2.2", "2"), ("64.2", "64"), ("10.2", "10")]
    ):
        flower2.append(
            {
                "ID": plant_id,
                "TRT": "c" if plant_id != "10.2" else "h",
                "geno": geno,
                "f1": 4 + i,
                "f2": 1,
            }
        )
    write_csv(root, "df2_exp2.csv", flower2)
    write_csv(root, "test_exp2.csv", [{"date": "7/19/23"}, {"date": "7/26/23"}])

    mompha2 = []
    for i, plant_id in enumerate(["10.1", "112.1", "2.2", "64.2", "10.2"]):
        mompha2 += [
            {
                "ID": plant_id,
                "date": "7/19/23",
                "mompha": 0,
                "positive mompha": i + 1,
            },
            {
                "ID": plant_id,
                "date": "7/26/23",
                "mompha": 0,
                "positive mompha": 0,
            },
        ]
    write_csv(root, "momphaCALC_exp2.csv", mompha2)
    write_csv(
        root,
        "fflr_overlap_ex2.csv",
        [
            {
                "ID": plant_id,
                "date": "7/17/23",
                "potential": 2,
                "flower": 2,
                "mompha": 0,
            }
            for plant_id in ["10.1", "112.1", "2.2", "64.2", "10.2"]
        ],
    )


def test_source_adapter_applies_control_and_source_fitness_rules(tmp_path):
    build_source_package(tmp_path)
    source = load_iwe078_source(tmp_path)

    assert source.eligible_ids["1"] == frozenset({"80.1", "6.1", "64.1", "2.1"})
    assert source.eligible_ids["2"] == frozenset({"10.1", "112.1", "2.2", "64.2"})

    fit1 = source.fitness.loc[source.fitness["experiment"] == "1"]
    fit2 = source.fitness.loc[source.fitness["experiment"] == "2"]

    # Exp1: 15 - (1 + 0.2*5 + 0.2*5) = 12
    assert all(v == pytest.approx(12.0) for v in fit1["final_reproduction"])
    # Exp2: 12 - (1 + 0.2*5 + 0.2*5) = 9
    assert all(v == pytest.approx(9.0) for v in fit2["final_reproduction"])
    assert set(source.fitness["treatment"]) == {"control"}


def test_source_adapter_reconstructs_potential_flowers_and_r_week_bins(tmp_path):
    build_source_package(tmp_path)
    source = load_iwe078_source(tmp_path)

    p = source.flowering.loc[
        (source.flowering["experiment"] == "1")
        & (source.flowering["plant_id"] == "80.1")
    ].copy()

    monday = pd.Timestamp("2023-07-10")
    row = p.loc[p["date"] == monday].iloc[0]

    # 7/12 open flowers = 9; fresh Mompha = 9 -> +1 potential flower;
    # source extra first-potential-flower row on 7/10 contributes +1.
    assert row["potential_flowers"] == pytest.approx(11.0)
    assert row["date"].weekday() == 0


def test_source_adapter_uses_positive_mompha_not_seasonal_totals(tmp_path):
    build_source_package(tmp_path)
    source = load_iwe078_source(tmp_path)

    p = source.attacks.loc[
        (source.attacks["experiment"] == "1")
        & (source.attacks["plant_id"] == "80.1")
    ].copy()
    row = p.loc[p["date"] == pd.Timestamp("2023-07-10")].iloc[0]
    assert row["mompha_acquired"] == pytest.approx(1.0)


def test_source_adapter_does_not_keep_treated_plants(tmp_path):
    build_source_package(tmp_path)
    source = load_iwe078_source(tmp_path)

    all_ids = set(source.flowering["plant_id"]) | set(source.attacks["plant_id"])
    assert "80.2" not in all_ids
    assert "10.2" not in all_ids
