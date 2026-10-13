# Positioning against Kharouba et al. 2023: from mismatch prevalence to temporal signal propagation

Date: 2026-10-07  
Source: Kharouba et al. 2023, *Lack of evidence for the match-mismatch hypothesis across terrestrial trophic interactions*, Ecology Letters  
DOI: `10.1111/ele.14185`

## Why this paper is the nearest macro-scale precedent

Kharouba et al. provide the closest existing quantitative test of a general phenological match-mismatch rule in terrestrial systems.

Their quantitative corpus contains:

- 20 studies;
- 26 antagonistic consumer-resource interactions;
- at least five site-year timing/fitness datapoints per interaction.

They define relative timing as the difference in **calendar days** between consumer and resource phenology, usually using a midpoint or other source-backed estimate of each seasonal distribution.

Fitness is standardized within each interaction and they fit hierarchical linear and quadratic fitness-vs-relative-timing relationships.

## Their core negative result

They do not recover the canonical general prediction that fitness peaks at exact synchrony and declines on both sides.

Across 26 interactions:

- hierarchical quadratic coefficient = **-1.7 × 10^-4 standardized fitness/day**, 90% CI **-5.0 × 10^-4 to +8.0 × 10^-5**;
- quadratic versus linear predictive difference: **elpd_diff = -2.6**, insufficient to favor the quadratic model;
- 13/26 interactions show no support for match-mismatch;
- 4/26 show the predicted quadratic peak;
- 7/26 show a supporting linear relation, but 6/7 sample only one side of asynchrony.

The overall hierarchical linear relationship is weakly negative:

- **beta = -5.2 × 10^-3 standardized fitness/day**;
- 90% CI **-0.011 to -0.0035**.

Thus their result is not that timing never matters. It is that one general calendar-relative fitness curve is not prevalent across the terrestrial antagonistic systems sampled.

## What Kharouba et al. already identify

IWE must not claim novelty for the generic idea that the timing metric may be biologically misspecified.

Kharouba et al. explicitly note that:

- only 6/26 interactions define the expected match a priori;
- different fitness components can respond differently to timing;
- only two cases measure total fitness;
- a common metric such as relative calendar days may be insufficient;
- overlap integrals, lifespan/life-stage information and "biological time" may provide better coordinates.

They therefore already motivate life-stage-aware phenological metrics.

## What IWE adds

The IWE pivot addresses a different empirical question.

Kharouba asks:

> Across systems, does consumer fitness follow a general function of consumer-resource relative timing?

IWE now asks:

> What happens to a source-backed temporal signal as it propagates through successive biological stages to final plant fitness?

The distinction matters because IWE records source-backed **transformations** rather than assuming that the upstream timing coordinate is carried unchanged downstream.

Current IWE transformation states include:

- `preserved`;
- `shifted_filtered`;
- `sign_reversed`;
- `erased`;
- `buffered`;
- `tracking_inertia`;
- `preserved_net_changed_mechanism`.

Examples already show the biological meaning of those states:

- IWE011: initial and final reproduction have opposite seasonal orientation after seed predation;
- IWE032: total egg exposure is shifted and narrowed into an active future-damage window before final reproduction;
- Kula 2012: flowering × oviposition synchrony changes sign against predation as the developmental phase margin crosses zero;
- Posledovich 2015: stage matching changes consumer performance but is erased before the mature-seedpod plant endpoint;
- IWE023: a >5-fold visitation decline is buffered by pollinator composition/effectiveness before mature seed set;
- Gols 2025: identical timing-manipulation architecture is buffered in one host plant but preserved in another.

## Scope differences

Kharouba et al.:

- focus on antagonistic consumer-resource interactions;
- take the **consumer** as the fitness subject;
- require observational variation across years/sites;
- exclude experimental mismatch tests;
- use days between taxa as the common relative-timing coordinate.

IWE:

- focuses on **plant final reproduction**;
- compares mutualist, antagonist and dual-role mixed interactions;
- retains both observational and experimental timing evidence but keeps provenance explicit;
- allows multiple biological stages within one interacting partner lineage;
- asks whether timing information is transformed before it reaches final fitness.

Mixed pollinating seed predators are especially diagnostic because the same partner lineage can provide immediate adult service and delayed offspring cost.

## The current IWE hypothesis after this comparison

The manuscript should **not** argue:

> previous mismatch studies failed because they used the wrong metric, and our stage-specific metric solves the problem.

The confirmatory gate currently contains zero programmes proving such general predictive superiority.

A defensible stronger question is:

> Is the weak generality of phenological mismatch partly produced by assuming that temporal information is conserved between interaction stages?

IWE can already test the premise that conservation is not guaranteed.

Its targeted propagation corpus contains final-fitness chains in which timing signals are preserved, filtered, reversed, erased and buffered.

The remaining confirmatory task is narrower:

> When stage-specific alignment is measurable, does it predict final plant fitness better than a simpler calendar or adult-only timing coordinate?

## Safe novelty statement

> Previous syntheses showed that a common relative-timing metric has weak and heterogeneous links to fitness. We extend that problem by treating phenological timing as information that can be transformed across interaction stages, and empirically track whether source-defined temporal signals persist to final plant reproduction.

This avoids claiming that life-stage timing itself is new, and places the novelty in **cross-stage propagation to final fitness**.
