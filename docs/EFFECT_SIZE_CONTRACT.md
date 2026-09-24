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
- `log_odds_ratio`

Effect families are not silently converted into one another. The low-level dependence-aware summary accepts only one effect family at a time. The reference workflow therefore stratifies extracted strict effects by native `effect_family` and never pools or contrasts different families. Cross-family synthesis requires a separately documented and executable conversion rule.

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


## Dependence rule

`dependence_id` is not descriptive metadata only. The executable primary reference analysis clusters uncertainty by `dependence_id`, and leave-one-out sensitivity removes one dependence cluster at a time.

The output must report both effect-row count and dependence-cluster count. Fewer than two dependence clusters in an interaction class is insufficient for an inferential SE/CI under the reference workflow; see `ANALYSIS_DEPENDENCE_CONTRACT.md`.


## Strict-H1 adjudication rule

Screening status and Tier-A provenance do not by themselves authorize a row for the strict synchrony analysis.

Source/component decisions are recorded in `data/registry/strict_h1_adjudications.csv`. Every real extracted study must be represented there, and every `strict_window` effect must match an exact `eligible + strict_extracted` adjudication for its effect ID and timing/effect-family fields.

`scripts/validate_adjudications.py` enforces this gate in CI.


## Summary-statistic reconstruction

A strict effect may be reconstructed from published group means, standard deviations and sample sizes when the exposure groups are defined by the timing contract independently of the fitness result.

For independent-group standardized mean differences, IWE uses the executable `hedges_g_from_summary()` helper. The contrast direction must be declared before calculation. The helper records Hedges' small-sample correction and sampling variance rather than treating the reported group SDs as standard errors.

A pooled within-group SD may also be reconstructed **deterministically** from a reported balanced one-way ANOVA when all of the following are source-backed:

- all group means for the same outcome are reported on one common linear scale;
- every group has the same independent sample size;
- the reported F statistic tests exactly those groups and that outcome; and
- the ANOVA degrees of freedom are consistent with the reported group count and sample sizes.

For this case IWE may use `F = MS_between / MS_within` to recover `MS_within`, then calculate the requested contrast with `hedges_g_from_balanced_anova_means()`. Means may be multiplied by one common positive constant (for example, reported relative to the maximum group mean), because that scale factor cancels from the SMD. This route is an algebraic reconstruction of reported residual variance, **not variance imputation and not cross-family conversion**.

The ANOVA route is prohibited when group sizes are unequal or unknown, the F statistic comes from a transformed/model-adjusted outcome incompatible with the reported means, the reported test includes different groups/covariates, or the degrees of freedom cannot be reconciled with the claimed design.
