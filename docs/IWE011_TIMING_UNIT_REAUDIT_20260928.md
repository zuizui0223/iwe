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

## Exposure-unit audit

The former strict effect used:

- HA = one permanent early-flowering plot;
- HD = one permanent late-flowering plot.

Published Table 1 pools plant observations across 2020–2023 and reports final fruit-set summaries:

- HA: mean 0.13, SD 0.19, n=177 plant observations;
- HD: mean 0.40, SD 0.29, n=127 plant observations.

Those plant observations are valid response measurements, but the synchrony exposure in the former contrast is assigned at the **plot level**. One HA plot and one HD plot do not become 177 and 127 independent timing exposures.

Consequently the former Hedges-g sampling variance used response-unit replication to stand in for exposure-unit replication. That variance is not a defensible strict meta-analytic sampling variance for a one-plot-versus-one-plot synchrony contrast.

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

A future strict Peucedanum effect requires both:

1. **independent partner timing** — focal-season adult *P. fulviguttella* abundance/availability measured by census, trapping or another activity series independent of egg receipt/damage; and
2. **compatible exposure replication** — timing variation represented at an inferential unit with real replication, for example multiple plot-years prospectively ordered by the independent adult window, or another source-backed individual-level exposure that is not merely inherited from one plot.

A final post-predation response must then be summarized at that same inferential structure.

The 2017–2019 and 2020–2023 programmes remain one dependence programme, `DEP_PEUCEDANUM_KUDO_PROGRAM`.

## Registry consequence

- `IWE011_HA_VS_HD_FINALSET_SMD` is removed from `data/extraction/direct_effects.csv`.
- `IWE011_HA_HD` becomes `unresolved + pending` with `direct_timing_sensitivity`.
- IWE010 is likewise not described as having an independently measured predator window.
- The antagonist strict-SMD cluster count returns to zero.
