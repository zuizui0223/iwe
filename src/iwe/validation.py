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
    TIMING_ANALYSIS_CLASSES,
    TIMING_DOMAINS,
    TIMING_METRIC_TYPES,
)


_SIGNED_TIMING_METRICS = {"plant_minus_partner", "partner_minus_plant"}
_ONE_SIDED_DOMAINS = {"plant_earlier_only", "partner_earlier_only"}


def _expected_exposure_direction(metric: str, domain: str) -> str | None:
    if metric == "overlap_index":
        return "synchrony"
    if metric == "absolute_mismatch":
        return "mismatch"
    if metric == "plant_minus_partner":
        if domain == "plant_earlier_only":
            return "synchrony"
        if domain == "partner_earlier_only":
            return "mismatch"
    if metric == "partner_minus_plant":
        if domain == "plant_earlier_only":
            return "mismatch"
        if domain == "partner_earlier_only":
            return "synchrony"
    return None


def _validate_timing_contract(row: pd.Series, prefix: str, errors: list[str]) -> None:
    metric = row["timing_metric_type"]
    analysis_class = row["timing_analysis_class"]
    domain = row["timing_domain"]
    exposure_direction = row["exposure_direction"]

    if metric not in TIMING_METRIC_TYPES:
        errors.append(f"{prefix}: invalid timing_metric_type")
        return
    if analysis_class not in TIMING_ANALYSIS_CLASSES:
        errors.append(f"{prefix}: invalid timing_analysis_class")
        return
    if domain not in TIMING_DOMAINS:
        errors.append(f"{prefix}: invalid timing_domain")
        return

    if row["evidence_tier"] == "C":
        if analysis_class != "proxy_only":
            errors.append(f"{prefix}: Tier C must use proxy_only timing_analysis_class")
        return
    if analysis_class == "proxy_only":
        errors.append(f"{prefix}: proxy_only timing_analysis_class is reserved for Tier C")
        return

    if analysis_class == "strict_window":
        if metric in _SIGNED_TIMING_METRICS and domain not in _ONE_SIDED_DOMAINS:
            errors.append(
                f"{prefix}: strict_window signed timing metric requires a one-sided timing_domain"
            )
        if metric in {"experimental_plant_shift", "seasonal_position"} and domain != "ordered_by_measured_window":
            errors.append(
                f"{prefix}: strict_window {metric} requires ordered_by_measured_window timing_domain"
            )
        if metric == "other_registered" and domain == "unknown":
            errors.append(f"{prefix}: strict_window other_registered timing metric cannot have unknown timing_domain")

        expected = _expected_exposure_direction(metric, domain)
        if expected is not None and exposure_direction != expected:
            errors.append(
                f"{prefix}: {metric} with timing_domain={domain} must use exposure_direction={expected}"
            )

    if analysis_class == "directional_mismatch":
        if metric not in _SIGNED_TIMING_METRICS:
            errors.append(f"{prefix}: directional_mismatch requires a signed timing metric")
        if domain not in _ONE_SIDED_DOMAINS:
            errors.append(f"{prefix}: directional_mismatch requires a one-sided timing_domain")


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

        _validate_timing_contract(row, prefix, errors)
    return errors


def build_primary_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Return strict Tier-A H1 evidence only.

    Rows can remain valid Tier-A extractions while being excluded from the strict
    synchrony estimand when their timing metric cannot yet be oriented without
    additional source-domain evidence.
    """
    errors = validate_effect_rows(df)
    if errors:
        raise ValueError("; ".join(errors))
    out = df.loc[
        (df["evidence_tier"] == "A")
        & (df["timing_analysis_class"] == "strict_window")
    ].copy()
    out["effect_oriented"] = [
        orient_effect(v, d)
        for v, d in zip(out["effect_native"], out["exposure_direction"], strict=True)
    ]
    return out.reset_index(drop=True)
