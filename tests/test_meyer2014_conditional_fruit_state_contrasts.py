"""Published Berberis conditional fruit-state contrasts, not an H1 effect."""
import csv
from pathlib import Path

from scripts.build_meyer2014_conditional_fruit_state_contrasts import generate


OUTPUT = Path("data/derived/meyer2014_conditional_abortion_contrasts.csv")


def _read_rows():
    with OUTPUT.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return {(r["habitat"], int(r["seeds_per_retained_fruit"])): r for r in rows}


def test_descriptive_fruit_contrasts_match_source_counts_exactly():
    assert OUTPUT.read_text(encoding="utf-8") == generate()
    rows = _read_rows()
    assert len(rows) == 4
    assert set(rows) == {
        ("pine", 1), ("pine", 2),
        ("dry_scrub", 1), ("dry_scrub", 2),
    }
    expected = {
        ("pine", 1): (418, 38, -0.011962),
        ("pine", 2): (463, 80, +0.479563),
        ("dry_scrub", 1): (120, 194, +0.105842),
        ("dry_scrub", 2): (93, 496, +0.029570),
    }
    for key, (without_n, with_n, delta) in expected.items():
        r = rows[key]
        assert int(r["n_without_puncture"]) == without_n
        assert int(r["n_with_puncture"]) == with_n
        assert float(r["descriptive_risk_difference_with_minus_without"]) == delta


def test_single_seed_last_unit_not_always_protected_under_dry_conditions():
    rows = _read_rows()
    moist = rows[("pine", 1)]
    dry = rows[("dry_scrub", 1)]
    assert float(moist["descriptive_risk_difference_with_minus_without"]) < 0
    assert float(dry["descriptive_risk_difference_with_minus_without"]) > 0.10
    # This is a contrast of nested observational retained fruits:
    # it does NOT identify an individual-plant causal puncture×drought effect.


def test_conditional_nonaborted_seed_bound_is_not_viable_seed_count():
    for r in _read_rows().values():
        nseed = int(r["seeds_per_retained_fruit"])
        for k in (
            "nonaborted_seeds_per_retained_fruit_upper_bound_without",
            "nonaborted_seeds_per_retained_fruit_upper_bound_with",
        ):
            ub = float(r[k])
            assert 0 <= ub <= nseed
        assert r["source_inference_limit"] == (
            "observed_fruit_state_only_not_intact_seed_or_plant_fitness"
        )
    # The paper explicitly pools larva-eaten and living nonaborted seeds:
    # lower bound on living from this state table alone is zero, and
    # neither bound includes whole-fruit losses before sampling.
