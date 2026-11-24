from __future__ import annotations

from collections import Counter

import pandas as pd

from .schema import INTERACTION_TYPES


SCREENING_STATES = {"registered", "candidate", "blocked", "ineligible"}
REASON_CODES = {
    "registered_propagation",
    "needs_source_audit",
    "dependence_unresolved",
    "timing_to_final_linkage",
    "no_final_fitness",
    "no_isolated_timing_signal",
    "wrong_biological_surface",
    "model_derived_final",
    "synthesis_not_single_chain",
}
PRIORITIES = {"REGISTERED", "P1", "P2", "DROP"}

REQUIRED_COLUMNS = [
    "study_id",
    "interaction_type",
    "screening_state",
    "reason_code",
    "priority",
    "candidate_chain",
    "notes",
]


def validate_propagation_screening(
    screening: pd.DataFrame,
    studies: pd.DataFrame | None = None,
) -> list[str]:
    errors: list[str] = []
    missing = [c for c in REQUIRED_COLUMNS if c not in screening.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    if screening["study_id"].duplicated().any():
        dup = sorted(
            screening.loc[screening["study_id"].duplicated(), "study_id"].astype(str)
        )
        errors.append(f"duplicate study_id values: {', '.join(dup)}")

    checks = {
        "interaction_type": INTERACTION_TYPES,
        "screening_state": SCREENING_STATES,
        "reason_code": REASON_CODES,
        "priority": PRIORITIES,
    }
    for column, allowed in checks.items():
        invalid = sorted(set(screening[column].dropna().astype(str)) - allowed)
        if invalid:
            errors.append(f"{column}: invalid values: {', '.join(invalid)}")

    for column in ("study_id", "candidate_chain", "notes"):
        if screening[column].fillna("").astype(str).str.strip().eq("").any():
            errors.append(f"{column} must be non-blank")

    registered = screening["screening_state"].eq("registered")
    if screening.loc[registered, "reason_code"].ne("registered_propagation").any():
        errors.append("registered rows must use registered_propagation")
    if screening.loc[registered, "priority"].ne("REGISTERED").any():
        errors.append("registered rows must use REGISTERED priority")

    ineligible = screening["screening_state"].eq("ineligible")
    if screening.loc[ineligible, "priority"].ne("DROP").any():
        errors.append("ineligible rows must use DROP priority")

    if studies is not None:
        study_ids = set(studies["study_id"].astype(str))
        screening_ids = set(screening["study_id"].astype(str))
        missing_from_screen = sorted(study_ids - screening_ids)
        extra = sorted(screening_ids - study_ids)
        if missing_from_screen:
            errors.append(
                "registered studies missing from propagation screen: "
                + ", ".join(missing_from_screen)
            )
        if extra:
            errors.append(
                "propagation screen contains unknown studies: " + ", ".join(extra)
            )

        if "interaction_type_candidate" in studies.columns:
            expected = studies.set_index("study_id")["interaction_type_candidate"].astype(str)
            observed = screening.set_index("study_id")["interaction_type"].astype(str)
            common = sorted(set(expected.index) & set(observed.index))
            bad = [sid for sid in common if expected.loc[sid] != observed.loc[sid]]
            if bad:
                errors.append(
                    "interaction type differs from study registry: " + ", ".join(bad)
                )

    return errors


def propagation_screening_summary(screening: pd.DataFrame) -> dict[str, object]:
    errors = validate_propagation_screening(screening)
    if errors:
        raise ValueError("; ".join(errors))

    return {
        "n_studies": int(len(screening)),
        "by_state": dict(Counter(screening["screening_state"])),
        "by_reason": dict(Counter(screening["reason_code"])),
        "by_interaction": dict(Counter(screening["interaction_type"])),
        "candidates_by_interaction": dict(
            Counter(
                screening.loc[
                    screening["screening_state"].eq("candidate"),
                    "interaction_type",
                ]
            )
        ),
        "p1_candidates": sorted(
            screening.loc[
                screening["screening_state"].eq("candidate")
                & screening["priority"].eq("P1"),
                "study_id",
            ].astype(str)
        ),
        "blocked": sorted(
            screening.loc[
                screening["screening_state"].eq("blocked"),
                "study_id",
            ].astype(str)
        ),
    }


def render_propagation_screening(screening: pd.DataFrame) -> str:
    s = propagation_screening_summary(screening)

    def rows(mapping: dict[str, int]) -> list[str]:
        return [f"| {key} | {value} |" for key, value in sorted(mapping.items())]

    lines = [
        "# IWE propagation-screening coverage",
        "",
        "_Generated from data/registry/temporal_propagation_screening.csv; do not edit counts by hand._",
        "",
        "## Frozen base corpus",
        "",
        f"- Registered IWE publications screened: **{s['n_studies']}**",
        "",
        "| Propagation-screen state | Studies |",
        "|---|---:|",
        *rows(s["by_state"]),
        "",
        "The propagation ledger is therefore not an open-ended collection of illustrative examples. Every publication in the original 32-study IWE registry has an explicit propagation-screen state.",
        "",
        "## Reason codes",
        "",
        "| Reason | Studies |",
        "|---|---:|",
        *rows(s["by_reason"]),
        "",
        "## Interaction classes in the frozen corpus",
        "",
        "| Interaction type | Studies |",
        "|---|---:|",
        *rows(s["by_interaction"]),
        "",
        "## Unadjudicated candidates",
        "",
        "| Interaction type | Candidate studies |",
        "|---|---:|",
        *rows(s["candidates_by_interaction"]),
        "",
        "P1 source-audit queue: **" + ", ".join(s["p1_candidates"]) + "**.",
        "",
        "Blocked source/linkage queue: **" + ", ".join(s["blocked"]) + "**.",
        "",
        "## Interpretation",
        "",
        "The current temporal-signal ledger remains exploratory until the candidate rows above are adjudicated or source-closed. This screen prevents candidate selection from being driven only by whether a study produces an interesting transformation state.",
        "",
        "Registered does not mean preserved; it only means that a source-backed propagation state has already been assigned. Candidate studies must be adjudicated under the same transformation contract, including null, erased and buffered outcomes.",
        "",
    ]
    return "\n".join(lines)
