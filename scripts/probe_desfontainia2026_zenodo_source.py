"""Original-data gate for Desfontainia nectar robbery and seed production.

Valdivia & Orellana (2026), Ecology and Evolution 16 e73933,
doi:10.1002/ece3.73933.
Frozen open source DOI:10.5281/zenodo.18895003.

Original field design describes one controlled flowering/pollination
treatment each (bagged/no pollination, pollination/robber exclusion,
pollination/robbing permitted) in each of 40 individual shrubs.
Before any source effect: pin the exact workbook and author R-script
MD5 and verify *original individual shrub and flower-treatment keys*.

No source can transform same-shrub three treatments into 120
independent shrubs, and no observational monthly robbery abundance
is an individual flower's randomized exposure. Null post-hoc
significance is NOT proof of equivalence/no robbery costs.

Read XLSX OOXML metadata read-only via standard library; no source
data, XLSX workbook, or font exported or committed to GitHub.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from io import BytesIO
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from zipfile import ZipFile, BadZipFile

RECORD="18895003"
DOI="10.5281/zenodo.18895003"
ARTICLE_DOI="10.1002/ece3.73933"
ORIGINAL_MD5={
    "Raw Data Desfontainia fulgens.xlsx":"e7e59a06cc3eb7aed636620a85a1ea98",
    "analysis_desfontainia_fulgens.R":"9fd405c399ecad9c3fe54d1cd70b21c0",
    "README.md":"26430e11763882fa47e6025eb77f1d58",
}
URL_ROOT="https://zenodo.org/records/"+RECORD+"/files/"
OOXML_NS={
    "m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr":"http://schemas.openxmlformats.org/package/2006/relationships",
}
MAX_ORIGINAL_BYTES=1_200_000
MAX_ZIP_MEMBERS=180
MAX_ZIP_EXPANDED_BYTES=30_000_000
MAX_SHEET_ROWS=350_000
STAGE_LEADS=(
    "seed","fruit","reprod","pollin","rob","nectar","volume",
    "flower","plant","shrub","treat","site","visit","bee","bird",
    "year","date","time","block","ID","perfor","sugar","month"
)


def original_url(name: str)->str:
    if name not in ORIGINAL_MD5:
        raise ValueError("file absent from frozen original DOI manifest")
    return URL_ROOT+quote(name,safe="")+"?download=1"


def original_bytes(name: str)->bytes:
    with urlopen(Request(original_url(name),headers={
        "User-Agent":"IWE-original-desfontainia-ecology-audit/1.0",
        "Accept":"application/octet-stream,text/plain,*/*"
    }),timeout=50) as r:
        raw=r.read(MAX_ORIGINAL_BYTES+1)
    if len(raw)>MAX_ORIGINAL_BYTES:
        raise ValueError("original source exceeds expected cap")
    if hashlib.md5(raw).hexdigest()!=ORIGINAL_MD5[name]:
        raise ValueError("frozen original source MD5 mismatch: "+name)
    return raw


def _secure_xlsx_zip(z:ZipFile):
    infos=z.infolist()
    if not infos or len(infos)>MAX_ZIP_MEMBERS:
        raise ValueError("unexpected workbook ZIP manifest size")
    total=0
    for info in infos:
        p=PurePosixPath(info.filename)
        if p.is_absolute() or ".." in p.parts or "\\" in info.filename:
            raise ValueError("unsafe OOXML ZIP entry")
        total+=info.file_size
        if total>MAX_ZIP_EXPANDED_BYTES:
            raise ValueError("OOXML expansion exceeds bound")
    return infos


def _cell_column(reference):
    m=re.match(r"^([A-Z]+)[0-9]+$",str(reference))
    if m is None:
        raise ValueError("invalid OOXML cell reference")
    idx=0
    for c in m.group(1):
        idx=idx*26+ord(c)-64
    return idx


def workbook_inventory(raw:bytes)->dict:
    with ZipFile(BytesIO(raw)) as z:
        infos=_secure_xlsx_zip(z)
        names={i.filename for i in infos}
        for key in ("xl/workbook.xml","xl/_rels/workbook.xml.rels"):
            if key not in names:
                raise ValueError("missing XLSX workbook structure: "+key)
        root=ET.fromstring(z.read("xl/workbook.xml"))
        relroot=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap={rel.attrib.get("Id"):rel.attrib.get("Target","")
                for rel in relroot}
        strings=[]
        if "xl/sharedStrings.xml" in names:
            root_strings=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root_strings.findall("m:si",OOXML_NS):
                strings.append("".join(
                    n.text or "" for n in si.iter(
                        "{"+OOXML_NS["m"]+"}t"
                    )
                ))
        data=[]
        for sh in root.findall(".//m:sheet",OOXML_NS):
            sheet=sh.attrib.get("name")
            relationship=sh.attrib.get("{"+OOXML_NS["r"]+"}id")
            target=relmap.get(relationship,"")
            normalized=target.lstrip("/")
            if not normalized.startswith("xl/"):
                normalized="xl/"+normalized
            parts=PurePosixPath(normalized).parts
            if (".." in parts or normalized not in names
                    or not normalized.startswith("xl/worksheets/")):
                raise ValueError("untrusted original sheet source path: "+target)
            xml=ET.fromstring(z.read(normalized))
            excel_rows=xml.findall(".//m:sheetData/m:row",OOXML_NS)
            if len(excel_rows)>MAX_SHEET_ROWS:
                raise ValueError("implausible source observation volume")
            source_rows=[]
            count=0
            allcol=set()
            for row in excel_rows:
                filled=[]
                for c in row.findall("m:c",OOXML_NS):
                    col=_cell_column(c.attrib.get("r"))
                    typ=c.attrib.get("t")
                    v=c.find("m:v",OOXML_NS)
                    if v is not None:
                        value=v.text or ""
                        if typ=="s":
                            n=int(value)
                            if n>=len(strings):
                                raise ValueError("source sharedStrings index invalid")
                            value=strings[n]
                    else:
                        inline=c.find("m:is",OOXML_NS)
                        value="".join(
                            t.text or "" for t in inline.iter(
                                "{"+OOXML_NS["m"]+"}t"
                            )
                        ) if inline is not None else ""
                    if value!="":
                        filled.append((col,str(value).strip()))
                        allcol.add(col)
                if not filled:
                    continue
                count+=1
                if len(source_rows)<5:
                    source_rows.append(filled)
            headers=[v for _,v in source_rows[0]] if source_rows else []
            hints=[v for v in headers if any(
                k.lower() in v.lower() for k in STAGE_LEADS
            )]
            data.append({
                "sheet":sheet,
                "n_nonempty_excel_rows":count,
                "n_observed_columns":len(allcol),
                "header_candidates_first_nonempty_row":headers[:35],
                "source_stage_header_hints":hints,
                "initial_five_row_shapes":[
                    {"excel_columns":[k for k,_ in q],
                     "values_first_12":[v[:80] for _,v in q[:12]]}
                    for q in source_rows
                ],
                "source_shrub_treatment_join_verified":False,
                "effect_estimated":False,
            })
        if not data:
            raise ValueError("no original source worksheets")
        return {
            "source_workbook_md5":ORIGINAL_MD5[
                "Raw Data Desfontainia fulgens.xlsx"],
            "n_original_sheets":len(data),
            "sheets":data,
            "original_raw_file_archived_only":True,
            "paired_shrub_reproduction_effect_admitted":False,
        }


def script_hints(raw:bytes)->dict:
    lines=raw.decode("utf-8-sig").splitlines()
    patterns=("read_excel","read.xlsx","readxl","names(",
              "sheet=","seed","pollination","Rob","robbery",
              "hurdle","gee(","negbin","glmmTMB")
    hit=[{"line":i+1,"source_code_snippet":ln.strip()[:175]}
         for i,ln in enumerate(lines)
         if any(p.lower() in ln.lower() for p in patterns)]
    return {"n_lines":len(lines),"source_code_leads":hit[:115]}


def audit():
    result={
        "schema":"iwe_desfontainia2026_source_original_workbook_gate_v1",
        "source_doi":DOI,
        "paper_doi":ARTICLE_DOI,
        "experimental_shrub_sample_size_in_paper":40,
        "experimental_flower_treatments_in_paper":3,
        "source_verified":False,
        "original_paired_shrub_rows_verified":False,
        "source_effect_estimated":False,
        "strict_H1_effect_admitted":False,
    }
    try:
        wb=original_bytes("Raw Data Desfontainia fulgens.xlsx")
        code=original_bytes("analysis_desfontainia_fulgens.R")
        readme=original_bytes("README.md")
        result["source_workbook_profile"]=workbook_inventory(wb)
        result["source_analysis_script"]=script_hints(code)
        result["readme_n_lines"]=len(readme.decode("utf-8-sig").splitlines())
        result["source_verified"]=True
        result["status"]="exact_original_workbook_sheets_recovered_join_unresolved"
    except (OSError,TimeoutError,ValueError,BadZipFile,UnicodeError,ET.ParseError) as exc:
        result["status"]="original_source_access_or_integrity_blocked"
        result["source_error"]=type(exc).__name__+":"+str(exc)[:210]
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",type=Path,required=True)
    a=ap.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    result=audit()
    (a.outdir/"original_source_sheet_inventory.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",
        encoding="utf-8"
    )
    print("DESFONTAINIA_SOURCE_STATUS",result["status"],
          result.get("source_error",""))
    if result.get("source_verified"):
        print("DESFONTAINIA_ORIGINAL_SHEETS",json.dumps(
            result["source_workbook_profile"],ensure_ascii=False)[:40000])
        print("DESFONTAINIA_ORIGINAL_METHOD_HINTS",json.dumps(
            result["source_analysis_script"],ensure_ascii=False)[:12000])
    print("Source workbook sheet metadata is not an admitted individual-shrub effect")
    return 0 if result["source_verified"] else 2


if __name__=="__main__":
    raise SystemExit(main())
