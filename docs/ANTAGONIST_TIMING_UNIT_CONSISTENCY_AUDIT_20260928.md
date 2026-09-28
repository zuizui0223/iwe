# Antagonist timing-window and exposure-unit consistency audit

Date: 2026-09-28  
Scope: retrospective application of the frozen IWE timing contract to already-admitted and high-priority antagonist evidence

## Trigger

The Cardamine preflight made two requirements explicit:

1. the partner activity window must be measured independently of realized interaction outcomes such as eggs received by hosts, attack or damage;
2. the sampling variance of an SMD must reflect independent units of the timing exposure, not merely repeated response observations nested inside one exposed site/plot.

This audit applies those same requirements retrospectively to the Peucedanum IWE011 effect and the Tomares–Astragalus candidate.

## Rule 1 — egg receipt is not independent partner availability

A seasonal series of eggs newly deposited on host flowers/shoots is a realized interaction surface:

`adult presence × host availability × host choice × successful oviposition`.

It therefore cannot be reused as an independent adult-availability curve that prospectively defines synchrony.

Acceptable strict partner-window evidence includes focal-season adult census, trapping, visitation or another direct activity series independent of the plant reproductive response.

## Rule 2 — response replication is not exposure replication

If a synchrony state is assigned at plot/site level, many plants measured inside one plot replicate the response conditional on that plot; they do not create many independent realizations of the timing exposure.

An independent-groups SMD cannot therefore use plant/inflorescence n as though one high-overlap plot and one low-overlap plot were replicated treatment groups.

A strict meta-analytic variance needs either:

- multiple independently exposed units such as prospectively ordered plot-years/sites; or
- an individual-level timing exposure that genuinely varies among independent response units.

## IWE011 — Peucedanum × Phaulernis

### Source evidence

Kudo & Shibata (2025), DOI `10.1111/1365-2745.70130`, measures final intact-fruit production across five permanent flowering plots.

The paper states that *Phaulernis fulviguttella* oviposits on host umbels, usually in mid- to late July, and field measurements count eggs deposited on umbels.

Kudo & Shibata (2021), DOI `10.1002/ece3.7468`, describes the same seasonal window as a preliminary observation of the major oviposition period. Its quantitative programme measures flowering phenology, fruit production and mature fruit predation, not an independent adult-moth abundance time series.

### Former strict contrast

The former effect compared:

- HA, one mid-July permanent plot; and
- HD, one August permanent plot.

Plant-level Table 1 summaries were standardized with `n=177` and `n=127`.

This fails both retrospective rules:

- the partner window is oviposition/egg based rather than independent adult availability;
- the timing exposure is one plot versus one plot while the variance uses nested plant response n.

### Decision

Withdraw `IWE011_HA_VS_HD_FINALSET_SMD` from the strict corpus.

Retain the programme as direct seasonal-timing/final-fitness evidence. A future rescue requires independent focal-season adult timing and a replicated timing exposure at a compatible inferential unit.

## Tomares × Astragalus

### Source evidence

Jordano, Fernández Haeger & Rodríguez (1990), Oikos DOI `10.2307/3565947`, followed one tagged shoot per plant weekly in six Sierra Morena patches.

The weekly interaction series records immature-inflorescence availability and **newly laid T. ballus eggs**. Tagged shoots were later scored for ripe fruits and viable/aborted seeds.

The published temporal-coincidence comparison uses only patches 1 and 2.

The companion life-history paper, DOI `10.5962/p.266691`, establishes a broad regional adult flight season from late January to late April with a mid-March peak and strong host phenological coupling. The current public audit has not recovered a quantitative focal-season adult activity series that independently orders patch 1 versus patch 2.

### Previous blocker was incomplete

The prior IWE candidate classification treated the problem as only a nested-variance issue because Table 1 reports RSI on many inflorescences.

That is insufficient:

- egg receipt cannot serve as the independent partner window;
- patch 1 versus patch 2 is one patch per synchrony state;
- obtaining shoot-level SD does not create replication of the patch-level timing exposure.

### Decision

Demote `ANT002_TOMARES_ASTRAGALUS` from P1 `blocked_summary_stats` to P2 `blocked_timing_linkage`.

Strict rescue requires both an independent adult activity series and a timing-to-final-reproduction surface with compatible exposure replication.

## Corpus consequence

After this audit:

- mutualist strict rows remain unchanged;
- antagonist strict rows = **0**;
- mixed strict rows = **0** while IWE015 remains on variance hold;
- the apparent cross-class SMD coverage is therefore removed rather than preserved through inconsistent rules.

This is a reduction in apparent evidence quantity but an increase in contract consistency.

## Forward promotion rule

No antagonist candidate may be promoted merely because:

- a plant timing gradient is clear;
- attack/egg timing is seasonal;
- final reproduction is measured; and
- many plants/flowers are observed.

Promotion requires all of the following jointly:

1. independent partner-activity timing;
2. a prospectively defined synchrony exposure;
3. final post-interaction plant reproduction;
4. variance at units that replicate the exposure;
5. dependence represented explicitly across repeated sites/years/outcomes.

Cardamine remains the cleanest current route because its female adult flight season is defined from capture/recapture independently of the plant response, and the response-blind exposure rule is already frozen before outcome analysis.
