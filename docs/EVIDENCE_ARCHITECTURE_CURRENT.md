# IWE evidence architecture — current corpus

Date: 2026-09-19  
Status: **current-corpus diagnostic; systematic search not yet closed**

This document summarizes the present evidence architecture for IWE. It is not a final systematic-review prevalence estimate.

The machine-readable source is produced by:

```bash
python scripts/build_evidence_architecture.py
```

The current primary common-scale gate remains defined separately in `docs/COMMON_SCALE_FEASIBILITY_GATE.md`.

## Current class architecture

| Interaction class | Screened | Strict admitted records | Quantitative strict programmes closed | Common-scale Fisher-z programmes | Unresolved possible strict | Shape lane | Context only |
|---|---:|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 4 | 2 | 1 | 5 | 0 | 8 |
| antagonist | 31 | 1 | 1 | 1 | 7 | 3 | 20 |
| mixed pollinating seed predator | 29 | 1 | 1 | 1 | 2 | 1 | 25 |

Current-corpus quantitative closure fractions are:

- mutualist: `2 / 17 = 11.8%`;
- antagonist: `1 / 31 = 3.2%`;
- mixed pollinating seed predator: `1 / 29 = 3.4%`.

These fractions describe the current screened corpus only. They must not be interpreted as the biological frequency with which synchrony matters in nature.

## What the asymmetry means

The main empirical bottleneck is not simply a shortage of papers about phenology.

### Mutualists

Mutualist studies comparatively often place all three required pieces in one programme:

```text
plant timing
+ partner timing / availability
+ final plant reproduction
```

Even here, many records fail the strict estimand because flowering date is measured without an independently defined partner-activity window, or because timing manipulations also alter frost, water or other mechanisms.

Two independent mutualist programmes are currently quantitatively closed, but only one is presently on the Fisher-z common scale.

### Antagonists

Antagonist studies are abundant in the screened corpus, but most do not yield a monotone strict H1 effect.

Three recurrent designs dominate:

1. flowering date predicts attack or seed predation, but the animal activity curve is not independently measured;
2. animal timing is measured, but the endpoint is attack/oviposition rather than final plant reproduction;
3. timing-to-fitness is explicitly nonlinear or bidirectional, producing temporal escape windows rather than one monotone synchrony slope.

The third category is biologically important rather than a data-quality failure. IWE032–IWE034 are retained in a separate shape lane because forcing them into one signed H1 coefficient would erase the reported biology.

IWE068 is currently the only published antagonist programme quantitatively closed on the strict Fisher-z scale. IWE079 provides unusually direct evidence that a high-synchrony patch experienced a much larger reproductive cost than a similarly egg-loaded but temporally delayed patch, but only two patch-level synchrony units were available, so it remains context rather than a meta-analytic row. IWE078 demonstrates that another strict reconstruction is technically possible from public raw data, but it remains provisional and outside the primary programme count under `docs/SOURCE_ELIGIBILITY.md` because the corresponding research article has not yet been verified as formally published.

### Mixed pollinating seed predators

The mixed literature has a different measurement split.

Many nursery-pollination papers measure one or more of:

- partner tracking / phenology;
- pollination benefit;
- oviposition or larval cost;
- final seed production.

But these components are often not measured together on the same reproductive unit.

This is especially clear in dioecious figs, where seed production occurs in female figs while pollinator offspring and nursery costs occur in male figs. Those studies can identify a pollination-benefit channel but cannot be treated as a same-unit net mixed fitness effect.

Monoecious fig experiments are unusually valuable because seeds and pollinator offspring develop in the same syconium. IWE064 therefore closes a strict mixed H1 programme, while IWE066 supplies preregistered H2 shape evidence with an interior seed-production peak.

## Consequence for H1

The current Fisher-z common-scale programme counts remain:

- mutualist: 1;
- antagonist: 1;
- mixed: 1.

Therefore the cross-class primary H1 model remains `coverage_only`.

The current evidence does **not** license a class ranking or a claim that synchrony effects differ among interaction types.

The next useful evidence is independent replication on a compatible effect scale, not additional rows from already represented programmes.

## Evidence-architecture endpoint

If systematic search closure retains this strong asymmetry, it is itself a valid empirical result:

> the literature measures plant–partner timing and final plant reproduction with systematically different completeness across interaction roles, and antagonist/mixed systems are especially likely to be represented by attack-only, channel-only or nonlinear timing evidence rather than one comparable monotone synchrony-to-fitness effect.

That statement should be evaluated from the final closed search, not from the current fractions alone.

## Immediate priorities

1. close published independent strict programmes rather than add more effects from existing dependence clusters;
2. prioritize recoverable raw/data-linked antagonist and mixed systems;
3. keep nonlinear antagonist evidence in the shape lane rather than forcing it into H1;
4. keep provisional dataset-only effects outside the primary source gate;
5. complete the frozen backward/query/forward/citation search before interpreting class-level screening proportions as final.
