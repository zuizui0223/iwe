"""Deterministic source-grain checks: no synthetic fixture is real ecological evidence."""
import pytest

from scripts.analyze_crone2025_spring_conversion import (
    YEARS, _loo_rmse, _spearman, analyze, original_rows, SPRING_NAME,
)


def fixture():
    spring = []
    branches = []
    for year in YEARS:
        spring.extend([
            {"year": str(year), "tree.num": "HF1",
             "flowering.intensity": "high"},
            {"year": str(year), "tree.num": "HF2",
             "flowering.intensity": "low"},
        ])
        for treatment, filled, empty in (
            ("control", 5, 5), ("exclusion", 2, 8),
        ):
            branches.append({
                "year": str(year), "tree": "HF1", "branch": "A",
                "treatment": treatment,
                "num.filled": str(filled), "num.empty": str(empty),
                "num.grub": "0", "num.wrinkle": "0", "num.small": "0",
                "num.moldy": "0", "num.exit": "0", "num.missing": "2",
                "total.seed": "10", "mast.index": str(year - 2011),
            })
    return spring, branches


def test_same_calendar_year_and_source_tree_join_without_branch_pseudoreplication():
    spring, branches = fixture()
    annual, out = analyze(spring, branches, expected_tree_count=2)
    assert len(annual) == 12
    assert out["independent_year_clusters"] == 6
    assert out["total_original_exclusion_rows"] == 12
    row = next(r for r in annual if r["year"] == 2012
               and r["treatment"] == "control")
    assert row["spring_intensity_mean_0to3"] == 2
    assert row["p_intact_among_classified"] == 0.5
    assert row["p_intact_missing_worst"] == round(5/12, 8)
    assert row["p_intact_missing_best"] == round(7/12, 8)
    assert out["true_partner_adult_window_measured"] is False
    assert out["late_seed_mast_index_only_retrospective"] is True


def test_2013_source_missing_and_predation_columns_not_made_zero():
    spring, branches = fixture()
    row = next(r for r in branches if r["year"] == "2013"
               and r["treatment"] == "control")
    row.update({"num.exit": "NA", "num.moldy": "NA",
                "num.wrinkle": "NA", "num.small": "NA",
                "num.missing": "NA"})
    annual, out = analyze(spring, branches, expected_tree_count=2)
    a = next(r for r in annual if r["year"] == 2013
             and r["treatment"] == "control")
    assert a["optional_predation_unknown_rows"] == 1
    assert a["missing_unknown_rows"] == 1
    assert a["p_intact_missing_worst"] is None
    assert a["p_intact_missing_best"] is None
    assert out["incomparable_predation_category_years"] == [2013]
    assert out["incomplete_missing_status_years"] == [2013]


def test_reused_branch_label_not_a_unique_experimental_unit():
    spring, branches = fixture()
    branches.append(dict(branches[0]))
    annual, out = analyze(spring, branches, expected_tree_count=2)
    assert out["total_original_exclusion_rows"] == 13
    assert out["independent_year_clusters"] == 6
    a = next(r for r in annual if r["year"] == 2012
             and r["treatment"] == "control")
    assert a["source_branch_rows"] == 2
    assert a["distinct_branch_trees"] == 1


def test_seed_state_closure_and_unmatched_trees_fail_closed():
    spring, branches = fixture()
    branches[0]["total.seed"] = "12"
    with pytest.raises(ValueError, match="totals fail closure"):
        analyze(spring, branches, expected_tree_count=2)
    spring, branches = fixture()
    branches[0]["tree"] = "HF2000"
    with pytest.raises(ValueError, match="lacks observed earlier"):
        analyze(spring, branches, expected_tree_count=2)


def test_spearman_and_leave_year_out_are_no_fit_on_heldout_year():
    assert _spearman([1, 2, 3, 4], [10, 20, 30, 40]) == 1.0
    assert _spearman([1, 2, 3, 4], [40, 30, 20, 10]) == -1.0
    # This is a numerical software fixture, not empirical ecological evidence.
    x, y = [1, 2, 3, 4, 5], [2, 4, 6, 8, 10]
    assert _loo_rmse(x, y, linear=True) < 1e-12
    assert _loo_rmse(x, y, linear=False) > 0


def test_exact_original_read_requires_pinned_digest(monkeypatch):
    import scripts.analyze_crone2025_spring_conversion as script
    monkeypatch.setattr(script, "_get", lambda _: b"wrong original bytes")
    with pytest.raises(ValueError, match="checksum mismatch"):
        original_rows(SPRING_NAME)
