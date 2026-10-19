"""Jadera 2025 independent mixed-partner source archive audit (read-only).

Uses the exact publicly archived Comerford et al. data, 2025 Dryad DOI
10.5061/dryad.2bvq83c2b. Source-original experiments on different
Sapindaceae host plants must NOT be merged into a fictitious single
flower-date × adult observation × viable-seed response.

No author contact. No unsupported numeric effect sizes, no strict-H1
promotion; bounded original field/survey/year/plant source evidence only.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from html import unescape
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

DOI="10.5061/dryad.2bvq83c2b"
ENCODED="doi%3A10.5061%2Fdryad.2bvq83c2b"
ROOT="https://datadryad.org/api/v2/datasets/"+ENCODED
META=ROOT
ZIP_URL=ROOT+"/download"
MAX_ARCHIVE=5_000_000
MAX_FILE=300_000
TARGET_NAMES=frozenset({
    "Cost_of_a_Pollinating_Seed_Predator_to_the_Host_Plant.zip",
    "Greennhouse_time.zip",
    "Pollination_Success_in_the_Field.zip",
    "Test_of_Pollination_Success_in_a_Greenhouse.zip",
    "README.md",
    "Dryad_New_Twist_Old_Story_Code.Rmd",
    "Read_Me_A_New_Twist_On_An_Old_Story.pdf",
})
KEYS=(
    "date","time","flower","seeds","seed","pollen","fruit","nymph",
    "treatment","viabil","pollin","jadera","adult","month","year",
    "cardiospermum","koelreuteria","sapind","census","sample",
)


def _allowed_url(url: str) -> bool:
    p=urlsplit(url)
    host=(p.hostname or "").lower()
    if p.scheme!="https":
        return False
    if host=="datadryad.org":
        return p.path.startswith("/api/v2/datasets/"+ENCODED)
    # Dryad's official public object downloads can redirect to its
    # cloud storage; never follow to arbitrary external providers.
    return (
        host.endswith(".s3.amazonaws.com") or
        host=="s3.amazonaws.com" or
        host=="storage.googleapis.com"
    )


def _source_get(url: str, maxbytes: int=MAX_ARCHIVE)->tuple[bytes,str]:
    if not _allowed_url(url):
        raise ValueError("off-Dryad source download URL")
    req=Request(url,headers={
        "Accept":"application/json,application/zip,*/*;q=0.1",
        "User-Agent":"IWE-original-source-audit/1.0"
    })
    with urlopen(req,timeout=45) as response:
        final=response.geturl()
        if not _allowed_url(final):
            raise ValueError("source redirected to non-Dryad object storage")
        payload=response.read(maxbytes+1)
    if len(payload)>maxbytes:
        raise ValueError("unexpectedly large original archive")
    return payload,final


def _safe_name(name: str)->bool:
    norm=name.replace("\\","/")
    return not (norm.startswith("/") or ".." in norm.split("/"))


def _parse_csv_field_info(raw: bytes, filename: str)->dict:
    sample=raw.decode("utf-8-sig",errors="replace")
    head=sample.splitlines()[:3]
    record={"name":filename,"original_bytes":len(raw),
            "original_sha256":hashlib.sha256(raw).hexdigest(),
            "header":[], "rows":None,"source_stage_field_hints":[]}
    try:
        reader=csv.reader(StringIO(sample,newline=""))
        header=next(reader,[])
        record["header"]=header[:150]
        record["rows"]=sum(1 for _ in reader)
    except csv.Error:
        record["status"]="csv_parse_ambiguous_no_row_count"
        record["header"]=next(csv.reader([head[0]]),[]) if head else []
    record["source_stage_field_hints"]=[
        col for col in record["header"]
        if any(k in col.lower() for k in KEYS)
    ][:80]
    return record


def _source_lines(raw: bytes, name: str, maxhits: int=38)->list[dict]:
    lines=raw.decode("utf-8-sig",errors="replace").splitlines()
    output=[]
    for n,line in enumerate(lines,1):
        strip=line.strip()
        if not strip or len(strip)>600:
            continue
        found=[k for k in KEYS if k in strip.lower()]
        if not found:
            continue
        output.append({"source_file":name,"line_number":n,
                       "source_text_short":strip[:210],
                       "matches":found})
        if len(output)>=maxhits:
            break
    return output


def _inspect_zip(raw: bytes, prefix: str, depth: int)->list[dict]:
    if depth>2: return [{"file":prefix,"status":"zip_depth_limit"}]
    try:
        z=ZipFile(BytesIO(raw))
    except BadZipFile as exc:
        raise ValueError("not a source-valid ZIP payload") from exc
    out=[]
    with z:
        files=[q for q in z.infolist() if not q.is_dir()]
        if len(files)>120:
            raise ValueError("unexpected archive members")
        for item in files:
            if not _safe_name(item.filename) or item.file_size>MAX_FILE:
                raise ValueError("source archive path or member exceeds safety cap")
            name=prefix+"::"+item.filename
            if item.filename.startswith("__MACOSX/") or "/._" in item.filename:
                continue
            chunk=z.read(item)
            ext=Path(item.filename).suffix.lower()
            if ext==".zip":
                out.extend(_inspect_zip(chunk,name,depth+1))
            elif ext in (".csv",".tsv"):
                out.append(_parse_csv_field_info(chunk,name))
            elif ext in (".md",".rmd",".txt",".r"):
                out.append({"name":name,"original_bytes":len(chunk),
                            "original_sha256":hashlib.sha256(chunk).hexdigest(),
                            "source_line_leads":_source_lines(chunk,name)})
            else:
                out.append({"name":name,"original_bytes":len(chunk),
                            "extension":ext,
                            "content_reviewed":False})
    return out


def source_inventory() -> dict:
    record={
        "schema":"iwe_jadera2025_dryad_original_source_inventory_v1",
        "source_doi":DOI,
        "source_url":"https://datadryad.org/dataset/doi%3A"+DOI,
        "original_life_cycle_class":"mixed_pollinating_seed_predator",
        "source_retrieved":False,
        "independent_adult_calendar_window_verified":False,
        "same_host_and_same_unit_pollination_to_intact_seed_verified":False,
        "strict_h1_admission":False,
        "observed_original_source_files":[],
    }
    try:
        metadata,_=_source_get(META,maxbytes=300_000)
        obj=json.loads(metadata.decode("utf-8"))
        record["original_title"]=obj.get("title","")
        record["original_identifier"]=obj.get("identifier","")
        version=obj.get("_links",{}).get("stash:version",{})
        record["original_version_locator"]=version.get("href")
        archive,final=_source_get(ZIP_URL)
        if not archive.startswith(b"PK"):
            raise ValueError("Dryad download not a ZIP archive")
        record["source_archive_sha256"]=hashlib.sha256(archive).hexdigest()
        record["source_zip_bytes"]=len(archive)
        record["source_retrieved"]=True
        results=_inspect_zip(archive,"dryad_package",0)
        record["observed_original_source_files"]=results
        record["number_source_components"]=len(results)
        record["source_target_names_present"]=[
            x for x in TARGET_NAMES
            if any(x.lower() in str(f.get("name","")).lower()
                   for f in results)
        ]
        # Original unit correspondence still needs a human-read
        # source dictionary and exact per-file plant/partner ID join.
        record["mixed_lifecycle_stage_benefit_and_cost_distinct"]=True
        record["status"]="source_original_archive_inventory_recovered"
    except (OSError,TimeoutError,ValueError,TypeError,
            json.JSONDecodeError,HTTPError,URLError) as exc:
        record["status"]="source_access_blocked"
        record["access_issue"]=str(type(exc).__name__)[:80]+":"+str(exc)[:170]
    return record


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    args=p.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    report=source_inventory()
    (args.outdir/"original_source_inventory.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    print("JADERA_PUBLIC_SOURCE",report["status"],report.get("access_issue",""))
    print("JADERA_TITLE",report.get("original_title"))
    print("JADERA_COMPONENTS",report.get("number_source_components"))
    for item in report["observed_original_source_files"]:
        print("ORIGINAL_COMPONENT",item.get("name"),
              "ROWS",item.get("rows"),
              "HEADER",item.get("header"),
              "STAGE",item.get("source_stage_field_hints"))
        for line in item.get("source_line_leads",[])[:35]:
            print("SOURCE_METHOD_LINE",line["source_file"],line["line_number"],
                  line["source_text_short"])
    print("H1 source adult timing or same-unit final seeds not verified")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
