# IWE013 full-text strict-H1 audit

Date: 2026-09-24  
Source: Ehrlén, Raabova & Dahlgren (2015), *Ecology* 96:2280–2288, DOI `10.1890/14-1860.1`  
Decision: **not eligible for strict H1; remove from the antagonist #2 replication queue**

## Why this audit was needed

The replication-candidate ledger initially treated *Actaea spicata × Eupithecia immundata* as an independent antagonist programme with a measured predator window, final offspring fitness, and only missing SMD summary statistics. Full-text inspection shows that this was too permissive under the frozen timing contract.

## Study design recovered from the full text

- Field data were collected in 2008 from **1118 flowering plants in 15 populations** in Tullgarn, Sweden.
- Plants produce early terminal inflorescences in late May–early June and late basal inflorescences in late June–early July.
- In August, after seed-predator larvae had completed development and left fruits, the study counted intact fruits, attacked fruits, aborted/immature fruits, and seeds per fruit.
- **594/1118 plants (53.1%) produced both early and late flowers.**
- Early/late outcomes were analyzed as repeated measures: the authors explicitly used **mother-plant identity as a random grouping variable**.
- A common-garden offspring experiment and demographic IPM were used to quantify differences in offspring quality and reproductive value.

These facts make the study biologically informative and give it a direct post-predation reproductive surface.

## Timing gate: fails the strict-window contract

The paper states that *E. immundata* oviposition occurs from mid- to late June and that late infructescences often escape predation. However, that timing statement is cited to **Eriksson (1995)** and **von Zeipel et al. (2006)**. The 2008 focal study did not contemporaneously measure adult predator availability/activity.

The frozen IWE timing contract requires `seasonal_position` contrasts to be ordered by a **contemporaneously measured partner window**. This is the same fail-closed rule used for IWE027, where 2006 seed-set summaries are not promoted using the partner activity measured in 2007.

Therefore:

| replication gate | IWE013 |
|---|---|
| independent programme from IWE011 | yes |
| contemporaneously measured predator window | **no** |
| post-predation final reproduction | yes |
| SMD-ready summary statistics | **no** |
| strict replication status | **rejected_timing** |

Predation itself cannot be used as the missing activity measurement because that would infer synchrony from the response/mediator being tested.

## SMD gate: also not currently recoverable

The published early/late comparisons are not two independent groups. They are repeated observations within mother plants, and the paper's own models account for that dependence.

The paper reports useful marginal quantities (for example, early/late seed number per intact fruit and early/late seedling size), but the strict post-predation reproductive contrast is not published as an independent-group mean + SD/SE + n, nor as a paired difference with its variance/correlation.

IWE must therefore **not**:

- use fruit counts as if fruits were independent plants;
- compute an ordinary two-independent-groups Hedges g from repeated early/late observations;
- impute a within-plant correlation;
- treat the model-derived reproductive value ratio as an SMD.

Recovering individual-level data could solve the repeated-measures variance problem for a timing-sensitivity analysis, but it would **not** solve the missing contemporaneous partner-window gate for strict H1.

## Search consequence

Antagonist #2 remains genuinely open. Search should move away from IWE013 and prioritize studies that jointly contain:

1. a measured antagonist activity/availability window in the focal season,
2. plant timing that can be prospectively ordered as higher versus lower overlap,
3. final realized plant reproduction after antagonist damage, and
4. variance-bearing summaries or raw data compatible with the frozen SMD family.

A literature lead worth full-text adjudication is Evans, Smith & Gendron (1989), *Oecologia* 78:220–230, DOI `10.1007/BF00377159` (*Baptisia australis* with seasonally shifting flower/seed consumers). Its abstract explicitly reports three years of seasonal insect damage, late arrival of blister beetles, and consequences for seed production, but it is **not promoted** until the full text demonstrates a focal independently measured partner window and SMD-ready final reproduction.
