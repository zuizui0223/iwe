import pandas as pd
import pytest
from iwe.host_portfolio_sensitivity import build_portfolio_sensitivity


def toy():
    # Baseline native A,B; current A,B,C,D; new C,D.
    # Adding a host native in C makes old "new C" a native region.
    # Adding another host introduced in E creates a new added region.
    frozen = pd.DataFrame([
        {"accepted_plant_name_id": "1", "accepted_name": "BaseA",
         "native_host_units": 1, "contemporary_host_units": 3},
        {"accepted_plant_name_id": "2", "accepted_name": "BaseB",
         "native_host_units": 1, "contemporary_host_units": 2},
    ])
    all_records = []
    raw = [
        ("1", "BaseA", "frozen_host", {"A"}, {"A", "C", "D"}),
        ("2", "BaseB", "frozen_host", {"B"}, {"B", "D"}),
        ("3", "Arabis hirsuta",
         "observed_egg_candidate_not_confirmed_larval_viability", {"C"}, {"C"}),
        ("4", "Arabidopsis thaliana",
         "observed_egg_candidate_not_confirmed_larval_viability", {"B"}, {"B", "E"}),
        ("5", "Noccaea caerulescens",
         "observed_egg_candidate_not_confirmed_larval_viability", {"A"}, {"A"}),
    ]
    for ident, name, role, nat, curr in raw:
        for region in curr:
            all_records.append({
                "accepted_plant_name_id": ident,
                "accepted_name": name, "source_role": role,
                "area_code_l3": region,
                "native_present": region in nat,
                "contemporary_present": True,
            })
    return pd.DataFrame(all_records), frozen


def run(d=None, b=None):
    orig, baseline = toy()
    return build_portfolio_sensitivity(
        d if d is not None else orig, b if b is not None else baseline,
        baseline_counts=(2, 4, 2), frozen_n=2,
    )


def test_full_powerset_and_nonmonotone_added_geography():
    table, region, receipt = run()
    assert len(table) == 8
    assert receipt["frozen_baseline"] == {"native": 2, "contemporary": 4, "added": 2}
    full = table.loc[table["candidate_count"] == 3].iloc[0]
    assert (full["native_units"], full["contemporary_units"],
            full["introduced_added_units"]) == (3, 5, 2)
    assert full["baseline_added_now_native"] == 1
    assert full["newly_added_after_host_extension"] == 1
    arabis = table.loc[table["added_candidate_species"] == "Arabis hirsuta"].iloc[0]
    assert arabis["introduced_added_units"] == 1
    arabidopsis = table.loc[
        table["added_candidate_species"] == "Arabidopsis thaliana"
    ].iloc[0]
    assert arabidopsis["introduced_added_units"] == 3
    transitions = region.loc[region["scenario"] == full["scenario"]]
    assert set(transitions.loc[
        transitions["transition"] == "old_added_now_native",
        "area_code_l3"
    ]) == {"C"}
    assert set(transitions.loc[
        transitions["transition"] == "new_added_after_host_extension",
        "area_code_l3"
    ]) == {"E"}


def test_frozen_plant_source_mismatch_rejected():
    d, b = toy()
    d = d.loc[~((d["accepted_plant_name_id"] == "1") &
                (d["area_code_l3"] == "A"))]
    with pytest.raises(ValueError, match="frozen host WCVP source drift"):
        run(d=d, b=b)


def test_candidate_coverage_and_identity_rejected_when_incomplete():
    d, b = toy()
    d = d.loc[d["accepted_name"] != "Noccaea caerulescens"]
    with pytest.raises(ValueError, match="candidate name resolution"):
        run(d=d, b=b)
    d, b = toy()
    d.loc[d["accepted_name"] == "Noccaea caerulescens",
          "accepted_plant_name_id"] = "3"
    with pytest.raises(ValueError, match="nonunique accepted source"):
        run(d=d, b=b)


def test_duplicate_region_and_invalid_truth_flag_rejected():
    d, b = toy()
    with pytest.raises(ValueError, match="duplicate plant"):
        run(d=pd.concat([d, d.iloc[[0]]], ignore_index=True), b=b)
    d, b = toy()
    # Pandas 3 disallows assigning a string into a boolean dtype in-place.
    d["native_present"] = d["native_present"].astype(object)
    d.loc[0, "native_present"] = "unknown"
    with pytest.raises(ValueError, match="explicit true/false"):
        run(d=d, b=b)


def test_no_larval_viability_or_strict_h1_claim():
    _, _, receipt = run()
    assert receipt["egg_receipt_confirms_larval_suitability"] is False
    assert receipt["octoploid_cardamine_added_as_new_species"] is False
    assert receipt["causal_colonization_effect_identified"] is False
    assert receipt["new_iwe_strict_h1_effects"] == 0
