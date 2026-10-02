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
    "gaussian_cost_window",
    "host_stage_survival_filter",
    "sequential_flower_abortion_filter",
    "gaussian_effective_fitness_surface",
    "bimodal_escape_tradeoff",
    "alternative_escape_strategies",
    "within_tree_asynchrony_feedback",
    "accessible_redundancy_window",
    "developmental_phase_lag_reversal",
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
    "statistical_evidence",
    "source_summary_evidence",
    "source_model_reconstructed",
}

LANDSCAPE_STATUSES = {
    "strong_candidate",
    "reextract_directional",
    "directional_evidence",
    "realized_window_evidence",
    "selection_shift_evidence",
    "experimental_timing_evidence",
    "channel_decoupling_evidence",
    "mechanism_only",
    "context_only",
    "boundary_evidence",
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

    directional_evidence = df["landscape_status"].eq("directional_evidence")
    bad_directional_evidence = df.loc[
        directional_evidence
        & (
            df["window_reference_class"].ne("independent_partner_activity")
            | df["timing_geometry"].ne("two_sided_signed_lag")
        ),
        "component_id",
    ].astype(str)
    if len(bad_directional_evidence):
        errors.append(
            "directional_evidence requires independent partner activity and a two-sided signed lag: "
            + ", ".join(sorted(bad_directional_evidence))
        )

    channel_decoupling = df["landscape_status"].eq("channel_decoupling_evidence")
    bad_channel = df.loc[
        channel_decoupling
        & df["interaction_type"].ne("mixed_pollinating_seed_predator"),
        "component_id",
    ].astype(str)
    if len(bad_channel):
        errors.append(
            "channel_decoupling_evidence must be a mixed interaction: "
            + ", ".join(sorted(bad_channel))
        )

    experimental_timing = df["landscape_status"].eq("experimental_timing_evidence")
    bad_experimental_timing = df.loc[
        experimental_timing
        & (
            df["window_reference_class"].ne("direct_interaction_manipulation")
            | df["outcome_finality"].ne("final")
        ),
        "component_id",
    ].astype(str)
    if len(bad_experimental_timing):
        errors.append(
            "experimental_timing_evidence requires a direct interaction manipulation and final outcome: "
            + ", ".join(sorted(bad_experimental_timing))
        )

    selection_shift = df["landscape_status"].eq("selection_shift_evidence")
    bad_selection_shift = df.loc[
        selection_shift & df["outcome_finality"].ne("final"),
        "component_id",
    ].astype(str)
    if len(bad_selection_shift):
        errors.append(
            "selection_shift_evidence requires a final outcome: "
            + ", ".join(sorted(bad_selection_shift))
        )

    realized_window = df["landscape_status"].eq("realized_window_evidence")
    bad_realized_window = df.loc[
        realized_window
        & (
            df["window_reference_class"].ne("realized_interaction_window")
            | df["outcome_finality"].ne("final")
        ),
        "component_id",
    ].astype(str)
    if len(bad_realized_window):
        errors.append(
            "realized_window_evidence requires a realized interaction window and final outcome: "
            + ", ".join(sorted(bad_realized_window))
        )

    boundary = df["landscape_status"].eq("boundary_evidence")
    bad_boundary = df.loc[
        boundary & df["outcome_finality"].ne("final"), "component_id"
    ].astype(str)
    if len(bad_boundary):
        errors.append(
            "boundary_evidence requires a final outcome: "
            + ", ".join(sorted(bad_boundary))
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
                "realized_window_evidence",
                "selection_shift_evidence",
                "experimental_timing_evidence",
                "channel_decoupling_evidence",
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
        "The pilot now separates three biological objects that the original strict-H1 analysis compressed together: (1) partner exposure or realized interaction timing, (2) host-stage sensitivity to that interaction, and (3) final reproductive fitness. This preserves strict partner-window provenance while allowing antagonist and mixed studies to contribute the temporal object they actually identify.",
        "",
        "The branch now contains directional exposure mismatch (IWE001), a plot-level realized antagonist cost surface without plant-level pseudoreplication (IWE011), an antagonist-induced selection shift linked to attack (IWE012), mixed benefit-cost channel decoupling (IWE014), a quantitative mixed Yucca service-window mechanism in which later flowering reduces Tegeticula pollinator abundance and pollinator abundance raises fruit set in both years (Althoff 2005), a senita-cactus redundancy mechanism showing that alternative pollinators buffer only when their activity windows overlap receptive flowers, and a Silene-Hadena developmental phase-lag mechanism in which flowering × oviposition synchrony predicts predation in opposite directions in 2008 versus 2009 because larvae arrive at different delays relative to flowering and fruit maturation. The branch also contains experimentally isolated host-stage sensitivity (IWE031), a source-parameterized shift from raw egg exposure to an effective damaging window plus a source-model link from that window to final intact reproduction (IWE032), an independent Geum-Byturus final-fitness escape tradeoff with an interior optimum at 36% second-peak flowering (Sercu 2020), a Ulex boundary in which temporal escape and predator satiation yield nearly identical whole-season infestation and no flowering-type effect on annual reproduction (Atlan 2010), and a mixed Ficus racemosa boundary in which hotter-season nursery shrinkage reduces pollinator reproduction while seed production nearly doubles despite broadly similar within-tree asynchrony (Krishnan 2014). Mechanism breadth additionally includes an independent Portuguese Gentiana-Phengaris survival filter (Arnaldo 2014) and a taxonomically distinct Yucca-Tegeticula flower-abortion filter (Jadeja 2017). The decisive unresolved test is still independent replication of the raw-exposure-to-effective-window-to-final-fitness chain; IWE015 raw variance and numeric IWE032 female-flight timing remain high-value strong-anchor completions.",
        "",
    ]
    return "\n".join(lines)
