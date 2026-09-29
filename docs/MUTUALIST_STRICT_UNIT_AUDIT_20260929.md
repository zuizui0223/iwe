# Mutualist strict-effect unit audit — 2026-09-29

Scope: the four current real strict mutualist effects after the antagonist consistency re-audit.

Decision: **retain all four strict effects, but register three different unit semantics rather than treating all reported n values as the same kind of replication.**

## Why this audit was needed

The 2026-09-28 antagonist re-audit made clear that two distinct questions had been conflated:

1. does the source provide an admissible independent partner-activity window?
2. what biological unit is replicated by the response variance?

A valid strict effect needs a valid partner window, but its response variance does not necessarily imply replication of the timing exposure itself.

The new unit-provenance registry therefore separates:

- exposure grain;
- response sampling grain;
- variance interpretation;
- inference scope;
- causal-claim permission.

## IWE023 — Mertensia ciliata

Source: Gallagher & Campbell 2020, DOI `10.1002/ajb2.1439`  
Data: Dryad DOI `10.7280/D19X0D`

### Design

Sixty potted plants were overwintered and flowering was delayed at high elevation. In 2015, 10 randomly selected plants per week were moved back to RMBL, where warmer conditions induced flowering. Forty plants flowered, forming four weekly phenology groups.

Pollinator visitation was observed directly during each flowering week.

Seed set was calculated per potted plant from mature seeds / flowers.

### Unit decision

Exposure and response are both plant-level.

- design: `experimental_individual_timing`
- exposure grain: plant
- response grain: plant
- variance: `individual_effect_sampling`
- inference: `experimental_manipulation`
- causal claim allowed: yes

This is the cleanest unit alignment in the current strict corpus.

### Quantitative note

The public Dryad archive also exposes `gallagher&campbell_phenologyExperimentData.xlsx` (file-stream ID 341732), so the current ANOVA-based SMD reconstruction could in principle be upgraded to a direct raw plant-level calculation.

This execution environment receives HTTP 403 for the Dryad binary download, so the current source-backed ANOVA reconstruction remains in place. The raw upgrade is optional; it is not required for validity.

## IWE029 — Stigmaphyllon paralias

Source: Carneiro & Machado 2025, DOI `10.1093/aob/mcaf126`

### Design

The same population was sampled at two distinct seasonal periods separated by 3–4 weeks:

- peak flowering, when pollinator visitation was scarce;
- late flowering, after continued monitoring identified high pollinator activity.

Different plants were used at the two sampling periods. The study initially used 90 flowering individuals at each period, with plants at least 3 m apart. The seed-set model is plant-level.

Pollinator visitation was independently supported by oil-bee visit lesions and direct observation of three *Centris* species.

### Unit decision

The exposure is an observed individual flowering-period category, not a randomized seasonal treatment.

- design: `observational_individual_timing`
- exposure grain: plant
- response grain: plant
- variance: `source_model_sampling`
- inference: `descriptive_association`
- causal claim allowed: no

The published flowering-time coefficient and SE are valid for the observed plant-level temporal association. They must not be described as replicated manipulation of season or pollinator abundance.

## IWE027 — Phyllodoce aleutica

Source: Kameyama & Kudo 2009, DOI `10.1093/aob/mcp037`

### Design

At each of two sites, HIS and GOS, three 20 × 20 m plots were established along the snowmelt gradient: E, M and L.

In 2007, bumble-bee visitation was measured directly. A 5 × 5 m quadrat was established in each plot at peak flowering, and pollinator identity/caste and visitation were recorded across the season. Worker bumblebees appeared in late July and visitation increased sharply.

For natural seed set, 24 inflorescences were selected randomly in each plot. One intact flower per selected inflorescence was marked and its final mature-seed set was measured.

### Unit decision

The timing context is plot-level; the response sampling is inflorescence-level within each fixed plot.

- design: `fixed_context_group_comparison`
- exposure grain: plot
- response grain: inflorescence
- variance: `within_context_response_sampling`
- inference: `descriptive_association`
- causal claim allowed: no

The reported n=24 per plot therefore quantifies uncertainty in each plot's sampled seed-set distribution. It does **not** mean that the E/M timing context was replicated 24 times.

This does not invalidate the descriptive SMD. It limits the claim: the effect is a standardized contrast between fixed observed plot contexts under independently measured same-season pollinator activity.

HIS and GOS provide two site-specific contrasts but remain one conservative programme-level dependence cluster.

## Why IWE027 does not recreate the IWE011 problem

Both IWE027 and former IWE011 use responses sampled within fixed plots.

The decisive difference is partner-window provenance.

IWE027 directly measured pollinator visitation in 2007 and therefore passes the independent partner-window gate.

IWE011 did not recover an independent adult-*Phaulernis* activity series; the seasonal window was based on oviposition/egg observations. Its strict row remains withdrawn for that reason.

Thus fixed-context response sampling is not itself a strict-timing failure. It is an inference-scope constraint.

## Current corpus consequence

No current strict mutualist effect is removed by this audit.

The current real strict corpus remains:

- IWE029: 1 log-odds-ratio row;
- IWE027: 2 SMD rows, one dependence cluster;
- IWE023: 1 SMD row, one independent dependence cluster;
- antagonist: 0 strict rows;
- mixed: 0 strict rows while IWE015 remains on quantitative hold.

The mutualist SMD discovery milestone therefore remains two independent programme clusters, but only IWE023 has experimentally aligned individual-level exposure and response units.

## Forward rule

Every future strict effect must now pass **both**:

1. strict partner-window provenance; and
2. strict effect-unit provenance.

A future fixed-context comparison can be admitted as descriptive strict evidence when partner timing is independently measured and the response sampling unit is defensible, but its variance must be labeled as within-context response sampling and no causal timing-treatment claim is allowed.
