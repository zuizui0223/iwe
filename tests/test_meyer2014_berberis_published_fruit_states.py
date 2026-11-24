"""Source-exact fruit state counts, nonpromoting and no naive nested inference."""
import pandas as pd

SOURCE = "data/source_reconstructions/meyer2014_berberis_published_fruit_states.csv"


def _source():
    t = pd.read_csv(SOURCE)
    return t.set_index(["source_treatment", "seeds_per_fruit"])


def test_original_table1_source_counts_and_denominators():
    t = _source()
    expected = {
        ("P_minus", 2): (11, 131, 321, 463),
        ("P_plus", 2): (2, 61, 17, 80),
        ("S_minus", 2): (5, 64, 24, 93),
        ("S_plus", 2): (49, 356, 91, 496),
        ("P_minus", 1): (16, 402, 418),
        ("P_plus", 1): (1, 37, 38),
        ("S_minus", 1): (4, 116, 120),
        ("S_plus", 1): (27, 167, 194),
    }
    assert set(t.index) == set(expected)
    for (trt, nseed), values in expected.items():
        row = t.loc[(trt, nseed)]
        if nseed == 2:
            a, b, c, total = values
            assert tuple(int(row[k]) for k in ("F0_two_aborted", "F1_one_aborted", "F2_zero_aborted", "fruits_n")) == values
            assert a + b + c == total
        else:
            a, b, total = values
            assert tuple(int(row[k]) for k in ("f0_single_aborted", "f1_single_not_aborted", "fruits_n")) == values
            assert a + b == total


def test_pine_puncture_association_is_sibling_contingent_not_intact_seed_yield():
    t = _source()
    p2 = t.loc[("P_plus", 2)]
    u2 = t.loc[("P_minus", 2)]
    p1 = t.loc[("P_plus", 1)]
    u1 = t.loc[("P_minus", 1)]
    # Among two-seeded fruits, one aborted / two seeds (both nonaborted)
    # jumps from 131/463 to 61/80 with puncture.
    assert p2["F1_one_aborted"] / p2["fruits_n"] > .75
    assert u2["F1_one_aborted"] / u2["fruits_n"] < .30
    # The last available one-seeded unit does not show analogous elevation
    # in the same observational pine comparison (only 38 punctured fruits).
    assert p1["f0_single_aborted"] / p1["fruits_n"] < .03
    assert u1["f0_single_aborted"] / u1["fruits_n"] > .035
    # Nonaborted explicitly combines undamaged AND larva-eaten seeds:
    assert (t["nonaborted_contains_predated_seed"] == "yes").all()
    assert set(t["original_outcome_description"]) == {
        "source_fruit_state_not_verified_intact_seed"
    }


def test_no_pseudoreplicated_strict_h1_promotion():
    t = _source().reset_index()
    assert len(t) == 8
    assert set(t["study_id"]) == {"MEYER2014_BERBERIS"}
    assert "partner_adult_flight_DOY" not in t.columns
    assert "flowering_date" not in t.columns
    assert "plant_id" not in t.columns
    effects = pd.read_csv("data/extraction/direct_effects.csv")
    assert "MEYER2014_BERBERIS" not in set(effects["study_id"])
