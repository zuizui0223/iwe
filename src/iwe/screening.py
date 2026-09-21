from __future__ import annotations

import pandas as pd


SCREENING_STATUSES = ("include", "unresolved", "context_only", "exclude")
INTERACTION_LABELS = {
    "mutualist": "mutualist",
    "antagonist": "antagonist",
    "mixed_pollinating_seed_predator": "mixed pollinating seed predator",
}


def validate_study_registry(df: pd.DataFrame) -> list[str]:
    required = {
        "study_id",
        "source_id",
        "title",
        "system_id",
        "screening_status",
        "screening_reason",
        "interaction_type_candidate",
        "notes",
    }
    errors: list[str] = []
    missing = sorted(required - set(df.columns))
    if missing:
        return [f"missing study-registry columns: {', '.join(missing)}"]
    if df["study_id"].duplicated().any():
        errors.append("duplicate study_id detected")
    unknown_status = sorted(set(df["screening_status"].dropna()) - set(SCREENING_STATUSES))
    if unknown_status:
        errors.append(f"unknown screening_status: {unknown_status}")
    unknown_class = sorted(set(df["interaction_type_candidate"].dropna()) - set(INTERACTION_LABELS))
    if unknown_class:
        errors.append(f"unknown interaction_type_candidate: {unknown_class}")
    return errors


def screening_count_table(df: pd.DataFrame) -> pd.DataFrame:
    errors = validate_study_registry(df)
    if errors:
        raise ValueError("; ".join(errors))

    rows: list[dict[str, object]] = []
    for interaction_type in INTERACTION_LABELS:
        part = df.loc[df["interaction_type_candidate"] == interaction_type]
        row: dict[str, object] = {
            "candidate_class": INTERACTION_LABELS[interaction_type],
        }
        for status in SCREENING_STATUSES:
            row[status] = int((part["screening_status"] == status).sum())
        row["total"] = int(len(part))
        rows.append(row)

    total: dict[str, object] = {"candidate_class": "Total"}
    for status in SCREENING_STATUSES:
        total[status] = int((df["screening_status"] == status).sum())
    total["total"] = int(len(df))
    rows.append(total)
    return pd.DataFrame(rows)


def render_screening_snapshot(df: pd.DataFrame) -> str:
    counts = screening_count_table(df)
    total = counts.iloc[-1]

    lines = [
        "<!-- BEGIN GENERATED SCREENING SNAPSHOT -->",
        "_Generated from `data/registry/studies.csv`; do not edit this block by hand._",
        "",
        f"**Registered publications: {int(total['total'])}.** "
        f"Current decisions: {int(total['include'])} include, "
        f"{int(total['unresolved'])} unresolved, "
        f"{int(total['context_only'])} context only, "
        f"{int(total['exclude'])} exclude.",
        "",
        "| Candidate class | Include | Unresolved | Context only | Exclude | Total |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for _, row in counts.iterrows():
        label = str(row["candidate_class"])
        if label == "Total":
            label = "**Total**"
            vals = [f"**{int(row[s])}**" for s in ("include", "unresolved", "context_only", "exclude", "total")]
        else:
            vals = [str(int(row[s])) for s in ("include", "unresolved", "context_only", "exclude", "total")]
        lines.append(f"| {label} | " + " | ".join(vals) + " |")

    lines.extend(
        [
            "",
            "### Registry snapshot",
            "",
            "| Study | Candidate class | Status | Source | Title |",
            "|---|---|---|---|---|",
        ]
    )

    ordered = df.sort_values("study_id")
    for _, row in ordered.iterrows():
        title = str(row["title"]).replace("|", "\\|")
        source = str(row["source_id"]).replace("|", "\\|")
        klass = INTERACTION_LABELS[str(row["interaction_type_candidate"])]
        lines.append(
            f"| `{row['study_id']}` | {klass} | `{row['screening_status']}` | "
            f"`{source}` | {title} |"
        )

    lines.append("<!-- END GENERATED SCREENING SNAPSHOT -->")
    return "\n".join(lines)


def replace_screening_snapshot(document: str, snapshot: str) -> str:
    start = "<!-- BEGIN GENERATED SCREENING SNAPSHOT -->"
    end = "<!-- END GENERATED SCREENING SNAPSHOT -->"
    if start not in document or end not in document:
        raise ValueError("screening document is missing generated snapshot markers")
    before, rest = document.split(start, 1)
    _, after = rest.split(end, 1)
    return before.rstrip() + "\n\n" + snapshot + "\n\n" + after.lstrip()
