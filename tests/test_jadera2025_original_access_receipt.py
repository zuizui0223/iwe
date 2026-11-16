"""Jadera 2025 independent mixed system stays outside strict class inference."""
import pandas as pd
from pathlib import Path

DATA="data/source_reconstructions/jadera2025_public_original_access_gate.csv"


def test_official_dryad_public_version_without_source_file_rows():
    a=pd.read_csv(DATA)
    assert set(a.dryad_version_id)=={367420}
    assert a.original_file_metadata_public.eq("yes").all()
    assert a.original_file_bytes_recovered_github_runner.eq("no").all()
    assert a.strict_h1_effect_admitted.eq("no").all()
    assert a.independently_timed_adult_partner_activity_verified.eq("no").all()
    assert a.same_native_plant_unit_terminal_plant_seed_fitness_verified.eq("no").all()


def test_distinct_experiment_scopes_cannot_be_fake_net_fitness():
    x=pd.read_csv(DATA).set_index("route_id")
    assert x.loc["JAD2025-COST","experiment_type"]=="offspring_seed_viability_cost"
    assert x.loc["JAD2025-FIELD","experiment_type"]=="adult_pollination_field"
    assert x.loc["JAD2025-GREENHOUSE","experiment_type"]=="adult_pollination_greenhouse"
    assert x.loc["JAD2025-TIME","experiment_type"]=="greenhouse_timing_unreviewed"
    assert x.same_host_native_benefit_cost_linkage_verified.eq("no").all()
    d=Path(
        "docs/JADERA2025_MIXED_POLLINATION_SEED_COST_SOURCE_GATE_20261019.md"
    ).read_text(encoding="utf-8")
    assert "Cardiospermum halicacabum" in d
    assert "Koelreuteria elegans" in d
    assert "HTTP 401" in d and "HTTP 403" in d
    effects=pd.read_csv("data/extraction/direct_effects.csv")
    assert not effects.study_id.astype(str).str.contains("JADERA",case=False).any()
