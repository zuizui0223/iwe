# IWE068 extraction receipt — Ipomopsis aggregata × Hylemya sp. (Maxfield 2021)

Source article: Wu C, Powers JM, Hopp DZ, Campbell DR. *Effects of experimental warming on floral scent, display and rewards in two subalpine herbs*. Annals of Botany. DOI `10.1093/aob/mcad195`.

Public source repository: `jmpowers/ipomopsis-temp`, pinned at commit `9f4ceff87f5eb68c5a09f5e89ea457432e452542`.

Relevant pinned raw files:

- `data/traits/2021 Maxfield Phenology - 2021.csv` — repeated plant-level flowers/buds and Hylemya eggs;
- `data/traits/2021 Maxfield Seeds - 2021.csv` — fruit fate and seed counts;
- `data/2021 Maxfield Rosettes - 2021OTCs.csv` — plant treatment metadata.

Source transformation reference: `traits.Rmd` at the same pinned commit.

Status: **strict-H1 antagonist effect quantitatively closed**.

## Frozen design

The reconstruction contract below was frozen before the overlap–fitness result was computed.

### Primary biological subset

Use only plants with:

- `temp = control`;
- `snow = normal`.

The warming and early-snowmelt cells remain sensitivity lanes and cannot replace the primary result based on effect size or significance.

### Source phenology variables

The source workflow defines:

- `open = rowSums(open_*)`;
- `buds = rowSums(buds_*)`;
- `eggs = rowSums(eggs_*)`;
- `eggs_per_flower = eggs / (open + buds)`.

IWE reconstructs `plantid` from plot, subplot and plant, and preserves the source census recodes:

- `2021-07-02 -> 2021-06-30`;
- `2021-07-26 -> 2021-07-20`.

Plant × census combinations absent from the repeated phenology file are completed with zero floral availability and zero eggs for the IWE overlap reconstruction.

### Source reproductive outcome

The source code aggregates repeated reproductive records and defines:

- `seeds_per_fruit = seeds / fruits`;
- `fruits_aborted = aborts + flowers_buds_collected_last`;
- `seeds_est = seeds + seeds_fly + (flowers_buds_collected_early + fruits_early_uncountable) * [seeds/(fruits + fruits_aborted + fruits_fly_with_seeds + fruits_fly_no_seeds + fruits_caterpillar)] + fruits_split * seeds_per_fruit`;
- `fruits_with_seeds = fruits + fruits_split + fruits_fly_with_seeds`;
- `fruits_nonaborted = fruits_with_seeds + fruits_fly_no_seeds + fruits_caterpillar + fruits_split`;
- `flowers_est = fruits_nonaborted + aborts + flowers_buds`;
- `seeds_per_flower = seeds_est / flowers_est`.

`seeds_per_flower` was frozen as the primary plant reproductive outcome.

The Python reconstruction preserves R's NA propagation. In particular, fruitless plants with undefined `seeds_per_fruit` remain NA; they are not converted into artificial zero-fitness observations through `0 * NA -> 0` logic.

## Frozen timing metric

For focal primary plant `p` and census `t`:

`F[p,t] = open[p,t] + buds[p,t]`.

Estimate the Hylemya activity curve using all **other** primary plants:

`A[-p,t] = sum_{q != p} eggs[q,t] / sum_{q != p} (open[q,t] + buds[q,t])`.

The focal plant is left out to prevent its own egg load from mechanically generating its timing exposure.

Census dates for which the leave-one-out reference population has zero floral denominator are omitted. On valid dates, normalize both curves to sum to one and calculate histogram intersection:

`O[p] = sum_t min(Fnorm[p,t], Anorm[-p,t])`.

Properties:

- `O in [0,1]`;
- larger `O` means greater temporal overlap between focal reproductive structures and observed Hylemya oviposition activity;
- `timing_metric_type = overlap_index`;
- `phenology_source = direct_interaction`;
- `exposure_direction = synchrony`.

## Frozen quantitative effect

Among complete primary plants:

1. Pearson `r = cor(O[p], seeds_per_flower[p])`;
2. Fisher `z = atanh(r)`;
3. sampling variance `1/(n-3)`.

The native synchrony direction is retained. For this antagonist interaction, a negative effect means greater temporal matching to Hylemya is associated with lower plant reproductive performance.

## Executed result

The pinned reconstruction was executed in GitHub Actions from the three raw files above using `scripts/reconstruct_iwe068.py`.

Recovered primary effect:

| quantity | value |
|---|---:|
| complete plants `n` | 11 |
| Pearson `r` | -0.05224909311004083 |
| Fisher `z` | -0.05229671725455789 |
| variance | 0.125 |

The result is therefore **essentially null on the registered linear synchrony scale**. The point estimate is slightly negative, but it is small relative to its sampling uncertainty.

This row is registered in `data/extraction/direct_effects.csv` as `IWE068_MAXFIELD_FZ` with dependence ID `DEP_IWE068_IPOMOPSIS_HYLEMYA`.

## Reproducibility implementation

The repository now contains:

- `src/iwe/reconstruction.py` — deterministic source-variable reconstruction and leave-one-out overlap helpers;
- `tests/test_iwe068_reconstruction.py` — tests for overlap, source seed arithmetic, R-style NA propagation, date recoding/phenology preparation and seed aggregation;
- `scripts/reconstruct_iwe068.py` — fetches only the three pinned raw inputs and emits plant-level data plus the strict effect;
- CI execution of the reconstruction on every relevant branch update.

The analysis does not depend on the moving external `main` branch.

## Interpretation ceiling

IWE068 supports:

> In the Maxfield 2021 untreated/normal-snow subset, the prospectively frozen leave-one-out temporal overlap between `Ipomopsis aggregata` reproductive structures and Hylemya oviposition activity showed little linear association with source-defined seeds per flower (`r=-0.052`, `n=11`).

It does **not** establish:

- no antagonist timing effect in general;
- absence of nonlinear timing effects;
- absence of treatment-dependent effects;
- equivalence between Hylemya oviposition overlap and all forms of antagonist exposure;
- a class-level antagonist estimate from one programme.

## Consequence for IWE

IWE068 is the first quantitatively closed strict-H1 antagonist programme. Together with IWE001 (mutualist) and IWE064 (mixed pollinating seed predator), IWE now has at least one strict quantitative programme represented in each preregistered interaction class. This is a milestone for estimand coverage, **not** sufficient replication for a cross-class biological conclusion.
