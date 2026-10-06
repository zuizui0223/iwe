from __future__ import annotations

from collections import Counter

import pandas as pd

from .landscape import WINDOW_REFERENCE_CLASSES
from .schema import INTERACTION_TYPES


TRANSFORMATIONS = {
    "preserved",
    "sign_reversed",
    "shifted_filtered",
    "erased",
    "buffered",
    "tracking_inertia",
    "preserved_net_changed_mechanism",
}

FINAL_FITNESS_REACHED = {"yes", "no"}

REQUIRED_COLUMNS = [
    "propagation_id",
    "study_id",
    "interaction_type",
    "from_stage",
    "to_stage",
    "transformation",
    "final_fitness_reached",
    "dependence_id",
    "window_reference_class",
    "evidence_note",
]


def validate_propagation_registry(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    duplicated = df["propagation_id"].duplicated()
    if duplicated.any():
        values = sorted(df.loc[duplicated, "propagation_id"].astype(str))
        errors.append(f"duplicate propagation_id values: {', '.join(values)}")

    checks = {
        "interaction_type": INTERACTION_TYPES,
        "transformation": TRANSFORMATIONS,
        "final_fitness_reached": FINAL_FITNESS_REACHED,
        "window_reference_class": WINDOW_REFERENCE_CLASSES,
    }
    for column, allowed in checks.items():
        invalid = sorted(set(df[column].dropna().astype(str)) - allowed)
        if invalid:
            errors.append(f"{column}: invalid values: {', '.join(invalid)}")

    for column in ("propagation_id", "study_id", "from_stage", "to_stage", "dependence_id"):
        if df[column].fillna("").astype(str).str.strip().eq("").any():
            errors.append(f"{column} must be non-blank")

    return errors


def propagation_summary(df: pd.DataFrame) -> dict[str, object]:
    errors = validate_propagation_registry(df)
    if errors:
        raise ValueError("; ".join(errors))

    final = df[df["final_fitness_reached"].eq("yes")]

    final_transformations_by_class = {
        interaction_type: dict(Counter(group["transformation"]))
        for interaction_type, group in final.groupby("interaction_type")
    }
    final_transformations_by_reference = {
        reference_class: dict(Counter(group["transformation"]))
        for reference_class, group in final.groupby("window_reference_class")
    }

    prospective_reference = final[
        final["window_reference_class"].isin(
            {"independent_partner_activity", "direct_interaction_manipulation"}
        )
    ]
    realized_or_seasonal_reference = final[
        final["window_reference_class"].isin(
            {"realized_interaction_window", "seasonal_position_only"}
        )
    ]
    direction_retaining = {"preserved", "preserved_net_changed_mechanism"}

    return {
        "n_links": int(len(df)),
        "n_studies": int(df["study_id"].nunique()),
        "n_dependence_clusters": int(df["dependence_id"].nunique()),
        "by_transformation": dict(Counter(df["transformation"])),
        "by_interaction_type": dict(Counter(df["interaction_type"])),
        "by_reference_class": dict(Counter(df["window_reference_class"])),
        "final_links": int(len(final)),
        "final_studies": int(final["study_id"].nunique()),
        "final_by_transformation": dict(Counter(final["transformation"])),
        "final_transformations_by_class": final_transformations_by_class,
        "final_transformations_by_reference": final_transformations_by_reference,
        "prospective_final_links": int(len(prospective_reference)),
        "prospective_exact_preserved": int(
            prospective_reference["transformation"].eq("preserved").sum()
        ),
        "prospective_direction_retaining": int(
            prospective_reference["transformation"].isin(direction_retaining).sum()
        ),
        "realized_or_seasonal_final_links": int(len(realized_or_seasonal_reference)),
        "realized_or_seasonal_exact_preserved": int(
            realized_or_seasonal_reference["transformation"].eq("preserved").sum()
        ),
        "realized_or_seasonal_direction_retaining": int(
            realized_or_seasonal_reference["transformation"].isin(direction_retaining).sum()
        ),
    }


def render_propagation_audit(df: pd.DataFrame) -> str:
    summary = propagation_summary(df)

    def rows(mapping: dict[str, int]) -> list[str]:
        return [f"| {key} | {value} |" for key, value in sorted(mapping.items())]

    lines = [
        "# IWE temporal signal-propagation audit",
        "",
        "_Generated from data/registry/temporal_signal_components.csv; do not edit counts by hand._",
        "",
        "## Scope",
        "",
        f"- Registered propagation links: **{summary['n_links']}**",
        f"- Studies: **{summary['n_studies']}**",
        f"- Dependence clusters: **{summary['n_dependence_clusters']}**",
        f"- Links reaching a final plant-fitness endpoint: **{summary['final_links']}** "
        f"from **{summary['final_studies']} studies**",
        "",
        "A propagation link is not an effect size. It records whether a source-backed timing signal is preserved, transformed, reversed, erased, buffered, or fails to track a downstream stage. Multiple links from one programme retain one dependence cluster.",
        "",
        "## Transformation states",
        "",
        "| Transformation | Links |",
        "|---|---:|",
        *rows(summary["by_transformation"]),
        "",
        "## Interaction classes",
        "",
        "| Interaction type | Links |",
        "|---|---:|",
        *rows(summary["by_interaction_type"]),
        "",
        "## Provenance of the upstream temporal reference",
        "",
        "| Window-reference class | Links |",
        "|---|---:|",
        *rows(summary["by_reference_class"]),
        "",
        "## Transformations observed in chains that reach final plant fitness",
        "",
        "| Transformation | Links |",
        "|---|---:|",
        *rows(summary["final_by_transformation"]),
        "",
        "## Final-link transformations by interaction class",
        "",
        "This matrix is descriptive for the targeted pilot corpus. It is not a literature-wide prevalence estimate.",
        "",
        "| Interaction type | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        *[
            "| "
            + interaction_type
            + " | "
            + " | ".join(
                str(summary["final_transformations_by_class"].get(interaction_type, {}).get(state, 0))
                for state in [
                    "preserved",
                    "shifted_filtered",
                    "sign_reversed",
                    "erased",
                    "buffered",
                    "tracking_inertia",
                    "preserved_net_changed_mechanism",
                ]
            )
            + " |"
            for interaction_type in [
                "mutualist",
                "antagonist",
                "mixed_pollinating_seed_predator",
            ]
        ],
        "",
        "## Final-link transformations by timing-reference provenance",
        "",
        "This table is descriptive at the propagation-link level. IWE032 contributes two final-fitness links to the realized-interaction class, so these rows are not treated as independent studies.",
        "",
        "| Timing reference | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        *[
            "| "
            + reference_class
            + " | "
            + " | ".join(
                str(summary["final_transformations_by_reference"].get(reference_class, {}).get(state, 0))
                for state in [
                    "preserved",
                    "shifted_filtered",
                    "sign_reversed",
                    "erased",
                    "buffered",
                    "tracking_inertia",
                    "preserved_net_changed_mechanism",
                ]
            )
            + " |"
            for reference_class in [
                "independent_partner_activity",
                "direct_interaction_manipulation",
                "realized_interaction_window",
                "seasonal_position_only",
            ]
        ],
        "",
        "Prospectively defined timing references (independent partner activity or direct timing manipulation) retain the signal direction in "
        f"**{summary['prospective_direction_retaining']}/{summary['prospective_final_links']}** final-fitness links "
        f"({summary['prospective_exact_preserved']}/{summary['prospective_final_links']} are exact preserved). "
        "Realized-interaction or seasonal-position references retain direction in "
        f"**{summary['realized_or_seasonal_direction_retaining']}/{summary['realized_or_seasonal_final_links']}** links "
        f"({summary['realized_or_seasonal_exact_preserved']}/{summary['realized_or_seasonal_final_links']} exact preserved).",
        "",
        "The descriptive contrast is not driven by the duplicated Cardamine dependence cluster. If either of the two IWE032 final-fitness links is removed, direction retention in the realized/seasonal group is 1/7 or 2/7, while the prospective group remains 7/8.",
        "",
        "This contrast is not an inferential prevalence estimate: the corpus is targeted, interaction class and timing provenance are confounded, and some programmes contribute more than one propagation link. It is a source-backed diagnostic supporting the next hypothesis that temporal signals are most stable when timing is defined prospectively at or near the biologically effective interaction stage.",
        "",
        "## Interpretation",
        "",
        "The current pilot falsifies the idea that a phenological effect can be represented by one invariant synchrony coefficient carried unchanged from encounter to fitness. Source-backed timing signals are observed to persist, reverse sign, be shifted by host/consumer filtering, disappear before the next consumer stage, be buffered by alternative ecological routes, or fail to track moving resources. In the current targeted set, all four mutualist service-window links that reach final plant fitness are classified as preserved, whereas antagonist and mixed links occupy multiple transformation states. This class pattern is a hypothesis-generating contrast, not a prevalence estimate.",
        "",
        "Positive downstream propagation is not confined to Cardamine. Aucuba provides a direct timing manipulation in which complete gall induction that prevents seed production falls from 80.9% before 15 June to 8.8% after the host tissue window closes. Wise 2015 independently preserves experimentally shifted adult wheat-midge exposure timing to final seed damage/yield loss, while Wu 2015 links independently monitored adult occurrence × susceptible ear emergence to final yield loss across >400 cultivars. Cardamine adds ecotype-level phase-to-final-fate alignment, while Kula provides an independent mixed-system mechanistic sign reversal as a response-independent phase-safety margin crosses zero; Kula stops at predation rather than final plant fitness.",
        "",
        "Equally important are explicit nulls and buffers. James shows a flowering-time signal at oviposition that disappears by realized cheater larval load. Posledovich shows host-stage matching that affects herbivore performance but not the mature-seedpod escape endpoint. Long-term Lathyrus shows a moving phenology-predation covariance that does not explain flowering-time selection on intact-seed fitness. Hemborg–Després Trollius shows a different transformation: early flowers on multi-flowered plants receive more oviposition and higher relative predation, yet the additional reproductive units buffer that cost so multi-flowered plants finish with higher annual seed output.",
        "",
        "The confirmatory target is therefore signal propagation to final plant fitness, not the mere existence of a biologically plausible stage-specific timing mechanism.",
        "",
    ]
    return "\n".join(lines)
