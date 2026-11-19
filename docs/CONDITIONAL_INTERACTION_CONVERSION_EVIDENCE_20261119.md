# IWE — conditional conversion of interaction timing into plant reproduction
**Evidence-to-test audit, 2026-11-19.** Status: non-promoting integration memo; not a new meta-analysis or new biological replication.

This document connects the frozen strict-IWE corpus on main with the exploratory temporal-propagation pivot. It does **not** merge the pivot into main, alter any H1 admission decisions, or promote ALAN/chocho outcomes to strict synchrony effects.

## 1. Exact scientific claim

**Proposed testable hypothesis:** a measured plant–animal timing signal affects final reproductive performance conditional on the biological gate converting encounter into effective service, future damage, or viable offspring. Its direction and predictive value need not be invariant across the stages of an interaction.

This is stronger and more falsifiable than a single pooled signed synchrony coefficient, but it is currently a **hypothesis**, not a proven universal law. Distinguish three propositions:

1. **Encounter:** spatial and seasonal opportunity allows two organisms to meet.
2. **Conversion:** encounters become effective pollination, surviving consumers, retained fruit, or seed maturation; host ontogeny and resource limitation can change the conversion.
3. **Final outcome:** observed mature seeds, final yield or a separately declared post-cost endpoint; never silently replace these by visitation, eggs, potential fruit, model-predicted seed or seed-damage fraction.

A system can show a large change at 1 with little measurable change at 3. A source that observes only 1 and 3 does not by itself identify the step-2 mechanism.

## 2. Source-checked evidence map (different estimands, not poolable)

| Evidence family | Source-backed estimate | Independent unit and claim ceiling |
|---|---|---|
| Strict seasonal mutualist synchrony | 4 strict effects from 3 studies / 3 dependence clusters; common SMD family has 3 rows from **2** clusters. All 4 directions are positive | No valid class contrast: SMD clusters mutualist 2 / antagonist 0 / mixed 0; current conservative CR2 inferential gate requires >=5 clusters **per class** |
| Marginal nighttime reproductive access | Original-tree adjusted fruit index **+0.28367 [0.18220, 0.38514]** (61 publication IDs); seed index **+0.22173 [0.13570, 0.30776]** (54 IDs) | Existing Kendall & Nicholson 2025 studies reanalysed; normalized (open-day-only)/(open+day-only) indices, **not** ALAN effects, percentage losses, or evidence that night dominates day |
| Direct day-versus-night reproductive difference | Original-tree fruit index **+0.13757 [0.02301, 0.25213]**; original-tree seed index **+0.07168 [-0.15522, 0.29859]** | Same underlying literature as previous row; only fruit is resolved under this dependence structure. Do not count as independent replication of night-access effect |
| Temporal propagation pilot | **33** registered links, **27** dependence clusters; 30 labeled final links (24 clusters), but only **18** directly observed mature-seed/yield links (14 clusters) | Link categories are stage descriptions, not effect-size units. Final fates, derived indices, source-model predictions and seed predation must remain separate |
| Within-programme timing-provenance support | **0** independent programmes in the directly measured mature-seed/yield panel have both prospective timing and realized/seasonal timing references for a same-programme comparison | The prospective-versus-realized retention fractions are unpaired and confounded by system, design and endpoint; do not fit a causal depth moderator |
| Paired stage-comparator gate | **0/14** phase-alignment candidates are confirmatory-ready; 2 near-confirmatory but blocked; 1 retrospective paired realized positive and 1 adult–host positive lacking effective-stage measurement | Positive biological stage effects are not the same as demonstrated out-of-programme predictive superiority |
| ALAN cross-stage exposure | Grognuz & Knop 2026 preprint reported comparable illuminated/dark daytime choice rounds after three prior illumination nights: equal-round lit/dark seed ratios about **0.715** in each of Trifolium and Centaurea | Original published treatment means are reused rather than independent raw-potted-plant refits; 28 choice rounds are not 28 independently assigned light treatments. Does not prove nocturnal-moth mediation or any strict-IWE timing effect |
| Host-resource geography (chocho) | Fixed 239-butterfly host portfolio: introduced hosts expand potential regional larval-resource coverage by **54.9%**; Anthocharis all-host region union **162 -> 272** | Potential regional resource access is not a dated encounter, larval establishment or plant fitness effect; no spatial-to-temporal causal join is available |

Sources: [main strict audit](https://github.com/zuizui0223/iwe/blob/main/docs/EVIDENCE_AUDIT_STATUS.md); [original-tree nighttime marginal PR #127](https://github.com/zuizui0223/iwe/pull/127); [direct diel PR #126](https://github.com/zuizui0223/iwe/pull/126); [pivot propagation audit](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/TEMPORAL_SIGNAL_PROPAGATION_AUDIT.md); [endpoint sensitivity](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/PROPAGATION_ENDPOINT_STRICT_SENSITIVITY.md); [within-programme support](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/PROPAGATION_REFERENCE_SUPPORT_AUDIT.md); [phase gate](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/PHASE_ALIGNMENT_CONFIRMATORY_GATE.md); [daytime ALAN carryover PR #129](https://github.com/zuizui0223/iwe/pull/129); [chocho main](https://github.com/zuizui0223/chocho/blob/main/README.md).

**Accounting rules:** the strict H1 row count (4) is not the propagation-link count (33); 30 final-link labels are not 30 independently observed seed-production experiments; 18 links are not 18 independent clusters (there are 14). Different derived indices from one Kendall source are not independent literature or causal replications.

## 3. Hard counterexample: conversion versus phase matching

In the source-derived **7 region-season observations / 4 regions** for Parkinsonia–Penthobruchus, retrospective leave-one-region-out single-predictor regressions produce these source-reported RMSE values (percentage points of seed predation):

| Predictor | RMSE, pp |
|---|---:|
| Annual egg density | 20.58 |
| Host-stage-matched egg density | 19.93 |
| Host-stage-matched eggs × nonparasitized fraction × hatch fraction | 4.92 |
| **Nonparasitized fraction × hatch fraction, without stage or density** | **4.11** |

Thus phase matching *alone* improves only 20.58 -> 19.93, whereas survival eligibility explains most of the descriptive gain. The survival-only candidate even outperforms stage × survival in pooled RMSE (but in only 2/4 held-out regions). This defeats an automatic claim that stage matching was the source of the large apparent improvement.

The biological survival variables and seed fate were dissected from the **same late-collected samples**. Regressions are post-outcome exploratory and the 10-model ablation was selected after inspecting outcomes; region folds do not repair contemporaneous measurement or model-selection leakage. No predictive forecast, early-warning ability, formal comparative p-value or causal mediation is inferred.

Source: [Parkinsonia original-data ablation](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/LANDSCAPE_PARKINSONIA_CONVERSION_ABLATION.md).

The 2021 and 2022 three-plant–Osmia cohorts supply an independent boundary: exact-date bee overlap does not uniformly improve seed and F1 prediction above simple calendar/mean-bee baselines under held-out arenas, and the two cohorts are not two independent taxonomic programmes. A temporal coordinate can be biologically meaningful without preserving added prediction for every endpoint.

## 4. Primary falsifiable analysis specification

**Unit:** same marked plant or compatible tagged fruit-to-final-fate chain, within the same original experimental source; independent study/programme is the synthesis unit. Never treat repeated visits, multiple flowers, species within the same lab programme, or pseudo-repeated offspring groups as independent programmes.

**Before inspecting the new outcome**, freeze exposure definitions, a measured predictor-availability time, analysis inclusion rules, baseline models, unit-level matching and outer resampling blocks (years/sites/rooms as appropriate). Candidate endpoints must be analyzed separately: mature seed number, viability, fruit fate and seed-damage fraction are not interchangeable.

A minimum nested, same-row comparison is:

- M0: calendar/season + measured plant size/flower supply + design context.
- M1: M0 + independently observed partner activity during the plant's receptive period (not eggs/attack as an adult proxy).
- M2: M1 + independent susceptible host-state or later damaging-stage alignment.
- M3: M2 + pre-outcome measured survival/functional conversion filter.
- Critical ablations: M0 + host state **without** partner overlap; M0 + conversion filter **without** alignment. They distinguish stage matching from predictive information closer to the endpoint.
- For mixed nursery-pollination systems, benefit and offspring-cost channels must be timestamped and evaluated separately **before** a net post-cost outcome; not subtract incompatible observed units.

**Primary estimand:** within the same held-out units, the difference in loss (for example RMSE or negative log predictive density) between an explicitly pre-specified simpler comparator and stage-aligned predictor. Positive improvement is defined in advance as loss(simple) minus loss(stage). Report each held-out group, independent-programme contrast and a class-appropriate uncertainty analysis; do not select whichever comparator wins after looking at outcome. A model including the conversion filter must additionally outperform the **conversion-only** ablation to earn incremental phase credit.

**Validation/stop rules:** require at least two genuinely independent held-out groups for an exploratory comparison and meaningful larger independent coverage for inference; block an explicit future time/site transfer where feasible. If any predictor is measured at or after the endpoint, or any upstream/end-stage observations are from mismatched plants, stop the prospective claim and label as descriptive. If random assignment is at room/site/lamp level, do not use the number of individual flowers or observations as treatment replicates. Do not label a between-study index difference as a within-study moderator. Use pre-declared dependence clusters in resampling and evidence synthesis.

Potential confirmatory interpretation requires source-backed final plant outcome, paired comparator, temporal independence of predictors, identifiable stage/filter coordinate and transport beyond the training programme. A significant source-specific association by itself does **not** satisfy this gate.

## 5. Locked source completion routes (not new H1 effects)

**Cardamine–Anthocharis (IWE032).** Existing 2012–2014 Dryad plant transects and final dehiscence records can support the plant side; the 2024 paper explicitly states that female flight comes from dates of **capture and recapture**, not from eggs. The missing source object is numeric female capture/recapture event dates, or source-certified 2012–2014 q10/q90 boundaries on the **same calendar scale**. Do not digitize a panel relative to first flowering and call the numbers absolute day-of-year. The earlier 2005–2010 MRR series in the 2016 thesis is not the contemporary 2012–2014 female-flight source. After retrieval, run the existing response-blind preflight and keep early-vs-core and late-vs-core escape separate.

- [Original 2024 article, Methods §2.3](https://doi.org/10.1002/ece3.11330)
- [Original 2012–2014 plant Dryad record](https://doi.org/10.5061/dryad.v9s4mw741)
- [Cardamine phase gate](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/PHASE_ALIGNMENT_CONFIRMATORY_GATE.md)

**Hurlburt 2004 Yucca–Tegeticula.** The original doctoral thesis is publicly catalogued and adult monitoring, flowering and mature-fruit dissections are documented, but marked flowering cohorts have not been source-joined to the **same** final mature-fruit and viable-seed rows. It remains a near-confirmatory **blocked** programme, not a quantitative mixed-system replication.

## 6. Decisions frozen at this checkpoint

1. **Keep the current strict three-class H1 unchanged**: insufficient antagonist and mixed class clusters for inferential comparison.
2. **Keep marginal night-access and direct diel dominance distinct**: these indices measure different contrasts in overlapping published experiments; neither is a causal light effect.
3. **Retain the conditional-conversion hypothesis as testable, not established**. Preserve successes, sign reversals and null/erasure cases under original dependence IDs.
4. **Do not use observational survival/egg-stage variables measured with the final fate as prospective predictors**. Parkinsonia shows why a conversion-only ablation is essential.
5. **Focus retrieval on one missing source object per near-confirmatory programme**, beginning with 2012–2014 Cardamine female timing. Until the same-unit comparison is estimable, no cross-system causal-depth meta coefficient is warranted.

Provenance checkpoint: main commit 3dcb8419dbc7752a2aa45bd6172309440579ba83; pivot PR #62 head 7b7fa72c14b045ccae93aab274613a90429119ed (last updated 2026-10-26). At audit time main and pivot had diverged (pivot ahead 569 / behind 19 relative to main). This memo lives on a separate main-based review branch intentionally, without merging either lineage.