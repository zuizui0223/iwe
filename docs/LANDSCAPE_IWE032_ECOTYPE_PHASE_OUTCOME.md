# IWE032 — oviposition phase predicts whether plants outrun larval damage

Date: 2026-10-03  
Study: Davies & Saccheri 2024, *Cardamine pratensis × Anthocharis cardamines*  
DOI: `10.1002/ece3.11330`  
Landscape role: positive final-outcome evidence for a realized stage-specific phase coordinate.

## Why this matters

The strict IWE032 route still lacks the numeric 2012–2014 adult female flight distribution needed for a paired adult-window comparison.

But the source directly reports a different stage-specific coordinate at the individual/ecotype level:

`oviposition interval = egg-laying date - first flowering date`.

It also follows attacked plants to dehiscence or complete larval consumption.

Therefore the paper already closes a narrower causal chain:

`flowering -> oviposition delay -> larval activation / developmental race -> final plant fate`.

## Ecotype contrast in phase

The early ecotype experiences substantially later oviposition relative to first flowering:

- early ecotype: **11.50 ± 1.44 d**, N = 31;
- late ecotype: **5.72 ± 0.53 d**, N = 270.

The source attributes the longer interval to the advanced flowering phenology of the early ecotype.

## Oviposition interval defines an active/inactive transition

On the late ecotype, eggs laid within 7 days after flowering were the group that produced fifth-instar larvae:

- active eggs, ≤7 d: **N = 158**;
- eggs laid later than 8 d: **N = 87**, and did not produce full-grown larvae.

Thus the realized egg event is filtered by its phase relative to host development before it becomes a damaging larval event.

## Final plant fate differs in the predicted direction

Among early-ecotype plants bearing final-instar larvae:

- **34%** dehisced before the larva completed development;
- **41%** were wholly consumed before dehiscence.

For the late ecotype:

- only **4%** dehisced before larval development completed;
- **58%** were wholly consumed.

The three-category fate distributions differ significantly:

`chi-square(df=2) = 11.95, p = 0.003`.

The paper explicitly links the higher early-ecotype escape fraction to delayed egg-laying relative to flowering.

## Interpretation

This is a positive final-outcome test of the stage-specific model:

> when oviposition occurs later relative to host development, the host has more time to reach dehiscence before the damaging consumer stage completes development.

The result is stronger than an intermediate larval-performance association because the endpoint is whether reproductive units reach dehiscence before being consumed.

It also explains why raw adult flight, realized oviposition and effective larval cost should not be collapsed into one synchrony variable.

## Why the confirmatory gate is still not fully closed

This comparison does **not** yet establish that the stage-specific phase coordinate predicts fitness better than a simpler adult-flight or calendar coordinate.

The adult female flight distribution used in Figure 4 is still not numerically recoverable in the present runtime. Without it, the same biological units cannot be scored under both:

1. adult-flight overlap; and
2. oviposition/effective-cost phase.

Accordingly the phase-alignment registry remains `near_confirmatory`, not `confirmatory_ready`.

## Reproducibility

Source-backed values are stored in
`data/source_reconstructions/iwe032_ecotype_phase_outcome.csv`.
