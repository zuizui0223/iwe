from .schema import EXPOSURE_DIRECTIONS


def orient_effect(value: float, exposure_direction: str) -> float:
    """Orient an extracted effect so positive always means more synchrony -> higher reproduction."""
    if exposure_direction not in EXPOSURE_DIRECTIONS:
        raise ValueError(f"unknown exposure_direction: {exposure_direction}")
    return float(value) if exposure_direction == "synchrony" else -float(value)
