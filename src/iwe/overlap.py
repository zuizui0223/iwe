def normalized_overlap(start_a: float, end_a: float, start_b: float, end_b: float) -> float:
    """Return interval overlap divided by union length.

    Intervals are treated as continuous half-open spans for duration arithmetic.
    Identical nonzero intervals return 1, disjoint intervals return 0.
    """
    if end_a <= start_a or end_b <= start_b:
        raise ValueError("interval ends must be greater than starts")
    overlap = max(0.0, min(end_a, end_b) - max(start_a, start_b))
    union = max(end_a, end_b) - min(start_a, start_b)
    return overlap / union
