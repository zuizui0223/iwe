"""Original 2022 warming source-grain and phenotype allocation audit.

Designed specifically to detect false joining of six-seed species×arena
germination trials to 208 sampled-fruit flower IDs. Requires exact original
MD5 and R-export index before examining any ecological contrasts.

All values are original-source-only; output is aggregated group counts and
integrity checks. No effect is fitted or marked strict IWE H1.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from io import BytesIO, StringIO
import json
from math import isfinite
from pathlib import Path
from zipfile import ZipFile

from scripts.probe_demanincor2022_stage_zip import fetch_original


NAMES = (
    "data_seeds_germ_pSEM.txt", "data_bee_nest_pSEM.txt",
    "bee_abund_2022.txt", "flwrcount_temp2022.txt",
)


def original_table(z: ZipFile, name: str) -> list[dict[str, str]]:
    if name not in NAMES:
        raise ValueError("unregistered source dataset")
    inf = z.getinfo(name)
    if inf.file_size > 1_000_000:
        raise ValueError("source table unexpectedly large")
    raw = z.read(inf).decode("utf-8-sig")
    r = csv.reader(StringIO(raw), delimiter="\t")
    h = next(r, [])
    if not h or len(h) != len(set(h)):
        raise ValueError("source header missing/duplicate")
    values = [row for row in r if any(x.strip() for x in row)]
    if not values:
        raise ValueError("empty source table")
    # R row.names=TRUE: exact unheaded index 1..n only, never guess shifts.
    if (all(len(row) == len(h)+1 for row in values)
            and all(row[0].strip() == str(i)
                    for i, row in enumerate(values, 1))):
        values = [row[1:] for row in values]
    elif not all(len(row) == len(h) for row in values):
        raise ValueError("original source columns not aligned")
    return [dict(zip(h, row)) for row in values]


def numeric(row: dict, key: str, allow_na: bool = False):
    val = str(row.get(key, "")).strip()
    if val.lower() in ("na", "nan", "null", ""):
        if allow_na:
            return None
        raise ValueError("required source value missing: " + key)
    try:
        out = float(val)
    except ValueError as exc:
        raise ValueError("not numeric source " + key) from exc
    if not isfinite(out):
        raise ValueError("infinite source numeric")
    return out


def _group_key(row: dict) -> tuple[str, str, str]:
    return tuple(row[k] for k in ("trtmt", "arena", "sp"))


def _constant_report(groups: dict, col: str) -> dict:
    group_ns = {k: len({v[col] for v in rows})
                for k, rows in groups.items()}
    variable = {"/".join(k): n
                for k, n in group_ns.items() if n != 1}
    return {
        "n_groups": len(groups),
        "groups_with_repeated_identical_value": sum(
            len(groups[k]) > 1 and group_ns[k] == 1
            for k in groups
        ),
        "groups_with_multiple_values": len(variable),
        "variable_group_examples": dict(list(variable.items())[:8]),
        "n_source_rows_repeated_on_same_group_value": sum(
            len(groups[k])-1 for k in groups if group_ns[k] == 1
        ),
    }


def audit_source_tables(d: dict[str, list[dict]]) -> dict:
    stage = d["data_seeds_germ_pSEM.txt"]
    bee_fitness = d["data_bee_nest_pSEM.txt"]
    daily_bee = d["bee_abund_2022.txt"]
    daily_flower = d["flwrcount_temp2022.txt"]
    required = ("trtmt","arena","sp","plant_flwr_ID",
                "seeds","ovules","ovules_tot","seed_set",
                "seeds_sown","germ","germ_prop","cotyl","cotyl_prop")
    for r in stage:
        if any(k not in r for k in required):
            raise ValueError("missing source fate field")
    if len(stage) != 208 or len(bee_fitness) != 208:
        raise ValueError("unexpected original source row counts")

    groups = defaultdict(list)
    source_ids = set()
    maternal_keys = set()
    orphan_source_ids = []
    wrong_ovule_closure = set()
    wrong_seed_fraction = set()
    seed_above_ovule_total = set()
    mismatches_by_species = Counter()
    mismatches_by_treatment = Counter()
    wrong_germ_closure = []
    wrong_cotyl_closure = []
    germ_after_cotyl = []
    for r in stage:
        key = _group_key(r)
        source_id = (*key, r["plant_flwr_ID"])
        if source_id in source_ids:
            raise ValueError("original tagged source ID duplicate")
        source_ids.add(source_id)
        groups[key].append(r)
        parent_id = r["plant_flwr_ID"].rsplit("_", 1)[0]
        maternal_keys.add((*key, parent_id))
        seeds = numeric(r, "seeds")
        undeveloped = numeric(r, "ovules")
        total = numeric(r, "ovules_tot")
        seedprop = numeric(r, "seed_set")
        if abs((seeds+undeveloped)-total) > 1e-6:
            wrong_ovule_closure.add(source_id)
        if total > 0 and abs(seedprop-seeds/total) > 1e-5:
            wrong_seed_fraction.add(source_id)
        if seeds > total:
            seed_above_ovule_total.add(source_id)
        if (source_id in wrong_ovule_closure
                or source_id in wrong_seed_fraction):
            mismatches_by_species[key[2]] += 1
            mismatches_by_treatment[key[0]] += 1
        sown = numeric(r, "seeds_sown")
        germ = numeric(r, "germ")
        cotyl = numeric(r, "cotyl")
        if germ > sown or cotyl > germ:
            germ_after_cotyl.append(source_id)
        if sown > 0 and abs(numeric(r,"germ_prop")-germ/sown)>1e-6:
            wrong_germ_closure.append(source_id)
        if sown > 0 and abs(numeric(r,"cotyl_prop")-cotyl/sown)>1e-6:
            wrong_cotyl_closure.append(source_id)

    bee_id = {(*_group_key(r),r["plant_flwr_ID"]) for r in bee_fitness}
    nest_summary = {
        "id_sets_identical": bee_id == source_ids,
        "n_original_source_rows": len(bee_fitness),
    }
    for col in ("nests", "cells", "cocoons", "bee_abund"):
        if col in bee_fitness[0]:
            by = defaultdict(list)
            for r in bee_fitness:
                by[_group_key(r)].append(r)
            nest_summary[col] = _constant_report(by, col)

    daily_keys = set()
    actual_days = defaultdict(set)
    for r in daily_bee:
        k = (r["trtmt"], r["arena"], int(numeric(r,"DOY")))
        if k in daily_keys:
            raise ValueError("duplicate independent bee source day")
        daily_keys.add(k)
        actual_days[k[:2]].add(k[2])
    flower_keys = set()
    daily_coverage = defaultdict(lambda: {"n_date_observations":0,
                                          "n_bee_date_matched":0,
                                          "observed_flower_count":0.0,
                                          "matched_flower_count":0.0})
    nonpositive_blooms = 0
    group2 = set(groups)
    flower_groups = set()
    for r in daily_flower:
        tag = r["trtmt_arena"]
        if "_" not in tag:
            raise ValueError("unrecognized original flower arena key")
        treatment,arena = tag.rsplit("_",1)
        if arena == "TR":
            continue  # source's artificial treatment aggregate
        k=(treatment,arena,r["species"])
        day=int(numeric(r,"DOY"))
        row_key=(*k,day)
        if row_key in flower_keys:
            raise ValueError("duplicate flower calendar group-date")
        flower_keys.add(row_key)
        flower_groups.add(k)
        blooms=numeric(r,"flwr_count")
        if blooms<0:
            raise ValueError("negative source flowers")
        if blooms==0:
            nonpositive_blooms+=1
        q=daily_coverage[k]
        q["n_date_observations"]+=1
        q["observed_flower_count"]+=blooms
        if day in actual_days[(treatment,arena)]:
            q["n_bee_date_matched"]+=1
            q["matched_flower_count"]+=blooms
    matches=group2.intersection(flower_groups)
    coverage=[
        q["matched_flower_count"]/q["observed_flower_count"]
        for k,q in daily_coverage.items()
        if k in matches and q["observed_flower_count"]>0
    ]
    key_types=Counter(k[0] for k in groups)
    mean=lambda z: sum(z)/len(z) if z else None
    duplicates=len(stage)-len(groups)
    return {
        "source_doi": "10.5281/zenodo.17830772",
        "status": "source_units_adjudicated_no_new_timing_fitness_effect",
        "n_original_sampled_fruit_or_flower_rows": len(stage),
        "n_source_treatment_arena_species_groups": len(groups),
        "original_treatment_levels": dict(key_types),
        "n_plant_prefix_group_keys": len(maternal_keys),
        "n_repeated_fruit_rows_beyond_species_arena": duplicates,
        "group_size_histogram": dict(Counter(len(v) for v in groups.values())),
        "original_2022_seedling_trial_unit": "six_seeds_per_treatment_arena_species_if_source_constancy_holds",
        "seed_and_seedling_grouping": {
            col: _constant_report(groups, col)
            for col in ("seeds_sown","germ","cotyl","germ_prop","cotyl_prop")
        },
        "fatal_sown_germ_cotyl_order_violations": len(germ_after_cotyl),
        "source_seed_arithmetic_audit": {
            "n_fruit_rows_sum_seed_plus_undeveloped_not_total":
                len(wrong_ovule_closure),
            "n_fruit_rows_seed_fraction_not_seeds_divided_by_total":
                len(wrong_seed_fraction),
            "n_fruit_rows_seeds_exceed_total_ovules":
                len(seed_above_ovule_total),
            "n_distinct_original_fruits_with_either_arithmetic_flag":
                len(wrong_ovule_closure | wrong_seed_fraction),
            "flagged_by_species": dict(mismatches_by_species),
            "flagged_by_room": dict(mismatches_by_treatment),
            "unresolved_fruit_rows_not_admitted_to_seeds_from_ovules_model":
                True,
        },
        "n_unique_original_germination_seeds_sown": sum(
            numeric(v[0], "seeds_sown") for v in groups.values()
        ),
        "germ_fraction_arithmetic_violations": len(wrong_germ_closure),
        "cotyl_fraction_arithmetic_violations": len(wrong_cotyl_closure),
        "same_ids_in_bee_nest_psem": nest_summary,
        "daily_bee_source_rows": len(daily_bee),
        "n_original_independent_arena_units": len(actual_days),
        "n_original_bee_census_arena_days": len(daily_keys),
        "n_original_arena_species_flowering_groups": len(flower_groups),
        "n_fruit_groups_matching_flower_time_group": len(matches),
        "n_fruit_groups_without_independent_flowering_group":
            len(group2-flower_groups),
        "n_groups_with_nonzero_observed_blooms_and_overlap_days":len(coverage),
        "mean_observed_flower_coverage_on_bee_census_days": mean(coverage),
        "observed_flower_coverage_min_max": [
            min(coverage),max(coverage)
        ] if coverage else None,
        "n_nonflower_source_rows":nonpositive_blooms,
        "temperature_room_is_biological_randomization_unit": True,
        "one_room_per_temperature_level_no_independent_temperature_reps": True,
        "germination_mother_id_link_verified": False,
        "each_2022_row_not_independent_germination_replicate": True,
        "strict_H1_effect_added": False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    args=parser.parse_args()
    with ZipFile(BytesIO(fetch_original(
        "deManincor-et-al.2025_data_pSEM.zip"
    ))) as archive:
        rows={name:original_table(archive,name) for name in NAMES}
    report=audit_source_tables(rows)
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"same_unit_quality_gate.json").write_text(
        json.dumps(report,indent=2)+"\n",encoding="utf-8"
    )
    print("DEMANINCOR2022_UNIT_GATE",
          json.dumps(report,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
