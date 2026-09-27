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

## Published summaries and dispersion audit

Table 1 labels its dispersion columns as mean ± SE.

| Year | Window | Adult plants n | Successful fruits mean | Reported ± value |
|---|---|---:|---:|---:|
| 2012 | early / Hadena-dominant | 59 | 2.66 | 2.95 |
| 2012 | late / co-pollinator-dominant | 58 | 3.91 | 4.13 |
| 2013 | early / Hadena-dominant | 55 | 9.77 | 6.91 |
| 2013 | late / co-pollinator-dominant | 55 | 8.60 | 7.01 |

The printed SE label is internally inconsistent with the same table. For example, fruit-initiation proportion is bounded on [0,1], yet the 2012-early row reports 0.91 ± 0.19 with n=59. If 0.19 were an SE, the implied SD would be 1.46. For a [0,1] variable with mean 0.91, the maximum possible SD is sqrt(0.91 × 0.09) = 0.286, so the SE interpretation is impossible.

The table also provides an internal positive check. Treating the four fruit-initiation dispersions (0.19, 0.19, 0.10, 0.10) as SDs and combining them with the reported group means and sample sizes yields an overall SD of about 0.152, reproducing the reported Overall value 0.92 ± 0.15. The successful-fruit and predation columns show the same SD-like scale.

IWE therefore adjudicates the Table 1 ± values as **standard deviations mislabeled as SE**, and uses them directly as SDs. The Dryad DOI remains recorded as the preferred raw-data cross-check, but the previous SE×sqrt(n) reconstruction is rejected by the source table's own bounded-variable constraints.

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

- high-overlap early: mean = 2.66, SD = 2.95, n = 59;
- low-overlap late: mean = 3.91, SD = 4.13, n = 58.

Applying the registered small-sample correction:

`g = -0.3465154178`

`var(g) = 0.0342671136`.

Effect ID:

`IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## 2013 effect

Using Table 1:

- high-overlap early: mean = 9.77, SD = 6.91, n = 55;
- low-overlap late: mean = 8.60, SD = 7.01, n = 55.

The reconstructed effect is:

`g = +0.1669290472`

`var(g) = 0.0359881819`.

Effect ID:

`IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## Dependence

Both year-specific effects come from the same population, experimental programme, focal interaction and paper.

They therefore share:

`DEP_SILENE_STELLATA_HADENA_MLBS`.

The two rows preserve year-specific effect heterogeneity without increasing the number of independent dependence clusters.

## Interpretation boundary

The two year effects have opposite signs: moderately negative in 2012 and small positive in 2013.

That sign reversal is compatible with the biological expectation that greater synchrony with a pollinating seed predator can shift the balance between pollination benefit and seed-predation cost across years, but two dependent year effects do not establish H2 or a general mixed-system average.

The late window also contains other effective moth pollinators, so the contrast represents the realized ecological consequence of changing overlap with *H. ectypa* in the actual pollinator community, not an isolated manipulation of *H. ectypa* presence.

## Reproducibility

The repository uses `hedges_g_from_summary()` for IWE015 because the source-table dispersion audit identifies the reported ± values as SDs despite the printed SE label. Regression tests reproduce both corrected year-specific effects and variances.
