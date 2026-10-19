"""Original Crone & Rapp 2025 maple masting source retrieval and grain screen.

Separate long-term whole-tree flowering and seeds (2011–2024) from
pollinator-exclusion experiments (2012–2017) and fruit/seed-filling
observations (2012–2014). Never project year totals onto a flower/date
fitness unit, nor pretend annual insect-predator abundance is known.

Official Zenodo DOI 10.5281/zenodo.15090572, author-deposited R
scripts and frozen CSV versions, read-only and no raw redistribution.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request,urlopen

RECORD="15090572"
DOI="10.5281/zenodo.15090572"
API="https://zenodo.org/api/records/"+RECORD
EXPECTED_NAMES={
    "HFmaple.flowering.qual.2011_2024.csv",
    "HFmaple.pollenexclusion.2012_2017.csv",
    "HFmaple.seedcounts.2011_2024.csv",
    "HFmaple.seedfilling.2012_2014.csv",
    "EOS only.R",
    "mast patterns only.R",
}
MAX_BYTES=100_000


def _allowed(url:str)->bool:
    p=urlsplit(url)
    return (p.scheme=="https" and p.hostname=="zenodo.org" and
            (p.path.startswith("/api/records/"+RECORD) or
             p.path.startswith("/records/"+RECORD+"/files/") or
             p.path.startswith("/api/files/")))


def _get(url:str)->bytes:
    if not _allowed(url):raise ValueError("off-record source reference")
    with urlopen(Request(url,headers={
        "User-Agent":"IWE-crone2025-original-data-source/1.0",
        "Accept":"text/csv,text/plain,application/json,*/*;q=0.1"
    }),timeout=40) as a:
        if not _allowed(a.geturl()):
            raise ValueError("source redirected off DOI's original Zenodo record")
        raw=a.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:
        raise ValueError("unexpectedly oversized original source component")
    return raw


def source_csv(raw:bytes,name:str)->dict:
    text=raw.decode("utf-8-sig",errors="replace")
    reader=csv.DictReader(StringIO(text,newline=""))
    headers=reader.fieldnames or []
    rows=list(reader)
    if not headers:raise ValueError("original CSV header absent")
    hints=[h for h in headers if any(
        k in h.lower() for k in (
            "tree","year","flower","seed","filled","predat",
            "bag","wind","insect","mast","treat","damage",
            "sex","date","count","pollin"
        )
    )]
    preview=[]
    for row in rows[:3]:
        preview.append({
            h: (str(row.get(h,""))[:25] if row.get(h) is not None else "")
            for h in headers[:18]
        })
    result={
        "source_file":name,
        "source_n_rows":len(rows),
        "source_headers":headers[:100],
        "biological_stage_column_candidates":hints[:90],
        "original_first_three_row_structure_only":preview,
        "exact_tree_year_join_verified":False,
        "source_raw_total_viable_seed_effect_inferred":False,
    }
    # These are counts of genuine date/year tokens, not assumed values.
    for col in headers:
        if col.lower() in {"year","yr"}:
            result["source_year_values"] = sorted(set(
                str(row.get(col,"")).strip() for row in rows
                if str(row.get(col,"")).strip()
            ))[:35]
    return result


def source_R_code(raw:bytes,name:str)->dict:
    lines=raw.decode("utf-8-sig",errors="replace").splitlines()
    match=re.compile(
        r"(?i)flower|predat|viab|seed|pollin|wind|insect|"
        r"female|male|samara|mast|bag|exclude|saturat"
    )
    matches=[]
    for i,line in enumerate(lines,1):
        if match.search(line):
            matches.append({
                "original_line":i,
                "short_source_expression":line.strip()[:155],
            })
        if len(matches)>=58:break
    return {"source_file":name,"source_R_lines":len(lines),
            "original_source_reanalysis_leads":matches,
            "real_biological_effect_recomputed":False}


def audit()->dict:
    manifest={
        "schema":"iwe_crone2025_acer_original_source_inventory_v1",
        "source_doi":DOI,
        "article_doi":"10.1002/ajb2.70046",
        "author_conclusions":{
            "mast_years_wind_pollination":"higher",
            "mast_years_predispersal_seed_predation":"lower",
            "mast_years_insect_pollination":"similar",
        },
        "experimental_time_scale":"interannual_masting_not_daily_adult_partner_activity",
        "independent_adult_pollinator_or_seed_predator_window_verified":False,
        "same_original_source_unit_net_final_seed_effect_verified":False,
        "strict_iwe_h1_admission":False,
        "source_retrieved":False,
        "original_files":[],
    }
    try:
        data=json.loads(_get(API))
        file_listing=data.get("files",{})
        entries=(file_listing.get("entries",file_listing)
                 if isinstance(file_listing,dict) else file_listing)
        if isinstance(entries,dict):
            files=list(entries.values())
        elif isinstance(entries,list):
            files=entries
        else:
            raise ValueError("source file metadata schema unresolved")
        named={i.get("key"):i for i in files}
        manifest["file_metadata_names"]=list(named)
        manifest["original_file_url_paths"]={
            key:urlsplit(item.get("links",{}).get("content","")).path[:180]
            for key,item in named.items()
        }
        if not EXPECTED_NAMES.issubset(named):
            raise ValueError("original file set is incomplete")
        original=[]
        for filename in sorted(EXPECTED_NAMES):
            item=named[filename]
            source_url=item.get("links",{}).get("content")
            raw=_get(source_url)
            md5=hashlib.md5(raw).hexdigest()
            reported=str(item.get("checksum","")).lower()
            if reported and reported not in ("md5:"+md5,md5):
                raise ValueError("original "+filename+" checksum mismatch")
            if filename.endswith(".csv"):
                rec=source_csv(raw,filename)
            else:
                rec=source_R_code(raw,filename)
            rec.update({"source_md5":md5,"reported_source_checksum":reported})
            original.append(rec)
        manifest["source_retrieved"]=True
        manifest["original_files"]=original
        manifest["status"]="original_file_schemas_verified"
    except (OSError,TimeoutError,ValueError,TypeError) as exc:
        manifest["status"]="original_source_access_blocked"
        manifest["source_error"]=type(exc).__name__+":"+str(exc)[:160]
    return manifest


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args()
    x.outdir.mkdir(parents=True,exist_ok=True)
    result=audit()
    (x.outdir/"source_original_file_fields.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8"
    )
    print("CRONE_ORIGINAL_SOURCE",result["status"],
          result.get("source_error",""))
    for row in result["original_files"]:
        print("SOURCE_MAPLE",row["source_file"],"ROWS",row.get("source_n_rows"),
              "HEADERS",row.get("source_headers"),
              "ORIGINAL_YEARS",row.get("source_year_values"))
        print("SOURCE_PREVIEW",row["source_file"],
              json.dumps(row.get("original_first_three_row_structure_only",[])))
        if "original_source_reanalysis_leads" in row:
            for lead in row["original_source_reanalysis_leads"][:30]:
                print("SOURCE_R_LINE",row["source_file"],
                      lead["original_line"],lead["short_source_expression"])
    print("Never promote annual masting as seasonal partner-adult synchrony")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
