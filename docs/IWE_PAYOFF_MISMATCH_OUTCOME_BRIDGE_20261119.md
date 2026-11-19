# IWE × PAYOFF: a two-stage mismatch-to-fitness bridge
Date: 2026-11-19
Status: **non-promoting, hypothesis/predictive-design note** on the IWE exploratory pivot. No new biological effect, no strict-H1 class promotion, no modification of either frozen PAYOFF paper.

## Decision

**Connect PAYOFF-B's generation/persistence of interactor phase mismatch to IWE's conversion of timed encounters into final plant reproduction.** Do not merge their incompatible estimands or label IWE seed/fate contrasts as measurements of PAYOFF controller parameters.

- **PAYOFF-B (source of temporal mismatch):** physiological readiness/entry phase, differential effective phase retention, information uptake/actionability, physical recourse, interaction-mediated coordination.
- **IWE (consequence of temporal mismatch):** independently defined adult-service windows, realized oviposition, delayed effective consumer exposure, host developmental filtering, alternative partner accessibility, and final post-cost reproduction.
- **PAYOFF architecture R−K (different, optional question):** selection for changing within-organism coupling/dimensionality. A temporal mismatch between species is **not** the trait-optimum separation or architecture gap in PAYOFF's SCH/BALANCE/BITA transport. No architecture payoff is estimated from IWE.

This is a bridge from **mismatch generation** to **fitness conversion**. Its empirical novelty and identification have not been established. Do not call generic timing-stage memory novel: the separate PAYOFF-B V5 annual-cycle-retention publication line was explicitly stopped for prior-art collision.

## A. Exact reduced mathematical bridge and its assumptions

PAYOFF-B's one-step two-actor phase controller is

    e_(i,t+1) = lambda_i e_(i,t) + w_(i,t).

Define mean incoming phase error m_t=(e_P+e_A)/2 and interactor difference Delta_t=e_P−e_A. Then

    Delta_(t+1) = (lambda_P−lambda_A)m_t
                   + ((lambda_P+lambda_A)/2)Delta_t
                   + (w_P−w_A).

For Delta_t=0 and equal innovations, this reduces to

    Delta_(t+1) = (lambda_P−lambda_A)m_t.

The PAYOFF-B reduced controller writes lambda_i=phi_i(1−G_i O_i g_i K_i). These factors are theoretical mechanisms, NOT separately identified in any same-pair IWE dataset. Species-wide temperature-response slopes (days per degree) are **not** lambda.

IWE's distinct plant-outcome layer can be represented locally as

    E[Y_final | Delta_service, Delta_cost, H, R, X]
      = Y_base(X) + B(Delta_service,H,R,X)
                  − C(Delta_cost,H,R,X),

where Y_final, B and C must be expressed in a **common final-reproduction unit** (e.g., expected viable seeds/plant); they are not interchangeable with visits, eggs, fruit counts or source indices. In particular:

- Delta_service = plant receptive/flowering phase relative to independently observed adult/service activity;
- Delta_cost = susceptible host phase relative to the effective *delayed* consumer phase (oviposition + development, conditional on hatch/parasitism/host state);
- H = plant host stage/susceptibility; R = genuinely time-accessible alternative partners; X = measured resources, temperature, effort and background risk.

For a *local* special case where both phase coordinates are the same Delta and H,R,X are held fixed, the chain rule gives

    d E[Y_final]/d m
      = (lambda_P−lambda_A) [B'(Delta)−C'(Delta)].

This is a mathematical **identity conditional on the model**, NOT an empirical estimate or a universally valid total climate effect. With delayed larvae, changing host stage, direct temperature effects or changed partner assemblages, additional phase derivatives and paths appear. Thus equal mismatch amplitude can have different, even opposite, reproductive effects.

For a weighted network, PAYOFF-B's prospective controller discordance is

    D_lambda = (sum_edges a_ij (lambda_i−lambda_j)^2) / (sum_edges a_ij).

This predicts squared *phase* mismatch under common-mode forcing, not summed final reproductive loss. A fitness-weighted network approximation would require **independently measured** edge-specific conversion curvature and a common local optimum; it is not licensed for antagonistic escape or nonmonotonic mixed interactions without explicit signed final-fitness surfaces.

## B. Source-matched evidence map (not independent replication)

| System / IWE status | What IWE already observes | What PAYOFF-B would additionally require | Joint claim gate |
|---|---|---|---|
| IWE023 Mertensia, independent service window | Four experimentally ordered flowering cohorts, independent visit activity, extracted final seed set; one existing mutualist programme | repeated within-actor timing errors and an independent plant/partner correction or response series | Final timing-to-seed contrast supported; controller generation **not** identified |
| IWE032 Cardamine–Anthocharis | flowering-to-oviposition 11.50 vs 5.72 d (ecotypes), attacked-plant pre-larval dehiscence 34% vs 4%, final fate distribution p=0.003 | numeric independent 2012–2014 female flight timing, then a separately estimated controller/forcing response | stage-to-final escape supported; partner generation **blocked** |
| Parkinsonia–Penthobruchus | seven matched region-seasons in four regions; stage/parasitoid/hatch filtering improves LO-region-out final predation RMSE 20.58 to 4.92 percentage points | independent adult availability and plant/consumer lambda on common seasonal shocks | positive effective-stage/fate prediction; adult controller **absent**, sample small |
| IWE031 Asclepias–monarch | manipulated host age at herbivory, final viable-seed sensitivity | matched natural adult and host timing plus actor correction data | identified *host-stage response*, not controller mismatch |
| IWE015 Silene stellata–Hadena | measured adult windows and post-predation fruit, but tagged-flower linkage and SE/SD interpretation disputed | verified plant/final outcomes and actor-specific phase-response series | **on hold**; no effect-size or controller admission |
| Osmia × 3 plants (2021/2022) | bloom × dated-bee records and sampled-fruit seeds/ovules; held-out timing gains vary by year, validation level, endpoint | independent actor controller/checkpoint series and better final maternal offspring endpoints | falsifier against universal timing superiority; cohorts one programme |
| PAYOFF-B Freimuth 2022 plant–pollinator slope benchmark | matched broad taxon-level temperature response contrasts in an independent publication | same pair/site/year final reproduction, independently estimated retention and host filters | **generation proxy only**; cannot assign IWE final-fitness slope |

Source grain and sign matter:
- IWE eggs/oviposition do **not** become independent adult availability and never enter strict-H1 by relabeling.
- Cardamine ecotypes, annual source cohorts, treatment groups or repeated plants are not independent taxonomic replication units.
- Parkinsonia's improved filtered prediction uses consumer fate (parasitism/hatch) and stage matching, **not** a directly estimated host-specific physiological controller.
- IWE 2021/2022 Osmia cohorts share a research programme; mixed CV results include genuine counterexamples and must stay in the analysis.
- No same interacting plant–animal pair currently provides independently identified lambda_P, lambda_A, Delta, final viable plant reproduction and replicated environmental forcing.

## C. Four distinct prospective predictions

### P1 — common-shock generation
After controlling initial signed phase, local environment and actor-specific innovations, a shared anomaly produces signed between-actor displacement proportional to lambda_P−lambda_A. Measure actor retentions before final seed outcomes. **Null:** matched temperature-sensitivity slopes or calendar date explain changes equally well.

### P2 — directional outcome conversion
Conditional on the same *signed adult* mismatch, host developmental state, larval lag and functional partner access modify final plant seed production. A higher overlap can be beneficial for mutualists, harmful for antagonist exposure, or nonmonotonic for a mixed system. **Null:** a single overlap/calendar predictor predicts independent held-out final outcomes as well as an explicitly staged model.

### P3 — conversion may erase generation
Strong mismatch generation does not guarantee final fitness loss: an effective host filter or compensation can buffer/reverse the outcome; minimal generated mismatch does not guarantee high net fitness if costs peak inside the adult service window. **Falsifier:** independent final-outcome cohorts consistently gain no held-out prediction from true stage/fate information after complexity and sampling effort are controlled.

### P4 — feedback and architecture are not inferred from observational timing alone
A pair's phase-response difference does not prove cue use or physiological feedback. Separating G, O, g and K requires readiness, information and action/opportunity measurements. Inferring PAYOFF's R−K architecture payoff additionally requires a manipulable/heritable architecture choice, objectively costed changes in the same final reproductive currency and an identifiable payoff surface. **Null:** only simple seasonal adjustment is seen; no evidence of evolving architectures or coordination lock.

## D. Executable empirical admission contract

Prioritize **one same-site, same-year, same-interacting-pair longitudinal programme** with:

1. Independently sampled plant flowering/receptivity and adult partner activity, plus a shared forcing anomaly and at least two timing checkpoints per actor (or a clearly identified exogenous differential timing response).
2. Matched realized service/egg deposition and later larval activity/consumer viability, recorded separately from independent adult windows.
3. Matched original host stage, resource/partner redundancy and final realized viable seed/fruit endpoint on defensible plant-level biological units; distinguish per-fruit from per-plant output.
4. Exposure/endpoint variance and dependency identifiers; no fabricated zeros, dispersion labels, year/site replication or causal inference from aggregate paths.
5. Predeclared held-out **whole year/site/programme** prediction: calendar/resources-only; adult-only overlap; stage-filtered exposure; reduced PAYOFF-generation × IWE-conversion model. Fit/tune only on training blocks. Measure the incremental gain for the **same terminal endpoint**, with uncertainty and negative controls.

Primary gate: source-verified, same-population paired generation plus conversion (not two publications juxtaposed), and genuine out-of-sample improvement over calendar, partner abundance and stage-only models. Secondary gate: multiple independent programmes and an honest prediction interval; do not make a universal claim from one site. If no paired data can identify both layers, stop at a **two-lane mechanistic hypothesis with separate validated parts**, not a cross-project causal coefficient.

## E. Priority and paper/branch boundary

**Primary next IWE source unlock:** original 2012–2014 *female* Anthocharis capture/recapture dates for IWE032, with plant/dehiscence unit linkage and error propagation. This would enable the **adult-versus-effective-stage** predictive test, but still not identify PAYOFF lambda_P and lambda_A.

**Strongest existing positive stage filter:** Parkinsonia stage+parasitism+hatch versus original annual egg-density; keep as exploratory source-based prediction with four held-out regions rather than claim a new multi-species confirmation.

**PAYOFF-side natural identification:** needs both actors' phase-response/checkpoint series before drawing a same-pair controller conclusion; Freimuth 2022 taxa temperature slopes are an ecological screening benchmark, not direct lambda estimates.

**Repository ownership:**
- IWE strict-H1 and all protected extraction/registry contracts remain unchanged; no false mixed/antagonist promotion.
- PAYOFF V2/V3/V5 frozen manuscripts and controller algebra remain unchanged; this is **not** a new PAYOFF theorem or reopened stopped annual-cycle-retention paper.
- This note lives only on a new branch of the IWE exploratory pivot; review it as integration design, not confirmatory result.

## Exact repo evidence consulted (2026-11-19)

- IWE pivot: [landscape registry](../data/registry/landscape_components.csv), [phase-alignment gates](../data/registry/phase_alignment_candidates.csv), [temporal signals](../data/registry/temporal_signal_components.csv), [cross-scale falsifiers](CROSS_SCALE_TIME_REFERENCE_SYNTHESIS_20261019.md).
- IWE strict main: https://github.com/zuizui0223/iwe/blob/main/docs/EVIDENCE_AUDIT_STATUS.md .
- PAYOFF controller asymmetry: https://github.com/zuizui0223/payoff/blob/main/theory/CONTROLLER_ASYMMETRY_MISMATCH.md (blob 7f6eacde1fbc519226f239eec85d9041d1fb2a56).
- PAYOFF readiness window: https://github.com/zuizui0223/payoff/blob/main/theory/READINESS_WINDOW_MISMATCH.md (blob c357cf55a95e25e814aaefb31d3be4ff727bff47).
- PAYOFF network discordance: https://github.com/zuizui0223/payoff/blob/main/theory/CONTROLLER_NETWORK_MISMATCH.md (blob 8d96e3fb514d3ebf4df13debc64af01925c27eee).
- PAYOFF frozen V3: https://github.com/zuizui0223/payoff/blob/main/docs/PAYOFF_B_V3_SCIENCE_FREEZE_20261003.md .
- PAYOFF bird/plant-pollinator empirical ceiling: https://github.com/zuizui0223/payoff/blob/main/docs/PAYOFF_B_CROSS_SYSTEM_EMPIRICAL_LANE_20260928.md .
- PAYOFF V5 prior-art STOP: https://github.com/zuizui0223/payoff/blob/main/docs/PAYOFF_B_V5_COLLISION_RESOLUTION_20261005.md .
- PAYOFF architecture meaning: https://github.com/zuizui0223/payoff/blob/main/README.md .
