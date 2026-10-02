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

For a mixed interaction, let O(t) denote oviposition/exposure, K(l) the distribution of delays from exposure to damaging consumer activity, and V_i(t) host vulnerability at the later time.

A conceptual offspring-mediated cost is:

C_i = integral P_i(s) O(s) [ integral K(l) V_i(s+l) dl ] ds.

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

The observed synchrony-predation sign reverses accordingly.

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
5. host tissue maturation/vulnerability;
6. final post-cost reproduction.

A direct test would estimate whether between-year or between-population changes in the phase difference between adult service and effective cost windows predict changes in final fitness geometry.

## Claim boundary

This model is a structured synthesis of measured quantities already present in the IWE corpus.

It is not yet an inferential claim that window realignment universally reduces heterogeneity.

Promotion still requires independent programmes with paired raw-adult and effective-cost windows linked to final reproduction.
