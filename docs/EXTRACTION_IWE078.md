# IWE078 extraction receipt — Oenothera biennis × Mompha stellella

Source data: Slimon K, Agrawal AA. 2026. *Data and scripts from Slimon & Agrawal (2026): "Phenological plasticity mediates sequential herbivory and fitness"*. Zenodo. DOI `10.5281/zenodo.19488509`.

Source status: public empirical dataset + analysis scripts associated with a 2026 manuscript title. A journal publication under this exact title has not yet been verified. This record therefore remains **unresolved strict-H1 pending source-status and quantitative reconstruction**, even if the raw reconstruction is technically successful.

Interaction class: `antagonist`.

Primary focal partner for strict reconstruction: `Mompha stellella`.

Plant: `Oenothera biennis`.

Dependence ID: `DEP_IWE078_OENOTHERA_MOMPHA`.

## Why this is a high-value strict candidate

The public Zenodo package contains, for two field experiments/cohorts:

- repeated plant-level flowering counts through the season;
- repeated `Mompha stellella` gall counts with a source-defined correction for gall persistence;
- final plant fruit/fitness measurements;
- experimental-treatment and genotype identifiers;
- complete R scripts documenting the original data processing.

The source abstract reports that phenological changes altered overlap with seed predators and that earlier versus later flowering had opposing effects on seed-predator damage and fitness pathways.

This is unusually close to the IWE strict chain:

```text
plant flowering distribution × observed seed-predator activity
-> temporal overlap
-> final realized reproduction
```

## Why the source `overlap` column is NOT the IWE primary metric

The supplied time-series scripts calculate an exploratory overlap value as:

```text
sum_week(plant potential flowers × pooled Mompha+Schinia count)
```

where pooled herbivore abundance is summed over all plants in the week.

This quantity is not normalized to either the plant's total flowering or the predator activity distribution. It therefore increases mechanically with flower production as well as temporal matching. The source scripts also state that this overlap index was exploratory/not explicitly used as a final-paper model variable.

IWE will retain the source `overlap` column for audit only. It will **not** enter strict H1 and will not be substituted for a normalized temporal-matching estimand.

This exclusion is frozen before calculating any IWE078 timing–fitness effect.

## Source-faithful flowering availability

The supplied source scripts define `potential` flowering as:

```text
potential flowers = observed open flowers + fresh Mompha galls / 9
```

because a `Mompha stellella` gall persists for approximately nine days whereas an open flower is treated as a one-day observation. The correction restores a galled bud to the flowering availability it would have represented.

IWE uses this source-defined `potential` variable as the plant flowering curve rather than inventing a new flowering reconstruction.

For focal plant `p` in week `t`:

```text
F[p,t] = source-defined potential flowers
```

## Primary partner-activity curve

The primary strict partner is `Mompha stellella`, not a post-hoc pooled seed-predator guild.

Reason:

1. `Mompha` has repeated plant-level time-series data across the flowering season;
2. the source explicitly implements a persistence-correction algorithm for new gall acquisition;
3. `Schinia florida` is sampled on fewer dates and on a different observation scale;
4. summing raw Mompha and Schinia counts would require an arbitrary cross-species weighting.

The source `momphaCALC` tables contain a week-over-week correction that distinguishes newly acquired galls from persisting/aging galls. IWE therefore defines the time-specific interaction event as the source-corrected **new Mompha acquisition**:

Experiment 1:

```text
M[p,t] = mompha gained + Pos GainedOLD+lostNEW
```

Experiment 2:

```text
M[p,t] = mompha gained + pos gin lost
```

Negative/impossible values are invalid. Missing values are not converted to zero unless the source algorithm itself defines the relevant correction term as zero.

This choice is frozen before the timing–fitness effect is calculated.

## Primary subset

Primary effects use source-defined **untreated control plants only**.

For Experiment 1 the source scripts map raw `TRT == "C"` to `Treatment == "Control"`.

For Experiment 2 the exact untreated control code will be mapped from the source treatment field before execution and must correspond to the source's unmanipulated control state; no treatment category may be selected based on its effect sign or precision.

Plants are additionally subject to the source's prospective cleaning rules:

- recognized experimental genotype;
- flowered during the experiment;
- not excluded by the source for severe groundhog/chop damage that invalidates reproductive measurement;
- valid final reproductive outcome;
- enough nonmissing time-series observations to normalize both curves.

No new minimum flower, predator, or fitness threshold will be introduced after inspecting the reconstructed effect.

## Frozen leave-one-plant-out timing metric

For each experiment separately, among primary control plants:

1. Bin observations on the source weekly survey grid.
2. For focal plant `p`, construct its source-defined potential-flowering curve `F[p,t]`.
3. Estimate the realized Mompha activity curve from **all other eligible control plants in the same experiment**:

   ```text
   A[-p,t] = sum_{q != p} M[q,t]
   ```

4. Restrict to weeks in which both the focal flowering curve and the leave-one-out activity curve are valid.
5. Require positive total focal flowering and positive total reference Mompha activity.
6. Normalize each curve:

   ```text
   Fnorm[p,t] = F[p,t] / sum_t F[p,t]
   Anorm[-p,t] = A[-p,t] / sum_t A[-p,t]
   ```

7. Define temporal overlap by histogram intersection:

   ```text
   O[p] = sum_t min(Fnorm[p,t], Anorm[-p,t])
   ```

`O[p]` ranges from 0 to 1. Larger values mean a greater fraction of the focal plant's reproductive window coincides with the observed Mompha interaction window.

This is registered as:

- `timing_metric_type = overlap_index`;
- `phenology_source = direct_interaction`;
- `exposure_direction = synchrony`.

The focal plant is excluded from the activity curve to prevent its own attack count from mechanically creating its synchrony score.

## Frozen final reproductive outcome

Primary plant performance uses the source's **realized final reproduction after seed-predator loss**, i.e. the same `fitness_frt` quantity from which the source constructs:

```text
log_total_fitness = log(fitness_frt + 1)
```

IWE uses `log_total_fitness` for the primary correlation because it follows the source's final SEM transformation and avoids introducing a new outcome transformation after inspection.

The outcome is not the source's potential flower count, seed-predator damage fraction, or simulated no-predator fitness.

## Frozen quantitative effect

For each experiment separately:

```text
r = cor(O[p], log_total_fitness[p])
z = atanh(r)
variance(z) = 1 / (n - 3)
```

The two experiment effects share:

```text
dependence_id = DEP_IWE078_OENOTHERA_MOMPHA
```

and count as **one independent biological programme**, not two independent studies.

A finite Fisher-z effect requires `n >= 4` complete primary plants and `|r| < 1`.

Because the partner is antagonistic, the sign is not flipped to match an expectation. A negative native effect means greater Mompha synchrony is associated with lower realized plant reproduction; a positive native effect means the opposite.

## Sensitivity analyses that cannot replace the primary result

The following may be computed only as labelled sensitivities:

1. use observed open flowers rather than source `potential` flowers;
2. use fresh Mompha prevalence rather than source-corrected new gall acquisition;
3. add `Schinia florida` to form a tracked seed-predator-guild activity curve;
4. include manipulated plants while adjusting for source treatment;
5. correlate overlap with untransformed `fitness_frt`.

None may replace the frozen control/Mompha/potential-flower/log-fitness effect because it is larger, smaller, more precise, or more favorable to H1.

## Source-status gate

The Zenodo record is an open empirical dataset with authors, a manuscript title, raw data and executable analysis scripts. Current public search has not verified a peer-reviewed publication under the exact manuscript title.

Therefore:

- the reconstruction may be implemented and audited now;
- its numerical result must remain provisional until IWE's source-eligibility rule explicitly admits this source form or a corresponding citable publication is verified;
- it cannot silently be promoted into the confirmatory H1 corpus merely because it supplies a needed antagonist replication.

## Claim ceiling before reconstruction

At this stage IWE078 supports only:

> a public two-cohort Oenothera dataset contains source-documented flowering time series, directly observed Mompha seed-predator timing, and final realized reproduction sufficient for a prospectively frozen strict timing–fitness reconstruction.

No IWE078 effect sign, magnitude, class mean, or H1 support state is claimed before the frozen reconstruction is executed and the source-status gate is resolved.
