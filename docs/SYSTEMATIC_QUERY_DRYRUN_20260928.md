# Systematic-query dry run — antagonist/mixed discovery

Date: 2026-09-28  
Status: **discovery only; does not satisfy any required search-run row**

## Purpose

Before executing the registered Web of Science / Scopus / dissertation search runs, IWE used broad web discovery with wording aligned to the planned antagonist and mixed query families.

This was a sensitivity check for obvious omissions in the targeted corpus, not a substitute for the systematic-search coverage gate.

No row in `data/registry/search_runs.csv` is marked completed by this exercise.

## Query concepts

The dry run combined variants of:

- `flowering phenology`, `phenological synchrony`, `flowering time`, `mismatch`;
- `seed predator`, `herbivore`, `florivore`, `oviposition`;
- `seed production`, `seed set`, `fruit set`, `fitness`, `reproduction`;
- `pollinating seed predator`, `nursery pollination`, and named nursery-pollination clades.

## New publications recovered

### IWE033 — Thompson & Gilbert 2014

DOI: `10.1016/j.baae.2014.05.003`  
System: *Thymus decussatus × Pseudophilotes sinaicus*  
Decision: `context_only`

Why it was new/useful:

- directly measures plant flowering and specialist-herbivore timing;
- explicitly frames the system as phenological synchrony;
- larvae consume buds and flowers.

Why it does not enter Tier A:

- the reported response is butterfly timing/abundance/population dynamics;
- no plant seed/fruit/fecundity endpoint is attached to the synchrony contrast.

### IWE034 — Fogelström et al. 2017

DOI: `10.1002/ecy.1676`  
System: *Cardamine pratensis × Anthocharis cardamines*  
Decision: `context_only`

Why it was new/useful:

- experimentally manipulates butterfly phenology relative to genetically identical host populations;
- relative phenology determines which flowering phenotypes receive attack.

Why it does not enter Tier A:

- the reported timing-facing response is butterfly preference/attack-mediated selection;
- no final plant seed/fruit/fecundity endpoint is reported for the synchrony manipulation.

### IWE035 — Valdés & Ehrlén 2021

DOI: `10.1002/ecy.3466`  
System: *Lathyrus vernus* with vertebrate grazers and predispersal seed predators  
Decision: `context_only`

Why it was new/useful:

- 21 years of flowering phenology, antagonist interaction intensity and plant fitness;
- final plant response includes intact seed production.

Why it does not enter strict synchrony:

- grazing and seed-predation intensities are realized interaction/damage measures;
- no independently measured antagonist activity window is used to order plant timing;
- interaction intensity cannot be recycled as the partner-availability curve.

## Dry-run result

The targeted corpus gained **three biologically relevant antagonist publications** but:

- strict Tier-A rows added: **0**;
- independent strict SMD clusters added: **0**.

The three failures illustrate distinct evidence-architecture gaps:

1. good synchrony + no plant fitness;
2. experimental synchrony + mechanism/attack but no final plant fitness;
3. plant timing + final fitness but no independent partner-timing reference.

## Claim boundary

This dry run cannot be used to estimate how common these failure modes are in the literature.

Its purpose is only to:

- identify obvious missing publications before formal searches;
- test whether the frozen eligibility contract behaves sensibly on new records;
- preserve discovery provenance;
- provide anchors for the later required citation-snowball run.

Formal search coverage remains `targeted_only` until all required search runs are executed, exported and deduplicated.
