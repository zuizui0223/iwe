"""Synthetic unit grains: source events are not final intact seeds."""
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts.analyze_slimon2026_window_edges import (
    _date_doy, _safe_spearman, audit_year,
)


def _csv(data):
    columns = data[0]
    return "\n".join([",".join(map(str, row)) for row in data]) + "\n"


def _zip_source():
    b = BytesIO()
    with ZipFile(b, "w") as z:
        for year, exp in ((2022, "exp1"), (2023, "exp2")):
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
        first = audit_year(zf, 2022)
        second = audit_year(zf, 2023)
    assert first["joint_plant_ids_n"] == 14
    assert second["joint_plant_ids_n"] == 14
    assert second["original_tables"]["schinia_stage"]["repeated_measurement_rows"] == 14
    assert first["source_date_scale_crosscheck"]["n_last_before_first"] == 0
    assert first["strict_h1_effect_eligible"] is False
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
            audit_year(zf, 2022)
