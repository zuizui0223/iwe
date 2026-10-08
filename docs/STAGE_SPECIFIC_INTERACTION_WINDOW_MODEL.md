# Stage-specific interaction-window model

Date: 2026-10-02  
Status: empirical bookkeeping model motivated by the pivot; not a new fitted theory and not part of strict H1.

## Core idea

A single animal species can expose a plant to more than one biologically distinct temporal window.

For a pollinating seed predator:

1. the **adult service window** determines access to pollination benefit;
2. the **offspring cost window** occurs later, after oviposition and consumer development;
3. host reproductive tissues can change vulnerability between those two stages.

Therefore "synchrony with the partner" is not a unique state variable.

The relevant question is:

> Which interaction stage is synchronized with which plant stage?

## Bookkeeping formulation

Let a plant's receptive/reproductive schedule for phenotype or individual i be P_i(t).

Let A(t) be focal adult service activity.

A conceptual benefit surface is:

B_i = integral P_i(t) A(t) dt.

For a mixed interaction, let O(t) denote oviposition/exposure, K(l) the distribution of delays from exposure to damaging consumer activity, S_i(s,l) the probability that an exposure survives non-host conversion filters to become a damaging consumer (for example egg hatch or parasitoid escape), and H_i(t | history) the host retention/vulnerability state at the later time.

The explicit dependence on interaction history matters because the host filter can itself be altered by the interaction. Rheum-Bradysia provides the motivating case: oviposition changes IAA dynamics and lowers fruit abortion before larvae hatch.

Let Q_i(s) describe consumer targeting of reproductive units at exposure time. This is needed because consumers can preferentially select units likely to survive a later host filter, as in Lathyrus-Bruchus.

A conceptual offspring-mediated cost is:

C_i = integral P_i(s) O(s) Q_i(s) [ integral K(l) S_i(s,l) H_i(s+l | history) dl ] ds.

The net reproductive consequence is some source-appropriate function:

W_i = g(B_i, C_i, other ecological pathways).

IWE does **not** assume that B and C are measured on the same scale or can always be numerically subtracted. The equations specify which temporal objects must be distinguished.

For systems with alternative mutualists, define time-indexed accessible redundancy conceptually as:

R_eff(t) = sum_j I(partner_j active at t AND able to access receptive flowers at t).

R_eff modifies the service side; it is not equivalent to partner richness.

## Empirical predictions

### P1 — adult synchrony and cost synchrony can diverge

High overlap with an adult service/oviposition window need not imply high overlap with the later damaging stage.

Kula 2012 gives the direct mixed-system example: flowering x oviposition synchrony predicts more predation in 2008 but less predation in 2009.

### P2 — developmental phase lag can reverse effect sign

Let D be the time from exposure/oviposition to damaging consumer activity and H the time required for the host tissue to mature or harden beyond vulnerable stages.

When D is short relative to H, high exposure synchrony should increase cost.

When D is long relative to H, synchronized reproductive units can mature before consumers become damaging, so high adult/oviposition synchrony can reduce later cost.

In the Kula programme:

- 2008 flower/egg to first larva = 10/5 d; fruit maturation = 21.3 d;
- 2009 flower/egg to first larva = 17/15 d; fruit maturation = 16.7 d.

A response-independent **margin to first detected mobile larva** can be calculated descriptively:

`M_detect = (first flower -> first observed mobile larva) - mean fruit collection interval`.

Point estimates are **-11.3 d** (2008) and **+0.3 d** (2009), but the 2009 maturation-only ±2SE sensitivity interval is **-0.50 to +1.10 d** and already spans zero.

Crucially, the original study visited plants every **2–4 days** and usually first detected larvae only after they were moving between flowers, at approximately **10–15 mm**. First detection is not the onset of larval feeding, and the reported maturation interval is estimated from fruit collection dates rather than direct tissue hardening. Thus **no positive host-safety threshold has been demonstrated**.

The year-to-year difference in developmental lead remains consistent with the opposite predation slopes. The margin is not a validated two-year phase-threshold law or a final-fitness predictor.

### P3 — climate can alter interaction outcome without changing adult overlap

Temperature or moisture can change:

- consumer developmental rate K;
- host maturation/vulnerability V;
- adult activity A;
- plant flowering P.

Therefore two years with similar qualitative adult-partner overlap can have different effective cost surfaces if D or H changes.

This is the mixed-interaction extension of the established "developmental race" between herbivore larvae and maturing host plants.

### P4 — effective cost windows are stage-specific

Cardamine-Anthocharis provides an independent antagonist example.

The total-egg peak occurs at flowering-date z = -1.10, whereas the subset of active eggs capable of generating damaging later larvae peaks at z = -0.61 with a narrower distribution.

Raw exposure and effective future cost therefore occupy different windows.

### P5 — redundancy only buffers within its own access window

Senita cactus shows that alternative pollinators can be present in the community yet contribute zero effective redundancy if they cannot access flowers at the relevant time.

Thus mismatch buffering should be modeled against R_eff(t), not species richness.

### P6 — host filtering is endogenous to the interaction

A developmental filter is not necessarily a fixed plant property.

Two opposite feedbacks are already present in the corpus:

- *Lathyrus–Bruchus*: the seed predator uses phenology/position and other cues to target fruits with lower future abortion probability, partly bypassing the host filter;
- *Rheum–Bradysia*: oviposition strongly reduces fruit abortion and changes IAA dynamics before larvae hatch, consistent with partner-induced modification of the host filter.

Therefore host retention/vulnerability should be represented as conditional on interaction history, not only on calendar time or plant stage.

### P7 — mechanistic alignment need not predict final plant fitness

Posledovich 2015 directly manipulates host stage at oviposition and developmental temperature. Those variables strongly affect herbivore performance, yet the probability that the first host outgrows the larva and forms mature seedpods depends only on host species identity.

Likewise, the 21-year *Lathyrus* series shows that spring climate changes which flowering phenologies experience seed predation, but year-to-year changes in the phenology–seed-predation covariance do not explain flowering-time selection on intact-seed fitness.

Thus the confirmatory target is not whether stage alignment affects some intermediate process. It is whether stage alignment improves explanation of **final plant fitness**.

### P8 — post-exposure conversion filters can sharpen effective windows

A realized egg or attack event is not automatically a future damaging consumer.

In Parkinsonia-Penthobruchus, the same seven region-season units show a monotonic descriptive improvement from annual ground-pod egg density to stage-matched egg density to stage-matched egg density filtered by observed parasitism and hatch:

- Pearson r with final seed predation: 0.476 -> 0.596 -> 0.938;
- leave-one-**region**-out RMSE: **20.58 -> 19.93 -> 4.92** percentage points (7 region-season records, 4 held-out regions);
- outcome-exposed exploratory ablation: measured nonparasitized × hatch fraction **alone** yields **4.11 pp**, without matching egg density to host stage.

This is a useful retrospective paired diagnostic, but not a confirmatory test: adult timing is absent, n=7, and parasitism/hatch are mechanistically close to final seed destruction. Crucially, the source Table 5 egg-status and seed-fate measurements come from the same late-collected pod samples, rather than measuring survival in advance of the final outcome.

Accordingly, S_i can be used only when it is defined from pre-final biological processes and frozen independently of the final response. A filter cannot be tuned or selected because it maximizes agreement with final fitness.


## Relation to the original IWE classes

### Mutualists

The dominant object is the service window B(t), with potential asymmetry on either side.

### Antagonists

The dominant object is the effective cost window, which can differ from adult abundance or oviposition because of consumer development and host vulnerability.

### Mixed pollinating seed predators

The same lineage creates at least two stage-specific windows:

- adult service;
- delayed offspring cost.

This makes mixed systems a special test of **phase difference between interaction stages**, not merely an intermediate value between mutualism and antagonism.

## What would directly test the model

The strongest dataset has all of the following at a shared biological unit:

1. plant reproductive timing;
2. adult focal-partner activity;
3. oviposition/exposure timing;
4. delayed consumer activity or stage-specific survival;
5. non-host post-exposure conversion/survival processes such as hatch or parasitism, when biologically relevant;
6. host tissue maturation/vulnerability;
7. final post-cost reproduction.

A direct test would estimate whether between-year, between-population or experimental changes in the phase difference between adult service and effective cost windows predict changes in final fitness geometry, and whether that prediction improves on calendar timing and adult-only timing. Nulls such as Posledovich 2015 and the long-term Lathyrus result must be retained in that comparison.

## Candidate exception: persistent costs can outlive the consumer

A biologically later consumer census need not be the causal stage where the plant's future seed loss was determined. Earlier feeding can irreversibly injure developing reproductive tissue; an induced host response can also impose a lasting resource cost even if the offending larvae later die.

Chavalle et al. (2015), *Triticum aestivum–Sitodiplosis mosellana*, report that timed insecticide protection reduced later larval abundance and increased harvested yield even in a midge-resistant cultivar. Their interpretation offers **early larval damage or costly defence induction** as alternatives, not an identified mechanism.

The stage-specific model must therefore admit an **impact-history term** distinct from surviving later larvae. This changes the confirmatory prediction:

> The best candidate temporal predictor is the stage where reproductive consequences are incurred or become difficult to reverse, which need not be the last observable consumer stage.

This is a hypothesis, not a fitted law. It needs pre-harvest early-attack or plant-response measurements plus later consumer observations and harvested seed/yield at the same biological unit. A surviving-larva-only comparator must remain in the falsification set.

Source receipt: `docs/LANDSCAPE_CHAVALLE2015_EARLY_IMPACT_TRACE.md`.

## Claim boundary

This model is a structured synthesis of measured quantities already present in the IWE corpus.

It is not yet an inferential claim that window realignment universally reduces heterogeneity.

Promotion still requires independent programmes in which stage/phase alignment varies and is linked to final reproduction. Independent examples showing stage structure alone, host-filter manipulation, or herbivore-performance effects are supporting mechanism evidence, not substitutes for that test.
