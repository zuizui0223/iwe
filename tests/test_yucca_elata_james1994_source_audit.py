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
