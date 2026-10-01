import math

import pandas as pd
import pytest

from iwe.iwe023_raw import audit_iwe023_raw, workbook_inventory


def _synthetic_iwe023():
    means = [0.85, 1.00, 0.91, 0.69]
    mse = 0.17025 / 1.01
    amplitude = math.sqrt(0.9 * mse)
    residuals = [-amplitude] * 5 + [amplitude] * 5
    rows = []
    plant = 0
    for week, mean in enumerate(means, start=1):
        for residual in residuals:
            plant += 1
            rows.append(
                {
                    "week_label": f"week{week}",
                    "plant": f"P{plant:02d}",
                    "seed_set": mean + residual,
                }
            )
    return pd.DataFrame(rows)


def test_raw_audit_reconstructs_published_iwe023(tmp_path):
    path = tmp_path / "iwe023.csv"
    _synthetic_iwe023().to_csv(path, index=False)

    summary, anova, effect = audit_iwe023_raw(
        path,
        week_col="week_label",
        plant_col="plant",
        seed_set_col="seed_set",
    )
    assert list(summary["n"]) == [10, 10, 10, 10]
    assert summary["relative_mean_matches"].all()
    assert anova.iloc[0]["f_statistic"] == pytest.approx(1.01)
    row = effect.iloc[0]
    assert bool(row["raw_effect_ready"])
    assert row["effect_native"] == pytest.approx(0.3815303645)
    assert row["variance_native"] == pytest.approx(0.1937181574)


def test_raw_audit_can_derive_seed_set_from_counts(tmp_path):
    rows = []
    for week in range(1, 5):
        for plant in range(10):
            rows.append(
                {
                    "week": week,
                    "plant": f"{week}-{plant}",
                    "mature_seeds": float(week + plant + 1),
                    "flowers": 10.0,
                }
            )
    path = tmp_path / "derived.csv"
    pd.DataFrame(rows).to_csv(path, index=False)

    summary, _, _ = audit_iwe023_raw(
        path,
        week_col="week",
        plant_col="plant",
        mature_seeds_col="mature_seeds",
        flowers_col="flowers",
        mean_tolerance=10,
        f_tolerance=100,
    )
    assert len(summary) == 4
    assert list(summary["n"]) == [10, 10, 10, 10]


def test_raw_audit_fails_on_ambiguous_repeated_plant_values(tmp_path):
    df = _synthetic_iwe023()
    duplicate = df.iloc[[0]].copy()
    duplicate["seed_set"] += 1
    df = pd.concat([df, duplicate], ignore_index=True)
    path = tmp_path / "bad.csv"
    df.to_csv(path, index=False)

    with pytest.raises(ValueError, match="conflicting seed-set"):
        audit_iwe023_raw(
            path,
            week_col="week_label",
            plant_col="plant",
            seed_set_col="seed_set",
        )


def test_week_order_must_be_explicit_when_labels_are_not_orderable(tmp_path):
    df = _synthetic_iwe023()
    df["week_label"] = df["week_label"].map(
        {"week1": "early", "week2": "middleA", "week3": "middleB", "week4": "late"}
    )
    path = tmp_path / "labels.csv"
    df.to_csv(path, index=False)

    with pytest.raises(ValueError, match="provide --week-order"):
        audit_iwe023_raw(
            path,
            week_col="week_label",
            plant_col="plant",
            seed_set_col="seed_set",
        )

    _, anova, effect = audit_iwe023_raw(
        path,
        week_col="week_label",
        plant_col="plant",
        seed_set_col="seed_set",
        week_order=["early", "middleA", "middleB", "late"],
    )
    assert anova.iloc[0]["f_statistic"] == pytest.approx(1.01)
    assert bool(effect.iloc[0]["raw_effect_ready"])


def test_workbook_inventory_lists_sheets_and_columns(tmp_path):
    path = tmp_path / "book.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame({"week": [1], "plant": ["A"]}).to_excel(
            writer, sheet_name="experiment", index=False
        )
        pd.DataFrame({"x": [1]}).to_excel(writer, sheet_name="notes", index=False)

    out = workbook_inventory(path)
    assert list(out["sheet"]) == ["experiment", "notes"]
    assert "week" in out.loc[out["sheet"] == "experiment", "columns"].iloc[0]
