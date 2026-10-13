"""Archive record locator leads are not synthetic mixed H1 observations."""
from pathlib import Path

import pandas as pd

from iwe.replication_routes import validate_replication_completion_routes

QUEUE = "data/source_reconstructions/hurlburt2004_archival_record_locator_queue.csv"


def test_public_archive_leads_are_not_original_matching_final_seed_data():
    a = pd.read_csv(QUEUE).set_index("route_id")
    assert set(a.index) == {
        "HUR_ARCH_2004", "HUR_ARCH_2005", "HUR_ARCH_2007",
        "HUR_ARCH_2011", "HUR_ARCH_UALBERTA_DATA",
        "HUR_ARCH_AAFC_RECORDS"
    }
    assert a["candidate_id"].eq("MIX002_HURLBURT_2004").all()
    assert a["original_marked_flower_event_rows_verified"].eq("no").all()
    assert a["adult_census_dates_verified"].eq("no").all()
    assert a["same_unit_postlarval_viable_seeds_verified"].eq("no").all()
    assert a["strict_h1_admitted"].eq("no").all()
    assert a.loc["HUR_ARCH_2004", "document_status"] == (
        "original_pdf_recovered_and_read"
    )


def test_later_reports_do_not_fill_original_1999_to_2002_seed_link():
    a = pd.read_csv(QUEUE).set_index("route_id")
    assert a.loc["HUR_ARCH_2005", "target_years"] == "2005"
    assert a.loc["HUR_ARCH_2007", "target_years"] == "2007"
    assert a.loc["HUR_ARCH_2011", "target_years"] == "2011"
    assert set(a.loc[["HUR_ARCH_2005", "HUR_ARCH_2007", "HUR_ARCH_2011"],
                     "document_status"]) == {
                         "citation_only_public_fulltext_not_recovered"
                     }


def test_hurlburt_route_remains_blocked_after_archival_discovery():
    routes = pd.read_csv("data/registry/replication_completion_routes.csv")
    candidates = pd.read_csv("data/registry/replication_candidates.csv")
    assert validate_replication_completion_routes(routes, candidates) == []
    row = routes.set_index("candidate_id").loc["MIX002_HURLBURT_2004"]
    assert row["source_access"] == "thesis_public_insufficient"
    assert row["unlock_type"] == "timing_linkage"
    assert row["next_action_type"] == "contact_or_archive"
    assert "no author contact" in row["next_action"]
    assert "CODEBOOK/CUSTODIAN LEADS ONLY" in row["next_action"]
    assert row["last_audited"] == "2026-10-09"
    assert Path(
        "docs/HURLBURT2004_NO_CONTACT_ARCHIVE_ROUTE_20261009.md"
    ).exists()
