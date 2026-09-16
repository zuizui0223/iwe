import pytest

from iwe.overlap import normalized_overlap


def test_normalized_overlap_is_one_for_identical_intervals():
    assert normalized_overlap(1, 10, 1, 10) == pytest.approx(1.0)


def test_normalized_overlap_is_zero_for_disjoint_intervals():
    assert normalized_overlap(1, 3, 5, 8) == pytest.approx(0.0)


def test_normalized_overlap_uses_union_denominator():
    assert normalized_overlap(1, 5, 3, 7) == pytest.approx(2 / 6)


def test_normalized_overlap_rejects_invalid_intervals():
    with pytest.raises(ValueError):
        normalized_overlap(5, 1, 2, 3)
