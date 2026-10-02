# Independent host-stage filtering — Arnaldo et al. 2014

Date: 2026-10-02  
Study: Arnaldo et al. 2014, *Gentiana pneumonanthe × Phengaris alcon*  
DOI: `10.1007/s10841-014-9721-x`  
Study region: Portugal  
Status: mechanism-only replication; not plant final-fitness evidence.

## Why this programme matters

The Cardamine result shows that raw egg exposure and the effective damaging window can differ because host timing filters whether eggs develop into damaging larvae.

Arnaldo et al. provide an independent programme with the same general causal ordering:

`oviposition timing × host developmental stage -> offspring survival/development`.

The study monitored **127 gentian shoots and 837 eggs** through three parts of the butterfly flight period.

## Seasonal exposure pattern

The reported period summaries are:

| Flight period | Shoots | Apical bud length | Eggs per shoot |
|---|---:|---:|---:|
| 1 | 39 | 1.59 ± 0.81 | 8.87 ± 8.14 |
| 2 | 41 | 1.86 ± 0.88 | 6.00 ± 6.36 |
| 3 | 47 | 2.60 ± 1.04 | 5.21 ± 5.30 |

Egg exposure is therefore highest during the first third of the flight period while host buds are, on average, less developed.

## Host filtering of exposure

The offspring-survival GLM reports survival differences associated with both host state and oviposition time.

| Predictor | Survival-model estimate | Source p |
|---|---:|---:|
| Flower-bud length | +0.350 | 0.017 |
| Flower developmental stage | -1.088 | 0.005 |
| Oviposition period 2 vs 1 | -0.881 | <0.001 |
| Oviposition period 3 vs 1 | -0.536 | 0.033 |

The source reports approximately 55% offspring survival overall, with greater survival from eggs on larger buds and buds in an early developmental stage; offspring of early-flying females also survive better.

## Relation to the IWE pivot

This result independently supports the distinction between:

1. **raw exposure** — when and where eggs are deposited;
2. **effective antagonist exposure** — the subset of those eggs whose host-stage context permits successful offspring development.

The direction of the filter is system-specific. Cardamine defenses make sufficiently delayed eggs ineffective, whereas in this Portuguese Gentiana programme offspring performance depends jointly on bud size, developmental stage and season.

The general candidate principle is therefore not that host filtering always shifts a cost window later. It is:

> host phenology transforms the mapping from partner exposure to effective biotic cost.

## Independence and claim boundary

This is geographically and investigator-wise distinct from the IWE012 Valdés–Ehrlén programme in southwest Sweden, despite using the same plant and butterfly species.

It does not measure final plant reproductive fitness and is therefore registered as `mechanism_only`.

It cannot by itself support a plant fitness-landscape effect size. Its role is to replicate the **pre-fitness host-stage filter** that makes raw partner activity an incomplete definition of the biologically effective interaction window.

Machine-readable source summaries are retained in `data/source_reconstructions/arnaldo2014_host_stage_filter.csv`.
