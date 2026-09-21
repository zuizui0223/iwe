# Effect-size contract

## Orientation

Every **strict primary** effect is oriented so:

> positive = greater phenological synchrony is associated with higher plant reproductive performance.

Orientation is not inferred from a source word such as `mismatch` or `lag`. The native timing definition, analysis class, and observed/design domain must first satisfy `TIMING_METRIC_CONTRACT.md`.

Examples:

- an `overlap_index` whose larger values mean more overlap keeps its sign;
- an `absolute_mismatch` is oriented by multiplying the native effect by `-1`;
- a signed `plant_minus_partner` or `partner_minus_plant` slope can be oriented as synchrony only on a demonstrated one-sided domain;
- a signed lag with unknown or two-sided domain is not admitted to the strict H1 dataset.

The original native effect and timing fields remain preserved.

## Registered effect families

The first release accepts these `effect_family` values:

- `standardized_slope`
- `fisher_z`
- `standardized_mean_difference`
- `log_response_ratio`

Effect families are not silently converted into one another. The primary software can summarize a common family or a table whose values have already been placed on a justified common scale outside IWE. Cross-family pooling requires a separately documented conversion rule.

## Required fields for an extracted effect

- `effect_id`
- `study_id`
- `dataset_id`
- `dependence_id`
- `plant_taxon`
- `animal_taxon`
- `interaction_type`
- `evidence_tier`
- `phenology_source`
- `timing_metric_type`
- `timing_analysis_class`
- `timing_domain`
- `exposure_direction`
- `outcome_family`
- `effect_family`
- `effect_native`
- `variance_native`
- `sample_size`
- `source_id`

Optional contextual fields include site, year, latitude, elevation, island status, specialization, redundancy, and notes.

## Allowed values

`interaction_type`:
- `mutualist`
- `antagonist`
- `mixed_pollinating_seed_predator`

`evidence_tier`:
- `A`
- `B`
- `C`

`phenology_source`:
- `direct_interaction`
- `direct_activity`
- `experimental_timing`
- `occurrence_proxy`

`timing_metric_type`:
- `overlap_index`
- `absolute_mismatch`
- `plant_minus_partner`
- `partner_minus_plant`
- `experimental_plant_shift`
- `seasonal_position`
- `other_registered`

`timing_analysis_class`:
- `strict_window`
- `direct_timing_sensitivity`
- `directional_mismatch`
- `unresolved_for_strict_h1`
- `proxy_only`

`timing_domain`:
- `nonnegative`
- `plant_earlier_only`
- `partner_earlier_only`
- `both_sides`
- `ordered_by_measured_window`
- `unknown`
- `not_applicable`

`exposure_direction`:
- `synchrony`
- `mismatch`

## Variance rule

Primary meta-analysis requires a finite positive sampling variance. Missing variance is unresolved and is never replaced automatically by a mean, median, or guessed standard error.

## Duplicate rule

`effect_id` must be unique. Multiple effects may share a `dependence_id`; this explicitly records correlated evidence. Duplicate source rows without an explicit dependence identifier fail validation.

## Tier and strict-H1 rule

Tier A identifies direct matched phenology–fitness evidence, but Tier A alone is not sufficient for the strict H1 synchrony estimand.

`build_primary_dataset()` requires both:

- `evidence_tier == "A"`; and
- `timing_analysis_class == "strict_window"`.

Tier-A rows classified as `direct_timing_sensitivity`, `directional_mismatch`, or `unresolved_for_strict_h1` remain valid extracted evidence but cannot enter the strict H1 pool. Tier B remains mechanistic/context evidence. Tier C is potential-overlap proxy evidence and must use `proxy_only`; it cannot be promoted by having a small variance or large sample size.
