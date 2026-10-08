"""Source-grain checks for randomized spatial egg placement vs later-selected stages."""
import pandas as pd

RANDOMIZED = "data/source_reconstructions/labouche2013_randomized_egg_position.csv"
POSTATTACK = "data/source_reconstructions/labouche2013_postattack_fruit_abortion.csv"


def test_randomized_source_has_one_flower_per_plant_without_plant_fitness_promotion():
    rows = pd.read_csv(RANDOMIZED).set_index("endpoint")
    assert set(rows.index) == {
        "successful_fruit_attack",
        "initial_fruit_development",
        "fruit_mass_among_developed",
    }
    assert set(rows["egg_position_randomized"]) == {"yes"}
    assert set(rows["source_assignment_grain"]) == {"one_flower_per_female_plant"}
    assert set(rows["n_inside_assigned"]) == {71}
    assert set(rows["n_outside_assigned"]) == {66}
    assert set(rows["final_intact_seed_outcome"]) == {"no"}
    assert (rows["endpoint_day"] == 10).all()
    assert all(rows["doi"] == "10.1111/1365-2435.12062")


def test_randomized_placement_changes_attack_and_early_fruit_development():
    t = pd.read_csv(RANDOMIZED).set_index("endpoint")
    attack = t.loc["successful_fruit_attack"]
    develop = t.loc["initial_fruit_development"]
    assert attack["inside_group_mean"] == 44
    assert attack["outside_group_mean"] == 29
    assert attack["inside_reported_se"] == 8
    assert attack["outside_reported_se"] == 4
    assert attack["source_reported_p"] == 0.033
    assert develop["inside_group_mean"] == 83
    assert develop["outside_group_mean"] == 97
    assert develop["source_reported_p"] == 0.005
    assert attack["post_assignment_selection"] == "no"
    assert develop["post_assignment_selection"] == "no"
    # The means are across source populations, not reconstructed 71/66
    # binomial success counts at the assigned-plant level.
    assert set(t["measurement_unit"].iloc[:2]) == {"percent_population_means"}


def test_mass_and_abortion_condition_on_posttreatment_events():
    t = pd.read_csv(RANDOMIZED).set_index("endpoint")
    mass = t.loc["fruit_mass_among_developed"]
    assert mass["post_assignment_selection"] == "yes"
    assert mass["n_inside_endpoint"] == 63
    assert mass["n_outside_endpoint"] == 59
    assert mass["inside_group_mean"] == 511
    assert mass["outside_group_mean"] == 576
    post = pd.read_csv(POSTATTACK).iloc[0]
    assert post["successfully_attacked_aborted"] == 15
    assert post["successfully_attacked_total"] == 42
    assert post["not_successfully_attacked_aborted"] == 1
    assert post["not_successfully_attacked_total"] == 81
    assert post["causal_attack_vs_nonattack_randomized"] == "no"
    assert post["strict_partner_synchrony_measure"] == "no"
    assert post["final_intact_seed_outcome"] == "no"
    assert post["source_reported_p"] == "less_than_0.0001"


def test_not_strict_h1_effect_or_extra_replication():
    fx = pd.read_csv("data/extraction/direct_effects.csv")
    assert "LABOUCHE2013_SILENE_HADENA" not in set(fx["study_id"])
    assert not set(pd.read_csv(RANDOMIZED).columns) & {
        "adult_flight_DOY", "flowering_partner_overlap", "mature_intact_seeds",
    }
