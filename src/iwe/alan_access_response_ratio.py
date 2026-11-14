"""Within-study light-response modification by pollinator access.

Transforms reported rounded percentages, not original observations.  The
open/night ratio of light-response ratios is NOT an absolute open/night
pollen ratio.  Missing nonsignificant estimates are never set to one.
"""
from __future__ import annotations
import math

DOI = '10.1093/jpe/rtag160'
DEFINITIONS = {
    'conspecific_pollen': 'conspecific_pollen_grains_per_stigma',
    'seed_set': 'developed_seeds_divided_by_total_ovules_per_fruit',
}
PLANTS = ('Pedicularis kansuensis', 'Euphrasia regelii')
ACCESSES = ('open', 'day_only', 'night_only')
SOURCE_PERCENT = {
    ('Pedicularis kansuensis','conspecific_pollen','open'): -23.09,
    ('Pedicularis kansuensis','conspecific_pollen','night_only'): -53.8,
    ('Pedicularis kansuensis','seed_set','night_only'): -56.0,
}


def compare_light_responses(open_ratio: float | None, night_ratio: float | None) -> dict:
    """Return descriptive B=log(RR_open/RR_night); no invented variance.

    Each input uses its OWN unlit comparator in the SAME endpoint,
    population, light treatment, and experiment.  The source adapter is
    responsible for those matching conditions. Zero ratios stay zero but
    no arbitrary continuity correction is applied to their log contrast.
    """
    for value in (open_ratio, night_ratio):
        if value is not None and (not math.isfinite(value) or value < 0):
            raise ValueError('Ratios must be finite, nonnegative or None')
    out = {
        'open_light_ratio': open_ratio, 'night_light_ratio': night_ratio,
        'ratio_of_response_ratios': None, 'log_ratio_of_response_ratios': None,
        'relative_change_gap_percentage_points': None,
        'variance': None, 'ci95': None, 'p_value': None,
        'identifies_absolute_open_over_night_response': False,
        'demonstrates_daytime_compensation': False,
        'new_independent_study': False,
    }
    if open_ratio is None or night_ratio is None:
        out['status'] = 'missing_point_estimate'
    elif open_ratio == 0 or night_ratio == 0:
        out['status'] = 'zero_ratio_log_contrast_undefined'
    else:
        log_ratio = math.log(open_ratio) - math.log(night_ratio)
        value = open_ratio / night_ratio
        if not math.isfinite(value):
            raise ValueError('Response-ratio contrast overflow')
        out.update(
            status='descriptive_point_only_no_sampling_covariance',
            ratio_of_response_ratios=value,
            log_ratio_of_response_ratios=log_ratio,
            relative_change_gap_percentage_points=100*(open_ratio-night_ratio),
        )
    return out


def from_scoped_source(rows: list[dict[str,str]]) -> tuple[list[dict],dict]:
    """Match the pre-existing 2-plant x 2-endpoint x 3-access source grid.

    The DOI identifies one experiment; source pages and explicit access
    keep unlike outcomes and article-wide visitor counts out of a pair.
    """
    required = {'doi','plant','endpoint','pollination_access','reported_effect',
                'percent_change','lit_dark_ratio','endpoint_definition',
                'source_pages','sem','sampling_variance','p_value','raw_data_obtained'}
    if any(not required <= set(row) for row in rows):
        raise ValueError('Missing source scope columns')
    expected = {(p,e,a) for p in PLANTS for e in DEFINITIONS for a in ACCESSES}
    keys = [(r['plant'],r['endpoint'],r['pollination_access']) for r in rows]
    if len(keys)!=12 or len(set(keys))!=12 or set(keys)!=expected:
        raise ValueError('Expected complete unique 2 x 2 x 3 access grid')
    values={}
    for key,row in zip(keys,rows):
        if row['doi']!=DOI or row['raw_data_obtained']!='no':
            raise ValueError('Source identity or evidence tier changed')
        if row['endpoint_definition']!=DEFINITIONS[row['endpoint']]:
            raise ValueError('Endpoint definition/denominator mismatch')
        if any(row[k].strip() for k in ('sem','sampling_variance','p_value')):
            raise ValueError('Unextracted sampling precision cannot be manufactured')
        if not row['source_pages'].strip():
            raise ValueError('Original source page provenance is missing')
        if key in SOURCE_PERCENT:
            pct=float(row['percent_change']); rr=float(row['lit_dark_ratio'])
            if (row['reported_effect']!='decrease_reported' or
                not math.isclose(pct,SOURCE_PERCENT[key],abs_tol=1e-12) or
                not math.isclose(rr,1+pct/100,rel_tol=1e-12,abs_tol=1e-12)):
                raise ValueError('Published percentage or scoped ratio drift')
            values[key]=rr
        else:
            if (row['reported_effect']!='no_significant_effect_reported' or
                row['percent_change'].strip() or row['lit_dark_ratio'].strip()):
                raise ValueError('Unknown nonsignificant point estimate must remain missing')
            values[key]=None
    pairs=[]
    for plant in PLANTS:
        for endpoint,definition in DEFINITIONS.items():
            out=compare_light_responses(values[(plant,endpoint,'open')],
                                        values[(plant,endpoint,'night_only')])
            pairs.append({'source_doi':DOI,'plant':plant,'endpoint':endpoint,
                          'endpoint_definition':definition,
                          'exposure_comparison':'ALAN_lit_vs_unlit_within_each_access_arm',
                          'access_modifier':'open_vs_night_only', **out})
    valid=sum(p['ratio_of_response_ratios'] is not None for p in pairs)
    receipt={
        'schema':'iwe_lu2026_matched_access_light_response_v1',
        'source_doi':DOI,'original_independent_studies':1,
        'scoped_input_contrasts':12,'matched_species_endpoint_pairs':4,
        'numeric_paired_contrasts':valid,'not_numeric_paired_contrasts':len(pairs)-valid,
        'variance_available_contrasts':0,'inferential_meta_ready_contrasts':0,
        'formula':'log[(Y_lit,open/Y_dark,open)/(Y_lit,night/Y_dark,night)]',
        'variance_formula':'Var(logRR_open)+Var(logRR_night)-2*Cov(logRR_open,logRR_night)',
        'unknown_shared_block_covariance_assumed_zero':False,
        'raw_observations_reestimated':False,
        'published_rounded_percentages_transformed':True,
        'number_of_additional_significant_results':0,
        'full_reproductive_compensation_demonstrated':False,
        'global_ALAN_or_island_effect_identified':False,
        'new_iwe_strict_h1_effects':0,
    }
    return pairs,receipt
