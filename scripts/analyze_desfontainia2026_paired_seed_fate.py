"""Original paired-shrub Desfontainia robbing versus legitimate-pollination seed fate.

Valdivia & Orellana (2026), Ecology and Evolution,
DOI 10.1002/ece3.73933. Original open Zenodo DOI
10.5281/zenodo.18895003. Exact workbook MD5 verified
against original author archive. No raw workbook or
individual shrub-by-treatment rows redistributed.

Interpretation: 40 shrubs, three flower conditions observed per
shrub, NOT 120 independent plants. Two experimental controls
relate to pollinator access (bagged vs taped) and to
robber access conditional on pollinators (taped versus selected
already-perforated open flowers). Critically the latter contrast
has different selection/anthesis history, and is not a
randomized assignment of robbery to identical untreated flowers.

Estimate observed mean paired seed counts, seed production
probability, paired-bootstrap CIs, exact discordant-pair
binomial tests. No "non-significant" -> equivalent claim;
no inference to season-specific adult flight from iNaturalist
monthly robber observations. No new IWE strict H1 effect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from io import BytesIO
from math import comb, isfinite, sqrt
from pathlib import Path, PurePosixPath
from statistics import mean, median
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from scripts.probe_desfontainia2026_zenodo_source import (
    original_bytes, OOXML_NS, _secure_xlsx_zip, _cell_column,
    ORIGINAL_MD5, DOI,
)

SOURCE_SHEET="Seeds per pollination treatment"
EXPECTED_HEADERS=("Plant", "Seed (-P-R)", "Seeds (+P-R)", "Seeds (+P+R)")
NECTAR_SHEET="Nectar rewards"
N_SHRUBS=40
BOOTSTRAP_REPS=12000
SEED=20261026


def source_sheet_rows(raw:bytes, name:str):
    """Read an exact literal worksheet by original header, no silent joins."""
    with ZipFile(BytesIO(raw)) as z:
        infos=_secure_xlsx_zip(z)
        names={q.filename for q in infos}
        workbook=ET.fromstring(z.read("xl/workbook.xml"))
        relroot=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap={q.attrib.get("Id"):q.attrib.get("Target","")
                for q in relroot}
        key=None
        for s in workbook.findall(".//m:sheet",OOXML_NS):
            if s.attrib.get("name")==name:
                key=relmap.get(s.attrib.get("{"+OOXML_NS["r"]+"}id"))
        if key is None:
            raise ValueError("required original source sheet not found: "+name)
        sheet_path=key.lstrip("/")
        if not sheet_path.startswith("xl/"):
            sheet_path="xl/"+sheet_path
        if (sheet_path not in names or ".." in PurePosixPath(sheet_path).parts
                or not sheet_path.startswith("xl/worksheets/")):
            raise ValueError("untrusted biological stage sheet source")
        strings=[]
        if "xl/sharedStrings.xml" in names:
            shared=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in shared.findall("m:si",OOXML_NS):
                strings.append("".join(
                    x.text or "" for x in si.iter(
                        "{"+OOXML_NS["m"]+"}t")
                ))
        root=ET.fromstring(z.read(sheet_path))
        original=[]
        for source_row in root.findall(".//m:sheetData/m:row",OOXML_NS):
            cells={}
            for c in source_row.findall("m:c",OOXML_NS):
                column=_cell_column(c.attrib.get("r"))
                typ=c.attrib.get("t")
                v=c.find("m:v",OOXML_NS)
                if v is not None:
                    value=v.text or ""
                    if typ=="s":
                        idx=int(value)
                        if idx<0 or idx>=len(strings):
                            raise ValueError("untrusted shared string index")
                        value=strings[idx]
                else:
                    inline=c.find("m:is",OOXML_NS)
                    value="".join(x.text or "" for x in inline.iter(
                        "{"+OOXML_NS["m"]+"}t")
                    ) if inline is not None else ""
                if value.strip()!="":
                    if column in cells:
                        raise ValueError("duplicate source column in one row")
                    cells[column]=value.strip()
            if cells:
                original.append(cells)
        if not original:
            raise ValueError("empty original biological stage sheet")
        header=original.pop(0)
        if set(header)!={1,2,3,4} and name==SOURCE_SHEET:
            raise ValueError("unexpected extra original seed treatment header cells")
        columns={k:v for k,v in header.items()}
        if len(columns)!=len(set(columns.values())):
            raise ValueError("duplicate original source column name")
        rows=[]
        for source_row in original:
            rows.append({label:source_row.get(column)
                         for column,label in columns.items()})
        return list(columns.values()), rows


def _nonnegative_integer(v, label):
    if v is None or str(v).strip()=="":
        raise ValueError("original flower/seed outcome missing: "+label)
    try:
        value=float(v)
    except (TypeError,ValueError) as exc:
        raise ValueError("nonnumeric original seed count: "+label) from exc
    if not isfinite(value) or value<0 or int(value)!=value:
        raise ValueError("original mature seed count must be nonnegative integer")
    return int(value)


def paired_shrub_records(rows):
    if len(rows)!=N_SHRUBS:
        raise ValueError("expected exactly 40 original shrubs")
    if not rows or set(rows[0])!=set(EXPECTED_HEADERS):
        raise ValueError("source original treatment labels do not match")
    out=[]
    ids=set()
    for row in rows:
        sid=_nonnegative_integer(row["Plant"],"source shrub ID")
        if sid in ids:
            raise ValueError("duplicate original shrub ID")
        ids.add(sid)
        out.append({
            "plant":sid,
            "bagged":_nonnegative_integer(row["Seed (-P-R)"],"bagged"),
            "pollination_no_robbery":_nonnegative_integer(
                row["Seeds (+P-R)"],"pollination/no robbery"),
            "pollination_with_robbery":_nonnegative_integer(
                row["Seeds (+P+R)"],"pollination/robbery"),
        })
    if len(ids)!=N_SHRUBS:
        raise ValueError("incomplete independent original plant IDs")
    return sorted(out,key=lambda x:x["plant"])


def mean_difference(a,b):
    if not a or len(a)!=len(b):
        raise ValueError("paired source observations required")
    return mean(x-y for x,y in zip(a,b))


def bootstrap_difference(a,b,reps=BOOTSTRAP_REPS,seed=SEED):
    if reps<100:
        raise ValueError("insufficient bootstrap repetitions")
    n=len(a)
    if n!=len(b) or not n:
        raise ValueError("bootstrap requires observed paired shrubs")
    rng=random.Random(seed)
    sampled=[]
    for _ in range(reps):
        sample=[rng.randrange(n) for _ in range(n)]
        sampled.append(sum(a[i]-b[i] for i in sample)/n)
    sampled.sort()
    return [sampled[int(.025*(reps-1))],
            sampled[int(.975*(reps-1))]]


def paired_binary_discordance(a,b):
    if len(a)!=len(b):
        raise ValueError("binary treatment pairs unmatched")
    # a / b source counts -> a > 0 and b > 0 indicators.
    a_only=sum(x>0 and y==0 for x,y in zip(a,b))
    b_only=sum(y>0 and x==0 for x,y in zip(a,b))
    both=sum(x>0 and y>0 for x,y in zip(a,b))
    neither=sum(x==0 and y==0 for x,y in zip(a,b))
    discordant=a_only+b_only
    p=min(1.,2*sum(comb(discordant,k) for k in
                   range(min(a_only,b_only)+1))/2**discordant
          ) if discordant else 1.
    return {
        "only_first_positive":a_only,
        "only_second_positive":b_only,
        "both_positive":both,
        "both_zero":neither,
        "exact_two_sided_p_mcnemar":p,
        "test_description":"exact paired discordant sign, not equivalence test",
    }


def summarize_contrast(first,second):
    return {
        "paired_mean_seed_count_difference":
            mean_difference(first,second),
        "paired_mean_count_difference_95pct_bootstrap":
            bootstrap_difference(first,second),
        "mean_first":mean(first),"mean_second":mean(second),
        "median_first":median(first),"median_second":median(second),
        "p_seeds_first":mean(x>0 for x in first),
        "p_seeds_second":mean(x>0 for x in second),
        "paired_seed_presence_difference":
            mean((x>0)-(y>0) for x,y in zip(first,second)),
        "paired_seed_presence_95pct_bootstrap":bootstrap_difference(
            [int(x>0) for x in first],
            [int(y>0) for y in second]),
        "binary_discordance":paired_binary_discordance(first,second),
    }


def nectar_schema_statuses(rows):
    """Original nectar status must be read, not inferred from fruit treatment."""
    required={"Plant","Flower","Status",
              "Nectar volumen (microliter)",
              "Nectar concentration (% w/w)"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("source nectar column names unverified")
    plants={str(r["Plant"]) for r in rows}
    statuses=Counter(str(r["Status"]) for r in rows)
    return {
        "n_original_nectar_flower_measurements":len(rows),
        "n_original_nectar_shrub_IDs":len(plants),
        "source_literal_nectar_status_levels":dict(statuses),
        "nectar_and_seed_source_shrubs_linked_by_ID":False,
        "nectar_effect_computed":False,
    }


def _numeric_nectar(value):
    if value is None or str(value).strip().lower() in (
        "", "na", "nan", "null", "."
    ):
        return None
    try:
        x=float(value)
    except (TypeError,ValueError) as exc:
        raise ValueError("nonnumeric original nectar volume") from exc
    if not isfinite(x) or x<0:
        raise ValueError("negative or nonfinite original floral nectar")
    return x


def _ranks(a):
    """Average ranks for ties without a scientific software dependency."""
    n=len(a)
    out=[0.]*n
    for i,v in enumerate(a):
        less=sum(x<v for x in a)
        equal=sum(x==v for x in a)
        out[i]=less+(equal+1)/2
    return out


def spearman_paired_shrubs(x,y):
    if len(x)!=len(y) or len(x)<3:
        raise ValueError("paired shrub rank inputs required")
    a,b=_ranks(x),_ranks(y)
    am,bm=mean(a),mean(b)
    num=sum((v-am)*(w-bm) for v,w in zip(a,b))
    va=sum((v-am)**2 for v in a)
    vb=sum((v-bm)**2 for v in b)
    return num/sqrt(va*vb) if va>0 and vb>0 else None


def bootstrap_spearman_paired_shrubs(x,y,reps=4000,seed=SEED):
    """Paired-SHRUB bootstrap; never bootstrap the 400 nectar flowers as independent."""
    if len(x)!=len(y) or len(x)<4:
        raise ValueError("correlation requires matched independent shrubs")
    rng=random.Random(seed)
    n=len(x)
    values=[]
    for _ in range(reps):
        ids=[rng.randrange(n) for __ in range(n)]
        rho=spearman_paired_shrubs([x[i] for i in ids],[y[i] for i in ids])
        if rho is not None:
            values.append(rho)
    if len(values)<reps*.9:
        return {
            "valid_bootstrap_samples":len(values),
            "confidence_interval":None,
            "status":"insufficient_variation_in_resampled_shrubs",
        }
    values.sort()
    return {
        "valid_bootstrap_samples":len(values),
        "confidence_interval":[
            values[int(.025*(len(values)-1))],
            values[int(.975*(len(values)-1))]
        ],
        "status":"exploratory_paired_shrub_rank_uncertainty",
    }


def paired_nectar_volume(rows,paired_seed_rows):
    """The publication explicitly uses the same 40 SHRUBS for nectar/seed.

    Nectar flowers were removed for extraction, hence could NOT be the
    same tagged experimental flowers subsequently scored for seeds.
    The inter-sheet ID mapping is biological at shrub scale only.
    """
    expected_status={"Robada","No dañada"}
    shrub_ids={z["plant"] for z in paired_seed_rows}
    by=defaultdict(lambda:defaultdict(list))
    missing_volume=Counter()
    raw_status=Counter()
    original_shrub_status_rows=Counter()
    flower_ids=set()
    for r in rows:
        shrub=_nonnegative_integer(r.get("Plant"),"nectar source shrub ID")
        if shrub not in shrub_ids:
            raise ValueError("nectar observation references unknown seed shrub")
        status=str(r.get("Status","")).strip()
        raw_status[status]+=1
        if status not in expected_status:
            raise ValueError("unrecognized original Spanish floral status")
        flower_id=_nonnegative_integer(r.get("Flower"),"original nectar flower ID")
        if (shrub,flower_id) in flower_ids:
            raise ValueError("duplicate original nectar flower ID within shrub")
        flower_ids.add((shrub,flower_id))
        original_shrub_status_rows[(shrub,status)]+=1
        val=_numeric_nectar(r.get("Nectar volumen (microliter)"))
        if val is None:
            missing_volume[status]+=1
        else:
            by[shrub][status].append(val)
    if len(rows)!=400:
        raise ValueError("original nectar sample is not 400 flower rows")
    if set(by)!=shrub_ids:
        raise ValueError("not all shrub IDs have original nectar observations")
    if set(raw_status)!=expected_status or set(raw_status.values())!={200}:
        raise ValueError("unexpected 200 robbed / 200 healthy flowers")
    if any(original_shrub_status_rows[(shrub,status)] != 5
           for shrub in shrub_ids for status in expected_status):
        raise ValueError("original nectar design not 5 + 5 flowers per shrub")
    if len(flower_ids)!=400:
        raise ValueError("original nectar flower observations not unique")
    per_shrub=[]
    for shrub in sorted(shrub_ids):
        pierced=by[shrub]["Robada"]
        healthy=by[shrub]["No dañada"]
        if not pierced or not healthy:
            raise ValueError("no paired nectar statuses on a sampled shrub")
        per_shrub.append({
            "shrub":shrub,
            "mean_pierced":mean(pierced),
            "mean_healthy":mean(healthy),
            "n_pierced_measured":len(pierced),
            "n_healthy_measured":len(healthy),
        })
    robbed=[z["mean_pierced"] for z in per_shrub]
    healthy=[z["mean_healthy"] for z in per_shrub]
    healthy_mean=mean(healthy)
    robbed_mean=mean(robbed)
    seed_by_shrub={z["plant"]:z for z in paired_seed_rows}
    reduced_reward=[
        z["mean_healthy"]-z["mean_pierced"]
        for z in per_shrub
    ]
    seed_change=[
        seed_by_shrub[z["shrub"]]["pollination_with_robbery"]-
        seed_by_shrub[z["shrub"]]["pollination_no_robbery"]
        for z in per_shrub
    ]
    complete=[z for z in per_shrub
              if z["n_pierced_measured"]==5
              and z["n_healthy_measured"]==5]
    complete_depletion=[
        z["mean_healthy"]-z["mean_pierced"] for z in complete
    ]
    complete_seed_change=[
        seed_by_shrub[z["shrub"]]["pollination_with_robbery"]-
        seed_by_shrub[z["shrub"]]["pollination_no_robbery"]
        for z in complete
    ]
    return {
        "paired_shrubs_with_nectar_and_seed_outcomes":len(per_shrub),
        "original_flower_status_counts":dict(raw_status),
        "source_design_exactly_five_of_each_status_per_shrub":True,
        "n_shrubs_five_numeric_nectar_observations_in_both_statuses":
            len(complete),
        "source_same_focal_shrubs_used_for_nectar_and_seeds":
            True,  # Valdivia & Orellana 2026, Methods sections 2.3 / 2.5
        "source_same_tagged_flowers_for_nectar_and_seed_fates":False,
        "unrecorded_flower_nectar_volumes":dict(missing_volume),
        "n_pierced_with_numeric_nectar":sum(z["n_pierced_measured"]
                                           for z in per_shrub),
        "n_healthy_with_numeric_nectar":sum(z["n_healthy_measured"]
                                           for z in per_shrub),
        "mean_pierced_nectar_per_flower_uL":
            robbed_mean,
        "mean_healthy_nectar_per_flower_uL":
            healthy_mean,
        "healthy_divided_by_pierced_nectar_volume":
            healthy_mean/robbed_mean if robbed_mean>0 else None,
        "mean_pierced_minus_healthy_nectar_difference_uL":
            mean_difference(robbed,healthy),
        "paired_95pct_bootstrap_nectar_difference_uL":
            bootstrap_difference(robbed,healthy),
        "spearman_shrub_level_nectar_depletion_vs_seed_change":
            spearman_paired_shrubs(reduced_reward,seed_change),
        "exploratory_95pct_paired_shrub_bootstrap_spearman":
            bootstrap_spearman_paired_shrubs(reduced_reward,seed_change),
        "five_plus_five_complete_nectar_shrub_sensitivity":{
            "n_shrubs":len(complete),
            "spearman_nectar_depletion_vs_seed_difference":
                spearman_paired_shrubs(
                    complete_depletion,complete_seed_change
                ) if len(complete)>=3 else None,
            "correlation_not_identifiable_when_too_few":len(complete)<3,
        },
        "no_individual_flower_nectar_to_seed_fate_join":True,
        "observational_nectar_loss_seed_change_correlation_is_not_mediation":
            True,
    }


def run_original():
    original=original_bytes("Raw Data Desfontainia fulgens.xlsx")
    source_headers,seed_rows=source_sheet_rows(original,SOURCE_SHEET)
    if tuple(source_headers)!=EXPECTED_HEADERS:
        raise ValueError("author source seed treatment headers changed")
    source=paired_shrub_records(seed_rows)
    controls=[r["bagged"] for r in source]
    no_rob=[r["pollination_no_robbery"] for r in source]
    with_rob=[r["pollination_with_robbery"] for r in source]
    nectar_headers,nectar_rows=source_sheet_rows(original,NECTAR_SHEET)
    nectar=nectar_schema_statuses(nectar_rows)
    if nectar["n_original_nectar_shrub_IDs"]!=N_SHRUBS:
        raise ValueError("source nectar/shrub sampling count drift")
    paired_nectar=paired_nectar_volume(nectar_rows,source)
    report={
        "schema":"iwe_desfontainia2026_within_shrub_reproductive_buffer_v1",
        "source_doi":DOI,
        "source_workbook_md5":ORIGINAL_MD5[
            "Raw Data Desfontainia fulgens.xlsx"],
        "n_original_shrubs":N_SHRUBS,
        "n_original_seed_treatment_rows":len(seed_rows),
        "n_treatments_per_shrub":3,
        "source_seed_case_count_by_treatment":{
            "bagged_no_pollinators_no_robbers":sum(x>0 for x in controls),
            "pollinators_robbers_deterred":sum(x>0 for x in no_rob),
            "pollinators_robbers_allowed":sum(x>0 for x in with_rob),
        },
        "effects":{
            "pollinator_access_no_robbery_vs_bagged":
                summarize_contrast(no_rob,controls),
            "robber_allowed_vs_deterred_given_pollinator_access":
                summarize_contrast(with_rob,no_rob),
        },
        "original_nectar_status_inventory":nectar,
        "original_paired_nectar_depletion":paired_nectar,
        "claims": {
            "one_shrub_three_treatments_clustered":True,
            "paired_shrub_bootstrap_nonparametric_exploratory":True,
            "robbed_flower_preselected_naturally_perforated":True,
            "not_randomized_same_phenological_stage_robber_assignment":True,
            "no_null_effect_equivalence_inferred":True,
            "absolute_mature_seeds_not_total_viable_maternal_fitness":True,
            "no_independently_dated_adult_activity_for_tagged_flowers":True,
            "strict_h1_additional_effects":0,
        },
    }
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--outdir",type=Path,required=True)
    args=parser.parse_args()
    result=run_original()
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"paired_shrub_seed_contrasts.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print("DESFONTAINIA_PAIRED_SHRUB_RESULT",
          json.dumps(result,sort_keys=True,ensure_ascii=False)[:18000])
    print("Never infer exact no-effect of robber access from non-significant contrast")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
