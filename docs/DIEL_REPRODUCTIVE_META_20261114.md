# Diel reproductive contribution: a source-precision reanalysis

## Result and scope, 2026-11-14

This is an exploratory reanalysis of the **published Kendall & Nicholson source dataset**, not independent new observations and NOT a meta-analysis of artificial-light treatments. Primary publication: DOI [10.1111/ele.70036](https://doi.org/10.1111/ele.70036). The original paper already compared day/night/open access. The extension here is variance-aware, publication-grain synthesis of four-arm nonadditivity, with contrast-specific coverage and explicit covariance uncertainty. It complements, rather than independently replicates, ALAN draft PR #58.

Authentic public source: 1,652 treatment rows, 140 source publication IDs; Git blob `39a82d966afcdde670603add1c881ace8791ffe9`, SHA256 `1d9c4c778206584130308b99ba21d902b0ccf1047118dfcf52abaec9d652e2aa`. The original final paper used 135 studies after its own analysis exclusions. Our bounded contrasts and transparent eligibility differ; we do not claim to reproduce that paper's phylogenetic model or its exact final study set.

**Available means:** 344 distinct source cells / 114 publication IDs / 114 source plant taxa. A cell is study × plant/cultivar × locality/site-period × coordinates × year/month range × reproductive metric/units × additional treatment. Means are never averaged across different cultivars, source site-periods or additional interventions.

**Usable source precision:** 276 cells / 96 publication IDs / 94 plant taxa contribute to at least one of the six primary models. A single cell can inform multiple contrasts; these counts are unions, not a sum of independent effects. Only source SE or SD with integer n >= 2 is used. SD converts to SE via SD/sqrt(n). Unsupported CI/range labels, unknown n and zero first-order variances stay outside inverse-variance models, but their valid means remain in descriptive selection checks.

**Four-arm coverage:** 180 source cells have valid open, day-only, night-only and full-exclusion means. We do NOT require all four arms or all four errors for a contrast that mathematically uses only two. A missing full-exclusion error therefore does not exclude a valid open-versus-day comparison. This coverage refinement was made during exploratory development; both minimal-arm and four-arm-complete results are retained. There was no prospective preregistration.

## Estimands and replication

Let O=open day and night, D=day-only, N=night-only, and C=complete visitor exclusion, using the identical original reproductive endpoint and units within each cell.

- Marginal night-access contrast: `M_N=(O-D)/(O+D)`. Positive means open access outperforms day-only access.
- Marginal day-access contrast: `M_D=(O-N)/(O+N)`. Positive means open access outperforms night-only access.
- Four-arm nonadditivity: `I=(O+C-D-N)/(O+C+D+N)`. Negative means subadditive outcomes on the original measurement scale. It does not prove dynamic pollinator compensation, ecological redundancy, or a specific physiological mechanism.

These bounded indices are **not percentages**. Zero observed outcomes are retained when the denominator is positive; 0/0 remains unestimable. No arbitrary continuity corrections are added.

For f=(a'm)/(b'm), the derivative for each source arm mean is `g_i=(a_i-f*b_i)/(b'm)`. Source variances and correlations between arms are not all known. The primary first-order sampling variance upper bound is `(sum(abs(g_i)*SE_i))^2`, which follows from the covariance Cauchy-Schwarz bound. It is conditional on the reported SE/SD and sampling n being appropriate. It is not an empirical estimate of the missing covariance.

Multiple cell contrasts within a publication and reproductive endpoint are first averaged equally. Their unknown cross-cell covariance is again bounded: publication variance upper bound `(sum(cell_SE)/number_cells)^2`. Each publication then contributes one effect per model, not one independent trial per plant or fruit. Publication IDs may still share experimental programmes and phylogenetic dependence is not modelled.

Fit intercept-only REML heterogeneity and modified Knapp-Hartung t intervals using `q*=max(1,q)`; see Röver, Knapp & Friede 2015, DOI [10.1186/s12874-015-0091-1](https://doi.org/10.1186/s12874-015-0091-1). The six primary tests (three contrasts × two endpoints) use Holm correction. The displayed 95% intervals are individual-model intervals, not simultaneous intervals. Fruit and seed outcomes are never pooled together.

An upper bound on sampling variance does NOT guarantee a monotonically wider final REML interval: changing sampling variances changes heterogeneity and study weights. Therefore the independent-arm/cell approximation is retained as a sensitivity, alongside equal-publication and equal-family bootstraps.

## Primary model results

| Endpoint | Contrast | Source cells | Publications | Mean index | 95% mKH CI | Holm p across six |
|---|---|---:|---:|---:|---|---:|
| Fruit set | Night marginal | 137 | 62 | +0.28680 | +0.20191 to +0.37168 | 3.64e-8 |
| Fruit set | Day marginal | 146 | 66 | +0.15206 | +0.09023 to +0.21390 | 2.57e-5 |
| Seed set | Night marginal | 109 | 55 | +0.22507 | +0.14206 to +0.30808 | 6.72e-6 |
| Seed set | Day marginal | 116 | 60 | +0.08961 | +0.01589 to +0.16333 | .03611 |
| Fruit set | Four-arm nonadditivity | 85 | 48 | -0.06575 | -0.12610 to -0.00541 | .03611 |
| Seed set | Four-arm nonadditivity | 40 | 28 | -0.07486 | -0.10897 to -0.04076 | .000346 |

The four positive marginal contrasts persist in the nominal intervals of every leave-one-publication-out primary refit. Their largest single-publication weights are about 2.1–2.4%, so no one source accounts for those marginal conclusions. Equal-publication and equal-family bootstrap checks also retain positive marginal means, including the broader panels lacking usable variance. These bootstrap sensitivity intervals are exploratory and not family-wise multiplicity adjusted.

The prediction intervals for all four marginal effects span zero. Thus a positive average across the represented literature does not mean that every species/site depends on both time windows, and does not estimate a future ALAN response.

## Important sensitivity failures, not suppressed

- With reported daytime/nighttime access durations within 10% of each other, the seed daytime-marginal result is unresolved: 15 publications, +0.0574, CI -0.1325 to +0.2474. Other such duration-balanced marginal comparisons remain positive at nominal 95%. This does not establish a between-subset interaction.
- Fruit-set nonadditivity is fragile. It crosses zero in 6 of 48 leave-one-publication-out fits, and in native-only, explicit-unit, balanced-duration, unweighted-publication and family-level checks. Do not claim a universal fruit-set redundancy effect.
- Seed-set nonadditivity remains negative after every one-publication deletion and under the independent-variance sensitivity, but the primary bound-weight fit places 39.9% weight on one publication (`Jaca_2020`) and estimates tau2=0. The precision-panel family-balanced bootstrap (19 families) crosses zero (approximately -0.127 to +0.006). The broader mean-only family panel is negative, but differs in source coverage. Treat this as suggestive scale-dependent subadditivity, not definitive pollinator replacement.
- Original error labels were read as supplied; this analysis did not verify all SE, SD, sample units and denominators against every primary study. Original n may represent flowers, fruits or plants.
- Some source outcome units are literal NA. They remain within exact matched source cells, with an explicit-unit sensitivity. Seed-set sources include different biological denominators, so neither a pooled seed count nor a universal seed-loss percentage is inferred.

## Consequence for the IWE–ALAN–chocho connection

The source literature supports a constrained conclusion: **when access is limited to daytime only, average reproductive outcome is lower than with day-and-night access; the converse also holds on average but is weaker for seed outcomes under balanced durations**. Existing daytime visitors cannot simply be assumed to deliver the full reproductive outcome when nighttime access is removed.

However, excluding an entire time window is not equivalent to experimentally changing illumination, attracting or repelling visitors, shifting flowering phenology, or allowing behavioral compensation after a disturbance. The new results are a functional baseline against which ALAN mechanisms can be tested, not ALAN effect sizes.

IWE's Lu access-specific observation (night-only damage differs from open-access response) and this multi-study exclusion baseline ask related but different questions. Four-arm nonadditivity may reflect saturation, wind/autogamy, handling or bag microclimate as well as partial overlap of visitor functions. It cannot establish which alternative visitor has restored pollen delivery.

`chocho` adds potential larval-host geography, not an observed pollen or seed endpoint. No global nightlight×host-range coefficient, island-mainland light manipulation, or strict IWE seasonal-synchrony H1 effect is added. Native-only comparisons concern source plant status, NOT island status.

## Reproduction and outputs

```bash
python -m pytest -q tests/test_diel_reserve_meta.py
python scripts/run_diel_reserve_meta.py --author /path/to/DvN_LiteratureDataClean_2024-09-13.csv --traits /path/to/SppTraitData_clean.csv --out-dir results/diel-reserve
```

The original public sources are verified against their Git blobs before modelling. Exports are aggregate-only: all primary/sensitivity models, sample-selection accounting, leave-one-publication-out ranges, publication/family bootstrap summaries and source/interpretation receipt. Raw literature notes, source sites and source rows are not copied into the analytical result artifact.
