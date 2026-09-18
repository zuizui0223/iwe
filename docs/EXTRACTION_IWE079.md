# IWE079 extraction receipt — Astragalus lusitanicus × Tomares ballus

Source: Jordano D, Fernández Haeger J, Rodríguez J. 1990. *The effect of seed predation by Tomares ballus (Lepidoptera: Lycaenidae) on Astragalus lusitanicus (Fabaceae): determinants of differences among patches*. Oikos 57:250–256. DOI `10.2307/3565947`.

Status: **published unresolved strict-H1 antagonist candidate; quantitative source table/data recovery pending**.

## Why this is unusually close to strict H1

The peer-reviewed source explicitly links three quantities across host-plant patches:

1. temporal availability of immature `Astragalus lusitanicus` inflorescences;
2. the `Tomares ballus` oviposition period / egg load;
3. loss of final plant fecundity through consumption of flowers and developing seeds.

The source abstract states that spatial heterogeneity in the butterfly effect on plant fecundity was explained not only by patch differences in egg load but also by **variation in synchrony between the oviposition period and temporal availability of immature inflorescences**.

This is stronger for IWE than a study in which flowering date merely predicts damage: the animal interaction window itself is part of the source explanation.

## Source eligibility

This is a formally published peer-reviewed journal article and therefore satisfies `docs/SOURCE_ELIGIBILITY.md`.

The study is independent of the currently closed IWE068 `Ipomopsis × Hylemya` antagonist programme and of provisional IWE078.

## Primary biological unit

The recoverable primary unit should be the source's biological **patch**, because the reported synchrony and fecundity heterogeneity are patch-level quantities.

Multiple plants, inflorescences or seed observations within a patch must not be promoted to independent meta-analytic programmes.

All effects from the paper share:

`dependence_id = DEP_IWE079_ASTRAGALUS_TOMARES`.

## Timing exposure

Do not invent a new overlap metric from the abstract.

Primary extraction must preserve the exact source definition used to relate:

- the `T. ballus` oviposition period / egg timing; and
- availability of immature `A. lusitanicus` inflorescences.

Before a numerical effect is entered, the full source must establish:

1. the time grain of both curves or windows;
2. whether synchrony is represented continuously, categorically, or as a source-derived index;
3. whether larger native values mean greater matching or greater mismatch;
4. whether the same timing definition is available for all patches entering the fecundity analysis.

If the published analysis contains only a qualitative synchrony interpretation and no reconstructable patch-level timing variable, IWE079 remains unresolved rather than being converted from calendar flowering date.

## Final fitness outcome

The strict endpoint must be a final plant reproductive quantity from the same patch context after seed-predator attack can act, such as:

- surviving seed production;
- realized seed set;
- final fecundity expressed in seeds or an equivalent source-defined reproductive output.

Egg load, attack incidence, larval abundance and percentage damage alone are intermediate antagonist channels and cannot substitute for final plant fitness.

## Quantitative effect route

Preferred route, in order:

1. recover source patch-level synchrony and final fecundity values and compute a Pearson correlation, then Fisher `z = atanh(r)` with `var(z)=1/(n-3)`;
2. recover a source regression coefficient with its SE/variance if it directly estimates synchrony -> final fecundity;
3. recover a prospectively orderable matched-vs-mismatched contrast with means, uncertainty and sample sizes.

If synchrony predicts only egg load while final fecundity is reported separately, the two paths are not multiplied or algebraically combined to manufacture a net effect.

## Prohibited shortcuts

IWE079 must not use as a meta-analytic effect:

- the later literature statement that attack can reduce seed production by up to about 81%;
- a P value without an effect magnitude;
- egg load as if it were final plant fitness;
- the sign of a narrative statement;
- a figure digitized by eye without a reproducible extraction procedure;
- individual flowers/seeds as independent observations when synchrony is patch-level.

## Current recovery status

Public bibliographic sources and an author-uploaded full-text record confirm that the Oikos article exists and that the central mechanism is patch-level variation in oviposition-window × immature-inflorescence synchrony tied to fecundity loss.

The currently machine-retrievable public text does not expose the required patch-level quantitative table/variance structure. Therefore no effect has been entered into `direct_effects.csv` or `common_scale_fisher_z.csv`.

## Claim ceiling

Before quantitative recovery, IWE079 supports only:

> a published antagonist study explicitly attributes among-patch variation in host-plant fecundity loss to variation in temporal matching between a seed predator's oviposition period and the host's immature reproductive structures.

It does not yet contribute an antagonist programme to the primary H1 common-scale gate.
