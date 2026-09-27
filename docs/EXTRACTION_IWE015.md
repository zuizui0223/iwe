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

Table 1 labels the group dispersions as standard errors, but that label is internally inconsistent with the same table's bounded proportion outcomes. For example, fruit-initiation proportion is 0.91 ± 0.19 at n=59; an SE of 0.19 would imply an SD greater than 1 for a variable bounded to [0,1], which is impossible. The printed dispersions are therefore treated as SD-like values rather than multiplied by sqrt(n). The public Dryad record (`10.5061/dryad.6q573n5w1`) exposes four female CSVs plus the authors' analysis script for a row-level replication audit.

| Year | Window | Adult plants n | Successful fruits mean | Printed dispersion (source labels SE) |
|---|---|---:|---:|---:|
| 2012 | early / Hadena-dominant | 59 | 2.66 | 2.95 |
| 2012 | late / co-pollinator-dominant | 58 | 3.91 | 4.13 |
| 2013 | early / Hadena-dominant | 55 | 9.77 | 6.91 |
| 2013 | late / co-pollinator-dominant | 55 | 8.60 | 7.01 |

The source's `SE` label is not accepted mechanically because it fails a bounded-outcome consistency check elsewhere in the same table. IWE uses the printed dispersion directly as the group SD for the successful-fruit SMD and preserves the label discrepancy in the extraction receipt.

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

- high-overlap early: mean = 2.66, SD-like printed dispersion = 2.95, n = 59;
- low-overlap late: mean = 3.91, SD-like printed dispersion = 4.13, n = 58.

Applying the registered independent-groups Hedges correction directly to those dispersions:

`g = -0.3465154178`

`var(g) = 0.0342671136`.

Effect ID:

`IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## 2013 effect

Using Table 1:

- high-overlap early: mean = 9.77, SD-like printed dispersion = 6.91, n = 55;
- low-overlap late: mean = 8.60, SD-like printed dispersion = 7.01, n = 55.

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

The two year effects have opposite signs: a moderate negative 2012 association and a smaller positive 2013 association. This is more heterogeneous than the previous near-zero reconstruction and is compatible with year-to-year shifts in the balance between pollination benefit and seed-predation cost. Because both years belong to one dependence cluster, they still do not establish H2 or a general mixed-system average.

The late window also contains other effective moth pollinators, so the contrast represents the realized ecological consequence of changing overlap with *H. ectypa* in the actual pollinator community, not an isolated manipulation of *H. ectypa* presence.

## Reproducibility

The repository now uses `hedges_g_from_summary()` for IWE015, treating the printed Table 1 dispersions as SD-like values after the bounded-outcome consistency failure of the `SE` label. Regression tests reproduce both corrected year-specific effects and variances. The Dryad archive identity, version date, female CSV filenames and analysis script are recorded separately in the source audit.
