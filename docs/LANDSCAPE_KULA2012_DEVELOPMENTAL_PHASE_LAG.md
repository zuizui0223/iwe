# Kula 2012 — developmental phase lag reverses the cost of synchrony

Date: 2026-10-02  
Programme: *Silene stellata × Hadena ectypa*, Mountain Lake Biological Station  
Source: Abigail A. Rogers Kula 2012 PhD dissertation, Chapter 3  
Repository: University of Maryland DRUM, handle `1903/12597`  
Landscape role: mixed-system mechanism showing that adult/oviposition synchrony and larval cost synchrony can have opposite geometry.

## Design

Chapter 3 followed individual *S. stellata* plants through the 2008 and 2009 flowering seasons.

The programme measured through each season:

- adult *H. ectypa* visitation;
- co-pollinator visitation;
- individual plant flowering;
- *H. ectypa* oviposition;
- larval density;
- initiated fruit set;
- flower and fruit predation.

New flowers on focal plants were marked repeatedly, allowing individual flowering distributions to be combined with the population oviposition curve.

The source synchrony score is:

`Synchrony_i = sum_t proportion_of_plant_i_flowers_open_t × eggs_per_flower_t`.

This is a realized oviposition-window metric, not an independent adult-availability score.

## The key result: the sign reverses between years

Synchrony had no detectable effect on initiated fruit set in either year:

- 2008: chi-square = 2.33, p = 0.1271;
- 2009: chi-square = 2.21, p = 0.137.

But synchrony strongly predicted flower/fruit predation in **opposite directions**:

- **2008:** higher synchrony -> higher predation, chi-square = **46.47**, p < 0.0001;
- **2009:** higher synchrony -> lower predation, chi-square = **16.74**, p < 0.0001.

Mean synchrony was about twice as high in 2009:

- 2008: 0.16 ± 0.01 SE;
- 2009: 0.32 ± 0.03 SE.

Mean predation was:

- 2008: 0.34 ± 0.03 SE;
- 2009: 0.46 ± 0.04 SE.

The reversal therefore cannot be summarized as a universal positive or negative effect of adult/oviposition synchrony.

## Developmental phase lag is a plausible mechanism, not a proven threshold

The source finds opposite significant synchrony–predation relationships in the two years. Flowering and oviposition shifted much more than the detected larval activity, and mean fruit maturation was faster in 2009.

Relative to the **first larva observed on a focal plant**:

- 2008: first flowering preceded detection by **10 days**, first egg by **5 days**;
- 2009: first flowering preceded detection by **17 days**, first egg by **15 days**.

Mean time from flower marking to end-of-season collection of its fruit/flower set was:

- 2008: **21.3 ± 0.28 SE days**;
- 2009: **16.7 ± 0.40 SE days**.

The dissertation proposes that earlier flowering/oviposition in 2009 gave fruits a longer developmental lead before *large, mobile* larvae became abundant. This is biologically plausible but does not establish the beginning of feeding.

**Observation-lag limitation, verified in the original Methods:** focal plants were visited every **2–4 days**. Larvae were usually first detected *after* they started moving among flowers, at approximately **10–15 mm** body length. The cited third-instar comparison is to related *Hadena bicruris*, not a direct measurement of the first feeding instar of *H. ectypa*. Thus the first recorded larva is a **delayed detection event**, not a measured onset of damage.

**Fruit-state limitation:** the maturation interval is calculated from flower marking to an end-of-season collection date based on fruit/flower condition. The actual date on which an individual fruit becomes unavailable to feeding larvae is not directly estimated.

## Descriptive margin to first **detected** mobile larva — uncertainty audit

The source summaries support a descriptive calendar margin, not a hardening or refuge threshold:

`detection margin = first detected larva date - first flowering date - mean collection/maturation interval`.

This margin uses the source's *earliest flowering date* and *first observed mobile larva*, not a matched individual egg–larva–fruit development trajectory.

| Year | Detection lag from first flower | Mean collection interval ± SE | Detection margin | Maturation-only ±2SE range | Observed synchrony–predation sign |
|---|---:|---:|---:|---:|---|
| 2008 | 10 d | 21.3 ± 0.28 d | **−11.3 d** | −11.86 to −10.74 d | positive |
| 2009 | 17 d | 16.7 ± 0.40 d | **+0.3 d** | **−0.50 to +1.10 d** | negative |

The ±2SE range is only a sensitivity check for the **mean collection interval** under the original reported SE. It is **not** a full confidence interval for the interaction phase because first-larva detection error, between-plant variation, flower-stage uncertainty and the unknown start of feeding are unquantified.

The 2009 margin crosses zero even before those additional uncertainties are considered. **The data do not demonstrate that fruits matured before larvae began damaging them.** It would be incorrect to classify 2009 as a confidently positive “safety margin” or to claim an experimentally identified zero-crossing threshold.

The descriptive contrast—much greater flower-to-detected-larva lead and faster average collection/maturation in 2009—remains compatible with the source's stage-lag explanation of the opposite predation slopes. It is not an independent test or a confirmed threshold mechanism.

The derivation remains executable in `scripts/build_kula2012_phase_margin.py` and writes `data/derived/kula2012_phase_safety_margin.csv` (historical filename retained for compatibility). The generated columns explicitly refer to **detection**, retain the maturation-only ±2SE check and set `damaging_onset_directly_observed=False` in both years.

## General mechanism

For interactions with delayed consumer stages, the effective cost window is not the adult or oviposition window itself.

Conceptually:

`effective_cost_window = exposure_window ⊗ consumer_developmental_lag × host_vulnerability`.

The convolution symbol is bookkeeping, not a fitted kernel in this analysis.

This yields a more precise version of the landscape hypothesis:

> adult synchrony predicts benefit only through the adult service stage; offspring-mediated cost is shifted by development time and by how host tissue vulnerability changes before consumers begin feeding.

This mechanism connects the mixed Silene-Hadena result to the Cardamine-Anthocharis active-egg filter: in both systems, the realized damaging window is displaced from raw interaction timing by consumer development and host state.

## Relation to IWE015

The 2008-2009 Chapter 3 data belong to the same Mountain Lake *S. stellata-H. ectypa* research programme as later IWE015 work and therefore do **not** create an independent mixed dependence cluster.

They are nevertheless important for interpreting the opposite-sign 2012/2013 diagnostic IWE015 effects: interannual changes in developmental phase relations provide a source-backed mechanism by which greater focal-partner overlap can change sign in net reproductive consequences.

No cross-year causal identity is assumed; this is a mechanistic precedent, not a post hoc explanation of the later data.

## Attempted closure to final successful fruit — not recoverable from the public summaries

The Chapter 3 methods were re-audited against the dissertation PDF itself.

Every newly opened focal flower was individually marked, and at the end of the season all flowers and fruits were collected by plant and marking period and assessed in the laboratory. The source therefore **did record a successful-fruit state** at the underlying flower level.

However, the published Chapter 3 summaries expose only two plant/marking-period proportions:

1. **initiated fruit set** = fruits initiated / total flowers, where initiated fruits include both fruits with seeds and fruits later eaten by *H. ectypa*, but exclude unpollinated flowers and flowers eaten before fruit initiation;
2. **predation** = flowers eaten + fruits eaten / total flowers, excluding unpollinated flowers and successful fruits.

Those two aggregates do not identify the successful-fruit proportion.

In particular,

`initiated fruit set - predation`

is **not valid**, because predation contains both:

- eaten fruits, which are included in initiated fruit set; and
- eaten flowers, which are not included in initiated fruit set.

The dissertation tables and Appendix A provide synchrony, initiated fruit set, predation, flowering dates and maturation timing, but do not publish the separate eaten-flower versus eaten-fruit counts needed to recover successful fruits.

Therefore no final post-cost fruit metric is reconstructed from Chapter 3.

The exact unlock would be the underlying flower-level fate table or a source-backed summary that separates:

- unpollinated flowers;
- flowers eaten before fruit initiation;
- fruits eaten after initiation;
- successful mature fruits.

Until such an object is recovered, the phase-safety-margin result remains a **cost-channel mechanism**, not a final-fitness effect.

## Claim boundary

This component is not a strict mixed net-fitness effect:

- synchrony is based on egg receipt/oviposition rather than independent adult activity;
- initiated fruit set is a benefit-channel intermediate;
- predation is a cost channel rather than final viable-seed production.

It is registered as `mechanism_only` and shares the Mountain Lake dependence cluster.

Source-backed values are stored in
`data/source_reconstructions/kula2012_silene_phase_lag.csv`.
