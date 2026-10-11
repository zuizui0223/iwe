# Parkinsonia conversion-bottleneck ablation — outcome-exposed falsification

Date: 2026-10-08
System: *Parkinsonia aculeata × Penthobruchus germaini*
Source: van Klinken & Flack 2008, DOI `10.1111/j.1365-2664.2008.01478.x`
Status: **EXPLORATORY / outcome exposed / non-confirmatory**.

## Why this reanalysis was needed

The original three-coordinate paired diagnostic suggested that annual egg density performed poorly, host-stage-matched egg density slightly better, and stage-matched density filtered by egg parasitism and hatch much better. That result cannot by itself show whether the benefit comes from temporal matching, from the downstream survival bottleneck, or from their product.

An explicit falsification test asks: **does the measured survival/conversion fraction predict final seed predation as well as the supposedly more mechanistically complete stage-matched exposure?**

## Fixed source units and matching rules

The comparison uses the same **7 region-season records from 4 regions**, the same reported final percentage seed predation, and the same leave-one-**region**-out folds and single-predictor intercept+linear-slope model as the prior published-source reconstruction.

Raw values are in `data/source_reconstructions/vanklinken2008_paired_stage_diagnostic.csv`. Stage-matched eggs are drawn from the source-defined late sampling window; survival fraction is `(1 - egg parasitism / 100) × (egg hatch / 100)`. All fractions are measured within the same source units and are not independent experiments.

**Critical timing-of-measurement audit:** the original Methods state that collected pods were frozen and then dissected to examine egg presence/condition (including parasitism and hatch) **and seed fate in the same sample**. Table 5 lists egg density, egg parasitism, egg hatch and seed predation for the late pod collections in the same region-season. Thus parasitism and hatch are biologically upstream of larval seed consumption, but their empirical values were **not available at an independent time prior to the outcome observation**. They are **contemporaneous retrospective diagnostics**, not operational early-warning predictors. Blocking regions during regression CV cannot transform same-sample measurements into a prospective forecast.

**Crucial selection disclosure:** the ten ablation predictors were specified after inspecting the seven final outcomes and the original three-model results. The leave-one-region-out folds re-fit regression coefficients but **do not nest the predictor-selection process**. Their ranking is descriptive/optimistic and must not be presented as an unbiased validation of a selected model.

## All ten single-predictor candidates

| Predictor | Pearson r with final predation | Region-blocked RMSE (pp) | MAE (pp) |
|---|---:|---:|---:|
| Annual egg density | 0.476 | 20.58 | 19.04 |
| Stage-matched egg density | 0.596 | 19.93 | 16.10 |
| Nonparasitized fraction | 0.952 | 4.72 | 4.14 |
| Hatch fraction | 0.313 | 15.83 | 14.40 |
| **Nonparasitized × hatch fraction** | **0.972** | **4.11** | **3.61** |
| Annual eggs × nonparasitized fraction | 0.772 | 10.92 | 9.88 |
| Stage eggs × nonparasitized fraction | 0.846 | 7.66 | 6.78 |
| Stage eggs × hatch fraction | 0.822 | 6.98 | 5.84 |
| Annual eggs × joint survival | 0.862 | 8.18 | 7.31 |
| Stage eggs × joint survival | 0.938 | 4.92 | 4.78 |

The alternative **joint survival fraction alone** gives held-region-out retrospective RMSE **4.11 pp**, versus **4.92 pp** when multiplied by stage-matched egg density. The difference is only **0.82 pp**, not a tested biological superiority. But it is sufficient to defeat a claim that temporal stage matching is needed to explain the apparent retrospective association in this sample.

## Held-out-region heterogeneity

The global 4.11-vs-4.92 pp RMSE ordering does **not** repeat in every held-out region. Using the same unbounded OLS fitted on the three remaining regions:

| Held-out region | Observations | Joint survival fraction RMSE | Stage eggs × joint survival RMSE | Lower error |
|---|---:|---:|---:|---|
| Victoria River District | 2 | 4.92 | 4.16 | Stage × survival |
| Barkly Tablelands | 2 | 4.01 | 4.36 | Survival alone |
| Central Queensland | 2 | 1.25 | 6.23 | Survival alone |
| Central Australia | 1 | 5.87 | 4.42 | Stage × survival |

The survival-only model wins **2 of 4** held-out regions, not all four. Its lower pooled RMSE is influenced strongly by the two Central Queensland observations. This makes a general model-ranking claim even less defensible and reinforces the need for an external data source with temporally separated predictor and outcome measurements.

## Ecological interpretation

Across these source regions/seasons, measured egg parasitism is highly variable. The fraction of eggs capable of producing viable beetles is strongly associated with realized final seed destruction, even if raw egg density is removed from the simple linear predictor.

This does **not** mean temporal alignment is biologically irrelevant. The source documents tracking inertia, with egg deposition declining as seed pods mature; stage alignment might matter in other populations or before the survival bottleneck. It means only that the **current seven-point predictive evidence does not identify an incremental timing effect conditional on the conversion filter**.

More detailed biological stories must distinguish:

1. adult/partner encounter and potential oviposition;
2. realized stage-specific egg exposure;
3. parasitism and hatch survival;
4. subsequent seed damage and compensatory plant reproduction.

A better predictor at stage 3 does not demonstrate that the earlier stage 2 timing was causal, and it may be biologically close to the final endpoint.

## Inferential and causal boundaries

- **Seven records / four groups** is inadequate for stable generalization; region blocks are uneven and some predictions are even negative because the source-compatible OLS model is unconstrained.
- Comparing **ten predictors after observing the outcome** induces winner's curse despite leave-one-region-out regression refits.
- **Contemporaneous same-sample measurement:** Table 5 egg parasitism/hatch and final seed fate are measured by dissecting the same late pod samples. The survival fractions are not independently measured ahead of the later damage; these RMSEs are diagnostic reconstruction scores, **not prospective seed-damage forecasting**.
- Parasitism and hatch may depend on climate, local parasitoid assemblages, region and density, so the survival-only association need not be causal.
- Both stage-matched and annual egg density are realized oviposition rather than independently observed adult activity.
- A robust test would need a larger external or withheld dataset, temporal and regional replication, independently defined conversion filters, and prespecified comparisons between adult-only, host-stage-only, survival-only and stage×survival models.
- No dataset, coefficient or original strict-H1 row is promoted by this result.

## Reproducibility

`scripts/build_vanklinken2008_conversion_ablation.py` computes all ten predictors under unchanged region folds, validates source-domain constraints, and writes `data/derived/vanklinken2008_conversion_ablation_metrics.csv`. `--check` and the new tests fail if the generated output drifts.
