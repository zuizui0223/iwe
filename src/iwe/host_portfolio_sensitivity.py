"""Three observed-egg candidate species as counterfactual potential host resources.

Egg receipt is not verification of larval survival, host suitability, or
butterfly occupancy. None of the calculations changes IWE strict H1.
"""
from __future__ import annotations

from itertools import combinations
import math
import pandas as pd

CANDIDATES = ("Arabis hirsuta", "Arabidopsis thaliana", "Noccaea caerulescens")
PRESENCE_COLUMNS = {
    "accepted_plant_name_id", "accepted_name", "source_role",
    "area_code_l3", "native_present", "contemporary_present",
}
FROZEN_COLUMNS = {
    "accepted_plant_name_id", "accepted_name", "native_host_units",
    "contemporary_host_units",
}
NEW_ROLE = "observed_egg_candidate_not_confirmed_larval_viability"


def _bool(series: pd.Series, label: str) -> pd.Series:
    s = series.astype("string").str.strip().str.lower()
    if s.isna().any() or not s.isin(["true", "false"]).all():
        raise ValueError(f"{label} must have explicit true/false")
    return s.eq("true")


def _counts(series: pd.Series, label: str) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.isna().any() or (s < 0).any() or (s % 1 != 0).any():
        raise ValueError(f"{label}: nonnegative integer expected")
    return s.astype("int64")


def build_portfolio_sensitivity(
    regional: pd.DataFrame,
    frozen: pd.DataFrame,
    *,
    baseline_counts: tuple[int, int, int] = (162, 272, 110),
    frozen_n: int = 11,
    candidate_names: tuple[str, ...] = CANDIDATES,
    reference_added_regions: set[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    if not PRESENCE_COLUMNS <= set(regional):
        raise ValueError("missing WCVP regional presence columns")
    if not FROZEN_COLUMNS <= set(frozen):
        raise ValueError("missing frozen source host columns")
    d = regional.copy().fillna("")
    for col in ("accepted_plant_name_id", "accepted_name", "source_role", "area_code_l3"):
        d[col] = d[col].astype(str).str.strip()
        if d[col].eq("").any():
            raise ValueError(f"blank or null {col}")
    if d.duplicated(["accepted_plant_name_id", "area_code_l3"]).any():
        raise ValueError("duplicate plant ID and region")
    if not d["source_role"].isin(["frozen_host", NEW_ROLE]).all():
        raise ValueError("unrecognized host source role")
    d["native_present"] = _bool(d["native_present"], "native_present")
    d["contemporary_present"] = _bool(d["contemporary_present"], "contemporary_present")
    if (~d["contemporary_present"]).any():
        raise ValueError("regional table must be contemporary-only rows")
    taxa = d[["accepted_plant_name_id", "accepted_name", "source_role"]].drop_duplicates()
    if taxa["accepted_plant_name_id"].duplicated().any() or taxa["accepted_name"].duplicated().any():
        raise ValueError("nonunique accepted source taxon IDs or names")

    base = frozen.copy()
    for col in ("accepted_plant_name_id", "accepted_name"):
        base[col] = base[col].astype(str).str.strip()
    if len(base) != frozen_n or base["accepted_plant_name_id"].duplicated().any():
        raise ValueError("frozen source host count/identities drift")
    base["native_host_units"] = _counts(base["native_host_units"], "frozen native")
    base["contemporary_host_units"] = _counts(base["contemporary_host_units"], "frozen contemporary")
    base_ids = set(base["accepted_plant_name_id"])
    if not base_ids <= set(taxa["accepted_plant_name_id"]):
        raise ValueError("frozen host ID missing from WCVP reconstruction")
    for _, row in base.iterrows():
        host = d.loc[d["accepted_plant_name_id"] == row["accepted_plant_name_id"]]
        if (len(host) != row["contemporary_host_units"]
                or int(host["native_present"].sum()) != row["native_host_units"]
                or host.iloc[0]["accepted_name"] != row["accepted_name"]
                or host.iloc[0]["source_role"] != "frozen_host"):
            raise ValueError(f"frozen host WCVP source drift: {row['accepted_name']}")

    added = taxa.loc[taxa["source_role"] == NEW_ROLE]
    if len(added) != len(candidate_names) or set(added["accepted_name"]) != set(candidate_names):
        raise ValueError("observed-egg candidate name resolution incomplete or unexpected")
    candidates = dict(zip(added["accepted_name"], added["accepted_plant_name_id"]))
    if base_ids & set(candidates.values()):
        raise ValueError("candidate ID already in frozen host portfolio")
    nat = {}
    contemp = {}
    for ident, part in d.groupby("accepted_plant_name_id"):
        nat[ident] = set(part.loc[part["native_present"], "area_code_l3"])
        contemp[ident] = set(part["area_code_l3"])

    def union(ids: set[str]) -> tuple[set[str], set[str], set[str]]:
        native = set().union(*(nat[i] for i in ids))
        current = set().union(*(contemp[i] for i in ids))
        if not native <= current:
            raise ValueError("portfolio native range not included in current range")
        return native, current, current - native

    bn, bc, be = union(base_ids)
    if (len(bn), len(bc), len(be)) != baseline_counts:
        raise ValueError("frozen whole-butterfly 162/272/110 baseline drift")
    if reference_added_regions is not None and be != reference_added_regions:
        raise ValueError("frozen original 110 region codes do not match source reconstruction")

    reports: list[dict] = []
    transitions: list[dict] = []
    for k in range(len(candidate_names) + 1):
        for choice in combinations(candidate_names, k):
            scenario = "frozen_11" if k == 0 else "frozen_11_plus_" + "__".join(choice)
            ids = base_ids | {candidates[c] for c in choice}
            native, current, new = union(ids)
            retained = be & new
            lost = be - new
            gained = new - be
            if len(retained) + len(lost) != len(be) or len(retained) + len(gained) != len(new):
                raise ValueError("region transition accounting does not reconcile")
            reports.append({
                "scenario": scenario,
                "candidate_count": k,
                "added_candidate_species": ";".join(choice),
                "host_count": len(ids),
                "native_units": len(native),
                "contemporary_units": len(current),
                "introduced_added_units": len(new),
                "delta_native_vs_frozen": len(native) - len(bn),
                "delta_contemporary_vs_frozen": len(current) - len(bc),
                "delta_added_vs_frozen": len(new) - len(be),
                "baseline_added_retained": len(retained),
                "baseline_added_now_native": len(lost),
                "newly_added_after_host_extension": len(gained),
                "contemporary_over_native_ratio": len(current)/len(native) if native else float("nan"),
                "biological_basis": "egg_receipt_only_larval_suitability_unverified",
                "strict_h1_effects_created": 0,
            })
            for region in sorted(be | new):
                status = (
                    "retained_added" if region in retained else
                    "old_added_now_native" if region in lost else
                    "new_added_after_host_extension" if region in gained else
                    "invalid"
                )
                if status == "invalid":
                    raise ValueError("invalid region state")
                transitions.append({
                    "scenario": scenario, "area_code_l3": region,
                    "previously_added": region in be,
                    "scenario_added": region in new,
                    "transition": status,
                })
    output = pd.DataFrame(reports)
    if len(output) != 2 ** len(candidate_names):
        raise ValueError("not all taxon subsets evaluated")
    fully_added = output.loc[output["candidate_count"] == len(candidate_names)]
    if len(fully_added) != 1:
        raise ValueError("full candidate scenario missing")
    result = {
        "schema": "iwe_chocho_host_extension_v0.1",
        "frozen_original_host_count": frozen_n,
        "frozen_baseline": {"native": len(bn), "contemporary": len(bc), "added": len(be)},
        "taxon_candidates_from_observed_eggs": list(candidate_names),
        "scenarios_tested": len(output),
        "all_candidates": fully_added.iloc[0].to_dict(),
        "egg_receipt_confirms_larval_suitability": False,
        "octoploid_cardamine_added_as_new_species": False,
        "observed_host_use_time_window_validated": False,
        "causal_colonization_effect_identified": False,
        "new_iwe_strict_h1_effects": 0,
        "chocho_frozen_paper_modified": False,
    }
    return output, pd.DataFrame(transitions), result
