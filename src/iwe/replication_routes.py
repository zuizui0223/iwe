from __future__ import annotations

import pandas as pd


ALLOWED_SOURCE_ACCESS = {
    "public_source_insufficient",
    "longform_not_public",
    "repository_inactive",
    "thesis_public_insufficient",
    "programme_models_unlinked",
}
ALLOWED_PUBLIC_SEARCH_STATUS = {"active", "exhausted", "monitor_only"}
ALLOWED_UNLOCK_TYPES = {
    "final_surface",
    "timing_linkage",
    "correct_unit_variance",
    "fate_level_raw_data",
    "same_unit_raw_data",
}
ALLOWED_NEXT_ACTION_TYPES = {
    "retrieve_longform",
    "contact_or_archive",
    "monitor_repository",
    "search_same_programme_data",
}
ELIGIBLE_CANDIDATE_STATUSES = {
    "blocked_summary_stats",
    "blocked_effect_form",
    "blocked_final_surface",
    "blocked_timing_linkage",
}


def validate_replication_completion_routes(
    routes: pd.DataFrame, candidates: pd.DataFrame
) -> list[str]:
    required = {
        "candidate_id",
        "target_class",
        "route_rank",
        "source_access",
        "public_search_status",
        "unlock_type",
        "unlock_requirement",
        "next_action_type",
        "next_action",
        "stop_rule",
        "last_audited",
    }
    missing = sorted(required - set(routes.columns))
    if missing:
        return [f"missing replication-route columns: {', '.join(missing)}"]

    errors: list[str] = []
    if routes["candidate_id"].duplicated().any():
        errors.append("duplicate completion-route candidate_id detected")

    candidate_required = {"candidate_id", "target_class", "status", "priority"}
    candidate_missing = sorted(candidate_required - set(candidates.columns))
    if candidate_missing:
        errors.append(
            f"candidate ledger missing route-validation columns: {', '.join(candidate_missing)}"
        )
        return errors

    unknown_access = sorted(set(routes["source_access"].dropna()) - ALLOWED_SOURCE_ACCESS)
    if unknown_access:
        errors.append(f"unknown source_access values: {unknown_access}")
    unknown_search = sorted(
        set(routes["public_search_status"].dropna()) - ALLOWED_PUBLIC_SEARCH_STATUS
    )
    if unknown_search:
        errors.append(f"unknown public_search_status values: {unknown_search}")
    unknown_unlock = sorted(set(routes["unlock_type"].dropna()) - ALLOWED_UNLOCK_TYPES)
    if unknown_unlock:
        errors.append(f"unknown unlock_type values: {unknown_unlock}")
    unknown_action = sorted(
        set(routes["next_action_type"].dropna()) - ALLOWED_NEXT_ACTION_TYPES
    )
    if unknown_action:
        errors.append(f"unknown next_action_type values: {unknown_action}")

    lookup = candidates.set_index("candidate_id", drop=False)
    for idx, row in routes.iterrows():
        cid = str(row["candidate_id"])
        if cid not in lookup.index:
            errors.append(f"row {idx} candidate_id={cid}: candidate not found in ledger")
            continue

        cand = lookup.loc[cid]
        if isinstance(cand, pd.DataFrame):
            errors.append(f"row {idx} candidate_id={cid}: candidate ledger is not unique")
            continue

        if str(row["target_class"]) != str(cand["target_class"]):
            errors.append(
                f"row {idx} candidate_id={cid}: target_class disagrees with candidate ledger"
            )
        if str(cand["status"]) not in ELIGIBLE_CANDIDATE_STATUSES:
            errors.append(
                f"row {idx} candidate_id={cid}: completion route points to non-blocked status {cand['status']}"
            )
        if str(cand["priority"]) not in {"P1", "P2"}:
            errors.append(
                f"row {idx} candidate_id={cid}: completion route requires P1/P2 candidate, got {cand['priority']}"
            )

        try:
            rank = int(row["route_rank"])
        except (TypeError, ValueError):
            errors.append(f"row {idx} candidate_id={cid}: route_rank must be an integer")
        else:
            if rank < 1:
                errors.append(f"row {idx} candidate_id={cid}: route_rank must be >= 1")

        for field in ("unlock_requirement", "next_action", "stop_rule", "last_audited"):
            if pd.isna(row[field]) or not str(row[field]).strip():
                errors.append(f"row {idx} candidate_id={cid}: {field} must be non-empty")

        if (
            str(row["source_access"]) == "repository_inactive"
            and str(row["public_search_status"]) != "monitor_only"
        ):
            errors.append(
                f"row {idx} candidate_id={cid}: inactive repository must use monitor_only public search status"
            )

    for target_class, group in routes.groupby("target_class"):
        ranks: list[int] = []
        for value in group["route_rank"]:
            try:
                ranks.append(int(value))
            except (TypeError, ValueError):
                pass
        expected = list(range(1, len(group) + 1))
        if sorted(ranks) != expected:
            errors.append(
                f"target_class={target_class}: route_rank must be contiguous 1..{len(group)}"
            )

    return errors


def active_completion_routes(
    routes: pd.DataFrame, candidates: pd.DataFrame
) -> pd.DataFrame:
    errors = validate_replication_completion_routes(routes, candidates)
    if errors:
        raise ValueError("; ".join(errors))
    return routes.sort_values(["target_class", "route_rank"]).reset_index(drop=True)
