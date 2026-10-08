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
        "IMAI2006_AUCUBA"
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
    assert len(df) == 5
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
