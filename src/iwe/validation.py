from __future__ import annotations

import math
import pandas as pd

from .effects import orient_effect
from .schema import (
    EFFECT_FAMILIES,
    EVIDENCE_TIERS,
    EXPOSURE_DIRECTIONS,
    INTERACTION_TYPES,
    PHENOLOGY_SOURCES,
    REQUIRED_EFFECT_COLUMNS,
)


def validate_effect_rows(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = [c for c in REQUIRED_EFFECT_COLUMNS if c not in df.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    if df["effect_id"].duplicated().any():
        errors.append("duplicate effect_id detected")

    for idx, row in df.iterrows():
        prefix = f"row {idx}"
        if row["interaction_type"] not in INTERACTION_TYPES:
            errors.append(f"{prefix}: invalid interaction_type")
        if row["evidence_tier"] not in EVIDENCE_TIERS:
            errors.append(f"{prefix}: invalid evidence_tier")
        if row["phenology_source"] not in PHENOLOGY_SOURCES:
            errors.append(f"{prefix}: invalid phenology_source")
        if row["exposure_direction"] not in EXPOSURE_DIRECTIONS:
            errors.append(f"{prefix}: invalid exposure_direction")
        if row["effect_family"] not in EFFECT_FAMILIES:
            errors.append(f"{prefix}: invalid effect_family")
        if pd.isna(row["dependence_id"]) or not str(row["dependence_id"]).strip():
            errors.append(f"{prefix}: missing dependence_id")
        if pd.isna(row["effect_native"]) or not math.isfinite(float(row["effect_native"])):
            errors.append(f"{prefix}: effect_native must be finite")
        if pd.isna(row["variance_native"]):
            errors.append(f"{prefix}: variance_native is required")
        else:
            variance = float(row["variance_native"])
            if not math.isfinite(variance) or variance <= 0:
                errors.append(f"{prefix}: variance_native must be finite and > 0")
        if pd.isna(row["sample_size"]):
            errors.append(f"{prefix}: sample_size is required")
        else:
            n = float(row["sample_size"])
            if not math.isfinite(n) or n <= 0 or int(n) != n:
                errors.append(f"{prefix}: sample_size must be a positive integer")
        if row["evidence_tier"] == "C" and row["phenology_source"] != "occurrence_proxy":
            errors.append(f"{prefix}: Tier C must use occurrence_proxy phenology_source")
        if row["phenology_source"] == "occurrence_proxy" and row["evidence_tier"] != "C":
            errors.append(f"{prefix}: occurrence_proxy must remain Tier C")
    return errors


def build_primary_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Validate extraction rows and return Tier-A direct evidence with explicit orientation."""
    errors = validate_effect_rows(df)
    if errors:
        raise ValueError("; ".join(errors))
    out = df.loc[df["evidence_tier"] == "A"].copy()
    out["effect_oriented"] = [
        orient_effect(v, d)
        for v, d in zip(out["effect_native"], out["exposure_direction"], strict=True)
    ]
    return out.reset_index(drop=True)
