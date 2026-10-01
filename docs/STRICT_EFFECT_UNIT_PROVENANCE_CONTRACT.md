# Strict effect-unit provenance contract

Date: 2026-09-29  
Status: executable

## Purpose

A strict effect can have a valid partner window and still be misinterpreted if the response sampling unit is confused with replication of the timing exposure.

IWE therefore records exposure/response grain separately from partner-window provenance.

Every current real `strict_window` effect must have exactly one row in:

`data/registry/strict_effect_unit_provenance.csv`.

## Core distinction

A response can be sampled repeatedly inside one fixed exposure context.

For example, 24 inflorescences sampled inside one early-snowmelt plot provide information about the **response distribution in that plot**. They do not create 24 independent replications of the plot-level timing context.

This does not automatically invalidate a descriptive group contrast. It changes the interpretation of its variance and the scope of the claim.

IWE distinguishes:

- **individual-effect sampling** — exposure and response are assigned/measured at the same independent biological unit;
- **source-model sampling** — a source model directly estimates an individual-level observed timing contrast;
- **within-context response sampling** — response units are nested inside a larger fixed timing context such as a plot.

## Inference scopes

`experimental_manipulation`

Used only when the timing exposure is experimentally assigned at the same grain as the response unit. The current example is IWE023.

`descriptive_association`

Used for observational or fixed-context comparisons. This scope can support a strict timing–fitness association when partner timing is independently measured, but it cannot be described as a randomized/replicated causal timing treatment.

If exposure grain and response grain differ, CI requires:

- `variance_interpretation = within_context_response_sampling`;
- `inference_scope = descriptive_association`;
- `causal_claim_allowed = no`.

## Current strict effects

### IWE023 — experimental individual timing

Potted *Mertensia ciliata* plants were randomly selected each week for release from delayed-flowering conditions. Seed set is calculated per plant.

Exposure grain and response grain are both plant-level.

### IWE029 — observational individual timing

Different *Stigmaphyllon paralias* individuals were sampled during peak and late flowering periods. The source binomial seed-set model is plant-level.

The source-model SE is retained as plant-level observational model uncertainty, not as replication of season.

### IWE027 — fixed-context group comparison

At each site, E/M/L are fixed 20 × 20 m plots. The source randomly samples 24 inflorescences per plot for natural seed set.

The SMD variance describes response sampling within those fixed plot contexts. It does not imply 24 independent timing treatments.

IWE keeps HIS and GOS as two site-specific effect rows but assigns them to one conservative programme-level dependence cluster.

## Relation to the IWE011 withdrawal

The former IWE011 HA-versus-HD effect compared two fixed plots. Under this clarified unit contract, fixed-context response sampling **alone is not a universal automatic exclusion**.

IWE011 remains withdrawn because its more fundamental strict-window requirement fails: the public programme defines the moth seasonal window from oviposition/egg observations rather than an independent adult-moth activity series.

The former plant-level variance also cannot be presented as replicated timing-treatment uncertainty, but this is now an interpretation boundary rather than the sole reason for exclusion.

## Relation to Tomares

The same distinction applies to *Tomares × Astragalus*.

Patch-level response sampling is not by itself fatal to a descriptive fixed-context contrast. However, the current public Oikos summaries are nested at inflorescence grain within tagged shoots, and the partner-side synchrony series is newly laid eggs rather than independent adult availability.

A rescue therefore still requires:

1. an independent adult timing source; and
2. response variance at a defensible biological sampling unit, such as tagged shoots, if a fixed-context patch contrast is retained.

Multiple independent patches would strengthen causal/generalized inference but are not imposed as a universal prerequisite for descriptive strict association.

## Planned IWE015 unit semantics

IWE015 is currently absent from the strict corpus because its raw variance is unresolved. If raw 2012/2013 effects return, the unit semantics are predeclared as:

- `design_type = observational_individual_timing`;
- `exposure_grain = plant`;
- `response_grain = plant`;
- `variance_interpretation = individual_effect_sampling`;
- `inference_scope = descriptive_association`;
- `causal_claim_allowed = no`.

The early and late experiments use distinct plants selected in the same field population. The seasonal context is observed rather than experimentally randomized, so a returning IWE015 SMD remains descriptive despite plant-level exposure/response alignment.

## CI behavior

`scripts/validate_unit_provenance.py` fails when:

- a current real strict-window effect lacks unit provenance;
- unit provenance points to a non-current/non-strict effect;
- nested exposure/response grain is labeled causal;
- nested sampling is not explicitly registered as within-context response sampling;
- an experimental individual timing design does not align exposure and response units.

This registry does not replace dependence clustering across studies/programmes. It documents the within-effect sampling meaning before programme-level meta-analysis begins.
