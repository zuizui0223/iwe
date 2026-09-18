# IWE079 extraction receipt — Astragalus lusitanicus × Tomares ballus

Source: Jordano D, Fernández Haeger J, Rodríguez J. 1990. *The effect of seed predation by Tomares ballus (Lepidoptera: Lycaenidae) on Astragalus lusitanicus (Fabaceae): determinants of differences among patches*. Oikos 57:250–256. DOI `10.2307/3565947`.

Status: **context_only — direct synchrony mechanism plus final-fitness evidence, but no estimable strict H1 synchrony effect**.

Interaction class: `antagonist`.

Dependence ID: `DEP_IWE079_ASTRAGALUS_TOMARES`.

## Full-text recovery

An author-uploaded seven-page copy of the published Oikos article was recovered and inspected on 2026-09-19.

The source is formally published and satisfies `docs/SOURCE_ELIGIBILITY.md`. The reason it does not enter primary H1 is quantitative identification, not source status.

## What the study actually measured

The field study followed six patches of `Astragalus lusitanicus` in 1986.

For marked shoots, investigators:

- tagged successive inflorescences and recorded their initial flower-bud counts;
- classified inflorescence developmental age;
- examined shoots weekly;
- counted newly laid `Tomares ballus` eggs, which could be distinguished from previously counted eggs;
- recorded ripe fruits and viable/aborted seeds at the end of the season.

The source-defined reproductive success index was:

`RSI = ripe fruits / initial flower buds`.

Thus the study genuinely contains both a time-resolved antagonist interaction window and a final plant reproductive endpoint.

## Why it still does not close strict H1

The source states that the detailed temporal-coincidence analysis between `T. ballus` egg laying and `A. lusitanicus` flowering phenology could be performed for **patches 1 and 2 only**, because egg counts were too sparse in the remaining patches.

The two focal patches had similar average egg load per shoot but differed in temporal matching:

- patch 1: clear synchrony between egg laying and availability of immature inflorescences;
- patch 2: egg laying was noticeably delayed relative to the immature-inflorescence window.

The corresponding source estimates of predator-associated RSI reduction were:

- patch 1: **76.5%**;
- patch 2: **26.7%**.

The paper therefore gives unusually direct evidence that timing can modify the realized reproductive cost of an antagonist even when average egg load is similar.

However, only two patch-level synchrony units are available. The source does not report a continuous synchrony index with sampling uncertainty across a sufficient number of independent patches. Consequently IWE cannot estimate a study-level synchrony–fitness slope/correlation with a defensible sampling variance.

The contrast cannot be promoted by treating the many plants, inflorescences, eggs or seeds inside the two patches as independent synchrony replicates because the timing exposure is defined at patch level.

## Source quantitative anchors

### Patch-level egg load and overall RSI

The published Table 1 reports mean egg load and RSI by patch. Examples include:

- patch 1: egg load `9.11 ± 0.14`; RSI `6.65 ± 0.76%`;
- patch 2: egg load `8.92 ± 0.21`; RSI `12.98 ± 1.82%`.

These quantities are useful for checking that patches 1 and 2 have similar egg loads but different overall reproduction. They do not themselves constitute a synchrony effect.

### Attacked versus control shoots

For patches 1–5 the experiment compared attacked and egg-removal control shoots. Table 2 reports, among other results:

- patch 1: attacked RSI `0.04` versus control `0.17`; predator effect `76.5%`;
- patch 2: attacked RSI `0.11` versus control `0.15`; predator effect `26.7%`;
- patch 5: attacked RSI `0.15` versus control `0.19`; predator effect `21.1%`.

These quantify the final reproductive cost of attack. They must not be re-labelled as synchrony coefficients.

## Why no Fisher-z row is constructed

A strict Fisher-z reconstruction would require several independent biological units with both:

1. a quantified partner-matching exposure; and
2. final plant reproduction.

Here, the detailed synchrony comparison is effectively `n = 2` patches. That is insufficient for a finite Fisher-z sampling variance `1/(n-3)`, and no alternative source regression coefficient for synchrony -> final fecundity is reported.

IWE therefore does not:

- infer a correlation from two patches;
- digitize Fig. 5 into pseudo-replicates;
- use egg-load correlations as a substitute for timing;
- use attacked/control plant sample sizes as if they were synchrony replication;
- convert the reported 76.5% versus 26.7% contrast into an unregistered effect family.

## Biological interpretation retained

IWE079 is strong evidence for the mechanism:

> the reproductive cost imposed by a seed predator can depend on temporal coincidence between its oviposition window and the host plant's susceptible reproductive stage, not only on average enemy load.

That is directly relevant to the evidence-architecture result: antagonist timing can be biologically decisive while remaining difficult to represent as one comparable study-level monotone synchrony effect.

## Claim ceiling

IWE079 supports direct antagonist timing context and final-fitness interpretation.

It does **not** contribute an independent programme to the primary H1 meta-analysis or the Fisher-z common-scale gate.
