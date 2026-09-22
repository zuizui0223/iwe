from __future__ import annotations

import pandas as pd

from .schema import INTERACTION_TYPES


TARGET_EFFECT_FAMILY = "standardized_mean_difference"
MIN_INDEPENDENT_CLUSTERS_PER_CLASS = 2
REPLICATION_PRIORITY = [
    "mixed_pollinating_seed_predator",
    "antagonist",
    "mutualist",
]


def replication_target_status(
    real_primary: pd.DataFrame,
    effect_family: str = TARGET_EFFECT_FAMILY,
    minimum_clusters: int = MIN_INDEPENDENT_CLUSTERS_PER_CLASS,
) -> dict[str, object]:
    """Return the executable replication gap for the target native effect family."""
    if minimum_clusters < 1:
        raise ValueError("minimum_clusters must be >= 1")

    if real_primary.empty:
        family = real_primary.copy()
    else:
        family = real_primary.loc[
            real_primary["effect_family"].astype(str) == effect_family
        ].copy()

    current = {
        interaction_type: int(
            family.loc[
                family["interaction_type"] == interaction_type, "dependence_id"
            ].nunique()
        )
        for interaction_type in sorted(INTERACTION_TYPES)
    }
    missing = {
        interaction_type: max(0, minimum_clusters - count)
        for interaction_type, count in current.items()
    }
    priority = [
        interaction_type
        for interaction_type in REPLICATION_PRIORITY
        if missing.get(interaction_type, 0) > 0
    ]

    return {
        "effect_family": effect_family,
        "minimum_independent_clusters_per_class": minimum_clusters,
        "current_independent_clusters_by_class": current,
        "clusters_needed_by_class": missing,
        "priority_classes": priority,
        "status": "complete" if not priority else "incomplete",
    }
