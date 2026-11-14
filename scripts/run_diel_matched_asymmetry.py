#!/usr/bin/env python3
"""Source-pinned matched reproductive access comparison; aggregate-only exports."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from iwe.diel_matched_asymmetry import extract_matched, analyse_matched


def clean(obj):
    if isinstance(obj,dict):return {str(k):clean(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [clean(x) for x in obj]
    if isinstance(obj,np.generic):return clean(obj.item())
    if isinstance(obj,float) and not np.isfinite(obj):return None
    return obj


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--traits',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--bootstrap',type=int,default=10000)
    a=ap.parse_args()
    if a.bootstrap<1000:ap.error('At least 1000 study-bootstrap draws are required')
    f,source=extract_matched(a.author,a.traits)
    models,coverage,traits,influence,receipt=analyse_matched(f,nboot=a.bootstrap)
    receipt['source']=source;receipt['bootstrap_repetitions']=a.bootstrap;receipt['bootstrap_seed']=20261114
    receipt['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (a.author,a.traits)}
    a.out.mkdir(parents=True,exist_ok=True)
    for name,df in [('matched_models.csv',models),('matched_source_coverage.csv',coverage),
                    ('anthesis_associations.csv',traits),('matched_leave_one_publication.csv',influence)]:
        df.to_csv(a.out/name,index=False)
    (a.out/'matched_asymmetry_receipt.json').write_text(json.dumps(clean(receipt),indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(clean({'source':source,'primary':receipt['primary_models'],
        'trait_precision_publication':traits[(traits.panel=='source_precision')&(traits.resampling_unit=='publication')].to_dict('records'),
        'within':receipt['within_publication_trait_checks']}),indent=2,ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
