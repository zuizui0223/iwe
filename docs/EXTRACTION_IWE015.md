# IWE015 extraction receipt — Zhou et al. 2020

Source: Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB. 2020. *Variable and sexually conflicting selection on Silene stellata floral traits by a putative moth pollinator selective agent*. Evolution 74:1321–1334. DOI `10.1111/evo.13965`.

Archived data: Dryad DOI `10.5061/dryad.6q573n5w1`.

Status: **strict-H1 admissibility unresolved**. Independent contemporaneous adult activity is source documented, but the final-fruit counts cannot yet be linked unambiguously to the stated one-week tagged flowering cohorts; the published dispersion label is also unverified. Neither 2012 nor 2013 is a quantitative strict-H1 effect.

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

This is an observed post-predation reproductive endpoint in the publication, **but whether every counted fruit derives from the one-week source-defined flowering-exposure cohort is unresolved**. Its biological finality does not by itself establish timing-to-fitness linkage.

## Published summaries

Table 1 labels the group dispersions as standard errors, but that label is internally inconsistent with the same table's bounded proportion outcomes. For example, fruit-initiation proportion is 0.91 ± 0.19 at n=59; an SE of 0.19 would imply an SD greater than 1 for a variable bounded to [0,1], which is impossible. The printed dispersions are consequently **ambiguous and unusable for primary quantitative extraction**. An SD-like interpretation is retained solely as a sensitivity calculation, not as a verified source property. The public Dryad record (`10.5061/dryad.6q573n5w1`) exposes four female CSVs plus the authors' analysis script for a row-level replication audit.

| Year | Window | Adult plants n | Successful fruits mean | Printed dispersion (source labels SE) |
|---|---|---:|---:|---:|
| 2012 | early / Hadena-dominant | 59 | 2.66 | 2.95 |
| 2012 | late / co-pollinator-dominant | 58 | 3.91 | 4.13 |
| 2013 | early / Hadena-dominant | 55 | 9.77 | 6.91 |
| 2013 | late / co-pollinator-dominant | 55 | 8.60 | 7.01 |

The source's `SE` label is not accepted mechanically because it fails a bounded-outcome consistency check elsewhere in the same table. For the diagnostic calculations below **only**, hypothetical SD values are set equal to the printed dispersions; this assumption is not verified, and neither diagnostic SMD is admitted to IWE's primary corpus.

## Hypothetical effect orientation (not yet an admissible contrast)

The native contrast is fixed before using reproductive values:

`high focal-partner overlap (early Hadena-dominant) - low focal-partner overlap (late co-pollinator-dominant)`.

Therefore:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window` **only if** the original flowering-to-final-fruit unit join is verified;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

Positive g means greater synchrony with the mixed pollinating seed predator is associated with greater final female reproductive performance.

## Dual admission hold: flowering-to-fitness unit linkage and source dispersion

The publication explicitly defines the printed dispersion as `SE=standard error`. However, Table 1 also reports bounded fruit-initiation proportions such as `0.91 ± 0.19` for `n=59`. If 0.19 were an SE, the implied SD would be `0.19*sqrt(59) > 1`, which is impossible for a variable bounded to [0,1]. The predation-rate dispersions create the same problem.

This is strong evidence of a source-label or table-assembly error, but it does not by itself prove that every printed dispersion is an SD. Therefore IWE does **not** promote either the literal-SE reconstruction or the SD-like reconstruction into `direct_effects.csv` until the public Dryad female CSVs are recalculated. Candidate diagnostic values may be reported in this receipt as explicitly **conditional arithmetic**, not meta-analytic evidence. Independently of the SE/SD problem, the reported 2013 one-week tagged flowers (294 early and 281 late) are fewer than the successful-fruit totals implied by Table 1 (9.77 × 55 and 8.60 × 55). The original `data_analysis.R` and plant/flower-level female tables must determine whether these quantities have different source-unit universes. Until then the strict timing–outcome join is unresolved; see `IWE015_DRYAD_VARIANCE_AUDIT.md`.

## 2012 conditional, non-promoting diagnostic reconstruction

Using Table 1:

- high-overlap early: mean = 2.66, SD-like printed dispersion = 2.95, n = 59;
- low-overlap late: mean = 3.91, SD-like printed dispersion = 4.13, n = 58.

Applying the registered independent-groups Hedges correction directly to those dispersions:

`g = -0.3465154178`

`var(g) = 0.0342671136`.

Effect ID:

`IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD`.

## 2013 conditional, non-promoting diagnostic reconstruction

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

The source **group means** have opposite early-minus-late successful-fruit directions (−1.25 in 2012 and +1.17 in 2013), with predation contrasts of +18 and +1 percentage points. This describes heterogeneity in Table 1 but **does not establish** a statistically significant timing × year interaction, let alone a pollination-benefit versus larval-cost mechanism. The conditional g values above are illustrative arithmetic under an unverified SD assumption, not effect estimates. These are two years of one shared programme and cannot establish H2 or a general mixed-system average.

The late window also contains other effective moth pollinators, so the contrast represents the realized ecological consequence of changing overlap with *H. ectypa* in the actual pollinator community, not an isolated manipulation of *H. ectypa* presence.

## Reproducibility

The repository retains calculation regression tests for both possible interpretations as diagnostics, but no IWE015 effect is admitted to the strict corpus until **both source-group/final-fruit unit linkage and raw variance** are verified. The Dryad archive identity, version date, female CSV filenames and analysis script are recorded in `IWE015_DRYAD_VARIANCE_AUDIT.md`.
