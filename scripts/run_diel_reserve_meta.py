#!/usr/bin/env python3
"""Reanalyse source day/night/open/closed reproduction; no artificial-light effect."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from iwe.diel_reserve_meta import extract,analyse,robustness


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--author',type=Path,required=True)
    p.add_argument('--traits',type=Path,required=True)
    p.add_argument('--out-dir',type=Path,required=True)
    a=p.parse_args()
    cells,audit=extract(a.author)
    models,selection,receipt=analyse(cells)
    leave,boot,traitaudit=robustness(cells,a.traits)
    receipt.pop('publication_effects_internal')
    eligible=cells[cells.precision_status.eq('source_precision_available')]
    receipt['coverage']={
        'available_mean_cells_any_contrast':int(cells.cell_id.nunique()),
        'available_mean_publications':int(cells.study.nunique()),
        'available_mean_plant_taxa':int(cells.plant.nunique()),
        'source_precision_cells_any_contrast':int(eligible.cell_id.nunique()),
        'source_precision_publications':int(eligible.study.nunique()),
        'source_precision_plant_taxa':int(eligible.plant.nunique()),
        'full_fourarm_valid_mean_cells':int(cells[cells.complete_fourarm_means].cell_id.nunique())}
    receipt['original_analysis_scope_not_reproduced']=True
    receipt['new_scope']='All original fruit/seed source cells; contrast-specific arms and precision; no satellite-year restrictions'
    receipt['source_audit']=audit;receipt['family_sensitivity_source']=traitaudit
    receipt['limits']=[
        'These are diel exclusion experiments, not ALAN manipulations or measured light dose responses.',
        'Common-placebo/control and across-cell covariances are unknown; first-order variance upper bounds are used.',
        'An upper sampling-variance bound need not widen a REML interval monotonically because heterogeneity weights change.',
        'Publication IDs are not verified independent experimental programmes; shared taxa/phylogeny remain.',
        'Bagging, wind, selfing and saturating fruit/seed response can cause nonadditivity without visitor compensation.',
        'Source errors are not revalidated against every primary paper; n may represent flowers or plants.',
        'The 140-ID public source differs from the authors final 135-study analysis; this reanalysis has its own explicit selection.',
        'Seed metric names include different denominators; only matched source cells are compared and endpoints stay separate.',
        'No new IWE seasonal-synchrony H1 effect, island-mainland ALAN contrast or chocho geographic effect is generated.']
    a.out_dir.mkdir(parents=True,exist_ok=True)
    models.to_csv(a.out_dir/'diel_meta_models.csv',index=False)
    selection.to_csv(a.out_dir/'source_selection_sensitivity.csv',index=False)
    leave.to_csv(a.out_dir/'leave_one_publication_out.csv',index=False)
    boot.to_csv(a.out_dir/'publication_family_balanced_bootstrap.csv',index=False)
    (a.out_dir/'diel_meta_receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'coverage':receipt['coverage'],'primary':receipt['primary_models']},indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
