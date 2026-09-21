# IWE081 extraction receipt — alpine plant community × bees/flies

Source: Mizunaga Y, Kudo G. 2017. *A linkage between flowering phenology and fruit-set success of alpine plant communities with reference to the seasonality and pollination effectiveness of bees and flies*. Oecologia 185:453–464. DOI `10.1007/s00442-017-3946-9`.

Open author manuscript: Hokkaido University HUSCAP, handle `2115/71818`.

Status: **unresolved strict-H1 mutualist candidate; the direct pollinator-frequency → fruit-set relationship is source-defined, but its coefficient/covariance or raw population table has not yet been recovered**.

Interaction class: `mutualist`.

Dependence ID: `DEP_IWE081_ALPINE_BEE_FLY`.

## Why this is unusually close to strict H1

The study measured, across alpine plant populations and years:

- population flowering phenology;
- seasonal visitation frequencies of bumble bees, syrphid flies and non-syrphid flies;
- natural fruit-set success;
- pollination-system assignment of focal plant populations.

The source does not merely regress fruit set on calendar week. For the direct pollinator-effect analysis it estimates the visitation frequency expected at each population's flowering peak and relates that partner-availability value to natural fruit set.

This closes the biological chain:

```text
plant flowering peak × measured pollinator activity curve
-> pollinator frequency at that flowering peak
-> natural fruit-set success
```

Bee-pollinated and fly-pollinated populations are analysed separately because the source shows strong differences in pollination effectiveness.

## Primary timing exposure

The primary exposure is the **source-estimated visitation frequency of the appropriate pollinator guild at the focal population's flowering peak**.

It is not:

- flowering week alone;
- total seasonal visitor abundance;
- a pooled bee+fly index;
- a post-hoc absolute mismatch reconstructed from calendar dates.

Larger exposure values mean that the focal population flowers when more effective partner activity is available. Under IWE this is a direct interaction-window availability metric with `exposure_direction = synchrony`.

## Primary outcome

The primary outcome is the source's natural fruit-set success for the same plant population/year unit.

Hand-pollination or pollen-limitation manipulations, if present in ancillary source material, cannot replace the natural reproductive endpoint for this strict effect.

## Dependence structure

The preferred quantitative unit is:

`plant population × year × pollinator-system lane`.

Rows from the same year, study site/community and pollinator guild are not independent publications. All quantitative rows from this article share `DEP_IWE081_ALPINE_BEE_FLY`.

Bee- and fly-pollinated lanes may be retained as dependent subeffects if source covariance/raw data permit; they do not count as independent programmes.

## What is already recoverable from the article

The accepted manuscript documents:

1. year-specific seasonal models for pollinator visitation frequency;
2. population flowering peaks;
3. natural fruit-set values;
4. direct logistic relationships between pollinator visitation frequency at flowering peak and fruit-set success.

The plotted direct relationship is biologically admissible. However, the article does not print the direct visitation-frequency → fruit-set logistic coefficient together with its standard error/covariance.

The seasonal visitation and fruit-set model tables cannot be algebraically combined into a sampling variance for the direct relationship without the covariance/raw population-level observations.

## Quantitative admission routes

IWE081 may enter `direct_effects.csv` only if one of these is recovered prospectively:

1. the population/year table underlying the direct relationship, permitting a registered correlation/model coefficient and sampling variance;
2. the source logistic coefficient for visitation frequency → fruit set plus its SE/covariance;
3. a supplementary/source repository containing sufficient population-level fruit-set denominators and partner-frequency estimates to refit the source relationship.

If multiple effect rows are produced, they retain study/year/guild dependence rather than being counted as independent programmes.

## Figure-derived prediction warning

Source Figure 4 is biologically useful but is **not** a set of new independent empirical synchrony observations. The plotted visitation-frequency and fruit-set values are generated from the source's seasonal models at weekly intervals. Multiple plotted weeks therefore share the same fitted model, source populations and year-level data.

IWE will not:

- count Figure-4 weekly prediction points as independent observations;
- compute a Fisher-z variance as `1/(number_of_plotted_points - 3)`;
- use a near-perfect correlation between two fitted seasonal curves as if it were a sampling correlation among independent populations;
- infer the direct coefficient covariance by algebraically combining the separate visitation-vs-week and fruit-set-vs-week model tables.

A quantitative strict effect still requires the underlying population/year observations or the source's direct partner-frequency coefficient with valid uncertainty.

## Figure-digitization rule

The current primary route does **not** digitize the plotted direct relationship by eye.

A later reproducible figure-extraction route is allowed only if, before extracting effect values:

- the numerical calibration procedure is frozen;
- all plotted population points can be recovered without subjective selection;
- enough denominator/uncertainty information exists to obtain a defensible sampling variance;
- the reconstructed source model is validated against printed source summaries.

If those conditions are not met, the figure remains visual evidence rather than a meta-analytic effect.

## Current source-recovery status

The peer-reviewed publication and HUSCAP accepted manuscript are public and source-eligible.

A targeted public-source search has not yet identified a separate raw population dataset or supplementary table exposing the direct logistic coefficient/covariance. The quantitative blocker is therefore narrow: **effect/variance recovery**, not biological eligibility.

## Claim ceiling

At present IWE081 supports:

> in a published alpine-community study, plant populations flowering under greater measured activity of their effective pollinator guild had higher natural fruit-set success, and this direct partner-availability relationship differed between bee- and fly-pollinated systems.

It does not yet contribute an independent Fisher-z or other registered common-scale programme to H1.
