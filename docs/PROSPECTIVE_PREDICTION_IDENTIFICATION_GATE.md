# IWE prospective prediction-identification gate

Date: 2026-10-08
Status: mandatory interpretation gate for stage-specific final-fitness claims on the pivot branch. Original strict-H1 corpus remains unchanged.

## Central ecological test

> Does knowing **which encounters become biologically effective interactions** improve out-of-sample prediction of final plant reproduction beyond knowing the plant calendar and adult-partner availability alone?

A stage-specific coordinate is a mechanistic description until it passes temporal provenance, biological-unit linkage and validation gates. Extra detail and better retrospective fit alone are insufficient.

## Separate the axes

1. **What was observed?** Independent adult flight/activity; realized oviposition; larval establishment; host tissue/vulnerability; parasitoid suppression; mature seed/fruit fate.
2. **When was it observed?** Before final reproductive outcome; at the same late destructive collection as the outcome; after outcome; or not source-verifiable.
3. **At which grain?** Plant, flower, fruit, field, plot-year or region-season; do not promote nested samples into independent replicates.
4. **How was the coordinate chosen?** Response-blind; defined from prior source; or constructed/selected after viewing final outcomes.
5. **How was the model tested?** Untouched future year/region/study; blocked CV with prespecified models; within-source folds only; or explanatory fit.

## Current quantitative examples

| Programme | Temporal provenance | Final endpoint | Paired comparison | Correct status |
|---|---|---|---|---|
| **Parkinsonia–Penthobruchus** (van Klinken & Flack 2008) | Annual/late realized egg exposure; egg parasitism/hatch and seed fate assessed on the **same late pod collection** | Seeds consumed | Annual egg density vs stage eggs vs late survival filters, 7 region-seasons/4 regions; ten-model ablation chosen after seeing outcome | **Retrospective biological explanation only**; not a forward prediction or proof of incremental stage timing |
| **Pisum–Cydia** (Riemer et al. 2024) | Independent first-male trapping and flowering recorded before terminal seed damage | % damaged pea seeds in 88 fields | Flowering-only vs adult-arrival × flowering GAM; field-wise LOOCV RMSE 9.20 → 7.36 pp | **Prospective-in-variable-order paired diagnostic**; no adult-only or effective consumer-stage comparator, no held-out-year validation |
| **Cardamine–Anthocharis** (Davies & Saccheri 2024) | Flower-to-egg host stage and active-egg filter prior to final fate; source female adult distribution incomplete | Dehiscence/whole-ramet consumption, intact reproductive units | Ecotype phase-to-fate; modeled active-egg fitness trough | **Positive stage/final-fate association**, but missing same-unit raw adult-flight-vs-filter predictive comparison |
| **Silene–Hadena** (Kula 2012) | Observed flowering and oviposition; first detected larvae are already mobile rather than first feeders | Flower/fruit predation; no re-extractable net successful-fruit endpoint | Opposite synchrony–predation signs across two years; descriptive detection margin −11.3 and +0.3 days, latter spans zero under maturation-only uncertainty | **Mechanistic hypothesis**, not a confirmed safe-threshold effect or final-fitness test |
| **Aucuba–Asphondylia** (Imai et al. 2006) | Adult emergence monitored; oviposition timing experimentally shifted | Gall induction causing complete seed failure | Early vs late fruit-stage exposure | **Causal timing-to-final-fate positive**, no paired simple/adult-only vs delayed-filter predictive comparison |
| **Wheat midge** (Wu 2015 / Wise 2015) | Adult occurrence monitored or experimentally imposed relative to susceptible wheat stage | Final yield loss / seed damage | Source timing-stage effects | **Stage-specific final-endpoint positives**, but not the required prospectively compared downstream conversion models |

## Biological endpoint boundaries are not model-comparison nulls

Two independently sourced studies restrict the ecological mechanism, but do **not** furnish negative paired M2/M4/M5 prediction tests:

- **Posledovich et al. 2015**, DOI 10.1111/1365-2656.12417: experimental host-stage and temperature shifts affected larval performance, while the reported binary mature-seedpod-outgrowth GLM selected host species identity. The outgrowth GLM was fit to initial hosts replaced by a second host plant, not to every original host. It does not count all viable seeds and it does not compare stage-specific versus calendar/adult-only models on untouched observations.
- **Valdés & Ehrlén 2021**, DOI 10.1002/ecy.3466: in a 21-year *Lathyrus* series, variation in the flowering–seed-predation covariance did not significantly moderate flowering-time selection (estimate -0.033, 95% CI -0.101 to 0.037). There is no measured delayed consumer-stage predictor or paired M2/M4/M5 predictive comparison, and a non-significant coefficient is not evidence of equivalence.

The registry therefore records both as `boundary_null` with `paired_simpler_vs_stage_comparison=no`. Only comparisons explicitly registered as `paired_model_null` or `paired_realized_positive` may enter paired model counts. The latter may remain retrospective, so paired does not mean confirmatory.

## Mandatory falsification comparators

For a newly recovered source with genuinely pre-outcome observations and a common biological unit, predeclare:

- M0 — source-reported non-timing baseline/environmental predictors;
- M1 — host phenological timing alone;
- M2 — independent adult-partner timing (or adult + host timing, with an explicit adult-only model);
- M3 — oviposition or stage-matched encounter, if measured in advance;
- M4 — source-defined pre-outcome survival / host filter alone;
- M5 — stage-matched exposure × filter, with functional form fixed before seeing final reproduction.

Test whether M5 **really** beats M4 and M2 in held-out, independent biological units; do not substitute 'the deepest model beat M1' for incremental identification. Ensure there are enough independent seasons/regions for outer validation and use group-wise or temporal holdout. Parameter tuning and predictor selection must be nested within training data or frozen from a distinct source.

## Fail-closed decisions

- No retrospective predictor measured alongside seed fate can be called a prospective forecast.
- No statistic from a selected model after examining test outcomes can be described as an unbiased validation estimate.
- A measured conversion filter may be temporally downstream of eggs but need not be causally exogenous; parasitoid environment, consumer density and host condition can confound it.
- **The latest surviving consumer count need not be a sufficient damage proxy.** A consumer may injure the host before dying, or induce a costly plant response. Chavalle et al. (2015) report improved harvested yield after midge suppression even in a resistant wheat cultivar, but do not independently identify early feeding versus induced defence. An early-attack/host-response comparator is required where such persistent effects are plausible.
- Similar final outcomes can arise through different mechanisms; null and buffering controls (Posledovich, Lathyrus, Ulex, Mertensia, Trollius) remain mandatory.
- Prediction can be of final seed loss, viable seeds or integrated reproductive success; these responses are **not automatically interchangeable** and each model comparison must use one fixed endpoint and unit.

## Next experimental/archival unlock

Prioritize a study with **independent adult occurrence, source-defined host susceptibility, pre-fate consumer survival/establishment, and later intact/viable seeds for the same field/plant/date**, ideally with independent years or sites untouched by model selection. When final damage can persist after consumer mortality, recover **early-attack intensity or pre-harvest host-response measurements** as well: compare the late-survivor-only model against a prespecified early-impact-trace model, not just the stage-matched product. Without such data, retain the ecological conversion-bottleneck hypothesis as exploratory rather than promoting PR #62's full prediction claim.
