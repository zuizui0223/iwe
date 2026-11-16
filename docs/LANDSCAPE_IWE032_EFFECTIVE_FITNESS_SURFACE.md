# IWE032 — effective interaction window predicts final plant fitness

Date: 2026-10-02  
Study: Davies & Saccheri 2024, *Cardamine pratensis × Anthocharis cardamines*  
DOI: `10.1002/ece3.11330`  
Status: source-model-reconstructed final-fitness landscape; realized/effective window, not strict adult-flight evidence.

## Why this is a separate component

The Cardamine programme contains three different temporal objects:

1. female butterfly flight — the strongest independent partner-exposure reference, still missing as a numeric 2012–2014 event distribution;
2. total versus active egg load — a realized-interaction filter showing which ovipositions can produce damaging larvae;
3. final plant fitness — intact reproductive units at dehiscence.

The present component links objects 2 and 3 using the paper's own fitness equation. It does **not** substitute active eggs for independent adult activity.

## Source fitness model

For a ramet with potential reproductive units `R` and flowering phenology `z`, the source defines

`F(R,z) = R [ I- - E(R,z) L (I- - I+) ]`,

where:

- `I-` = proportion of reproductive units intact at dehiscence without fifth-instar larvae;
- `I+` = corresponding proportion with fifth-instar larvae;
- `E(R,z)` = active egg load as a Gaussian function of flowering date;
- `L = 0.22` = proportion of eggs surviving to fifth instar.

Because `I- > I+`, fitness decreases monotonically with active egg load. Therefore the fitness trough occurs at the center of the active-egg Gaussian.

## Reconstructed source-model troughs

### High-fecundity ramets

Source inputs:

- R = 29.8;
- I- = 0.3784;
- I+ = 0.1206;
- active egg curve amplitude = 2.00;
- center z = -0.53;
- sigma = 0.63;
- L = 0.22.

Derived:

- baseline predicted intact RU outside the antagonist cost window = **11.2763**;
- predicted intact RU at the effective cost peak = **7.8960**;
- predicted loss at the trough = **3.3803 RU**, or **29.98%** of the baseline.

### Medium-fecundity ramets

Source inputs:

- R = 15.4;
- I- = 0.2829;
- I+ = 0.0477;
- active egg curve amplitude = 0.75;
- center z = -0.76;
- sigma = 0.78;
- L = 0.22.

Derived:

- baseline predicted intact RU = **4.3567**;
- predicted intact RU at the effective cost peak = **3.7590**;
- predicted loss = **0.5976 RU**, or **13.72%**.

## Biological result

The host-filtered active-egg window is not merely associated with an intermediate attack variable. Under the source's prospectively stated model and observed grazing costs, it directly determines a final reproductive-fitness trough.

The same effective window is phenotype-dependent:

- high-fecundity ramets have a higher, narrower active-egg peak and a deeper predicted fitness trough;
- medium-fecundity ramets have a lower, broader peak and a shallower predicted trough.

This supplies the first IWE programme in which a pre-fitness host filter is quantitatively propagated to final plant reproduction without defining the filter from the final fitness outcome itself.

## Claim boundary

This is **source-model-reconstructed** fitness, not a new individual-level causal estimate and not an independent programme replication.

The same Cardamine dependence cluster is used for all components.

The strict IWE032 adult-flight route remains blocked until the numeric 2012–2014 female capture/recapture timing distribution is recovered.

The next decisive test is independent replication of this raw-exposure -> effective-window -> final-fitness chain in another biological programme.

## Reproducibility

Source parameters are stored in `data/source_reconstructions/iwe032_effective_fitness_parameters.csv`.

`scripts/build_iwe032_effective_fitness_surface.py` deterministically produces `data/derived/iwe032_effective_fitness_surface.csv`.
