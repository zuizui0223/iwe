"""Original public README is metadata, not recovered experiment-level CSVs."""
import csv
from pathlib import Path

REGISTRY = Path(
    "data/source_reconstructions/jadera2025_benefit_cost_unit_matrix.csv"
)
REPORT = Path("docs/JADERA2025_README_STAGE_AND_UNIT_ADMISSION_20261019.md")


def _data():
    with REGISTRY.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_five_components_cannot_be_five_independent_fitness_programmes():
    data=_data()
    assert len(data)==5
    assert {x["programme"] for x in data}=={"JADERA2025"}
    assert {x["source_experiment"] for x in data}=={
        "pollen_capture", "greenhouse_pollination",
        "field_pollination", "adult_nectar_survival",
        "nymph_seed_viability",
    }
    assert all(x["strict_h1_eligible"]=="no" for x in data)
    assert all(x["source_only_evidence_status"].endswith(
        "original_CSV_bytes_blocked"
    ) for x in data)


def test_greenhouse_pod_removal_and_cluster_grain_not_final_seed_fitness():
    data={d["source_experiment"]:d for d in _data()}
    green=data["greenhouse_pollination"]
    assert green["n_stated"]=="48_plants_16_tents_3_plants_per_tent"
    assert green["recorded_endpoint"]=="seedpods_per_flower_over_seven_weeks"
    assert green["source_linked_viable_terminal_seed"]=="no_seedpods_removed_early"
    assert "not_independent_wild_adult_activity" in green["partner_timing_provenance"]
    assert data["nymph_seed_viability"]["n_stated"]=="30_seeds_per_nymph_dose_reported"
    assert "0_vs_1_vs_2_vs_3_vs_4_nymphs_per_seed"==(
        data["nymph_seed_viability"]["experimental_intervention"]
    )
    assert data["field_pollination"]["observational_grain"]==(
        "inflorescence_branch_nested_tree_and_year"
    )


def test_source_metadata_is_not_source_data_or_strict_h1_admission():
    doc=REPORT.read_text(encoding="utf-8")
    norm=" ".join(doc.lower().split())
    for term in (
        "original csv bytes", "http 401", "403",
        "seedpods", "removed", "independent wild-adult",
        "same biological unit", "mixed", "mutualist 2",
    ):
        assert term in norm
    assert "first hemiptera" in norm
    assert "strict-h1 independent clusters remain" in norm
