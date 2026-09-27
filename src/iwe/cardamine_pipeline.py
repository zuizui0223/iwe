from __future__ import annotations

import pandas as pd

from .cardamine_outcome import cardamine_smd_audit, cardamine_smd_effects
from .cardamine_timing import cardamine_timing_only_exposure


def run_cardamine_preflight(
    plant_observations: pd.DataFrame,
    adult_events: pd.DataFrame,
    plant_summaries: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run the frozen Cardamine timing -> audit -> SMD pipeline.

    The three inputs stay conceptually separate:
    - plant_observations: timing-only repeated flower observations;
    - adult_events: source-backed female capture/recapture DOYs;
    - plant_summaries: source-normalized max/final reproductive units.

    No output is promoted into the IWE extraction table by this function.
    """
    exposure = cardamine_timing_only_exposure(plant_observations, adult_events)
    audit = cardamine_smd_audit(exposure, plant_summaries)
    effects = cardamine_smd_effects(exposure, plant_summaries)
    return exposure, audit, effects
