from __future__ import annotations

from collections import Counter

import pandas as pd


ALLOWED_SOURCES = {
    "web_of_science",
    "scopus",
    "proquest_dissertations",
    "openalex",
    "citation_snowball",
}
ALLOWED_REQUIREMENTS = {"required", "supplementary"}
ALLOWED_STATUSES = {"planned", "completed", "blocked_access"}
ALLOWED_DEDUP = {"pending", "complete", "not_applicable"}


def validate_search_runs(df: pd.DataFrame) -> list[str]:
    required = {
        "run_id",
        "source",
        "query_family",
        "coverage_requirement",
        "source_query",
        "status",
        "run_date",
        "result_count",
        "export_path",
        "dedup_status",
        "notes",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        return [f"missing search-run columns: {', '.join(missing)}"]

    errors: list[str] = []
    if df["run_id"].duplicated().any():
        errors.append("duplicate search run_id detected")

    checks = [
        ("source", ALLOWED_SOURCES),
        ("coverage_requirement", ALLOWED_REQUIREMENTS),
        ("status", ALLOWED_STATUSES),
        ("dedup_status", ALLOWED_DEDUP),
    ]
    for column, allowed in checks:
        unknown = sorted(set(df[column].dropna().astype(str)) - allowed)
        if unknown:
            errors.append(f"unknown {column}: {unknown}")

    for idx, row in df.iterrows():
        prefix = f"search row {idx} run_id={row['run_id']}"
        for field in ("run_id", "source", "query_family", "coverage_requirement", "source_query"):
            if pd.isna(row[field]) or not str(row[field]).strip():
                errors.append(f"{prefix}: {field} must be non-empty")

        status = str(row["status"])
        dedup = str(row["dedup_status"])
        if status == "completed":
            if pd.isna(row["run_date"]) or not str(row["run_date"]).strip():
                errors.append(f"{prefix}: completed run requires run_date")
            try:
                count = int(row["result_count"])
            except (TypeError, ValueError):
                errors.append(f"{prefix}: completed run requires integer result_count")
            else:
                if count < 0:
                    errors.append(f"{prefix}: result_count must be >= 0")
            if pd.isna(row["export_path"]) or not str(row["export_path"]).strip():
                errors.append(f"{prefix}: completed run requires export_path")
            if dedup != "complete":
                errors.append(f"{prefix}: completed run requires dedup_status=complete")
        else:
            if dedup == "complete":
                errors.append(
                    f"{prefix}: non-completed run cannot claim dedup_status=complete"
                )
    return errors


def search_coverage_status(df: pd.DataFrame) -> dict[str, object]:
    errors = validate_search_runs(df)
    if errors:
        raise ValueError("; ".join(errors))

    required = df.loc[df["coverage_requirement"] == "required"].copy()
    complete_mask = (
        (required["status"] == "completed")
        & (required["dedup_status"] == "complete")
    )
    complete_required = int(complete_mask.sum())
    required_total = int(len(required))

    return {
        "total_runs": int(len(df)),
        "required_runs": required_total,
        "supplementary_runs": int(
            (df["coverage_requirement"] == "supplementary").sum()
        ),
        "required_completed": complete_required,
        "required_remaining": required_total - complete_required,
        "status_counts": dict(Counter(df["status"].astype(str))),
        "source_counts": dict(Counter(df["source"].astype(str))),
        "systematic_claim_status": (
            "systematic_ready"
            if required_total > 0 and complete_required == required_total
            else "targeted_only"
        ),
    }


def render_search_coverage_status(df: pd.DataFrame) -> str:
    status = search_coverage_status(df)
    lines = [
        "# IWE search coverage status",
        "",
        "_Generated from data/registry/search_runs.csv; do not edit counts by hand._",
        "",
        f"**Systematic-claim status: {status['systematic_claim_status']}.**",
        "",
        f"Planned/registered search runs: {status['total_runs']} total, "
        f"{status['required_runs']} required and {status['supplementary_runs']} supplementary.",
        f"Required runs complete and deduplicated: {status['required_completed']} / "
        f"{status['required_runs']} ({status['required_remaining']} remaining).",
        "",
        "Until every required run is complete and deduplicated, IWE may describe the "
        "current evidence set only as a targeted corpus. It must not report registry "
        "fractions as prevalence estimates for the entire literature or call the search exhaustive.",
        "",
        "| Run | Source | Query family | Requirement | Status | Dedup | Results |",
        "|---|---|---|---|---|---|---:|",
    ]
    for _, row in df.sort_values("run_id").iterrows():
        result_count = (
            ""
            if pd.isna(row["result_count"]) or str(row["result_count"]).strip() == ""
            else str(row["result_count"])
        )
        lines.append(
            f"| {row['run_id']} | {row['source']} | {row['query_family']} | "
            f"{row['coverage_requirement']} | {row['status']} | "
            f"{row['dedup_status']} | {result_count} |"
        )

    lines.extend(
        [
            "",
            "## Readiness rule",
            "",
            "A required search run is complete only when its exact source query, run date, "
            "result count, exported record file, and post-export deduplication are all recorded. "
            "Citation snowballing is a required run rather than an informal afterthought.",
            "",
            "OpenAlex is retained as supplementary triangulation. It does not replace the "
            "two broad bibliographic indexes or dissertation/grey-literature search in the "
            "required coverage plan.",
            "",
        ]
    )
    return "\n".join(lines)
