# IWE067 extraction receipt — Ipomopsis aggregata × Hylemya sp.

Source: Price MV, Waser NM, Lopez DA, Ramírez VD, Rosas CE. 2021. *Predispersal Seed Predation Obscures the Detrimental Effect of Dust on Wildflower Reproduction*. International Journal of Plant Sciences 182:277–285. DOI `10.1086/713440`.

Public data:

- flowering + Hylemya egg census: Dryad `10.6086/D18D7B`;
- mature fruit/fate/seed data: Dryad `10.6086/D10X1R`.

Status: **unresolved strict-H1 antagonist candidate; reconstruction rule is frozen and implemented, but raw Dryad files are not yet materialized**.

## Why this can identify a strict timing effect

For three summers the study censused plants every four days, recording open flowers and Hylemya eggs. Hylemya oviposition was concentrated early in the flowering season and, pooled across years, declined by approximately `0.03 eggs per flower` per successive four-day census. The year × census term was also significant, so year-specific activity curves are required.

Flowers/fruits were followed to reproductive outcome. In 2017 and 2018 all flowers were marked with census-specific calyx colors and mature fruits were scored as aborted, expanded/unparasitized, or parasitized; full-sized seeds were counted for intact fruits. These years therefore contain both a realized antagonist activity window and final reproductive fate at plant level.

The article reports that only about 42% of eggs were detected, but the probability of missing an egg did not differ detectably among census dates or dust treatments. Egg counts can therefore be used as a relative temporal activity index, while not being interpreted as absolute Hylemya abundance.

## Why 2016 is excluded from the strict reconstruction

In 2016 the complete fruit dataset is available only for the subset of fruits on which an egg had been detected; all flowers were not cohort-marked in the same way as in 2017–2018. Using 2016 would therefore condition the final-fitness sample on antagonist detection.

The strict reconstruction is frozen to **2017 and 2018 only**.

## Primary population and treatment

Primary strict effects use **clean control plants only**.

Dust is an experimental treatment that changes stigma pollen loads and Hylemya attack. Pooling dusty and control plants would create treatment-induced covariance between the timing/exposure process and reproduction. Dusted plants are reserved for a sensitivity analysis and never substituted into the primary effect because they increase sample size.

## Frozen timing metric

For each year separately:

1. For each focal control plant `p` and census `t`, let `F[p,t]` be its observed number of open flowers.
2. Estimate the population Hylemya interaction-activity curve for the focal plant using **all other control plants in that year**:

   `A[-p,t] = total detected Hylemya eggs / total open flowers`

   at census `t`, excluding plant `p` from numerator and denominator.
3. Set negative or impossible rates to missing/error; do not impute censuses with zero flowers in the reference population.
4. Normalize the focal plant flowering curve and the leave-one-plant-out Hylemya activity curve across the shared valid censuses so each sums to one.
5. Define temporal overlap by histogram intersection:

   `O[p] = sum_t min(Fnorm[p,t], Anorm[-p,t])`.

`O` ranges from 0 to 1, with larger values meaning that the plant places a larger share of its flowers within the realized Hylemya oviposition window.

This is registered as `timing_metric_type = overlap_index` and `phenology_source = direct_interaction`.

No alternative overlap metric will replace it after seed/fruit outcomes are viewed. Other metrics may be reported only as labelled sensitivity analyses.

## Frozen final-fitness outcome

Primary outcome per plant:

`W[p] = expanded_unparasitized_fruits / all_scored_marked_flowers`.

This is a final successful-fruit outcome that requires no imputation of seed numbers into Hylemya-destroyed fruits.

Aborted and parasitized fruits are failures for this endpoint. Missing/incomplete fruit records are excluded from numerator and denominator rather than guessed.

A secondary seed-output endpoint may be constructed only if the raw fruit file permits a source-faithful count of intact full-sized seeds for every fate category without assigning unobserved seed values. The paper's simulated no-Hylemya seed values are **never** used as observed fitness.

## Frozen quantitative effect

For each of 2017 and 2018 separately, among complete control plants:

- compute Pearson `r = cor(O[p], W[p])`;
- transform to `z = atanh(r)`;
- sampling variance `1/(n-3)`.

The two year effects share `dependence_id = DEP_IWE067_IPOMOPSIS_HYLEMYA` and are not independent programmes.

Because `O` is antagonist overlap, the native exposure direction is `synchrony`: a negative native effect means greater plant–Hylemya temporal matching is associated with poorer plant reproductive success. IWE does **not** flip antagonist signs to fit a preferred biological direction; the general orientation rule remains `greater synchrony -> higher plant reproduction`.

## Completeness rules

A plant is included only if it has:

- a control-treatment identifier;
- at least one valid open-flower census and enough shared censuses to calculate normalized overlap;
- a unique plant identifier that joins the phenology and fruit datasets;
- a nonzero number of scored marked flowers in the final fruit dataset.

No minimum flower-count threshold is introduced after viewing outcomes.

## Sensitivity analyses (not primary replacements)

1. Repeat the same reconstruction among dusty plants, keeping effects separate from controls.
2. Recompute the activity curve using all plants but still leave the focal plant out; label this as treatment-mixed activity sensitivity.
3. If source-faithful intact-seed output is available for all fruit fates, repeat with seeds per scored flower.

None can replace the frozen control-plant successful-fruit effect because it is weaker or less significant.

## Current implementation and data-access status

The frozen reconstruction is now implemented in `src/iwe/iwe067.py` and regression-tested in `tests/test_iwe067_reconstruction.py`. The executable entry point is `scripts/reconstruct_iwe067.py`. The code fixes the leave-one-plant-out overlap calculation, the successful-fruit endpoint, the 2017/2018 year restriction, the control-only primary subset, missing-value behavior, and Fisher-z variance before the raw outcomes are available.

The Dryad landing pages expose the exact required files:

- `Flower_and_Hylemya_Egg_Census_DATA.txt` — Dryad file stream `546028`;
- `2016-2018DustStudyFruitDataForDeposit.txt` — Dryad file stream `1064066`.

The linked file-stream endpoints currently return HTTP 403 in the execution environment, and a second direct-download route also fails. The landing-page metadata and the published article independently confirm that the first file contains plant-by-census flowering/egg data and that the second contains final flower/fruit fates for 2017–2018.

The remaining implementation step is therefore narrow: materialize the two raw text files, map their source column names/fate codes into the canonical columns required by `iwe.iwe067`, and execute the already-frozen reconstruction. No choice of timing metric, treatment subset, outcome, year set, or effect-size formula remains open.

This is an access limitation, not a negative adjudication. IWE067 remains `unresolved_strict` until the raw files can be materialized or an equivalent source-level coefficient is recovered.

## Claim ceiling

Before numerical reconstruction, IWE067 supports only:

> a published dataset exists in which flowering phenology, realized Hylemya oviposition timing, and final reproductive fate were measured on the same experimental plant population with sufficient identifiers to prospectively reconstruct a strict antagonist overlap–fitness effect.

No effect sign or magnitude is claimed until the frozen reconstruction is executed.
