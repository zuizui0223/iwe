# IWE015 extraction receipt — Zhou et al. 2020

Source: Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB. 2020. *Variable and sexually conflicting selection on Silene stellata floral traits by a putative moth pollinator selective agent*. Evolution 74:1321–1334. DOI `10.1111/evo.13965`.

Archived data: Dryad DOI `10.5061/dryad.6q573n5w1`.

Status: **strict-H1 mixed pollinating-seed-predator evidence extracted for 2012 and 2013**.

## Timing design

At the Mountain Lake Biological Station population, adult *Hadena ectypa* abundance peaks early in the *Silene stellata* flowering season and drops rapidly as generalist co-pollinating moths become dominant.

The authors therefore ran two experiments in each year:

- **early** — *H. ectypa*-dominant period;
- **late** — co-pollinator-dominant period.

Pollinator surveys and flower egg counts were used to confirm the seasonal change in *H. ectypa* activity.

The early/late contrast is therefore not inferred from calendar date alone. It is independently ordered by the measured activity of the focal mixed partner.

## Why this is a mixed interaction

Adult *H. ectypa* pollinate while nectaring, and females may oviposit during the same visits. Larvae subsequently consume flowers and developing fruits/seeds.

Thus greater temporal overlap with *H. ectypa* simultaneously changes:

- a potential pollination benefit;
- an oviposition / seed-predation cost.

Late-season generalist moths are effective pollinators but do not impose the same seed-predation cost.

## Reproductive outcome

The paper defines **successful fruits** as initiated fruits that remained free from *H. ectypa* predation.

Successful fruit number is used as the female reproductive-success measure and is reported to correlate strongly with seed set.

This is therefore a final post-predation reproductive outcome rather than visitation, fruit initiation, egg load, or potential seed set.

## Published summaries

Table 1 reports group means and standard errors.

| Year | Window | Adult plants n | Successful fruits mean | Reported SE |
|---|---|---:|---:|---:|
| 2012 | early / Hadena-dominant | 59 | 2.66 | 2.95 |
| 2012 | late / co-pollinator-dominant | 58 | 3.91 | 4.13 |
| 2013 | early / Hadena-dominant | 55 | 9.77 | 6.91 |
| 2013 | late / co-pollinator-dominant | 55 | 8.60 | 7.01 |

The source explicitly labels these quantities as mean ± SE. IWE therefore reconstructs each group standard deviation as

`SD = SE * sqrt(n)`

before calculating an independent-groups Hedges g.

## Effect orientation

The native contrast is fixed before using reproductive values:

`high focal-partner overlap (early Hadena-dominant) - low focal-partner overlap (late co-pollinator-dominant)`.

Therefore:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

Positive g means greater synchrony with the mixed pollinating seed predator is associated with greater final female reproductive performance.

## 2012 effect

Using Table 1:

- high-overlap early: mean = 2.66, SE = 2.95, n = 59;
- low-overlap late: mean = 3.91, SE = 4.13, n = 58.

After converting SE to SD and applying the registered small-sample correction:

`g = -0.0453662495`

`var(g) = 0.0337540056`.

Effect ID:

`IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## 2013 effect

Using Table 1:

- high-overlap early: mean = 9.77, SE = 6.91, n = 55;
- low-overlap late: mean = 8.60, SE = 7.01, n = 55.

The reconstructed effect is:

`g = +0.0225087081`

`var(g) = 0.0358615214`.

Effect ID:

`IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## Dependence

Both year-specific effects come from the same population, experimental programme, focal interaction and paper.

They therefore share:

`DEP_SILENE_STELLATA_HADENA_MLBS`.

The two rows preserve year-specific effect heterogeneity without increasing the number of independent dependence clusters.

## Interpretation boundary

The two year effects are close to zero and have opposite signs.

That pattern is compatible with the biological expectation that greater synchrony with a pollinating seed predator can have offsetting pollination benefits and seed-predation costs, but two dependent year effects do not establish H2 or a general mixed-system average.

The late window also contains other effective moth pollinators, so the contrast represents the realized ecological consequence of changing overlap with *H. ectypa* in the actual pollinator community, not an isolated manipulation of *H. ectypa* presence.

## Reproducibility

The repository implements `hedges_g_from_mean_se()`, which converts the source-labeled SEs to SDs and calls the registered Hedges-g calculation. Regression tests reproduce both year-specific effects and variances.
