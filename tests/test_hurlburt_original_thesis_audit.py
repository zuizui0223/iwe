"""Original-thesis published runs tests are context, not strict effect sizes."""
import pandas as pd

from iwe.replication_routes import validate_replication_completion_routes

SOURCE = "data/source_reconstructions/hurlburt2004_original_thesis_table3_10_runs.csv"


def test_original_hurlburt_table3_10_exact_published_site_year_design():
    x = pd.read_csv(SOURCE)
    assert len(x) == 9
    assert x.groupby("site").size().to_dict() == {
        "Onefour": 4, "Loma": 3, "Fort_Benton": 2
    }
    assert set(x.physical_pdf_page) == {127}
    assert set(x.source_table) == {"Table_3_10"}
    assert set(x.source_doi) == {"10.7939/r3-fe1d-kj80"}
    assert (x.flowering_vs_fruiting_p > .05).all()
    assert (x.visitation_vs_fruiting_p > .05).all()
    assert (x.strict_h1_effect == "no").all()
    assert (x.year_site_independent_timing_to_final_seed_effect == "no").all()
    p = x.set_index(["site", "year"])
    assert [p.loc[("Onefour", i), "flowering_vs_fruiting_p"]
            for i in range(1999, 2003)] == [.244, .579, .598, .216]
    assert p.loc[("Loma", 2000), "visitation_vs_fruiting_p"] == .171


def test_public_original_thesis_no_longer_claimed_undownloadable():
    routes = pd.read_csv("data/registry/replication_completion_routes.csv")
    candidates = pd.read_csv("data/registry/replication_candidates.csv")
    assert validate_replication_completion_routes(routes, candidates) == []
    r = routes.set_index("candidate_id").loc["MIX002_HURLBURT_2004"]
    assert r.source_access == "thesis_public_insufficient"
    assert r.public_search_status == "exhausted"
    assert r.next_action_type == "contact_or_archive"
    assert "no author contact" in r.next_action.lower()
    assert "post-larval" in r.unlock_requirement
    assert r.last_audited == "2026-10-08"
