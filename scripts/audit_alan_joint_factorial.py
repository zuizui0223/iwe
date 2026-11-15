#!/usr/bin/env python3
"""Audit real source feasibility and simulate denominator-linked false slope.

No experimental ALAN causal effects or field observations are fitted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from iwe.alan_joint_factorial import (
    shared_denominator_null, macgregor_pooled_caging_check,
    validate_published_factorial_gate,
)

DEFAULT_SOURCE=Path('data/registry/alan_iwe_light_access_source_v01.csv')


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=DEFAULT_SOURCE)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--replications',type=int,default=20000)
    a=ap.parse_args()
    with a.source.open(newline='',encoding='utf-8') as handle:
        studies=list(csv.DictReader(handle))
    outcome=validate_published_factorial_gate(studies)
    rates=macgregor_pooled_caging_check()
    simulations=[shared_denominator_null(n_per_arm=n,repetitions=a.replications)
                 for n in (20,60,200)]
    result={**outcome,
            'original_MACGREGOR_rate_diagnostic':rates,
            'source_csv_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),
            'source_DOIs':['10.1002/ecs2.2550','10.1093/jpe/rtag160'],
            'source_metadata_source':'public_published_articles_and_2026_11_15_source_audit',
            'synthetic_no_ALAN_effect_null':simulations,
            'systematic_literature_census_performed':False,
            'same_study_Lu_and_network_experiment_independence_verified':False,
            'published_study_interaction_beta_reported_as_zero':False,
            'no_unverified_raw_rows_or_SE_reconstructed':True}
    a.output_dir.mkdir(parents=True,exist_ok=True)
    (a.output_dir/'alan_factorial_source_gate_receipt.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    with (a.output_dir/'null_shared_dark_control.csv').open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(simulations[0]));writer.writeheader();writer.writerows(simulations)
    with (a.output_dir/'study_factorial_eligibility.csv').open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(studies[0]));writer.writeheader();writer.writerows(studies)
    print(json.dumps({'studies':outcome['papers_with_factorial_design'],
          'recomputable_interactions':outcome['individually_source_recomputable_delta_interactions'],
          'synthetic_negative_beta_fractions':[round(s['shared_control_fraction_negative'],4) for s in simulations],
          'output_dir':str(a.output_dir)},indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
