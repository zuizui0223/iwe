# Antagonist timing-window and exposure-unit consistency audit

Date: 2026-09-28  
Scope: retrospective application of the frozen IWE timing contract to already-admitted and high-priority antagonist evidence

## Trigger

The Cardamine preflight made two requirements explicit:

1. the partner activity window must be measured independently of realized interaction outcomes such as eggs received by hosts, attack or damage;
2. response sampling and replication of the timing exposure must be distinguished explicitly; nested response observations may quantify a fixed-context mean difference but must not be misdescribed as replicated timing treatments.

This audit applies those same requirements retrospectively to the Peucedanum IWE011 effect and the Tomares–Astragalus candidate.

## Rule 1 — egg receipt is not independent partner availability

A seasonal series of eggs newly deposited on host flowers/shoots is a realized interaction surface:

`adult presence × host availability × host choice × successful oviposition`.

It therefore cannot be reused as an independent adult-availability curve that prospectively defines synchrony.

Acceptable strict partner-window evidence includes focal-season adult census, trapping, visitation or another direct activity series independent of the plant reproductive response.

## Rule 2 — response sampling is not exposure replication

If a synchrony state is assigned at plot/site level, many plants measured inside one plot replicate the **response conditional on that fixed context**; they do not create many independent realizations of the timing treatment.

This distinction changes interpretation rather than automatically invalidating every fixed-context contrast.

A strict descriptive association may retain response-level sampling variance when:

- the partner window itself is independently measured;
- the source response units are defensible biological sampling units;
- the variance is explicitly labeled `within_context_response_sampling`; and
- the claim is explicitly non-causal.

Such an effect estimates a standardized difference between the sampled response distributions in those fixed timing contexts. It does **not** estimate uncertainty from repeated manipulation of the timing exposure.

Experimental/causal timing claims require exposure and response units to align, or otherwise require genuine replication of the exposure.

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

The first point is a strict-gate failure: the partner window is oviposition/egg based rather than independent adult availability.

The second point is an interpretation problem rather than a universal exclusion under the clarified unit contract: the timing exposure is one plot versus one plot while the plant-level variance samples response distributions within those plots. That variance could only support a non-causal fixed-context association, not replicated timing-treatment inference.

### Decision

Withdraw `IWE011_HA_VS_HD_FINALSET_SMD` from the strict corpus.

Retain the programme as direct seasonal-timing/final-fitness evidence. A future rescue first requires independent focal-season adult timing. If the effect remains a fixed HA-versus-HD contrast, it must carry explicit within-context response-sampling semantics and a descriptive/non-causal claim boundary; multiple independently varying plot-years would permit stronger inference.

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
- the published RSI summaries use nested inflorescence observations rather than a clean plant/shoot response variance;
- patch 1 versus patch 2 is a fixed-context contrast and therefore cannot be described as replicated timing treatment even if a correct response variance is recovered.

### Decision

Demote `ANT002_TOMARES_ASTRAGALUS` from P1 `blocked_summary_stats` to P2 `blocked_timing_linkage`.

Strict rescue requires both an independent adult activity series and a final-reproduction variance at a defensible tagged-shoot/plant sampling unit. If the contrast remains patch 1 versus patch 2, it must be retained as descriptive/non-causal fixed-context evidence rather than a replicated timing treatment.

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
4. explicit unit provenance distinguishing exposure grain from response sampling grain;
5. a variance interpretation compatible with that grain, with non-causal labeling for fixed-context comparisons;
6. dependence represented explicitly across repeated sites/years/outcomes.

Cardamine remains the cleanest current route because its female adult flight season is defined from capture/recapture independently of the plant response, and the response-blind exposure rule is already frozen before outcome analysis.
