# Timing metric contract

Date: 2026-09-16
Status: frozen before extraction beyond IWE001; IWE001 domain audit repaired 2026-09-16

## Why this contract exists

Phenological studies use several non-equivalent timing variables. A signed lag can distinguish whether the plant or its partner is early, whereas an absolute mismatch collapses the two directions. Experimental flowering-date treatments may not measure partner phenology directly. A generic rule of multiplying every variable called `mismatch` by -1 is therefore insufficient for quantitative synthesis.

IWE will preserve the native timing definition before any orientation or pooling.

## Canonical timing classes

Every extracted Tier-A effect must be assigned one `timing_metric_type` in its extraction receipt or queue:

- `overlap_index` — larger native values mean greater temporal overlap by construction;
- `absolute_mismatch` — non-negative distance from temporal matching, irrespective of which partner is earlier;
- `plant_minus_partner` — signed plant timing minus partner timing;
- `partner_minus_plant` — signed partner timing minus plant timing;
- `experimental_plant_shift` — experimental early/late plant timing without a directly measured partner-timing variable;
- `seasonal_position` — observational early/late position in a season, used only when contemporaneous partner availability is measured sufficiently to interpret the contrast;
- `other_registered` — allowed only after a source-specific definition is documented in an extraction receipt.

## Required source definition

For every real effect, the extraction receipt must state:

1. the biological events being compared;
2. the source equation or verbal definition of the timing metric;
3. which sign corresponds to plant earlier, exact matching, and partner earlier;
4. whether the metric is signed or absolute;
5. whether the effect is based on observed partner activity, a timing manipulation, or a proxy.

Source terminology is retained even when it conflicts with terminology in another paper.

## Canonical lag

For signed timing analyses IWE defines an optional canonical lag

`lag_PP = plant_timing - partner_timing`.

Therefore:

- `lag_PP < 0`: the plant is earlier than the partner;
- `lag_PP = 0`: matched focal timing;
- `lag_PP > 0`: the plant is later than the partner.

A source using `partner_timing - plant_timing` must be multiplied by -1 before being represented as `lag_PP`.

`lag_PP` is **not** itself a synchrony score. Moving from -7 to -3 days is greater synchrony, whereas moving from +3 to +7 days is lower synchrony. Consequently, a single linear coefficient on signed lag cannot in general be re-labelled as an effect of synchrony.

## Primary H1 synchrony estimand

For the primary H1 analysis, an effect may be oriented as `greater synchrony -> plant reproductive performance` only when one of the following is justified.

### A. Explicit overlap

The source uses an overlap metric whose biological direction is known. No sign transformation is needed if larger means more overlap.

### B. Absolute mismatch

The source uses `|plant_timing - partner_timing|` or another non-negative mismatch magnitude. The effect is multiplied by -1 so that larger oriented effects correspond to greater synchrony.

### C. One-sided mismatch domain

All observations used for the effect lie on one declared side of matching, and the source biology supports monotonic movement toward or away from zero. The extraction receipt must list the retained domain and show that no opposite-sign observations enter that effect.

For example, with native `partner_timing - plant_timing`, restricting to values `>= 0` means the plant flowers on or before partner appearance. Larger values are then unambiguously greater plant-earlier mismatch and can be oriented toward synchrony by a sign reversal.

### D. Experimental timing contrast with a measured interaction window

An experimental plant-timing treatment may enter H1 if partner availability across treatments is measured and the treatment can be ordered prospectively as more versus less matched. The contrast must be based on that order, not simply on `late > early`.

## Directional mismatch is a separate estimand

When data span both sides of matching, IWE will not force them into one linear synchrony slope. Instead, where data permit, estimate directional responses separately:

- `plant_earlier_mismatch`: `lag_PP < 0`;
- `partner_earlier_mismatch`: `lag_PP > 0`.

This supports a predeclared directional-mismatch analysis motivated by systems in which the two mismatch directions have asymmetric reproductive effects. The 2024 Qilian alpine-community study is an example where pollinator-earlier and flower-earlier mismatch patterns were reported to differ in fecundity impact.

Directional mismatch is a moderator/shape analysis, not a replacement for H1.

## Experimental flowering-time studies

Studies that manipulate flowering date but do not directly quantify a partner timing curve remain scientifically useful, but they are not automatically strict synchrony effects.

They are classified as:

- `strict_window` if contemporaneous partner availability allows treatments to be ordered by matching;
- `direct_timing_sensitivity` if flowering time is experimentally changed and reproductive output is measured but the partner window is not explicitly recoverable.

The latter may enter a predeclared sensitivity analysis and may support statements about seasonal timing effects, but not the strict claim that phenological synchrony caused the response.

## IWE001 source-specific convention and repair

Kudo & Ida (2013) Appendix A reports `Mismatch day` as bumblebee first-detection date minus flowering-onset date. Thus its native sign is `partner_minus_plant`:

- positive: plant flowers before bee detection;
- zero: matching onset/detection;
- negative: bee detection precedes flowering.

The dataset contains observations on both sides of zero. Therefore the original all-row signed correlations cannot be used as strict H1 synchrony effects.

The strict-H1 IWE001 extraction is now restricted to rows with native `Mismatch day >= 0` within each population. This satisfies the one-sided-domain rule: within the retained rows, increasing native mismatch always means moving farther from matching on the plant-earlier side. Negative-mismatch rows are preserved in the source-row audit for directional analyses but are excluded from the strict-H1 effect.

See `docs/EXTRACTION_IWE001.md` and `data/extraction/source_rows/IWE001_appendix_A1.csv`.

## IWE002 source-specific warning

Kudo & Cooper (2019) describes mismatch as flowering onset minus bee emergence, i.e. `plant_minus_partner`, the opposite algebraic sign from the Kudo & Ida (2013) Appendix-A column. The two publications therefore cannot share a sign transform merely because both use the word `mismatch`.

Before IWE002 effects are added to `direct_effects.csv`, the extracted source variable must be converted to the canonical `lag_PP` convention and its one-sided/absolute treatment must be documented. IWE001/IWE002 population-year overlap must also be resolved before both contribute to a pooled result.

## Claim boundary

IWE will never treat:

- signed lag as absolute synchrony without checking its domain;
- `early` or `late` as inherently good/bad or matched/mismatched;
- calendar date as partner synchrony unless partner availability is measured;
- first detection, peak abundance and full activity overlap as interchangeable timing events;
- occurrence-derived phenology as direct interaction timing.

A study can remain `unresolved` or move to a timing-sensitivity analysis if its timing definition cannot support the strict H1 estimand. That is preferable to changing the estimand after seeing the result.
