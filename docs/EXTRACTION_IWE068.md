# IWE068 extraction receipt — Ipomopsis aggregata × Hylemya sp. (Maxfield 2021)

Source article: Wu C, Powers JM, Hopp DZ, Campbell DR. *Effects of experimental warming on floral scent, display and rewards in two subalpine herbs*. Annals of Botany. DOI `10.1093/aob/mcad195`.

Public source repository: `jmpowers/ipomopsis-temp`, pinned for this reconstruction at commit `9f4ceff87f5eb68c5a09f5e89ea457432e452542`.

Relevant files at the pinned commit:

- `data/traits/2021 Maxfield Phenology - 2021.csv` — repeated plant-level flowers/buds and Hylemya eggs;
- `data/traits/2021 Maxfield Seeds - 2021.csv` — fruit fate and seed counts;
- `data/2021 Maxfield Rosettes - 2021OTCs.csv` — plant treatment metadata;
- `traits.Rmd` — source code defining plant IDs, phenology variables and the final seed-fitness variables.

Status: **unresolved strict-H1 antagonist candidate; reconstruction frozen before the overlap–fitness result is computed**.

## Source data architecture

The source code constructs a stable `plantid` at Maxfield and joins phenology and reproductive data to the same plant metadata.

Phenology variables are defined prospectively by the source as:

- `open = rowSums(open_*)`;
- `buds = rowSums(buds_*)`;
- `eggs = rowSums(eggs_*)`;
- `eggs_per_flower = eggs / (open + buds)`.

The source recodes two late census dates to their intended census rounds:

- `2021-07-02 -> 2021-06-30`;
- `2021-07-26 -> 2021-07-20`.

Missing plant × census combinations are completed with zero `open` and `buds`, following the source workflow.

The reproductive source code aggregates repeated seed/fruit records by plant and defines:

- `seeds_per_fruit = seeds / fruits`;
- `fruits_aborted = aborts + flowers_buds_collected_last`;
- `seeds_est = seeds + seeds_fly + (flowers_buds_collected_early + fruits_early_uncountable) * [seeds/(fruits + fruits_aborted + fruits_fly_with_seeds + fruits_fly_no_seeds + fruits_caterpillar)] + fruits_split * seeds_per_fruit`;
- `fruits_with_seeds = fruits + fruits_split + fruits_fly_with_seeds`;
- `fruits_nonaborted = fruits_with_seeds + fruits_fly_no_seeds + fruits_caterpillar + fruits_split`;
- `flowers_est = fruits_nonaborted + aborts + flowers_buds`;
- `seeds_per_flower = seeds_est / flowers_est`.

`seeds_per_flower` is the source analysis's final plant reproductive-fitness variable and is therefore frozen as the IWE068 primary outcome. IWE will reproduce the source definition rather than selecting a different outcome after seeing the result.

## Frozen primary biological subset

Primary IWE068 reconstruction uses only plants with:

- `temp = control`;
- `snow = normal`.

Rationale: the experiment independently manipulates temperature (`control` versus open-top-chamber warming) and snowmelt (`normal` versus early). IWE's primary aim here is the naturally realized antagonist timing–fitness association. Including warmed or early-snowmelt plants in the primary effect would allow an experimental treatment to induce covariance between flowering phenology, Hylemya activity and reproduction.

The other treatment cells are retained only as labelled sensitivity analyses. They can never replace the primary control-normal result because their effects are larger, smaller, or more significant.

All seasonal census dates for the control-normal plants are retained, including dates before temperature chambers were installed, because these plants did not receive the warming treatment and the full flowering/egg activity window is the exposure of interest.

## Frozen timing metric

For each focal primary plant `p` and census `t`:

1. Define plant floral availability as

   `F[p,t] = open[p,t] + buds[p,t]`.

   This matches the denominator used by the source for `eggs_per_flower` and therefore includes the reproductive structures available to Hylemya oviposition.

2. Estimate the realized Hylemya activity curve using all **other** primary plants:

   `A[-p,t] = sum_{q != p} eggs[q,t] / sum_{q != p} (open[q,t] + buds[q,t])`.

   The focal plant is left out to prevent its own realized egg load from mechanically generating its timing exposure.

3. Keep census dates for which the leave-one-out reference population has a positive floral denominator. No activity rate is imputed where the reference population has zero flowers/buds.

4. On the shared valid census dates, normalize the focal floral curve and reference Hylemya curve to sum to one:

   `Fnorm[p,t] = F[p,t] / sum_t F[p,t]`

   `Anorm[-p,t] = A[-p,t] / sum_t A[-p,t]`.

5. Define overlap by histogram intersection:

   `O[p] = sum_t min(Fnorm[p,t], Anorm[-p,t])`.

`O` lies in `[0,1]`; larger values mean a greater fraction of the plant's reproductive structures occur within the observed Hylemya oviposition window.

This is registered as:

- `timing_metric_type = overlap_index`;
- `phenology_source = direct_interaction`;
- `exposure_direction = synchrony`.

No alternative overlap, peak-lag, first-date or flowering-date metric may replace this primary metric after the plant fitness values are analyzed.

## Frozen quantitative effect

Among complete `temp=control, snow=normal` plants:

- compute Pearson `r = cor(O[p], seeds_per_flower[p])`;
- transform `z = atanh(r)`;
- use sampling variance `1/(n-3)`.

The native direction is retained. Because this is an antagonist overlap exposure, a negative z means greater temporal matching to Hylemya is associated with lower seed production per flower. IWE does not reverse antagonist effects to make them biologically positive.

Register the resulting row only if `n >= 4`, all included plants have finite `O` and `seeds_per_flower`, and both variables have non-zero variance.

## Frozen sensitivity analyses

These are secondary and cannot replace the primary result:

1. `temp=control, snow=early` plants analyzed separately with the identical reconstruction;
2. `temp=warmed, snow=normal` plants analyzed separately;
3. `temp=warmed, snow=early` plants analyzed separately;
4. all treatment cells analyzed in one model only if treatment-cell effects are explicitly retained rather than pooled as if observationally homogeneous.

The primary control-normal row remains the strict-H1 evidence unit regardless of the sensitivity results.

## Reproducibility contract

The reconstruction script must fetch only the three raw files above from the pinned external commit `9f4ceff87f5eb68c5a09f5e89ea457432e452542`, verify the expected columns, reproduce the source variable definitions, and emit:

- plant-level overlap and `seeds_per_flower` for the primary subset;
- n, Pearson r, Fisher z and variance;
- treatment-cell sensitivity summaries;
- the external commit SHA and input paths used.

The result must not depend on the moving `main` branch of the external repository.

## Claim ceiling

Before executing the pinned reconstruction, IWE068 supports only:

> a public, source-coded dataset exists in which repeated plant flowering/bud availability, Hylemya egg activity and final plant seed production can be linked at plant level, allowing a prospectively frozen strict antagonist timing–fitness reconstruction.

No effect sign or magnitude is claimed until the frozen script is run.
