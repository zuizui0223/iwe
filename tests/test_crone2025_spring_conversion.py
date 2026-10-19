"""Deterministic source-grain checks: no synthetic fixture is real ecological evidence."""
import pytest

from scripts.analyze_crone2025_spring_conversion import (
    YEARS, _loo_rmse, _spearman, _exact_permutation_p,
    _stage_test, analyze, original_rows, SPRING_NAME,
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
    assert out["total_evaluated_branch_rows"] == 12
    assert out["total_unobserved_all_NA_branch_rows"] == 0
    assert row["p_intact_among_nonempty_classified"] == 1.0  # all 5 nonempty are filled
    # All years in this synthetic fixture have the same spring index and
    # identical reproductive fractions. There is no defined Spearman rho.
    assert out["endpoint_comparisons"]["initial_nonempty_proxy"][
        "spearman_annual"
    ] is None


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


def test_original_2016_all_na_branch_is_unobserved_not_zero_reproduction():
    spring, branches = fixture()
    all_missing = dict(branches[0])
    for key in (
        "num.filled", "num.empty", "num.grub", "num.wrinkle",
        "num.small", "num.moldy", "num.exit", "num.missing"
    ):
        all_missing[key] = "NA"
    all_missing["total.seed"] = "0"
    branches.append(all_missing)
    annual, out = analyze(spring, branches, expected_tree_count=2)
    row = next(r for r in annual if r["year"] == 2012
               and r["treatment"] == "control")
    assert row["source_branch_rows"] == 2
    assert row["observed_branch_rows"] == 1
    assert row["unobserved_all_NA_branch_rows"] == 1
    assert row["classified_pods"] == 10
    assert out["total_original_exclusion_rows"] == 13
    assert out["total_evaluated_branch_rows"] == 12
    assert out["total_unobserved_all_NA_branch_rows"] == 1
    assert out["unobserved_branch_years"] == [2012]

    all_missing["total.seed"] = "1"
    with pytest.raises(ValueError, match="unobserved branch"):
        analyze(spring, branches, expected_tree_count=2)


def test_partial_missing_required_seed_state_is_not_inferred_from_total():
    spring, branches = fixture()
    branches[0]["num.filled"] = "NA"
    with pytest.raises(ValueError, match="required numeric source field"):
        analyze(spring, branches, expected_tree_count=2)


def test_six_year_exact_permutation_is_not_asymptotic_significance_claim():
    x = [0.5, 1.3, 1.55, 1.9, 2.25, 3.0]
    y = [0.13, 0.2037, 0.3239, 0.1538, 0.45, 0.489]
    out = _stage_test(x, y)
    assert out["spearman_annual"] == 0.828571
    assert out["exact_permutation_two_sided_exploratory"] == 0.058333
    assert _exact_permutation_p([1, 2, 3, 4, 5, 6],
                                [1, 2, 3, 4, 5, 6]) == pytest.approx(2/720)
    assert _stage_test([1]*6, [2]*6)["spearman_annual"] is None
    assert _stage_test([1]*6, [2]*6)["loo_year_relative_rmse_change"] is None


def test_tree_weighting_and_two_samara_sensitivity_are_not_equivalent():
    spring, branches = fixture()
    for year in YEARS:
        # One tiny second tree has perfect intact seed fraction.
        # In a typical-tree mean, this 2-samara tree counts as much
        # as the 10-samara original tree; in a samara fraction it doesn't.
        branches.append({
            "year": str(year), "tree": "HF2", "branch": "B",
            "treatment": "control",
            "num.filled": "2", "num.empty": "0", "num.grub": "0",
            "num.wrinkle": "0", "num.small": "0", "num.moldy": "0",
            "num.exit": "0", "num.missing": "0",
            "total.seed": "2", "mast.index": str(year - 2011),
        })
    annual, out = analyze(spring, branches, expected_tree_count=2)
    row = next(r for r in annual if r["year"] == 2012
               and r["treatment"] == "control")
    assert row["p_intact_among_classified"] == round(7/12, 8)
    ty = out["tree_vs_samara_unit_sensitivity"]
    all_tree = ty["minimum_classified_samaras_1"]
    ten_seed = ty["minimum_classified_samaras_10"]
    assert all_tree["tree_sample_count_by_year"][2012] == 2
    assert ten_seed["tree_sample_count_by_year"][2012] == 1
    assert all_tree["yearwise_tree_mean_stages"][
        "intact_fraction_all_classified"
    ]["2012"] == 0.75
    assert ten_seed["yearwise_tree_mean_stages"][
        "intact_fraction_all_classified"
    ]["2012"] == 0.5
