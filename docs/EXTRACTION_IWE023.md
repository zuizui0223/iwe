# IWE023 extraction receipt — independent mutualist SMD replication

Date: 2026-09-24  
Study: Gallagher & Campbell, *Pollinator visitation rate and effectiveness vary with flowering phenology*  
DOI: `10.1002/ajb2.1439`  
System: *Mertensia ciliata* × seasonal pollinator assemblage  
Decision: **strict H1 eligible; second independent mutualist SMD cluster**

## Biological contrast

In 2015, flowering onset was experimentally shifted into four weekly cohorts spanning June 23 to July 20. Each cohort contained **10 plants** and plants were exposed to natural pollination for one week.

Pollinator visitation was measured directly during each flowering cohort in the same experiment. Visitation differed among weeks and was **more than fivefold higher in week 1 than in week 4**. The exposure contrast is therefore fixed before examining seed set:

- week 1 = higher contemporaneous partner availability / higher-overlap window;
- week 4 = lower contemporaneous partner availability / lower-overlap window.

The contrast is not oriented merely because week 1 is earlier.

Registered timing fields:

- `phenology_source = experimental_timing`
- `timing_metric_type = experimental_plant_shift`
- `timing_analysis_class = strict_window`
- `timing_domain = ordered_by_measured_window`
- `exposure_direction = synchrony`

## Final reproductive outcome

After the one-week pollination exposure, plants were standardized and mature seeds were later collected. Seed set was calculated per plant as mature seeds divided by flowers produced. Thus the outcome is a final plant reproductive endpoint, not visitation, pollen deposition, or an intermediate proxy.

## Published quantitative information

The dissertation reports the four experimental groups as:

| flowering cohort | n | observed seed set relative to maximum |
|---|---:|---:|
| week 1 | 10 | 0.85 |
| week 2 | 10 | 1.00 |
| week 3 | 10 | 0.91 |
| week 4 | 10 | 0.69 |

For this same outcome and these same four balanced groups, the source reports:

`F(3,36) = 1.01`.

The figure caption independently confirms means ± SEM from ten plants per week (N=40).

## Variance reconstruction

Let the published common-scale group means be

`m = [0.85, 1.00, 0.91, 0.69]`

with `n = 10` per group.

For a balanced one-way ANOVA,

`F = MS_between / MS_within`.

Therefore:

- grand mean = 0.8625;
- `SS_between = n * sum((m_i - grand_mean)^2) = 0.51075`;
- `MS_between = 0.51075 / 3 = 0.17025`;
- `MS_within = 0.17025 / 1.01 = 0.1685643564`;
- pooled within-group SD = `sqrt(MS_within) = 0.4105658978`.

The relative means differ from the original seed-set means only by one common positive scale factor. Both the mean difference and pooled SD receive that same factor, so the standardized mean difference is unchanged.

For week 1 (high partner availability) versus week 4 (low partner availability):

- Cohen's `d = (0.85 - 0.69) / 0.4105658978 = 0.3897060152`;
- df for the two-group contrast = 18;
- project small-sample correction `J = 1 - 3/(4*18 - 1) = 0.9577464789`;
- **Hedges' g = +0.3732395638**;
- **sampling variance = 0.1873253239**;
- contrast sample size = 20.

The executable reconstruction is implemented in `hedges_g_from_balanced_anova_means()` and covered by a regression test.

## Why this is not prohibited conversion or imputation

This extraction does **not**:

- convert a regression slope into an SMD;
- invent an SD, SE, or within-group correlation;
- digitize error bars;
- use seed-set values to decide which flowering week had greater partner availability.

The reported ANOVA F contains the pooled within-group residual variance for the same outcome and the same four balanced groups. Given all four group means and equal n, the pooled SD follows algebraically from the ANOVA identity.

## Source-rounding sensitivity

The source prints the relative means to two decimals and F to two decimals. Varying the non-maximum means by ±0.005 and F from 1.005 to 1.015 keeps the reconstructed Hedges g approximately within **+0.353 to +0.393**. The small positive effect is therefore not a sign artifact of reported rounding.

## Dependence

This programme is independent of IWE027 (*Phyllodoce aleutica* in Japan).

The effect receives:

`DEP_MERTENSIA_GALLAGHER_CAMPBELL_RMBL`.

This programme-level identifier is deliberately conservative. If IWE025 or another *Mertensia ciliata* RMBL analysis from the same research programme is extracted later, it should share this dependence ID unless source-level evidence establishes independence.

## Replication consequence

The native SMD family now has:

- mutualist: **2 independent clusters** — IWE027 and IWE023;
- antagonist: 1 independent cluster;
- mixed pollinating seed predator: 1 independent cluster.

Mutualist replication reaches the frozen minimum evaluability gate. H1 as a three-class comparison remains unavailable until antagonist and mixed each reach two independent SMD clusters.
