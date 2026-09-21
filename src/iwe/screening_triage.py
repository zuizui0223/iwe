from __future__ import annotations

from dataclasses import dataclass
import re

import pandas as pd


@dataclass(frozen=True)
class SourceTypeTriage:
    bucket: str
    next_action: str


def classify_source_type(record_type: object) -> SourceTypeTriage:
    """Classify source form for screening workflow only.

    This does not make a final IWE screening decision. It routes an unscreened
    record to the next source-eligibility action under docs/SOURCE_ELIGIBILITY.md.
    """
    text = str(record_type or "").strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", text).strip()

    if any(term in normalized for term in ["review", "meta analysis", "systematic review"]):
        return SourceTypeTriage(
            "review_or_synthesis",
            "screen_as_citation_source_not_independent_empirical_effect",
        )
    if any(term in normalized for term in ["dataset", "data set", "repository"]):
        return SourceTypeTriage(
            "dataset_or_repository",
            "identify_corresponding_formally_published_research_article",
        )
    if "preprint" in normalized:
        return SourceTypeTriage(
            "preprint",
            "identify_peer_reviewed_or_formally_published_version",
        )
    if any(term in normalized for term in ["dissertation", "thesis"]):
        return SourceTypeTriage(
            "thesis_or_dissertation",
            "identify_corresponding_eligible_published_article",
        )
    if any(term in normalized for term in ["conference", "abstract", "poster"]):
        return SourceTypeTriage(
            "conference_or_abstract",
            "identify_corresponding_eligible_published_article",
        )
    if any(term in normalized for term in ["editorial", "comment", "letter", "correction", "erratum"]):
        return SourceTypeTriage(
            "editorial_or_companion",
            "verify_whether_record_is_companion_to_an_empirical_article",
        )
    if any(term in normalized for term in ["journal article", "article", "research article", "proceedings"]):
        return SourceTypeTriage(
            "published_research_candidate",
            "manual_biological_estimand_screen",
        )
    if not normalized:
        return SourceTypeTriage(
            "unknown_source_type",
            "resolve_source_type_before_biological_screen",
        )
    return SourceTypeTriage(
        "other_source_type",
        "manual_source_type_and_biological_screen",
    )


def build_source_type_audit(ledger: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {
        "record_key",
        "record_type",
        "families",
        "screening_priority",
        "screening_decision",
    }
    missing = required - set(ledger.columns)
    if missing:
        raise ValueError(f"missing ledger columns: {sorted(missing)}")

    unscreened = ledger.loc[
        ledger["screening_priority"].isin(["P1", "P2", "P3"])
        & ledger["screening_decision"].fillna("").astype(str).str.strip().eq("")
    ].copy()

    triage = [classify_source_type(v) for v in unscreened["record_type"]]
    unscreened["source_type_bucket"] = [x.bucket for x in triage]
    unscreened["source_type_next_action"] = [x.next_action for x in triage]

    exploded = unscreened.assign(
        interaction_family=unscreened["families"].fillna("").astype(str).str.split(";")
    ).explode("interaction_family")
    exploded["interaction_family"] = exploded["interaction_family"].fillna("").str.strip()
    exploded = exploded.loc[exploded["interaction_family"] != ""].copy()

    summary = (
        exploded.groupby(
            ["screening_priority", "interaction_family", "source_type_bucket"],
            dropna=False,
        )
        .agg(
            n_records=("record_key", "nunique"),
            n_unique_record_types=("record_type", "nunique"),
        )
        .reset_index()
        .sort_values(
            ["screening_priority", "interaction_family", "n_records", "source_type_bucket"],
            ascending=[True, True, False, True],
        )
        .reset_index(drop=True)
    )

    queue = unscreened[
        [
            "record_key",
            "doi",
            "title",
            "publication_year",
            "record_type",
            "families",
            "screening_priority",
            "title_priority_score",
            "priority_reasons",
            "source_type_bucket",
            "source_type_next_action",
        ]
    ].copy()
    priority_order = {"P1": 0, "P2": 1, "P3": 2}
    bucket_order = {
        "published_research_candidate": 0,
        "unknown_source_type": 1,
        "other_source_type": 2,
        "dataset_or_repository": 3,
        "preprint": 4,
        "thesis_or_dissertation": 5,
        "conference_or_abstract": 6,
        "editorial_or_companion": 7,
        "review_or_synthesis": 8,
    }
    queue["_priority_order"] = queue["screening_priority"].map(priority_order)
    queue["_bucket_order"] = queue["source_type_bucket"].map(bucket_order).fillna(99)
    queue["title_priority_score"] = pd.to_numeric(
        queue["title_priority_score"], errors="coerce"
    ).fillna(0)
    queue = (
        queue.sort_values(
            ["_priority_order", "_bucket_order", "title_priority_score", "publication_year", "title"],
            ascending=[True, True, False, False, True],
        )
        .drop(columns=["_priority_order", "_bucket_order"])
        .reset_index(drop=True)
    )
    return summary, queue
