import pandas as pd

from iwe.screening_triage import build_source_type_audit, classify_source_type


def test_source_type_classifier_routes_without_final_decisions():
    assert classify_source_type("Journal Article").bucket == "published_research_candidate"
    assert classify_source_type("article").bucket == "published_research_candidate"
    assert classify_source_type("dataset").bucket == "dataset_or_repository"
    assert classify_source_type("preprint").bucket == "preprint"
    assert classify_source_type("PhD dissertation").bucket == "thesis_or_dissertation"
    assert classify_source_type("Review").bucket == "review_or_synthesis"


def test_source_type_audit_uses_only_unscreened_priority_rows():
    ledger = pd.DataFrame(
        [
            {
                "record_key": "a",
                "doi": "10/a",
                "title": "A",
                "publication_year": 2020,
                "record_type": "Journal Article",
                "families": "mutualist",
                "screening_priority": "P2",
                "title_priority_score": 6,
                "priority_reasons": "x",
                "screening_decision": "",
            },
            {
                "record_key": "b",
                "doi": "10/b",
                "title": "B",
                "publication_year": 2021,
                "record_type": "dataset",
                "families": "mutualist;antagonist",
                "screening_priority": "P3",
                "title_priority_score": 2,
                "priority_reasons": "",
                "screening_decision": "",
            },
            {
                "record_key": "c",
                "doi": "10/c",
                "title": "C",
                "publication_year": 2022,
                "record_type": "Journal Article",
                "families": "mutualist",
                "screening_priority": "screened_decision",
                "title_priority_score": 6,
                "priority_reasons": "x",
                "screening_decision": "context_only",
            },
        ]
    )

    summary, queue = build_source_type_audit(ledger)

    assert set(queue["record_key"]) == {"a", "b"}
    assert queue.loc[queue["record_key"] == "a", "source_type_bucket"].iloc[0] == "published_research_candidate"
    assert queue.loc[queue["record_key"] == "b", "source_type_bucket"].iloc[0] == "dataset_or_repository"

    b_rows = summary.loc[
        (summary["screening_priority"] == "P3")
        & (summary["source_type_bucket"] == "dataset_or_repository")
    ]
    assert set(b_rows["interaction_family"]) == {"mutualist", "antagonist"}
    assert set(b_rows["n_records"]) == {1}
