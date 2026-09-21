# IWE028 extraction/adjudication receipt — Albrectsen 2000

Source: Albrectsen BR. 2000. *Flowering phenology and seed predation by a tephritid fly: Escape of seeds in time and space*. Écoscience 7:433–438. DOI `10.1080/11956860.2000.11682614`.

Supporting source: Albrectsen BR. 2000. *The Dynamics of a Tephritid Seed Predator on Tripolium vulgare in a Stochastic and Heterogeneous Environment*. Doctoral thesis, Swedish University of Agricultural Sciences. Paper III is the focal Écoscience study.

Status: mechanistically strong antagonist timing evidence, **not admissible to strict H1**.

## Study system

The monocarpic host *Tripolium vulgare* has an extended flowering season and is attacked by the specialist tephritid seed predator *Paroxyna plantaginis*.

The study transplanted plants to eight islands and removed them successively through the season, with comparison to eleven natural populations. Early terminal flower heads were less often attacked under normal/high attack conditions, consistent with a temporal escape from the seed predator.

## What Paper III actually measures

The full-text context identifies three recorded variables for removed plants:

- morphological/flowering rank of each flower head;
- number of ovule depressions in the receptacle;
- attack by *P. plantaginis*.

The ovule count is explicitly a **potential seed-set** measure: each ovule is treated as having the potential to form one seed. It is not an observed final mature-seed outcome.

The terminal head is the first flower head to open; lateral heads flower progressively later.

## Evidence for a timing mechanism

The article and thesis support a real phenological mechanism:

- early terminal heads have lower attack risk;
- when flower heads are presented at an appropriate developmental stage, early heads are not intrinsically avoided by flies;
- the thesis therefore interprets the early escape as a mismatch between host flowering and seed-predator phenology.

This makes IWE028 useful antagonist mechanism/context evidence.

## Why it is not a strict H1 effect

The later thesis calculates **realized seed set** with a simple model rather than a direct reproductive measurement from Paper III.

The model combines:

1. intrinsic potential seed set as a function of flower-head age/rank;
2. selfing probability;
3. attack risk;
4. seed survival conditional on attack.

The appendix parameterization uses a lower attack risk for the first flowering terminal head (0.3) than for later lateral heads (0.5), while potential seed set also declines with head age/rank.

Thus the higher modeled realized seed set of early heads combines at least two mechanisms:

- an intrinsic rank/age difference in potential seed production;
- reduced antagonist attack due to phenological escape.

The strict IWE estimand requires a recoverable timing-to-final-reproduction effect with sampling variance. No variance-bearing coefficient isolating the antagonist timing component is recoverable from the published Paper III result or the thesis model.

## Executable adjudication

The component is registered as:

- `strict_h1_status = ineligible`;
- `quantitative_status = not_applicable`;
- `timing_metric_type = seasonal_position`;
- no effect row is added to `data/extraction/direct_effects.csv`.

IWE028 is therefore reclassified from `unresolved` to `context_only` in the screening registry.

## Claim boundary

IWE028 supports the mechanism:

`early flowering -> temporal escape from P. plantaginis -> lower attack risk`.

It also supports the qualitative expectation that this escape can raise realized seed production.

It does **not** supply a strict-H1 quantitative effect because final reproductive performance attributable specifically to antagonist synchrony is model-derived and lacks recoverable sampling variance.
