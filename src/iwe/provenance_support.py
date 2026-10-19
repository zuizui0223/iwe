"""Descriptive support audit for timing-reference claims in the IWE pilot.

This is an evidence-structure diagnostic, NOT a test of biological effect size,
causal information preservation, or prediction accuracy.
"""
from __future__ import annotations

import pandas as pd

from .endpoint_audit import RETAINING, validate_endpoint_audit
from .propagation import validate_propagation_registry

INTERACTION_TYPES = (
    "mutualist", "antagonist", "mixed_pollinating_seed_predator",
)
REFERENCE_CLASSES = (
    "independent_partner_activity", "direct_interaction_manipulation",
    "realized_interaction_window", "seasonal_position_only",
)
PROSPECTIVE = set(REFERENCE_CLASSES[:2])
REALIZED = set(REFERENCE_CLASSES[2:])


def provenance_support(propagation: pd.DataFrame, endpoints: pd.DataFrame) -> dict:
    """Report observed strata and whether *any* programme spans reference families.

    A shared dependence_id is necessary, but NOT sufficient, to identify a
    paired model comparison. Repeated links never count as new programmes.
    """
    errors = validate_propagation_registry(propagation)
    errors += validate_endpoint_audit(propagation, endpoints)
    if errors:
        raise ValueError("; ".join(errors))
    df = propagation.merge(
        endpoints[["propagation_id", "endpoint_class"]],
        on="propagation_id", validate="one_to_one",
    )
    # Never treat terminal fates, predation rates, derived fitness indices, or
    # model-predicted outcomes as observed mature-seed/yield equivalents.
    strict = df[
        df["endpoint_class"].eq("observed_mature_seed_or_yield")
        & df["direction_comparable"].eq("yes")
    ]
    final = df[
        df["endpoint_class"].ne("intermediate_only")
        & df["direction_comparable"].eq("yes")
    ]
    rows = []
    for interaction_type in INTERACTION_TYPES:
        for reference in REFERENCE_CLASSES:
            g = strict[
                strict["interaction_type"].eq(interaction_type)
                & strict["window_reference_class"].eq(reference)
            ]
            rows.append({
                "interaction_type": interaction_type,
                "window_reference_class": reference,
                "links": int(len(g)),
                "clusters": int(g["dependence_id"].nunique()),
                "retained_links": int(g["transformation"].isin(RETAINING).sum()),
            })

    def crosses_reference_family(frame: pd.DataFrame) -> list[str]:
        matched = []
        for dependence_id, group in frame.groupby("dependence_id"):
            # A dependence ID is not a valid common unit across different
            # interaction types. Fail rather than manufacturing a pair.
            if group["interaction_type"].nunique() != 1:
                raise ValueError("dependence cluster spans interaction types: " + str(dependence_id))
            observed = set(group["window_reference_class"])
            if observed & PROSPECTIVE and observed & REALIZED:
                matched.append(str(dependence_id))
        return sorted(matched)

    return {
        "strict_links": int(len(strict)),
        "strict_clusters": int(strict["dependence_id"].nunique()),
        "all_final_comparable_links": int(len(final)),
        "strata": rows,
        "strict_cross_family_clusters": crosses_reference_family(strict),
        "all_final_cross_family_clusters": crosses_reference_family(final),
    }


def render_provenance_support(propagation: pd.DataFrame, endpoints: pd.DataFrame) -> str:
    a = provenance_support(propagation, endpoints)
    lines = [
        "# IWE timing-reference support / positivity audit",
        "",
        "_Generated from temporal_signal_components.csv and propagation_endpoint_audit.csv._",
        "",
        "## Strict observed mature-seed/yield endpoint",
        "",
        f"- Direction-comparable links: **{a['strict_links']}**",
        f"- Distinct dependence clusters across these links: **{a['strict_clusters']}**",
        "",
        "| Interaction class | Timing reference | Links | Clusters | Direction retained |",
        "|---|---|---:|---:|---:|",
    ]
    for row in a["strata"]:
        lines.append(
            f"| {row['interaction_type']} | {row['window_reference_class']} | "
            f"{row['links']} | {row['clusters']} | {row['retained_links']} |"
        )
    lines += [
        "",
        "## Within-programme cross-reference support",
        "",
        "For this diagnostic, a cross-reference programme must contain at least one "
        "independent-partner/direct-manipulation link and one realized/seasonal "
        "link with the **same** dependence ID. This is only a necessary coverage "
        "condition, never sufficient for a paired prediction comparison.",
        "",
        f"- Strict mature-seed/yield cross-family programmes: "
        f"**{len(a['strict_cross_family_clusters'])}**",
        f"- All direction-comparable final endpoints (different endpoint types "
        f"kept separate for inference): **{len(a['all_final_cross_family_clusters'])}** "
        f"cross-family programmes among **{a['all_final_comparable_links']}** links",
        "",
        "## What can and cannot be concluded",
        "",
        "- The existing preservation proportions compare **different programmes, "
        "methods and biological endpoints**, not two timings observed on the same "
        "study units.",
        "- A zero stratum is missing support, **not** an observed failure of "
        "preservation. Repeated rows from one dependence cluster are not "
        "independent replications.",
        "- Direct experimental timing manipulations and direct adult-activity "
        "monitoring are distinct designs. Neither should be called a measured "
        "effective consumer stage without that stage actually being observed.",
        "- Even a positive cross-reference count would not prove paired model "
        "superiority: same endpoint, same units, pre-outcome filters, response-blind "
        "model selection and genuinely held-out predictions are still required.",
        "- These tables are diagnostic for the **targeted, outcome-aware pilot "
        "corpus**, not a population prevalence estimate, causal effect or "
        "eligible strict-H1 meta-analysis.",
        "",
        "**Decision:** Do not infer a general advantage of downstream or "
        "prospective timing from cross-programme direction-retention percentages. "
        "Keep the conversion-bottleneck hypothesis exploratory until a genuine "
        "same-unit paired comparison passes the prospective gate.",
        "",
    ]
    return "\n".join(lines)
