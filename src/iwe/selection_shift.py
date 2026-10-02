from __future__ import annotations

import math
from collections import Counter

import pandas as pd


AGENT_CLASSES = {"mutualist", "antagonist", "mixed"}
DESIGNS = {"population_context", "factorial_manipulation", "simulated_antagonist_damage", "pollination_supplementation"}
UNCERTAINTY_STATUSES = {
    "source_interaction_test_no_delta_se",
    "effect_size_ready_independent_groups",
    "effect_size_ready_source_reported_contrast",
}
DIRECTIONS = {"shift_to_earlier", "shift_to_later", "no_direction"}

REQUIRED_COLUMNS = [
    "shift_id",
    "study_key",
    "source_id",
    "plant_taxon",
    "agent_class",
    "agent",
    "design_type",
    "trait_native",
    "canonical_axis",
    "effect_definition",
    "estimate_native",
    "native_positive_meaning",
    "orientation_multiplier",
    "estimate_canonical",
    "se_canonical",
    "uncertainty_status",
    "formal_test",
    "direction_result",
    "dependence_id",
    "provenance",
    "notes",
]


def validate_selection_shift_registry(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return [f"missing required columns: {', '.join(missing)}"]

    if df["shift_id"].duplicated().any():
        duplicates = sorted(
            df.loc[df["shift_id"].duplicated(), "shift_id"].astype(str)
        )
        errors.append(f"duplicate shift_id values: {', '.join(duplicates)}")

    for column, allowed in {
        "agent_class": AGENT_CLASSES,
        "design_type": DESIGNS,
        "uncertainty_status": UNCERTAINTY_STATUSES,
        "direction_result": DIRECTIONS,
    }.items():
        invalid = sorted(set(df[column].dropna().astype(str)) - allowed)
        if invalid:
            errors.append(f"{column}: invalid values: {', '.join(invalid)}")

    for idx, row in df.iterrows():
        prefix = f"row {idx} ({row['shift_id']})"
        if row["canonical_axis"] != "earlier_flowering":
            errors.append(f"{prefix}: canonical_axis must be earlier_flowering")

        try:
            native = float(row["estimate_native"])
            canonical = float(row["estimate_canonical"])
            multiplier = float(row["orientation_multiplier"])
        except (TypeError, ValueError):
            errors.append(
                f"{prefix}: effect estimates and orientation must be numeric"
            )
            continue

        if multiplier not in {-1.0, 1.0}:
            errors.append(f"{prefix}: orientation_multiplier must be -1 or 1")
        if not math.isclose(
            canonical, native * multiplier, abs_tol=1e-10
        ):
            errors.append(
                f"{prefix}: canonical estimate does not equal native * orientation"
            )

        expected_direction = (
            "shift_to_earlier"
            if canonical > 0
            else "shift_to_later"
            if canonical < 0
            else "no_direction"
        )
        if row["direction_result"] != expected_direction:
            errors.append(
                f"{prefix}: direction_result must match canonical estimate sign"
            )

        status = row["uncertainty_status"]
        se = row["se_canonical"]
        if status.startswith("effect_size_ready"):
            if pd.isna(se) or not math.isfinite(float(se)) or float(se) <= 0:
                errors.append(
                    f"{prefix}: effect-size-ready row requires positive SE"
                )
        elif not pd.isna(se):
            errors.append(
                f"{prefix}: non-effect-size-ready row must not invent a delta SE"
            )

        if not str(row["dependence_id"]).strip():
            errors.append(f"{prefix}: dependence_id must be non-blank")

    return errors


def selection_shift_summary(df: pd.DataFrame) -> dict[str, object]:
    errors = validate_selection_shift_registry(df)
    if errors:
        raise ValueError("; ".join(errors))

    effect_ready = df[
        df["uncertainty_status"].astype(str).str.startswith("effect_size_ready")
    ]
    return {
        "n_rows": int(len(df)),
        "n_studies": int(df["study_key"].nunique()),
        "n_clusters": int(df["dependence_id"].nunique()),
        "by_agent_class": dict(Counter(df["agent_class"])),
        "by_direction": dict(Counter(df["direction_result"])),
        "effect_ready_rows": int(len(effect_ready)),
        "effect_ready_clusters": int(
            effect_ready["dependence_id"].nunique()
        ),
    }


def render_selection_shift_audit(df: pd.DataFrame) -> str:
    summary = selection_shift_summary(df)

    lines = [
        "# IWE signed selection-shift pilot",
        "",
        "_Generated from data/registry/selection_shift_components.csv._",
        "",
        "## Scope",
        "",
        f"- Rows: **{summary['n_rows']}**",
        f"- Studies: **{summary['n_studies']}**",
        f"- Dependence clusters: **{summary['n_clusters']}**",
        f"- Effect-size-ready rows: **{summary['effect_ready_rows']}**",
        f"- Effect-size-ready clusters: **{summary['effect_ready_clusters']}**",
        "",
        "All effects are oriented to one canonical coordinate: **positive = the interaction shifts selection toward earlier flowering**; negative = toward later flowering.",
        "",
        "## Agent classes",
        "",
        "| Agent class | Rows |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {key} | {value} |"
        for key, value in sorted(summary["by_agent_class"].items())
    )
    lines.extend(
        [
            "",
            "## Direction",
            "",
            "| Direction | Rows |",
            "|---|---:|",
        ]
    )
    lines.extend(
        f"| {key} | {value} |"
        for key, value in sorted(summary["by_direction"].items())
    )
    lines.extend(
        [
            "",
            "## Biological readout",
            "",
            "The pilot falsifies a simple calendar-direction rule for antagonists. In the Gentiana-Phengaris context, predator presence shifts flowering selection toward later flowering in both years. In the Gymnadenia factorial experiment, floral herbivores shift selection toward earlier flowering, while pollinators shift it toward later flowering. A separate Lythrum simulated-herbivory experiment independently shifts selection toward earlier flowering.",
            "",
            "Thus interaction role alone does not predict the sign of selection on calendar flowering date. The window-relative hypothesis is stronger: antagonists may favor temporal escape on whichever side of their effective interaction window is available, while mutualists can favor movement toward their effective service window.",
            "",
            "IWE012 retains its source-reported interaction tests because the published group means do not provide a defensible variance for the derived mean difference. No zero-covariance approximation is used. The Gymnadenia contrasts are effect-size ready because Appendix A2 reports four independent treatment-group gradients with SEs. The Lythrum damage contrast is also effect-size ready because the source directly reports the damage-by-flowering-time contrast and SE.",
            "",
        ]
    )
    return "\n".join(lines)
