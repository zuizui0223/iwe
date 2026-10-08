from pathlib import Path

import pandas as pd
import pytest

from iwe.provenance_support import provenance_support, render_provenance_support


def _data():
    return (
        pd.read_csv('data/registry/temporal_signal_components.csv'),
        pd.read_csv('data/registry/propagation_endpoint_audit.csv'),
    )


def test_current_pilot_has_no_within_programme_provenance_pairs():
    result = provenance_support(*_data())
    assert result['strict_links'] == 18
    assert result['strict_cross_family_clusters'] == []
    assert result['all_final_cross_family_clusters'] == []
    rows = {(x['interaction_type'], x['window_reference_class']): x
            for x in result['strata']}
    assert rows['mutualist', 'independent_partner_activity']['clusters'] == 5
    assert rows['mutualist', 'direct_interaction_manipulation']['clusters'] == 3
    assert rows['antagonist', 'realized_interaction_window']['clusters'] == 1
    assert rows['mixed_pollinating_seed_predator', 'independent_partner_activity']['clusters'] == 0
    assert rows['mixed_pollinating_seed_predator', 'seasonal_position_only']['links'] == 1


def test_cross_family_detection_uses_programmes_not_rows():
    propagation, endpoints = _data()
    # Alter one already classified link to represent a genuinely different
    # timing-reference family within the same programme. No source mutation.
    p = propagation.copy()
    mask = p['propagation_id'].eq('SIG_IWE025_MERTENSIA_FINAL')
    assert mask.sum() == 1
    p.loc[mask, 'window_reference_class'] = 'seasonal_position_only'
    result = provenance_support(p, endpoints)
    assert result['strict_cross_family_clusters'] == [
        'DEP_MERTENSIA_GALLAGHER_CAMPBELL_RMBL'
    ]
    assert result['all_final_cross_family_clusters'] == [
        'DEP_MERTENSIA_GALLAGHER_CAMPBELL_RMBL'
    ]


def test_invalid_provenance_fails_closed():
    p, e = _data()
    p = p.copy()
    p.loc[p['propagation_id'].eq('SIG_IWE001_FINAL'), 'window_reference_class'] = 'invented_activity'
    with pytest.raises(ValueError, match='window_reference_class'):
        provenance_support(p, e)


def test_report_is_current_and_does_not_promote_h1():
    content = render_provenance_support(*_data())
    assert 'same-unit paired comparison' in content
    assert 'eligible strict-H1 meta-analysis' in content
    assert Path('docs/PROPAGATION_REFERENCE_SUPPORT_AUDIT.md').read_text(encoding='utf-8') == content
