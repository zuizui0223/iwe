# IWE interaction-window meta-analysis — design

Date: 2026-09-16
Status: design approved in principle; implementation not yet started

## Purpose

IWE is a **meta-analytic empirical project**, not a new theory repository.

Its central question is:

> Does the fitness effect of phenological synchrony depend on interaction type?

The project will test this by synthesizing published plant–animal studies in which phenological overlap (or a directly related timing mismatch measure) and a reproductive or fitness consequence can be linked at the same biological scale.

The project will remain scientifically independent from SCH, BALANCE, SLK, BITA and PAYOFF. Those repositories may later use IWE results as empirical motivation or external context, but IWE will not estimate `L`, `R`, `K`, `Phi`, accessibility, invasion, fixation, occupancy, or BITA mechanism allocations.

## Primary hypotheses

### H1 — interaction-type moderation

The effect of phenological overlap on plant reproductive performance differs among interaction types.

Primary moderator classes:

1. `mutualist` — animal interaction is expected to increase plant reproductive performance through pollination or another directly beneficial reproductive service;
2. `antagonist` — animal interaction is expected to reduce plant reproductive performance through florivory, seed predation, ovule predation, or another direct reproductive cost;
3. `mixed_pollinating_seed_predator` — the same animal lineage or species provides pollination while its offspring consume reproductive tissue or seeds.

Primary prediction:

- mutualist systems: more synchrony tends to improve reproductive performance;
- antagonist systems: more synchrony tends to reduce reproductive performance;
- mixed systems: the net effect differs from both simple classes and may be weak or non-monotonic.

The interaction among overlap and interaction type is the primary inferential target. No universal sign is required for publication.

### H2 — non-monotonic synchrony in mixed interactions

Within `mixed_pollinating_seed_predator` systems, net reproductive performance may peak at intermediate synchrony because increasing overlap can increase both pollination benefit and seed-predation cost.

Primary mixed-system extension:

`fitness ~ overlap + overlap^2`

The quadratic term is tested only in the mixed class and only when the number and distribution of independent biological units make curvature estimable. Failure to detect curvature is a valid result.

### H3 — redundancy as a mismatch buffer

Where effective partner redundancy is measurable independently of the focal outcome, greater redundancy reduces the magnitude of reproductive loss associated with mismatch.

This is a secondary hypothesis, not required for the primary paper to close.

## Secondary moderators

Secondary moderators are predeclared but will not redefine the primary estimand:

- partner specialization / obligacy;
- effective partner redundancy;
- latitude;
- elevation;
- climatic seasonality;
- island versus mainland context;
- annual versus perennial plant life history;
- natural observational versus experimental phenology manipulation;
- direct interaction phenology versus occurrence-derived potential phenology.

These moderators are reported with uncertainty and are not used for post-hoc subgroup hunting.

## Unit of evidence

The preferred evidence unit is a `plant taxon × interacting partner × population/site × year/season × outcome` contrast or slope for which the overlap/mismatch measure and reproductive outcome refer to the same biological context.

Repeated outcomes or contrasts from the same study, site, population, species pair, or year are not treated as independent by default.

The extraction table will preserve clustering identifiers for:

- publication;
- experiment/data source;
- plant taxon;
- animal taxon;
- interaction pair;
- population/site;
- year/season;
- outcome family.

The primary model will use multilevel meta-analysis or robust variance treatment appropriate to the recovered dependence structure.

## Eligible evidence

A record is eligible for the primary direct-evidence analysis only if all of the following are true:

1. plant reproductive or fitness outcome is measured quantitatively;
2. phenological synchrony, overlap, mismatch, timing difference, or experimentally manipulated timing can be mapped to a declared timing exposure;
3. timing exposure and outcome refer to the same site/population and compatible time period;
4. the focal partner role is biologically identified well enough to assign an interaction class;
5. uncertainty, sample size, raw data, or another defensible route exists to construct an effect size and sampling variance;
6. the biological direction of the timing scale is recoverable so all primary effects can be oriented as `more synchrony`.

Records lacking direct fitness/reproductive outcomes may enter a separate mechanism/context table but not the primary meta-analysis.

## Evidence tiers

### Tier A — direct matched phenology–fitness evidence

Directly measured overlap/mismatch and reproductive outcome in the same system and context. This is the primary evidence tier.

### Tier B — direct phenology with intermediate functional outcome

Examples include pollinia removal, pollen deposition, visitation effectiveness, oviposition or seed attack without final plant reproductive performance. These support mechanism interpretation but do not replace Tier A fitness evidence.

### Tier C — occurrence-derived potential overlap

Flowering and animal activity curves reconstructed from GBIF, iNaturalist, herbarium, museum or other occurrence dates.

Tier C is a **potential-overlap proxy**. It is never pooled as if equivalent to directly observed interaction phenology. It may be used for external extension, candidate-system screening, or sensitivity analysis only after the direct meta-analysis is defined.

## Candidate system universe

The initial literature registry will explicitly search at least these system families:

- `Hadena × Caryophyllaceae`;
- `Epicephala × Phyllanthaceae`;
- `Tegeticula/Parategeticula × Yucca`;
- `Agaonidae × Ficus`;
- `Chiastocheta × Trollius`;
- `Greya × Lithophragma`;
- specialist and generalized pollination systems with replicated phenological mismatch and reproductive outcomes;
- florivore / seed-predator systems with replicated phenological overlap and reproductive outcomes.

These are starting strata, not guaranteed admissions. The search protocol must permit eligible systems outside these clades.

## Effect-size strategy

The project will preserve the native statistical meaning of each extracted result before conversion.

Preferred effect representations, in descending order of interpretability:

1. standardized slope of reproductive outcome on a continuous synchrony measure;
2. Fisher-z transformed correlation between synchrony and reproductive performance;
3. standardized mean difference from an experimental timing manipulation that creates more versus less synchrony;
4. log response ratio where outcome scale and zero handling are valid;
5. other effect forms only if a prospectively documented conversion preserves direction and variance.

All effects are oriented so positive values mean:

> greater phenological synchrony is associated with higher plant reproductive performance.

Therefore a negative effect in antagonist systems directly represents higher reproductive cost with synchrony.

Effect types will not be silently converted using unverifiable assumptions. If heterogeneous effect forms cannot be put on one defensible common scale, analyses will be stratified by effect family rather than forced into one pooled estimate.

## Primary analysis

The primary model tests moderation rather than a universal pooled synchrony effect.

Conceptually:

`effect_size ~ interaction_type`

where `effect_size` is already oriented as the reproductive effect of increased synchrony.

If primary studies provide raw or directly comparable continuous overlap slopes, a complementary individual-record model may be expressed as:

`fitness ~ overlap * interaction_type`

but the meta-analytic estimand remains the distribution of study-level synchrony effects across interaction classes.

Primary contrasts:

- mutualist versus antagonist;
- mutualist versus mixed;
- antagonist versus mixed.

The project will report class-specific pooled estimates and prediction intervals without requiring any class to be significantly different from zero.

## Mixed-system benefit/cost decomposition

For mixed pollinating-seed-predator systems, extract separate channels where available:

- pollination benefit;
- oviposition/larval reproductive cost;
- final net reproductive outcome.

These are not algebraically substituted for one another. A study enters the net-fitness meta-analysis only when a net reproductive outcome is directly observed or can be reconstructed from source data under a declared identity.

The benefit/cost decomposition is a mechanistic sub-analysis and does not import BITA labels or mechanism claims.

## Bias and robustness plan

The implementation will support, at minimum:

- multilevel dependence by publication and biological system;
- leave-one-system and leave-one-clade sensitivity;
- effect-form sensitivity;
- observational versus experimental timing contrast;
- Tier-A-only primary analysis;
- direct-versus-proxy separation;
- influence diagnostics;
- small-study / reporting-bias diagnostics only when the number and structure of studies make them interpretable;
- explicit treatment of missing variance rather than automatic imputation.

No clade, species, study, year, outcome or effect-size form may be removed because it weakens the preferred biological pattern.

## Claim ceiling

A positive primary result may support a statement of the form:

> Across the admitted literature, the reproductive consequence of phenological synchrony differs among interaction types.

A supported mixed-system curvature analysis may additionally support:

> In the admitted mixed pollinating-seed-predator evidence, greater synchrony is not uniformly associated with greater plant reproductive performance.

IWE will not claim from the meta-analysis alone that:

- phenological synchrony causally determines fitness in all systems;
- intermediate synchrony is universally optimal;
- any observed pattern identifies a specific evolutionary architecture;
- modularity, differentiation or architecture change has evolved because of interaction timing;
- `L`, `R`, `K`, `Phi` or any sister-repository theoretical quantity has been measured;
- occurrence-derived overlap equals realized interaction overlap;
- specialist interactions are universally more or less climate-sensitive.

## Repository architecture

Planned structure:

```text
README.md
pyproject.toml
.github/workflows/ci.yml

docs/
  HYPOTHESES.md
  SEARCH_AND_SCREENING_PROTOCOL.md
  EFFECT_SIZE_CONTRACT.md
  CLAIM_CEILING.md
  superpowers/specs/
  superpowers/plans/

data/
  registry/
    systems.csv
    studies.csv
  extraction/
    effect_template.csv
    direct_effects.csv
  derived/

src/iwe/
  schema.py
  overlap.py
  effects.py
  validation.py
  meta.py

scripts/
  validate_registry.py
  validate_extraction.py
  build_meta_dataset.py
  run_primary_meta.py
  run_sensitivity.py

examples/
  synthetic_effects.csv

tests/
  test_schema.py
  test_overlap.py
  test_effects.py
  test_validation.py
  test_meta.py
```

## Data flow

```text
system registry
    -> literature screening
    -> source-level extraction
    -> effect-size validation and orientation
    -> dependence-aware analysis dataset
    -> primary interaction-type meta-analysis
    -> mixed-system curvature / benefit-cost sub-analysis
    -> robustness and claim adjudication
```

Every derived row must retain source identifiers and a deterministic route back to the extracted source record.

## Validation principles

The software layer exists to prevent inferential drift, not to create a new statistical method.

Validation must fail closed on:

- unknown interaction classes;
- missing biological unit identifiers;
- missing effect direction/orientation metadata;
- impossible or inconsistent sample-size fields;
- Tier C proxy rows entering the Tier A primary dataset;
- duplicated primary evidence rows without an explicit dependence identifier;
- unregistered effect-size conversions.

Synthetic examples test software behavior only and never count as biological evidence.

## Success criterion for the first release

The first release is complete when it can:

1. validate a literature/system registry;
2. validate and orient extracted effect sizes;
3. produce a dependence-aware primary meta-analysis dataset;
4. fit and export class-specific and moderator contrasts on synthetic/example data;
5. keep direct evidence and occurrence-derived proxies formally separated;
6. generate a machine-readable claim-status summary showing which hypotheses are evaluable, supported, unsupported or unresolved from the current empirical corpus.

The first release does not require a positive ecological result. A well-powered null, interaction-type equivalence, or unresolved evidence structure is a valid endpoint.
