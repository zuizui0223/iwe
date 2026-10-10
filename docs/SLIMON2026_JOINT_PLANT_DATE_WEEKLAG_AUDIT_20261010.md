# IWE / Slimon 2026 — does a delayed host stage explain newly observed Mompha?

Date: 2026-10-10. Original public source:
[Slimon & Agrawal (2026), DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509).
Original source ZIP: `Freese Stats.zip`, fixed MD5
`151bbd516fc0032af2a2598cb5529c78`.
Executable source-linked audit:
`scripts/analyze_slimon2026_joint_fe_weeklag.py`.
Results receipt:
`data/source_reconstructions/slimon2026_joint_fe_weeklag_source.csv`.

**Scope:** a retrospective, outcome-exposed, exploratory analysis of
visible host-associated *Mompha* stage counts. There is NO original
recovered plant-by-plant net intact-seed fitness, independent adult
Mompha emergence/flight series, bud abundance, individual oviposition
date or direct randomized flowering-timing intervention.

## Biological question (not merely model selection)

Open flowers are a potentially misleading partner reference for a
*bud-boring* insect. At a weekly visit, newly visible *Mompha*
may represent the consequence of an earlier host tissue interaction
rather than an interaction occurring on the same visit. We ask whether
the source's measured `new Mompha>0` incidence is more associated
with **last week's**, **this week's**, or even **next week's**
open-flower status when both stable plant heterogeneity and seasonal
survey date are held constant.

The source's `new Mompha` columns are apparent new *visible
detections*, not directly timed oviposition. The prior week's **open**
flower is not necessarily the same bud, nor the relevant number of
susceptible buds. A timing lag in these series therefore cannot prove a
biological larval incubation interval.

## Original data contract

From the original `df2_exp1/2.csv` and
`df2_exp1_M/df2_exp2M.csv` files, join by
**source experiment × original plant ID × identical 2023 survey DOY**.
Count positivity (`Mompha>0`) instead of interpreting the numerical
counts as independent insects/offspring.

An analysis row exists only when the **same plant** has genuinely
recorded observations at time `t−7`, `t`, and `t+7`;
do NOT assign nearest survey, assume zero for a missing week, use
relative figure dates, or treat repeated rows as distinct
organisms. Both experiments flowered in **2023** and together form
**one** original biological programme.

This yields:

| Original source | Complete source plants | Complete `t±7` plant-visits | Survey days | Mompha-positive visits |
|---|---:|---:|---:|---:|
| exp1 | 148 | 1,055 | 8 | 390 |
| exp2 | 123 | 731 | 7 | 199 |

## Descriptive analysis and controls

Linear probability model for each original experiment separately:

`Mompha_visible_i,t ~ plant_i_FE + original_survey_day_t_FE + open_i,t−7 + open_i,t + open_i,t+7`.

Here `open_i,t` is binary `original flower count > 0`.
Each slope is the original source-unit adjusted difference in the
linear fitted detection probability, **not an oviposition probability
or a causal risk effect**.

The models also contrast plant+date FE baseline with only prior,
only present, or only following floral state, **on precisely the same
complete-case source subset**. Additional in-sample FE R² is
for diagnostic fit, **not** independent predictive validation.
The `t+7` state is a deliberately **imperfect comparator**, because
future flowering reflects the same plant's persistent reproductive
state and some of the same undetected buds; it cannot constitute a
clean mechanistic negative control.

For coefficient stability only, the bootstrap resamples **source
plant IDs** with replacement 160 times. Repeated weeks move with
their source plant. Report the percentile 2.5–97.5 ranges
descriptively. This does NOT account for fully joint
plant×calendar date/site/treatment dependence, the ex post
hypothesis or uncertainty in true bud availability, and it is
NOT a confirmatory CI, p-value, or repeated independent trial.

## Original source-derived findings

| Original experiment | Prior `t−7` slope | Current `t` slope | Following `t+7` slope |
|---|---:|---:|---:|
| exp1 | **+0.255** | +0.163 | −0.016 |
| exp2 | **+0.183** | +0.028 | −0.087 |

Plant bootstrap percentile ranges for prior open-flower status:
- exp1: **[+0.185, +0.315]**
- exp2: **[+0.069, +0.282]**

For current flowering:
- exp1 **[+0.094, +0.245]**
- exp2 **[−0.081, +0.126]**.

For following flowering:
- exp1 **[−0.101, +0.053]**
- exp2 **[−0.164, +0.025]**.

The **prior week's** open-flower status has the largest
positive joint-adjusted coefficient in both experiments. In a
one-variable-at-a-time sensitivity using the **same matched source
plants/visits** plus plant+date FE, previous week's
`open` has incremental in-sample FE R² of **0.0677** in exp1
and **0.0320** in exp2; same-day `open` yields **0.0250**
and **0.0006**. Future `open` yields **0.0035** and **0.0113**.
The full three-axis model provides incremental in-sample
FE R² **0.0914 / 0.0378** respectively.

This rejects, as a **description of these observed series**,
the simplistic idea that Mompha's visible stage can only be
associated with contemporaneously open flowers. It is **compatible
with** stage-detection delay, susceptible buds preceding full
anthesis, persistence of plant reproductive state, and many
other temporal dependencies. It does not distinguish those
mechanisms, and could also involve time-varying plant resources,
survey detection bias, or previous unobserved stages.

## Hard stop / research consequence

1. Do not call `open_t−7` the actual bud-infestation/oviposition
   event. We do **not** have source bud counts or individual moth
   tracking/egg times.
2. Do not call `open_t+7` a clean negative control; it is the
   following observation of the **same potentially persistent host
   reproductive process**.
3. Do not use post-hoc model fits as forward prediction or as
   estimates of natural selection on flowering duration.
4. Do not turn the source's estimated `fitness_seed` from
   genotype multipliers and damage-weighted fruit counts into an
   observed seed endpoint.
5. These two experiments are components of one source programme,
   not two independent years/clusters.

This is a **new within-programme source-grounded empirical timing
result**, but contributes **zero strict-H1 antagonist clusters**.

### Next decisive discriminator

Recover **bud abundance at the previous survey, oviposition
timestamps or early egg/larval stage** and track their conversion
to visible Mompha and ultimately intact seeds within the same
original plant/flower units. Only then can the hypothesized
stage-conversion delay be independently identified rather
than inferred from correlated floral states.
