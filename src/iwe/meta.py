from __future__ import annotations

import itertools
import math
import pandas as pd

from .schema import INTERACTION_TYPES


_CLASS_ORDER = [
    "mutualist",
    "antagonist",
    "mixed_pollinating_seed_predator",
]


def fixed_effect_summary(df: pd.DataFrame, group_col: str = "interaction_type") -> pd.DataFrame:
    """Reference inverse-variance summaries for software validation.

    This is not the final publication model. It intentionally ignores cross-row
    dependence and random effects; the real analysis must use a dependence-aware
    multilevel/RVE model after the empirical corpus is known.
    """
    rows: list[dict] = []
    for group, part in df.groupby(group_col, sort=False):
        weights = 1.0 / part["variance_native"].astype(float)
        effects = part["effect_oriented"].astype(float)
        weight_sum = float(weights.sum())
        estimate = float((weights * effects).sum() / weight_sum)
        se = math.sqrt(1.0 / weight_sum)
        q = float((weights * (effects - estimate) ** 2).sum())
        rows.append(
            {
                group_col: group,
                "estimate": estimate,
                "se": se,
                "ci_low": estimate - 1.96 * se,
                "ci_high": estimate + 1.96 * se,
                "q": q,
                "k": int(len(part)),
            }
        )
    out = pd.DataFrame(rows)
    if group_col == "interaction_type" and not out.empty:
        order = {name: i for i, name in enumerate(_CLASS_ORDER)}
        out = out.sort_values(group_col, key=lambda s: s.map(order)).reset_index(drop=True)
    return out


def class_contrasts(summary: pd.DataFrame) -> pd.DataFrame:
    """Return the three preregistered pairwise class contrasts.

    The standard error uses an independent-class approximation and is intended
    only as a first-release software/reference diagnostic.
    """
    if set(summary["interaction_type"]) - INTERACTION_TYPES:
        raise ValueError("summary contains unknown interaction_type")
    lookup = {row["interaction_type"]: row for _, row in summary.iterrows()}
    pairs = [
        ("mutualist", "antagonist"),
        ("mutualist", "mixed_pollinating_seed_predator"),
        ("antagonist", "mixed_pollinating_seed_predator"),
    ]
    rows: list[dict] = []
    for left, right in pairs:
        if left not in lookup or right not in lookup:
            continue
        estimate = float(lookup[left]["estimate"] - lookup[right]["estimate"])
        se = math.sqrt(float(lookup[left]["se"]) ** 2 + float(lookup[right]["se"]) ** 2)
        rows.append(
            {
                "contrast": f"{left} - {right}",
                "estimate": estimate,
                "se": se,
                "ci_low": estimate - 1.96 * se,
                "ci_high": estimate + 1.96 * se,
            }
        )
    return pd.DataFrame(rows)
