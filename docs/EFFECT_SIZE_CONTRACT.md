# Effect-size contract

## Orientation

Every primary effect is oriented so:

> positive = greater phenological synchrony is associated with higher plant reproductive performance.

If a source predictor is mismatch, lag, or absolute peak difference, the extracted native effect must be multiplied by `-1` during orientation. The original value and exposure direction remain preserved.

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

`exposure_direction`:
- `synchrony`
- `mismatch`

## Variance rule

Primary meta-analysis requires a finite positive sampling variance. Missing variance is unresolved and is never replaced automatically by a mean, median, or guessed standard error.

## Duplicate rule

`effect_id` must be unique. Multiple effects may share a `dependence_id`; this explicitly records correlated evidence. Duplicate source rows without an explicit dependence identifier fail validation.

## Tier rule

Only evidence tier `A` may enter the primary meta-analysis. Tier B remains mechanistic/context evidence. Tier C is potential-overlap proxy evidence and cannot be promoted by having a small variance or large sample size.