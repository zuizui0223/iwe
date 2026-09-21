# Analysis dependence contract

Date: 2026-09-21
Status: executable

## Inferential unit

IWE effect rows are not assumed independent merely because they occupy separate CSV rows.

The primary dependence identifier is `dependence_id`. Rows may share a `dependence_id` across sites, outcomes, experiments, or publications when the source evidence does not justify treating them as independent inferential replicates.

The empirical primary workflow must therefore use `dependence_id`, not row count and not publication count, as the replication unit for uncertainty.

## Reference primary summary

`scripts/run_primary_meta.py` uses `cluster_robust_summary()`.

For each interaction class:

1. the point estimate is the inverse-variance weighted mean of the admitted strict Tier-A effects;
2. residual score contributions are summed within `dependence_id`;
3. uncertainty uses a CR1 cluster-robust sandwich variance;
4. confidence intervals use a Student-t critical value with `m_dependence - 1` degrees of freedom.

The output reports both:

- `k_effects` — number of extracted effect rows;
- `m_dependence` — number of dependence clusters.

These quantities must never be described as interchangeable sample sizes.

## One-cluster fail-closed rule

If an interaction class has fewer than two distinct `dependence_id` values:

- a descriptive point estimate may be retained;
- `se`, `ci_low`, and `ci_high` are written as missing;
- `inferential_status = insufficient_dependence_clusters`.

Thus multiple rows from one dependence cluster cannot create a pseudo-precise confidence interval.

## Cross-class rule

A single `dependence_id` may not span multiple `interaction_type` values in the same primary table. The cluster-robust summary fails closed if that occurs.

If a biological source genuinely contributes to more than one interaction class, the dependence representation must be redesigned before class contrasts are used.

## Class contrasts

Pairwise H1 class contrasts use class-level cluster-robust standard errors and an independent-class approximation. The smaller of the two class degrees of freedom is used for the t critical value.

If either class has insufficient dependence clusters, the contrast point estimate may be retained descriptively but no inferential CI is produced.

This is a first-release reference analysis, not the final publication model. A later multilevel/RVE implementation may replace it, but it must preserve the same dependence identifiers and must not revert to effect-row independence.

## Sensitivity analysis

`scripts/run_sensitivity.py` performs leave-one-`dependence_id`-out analysis.

It does not use publication (`study_id`) as the omission unit because one dependence cluster may contain multiple publications and one publication may contain multiple dependent effects.

## H1 evaluability

The machine-readable claim gate requires at least one **common native effect family** (or a future registered conversion scale) that has:

- real strict Tier-A evidence in all three interaction classes; and
- at least two `dependence_id` clusters in every interaction class.

The reference workflow stratifies by `effect_family`; effects on different native scales are retained but are not numerically pooled or used for class contrasts. This minimum permits the reference cluster-robust variance to exist. It is not a claim that two clusters provide strong or publication-ready evidence.


## Cross-publication assignment registry

Known study-level overlap is registered in `data/registry/study_dependencies.csv`.

For rows with `dependency_status = confirmed`, every extracted effect from that study must use the registered `required_dependence_id`. `scripts/validate_dependencies.py` enforces this in CI.

Rows marked `unresolved` cannot be assigned a required cluster prospectively; their source overlap must be adjudicated first. This prevents a later publication from being counted as an independent cluster merely because it has a new DOI.
