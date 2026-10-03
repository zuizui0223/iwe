from __future__ import annotations

from collections import Counter

import pandas as pd

from .schema import INTERACTION_TYPES


EVIDENCE_STATES = {"yes", "no", "partial", "blocked"}
PHASE_ALIGNMENT_STATUSES = {
    "near_confirmatory",
    "mechanism_only",
    "boundary_null",
    "final_tracking_evidence",
    "paired_realized_positive",
    "final_landscape_no_alignment",
    "stage_structure",
    "host_sensitivity_final",
    "confirmatory_ready",
}

REQUIRED_COLUMNS = [
    "candidate_id",
    "study_id",
    "interaction_type",
    "dependence_id",
    "raw_or_adult_timing",
    "effective_consumer_timing",
    "prefinal_host_filter",
    "phase_alignment_varies",
    "final_plant_endpoint",
    "paired_simpler_vs_stage_comparison",
    "status",
    "blocker",
    "notes",
]


def validate_phase_alignment_registry(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    if df["candidate_id"].duplicated().any():
        duplicates = sorted(
            df.loc[df["candidate_id"].duplicated(), "candidate_id"].astype(str)
        )
        errors.append(f"duplicate candidate_id values: {', '.join(duplicates)}")

    invalid_interactions = sorted(
        set(df["interaction_type"].dropna().astype(str)) - INTERACTION_TYPES
    )
    if invalid_interactions:
        errors.append(
            "interaction_type: invalid values: " + ", ".join(invalid_interactions)
        )

    evidence_columns = [
        "raw_or_adult_timing",
        "effective_consumer_timing",
        "prefinal_host_filter",
        "phase_alignment_varies",
        "final_plant_endpoint",
        "paired_simpler_vs_stage_comparison",
    ]
    for column in evidence_columns:
        invalid = sorted(set(df[column].dropna().astype(str)) - EVIDENCE_STATES)
        if invalid:
            errors.append(f"{column}: invalid values: {', '.join(invalid)}")

    invalid_status = sorted(
        set(df["status"].dropna().astype(str)) - PHASE_ALIGNMENT_STATUSES
    )
    if invalid_status:
        errors.append("status: invalid values: " + ", ".join(invalid_status))

    for column in ["candidate_id", "study_id", "dependence_id", "blocker", "notes"]:
        if df[column].fillna("").astype(str).str.strip().eq("").any():
            errors.append(f"{column} must be non-blank")

    ready = df["status"].eq("confirmatory_ready")
    bad_ready = df.loc[
        ready
        & (
            df["raw_or_adult_timing"].ne("yes")
            | df["effective_consumer_timing"].ne("yes")
            | df["prefinal_host_filter"].ne("yes")
            | df["phase_alignment_varies"].ne("yes")
            | df["final_plant_endpoint"].ne("yes")
            | df["paired_simpler_vs_stage_comparison"].ne("yes")
        ),
        "candidate_id",
    ].astype(str)
    if len(bad_ready):
        errors.append(
            "confirmatory_ready requires all six evidence states=yes: "
            + ", ".join(sorted(bad_ready))
        )

    boundary = df["status"].eq("boundary_null")
    bad_boundary = df.loc[
        boundary
        & (
            df["phase_alignment_varies"].ne("yes")
            | df["final_plant_endpoint"].ne("yes")
            | df["paired_simpler_vs_stage_comparison"].ne("yes")
        ),
        "candidate_id",
    ].astype(str)
    if len(bad_boundary):
        errors.append(
            "boundary_null requires phase variation, final endpoint, and paired comparison: "
            + ", ".join(sorted(bad_boundary))
        )

    paired_positive = df["status"].eq("paired_realized_positive")
    bad_paired_positive = df.loc[
        paired_positive
        & (
            df["phase_alignment_varies"].ne("yes")
            | df["final_plant_endpoint"].ne("yes")
            | df["paired_simpler_vs_stage_comparison"].ne("yes")
        ),
        "candidate_id",
    ].astype(str)
    if len(bad_paired_positive):
        errors.append(
            "paired_realized_positive requires phase variation, final endpoint, and paired comparison: "
            + ", ".join(sorted(bad_paired_positive))
        )

    host_final = df["status"].eq("host_sensitivity_final")
    bad_host_final = df.loc[
        host_final
        & (
            df["raw_or_adult_timing"].ne("yes")
            | df["prefinal_host_filter"].ne("yes")
            | df["phase_alignment_varies"].ne("yes")
            | df["final_plant_endpoint"].ne("yes")
        ),
        "candidate_id",
    ].astype(str)
    if len(bad_host_final):
        errors.append(
            "host_sensitivity_final requires raw/adult timing, pre-final filter, phase variation, and final endpoint: "
            + ", ".join(sorted(bad_host_final))
        )

    near = df["status"].eq("near_confirmatory")
    bad_near = df.loc[
        near
        & (
            df["phase_alignment_varies"].ne("yes")
            | df["final_plant_endpoint"].ne("yes")
            | ~df["paired_simpler_vs_stage_comparison"].isin({"yes", "blocked"})
        ),
        "candidate_id",
    ].astype(str)
    if len(bad_near):
        errors.append(
            "near_confirmatory requires phase variation, final endpoint, and a paired comparison that is ready or explicitly blocked: "
            + ", ".join(sorted(bad_near))
        )

    return errors


def phase_alignment_summary(df: pd.DataFrame) -> dict[str, object]:
    errors = validate_phase_alignment_registry(df)
    if errors:
        raise ValueError("; ".join(errors))

    return {
        "n_candidates": int(len(df)),
        "n_dependence_clusters": int(df["dependence_id"].nunique()),
        "by_status": dict(Counter(df["status"])),
        "by_interaction_type": dict(Counter(df["interaction_type"])),
        "confirmatory_ready": int(df["status"].eq("confirmatory_ready").sum()),
        "near_confirmatory": int(df["status"].eq("near_confirmatory").sum()),
        "boundary_null": int(df["status"].eq("boundary_null").sum()),
        "paired_realized_positive": int(df["status"].eq("paired_realized_positive").sum()),
        "final_endpoint_yes": int(df["final_plant_endpoint"].eq("yes").sum()),
        "phase_varies_yes": int(df["phase_alignment_varies"].eq("yes").sum()),
        "paired_comparison_yes": int(
            df["paired_simpler_vs_stage_comparison"].eq("yes").sum()
        ),
        "paired_comparison_blocked": int(
            df["paired_simpler_vs_stage_comparison"].eq("blocked").sum()
        ),
    }


def render_phase_alignment_gate(df: pd.DataFrame) -> str:
    summary = phase_alignment_summary(df)

    lines = [
        "# Stage-specific phase-alignment confirmatory gate",
        "",
        "_Generated from data/registry/phase_alignment_candidates.csv; do not edit counts by hand._",
        "",
        "## Current gate",
        "",
        f"- Candidate programmes/components: **{summary['n_candidates']}**",
        f"- Dependence clusters: **{summary['n_dependence_clusters']}**",
        f"- Confirmatory-ready positive or null comparisons: **{summary['confirmatory_ready']}**",
        f"- Near-confirmatory blocked routes: **{summary['near_confirmatory']}**",
        f"- Registered direct null/boundary comparisons: **{summary['boundary_null']}**",
        f"- Positive paired realized comparisons (non-confirmatory): **{summary['paired_realized_positive']}**",
        "",
        "A programme is confirmatory_ready only when it has source-backed raw/adult timing, effective consumer timing, a pre-final host filter, variation in phase alignment, a final plant endpoint, and a paired simpler-vs-stage-specific timing comparison.",
        "",
        "## Evidence coverage",
        "",
        f"- Final plant endpoint present: **{summary['final_endpoint_yes']} / {summary['n_candidates']}**",
        f"- Phase/alignment varies: **{summary['phase_varies_yes']} / {summary['n_candidates']}**",
        f"- Paired simpler-vs-stage comparison available: **{summary['paired_comparison_yes']} / {summary['n_candidates']}**",
        f"- Paired comparison explicitly blocked by one recoverable object: **{summary['paired_comparison_blocked']} / {summary['n_candidates']}**",
        "",
        "## Candidate states",
        "",
        "| Candidate | Interaction | Raw/adult timing | Effective consumer timing | Pre-final filter | Phase varies | Final endpoint | Paired comparison | Status | Blocker |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]

    for _, row in df.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["candidate_id"]),
                    str(row["interaction_type"]),
                    str(row["raw_or_adult_timing"]),
                    str(row["effective_consumer_timing"]),
                    str(row["prefinal_host_filter"]),
                    str(row["phase_alignment_varies"]),
                    str(row["final_plant_endpoint"]),
                    str(row["paired_simpler_vs_stage_comparison"]),
                    str(row["status"]),
                    str(row["blocker"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "There is currently **no positive confirmatory-ready programme** showing that a stage-specific coordinate predicts final plant fitness better than a simpler calendar or adult-only coordinate.",
            "",
            "IWE032 Cardamine already contains a positive stage-specific phase-to-final-fate contrast; its remaining blocker is the numeric 2012–2014 female-flight coordinate needed for the paired adult-vs-stage comparison. Hurlburt 2004 Yucca remains the second near-confirmatory route, blocked by the mature-fruit join key. Aucuba-Asphondylia independently provides direct adult monitoring, experimental oviposition timing, a mechanistically defined host-tissue window, and final seed-producing versus gall fate, but lacks the paired simpler-vs-tissue-stage predictive comparison.",
            "",
            "Parkinsonia-Penthobruchus now provides an independent positive paired realized diagnostic: among seven matched region-season rows, annual ground-pod egg density correlates only moderately with final seed predation (r=0.476), stage-matched egg density after the vulnerable pod pulse improves the association (r=0.596), and filtering that stage-matched exposure by observed parasitism and hatch raises it to r=0.938; leave-one-out RMSE falls from 12.3 to 11.0 to 4.6 percentage points. Because the exposure is realized oviposition rather than independent adult timing, and the filter is consumer/parasitoid survival rather than a host-specific phase coordinate, this remains non-confirmatory.",
            "",
            "Aucuba-Asphondylia adds a stronger experimental host-window-to-final-fate test: adult emergence is monitored directly, attack timing is manipulated within the adult season, and complete gall induction that eliminates seed production drops from 80.9% before the host tissue window closes to 8.8% after it closes. It still lacks a same-unit predictive comparison of adult/calendar timing against the tissue-stage coordinate.",
            "",
            "The registry also retains complete nulls. Posledovich 2015 shows that manipulated stage matching and temperature alter herbivore performance without altering the mature-seedpod escape endpoint beyond host-species effects. The long-term Lathyrus programme shows that climate-driven changes in phenology–seed-predation covariance do not explain flowering-time selection on intact-seed fitness.",
            "",
            "Accordingly, stage-specific timing now has a positive paired realized comparison as well as final-seed-loss examples, but **predictive superiority over simpler adult/calendar timing under the full confirmatory contract remains open**.",
            "",
        ]
    )
    return "\n".join(lines)
