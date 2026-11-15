#!/usr/bin/env python3
"""Source-pinned original-tree sensitivity of direct day/night reproductive E."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import pandas as pd
from iwe.diel_index_selection import extract_direct
from iwe.diel_direct_lineage import analyse_direct_lineage

TREE_SOURCE='34324b8e97b87abdca53a6d578187d0bc239f2cab58974c48b58933398c84a7f'
ORIGINAL_SOURCE='3be56ba387a338795037f0fcee3e41ae2d9c5bcf26434f3421565ea10f18b07b'


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('author','traits','tree','original-analysis','out'):
        p.add_argument('--'+arg,type=Path,required=True)
    args=p.parse_args()
    if digest(args.tree)!=TREE_SOURCE or digest(args.original_analysis)!=ORIGINAL_SOURCE:
        raise ValueError('Original phylogeny or author final-analysis source checksum mismatch')
    e,source=extract_direct(args.author,args.traits)
    tree=json.loads(args.tree.read_text(encoding='utf-8'))
    original=pd.read_csv(args.original_analysis,dtype=str,keep_default_na=False)
    models,denominators,receipt=analyse_direct_lineage(e,tree,original)
    if (receipt['full_precision_cells']!=254 or
        receipt['full_precision_publication_ids']!=100 or
        receipt['tree_mapped_precision_cells']!=252 or
        receipt['tree_mapped_precision_publication_ids']!=99 or
        receipt['original_tree_tips']!=139 or len(original)!=1094):
        raise ValueError('Original source/eligible direct E source coverage changed')
    full_phy=models[(models.panel=='tree_common')&(models.model=='publication_species_phylogeny')]
    if full_phy.set_index('metric')['k_publications'].to_dict()!={'fruit set':69,'seed set':59}:
        raise ValueError('Original tree-comparable publication identity drift')
    receipt.update({
        'source_extraction':source,
        'input_sha256':{key:digest(getattr(args,key)) for key in
                        ('author','traits','tree','original_analysis')},
        'frozen_meta_roster_from_original_author':True,
        'comparisons_are_source_selected_not_new_experiments':True,
        'original_phylogeny_must_not_be_randomly_regrafted':True,
    })
    args.out.mkdir(parents=True,exist_ok=True)
    models.to_csv(args.out/'direct_phylogeny_models.csv',index=False)
    denominators.to_csv(args.out/'direct_denominator_source_coverage.csv',index=False)
    (args.out/'direct_phylogeny_receipt.json').write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(models[['metric','panel','model','k_publications','mean','ci_low','ci_high','p_nominal']].to_string(index=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
