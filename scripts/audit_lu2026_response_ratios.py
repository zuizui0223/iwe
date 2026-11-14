#!/usr/bin/env python3
"""Transform published, access-scoped ALAN responses without invented precision."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from iwe.alan_access_response_ratio import from_scoped_source

EXPECTED_SOURCE_BLOB = '73a04ebd962a3113ebfae410c1720468094ab60a'
DEFAULT = Path('data/registry/lu2026_access_scoped_contrasts_v01.csv')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=DEFAULT)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    raw=args.source.read_bytes()
    blob=hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
    if blob!=EXPECTED_SOURCE_BLOB:
        raise ValueError('Source scope table changed; review the primary publication before updating the pin')
    rows=list(csv.DictReader(raw.decode('utf-8').splitlines()))
    pairs,receipt=from_scoped_source(rows)
    receipt['input_git_blob_sha1']=blob
    receipt['input_sha256']=hashlib.sha256(raw).hexdigest()
    receipt['source_locator']='https://academic.oup.com/jpe/advance-article-pdf/doi/10.1093/jpe/rtag160/68754751/rtag160.pdf'
    receipt['source_scope']='accepted_manuscript_results_page14; source_percentages_only'
    receipt['figure_digitization_used']=False
    receipt['pdf_binary_sha256']=None
    receipt['supplement_TableS4b_retrieved']=False
    receipt['paired_results']=pairs
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    with (out/'access_matched_light_response_ratios.csv').open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(pairs[0]),lineterminator='\n');w.writeheader();w.writerows(pairs)
    (out/'access_response_ratio_receipt.json').write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
