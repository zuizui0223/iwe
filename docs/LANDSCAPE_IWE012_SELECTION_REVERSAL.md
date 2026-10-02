# IWE012 — antagonist-mediated reversal of flowering-time selection

Date: 2026-10-02  
Study: Valdés & Ehrlén, *Caterpillar seed predators mediate shifts in selection on flowering phenology in their host plant*  
DOI: `10.1002/ecy.1633`  
Status: quantitative signed-selection evidence; not a strict partner-window effect.

## Biological object

The study followed *Gentiana pneumonanthe* across 20 populations for two years and related population variation in phenotypic selection on flowering phenology to occurrence of the predispersal seed predator *Phengaris alcon*.

Fitness is the number of intact fruits, relativized within populations. Traits were standardized within populations.

The source interpretation fixes the sign of the reported phenology gradient:

- positive mean beta in predator-absent populations = selection for earlier flowering;
- negative mean beta in predator-present populations = selection for later flowering.

## Source-reported gradients

| Year | Predator absent | Predator present | Descriptive present-minus-absent shift |
|---|---:|---:|---:|
| 2010 | +0.22 ± 0.15 (95% CI half-width) | -0.19 ± 0.15 | -0.41 |
| 2011 | +0.30 ± 0.17 (95% CI half-width) | -0.10 ± 0.11 | -0.40 |

The study directly tests the change in phenology selection with predator context:

- 2010 Predation × Phenology: chi-square = 15.38, p < 0.001;
- 2011 Predation × Phenology: chi-square = 14.95, p < 0.001.

The derived -0.41 and -0.40 values are retained as descriptive signed shifts only. IWE does not construct a sampling variance for those differences from the printed group summaries because the required covariance/estimator information is not supplied by those means and confidence intervals.

## Mechanistic support

Within predator-present populations, earlier floral development increased attack probability in both study years. The source path analysis also reports that earlier phenology reduced fitness through attack probability and predation intensity.

Thus the direction reversal is not merely a between-population sign difference: within-population attack patterns are consistent with the seed predator preferentially imposing cost on earlier-flowering plants.

## Claim boundary

This study supports:

> occurrence of the seed predator is associated with a reproducible reversal of the directional flowering-time selection surface from earlier to later flowering, with source-reported Predation × Phenology tests in both years.

It does not by itself identify the complete adult-butterfly activity curve or a strict IWE synchrony effect. Predator presence differs among populations, so environmental covariance among populations remains a limitation for causal attribution despite the within-population attack mechanism.

Both years share one dependence cluster, `DEP_IWE012_GENTIANA`.

## Pivot consequence

IWE012 shows that an antagonist can rotate the calendar-time fitness surface rather than merely reduce mean fitness. Together with factorial evidence from *Gymnadenia*, where herbivores shift selection toward earlier flowering, it also shows why a universal "antagonists favor later flowering" rule is untenable. The candidate generality is window-relative escape, not calendar direction.
