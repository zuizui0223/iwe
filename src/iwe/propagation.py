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
DIRECTION_COMPARABLE = {"yes", "no"}

REQUIRED_COLUMNS = [
    "propagation_id",
    "study_id",
    "interaction_type",
    "from_stage",
    "to_stage",
    "transformation",
    "final_fitness_reached",
    "direction_comparable",
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
        "direction_comparable": DIRECTION_COMPARABLE,
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
    final_direction_comparable = final[final["direction_comparable"].eq("yes")]
    prospective_direction_comparable = prospective_reference[
        prospective_reference["direction_comparable"].eq("yes")
    ]
    realized_or_seasonal_direction_comparable = realized_or_seasonal_reference[
        realized_or_seasonal_reference["direction_comparable"].eq("yes")
    ]
    realized_or_seasonal_excluding_iwe032 = realized_or_seasonal_direction_comparable[
        realized_or_seasonal_direction_comparable["study_id"].ne("IWE032")
    ]

    programme_rows: list[dict[str, object]] = []
    for dependence_id, group in final.groupby("dependence_id"):
        interaction_types = set(group["interaction_type"].astype(str))
        reference_classes = set(group["window_reference_class"].astype(str))
        direction_group = group[group["direction_comparable"].eq("yes")]
        if direction_group.empty:
            continue
        transformations = list(direction_group["transformation"].astype(str))
        retained = [state in direction_retaining for state in transformations]

        if reference_classes.issubset(
            {"independent_partner_activity", "direct_interaction_manipulation"}
        ):
            provenance = "prospective"
        elif reference_classes.issubset(
            {"realized_interaction_window", "seasonal_position_only"}
        ):
            provenance = "realized_or_seasonal"
        else:
            provenance = "mixed_reference"

        if all(retained):
            retention_state = "all_retained"
        elif any(retained):
            retention_state = "mixed"
        else:
            retention_state = "none_retained"

        programme_rows.append(
            {
                "dependence_id": str(dependence_id),
                "interaction_type": (
                    next(iter(interaction_types))
                    if len(interaction_types) == 1
                    else "mixed_interaction_class"
                ),
                "provenance": provenance,
                "retention_state": retention_state,
            }
        )

    programme_df = pd.DataFrame(programme_rows)
    antagonist_programmes = programme_df[
        programme_df["interaction_type"].eq("antagonist")
    ]

    antagonist_retention_by_provenance: dict[str, dict[str, int]] = {}
    for provenance in ("prospective", "realized_or_seasonal"):
        part = antagonist_programmes[
            antagonist_programmes["provenance"].eq(provenance)
        ]
        counts = Counter(part["retention_state"])
        antagonist_retention_by_provenance[provenance] = {
            "n": int(len(part)),
            "all_retained": int(counts.get("all_retained", 0)),
            "mixed": int(counts.get("mixed", 0)),
            "none_retained": int(counts.get("none_retained", 0)),
        }

    antagonist_retention_by_reference_class: dict[str, dict[str, int]] = {}
    for reference_class in (
        "independent_partner_activity",
        "direct_interaction_manipulation",
        "realized_interaction_window",
        "seasonal_position_only",
    ):
        part = final[
            final["interaction_type"].eq("antagonist")
            & final["window_reference_class"].eq(reference_class)
            & final["direction_comparable"].eq("yes")
        ]
        programme_states: list[str] = []
        for _, group in part.groupby("dependence_id"):
            retained = group["transformation"].isin(direction_retaining)
            if retained.all():
                programme_states.append("all_retained")
            elif retained.any():
                programme_states.append("mixed")
            else:
                programme_states.append("none_retained")
        counts = Counter(programme_states)
        antagonist_retention_by_reference_class[reference_class] = {
            "n": int(len(programme_states)),
            "all_retained": int(counts.get("all_retained", 0)),
            "mixed": int(counts.get("mixed", 0)),
            "none_retained": int(counts.get("none_retained", 0)),
        }

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
        "final_direction_comparable_links": int(len(final_direction_comparable)),
        "prospective_final_links": int(len(prospective_reference)),
        "prospective_exact_preserved": int(
            prospective_reference["transformation"].eq("preserved").sum()
        ),
        "prospective_direction_comparable_links": int(
            len(prospective_direction_comparable)
        ),
        "prospective_direction_retaining": int(
            prospective_direction_comparable["transformation"].isin(direction_retaining).sum()
        ),
        "realized_or_seasonal_final_links": int(len(realized_or_seasonal_reference)),
        "realized_or_seasonal_exact_preserved": int(
            realized_or_seasonal_reference["transformation"].eq("preserved").sum()
        ),
        "realized_or_seasonal_direction_comparable_links": int(
            len(realized_or_seasonal_direction_comparable)
        ),
        "realized_or_seasonal_direction_retaining": int(
            realized_or_seasonal_direction_comparable["transformation"].isin(direction_retaining).sum()
        ),
        "realized_or_seasonal_excluding_iwe032_direction_comparable": int(
            len(realized_or_seasonal_excluding_iwe032)
        ),
        "realized_or_seasonal_excluding_iwe032_direction_retaining": int(
            realized_or_seasonal_excluding_iwe032["transformation"]
            .isin(direction_retaining)
            .sum()
        ),
        "final_programmes": int(len(programme_df)),
        "antagonist_programmes": int(len(antagonist_programmes)),
        "antagonist_retention_by_provenance": antagonist_retention_by_provenance,
        "antagonist_retention_by_reference_class": antagonist_retention_by_reference_class,
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
        f"- Final-fitness links with a directly comparable upstream/downstream direction: **{summary['final_direction_comparable_links']}**",
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
        "Prospectively defined timing references (independent partner activity or direct timing manipulation) are exact preserved in "
        f"**{summary['prospective_exact_preserved']}/{summary['prospective_final_links']}** final-fitness links. "
        "Among links whose upstream/downstream direction is directly comparable, they retain direction in "
        f"**{summary['prospective_direction_retaining']}/{summary['prospective_direction_comparable_links']}**. "
        "Realized-interaction or seasonal-position references are exact preserved in "
        f"**{summary['realized_or_seasonal_exact_preserved']}/{summary['realized_or_seasonal_final_links']}** links; "
        "among direction-comparable links they retain direction in "
        f"**{summary['realized_or_seasonal_direction_retaining']}/{summary['realized_or_seasonal_direction_comparable_links']}**.",
        "",
        "The shifted-filtered IWE032 total-egg -> active-egg link is explicitly marked direction-incomparable and is not counted as a directional failure. Excluding all IWE032 direction-comparable realized/seasonal links changes direction retention from "
        f"{summary['realized_or_seasonal_direction_retaining']}/{summary['realized_or_seasonal_direction_comparable_links']} "
        "to "
        f"{summary['realized_or_seasonal_excluding_iwe032_direction_retaining']}/"
        f"{summary['realized_or_seasonal_excluding_iwe032_direction_comparable']}, "
        "while the prospective group remains "
        f"{summary['prospective_direction_retaining']}/{summary['prospective_direction_comparable_links']}.",
        "",
        "This contrast is not an inferential prevalence estimate: the corpus is targeted, interaction class, endpoint, causal depth and study design are confounded, and some programmes contribute more than one propagation link. It motivates—but does not identify—a causal-depth hypothesis. In particular, the prospective category mixes independent adult monitoring with direct experimental timing manipulation.",
        "",
        "## Antagonist-only dependence-cluster sensitivity",
        "",
        "To reduce confounding by interaction class and repeated links, final-fitness links are also collapsed to one retention state per dependence cluster within antagonists.",
        "",
        "| Antagonist timing provenance | Programmes | All direction-comparable final links retain direction | Mixed retention | No direction-comparable final link retains direction |",
        "|---|---:|---:|---:|---:|",
        *[
            "| "
            + provenance
            + " | "
            + str(summary["antagonist_retention_by_provenance"][provenance]["n"])
            + " | "
            + str(summary["antagonist_retention_by_provenance"][provenance]["all_retained"])
            + " | "
            + str(summary["antagonist_retention_by_provenance"][provenance]["mixed"])
            + " | "
            + str(summary["antagonist_retention_by_provenance"][provenance]["none_retained"])
            + " |"
            for provenance in ("prospective", "realized_or_seasonal")
        ],
        "",
        "Within antagonists alone, prospective timing references yield "
        f"**{summary['antagonist_retention_by_provenance']['prospective']['all_retained']}/"
        f"{summary['antagonist_retention_by_provenance']['prospective']['n']} programmes with all direction-comparable final links retained**, "
        f"{summary['antagonist_retention_by_provenance']['prospective']['mixed']} mixed, and "
        f"{summary['antagonist_retention_by_provenance']['prospective']['none_retained']} none-retained. "
        "Once direction-incomparable links are excluded from this binary summary, realized/seasonal references yield "
        f"**{summary['antagonist_retention_by_provenance']['realized_or_seasonal']['all_retained']}/"
        f"{summary['antagonist_retention_by_provenance']['realized_or_seasonal']['n']} all-retained**, "
        f"{summary['antagonist_retention_by_provenance']['realized_or_seasonal']['mixed']} mixed, and "
        f"{summary['antagonist_retention_by_provenance']['realized_or_seasonal']['none_retained']} none-retained. "
        "This programme-level sensitivity removes the mutualist-class imbalance and collapses repeated links, while remaining descriptive rather than inferential.",
        "",
        "## Antagonist-only exact-reference sensitivity",
        "",
        "The prospective category still mixes observational adult monitoring with direct timing experiments. The same antagonist links are therefore split by their exact timing-reference class.",
        "",
        "| Antagonist reference class | Programmes | All retained | Mixed | None retained |",
        "|---|---:|---:|---:|---:|",
        *[
            "| "
            + reference_class
            + " | "
            + str(summary["antagonist_retention_by_reference_class"][reference_class]["n"])
            + " | "
            + str(summary["antagonist_retention_by_reference_class"][reference_class]["all_retained"])
            + " | "
            + str(summary["antagonist_retention_by_reference_class"][reference_class]["mixed"])
            + " | "
            + str(summary["antagonist_retention_by_reference_class"][reference_class]["none_retained"])
            + " |"
            for reference_class in (
                "independent_partner_activity",
                "direct_interaction_manipulation",
                "realized_interaction_window",
                "seasonal_position_only",
            )
        ],
        "",
        "This split makes the design confounding explicit: independent adult monitoring and direct timing manipulations should not be interpreted as one biological causal-depth treatment. The table is a diagnostic for where confirmatory matched-design evidence is still missing.",
        "",
        "## Interpretation",
        "",
        "The current pilot falsifies the idea that a phenological effect can be represented by one invariant synchrony coefficient carried unchanged from encounter to fitness. Source-backed timing signals are observed to persist, reverse sign, be shifted by host/consumer filtering, disappear before the next consumer stage, be buffered by alternative ecological routes, or fail to track moving resources. In the current targeted mutualist set, three final-fitness links are classified as preserved and IWE023 Mertensia is classified as buffered: visitation declines more than fivefold across flowering cohorts, but changing pollinator composition/effectiveness prevents a significant seed-set response across weeks. Antagonist and mixed links occupy multiple additional transformation states. This class pattern is a hypothesis-generating contrast, not a prevalence estimate.",
        "",
        "Positive downstream propagation is not confined to Cardamine. Aucuba provides a direct timing manipulation in which complete gall induction that prevents seed production falls from 80.9% before 15 June to 8.8% after the host tissue window closes. Wise 2015 independently preserves experimentally shifted adult wheat-midge exposure timing to final seed damage/yield loss, while Wu 2015 links independently monitored adult occurrence × susceptible ear emergence to final yield loss across >400 cultivars. Cardamine adds ecotype-level phase-to-final-fate alignment, while Kula provides an independent mixed-system mechanistic sign reversal as a response-independent phase-safety margin crosses zero; Kula stops at predation rather than final plant fitness.",
        "",
        "Equally important are explicit nulls and buffers. Mertensia shows a prospective mutualist signal that is buffered: total visitation falls more than fivefold, but a shift toward more effective bumblebee visits leaves no significant seed-set difference across flowering weeks. Gols 2025 gives an independent prospective antagonist stress test within one experiment: herbivory timing is buffered before integrated reproductive potential in Sinapis arvensis but preserved in Brassica nigra. James shows a flowering-time signal at oviposition that disappears by realized cheater larval load. Posledovich shows host-stage matching that affects herbivore performance but not the mature-seedpod escape endpoint. Long-term Lathyrus shows a moving phenology-predation covariance that does not explain flowering-time selection on intact-seed fitness. Hemborg–Després Trollius shows a different transformation: early flowers on multi-flowered plants receive more oviposition and higher relative predation, yet the additional reproductive units buffer that cost so multi-flowered plants finish with higher annual seed output.",
        "",
        "The confirmatory target is therefore signal propagation to final plant fitness, not the mere existence of a biologically plausible stage-specific timing mechanism.",
        "",
    ]
    return "\n".join(lines)
