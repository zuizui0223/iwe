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
- `log_rate_slope_per_day`
- `log_odds_ratio`

Effect families are not silently converted into one another. The primary software can summarize a common family or a table whose values have already been placed on a justified common scale outside IWE. Cross-family pooling requires a separately documented conversion rule.

### `log_rate_slope_per_day`

This family is reserved for a continuous one-sided timing exposure measured in **days**, where the response is modeled on a log scale or with a count GLM using a log link. The native effect is:

`change in log expected reproductive output per additional day of mismatch/delay`.

Examples include experimentally delaying pollinator arrival after the onset of floral receptivity and modeling seed counts with a Poisson log-link model.

A reconstructed slope may enter this family only when source group means, sampling variances and timing values are sufficient to obtain a transparent weighted log-linear slope. The reconstruction formula and source rows must be documented in an extraction receipt.

`log_rate_slope_per_day` is **not interchangeable** with a two-group `log_response_ratio`. It must be analyzed separately unless a prospective conversion to a common exposure scale is registered.

### `log_odds_ratio`

This family stores a source-model coefficient from a binomial/logit model when a declared two-state timing contrast has been independently ordered as lower versus higher plant–partner synchrony. The native effect is the log odds ratio for plant reproductive success in the higher-synchrony state relative to the lower-synchrony state.

The timing order must be established from partner activity/interaction measurements, not from the reproductive outcome itself. A log-odds effect remains on its source-native scale and is not silently converted to Fisher-z, SMD, or a log response ratio.

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
