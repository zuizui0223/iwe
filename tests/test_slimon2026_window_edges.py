"""Synthetic unit grains: source events are not final intact seeds."""
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts.analyze_slimon2026_window_edges import (
    _date_doy, _source_full_date_year, audit_experiment,
)


def _csv(data):
    columns = data[0]
    return "\n".join([",".join(map(str, row)) for row in data]) + "\n"


def _zip_source():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        for exp in ("exp1", "exp2"):
            n = 14
            host = [["ID", "first_flr", "num_flr", "geno"]]
            last = [["ID", "last_flower"]]
            fit = [["ID", "schinia", "lg frt", "sm frt", "abort"]]
            mompha = [["ID", "FINAL_Mompha"]]
            stage = [["ID", "sf_larvae_7_26"]]
            for i in range(n):
                host.append([str(i), 190 + i, 10 + i, "2"])
                last.append([str(i), 205 + i,])
                fit.append([str(i), i, 2 + i, 3 + i, 0])
                mompha.append([str(i), i % 6])
                stage.append([str(i), i % 3])
                if exp == "exp2":
                    stage.append([str(i), i % 2])
            prefix = "Freese Stats/"
            z.writestr(prefix + ("main_exp1.csv" if exp == "exp1" else "main_exp2.csv"), _csv(host))
            z.writestr(prefix + ("d_pheno.csv" if exp == "exp1" else "d_pheno_exp2.csv"), _csv(last))
            z.writestr(prefix + ("fitness_exp1.csv" if exp == "exp1" else "Exp 2 fitness.csv"), _csv(fit))
            z.writestr(prefix + ("comp_final_sum_exp1.csv" if exp == "exp1" else "comp_final_sum_exp2.csv"), _csv(mompha))
            z.writestr(prefix + ("df2_exp1F.csv" if exp == "exp1" else "df2_exp2F.csv"), _csv(stage))
    return b.getvalue()


def test_two_cohorts_have_real_plant_grain_and_no_fake_seed_fitness():
    with ZipFile(BytesIO(_zip_source())) as zf:
        first = audit_experiment(zf, "exp1")
        second = audit_experiment(zf, "exp2")
    assert first["joint_plant_ids_n"] == 14
    assert second["joint_plant_ids_n"] == 14
    assert first["flowering_calendar_year"] == second["flowering_calendar_year"] == 2023
    assert second["original_tables"]["schinia_stage"]["repeated_measurement_rows"] == 14
    assert first["source_date_scale_crosscheck"]["n_last_before_first"] == 0
    assert first["strict_h1_effect_eligible"] is False
    assert "opportunity_adjustment_assumption" in first
    proxies = [a for a in first["exploratory_correlations"]
               if a["response_component"] == "mompha_per_opportunity_proxy"]
    assert len(proxies) == 2
    assert all(a["n"] == 14 for a in proxies)
    assert second["direct_final_seed_counts_obtained"] is False
    pair = [v for v in first["exploratory_correlations"]
            if v["phenology_axis"] == "first_doy"
            and v["response_component"] == "schinia_fruit_count"]
    assert len(pair) == 1
    assert pair[0]["rho"] == 1.0


def test_missing_dates_fail_source_relative_figure_coordinate_check():
    assert _date_doy("2022-07-11", 2022) == 192
    assert _date_doy("2023-07-11", 2022) != 192
    assert _date_doy("366", 2023) == 366  # audited upstream; do not invent time series


def test_any_duplicate_plant_id_fails_instead_of_join_multiplication():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        z.writestr("Freese Stats/main_exp1.csv", "ID,first_flr,num_flr,geno\n1,190,10,2\n1,191,11,2\n")
        z.writestr("Freese Stats/d_pheno.csv", "ID,last_flower\n1,222\n")
        z.writestr("Freese Stats/fitness_exp1.csv", "ID,schinia,lg frt,sm frt,abort\n1,2,3,5,0\n")
        z.writestr("Freese Stats/comp_final_sum_exp1.csv", "ID,FINAL_Mompha\n1,1\n")
        z.writestr("Freese Stats/df2_exp1F.csv", "ID #,sf_adult_7_11\n1,2\n")
    with ZipFile(BytesIO(b.getvalue())) as zf:
        with pytest.raises(ValueError, match="duplicate"):
            audit_experiment(zf, "exp1")


def test_original_experiment_number_cannot_relabel_source_calendar_year():
    assert _source_full_date_year("7/12/23") == 2023
    assert _source_full_date_year("7/12/2023") == 2023
    assert _source_full_date_year("192") is None
    assert _source_full_date_year("NA") is None


def test_conditional_two_edge_rank_is_not_an_unadjusted_risk_estimate():
    import pandas as pd
    from scripts.analyze_slimon2026_window_edges import (
        _partial_rank_window_association,
    )
    rows = [
        {
            "first_doy": 170 + (i % 13),
            "last_doy": 230 + ((i * 7) % 17),
            "mompha_per_opportunity_proxy": (
                0.15 + (i % 13) * 0.01 + ((i * 3) % 5) * 0.001
            ),
            "geno": "2" if i % 2 else "6",
            "source_treatment": "JA" if i % 3 else "control",
        }
        for i in range(54)
    ]
    out = _partial_rank_window_association(
        pd.DataFrame(rows),
        "first_doy", "mompha_per_opportunity_proxy", "last_doy",
    )
    assert out["n"] == 54
    assert out["status"] == "descriptive_conditional_association_no_inference"
    assert out["partial_rank_rho"] > 0.3
    assert out["source_genotype_categories"] == 2
    assert out["source_treatment_categories"] == 2
