"""Source-design proof obligations for host-fate forecasting vs inducing."""
import pandas as pd

MATRIX = "data/source_reconstructions/host_retention_causal_gate_matrix.csv"
RHEUM = "data/source_reconstructions/song2016_rheum_causal_design_audit.csv"


def test_rheum_pollen_randomized_but_fly_oviposition_self_selected():
    df = pd.read_csv(RHEUM).set_index("source_component")
    assert len(df) == 6
    random = df[df["design_type"] == "randomized_within_plant_flowers"]
    assert list(random.index) == ["pollination_source_comparison"]
    assert random.iloc[0]["randomly_assigned_variable"] == (
        "open_vs_hand_self_vs_hand_cross"
    )
    assert set(df["can_identify_effect_of_oviposition"]) == {"no"}
    assert set(df["can_identify_IAA_mediation"]) == {"no"}
    assert set(df["has_final_intact_seeds"]) == {"no"}
    assert df.loc["naturally_oviposited_vs_intact", "design_type"] == (
        "observational_fly_choice"
    )
    assert df.loc["naturally_oviposited_vs_intact",
                  "n_independent_plants_per_comparison"] == 7
    assert df.loc["natural_fly_eggs_vs_hand_pollinated_no_fly",
                  "n_independent_plants_per_comparison"] == 5
    assert "bag_and_hand_pollination" in df.loc[
        "natural_fly_eggs_vs_hand_pollinated_no_fly",
        "causal_identification_note"
    ]


def test_experimental_timing_and_cue_controls_are_not_merged_with_observations():
    df = pd.read_csv(MATRIX).set_index("programme")
    assert set(df.index) == {
        "SONG2016_RHEUM", "OSTERGARD2007_LATHYRUS",
        "MEYER2014_BERBERIS", "JADEJA2017_YUCCA",
        "IMAI2006_AUCUBA", "GOTO2010_GLOCHIDION",
        "BRODY2000_IPOMOPSIS", "LABOUCHE2013_SILENE_HADENA"
    }
    assert df.loc["SONG2016_RHEUM", "independent_randomized_exposure"] == (
        "pollen_source_only"
    )
    assert df.loc["JADEJA2017_YUCCA", "independent_randomized_exposure"] == (
        "basal_fruit_presence"
    )
    assert df.loc["IMAI2006_AUCUBA", "independent_randomized_exposure"] == (
        "oviposition_date"
    )
    assert (df["strict_h1_eligible_from_this_source"] == "no").all()


def test_true_plant_fitness_not_automatically_obtained_from_retained_fruits():
    df = pd.read_csv(MATRIX)
    assert len(df) == 8
    assert df.loc[
        df["programme"] == "SONG2016_RHEUM",
        "final_intact_seed_by_exposure_available",
    ].iloc[0] == "no"
    assert df.loc[
        df["programme"] == "MEYER2014_BERBERIS",
        "final_intact_seed_by_exposure_available",
    ].iloc[0] == "no"
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert not any(effects["study_id"].isin(df["programme"]))


def test_same_observed_egg_retention_table_can_be_generated_by_two_causal_models():
    # SYNTHETIC identifiability counterexample, NOT Rheum source data.
    # Same observed (egg,retention) frequencies for:
    # A. randomly assigned eggs increase retention, or
    # B. latent initially favorable host state drives female choice
    #    AND independently drives retention, with eggs having no effect.
    observed = {
        (1, 1): 0.40, (1, 0): 0.10,
        (0, 1): 0.20, (0, 0): 0.30,
    }
    randomized_manipulation = {
        (o, y): (0.5 * (0.8 if y else 0.2) if o else
                 0.5 * (0.4 if y else 0.6))
        for o in (0, 1) for y in (0, 1)
    }
    latent = {1: 0.6, 0: 0.4}
    # P(eggs=1 | host state U=1)=2/3; P(eggs=1 | U=0)=1/4
    selection_only = {
        (o, y): latent[y] * (
            ((2 / 3) if o else (1 / 3)) if y == 1
            else ((1 / 4) if o else (3 / 4))
        )
        for o in (0, 1) for y in (0, 1)
    }
    for event, target in observed.items():
        assert abs(randomized_manipulation[event] - target) < 1e-12
        assert abs(selection_only[event] - target) < 1e-12
    # This is a possible-model proof that observational significance
    # cannot distinguish egg-induced retention from preferential egg choice.


def test_glochidion_modelled_counterfactual_is_not_randomized_seed_fitness():
    source = pd.read_csv(
        "data/source_reconstructions/goto2010_glochidion_abortions_costs.csv"
    ).iloc[0]
    assert source["modelled_seed_production_gain_pct"] == 16
    assert source["max_reported_moth_fitness_loss_pct"] == 62
    assert source["plant_counterfactual_comparator"] == (
        "modelled_random_flower_abortion"
    )
    assert source["adult_phenology_timing_contrast"] == "no"
    assert source["raw_same_unit_plant_fitness_available"] == "no"
    benchmark = pd.read_csv(MATRIX).set_index("programme")
    assert benchmark.loc["GOTO2010_GLOCHIDION",
                         "independent_randomized_exposure"] == "no"
    assert benchmark.loc["GOTO2010_GLOCHIDION",
                         "strict_h1_eligible_from_this_source"] == "no"


def test_published_2000_no_choice_experiment_is_not_equated_to_pure_egg_injection():
    table = pd.read_csv(MATRIX).set_index("programme")
    row = table.loc["BRODY2000_IPOMOPSIS"]
    assert row["source_doi"] == "10.1007/PL00008867"
    assert row["independent_randomized_exposure"] == (
        "forced_no_choice_female_caging_random_assignment_not_verified"
    )
    assert row["final_intact_seed_by_exposure_available"] == "no"
    assert row["strict_h1_eligible_from_this_source"] == "no"
    assert "caging" in row["remaining_unresolved_mechanism"]


def test_labouche_randomized_egg_location_is_not_randomized_flower_trait():
    row = pd.read_csv(MATRIX).set_index("programme").loc[
        "LABOUCHE2013_SILENE_HADENA"
    ]
    assert row["interaction_type"] == "mixed_pollinating_seed_predator"
    assert row["source_doi"] == "10.1111/1365-2435.12062"
    assert row["independent_randomized_exposure"] == "egg_position_inside_vs_outside"
    assert row["final_intact_seed_by_exposure_available"] == "no"
    assert row["strict_h1_eligible_from_this_source"] == "no"
    assert "corolla_length_observational" in row["remaining_unresolved_mechanism"]

    random = pd.read_csv(
        "data/source_reconstructions/labouche2013_randomized_egg_position.csv"
    ).set_index("endpoint")
    assert set(random["n_inside_assigned"]) == {71}
    assert set(random["n_outside_assigned"]) == {66}
    assert random.loc["successful_fruit_attack", "source_reported_p"] == 0.033
    assert random.loc["initial_fruit_development", "source_reported_p"] == 0.005
    assert random.loc["fruit_mass_among_developed", "post_assignment_selection"] == "yes"


def test_labouche_natural_trait_association_and_non_significant_service_are_not_equivalence():
    rows = pd.read_csv(
        "data/source_reconstructions/labouche2013_trait_position_service.csv"
    ).set_index("source_component")
    assert set(rows.index) == {
        "natural_flower_morphology_vs_egg_position",
        "natural_egg_position_vs_fertilized_ovules",
        "natural_tube_length_vs_fertilized_ovules_no_egg",
    }
    morph = rows.loc["natural_flower_morphology_vs_egg_position"]
    assert morph["design"] == "observational_common_garden"
    assert morph["analysis_n"] == 71
    assert morph["source_coefficient"] == -4.69
    assert morph["source_coefficient_se"] == 1.5
    assert morph["source_p"] == 0.003
    assert morph["fitted_crossover_mm"] == 19
    assert morph["randomized_predictor"] == "no"
    assert morph["causal_crossover_identified"] == "no"
    service = rows.loc["natural_egg_position_vs_fertilized_ovules"]
    assert service["analysis_n"] == 80
    assert service["source_p"] == 0.2
    assert service["equivalence_test"] == "no"
    assert service["randomized_predictor"] == "no"
    assert (
        rows.loc["natural_tube_length_vs_fertilized_ovules_no_egg", "source_p"]
        == 0.47
    )
