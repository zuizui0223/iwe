from pathlib import Path
import json, subprocess, sys
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def test_original_source_gate_and_synthetic_null_cli(tmp_path):
    r=subprocess.run([
        sys.executable,str(ROOT/'scripts/audit_alan_joint_factorial.py'),
        '--source',str(ROOT/'data/registry/alan_iwe_light_access_source_v01.csv'),
        '--output-dir',str(tmp_path), '--replications','2000',
    ],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    z=json.loads((tmp_path/'alan_factorial_source_gate_receipt.json').read_text())
    assert z['individually_source_recomputable_delta_interactions']==0
    assert len(z['source_csv_sha256'])==64
    assert z['original_MACGREGOR_rate_diagnostic']['can_be_used_as_dark_open_moderator'] is False
    sims=pd.read_csv(tmp_path/'null_shared_dark_control.csv')
    assert sims['flowers_per_treatment'].tolist()==[20,60,200]
    assert (sims['shared_control_mean_beta']<0).all()
    assert (sims['shared_control_fraction_negative']>.55).all()
    assert len(pd.read_csv(tmp_path/'study_factorial_eligibility.csv'))==2
