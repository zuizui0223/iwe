"""Non-promoting original-summary audit of James et al. 1994, Oikos 69:207–216."""
from pathlib import Path

import pandas as pd


SOURCE = Path("data/source_reconstructions/james1994_yucca_elata_source_summary.csv")
CANDIDATE_ID = "MIX002_YUCCA_ELATA_JAMES1994"


def test_source_summary_is_one_programme_not_11786_effects():
    t = pd.read_csv(SOURCE)
    assert len(t) == 1
    r = t.iloc[0]
    assert r["study_id"] == "JAMES1994_YUCCA_ELATA"
    assert r["article_doi"] == "10.2307/3546140"
    assert r["publication_year"] == 1994
    assert r["inflorescences_n"] == 38
    assert r["flowers_monitored_n"] == 11786
    assert r["mature_fruits_n"] == 699
    assert (t["independent_nightly_moth_activity_raw_recovered"] == "no").all()
    assert (t["night_to_viable_seeds_join_recovered"] == "no").all()


def test_pooled_fruit_fraction_is_not_reported_inflorescence_mean():
    row = pd.read_csv(SOURCE).iloc[0]
    pooled = row["mature_fruits_n"] / row["flowers_monitored_n"]
    assert pooled == 699 / 11786
    assert round(pooled * 100, 2) == 5.93
    assert abs(pooled - row["pooled_mature_fruits_per_monitored_flower"]) < 1e-8
    assert row["reported_mature_fruit_percent"] == 6.6
    assert row["reported_inflorescence_fruit_percent_min"] == 1.4
    assert row["reported_inflorescence_fruit_percent_max"] == 15.1
    # 5.93% and 6.6% summarize different potential aggregation grains;
    # neither supplies an individual-level variance or a source SEM.


def test_biological_host_retention_and_moth_summary_remains_nonpromoting():
    row = pd.read_csv(SOURCE).iloc[0]
    assert row["reported_fruit_retention_window_nights_mean"] == 5
    assert row["reported_window_fraction_of_flowering_period"] == 0.36
    assert row["observed_moth_pollinated_subset_n"] == 31
    assert row["reported_abortion_fraction_in_moth_pollinated_subset"] == 0.9
    assert row["moth_abundance_and_opening_recorded_nightly"] == "yes"
    assert row["relation_moth_abundance_to_mature_fruit_set"] == "no_detected_correlation"
    assert row["extra_hand_pollination_increased_mature_fruit_set"] == "no_significant_gain"
    assert "smd" not in " ".join(pd.read_csv(SOURCE).columns).lower()
    # Observed resource-limited context does not prove a unique cause
    # or justify a plant/inflorescence variance from flower counts.


def test_new_yucca_candidate_and_completion_route_are_nonpromoting():
    candidates = pd.read_csv("data/registry/replication_candidates.csv")
    rows = candidates.loc[candidates["candidate_id"].eq(CANDIDATE_ID)]
    assert len(rows) == 1
    row = rows.iloc[0]
    assert row["target_class"] == "mixed_pollinating_seed_predator"
    assert row["independent_programme"] == "yes"
    assert row["timing_window_measured"] == "yes"
    assert row["post_predation_final_reproduction"] == "partial"
    assert row["smd_summary_stats"] == "no"
    assert row["status"] == "blocked_final_surface"
    assert row["priority"] == "P2"

    routes = pd.read_csv("data/registry/replication_completion_routes.csv")
    route = routes.loc[routes["candidate_id"].eq(CANDIDATE_ID)]
    assert len(route) == 1
    assert route.iloc[0]["route_rank"] == 5
    assert route.iloc[0]["unlock_type"] == "same_unit_raw_data"
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert "JAMES1994_YUCCA_ELATA" not in set(effects["study_id"])
    # A new screening lead is not a quantitative independent replication.


def test_jadeja_experiment_changes_site_acceptance_not_proven_larval_fitness():
    stages = pd.read_csv(
        "data/source_reconstructions/jadeja2017_yucca_host_cue_stage_summary.csv"
    ).set_index("stage")
    assert set(stages.index) == {
        "flower_acceptance",
        "conditional_oviposition_intensity",
        "larval_emergence",
    }
    first = stages.loc["flower_acceptance"]
    second = stages.loc["conditional_oviposition_intensity"]
    last = stages.loc["larval_emergence"]
    assert first["n_trials"] == second["n_trials"] == 29
    assert first["n_positive_trials"] == second["n_positive_trials"] == 16
    assert first["reported_p"] == 0.048
    assert first["basal_fruit_association"] == "negative"
    assert second["reported_p"] == 0.61
    assert second["basal_fruit_association"] == "not_significant"
    assert last["n_fruits"] == 243
    assert last["reported_p"] == 0.7
    assert last["p_operator"] == "greater_than"
    assert all(stages["final_plant_intact_seed_endpoint"] == "no")
    assert (
        last["source_scope"] == "separate_observational_fruit_sample"
    )
    # Null tests do not prove equality, and distinct source units do not
    # establish prospective host-cue to larval survival to plant seed fitness.
