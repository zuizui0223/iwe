# Slimon & Agrawal (2026): does an open-flower/Mompha detection association survive survey-date and plant conditioning?

Date: 2026-10-10. Original source: [Zenodo DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509), exact `Freese Stats.zip` original MD5 `151bbd516fc0032af2a2598cb5529c78`. Analysis: `scripts/analyze_slimon2026_date_plant_controls.py`. Source-derived, two-row numerical receipt: `data/source_reconstructions/slimon2026_date_plant_stage_confounding.csv`. **Non-promoting exploratory test.**

## Two plausible explanations to distinguish

Prior IWE source audit found that a newly visible `Mompha` count is positive in more **same-plant survey visits** with open flowers than without open flowers. But this is not necessarily stage choice: the association could arise from the calendar date (flower and insect activity co-occur seasonally) or stable plant heterogeneity (large flowering individuals attract or support more insects).

The critical original biology is that *Mompha stellella* is a **bud** consumer, not a specialist ovipositing into already open corollas. This audit does **not** turn a current open-flower snapshot into a valid flower-bud denominator or treat observation as the date of moth oviposition.

## Methods held constant

Original source-wide `df2_exp1/2.csv` weekly flower counts and `df2_exp1_M/df2_exp2M.csv` weekly new Mompha counts were joined on **original plant ID × exact 2023 survey date**. Missing source dates or counts were not zero-imputed. The two experiments are components of one 2023 programme, not two independent annual replications.

Three prespecified, distinct **descriptive** estimands were calculated:

1. **Pooled plant-visit positive fraction difference**, open-flower snapshot versus no-open-flower snapshot.
2. **Within-exact-date positive fraction difference**. For each date with both open and zero-open plants, take the positive fraction contrast, then average with balance weight `n_open*n_no_open/(n_open+n_no_open)`. This conditions on calendar survey day but not stable plant size/propensity.
3. **Within-original-plant difference**, contrasting each plant's open-versus-zero-open observations when both were present; average using the analogous balance weight. This conditions on time-invariant plant properties but **not** calendar date.

The two conditioning analyses are separate **one-confounder-at-a-time** sensitivity tests, not a joint fixed-effect model. Cluster bootstrap samples **original plant IDs** (400 resamples, seed 20261010) and carries each plant's repeated visits together. The 2.5–97.5 percentile ranges are **descriptive plant-resampling stability intervals**, *not* validated causal or hierarchical population confidence intervals; survey-date-level and site-level dependence and measurement/detection biases remain.

## Original derived results

| Measure | Experiment 1 | Experiment 2 |
|---|---:|---:|
| Original plant IDs in these **two** observation sheets | 150 | 123 |
| Exact-date matched plant-visits | 1,470 | 987 |
| Exact calendar survey dates | 11 | 9 |
| Positive / visits with open flowers | 115 / 270 = 42.6% | 36 / 110 = 32.7% |
| Positive / visits with zero open flowers | 291 / 1,200 = 24.3% | 188 / 877 = 21.4% |
| Raw pooled positive-rate difference | **+18.34 pp** | **+11.29 pp** |
| Within-exact-date difference | **+18.35 pp** | **+11.14 pp** |
| Plant-resampling range, date-conditioned | [+13.06, +24.20] pp | [+1.42, +20.06] pp |
| Within-original-plant difference | **+15.64 pp** | +6.46 pp |
| Source plants with both snapshot states | 123 | 74 |
| Plant-resampling range, plant-conditioned | [+10.31, +21.84] pp | [−3.12, +16.34] pp |

**Why experiment 1 here contains 150 plants/1,470 visits whereas PR #91 listed 149 plants/1,468 visits:** this particular open-flower-vs-Mompha comparison requires only the **two original dated source observation sheets**. PR #91 used an **additional intersection with individual first/last flowering date records**, losing one plant and two visits. The populations and estimands are different. The previous 149/1,468 values are not incorrect. **Never mix their denominators or interpret the extra plant as new annual replication.**

### Ecological inference and limits

- The open-flower-positive association is **not entirely explained by source survey-day timing** in either experiment: date-conditioned descriptive differences are close to pooled differences. This is evidence **against a pure between-survey-date compositional explanation**, not against all seasonal/detection confounding.
- The plant-conditioned comparison is weaker, particularly in experiment 2, where its plant-resampling interval includes zero. Stable between-plant characteristics explain **some** of the unadjusted comparison or at least alter which observations have weight; the decomposition does not identify how much is causal confounding.
- Both estimates remain consistent with plants in a high overall reproductive state having **buds and open flowers concurrently**, while a bud-borer's observed presence is delayed or persists after its original entry. This is **a plausible mechanism**, not proof of preferential selection for any tissue-stage.
- Original data still lack a verified independent adult **Mompha** flight curve, true bud-at-risk counts on each date, direct oviposition timestamps and same-plant observed net intact mature seed output. `new Mompha` source counts may represent detection/phenological stages of host-associated insects, not egg deposition.
- The source is outcome exposed and this is exploratory, not prospective out-of-sample prediction, preregistered causal estimation, or replication of strict H1.

**Admission:** strict H1 antagonist clusters added **0**; dataset remains one independent biological programme with two 2023 experiments. The updated interpretation is to replace the claim that zero-open snapshots reveal a preference with the narrower result: **open flowers mark a period of elevated host-associated Mompha detection even after controlling separately for survey date and plant identity**. Additional first-principles measurement must target **buds and oviposition**, not simply the same-date open-flower counts.
