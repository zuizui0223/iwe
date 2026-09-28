from __future__ import annotations

from collections import Counter

import pandas as pd

from .replication import (
    MIN_INDEPENDENT_CLUSTERS_PER_CLASS,
    MIN_INFERENTIAL_CLUSTERS_PER_CLASS,
)


CLASS_ORDER = (
    "mutualist",
    "antagonist",
    "mixed_pollinating_seed_predator",
)
CLASS_LABELS = {
    "mutualist": "mutualist",
    "antagonist": "antagonist",
    "mixed_pollinating_seed_predator": "mixed pollinating seed predator",
}
REJECTED_CANDIDATE_STATUSES = {
    "rejected_timing",
    "rejected_dependence",
    "rejected_other",
}


def _counts(values: pd.Series) -> dict[str, int]:
    return dict(Counter(str(value) for value in values.dropna()))


def evidence_audit_summary(
    studies: pd.DataFrame,
    effects: pd.DataFrame,
    adjudications: pd.DataFrame,
    candidates: pd.DataFrame,
    routes: pd.DataFrame,
) -> dict[str, object]:
    """Return registry-derived descriptive evidence-audit counts."""
    strict = effects.loc[
        (effects["evidence_tier"].astype(str) == "A")
        & (effects["timing_analysis_class"].astype(str) == "strict_window")
    ].copy()
    smd = strict.loc[
        strict["effect_family"].astype(str) == "standardized_mean_difference"
    ].copy()

    strict_by_class: dict[str, dict[str, int]] = {}
    smd_by_class: dict[str, dict[str, int]] = {}
    for interaction_type in CLASS_ORDER:
        strict_part = strict.loc[
            strict["interaction_type"].astype(str) == interaction_type
        ]
        smd_part = smd.loc[
            smd["interaction_type"].astype(str) == interaction_type
        ]
        strict_by_class[interaction_type] = {
            "rows": int(len(strict_part)),
            "studies": int(strict_part["study_id"].astype(str).nunique()),
            "clusters": int(strict_part["dependence_id"].astype(str).nunique()),
        }
        smd_by_class[interaction_type] = {
            "rows": int(len(smd_part)),
            "studies": int(smd_part["study_id"].astype(str).nunique()),
            "clusters": int(smd_part["dependence_id"].astype(str).nunique()),
        }

    candidate_status = _counts(candidates["status"])
    rejected = sum(
        candidate_status.get(status, 0) for status in REJECTED_CANDIDATE_STATUSES
    )
    blocked = sum(
        count
        for status, count in candidate_status.items()
        if status.startswith("blocked_")
    )
    ready = candidate_status.get("ready", 0)

    return {
        "registered_publications": int(len(studies)),
        "screening_status": _counts(studies["screening_status"]),
        "publications_by_candidate_class": _counts(
            studies["interaction_type_candidate"]
        ),
        "direct_effect_rows": int(len(effects)),
        "strict_effect_rows": int(len(strict)),
        "strict_studies": int(strict["study_id"].astype(str).nunique()),
        "strict_clusters": int(strict["dependence_id"].astype(str).nunique()),
        "strict_by_class": strict_by_class,
        "strict_effect_families": _counts(strict["effect_family"]),
        "smd_effect_rows": int(len(smd)),
        "smd_by_class": smd_by_class,
        "adjudication_quantitative_status": _counts(
            adjudications["quantitative_status"]
        ),
        "replication_candidates": int(len(candidates)),
        "candidate_status": candidate_status,
        "candidate_rejected": int(rejected),
        "candidate_blocked": int(blocked),
        "candidate_ready": int(ready),
        "completion_routes": int(len(routes)),
        "routes_by_class": _counts(routes["target_class"]),
        "routes_by_public_search_status": _counts(routes["public_search_status"]),
        "routes_by_source_access": _counts(routes["source_access"]),
        "routes_by_next_action": _counts(routes["next_action_type"]),
        "replication_milestone_clusters": MIN_INDEPENDENT_CLUSTERS_PER_CLASS,
        "reference_inferential_clusters": MIN_INFERENTIAL_CLUSTERS_PER_CLASS,
    }


def _pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{100.0 * numerator / denominator:.1f}%"


def render_evidence_audit_status(
    studies: pd.DataFrame,
    effects: pd.DataFrame,
    adjudications: pd.DataFrame,
    candidates: pd.DataFrame,
    routes: pd.DataFrame,
) -> str:
    """Render the current registry-derived evidence-audit status as Markdown."""
    s = evidence_audit_summary(studies, effects, adjudications, candidates, routes)
    screening = s["screening_status"]
    candidate_status = s["candidate_status"]
    route_search = s["routes_by_public_search_status"]
    route_actions = s["routes_by_next_action"]
    strict_families = s["strict_effect_families"]

    lines = [
        "# IWE evidence audit status",
        "",
        "_Generated from the study, effect, adjudication, replication-candidate, and completion-route registries. Do not edit counts by hand._",
        "",
        "## 1. Publication screening",
        "",
        f"**{s['registered_publications']} registered publications** are currently tracked: "
        f"{screening.get('include', 0)} include, "
        f"{screening.get('unresolved', 0)} unresolved, and "
        f"{screening.get('context_only', 0)} context-only.",
        "",
        "| Candidate class | Registered publications |",
        "|---|---:|",
    ]
    for interaction_type in CLASS_ORDER:
        lines.append(
            f"| {CLASS_LABELS[interaction_type]} | "
            f"{s['publications_by_candidate_class'].get(interaction_type, 0)} |"
        )

    lines.extend(
        [
            "",
            "## 2. Strict-H1 quantitative corpus",
            "",
            f"The extraction registry contains **{s['direct_effect_rows']} quantitative rows**, "
            f"of which **{s['strict_effect_rows']} rows from {s['strict_studies']} studies "
            f"and {s['strict_clusters']} dependence clusters** currently satisfy the "
            "strict Tier-A synchrony gate.",
            "",
            "| Interaction class | Strict rows | Strict studies | Dependence clusters | SMD rows | SMD clusters |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for interaction_type in CLASS_ORDER:
        strict = s["strict_by_class"][interaction_type]
        smd = s["smd_by_class"][interaction_type]
        lines.append(
            f"| {CLASS_LABELS[interaction_type]} | {strict['rows']} | "
            f"{strict['studies']} | {strict['clusters']} | {smd['rows']} | "
            f"{smd['clusters']} |"
        )

    family_text = ", ".join(
        f"{family} = {count}"
        for family, count in sorted(strict_families.items())
    )
    lines.extend(
        [
            "",
            f"Strict rows currently use two native effect families: {family_text}.",
            "",
            "For the common standardized_mean_difference family, independent "
            f"cluster counts are **{s['smd_by_class']['mutualist']['clusters']} mutualist / "
            f"{s['smd_by_class']['antagonist']['clusters']} antagonist / "
            f"{s['smd_by_class']['mixed_pollinating_seed_predator']['clusters']} mixed**.",
            f"The **{s['replication_milestone_clusters']}-cluster threshold is a discovery milestone only**; "
            f"the current reference workflow requires at least "
            f"{s['reference_inferential_clusters']} dependence clusters per class "
            "before robust class-level inference is considered evaluable.",
            "",
            "**Current consequence:** no native effect family has adequate independent "
            "replication across all three interaction classes, so H1 is not currently evaluable.",
            "",
            "## 3. Replication-candidate audit",
            "",
            f"The replication ledger contains **{s['replication_candidates']} candidate programmes/leads**. "
            "This is a discovery/completion ledger, not a count of unique screened publications.",
            "",
            f"- **{s['candidate_rejected']} ({_pct(s['candidate_rejected'], s['replication_candidates'])})** are rejected under the frozen contracts.",
            f"- **{s['candidate_blocked']} ({_pct(s['candidate_blocked'], s['replication_candidates'])})** remain biologically relevant but blocked by a specific missing timing/outcome/variance/source object.",
            f"- **{s['candidate_ready']} ({_pct(s['candidate_ready'], s['replication_candidates'])})** are ready.",
            "",
            "| Candidate status | Count |",
            "|---|---:|",
        ]
    )
    for status, count in sorted(
        candidate_status.items(), key=lambda item: (-item[1], item[0])
    ):
        lines.append(f"| {status} | {count} |")

    lines.extend(
        [
            "",
            "The dominant rejection is the **timing contract**: "
            f"{candidate_status.get('rejected_timing', 0)} of "
            f"{s['replication_candidates']} candidate leads "
            f"({_pct(candidate_status.get('rejected_timing', 0), s['replication_candidates'])}) "
            "fail because partner activity is absent, imported from another season/study, "
            "or inferred from realized attack/egg receipt rather than measured independently.",
            "",
            "## 4. Completion-route audit",
            "",
            f"There are **{s['completion_routes']} unresolved completion routes**: "
            f"{s['routes_by_class'].get('mixed_pollinating_seed_predator', 0)} mixed-system "
            f"and {s['routes_by_class'].get('antagonist', 0)} antagonist routes.",
            f"Public search is marked **exhausted for {route_search.get('exhausted', 0)}** routes "
            f"and **monitor-only for {route_search.get('monitor_only', 0)}**; "
            f"there are **{route_search.get('active', 0)} active generic public-search routes**.",
            "",
            "| Next action | Routes |",
            "|---|---:|",
        ]
    )
    for action, count in sorted(
        route_actions.items(), key=lambda item: (-item[1], item[0])
    ):
        lines.append(f"| {action} | {count} |")

    lines.extend(
        [
            "",
            "This means the remaining gap is no longer well described as simply "
            "\"more literature searching.\" Most unresolved routes require a named "
            "long-form source, public binary asset, archive/raw table, or future repository release.",
            "",
            "## 5. Interpretation boundary",
            "",
            "The audit result is descriptive evidence about the **availability and "
            "compatibility of evidence in the current targeted IWE corpus under the frozen estimand**. "
            "The first-pass search is not yet an exhaustive systematic-review denominator, and these "
            "counts must not be interpreted as prevalence estimates for the entire literature. "
            "The audit is also not a biological estimate that synchrony effects do or do not differ "
            "among interaction classes.",
            "",
            "In particular:",
            "",
            "- absence from the strict corpus does not mean a study is biologically uninformative;",
            "- failure of the strict timing gate often reflects incompatible measurement grain rather than absence of phenological effects;",
            "- repeated rows from one programme do not create independent replication;",
            "- inaccessible or unreleased data contribute zero quantitative evidence until recovered;",
            "- the completion ledger documents exact unlock objects and stop rules so repeated generic searching cannot masquerade as progress.",
            "",
            "## 6. Paper-facing result",
            "",
            "Under a deliberately strict, prospectively defined synchrony estimand, the "
            "current targeted IWE corpus contains many biologically relevant studies but very few "
            "independent, variance-bearing plant-fitness contrasts that jointly preserve "
            "partner timing, post-interaction reproduction, and dependence. The empirical "
            "result at this stage is therefore an **evidence-architecture gap**, not a supported "
            "three-class H1 contrast.",
            "",
        ]
    )
    return "\n".join(lines)
