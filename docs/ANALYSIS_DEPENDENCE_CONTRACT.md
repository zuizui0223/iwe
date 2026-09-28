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

1. a REML working model estimates between-effect heterogeneity `tau2`;
2. the point estimate uses inverse `variance_native + tau2` weights;
3. uncertainty uses a CR2 bias-reduced cluster-robust sandwich variance with `dependence_id` as the cluster;
4. confidence intervals use a conservative Student-t reference with `m_dependence - 1` degrees of freedom;
5. inferential SEs/CIs are withheld whenever that conservative df is <4.

The output reports both:

- `k_effects` — number of extracted effect rows;
- `m_dependence` — number of dependence clusters.

These quantities must never be described as interchangeable sample sizes.

## Low-information fail-closed rule

A descriptive random-effects point estimate may be retained with very few clusters, but robust inference is not reported merely because a sandwich variance can be computed.

Under the current conservative reference rule:

- `df = m_dependence - 1`;
- if `df < 4`, `se`, `ci_low`, and `ci_high` are written as missing;
- `inferential_status = insufficient_cluster_information`.

Therefore two independent clusters give `df=1`: they are a meaningful replication milestone but do not contain enough information for a trustworthy CRVE confidence interval. This explicitly separates **replication discovery** from **inferential evaluability**.

## Cross-class rule

A single `dependence_id` may not span multiple `interaction_type` values in the same primary table. The cluster-robust summary fails closed if that occurs.

If a biological source genuinely contributes to more than one interaction class, the dependence representation must be redesigned before class contrasts are used.

## Class contrasts

Pairwise H1 class contrasts use class-level cluster-robust standard errors and an independent-class approximation. The smaller of the two class degrees of freedom is used for the t critical value.

If either class has insufficient dependence clusters, the contrast point estimate may be retained descriptively but no inferential CI is produced.

This is a first-release reference analysis. A later implementation should replace the conservative `m-1` df with the coefficient-specific Satterthwaite df used by mature CR2 implementations, but it must preserve the same dependence identifiers, retain the df<4 fail-closed rule, and never revert to effect-row independence.

## Sensitivity analysis

`scripts/run_sensitivity.py` performs leave-one-`dependence_id`-out analysis.

It does not use publication (`study_id`) as the omission unit because one dependence cluster may contain multiple publications and one publication may contain multiple dependent effects.

## H1 evaluability

The machine-readable claim gate requires at least one **common native effect family** (or a future registered conversion scale) that has:

- real strict Tier-A evidence in all three interaction classes; and
- enough independent `dependence_id` clusters in every class to reach the reference df floor.

With the current conservative `df=m-1` rule, this means at least **five clusters per class**. The separate two-cluster target is retained only as a search/replication milestone. The reference workflow stratifies by `effect_family`; effects on different native scales are retained but are not numerically pooled or used for class contrasts.


## Cross-publication assignment registry

Known study-level overlap is registered in `data/registry/study_dependencies.csv`.

For rows with `dependency_status = confirmed`, every extracted effect from that study must use the registered `required_dependence_id`. `scripts/validate_dependencies.py` enforces this in CI.

Rows marked `unresolved` cannot be assigned a required cluster prospectively; their source overlap must be adjudicated first. This prevents a later publication from being counted as an independent cluster merely because it has a new DOI.


## Replication-first target

For the current empirical build, the discovery target remains the native `standardized_mean_difference` family with a minimum of **two independent dependence clusters per interaction class**. This is a search milestone, not an inferential threshold.

This is stricter than merely having rows in all three classes. A new effect advances the replication target only when it introduces a previously unrepresented `dependence_id` in the target effect family.

Consequences:

- another year, site, outcome or model from an existing dependence cluster does not reduce the replication gap;
- converting an existing programme to another effect scale does not reduce the SMD replication gap;
- mixed-system recovery remains a priority while IWE015 is on quantitative hold; the antagonist class currently has zero strict SMD clusters after the IWE011 re-audit, so it must recover a first valid antagonist cluster and then a second; mutualist already satisfies the two-cluster discovery milestone;
- `src/iwe/replication.py` and the machine-readable claim status report the current and missing cluster counts.

The two-cluster threshold is only a replication milestone. H1 is not inferentially evaluable under the reference workflow until the cluster-information rule is satisfied.
