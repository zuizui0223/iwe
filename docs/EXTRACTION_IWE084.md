# IWE084 extraction receipt — Solidago graminifolia × Apis mellifera

Source: Gross RS, Werner PA. 1983. *Relationships among Flowering Phenology, Insect Visitors, and Seed-Set of Individuals: Experimental Studies on Four Co-occurring Species of Goldenrod (Solidago: Compositae).* Ecological Monographs 53:95–117. DOI `10.2307/1942589`.

Status: **strict-H1 mutualist programme quantitatively closed on a source-native standardized-mean-difference scale**.

Interaction class: `mutualist`.

Dependence ID: `DEP_IWE084_SOLIDAGO_APIS`.

## Why this study identifies a plant–partner timing contrast

The source independently monitored insect visitors through the 1980 flowering season and measured final filled-seed production of individually phenotyped goldenrod clones.

For `Solidago graminifolia`:

- Apis visual censuses were conducted from 12 August through 17 September;
- the first honeybee visits to `S. graminifolia` were recorded on 28 August;
- honeybees were uncommon before 1 September and were the dominant visitors through September;
- clones were divided into two phenological groups because of sample size;
- the source defines early clones by peak flowering **before 1 September 1980** and the complementary late group by the later peak-flowering period.

Therefore the source-defined early/late contrast is ordered by an independently observed partner-availability change before the seed outcome is converted to an IWE effect.

The IWE exposure is not calendar date itself. Calendar date only identifies the two source groups; the direct seasonal Apis record establishes that the late state represents greater effective-partner availability during flowering.

## Why only S. graminifolia enters the primary extraction

The paper contains four Solidago species, but the primary IWE effect is restricted to `S. graminifolia` for identification reasons.

### S. canadensis — excluded from primary

The source's hand-pollination experiment shows that late-flowering clones have greater maximum potential seed set than early-flowering clones even when pollen is supplied. The source therefore attributes much of its phenological seed-set difference to physiological or microenvironmental differences among clones rather than temporal pollinator availability.

### S. nemoralis — excluded from primary

Apis seasonality is relevant, but no comparable hand-pollination experiment was conducted to separate temporal pollinator limitation from intrinsic seasonal differences. Table 5 is also presented at ramet rather than clone grain, with a separate clone-level sensitivity table.

### S. juncea — excluded from primary

Apis is not the focal effective partner in the relevant flowering window; the species is primarily visited by native bees and beetles in this study, and the insect sampling does not cover the entire flowering season.

### S. graminifolia — admitted

For this species the source provides both the independent Apis timing shift and explicit mechanistic validation:

- early open-pollinated clones are pollen/pollinator limited;
- late open-pollinated clones are not detectably below their potential seed set;
- the source estimates that low pollinator frequency accounts for most of the reduction from potential seed set in early clones.

This species-selection rule is based on estimand identification, not on choosing the largest or most favorable seed-set contrast.

## Frozen outcome contrast

Use the 1980 natural/open-pollinated percentage of filled seeds from source Table 5 / Table 10 open controls.

Published values:

| partner-availability state | source phenology group | mean filled seeds | 95% CI | n clones |
|---|---|---:|---:|---:|
| lower | early | 21.71% | 14.97–29.31% | 10 |
| higher | late | 39.56% | 32.69–46.64% | 27 |

The source states that means and confidence intervals were back-transformed after angular transformation.

The within-clone pre/post-1-September comparison (34.13% versus 53.73%, n=31 heads/time state) is retained as mechanistic validation only. It is **not** the primary effect because the paired covariance is not reported and the 31 observations at the two times are not independent groups.

## Frozen effect reconstruction

The primary source-native effect family is `standardized_mean_difference`.

For each early/late group:

1. convert the published proportion mean and CI endpoints to the source angular scale:

   `theta = asin(sqrt(p))`;

2. verify that the transformed lower/upper CI distances are symmetric to rounding tolerance;
3. recover the transformed-scale standard error from the mean CI half-width using the two-sided 95% Student-t critical value with `df = n - 1`;
4. recover the transformed-scale standard deviation as `SD = SE * sqrt(n)`.

Then compute the independent-groups pooled SD:

`SD_pooled = sqrt(((n_low-1) SD_low^2 + (n_high-1) SD_high^2) / (n_low+n_high-2))`.

Define Cohen's `d` as:

`d = (theta_high - theta_low) / SD_pooled`.

Apply the small-sample Hedges correction with `df = n_low + n_high - 2`:

`J = Gamma(df/2) / (sqrt(df/2) * Gamma((df-1)/2))`;

`g = J * d`.

Sampling variance is frozen as:

`Var(d) = (n_low+n_high)/(n_low*n_high) + d^2/(2*(n_low+n_high-2))`;

`Var(g) = J^2 * Var(d)`.

The registered native effect is `g`, with positive direction meaning higher independently observed Apis availability during flowering is associated with greater final seed production.

## Numerical-source rule

Only the printed Table-5/Table-10 means, 95% CIs and clone sample sizes above enter the calculation.

IWE does not digitize Figure 11, treat its 3-day time bins as independent observations, or infer an `r` from the plotted fitted/aggregated temporal curves.

## Dependence

This is one biological programme regardless of the number of Solidago species, phenological groups, experimental pollination treatments or years:

`DEP_IWE084_SOLIDAGO_APIS`.

The registered strict row uses 1980 `S. graminifolia` only. Other source results remain within-study context/sensitivity evidence and do not create extra independent programmes.

## Causal ceiling

This is an observational timing contrast supported by direct seasonal partner monitoring and the source's pollination experiment. It should be interpreted as an association between a prospectively ordered low/high partner-availability flowering state and final reproduction, not as a randomized manipulation of synchrony.

## Frozen reconstruction result

The executable reconstruction in `src/iwe/iwe084.py` and `scripts/reconstruct_iwe084.py` uses only the published source rows stored in `data/extraction/source_rows/IWE084_table5.csv`.

The registered result is:

- early/lower-availability clones: `n = 10`;
- late/higher-availability clones: `n = 27`;
- transformed mean, early: `0.4846965804`;
- transformed mean, late: `0.6802242871`;
- recovered transformed SD, early: `0.1221815814`;
- recovered transformed SD, late: `0.1809128134`;
- Cohen `d = +1.1653423702`;
- exact Hedges correction `J = 0.9783912375`;
- **Hedges `g = +1.1401607637`**;
- **sampling variance = `0.1497495743`**.

The positive sign already has the registered IWE orientation: higher independently observed Apis availability during flowering is associated with higher final filled-seed production.

The result is entered as `IWE084_SGRAM_APIS_SMD` in `data/extraction/direct_effects.csv`.

## Claim ceiling after reconstruction

IWE084 closes one additional independent mutualist strict-H1 programme on the `standardized_mean_difference` family.

It does **not** increase the Fisher-z common-scale programme count, and it does not by itself open the cross-class H1 moderator model. Cross-family conversion remains prohibited unless a separate prospective conversion contract is added.
