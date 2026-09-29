# IWE011 timing and exposure-unit re-audit

Date: 2026-09-28  
Study: Kudo & Shibata (2025), *Phenological selection mosaic of predispersal seed predation affects gender variation in an andromonoecious plant*  
DOI: `10.1111/1365-2745.70130`  
Decision: **withdraw former strict-H1 SMD; retain as direct seasonal-timing/final-fitness evidence**

## Why this re-audit was required

IWE's timing contract now explicitly requires a partner window that can order plant timing independently of realized interaction outcomes.

Counts of eggs received by host flowers, attacked fruits, larval occupancy and seed damage cannot be recycled as independent partner availability because they already depend on host availability, host choice and interaction success.

The same rule used to block Cardamine egg receipt and the Bopp *Silene–Hadena* route must also apply to already-admitted effects.

## Partner-window audit

The 2025 paper states that *Phaulernis fulviguttella* lays eggs on terminal-umbel pedicels during the female floral stage, usually in mid- to late July. The field measurements record eggs deposited on host umbels after flowering.

The preceding Kudo & Shibata (2021) study is explicit that the mid- to late-July period came from **preliminary observation of oviposition**. Its repeated field programme measured:

- plant flowering phenology;
- plant traits and flower numbers;
- fruit production;
- mature fruit damage/predation.

It did not report a contemporaneous quantitative census, trapping series or other independent adult-moth abundance/availability curve that can prospectively order HA and HD before interaction outcomes are observed.

A general species flight period from external faunistic sources is not a substitute for a focal-season partner-availability series.

Therefore the former statement that HA and HD were "ordered by the measured moth window" was too strong.

## Exposure-unit interpretation

The former strict effect used:

- HA = one permanent early-flowering plot;
- HD = one permanent late-flowering plot.

Published Table 1 pools plant observations across 2020–2023 and reports final fruit-set summaries:

- HA: mean 0.13, SD 0.19, n=177 plant observations;
- HD: mean 0.40, SD 0.29, n=127 plant observations.

Those plant observations are valid **response sampling within fixed plot contexts**. They quantify uncertainty in the HA and HD response distributions, but they do not make the seasonal timing context itself 177 versus 127 times independently replicated.

Under the clarified strict effect-unit contract, this grain mismatch is not a universal automatic exclusion for a descriptive fixed-context association. It instead requires the effect to be explicitly non-causal and its variance to be interpreted as within-context response sampling.

IWE011 remains withdrawn for the stronger reason above: the partner window itself is not independently measured. If a valid adult-moth activity series were recovered, the fixed-plot response contrast could be reconsidered as a descriptive association with explicit unit provenance rather than being rejected solely because exposure grain and response grain differ.

## What remains scientifically useful

The programme still provides strong direct evidence that:

- local flowering timing varies markedly across nearby snowmelt plots and years;
- final intact-fruit production is measured after seed-predator damage;
- predation is concentrated in earlier seasonal contexts;
- flowering timing is strongly associated with final reproductive loss.

This remains valuable Tier-A/direct seasonal-timing evidence and mechanistic context. It is simply not a strict independently measured partner-synchrony SMD under the current contract.

The diagnostic published contrast remains:

`HA - HD Hedges g = -1.1368391965`

when plant-level summaries are mechanically standardized. This value is retained only in this audit history and must not be returned to `direct_effects.csv` without a redesigned estimand.

## Strict rescue conditions

A future strict Peucedanum effect first requires **independent partner timing** — focal-season adult *P. fulviguttella* abundance/availability measured by census, trapping or another activity series independent of egg receipt/damage.

If the rescued effect remains a fixed HA-versus-HD context comparison, its plant-level variance must be registered explicitly as within-context response sampling and the claim must remain descriptive/non-causal. Multiple plot-years or another genuinely replicated timing exposure would strengthen the design and would be required for a causal/generalized timing-treatment claim, but are not imposed as a universal prerequisite for a descriptive strict association.

The 2017–2019 and 2020–2023 programmes remain one dependence programme, `DEP_PEUCEDANUM_KUDO_PROGRAM`.

## Registry consequence

- `IWE011_HA_VS_HD_FINALSET_SMD` is removed from `data/extraction/direct_effects.csv`.
- `IWE011_HA_HD` becomes `unresolved + pending` with `direct_timing_sensitivity`.
- IWE010 is likewise not described as having an independently measured predator window.
- The antagonist strict-SMD cluster count returns to zero.
