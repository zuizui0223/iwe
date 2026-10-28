"""Evidence-grade controls: naturally chosen Rheum egg receipt is not randomized."""
from pathlib import Path
import pandas as pd

SOURCE = Path("data/source_reconstructions/song2016_rheum_causal_design_audit.csv")


def test_only_pollen_type_was_source_randomized():
    table = pd.read_csv(SOURCE)
    assert len(table) == 6
    random = table.loc[
        table["design_type"] == "randomized_within_plant_flowers"
    ]
    assert len(random) == 1
    assert random.iloc[0]["source_component"] == "pollination_source_comparison"
    assert random.iloc[0]["randomly_assigned_variable"] == (
        "open_vs_hand_self_vs_hand_cross"
    )
    assert set(table["can_identify_effect_of_oviposition"]) == {"no"}
    assert set(table["can_identify_IAA_mediation"]) == {"no"}
    assert set(table["has_final_intact_seeds"]) == {"no"}
    assert all(table["n_independent_plants_per_comparison"].dropna() <= 8)


def test_oviposition_and_IAA_observations_do_not_form_a_randomized_mediator_chain():
    table = pd.read_csv(SOURCE).set_index("source_component")
    exposure = table.loc["naturally_oviposited_vs_intact"]
    auxin = table.loc["natural_fly_eggs_vs_hand_pollinated_no_fly"]
    assert exposure["design_type"] == "observational_fly_choice"
    assert exposure["n_independent_plants_per_comparison"] == 7
    assert exposure["biological_unit"] == "plant_with_200_marked_flowers"
    assert "F_1_24_287.24" in exposure["source_result"]
    assert auxin["design_type"] == "observational_and_intervention_confounded"
    assert auxin["n_independent_plants_per_comparison"] == 5
    assert "bag_and_hand_pollination" in auxin["causal_identification_note"]
    assert "F_355.97" in auxin["source_result"]


def test_strict_effects_unchanged_and_nonsignificance_not_equivalence():
    table = pd.read_csv(SOURCE)
    assert (
        table.loc[table["source_component"] == "within_plant_flower_sequence",
                  "design_type"].iloc[0] == "observational_phenology"
    )
    assert (
        table.loc[
            table["source_component"] == "pollen_load_feeding_vs_feeding_oviposition",
            "causal_identification_note",
        ].iloc[0] ==
        "nonsignificant_difference_is_not_equivalence_of_pollen_service"
    )
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert "SONG2016_RHEUM" not in set(effects["study_id"])
