import pandas as pd
import pytest

from iwe.chocho_bridge import (
    build_candidate_resource_crosswalk,
    screen_spatiotemporal_windows,
)


def _candidates():
    return pd.DataFrame([
        {
            "candidate_id": "ANT002_CARDAMINE_ANTHOCHARIS_2024",
            "animal_taxon": "Anthocharis cardamines",
            "plant_taxon": "Cardamine pratensis",
            "target_class": "antagonist",
            "status": "blocked_timing_linkage",
        },
        {
            "candidate_id": "UNRESOLVED",
            "animal_taxon": "Anthocharis spp.",
            "plant_taxon": "Cardamine pratensis",
            "target_class": "antagonist",
            "status": "rejected_timing",
        },
    ])


def _metrics():
    return pd.DataFrame([
        {
            "species": "Anthocharis cardamines",
            "native_resource_units": 162,
            "contemporary_resource_units": 272,
            "introduced_added_units": 110,
            "resolved_host_species": 11,
        },
        {
            "species": "Papilio machaon",
            "native_resource_units": 191,
            "contemporary_resource_units": 191,
            "introduced_added_units": 0,
            "resolved_host_species": 54,
        },
    ])


def _pairs():
    return pd.DataFrame([
        {"insect_species": "Anthocharis cardamines", "accepted_name": "Cardamine pratensis"}
    ])


def _windows(**overrides):
    row = {
        "candidate_id": "ANT002_CARDAMINE_ANTHOCHARIS_2024",
        "host_taxon": "Cardamine pratensis",
        "wgsrpd3_unit": "ABC",
        "year": 2013,
        "range_origin": "introduced",
        "host_range_source": "synthetic:WCVP-regional-unit",
        "host_window_source": "synthetic:observed-plant",
        "partner_window_source": "synthetic:independent-female-capture",
        "host_window_basis": "observed_host_phenophase",
        "partner_window_basis": "independent_adult_activity",
        "host_start_doy": 100,
        "host_end_doy": 120,
        "partner_start_doy": 110,
        "partner_end_doy": 130,
    }
    row.update(overrides)
    return pd.DataFrame([row])


def test_exact_match_reproduces_frozen_anthocharis_geography_without_admission():
    out = build_candidate_resource_crosswalk(_candidates(), _metrics())
    assert len(out) == 1
    row = out.iloc[0]
    assert row["chocho_species"] == "Anthocharis cardamines"
    assert row["native_resource_units"] == 162
    assert row["contemporary_resource_units"] == 272
    assert row["introduced_added_units"] == 110
    assert row["geographic_expansion_ratio"] == pytest.approx(272 / 162)
    assert row["host_pair_status"] == "not_checked"
    assert row["geographic_aggregation"] == "butterfly_union_all_resolved_hosts"
    assert row["iwe_candidate_status"] == "blocked_timing_linkage"
    assert not bool(row["strict_h1_effect_admitted"])


def test_host_pair_confirmed_only_by_explicit_sidecar():
    out = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    assert out.loc[0, "host_pair_status"] == "confirmed_in_hosts_sidecar"
    missing = _pairs().assign(accepted_name="Cardamine hirsuta")
    unresolved = build_candidate_resource_crosswalk(_candidates(), _metrics(), missing)
    assert unresolved.loc[0, "host_pair_status"] == "not_found_in_supplied_sidecar"


def test_geography_reconciliation_fails_closed():
    bad = _metrics().copy()
    bad.loc[0, "introduced_added_units"] = 111
    with pytest.raises(ValueError, match="increments do not reconcile"):
        build_candidate_resource_crosswalk(_candidates(), bad)


def test_duplicate_metrics_and_candidate_ids_rejected():
    with pytest.raises(ValueError, match="duplicate species"):
        build_candidate_resource_crosswalk(
            _candidates(), pd.concat([_metrics(), _metrics().iloc[[0]]])
        )
    with pytest.raises(ValueError, match="duplicate candidate_id"):
        build_candidate_resource_crosswalk(
            pd.concat([_candidates(), _candidates().iloc[[0]]]), _metrics()
        )


def test_temporal_index_is_proxy_not_plant_fitness():
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    out = screen_spatiotemporal_windows(
        _windows(), crosswalk, allow_synthetic=True
    )
    assert out.loc[0, "phenophase_jaccard"] == pytest.approx(1 / 3)
    assert out.loc[0, "host_window_fraction"] == pytest.approx(0.5)
    assert out.loc[0, "range_origin"] == "introduced"
    assert out.loc[0, "source_tier"] == "proxy_only"
    assert not bool(out.loc[0, "strict_h1_effect_admitted"])
    assert "smd" not in " ".join(out.columns).lower()


def test_unverified_host_pair_cannot_compute_temporal_layer():
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics())
    with pytest.raises(ValueError, match="not confirmed"):
        screen_spatiotemporal_windows(_windows(), crosswalk, allow_synthetic=True)


@pytest.mark.parametrize("bad_window", [
    {"partner_window_basis": "egg_receipt"},
    {"host_window_basis": "damage"},
    {"range_origin": "unspecified"},
    {"host_window_source": ""},
    {"host_end_doy": 100},
    {"year": 2012.5},
    {"host_taxon": "Cardamine hirsuta"},
])
def test_invalid_or_recycled_time_evidence_never_enters_proxy(bad_window):
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    with pytest.raises(ValueError):
        screen_spatiotemporal_windows(
            _windows(**bad_window), crosswalk, allow_synthetic=True
        )


def test_synthetic_time_cannot_be_labeled_real_by_default():
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    with pytest.raises(ValueError, match="synthetic provenance"):
        screen_spatiotemporal_windows(_windows(), crosswalk)


def test_independent_regions_not_collapsed_or_filled_across_years():
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    one = _windows()
    two = _windows(year=2014, wgsrpd3_unit="DEF",
                   host_start_doy=100, host_end_doy=110,
                   partner_start_doy=120, partner_end_doy=140)
    out = screen_spatiotemporal_windows(
        pd.concat([one, two], ignore_index=True), crosswalk, allow_synthetic=True
    )
    assert len(out) == 2
    assert out["year"].tolist() == [2013, 2014]
    assert out["phenophase_jaccard"].tolist() == pytest.approx([1 / 3, 0])


def test_duplicate_regional_year_windows_rejected():
    crosswalk = build_candidate_resource_crosswalk(_candidates(), _metrics(), _pairs())
    with pytest.raises(ValueError, match="duplicated"):
        screen_spatiotemporal_windows(
            pd.concat([_windows(), _windows()], ignore_index=True),
            crosswalk, allow_synthetic=True
        )
