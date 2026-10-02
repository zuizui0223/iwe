from __future__ import annotations

from collections import Counter

import pandas as pd

from .schema import INTERACTION_TYPES


WINDOW_REFERENCE_CLASSES = {
    "independent_partner_activity",
    "realized_interaction_window",
    "historical_partner_window",
    "seasonal_position_only",
    "direct_interaction_manipulation",
}

TIMING_GEOMETRIES = {
    "two_sided_signed_lag",
    "seasonal_gradient",
    "seasonal_selection",
    "early_vs_late",
    "ordered_window",
    "interaction_timing_manipulation",
    "early_core_late",
}

FITNESS_CHANNELS = {
    "net_reproduction",
    "benefit_channel",
    "cost_channel",
    "total_offspring_fitness",
    "potential_reproduction",
}

OUTCOME_FINALITY = {"final", "not_final"}

QUANT_STATUSES = {
    "extracted",
    "native_extracted",
    "directional_extracted",
    "pending",
    "variance_hold",
    "blocked_timing_linkage",
}

LANDSCAPE_STATUSES = {
    "strong_candidate",
    "reextract_directional",
    "directional_evidence",
    "candidate_noncausal_window",
    "candidate_seasonal_landscape",
    "selection_shift_evidence",
    "mixed_channel_decomposition_candidate",
    "experimental_timing_candidate",
    "mechanism_only",
    "context_only",
}

REQUIRED_COLUMNS = [
    "component_id",
    "study_id",
    "interaction_type",
    "window_reference_class",
    "timing_geometry",
    "fitness_channel",
    "outcome_finality",
    "current_quant_status",
    "landscape_status",
    "dependence_id",
    "notes",
]


def validate_landscape_registry(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    if df["component_id"].duplicated().any():
        duplicates = sorted(
            df.loc[df["component_id"].duplicated(), "component_id"].astype(str)
        )
        errors.append(f"duplicate component_id values: {', '.join(duplicates)}")

    categorical_checks = {
        "interaction_type": INTERACTION_TYPES,
        "window_reference_class": WINDOW_REFERENCE_CLASSES,
        "timing_geometry": TIMING_GEOMETRIES,
        "fitness_channel": FITNESS_CHANNELS,
        "outcome_finality": OUTCOME_FINALITY,
        "current_quant_status": QUANT_STATUSES,
        "landscape_status": LANDSCAPE_STATUSES,
    }
    for column, allowed in categorical_checks.items():
        invalid = sorted(set(df[column].dropna().astype(str)) - allowed)
        if invalid:
            errors.append(f"{column}: invalid values: {', '.join(invalid)}")

    if df["component_id"].fillna("").astype(str).str.strip().eq("").any():
        errors.append("component_id must be non-blank")

    if df["dependence_id"].fillna("").astype(str).str.strip().eq("").any():
        errors.append("dependence_id must be non-blank")

    strong = df["landscape_status"].eq("strong_candidate")
    bad_strong = df.loc[
        strong
        & (
            df["window_reference_class"].ne("independent_partner_activity")
            | df["outcome_finality"].ne("final")
        ),
        "component_id",
    ].astype(str)
    if len(bad_strong):
        errors.append(
            "strong_candidate requires independent_partner_activity and final outcome: "
            + ", ".join(sorted(bad_strong))
        )

    directional = df["landscape_status"].eq("reextract_directional")
    bad_directional = df.loc[
        directional
        & (
            df["window_reference_class"].ne("independent_partner_activity")
            | df["timing_geometry"].ne("two_sided_signed_lag")
        ),
        "component_id",
    ].astype(str)
    if len(bad_directional):
        errors.append(
            "reextract_directional requires independent partner activity and a two-sided signed lag: "
            + ", ".join(sorted(bad_directional))
        )

    mixed_decomp = df["landscape_status"].eq(
        "mixed_channel_decomposition_candidate"
    )
    bad_mixed = df.loc[
        mixed_decomp
        & df["interaction_type"].ne("mixed_pollinating_seed_predator"),
        "component_id",
    ].astype(str)
    if len(bad_mixed):
        errors.append(
            "mixed_channel_decomposition_candidate must be mixed: "
            + ", ".join(sorted(bad_mixed))
        )

    mechanism = df["landscape_status"].eq("mechanism_only")
    bad_mechanism = df.loc[
        mechanism & df["outcome_finality"].eq("final"), "component_id"
    ].astype(str)
    if len(bad_mechanism):
        errors.append(
            "mechanism_only is reserved for non-final outcomes: "
            + ", ".join(sorted(bad_mechanism))
        )

    return errors


def landscape_pilot_summary(df: pd.DataFrame) -> dict[str, object]:
    errors = validate_landscape_registry(df)
    if errors:
        raise ValueError("; ".join(errors))

    strong = df[df["landscape_status"].eq("strong_candidate")]
    independent = df[
        df["window_reference_class"].eq("independent_partner_activity")
    ]
    recoverable = df[
        df["landscape_status"].isin(
            {
                "strong_candidate",
                "reextract_directional",
                "directional_evidence",
                "candidate_noncausal_window",
                "candidate_seasonal_landscape",
                "selection_shift_evidence",
                "mixed_channel_decomposition_candidate",
                "experimental_timing_candidate",
            }
        )
    ]

    return {
        "n_components": int(len(df)),
        "n_studies": int(df["study_id"].nunique()),
        "n_dependence_clusters": int(df["dependence_id"].nunique()),
        "by_interaction_type": dict(Counter(df["interaction_type"])),
        "by_reference_class": dict(Counter(df["window_reference_class"])),
        "by_landscape_status": dict(Counter(df["landscape_status"])),
        "strong_candidates_by_class": dict(Counter(strong["interaction_type"])),
        "independent_reference_by_class": dict(
            Counter(independent["interaction_type"])
        ),
        "recoverable_programmes_by_class": {
            interaction_type: int(group["dependence_id"].nunique())
            for interaction_type, group in recoverable.groupby("interaction_type")
        },
    }


def render_landscape_pilot_audit(df: pd.DataFrame) -> str:
    summary = landscape_pilot_summary(df)

    def rows(mapping: dict[str, int]) -> list[str]:
        return [
            f"| {key} | {value} |"
            for key, value in sorted(mapping.items())
        ]

    lines = [
        "# IWE landscape pilot audit",
        "",
        "_Generated from data/registry/landscape_components.csv; do not edit counts by hand._",
        "",
        "## Pilot scope",
        "",
        f"- Components: **{summary['n_components']}**",
        f"- Studies: **{summary['n_studies']}**",
        f"- Dependence clusters: **{summary['n_dependence_clusters']}**",
        "",
        "This is a deliberately small re-audit of already-screened IWE programmes. It is not a systematic-review denominator.",
        "",
        "## Components by interaction type",
        "",
        "| Interaction type | Components |",
        "|---|---:|",
        *rows(summary["by_interaction_type"]),
        "",
        "## Window-reference provenance",
        "",
        "| Reference class | Components |",
        "|---|---:|",
        *rows(summary["by_reference_class"]),
        "",
        "## Landscape readiness",
        "",
        "| Status | Components |",
        "|---|---:|",
        *rows(summary["by_landscape_status"]),
        "",
        "## High-provenance anchors",
        "",
        "Only strong_candidate rows combine a final reproductive outcome with an independently measured partner-activity window.",
        "",
        "| Interaction type | Strong candidates |",
        "|---|---:|",
        *rows(summary["strong_candidates_by_class"]),
        "",
        "## Independent partner-window coverage",
        "",
        "| Interaction type | Components with independent partner activity |",
        "|---|---:|",
        *rows(summary["independent_reference_by_class"]),
        "",
        "## Recoverable programme clusters under the broadened landscape question",
        "",
        "These counts include strong anchors plus directional re-extraction, realized-window, seasonal-landscape, mixed-decomposition, and direct-interaction-timing routes. They are **not** pooled effect counts and do not imply inferential adequacy.",
        "",
        "| Interaction type | Distinct dependence clusters |",
        "|---|---:|",
        *rows(summary["recoverable_programmes_by_class"]),
        "",
        "## Interpretation",
        "",
        "The pilot explicitly separates two problems that the original strict-H1 analysis combined: (1) whether timing predicts final reproduction, and (2) whether the partner window is independently identified. The landscape pivot can therefore recover antagonist and mixed timing geometry without calling egg receipt, attack, or damage an independent adult-availability curve.",
        "",
        "The next quantitative step is not a three-class pooled meta-analysis. It is programme-level geometry reconstruction, beginning with one-sided IWE001/IWE002, the IWE015 variance audit, and the IWE032 early/core/late antagonist surface.",
        "",
    ]
    return "\n".join(lines)
