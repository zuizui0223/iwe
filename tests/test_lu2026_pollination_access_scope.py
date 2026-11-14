import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / 'data/registry' / name).open(newline='', encoding='utf-8') as h:
        return list(csv.DictReader(h))


def test_56_percent_decline_is_not_an_unqualified_open_pollination_effect():
    rows=read('alan_reproduction_claims_v01.csv')
    row=next(r for r in rows if r['study_id']=='LU_REPRO2026_TIBET' and r['endpoint']=='seed_set')
    assert row.get('pollination_access') == 'night_only', 'The prior ledger drops the pollinator-access treatment for -56%.'
    assert row.get('endpoint_definition') == 'developed_seeds_divided_by_total_ovules_per_fruit'
    assert float(row['numeric_value']) == -56.0


def load_auditor():
    import importlib.util
    path=ROOT/'scripts/audit_lu2026_access_scope.py'
    spec=importlib.util.spec_from_file_location('lu_access_auditor',path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def test_two_species_three_arms_and_unknown_estimates_not_zero():
    rows=read('lu2026_access_scoped_contrasts_v01.csv')
    report=load_auditor().validate(rows,read('alan_reproduction_claims_v01.csv'))
    assert report['transcribed_source_contrasts']==12
    assert report['numeric_percent_changes_reported']==3
    assert report['nonsignificant_contrasts_with_unknown_point_estimates']==9
    assert report['open_seed_loss_minus56_supported'] is False
    assert report['original_observations_recovered'] is False
    assert report['figure_images_visually_verified'] is False
    assert report['new_meta_analytic_effects']==0


def test_open_seed_effect_cannot_be_silently_imputed_zero():
    import pytest
    rows=read('lu2026_access_scoped_contrasts_v01.csv')
    row=next(r for r in rows if r['plant']=='Pedicularis kansuensis' and r['endpoint']=='seed_set' and r['pollination_access']=='open')
    row['percent_change']='0'
    with pytest.raises(ValueError,match='unknown estimates'):
        load_auditor().validate(rows,read('alan_reproduction_claims_v01.csv'))


def test_sample_size_and_error_cannot_be_invented_from_twenty_plants():
    import pytest
    rows=read('lu2026_access_scoped_contrasts_v01.csv')
    rows[0]['sem']='0.01'
    with pytest.raises(ValueError,match='manufacture'):
        load_auditor().validate(rows,read('alan_reproduction_claims_v01.csv'))


def test_mean_seed_counts_and_seed_ovule_fraction_are_not_interchangeable():
    import pytest
    rows=read('lu2026_access_scoped_contrasts_v01.csv')
    next(r for r in rows if r['endpoint']=='seed_set')['endpoint_definition']='seeds_per_plant'
    with pytest.raises(ValueError,match='denominator'):
        load_auditor().validate(rows,read('alan_reproduction_claims_v01.csv'))


def test_duplicate_treatment_cannot_inflate_source_replication():
    import pytest
    rows=read('lu2026_access_scoped_contrasts_v01.csv')
    with pytest.raises(ValueError,match='exactly two plants'):
        load_auditor().validate(rows+[rows[0]],read('alan_reproduction_claims_v01.csv'))


def test_cli_creates_only_scoped_published_aggregates(tmp_path):
    import json,subprocess,sys
    p=subprocess.run([sys.executable,str(ROOT/'scripts/audit_lu2026_access_scope.py'),'--output-dir',str(tmp_path)],cwd=ROOT,capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    report=json.loads((tmp_path/'lu2026_access_scope_receipt.json').read_text())
    assert report['pollination_access_treatment_for_minus56_percent']=='night_only'
    assert report['supplementary_table_S4b_recovered'] is False
    assert report['new_iwe_strict_H1_effects']==0
