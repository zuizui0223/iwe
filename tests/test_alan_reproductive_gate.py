"""Scientific guards for the 2026 ALAN reproduction evidence crosswalk."""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

from iwe.alan_reproductive_gate import build_crossstudy_readiness
from iwe.alan_li_source import audit_li_original, ORIGINAL_GIT_BLOB_SHA1

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "data/registry/alan_reproduction_programmes_v01.csv"
C = ROOT / "data/registry/alan_reproduction_claims_v01.csv"


def inputs():
    return (pd.read_csv(P, dtype=str, keep_default_na=False),
            pd.read_csv(C, dtype=str, keep_default_na=False))


def synthetic_li():
    """Artificial data with 3 fields and 3 taxa; never marked source-verified."""
    out = io.StringIO()
    fields = ["round", "Treatment", "replicate", "species", "pollinated",
              "Seeds", "Fruit", "Label", "id"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for field in (1, 2, 3):
        for treatment in ("C", "P", "L"):
            for species in ("ML", "SN", "ZC"):
                yes = int(treatment == "L" or (treatment == "P" and field == 1))
                writer.writerow({
                    "round": 1, "Treatment": treatment, "replicate": field,
                    "species": species, "pollinated": yes,
                    "Seeds": yes * (field + 1), "Fruit": yes,
                    "Label": f"{field}-{treatment}-{species}", "id": "NA",
                })
    return out.getvalue().encode("utf-8")


def test_one_original_reproductive_chain_and_no_fabricated_meta():
    p, c = inputs()
    table, claims, result = build_crossstudy_readiness(p, c)
    assert len(table) == 9
    assert len(claims) == 14
    assert result["n_original_ALAN_manipulation_paper_rows"] == 8
    assert result["n_original_papers_with_reported_visit_pollen_reproduction"] == 1
    assert result["those_papers"] == ["LU_REPRO2026_TIBET"]
    assert result["n_complete_independent_seasonal_or_diel_phenophase_fitness_chains"] == 0
    assert result["n_complete_light_nursery_pollen_seedpredation_viableseed_chains"] == 0
    assert result["n_true_island_mainland_light_pollen_partner_reproduction_comparisons"] == 0
    assert result["new_strict_iwe_h1_effects"] == 0
    assert result["light_specific_reproductive_meta_effect"] is None
    row = table.set_index("study_id")
    assert not bool(row.loc["KENDALL2025_DIEL_META", "alan_manipulated"])
    assert not bool(row.loc["KENDALL2025_DIEL_META", "floral_schedule_measured"])
    assert bool(row.loc["SWISS_PHENO2026", "floral_schedule_measured"])
    assert not bool(row.loc["LI2026_UK", "conspecific_pollen_deposition_measured"])
    assert not bool(row.loc["BOOM2020_NETHERLANDS", "mature_seed_counts_measured"])


def test_dependent_lu_publications_are_not_falsely_independent():
    p, c = inputs()
    p.loc[p.study_id == "LU_REPRO2026_TIBET", "dependence_group"] = "independent_2026"
    with pytest.raises(ValueError, match="dependence unresolved"):
        build_crossstudy_readiness(p, c)


def test_egg_seed_count_cannot_become_pollen_data():
    p, c = inputs()
    p.loc[p.study_id == "LI2026_UK", "conspecific_pollen_deposition_measured"] = "yes"
    with pytest.raises(ValueError, match="not actually counted pollen"):
        build_crossstudy_readiness(p, c)
    p, c = inputs()
    p.loc[p.study_id == "BOOM2020_NETHERLANDS", "mature_seed_counts_measured"] = "yes"
    with pytest.raises(ValueError, match="NOT raw counted mature seeds"):
        build_crossstudy_readiness(p, c)


def test_real_light_vs_satellite_source_drift_rejected():
    p, c = inputs()
    p.loc[p.study_id == "KENDALL2025_DIEL_META", "alan_manipulated"] = "yes"
    with pytest.raises(ValueError, match="not an ALAN intervention"):
        build_crossstudy_readiness(p, c)
    p, c = inputs()
    p.loc[p.study_id == "KENDALL2025_DIEL_META", "floral_schedule_measured"] = "yes"
    with pytest.raises(ValueError, match="not same-site flowering phenophase"):
        build_crossstudy_readiness(p, c)


def test_original_source_claims_do_not_pass_as_new_significant_results():
    p, c = inputs()
    c.loc[
        (c.study_id == "BOOM2020_NETHERLANDS") &
        (c.endpoint == "estimated_seed_mean_ANOVA"),
        "numeric_value"
    ] = "0.01"
    with pytest.raises(ValueError, match="numeric drift"):
        build_crossstudy_readiness(p, c)
    p, c = inputs()
    c.loc[c.study_id == "KENDALL2025_DIEL_META", "verified_source_scope"] = (
        "original_author_publication_direct"
    )
    with pytest.raises(ValueError, match="not Kendall paper"):
        build_crossstudy_readiness(p, c)


def test_synthetic_seed_fixture_reconstructs_fields_but_never_authenticates():
    raw = synthetic_li()
    arms, fields, species, receipt = audit_li_original(raw, original_source_verified=False)
    assert len(arms) == 3
    assert len(fields) == 3
    assert len(species) == 6
    assert receipt["source_verified_original_git_blob"] is False
    assert receipt["field_signs_positive"] == 3
    assert receipt["original_field_blocks"] == 3
    assert receipt["original_source_git_blob_sha1"] != ORIGINAL_GIT_BLOB_SHA1
    assert receipt["source_pollinated_column_is_actual_conspecific_pollen"] is False
    assert receipt["observer_visitation_ever_measured_in_author_csv"] is False
    assert receipt["strict_iwe_h1_effects_created"] == 0
    with pytest.raises(ValueError, match="published original Git blob source changed"):
        audit_li_original(raw, original_source_verified=True)


def test_binary_seed_presence_is_derived_from_seed_counts_not_actual_stigma_pollen():
    text = synthetic_li().decode()
    corrupted = text.replace(",L,1,ML,1,2,1", ",L,1,ML,0,2,1")
    assert corrupted != text
    with pytest.raises(ValueError, match="Seeds > 0 rule failed"):
        audit_li_original(corrupted.encode(), original_source_verified=False)


def test_original_missing_seed_is_not_imputed_zero():
    text = synthetic_li().decode()
    text = text.replace(",P,2,ML,0,0,0", ",P,2,ML,NA,NA,NA")
    assert text != synthetic_li().decode()
    _, _, _, report = audit_li_original(text.encode(), original_source_verified=False)
    assert report["unknown_seed_outcome_plant_rows"] == 1
    assert report["source_verified_original_git_blob"] is False
