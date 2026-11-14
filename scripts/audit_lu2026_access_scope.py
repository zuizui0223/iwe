"""Treatment-scoped transcription of Lu JPE 2026, not a raw-data reanalysis.

The accepted manuscript reports -56% seed set in the nocturnal-only arm.
No nonsignificant open-arm effect is recoded as zero. Numeric variability,
block assignments and the original Table S4b are not available here.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path

DOI = '10.1093/jpe/rtag160'
KEYS = ('plant', 'endpoint', 'pollination_access')
EXPECTED = {
    ('Pedicularis kansuensis', 'conspecific_pollen', 'open'): -23.09,
    ('Pedicularis kansuensis', 'conspecific_pollen', 'night_only'): -53.8,
    ('Pedicularis kansuensis', 'seed_set', 'night_only'): -56.0,
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def validate(rows: list[dict[str, str]], legacy: list[dict[str, str]]) -> dict:
    wanted = {(s, e, a) for s in ('Pedicularis kansuensis', 'Euphrasia regelii')
              for e in ('conspecific_pollen', 'seed_set')
              for a in ('open', 'day_only', 'night_only')}
    actual = [tuple(r[k] for k in KEYS) for r in rows]
    if len(actual) != 12 or len(set(actual)) != 12 or set(actual) != wanted:
        raise ValueError('Require exactly two plants x two outcomes x three access arms')
    for r in rows:
        key = tuple(r[k] for k in KEYS)
        if r['doi'] != DOI or r['raw_data_obtained'] != 'no':
            raise ValueError('Source DOI / original-data status drift')
        if r['sem'] or r['sampling_variance'] or r['p_value']:
            raise ValueError('Do not manufacture unextracted errors or p values')
        if key in EXPECTED:
            if r['reported_effect'] != 'decrease_reported' or float(r['percent_change']) != EXPECTED[key]:
                raise ValueError('Reported treatment-specific percentage changed')
            if abs(float(r['lit_dark_ratio']) - (1 + EXPECTED[key] / 100)) > 1e-10:
                raise ValueError('Ratio must be a transformation of the reported percent only')
        elif (r['reported_effect'] != 'no_significant_effect_reported' or
              r['percent_change'] or r['lit_dark_ratio']):
            raise ValueError('Nonsignificant effects are unknown estimates, not zero')
        definition = ('developed_seeds_divided_by_total_ovules_per_fruit'
                      if r['endpoint'] == 'seed_set' else 'conspecific_pollen_grains_per_stigma')
        if r['endpoint_definition'] != definition:
            raise ValueError('Outcome denominator does not match Methods p11')
    scoped = [r for r in legacy if r['study_id'] == 'LU_REPRO2026_TIBET' and r['endpoint'] == 'seed_set']
    if len(scoped) != 1 or scoped[0].get('pollination_access') != 'night_only':
        raise ValueError('Legacy -56% claim still loses the night-only treatment')
    if scoped[0].get('endpoint_definition') != 'developed_seeds_divided_by_total_ovules_per_fruit':
        raise ValueError('Legacy seed_set has wrong denominator')
    return {
        'schema': 'iwe_lu_jpe_pollination_access_scope_v1',
        'source_doi': DOI,
        'source_evidence': 'accepted_manuscript_parsed_full_text_pages_8_to_16',
        'original_observations_recovered': False,
        'supplementary_table_S4b_recovered': False,
        'figure_images_visually_verified': False,
        'transcribed_source_contrasts': 12,
        'numeric_percent_changes_reported': 3,
        'nonsignificant_contrasts_with_unknown_point_estimates': 9,
        'paired_lit_unlit_plot_replicates_reported': 5,
        'pollination_access_treatment_for_minus56_percent': 'night_only',
        'seed_endpoint': 'developed_seeds_divided_by_total_ovules_per_fruit',
        'open_seed_loss_minus56_supported': False,
        'open_pollen_percent_change': -23.09,
        'open_seed_effect': 'no_significant_effect_reported_not_zero_not_equivalent',
        'effect_species_mating_system_causally_separable': False,
        'per_visit_moth_vs_fly_efficacy_measured': False,
        'formal_cross_species_interaction_reestimated': False,
        'independent_population_variance_available': False,
        'same_experimental_plots_as_Lu_network_article_verified': False,
        'new_meta_analytic_effects': 0,
        'new_iwe_strict_H1_effects': 0,
        'correction': 'Prior abstract-only ledger omitted pollination-access arm. Night-only susceptibility is not an open-pollination seed loss.',
        'biological_interpretation': 'An impairment of nocturnal pollen/reproduction need not translate into a resolved open-access seed decline; daytime buffering, dose-response saturation and limited precision remain alternatives.',
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scope', type=Path, default=Path('data/registry/lu2026_access_scoped_contrasts_v01.csv'))
    p.add_argument('--claims', type=Path, default=Path('data/registry/alan_reproduction_claims_v01.csv'))
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    rows = read(args.scope)
    result = validate(rows, read(args.claims))
    result['input_sha256'] = {x.name: hashlib.sha256(x.read_bytes()).hexdigest() for x in (args.scope, args.claims)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'lu2026_access_scope_receipt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (args.output_dir / 'lu2026_access_scoped_contrasts.csv').open('w', newline='', encoding='utf-8') as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
