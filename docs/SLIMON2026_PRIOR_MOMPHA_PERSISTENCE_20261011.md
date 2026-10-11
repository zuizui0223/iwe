# Slimon 2026: previous flower signal after previous visible Mompha detection

Date: 2026-10-11. Original data: Slimon & Agrawal (2026), [Zenodo DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509).
Pinned original `Freese Stats.zip` MD5:
`151bbd516fc0032af2a2598cb5529c78`.

Executable empirical follow-up:
`scripts/analyze_slimon2026_mompha_persistence.py`.
Numerical source receipt:
`data/source_reconstructions/slimon2026_prior_mompha_persistence.csv`.
GitHub Actions source-run:
https://github.com/zuizui0223/iwe/actions/runs/38107320936.

**Nonpromoting, outcome-exposed exploratory source reanalysis**, not a
causal test of a known flower-bud exposure date and not prospective
validation of predicted intact seed fitness.

## Why it is biologically informative

The previous source audit (PR #93) found stronger association of
newly observed `Mompha>0` with open flowers **seven days before**
than with the current or following week's open flowers, after
simultaneously controlling for source plant ID and the exact 2023
survey date.

That temporal association could be a **carryover of a visible
Mompha stage** rather than a delayed effect of flower/bud phenology.
If insect detections are persistent, a positive previous-week
Mompha record may explain the present-week detection without
invoking earlier floral stages. This new audit adds that original
observed previous-week Mompha state *as a separate covariate*.

Importantly, a plant's `new Mompha` column is the original
newly **visible host-associated observation**, not a reliable
adult presence/oviposition timestamp, a tracked individual insect,
or a known egg date. Conditioning on previous observed Mompha
may itself control a biological mediator of earlier host conditions,
and consequently cannot identify direct vs indirect causal effects.

## Original biological units and models

Both originally labelled `exp1` and `exp2` flowering observations
are dated **2023** and represent components of **one programme**,
not two independent year-level replications.

Only the original source plant × survey DOY records at exact
`t−7`, `t`, and `t+7` are used; prior Mompha is joined
from the **same original plant exactly seven days before**.
Missing survey dates, counts or source plant IDs are neither
interpolated nor zero-filled. The original source ZIP byte MD5
must match before any numerical analysis.

For each original experiment separately, four prespecified
plant+date fixed-effect **descriptive** models of current
`Mompha_visible>0` are compared on the same sample:

1. Flower states: open at `t−7`, `t`, `t+7`.
2. Prior visible Mompha status alone: `Mompha_visible(t−7)>0`.
3. Previous flower status together with prior visible Mompha.
4. Previous Mompha together with all three floral states.

For sensitivity, fit the same four predictors to
`log1p(number of newly visible Mompha observations)` rather
than a binary positive threshold. These numerical counts are
neither independently marked insects nor exact oviposition counts.

Plant-cluster bootstrap of the four-variable model resamples
**original plants**, keeping all their longitudinal visits together.
There are 120 deterministic replicates; 2.5–97.5 percentiles are
**descriptive source-resampling stability intervals, not
confirmatory CIs**. Survey days, site-level environment and
time-varying bud availability are not independently resampled.

## Source-backed result

| Source component | exp1 | exp2 |
|---|---:|---:|
| Complete-case source plants | 148 | 123 |
| Source plant × date rows | 1,055 | 731 |
| Current Mompha-positive plant-visits | 390 | 199 |
| Prior-week Mompha-positive plant-visits | 388 | 216 |
| Previously observed flowering slope, without prior Mompha | +0.255 | +0.183 |
| **Previous flowering slope, adding prior Mompha** | **+0.229** | **+0.177** |
| Prior visible Mompha stage slope, all floral states included | +0.201 | +0.211 |
| Current open-flower slope in extended model | +0.178 | +0.051 |
| Following-week open-flower slope in extended model | +0.022 | −0.053 |
| Incremental in-sample FE R², original three floral statuses | 0.0914 | 0.0378 |
| Incremental in-sample FE R², adding previous Mompha | 0.1289 | 0.0841 |

Descriptive 120-plant-resampling percentile intervals:
- previous flower with prior Mompha included:
  exp1 **[+0.175, +0.289]**, exp2 **[+0.086, +0.267]**;
- previous visible Mompha:
  exp1 **[+0.132, +0.277]**, exp2 **[+0.145, +0.264]**.

Thus the floral-stage association changes from +0.255 to +0.229
in exp1, and from +0.183 to +0.177 in exp2. Its complete
disappearance is **not supported by this sensitivity test**.
On the same source sample, previous Mompha has a separate
positive association with current visible Mompha, and improves
the in-sample model beyond the floral states.

The secondary `log1p(new visible Mompha count)` fit also
returns positive prior-flower coefficients:
**+0.361 (exp1)** and **+0.355 (exp2)** after including
previous Mompha, current open and future open. This suggests
the direction is not only an artefact of coding zero vs
positive detections. On this log-count scale the coefficients
must **not** be described as differences in individual insects
or attack rates.

## Ecology, limits and next critical evidence

The direct observation-level interpretation is:

> Earlier open-flower status and a previously detected Mompha
> stage **both** carry information about newly visible Mompha
> on the focal plant a week later, even after stable plant and
> exact survey-date adjustment.

This is consistent with **host reproductive state persisting
across surveys**, **flower-bud availability preceding anthesis**,
**stage-dependent insect detection latency**, **existing insect
populations carrying over** and combinations thereof. It does
NOT distinguish these mechanisms or prove that prior open
flowers caused current insect emergence.

It also cannot identify the actual susceptible flower-bud
window, a particular egg/larva cohort, true adult Mompha
activity/flight, or mature intact seeds after predation.
The source's `fitness_seed` is constructed using weighted
fruit damage and genotype-specific coefficients; we did not
convert it into raw surviving seeds.

The next **discriminating** original measurements would be
dated bud counts, first oviposition/initial gall detection,
direct sequential larval development, and final per-flower
intact seed output with source plant/flower keys. Until then,
avoid extrapolating a 7-day **statistical observation lag**
into a 7-day **biological oviposition-to-visible-larva interval**.

**Admission:** zero new strict antagonist-H1 effects or
independent clusters; the strict evidence remains mutualist 2,
antagonist 0, mixed 0.
