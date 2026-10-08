"""Endpoint-grain sensitivity for the IWE temporal propagation ledger.

A targeted, response-informed evidence audit, not a causal comparison.
"""
from __future__ import annotations

from collections import Counter

import pandas as pd

ENDPOINT_CLASSES = frozenset({
    "observed_mature_seed_or_yield",
    "observed_postcost_reproductive_units",
    "observed_terminal_fate",
    "observed_seed_damage_only",
    "derived_reproductive_index",
    "source_model_predicted_final",
    "intermediate_only",
})
SCOPES = {
    "mature_seed_yield": {"observed_mature_seed_or_yield"},
    "plus_postcost_fruits": {"observed_mature_seed_or_yield",
                             "observed_postcost_reproductive_units"},
    "plus_terminal_fates": {"observed_mature_seed_or_yield",
                            "observed_postcost_reproductive_units",
                            "observed_terminal_fate"},
    "original_final": ENDPOINT_CLASSES - {"intermediate_only"},
}
REFERENCE_GROUPS = {
    "prospective_design": {"independent_partner_activity",
                           "direct_interaction_manipulation"},
    "realized_or_seasonal": {"realized_interaction_window",
                             "seasonal_position_only"},
}
RETAINING = frozenset({"preserved", "preserved_net_changed_mechanism"})


def validate_endpoint_audit(propagation: pd.DataFrame,
                            endpoints: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    required = {"propagation_id", "endpoint_class", "rationale"}
    missing = sorted(required - set(endpoints.columns))
    if missing:
        return ["missing endpoint-audit columns: " + ", ".join(missing)]
    if endpoints["propagation_id"].duplicated().any():
        errors.append("duplicate propagation_id in endpoint audit")
    for field in ("propagation_id", "rationale"):
        if endpoints[field].fillna("").astype(str).str.strip().eq("").any():
            errors.append(field + " must be non-blank")
    invalid = sorted(set(endpoints["endpoint_class"].dropna().astype(str))
                     - ENDPOINT_CLASSES)
    if invalid:
        errors.append("invalid endpoint_class: " + ", ".join(invalid))
    pids = set(propagation["propagation_id"].astype(str))
    eids = set(endpoints["propagation_id"].astype(str))
    if pids - eids:
        errors.append("unclassified IDs: " + ", ".join(sorted(pids - eids)))
    if eids - pids:
        errors.append("unknown IDs: " + ", ".join(sorted(eids - pids)))
    if errors:
        return errors
    joined = propagation[["propagation_id", "final_fitness_reached"]].merge(
        endpoints[["propagation_id", "endpoint_class"]],
        on="propagation_id", validate="one_to_one"
    )
    intermediate = joined["endpoint_class"].eq("intermediate_only")
    bad = joined.loc[
        (intermediate & joined["final_fitness_reached"].ne("no"))
        | (~intermediate & joined["final_fitness_reached"].ne("yes")),
        "propagation_id",
    ]
    if len(bad):
        errors.append("endpoint/final-link inconsistency: "
                      + ", ".join(sorted(bad.astype(str))))
    return errors


def endpoint_sensitivity(propagation: pd.DataFrame,
                         endpoints: pd.DataFrame) -> dict[str, object]:
    errors = validate_endpoint_audit(propagation, endpoints)
    if errors:
        raise ValueError("; ".join(errors))
    df = propagation.merge(endpoints, on="propagation_id", validate="one_to_one")
    summary = []
    ant_programmes = []
    for name, classes in SCOPES.items():
        selected = df[df["endpoint_class"].isin(classes)]
        for reference, reference_classes in REFERENCE_GROUPS.items():
            g = selected[selected["window_reference_class"].isin(reference_classes)]
            comparable = g[g["direction_comparable"].eq("yes")]
            summary.append({
                "scope": name,
                "reference": reference,
                "links": int(len(g)),
                "comparable": int(len(comparable)),
                "retained": int(comparable["transformation"].isin(RETAINING).sum()),
                "exact_preserved": int(g["transformation"].eq("preserved").sum()),
                "clusters": int(g["dependence_id"].nunique()),
            })
            states = Counter()
            for _, programme in g[g["interaction_type"].eq("antagonist")].groupby("dependence_id"):
                valid = programme[programme["direction_comparable"].eq("yes")]
                if valid.empty:
                    continue
                retention = valid["transformation"].isin(RETAINING)
                state = ("all" if retention.all()
                         else "mixed" if retention.any() else "none")
                states[state] += 1
            ant_programmes.append({
                "scope": name,
                "reference": reference,
                "programmes": sum(states.values()),
                "all": states["all"],
                "mixed": states["mixed"],
                "none": states["none"],
            })
    return {
        "n_links": int(len(df)),
        "endpoint_counts": dict(Counter(df["endpoint_class"])),
        "summary": summary,
        "ant_programmes": ant_programmes,
    }


def render_endpoint_sensitivity(propagation: pd.DataFrame,
                                endpoints: pd.DataFrame) -> str:
    d = endpoint_sensitivity(propagation, endpoints)
    lines = [
        "# IWE propagation endpoint sensitivity",
        "",
        "_Generated from temporal_signal_components.csv and propagation_endpoint_audit.csv._",
        "",
        "## Endpoint types",
        "",
        "Mature seed/yield, intact post-cost fruits, terminal seedpod or gall fates, "
        "mature-seed damage, constructed reproductive potential and source-model "
        "fitness predictions are **different biological endpoints**, not exchangeable "
        "replicates of one fitness measurement.",
        "",
        "| Endpoint | Links |",
        "|---|---:|",
    ]
    lines += [f"| {k} | {v} |"
              for k,v in sorted(d["endpoint_counts"].items())]
    lines += [
        "",
        "## Retention under nested endpoint definitions",
        "",
        "Retained direction means preserved or preserved_net_changed_mechanism. "
        "Incomparable links never enter the direction denominator.",
        "",
        "| Scope | Reference | Links | Direction comparable | Direction retained | "
        "Exact preserved | Clusters |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in d["summary"]:
        lines.append(f"| {r['scope']} | {r['reference']} | {r['links']} | "
                     f"{r['comparable']} | {r['retained']} | "
                     f"{r['exact_preserved']} | {r['clusters']} |")
    lines += [
        "",
        "## Antagonist dependence-cluster sensitivity",
        "",
        "Repeated links within a dependence cluster are collapsed; no comparable "
        "link means no classification, not a failure.",
        "",
        "| Scope | Reference | Programmes | All retained | Mixed | None |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in d["ant_programmes"]:
        lines.append(f"| {r['scope']} | {r['reference']} | "
                     f"{r['programmes']} | {r['all']} | {r['mixed']} | {r['none']} |")
    lines += [
        "",
        "## Scope and interpretation",
        "",
        "- Terminal gall or mature-seedpod fate is informative, but is not an intact-seed count.",
        "- Seed number multiplied by germination is constructed reproductive potential, "
        "not observed offspring recruitment.",
        "- A predicted intact reproductive-unit value propagated through a source equation "
        "is not independently observed final fitness.",
        "- Percentage of mature seeds consumed measures a cost, not automatically net "
        "reproductive production per plant.",
        "- The original final-link denominator remains unchanged. These are nested "
        "descriptive sensitivity subsets, not post-hoc claims that a previously "
        "included study was scientifically invalid.",
        "- Timing provenance is confounded with biological system, study design and "
        "endpoint; these ratios cannot identify a causal stage effect or demonstrate "
        "out-of-sample predictive superiority.",
        "",
    ]
    return "\n".join(lines)
