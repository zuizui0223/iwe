import importlib.util
import math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]

def module():
    path=ROOT/'src/iwe/alan_access_response_ratio.py'
    assert path.exists(), 'within-study access-response module not implemented'
    spec=importlib.util.spec_from_file_location('access_ratio_under_test',path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def source_rows():
    import csv
    with (ROOT/'data/registry/lu2026_access_scoped_contrasts_v01.csv').open(newline='',encoding='utf-8') as h:
        return list(csv.DictReader(h))

def test_same_response_ratio_and_no_unsourced_precision():
    x=module().compare_light_responses(0.7691,0.462)
    assert x['ratio_of_response_ratios']==pytest.approx(1.6647186147186146)
    assert x['log_ratio_of_response_ratios']==pytest.approx(0.5096561089812692)
    assert x['relative_change_gap_percentage_points']==pytest.approx(30.71)
    assert x['variance'] is None and x['ci95'] is None and x['p_value'] is None

def test_missing_nonsignificant_seed_point_estimate_is_not_zero_effect():
    x=module().compare_light_responses(None,0.44)
    assert x['ratio_of_response_ratios'] is None
    assert x['status']=='missing_point_estimate'

def test_effects_are_light_ratios_not_open_versus_night_raw_pollen():
    x=module().compare_light_responses(0.8,0.4)
    assert x['ratio_of_response_ratios']==2
    assert x['identifies_absolute_open_over_night_response'] is False
    assert x['demonstrates_daytime_compensation'] is False

def test_zero_outcomes_are_not_given_a_pseudocount():
    for a,b in [(0,0.4),(0.8,0),(0,0)]:
        x=module().compare_light_responses(a,b)
        assert x['status']=='zero_ratio_log_contrast_undefined'
        assert x['log_ratio_of_response_ratios'] is None

def test_negative_or_nonfinite_source_ratio_rejected():
    for a,b in [(-1,.4),(float('nan'),.4),(.4,float('inf'))]:
        with pytest.raises(ValueError): module().compare_light_responses(a,b)

def test_complete_four_species_outcome_pairs_but_only_one_numeric():
    pairs,receipt=module().from_scoped_source(source_rows())
    assert len(pairs)==4
    assert receipt['numeric_paired_contrasts']==1
    assert receipt['not_numeric_paired_contrasts']==3
    assert receipt['original_independent_studies']==1
    assert receipt['variance_available_contrasts']==0
    assert receipt['new_iwe_strict_h1_effects']==0
    seed=next(x for x in pairs if x['plant']=='Pedicularis kansuensis' and x['endpoint']=='seed_set')
    assert seed['night_light_ratio']==.44 and seed['open_light_ratio'] is None
    assert seed['ratio_of_response_ratios'] is None

def test_duplicate_or_wrong_denominator_or_altered_arm_fails():
    original=source_rows()
    variants=[original+[original[0]]]
    changed=[dict(x) for x in original]; changed[0]['endpoint_definition']='seeds_per_plant'; variants.append(changed)
    changed=[dict(x) for x in original]; changed[0]['pollination_access']='night_only'; variants.append(changed)
    changed=[dict(x) for x in original]; changed[0]['lit_dark_ratio']='0.5'; variants.append(changed)
    for rows in variants:
        with pytest.raises(ValueError): module().from_scoped_source(rows)

def test_nulls_never_become_zero_and_only_source_signed_ratios_enter():
    rows=source_rows()
    r=next(x for x in rows if x['plant']=='Pedicularis kansuensis' and x['endpoint']=='seed_set' and x['pollination_access']=='open')
    r['percent_change']='0';r['lit_dark_ratio']='1'
    with pytest.raises(ValueError): module().from_scoped_source(rows)

def test_no_unextracted_variance_may_be_pretended_known():
    rows=source_rows();rows[0]['sampling_variance']='0.01'
    with pytest.raises(ValueError,match='precision'):
        module().from_scoped_source(rows)

def test_cli_checks_exact_source_and_writes_four_pairs(tmp_path):
    import csv,json,os,subprocess,sys
    env=dict(os.environ);env['PYTHONPATH']=str(ROOT/'src')+os.pathsep+env.get('PYTHONPATH','')
    p=subprocess.run([sys.executable,str(ROOT/'scripts/audit_lu2026_response_ratios.py'),
                      '--output-dir',str(tmp_path)],cwd=ROOT,env=env,text=True,capture_output=True)
    assert p.returncode==0,p.stderr
    result=json.loads((tmp_path/'access_response_ratio_receipt.json').read_text())
    assert result['input_git_blob_sha1']=='73a04ebd962a3113ebfae410c1720468094ab60a'
    assert result['numeric_paired_contrasts']==1 and result['variance_available_contrasts']==0
    with (tmp_path/'access_matched_light_response_ratios.csv').open(newline='') as h:
        rows=list(csv.DictReader(h))
    assert len(rows)==4
    assert sum(r['ratio_of_response_ratios']!='' for r in rows)==1
