# Temporal signal propagation as the unifying IWE model

Date: 2026-10-03  
Status: mechanistic synthesis on the pivot branch; not a pooled meta-analytic estimand.

## Why a single synchrony coefficient fails

The original IWE design assumed that a study could be reduced to a relation of the form:

`phenological synchrony -> final plant fitness`.

The empirical audit shows that this compresses several causal stages that can transform the temporal signal before fitness is measured.

A more faithful chain is:

`T0 timing -> T1 encounter / service / oviposition -> T2 effective consumer or service stage -> T3 final plant fitness`.

The biological meaning of a timing effect depends on where along this chain it is measured.

## Signal transformations

The pivot now treats the temporal effect as something that can be transformed between stages.

### Preserved

The direction of the temporal signal survives to a later endpoint.

Example: IWE001. On the plant-earlier side of the *Corydalis–Bombus* axis, increasing temporal lead predicts lower final natural seed set across all three sites.

### Shifted or filtered

Only a subset of raw encounters remains biologically effective, changing the center or width of the relevant window.

Example: IWE032. The *Cardamine–Anthocharis* total-egg curve peaks at z = -1.10, whereas the active future-damage egg curve peaks at z = -0.61 and is narrower.

### Sign reversed

A downstream stage changes the direction of the timing association.

Examples:

- IWE011: early-to-late seasonal rank is weakly negative for initial fruit set but strongly positive for final post-predation reproduction.
- Kula 2012: flowering × oviposition synchrony predicts more predation in 2008 but less in 2009 as developmental phase relations change.

### Erased

A strong upstream timing signal disappears at a later stage.

Examples:

- James 1998: flowering timing predicts cheater oviposition, but not realized cheater larval load.
- Posledovich 2015: host stage and temperature affect larval performance, but not the mature-seedpod escape endpoint.
- long-term *Lathyrus*: climate changes the phenology–seed-predation relation, but that covariance does not explain flowering-time selection on intact-seed fitness.

### Buffered or bypassed

An alternative ecological route weakens the mapping from timing to final outcome.

Examples:

- *Ulex*: temporal escape and predator satiation yield almost identical whole-season damage.
- senita cactus: alternative pollinators buffer only when they overlap the receptive flower window.

### Tracking inertia

The consumer does not track the moving resource closely enough for potential exposure to become realized final cost.

Example: *Parkinsonia–Penthobruchus*. Egg density declines at pod maturation rather than peaking with seed availability, and realized seed predation remains modest relative to potential.

## Temporal information preservation / causal-depth hypothesis

The expanded ledger suggests a more general biological hypothesis than a mutualist-versus-antagonist sign contrast:

> **Temporal information is most likely to survive when the measured interaction stage is causally close to plant reproduction; every additional developmental, behavioral or compensatory layer creates an opportunity to shift, reverse, erase or buffer the signal.**

The current targeted pilot provides a deliberately descriptive contrast.

All four independently measured mutualist service-window chains that reach final plant fitness are currently classified as `preserved`:

- IWE001 *Corydalis–Bombus*;
- IWE023 *Mertensia* experimental flowering cohorts;
- IWE027 *Phyllodoce–Bombus*;
- IWE029 *Stigmaphyllon–Centris*.

These chains are comparatively shallow:

`partner service availability -> pollination -> mature seed`.

By contrast, antagonist and mixed systems often insert additional causal stages:

`adult / oviposition timing -> consumer development -> host filtering / targeting -> damage -> compensation / alternative pathways -> final fitness`.

The current antagonist/mixed final links therefore occupy multiple transformation states rather than one preserved state.

A provenance-based diagnostic now sharpens this observation without adding a new post hoc biological coding. Among final-fitness links:

- timing defined prospectively from independent partner activity or direct timing manipulation retains direction in **7/8** links;
- realized-interaction or seasonal-position references retain direction in **2/8** links;
- exact `preserved` states are **7/8** versus **1/8**, respectively.

The realized/seasonal side contains two Cardamine links from one dependence cluster; removing either leaves direction retention at 1/7 or 2/7, so the descriptive contrast does not depend on that duplicate.

This pattern must **not** be interpreted as a literature-wide class frequency or formal treatment effect. The pilot was assembled for IWE rather than sampled to estimate transformation prevalence; interaction class, endpoint choice and timing-reference provenance are confounded; and propagation links are not guaranteed independent.

The confirmatory version of the hypothesis is architectural rather than taxonomic:

> within comparable datasets, adding biologically required downstream stage information should improve final-fitness prediction when those stages genuinely transform exposure, but should not improve prediction when the extra stage is irrelevant.

Parkinsonia supplies the first positive paired diagnostic under this logic; Posledovich and long-term Lathyrus supply mandatory nulls.

## Why this helps explain the original IWE bottleneck

Different literatures sample different links in the chain.

Pollination studies often measure:

`partner activity -> visitation / pollen receipt -> fruit or seed set`.

Seed-predator studies often begin later:

`oviposition / attack -> larval survival / damage -> final intact seeds`.

Mixed pollinating seed-predator studies may contain two simultaneous chains:

`adult activity -> pollination benefit`

and

`adult oviposition -> developmental lag -> larval cost`.

A meta-analysis that forces all of these into a common "synchrony" coefficient is therefore combining effects that are measured at different causal depths and whose sign can change between those depths.

The evidence gap uncovered by strict H1 is partly a **causal-stage mismatch**, not merely missing sample size.

## Relationship to prior mismatch and buffering frameworks

This model overlaps with, but is not equivalent to, existing phenological mismatch theory.

- Visser & Gienapp 2019 emphasize evolutionary and demographic consequences of mismatch and the need to connect timing to fitness.
- Kharouba & Wolkovich 2020 identify a major disconnect between match-mismatch theory and the data normally collected, especially the scarcity of experiments that directly link timing to fitness.
- Kharouba et al. 2023 report limited support for the terrestrial match-mismatch hypothesis and emphasize assumptions and alternative fitness drivers.
- Weir & Phillimore 2024 explicitly synthesize buffering mechanisms that soften mismatch costs.

IWE treats buffering as one transformation state rather than as the entire framework. Its candidate addition is to track several possible fates of a source-backed timing signal—preservation, filtering, reversal, erasure, buffering and tracking failure—across explicit causal stages and through to final plant reproduction.

The term "temporal information preservation" is used as an internal working label. No claim is made that the phrase itself is novel.

## Relationship to the stage-specific window model

The stage-specific interaction-window model specifies the biological coordinates that can transform the signal:

- adult service / encounter timing;
- oviposition timing;
- consumer developmental lag;
- host maturation and vulnerability;
- host retention / abortion;
- consumer targeting;
- partner-induced host modification;
- accessible alternative partners.

Temporal signal propagation specifies the **consequence** of those mechanisms:

- preserve;
- shift/filter;
- reverse;
- erase;
- buffer;
- fail to track.

The two models therefore play different roles.

The stage-specific model explains *why* the signal changes.  
The propagation model records *how far and in what form* it reaches plant fitness.

## A response-independent phase coordinate

Where source timing allows it, developmental head start can be defined before inspecting final fitness.

For Kula 2012:

`phase safety margin = flower-to-first-larva delay - fruit maturation time`.

It is -11.3 d in 2008 and +0.3 d in 2009, matching the year-to-year reversal in the synchrony-predation sign.

For Cardamine, using the source-defined 7-d active-egg boundary as a descriptive ecotype reference:

- early ecotype mean flowering-to-egg interval 11.50 d -> +4.50 d from the active boundary;
- late ecotype 5.72 d -> -1.28 d.

The direction agrees with the ecotype-level final attacked-plant fate (34% vs 4% dehiscing before larval completion), but these summaries are not assumed to be individual-level paired observations.

This is exactly the kind of prospective coordinate needed for a future confirmatory test.

## Confirmatory prediction

The strongest test is no longer:

> does synchrony affect fitness?

It is:

> does a timing coordinate defined at the biologically effective causal stage explain final plant fitness better than calendar timing or an upstream encounter-only coordinate?

For a suitable multi-stage dataset, compare prospectively defined models based on:

1. calendar plant timing;
2. adult partner timing;
3. realized encounter / oviposition timing;
4. developmental phase or effective-consumer timing;
5. host-filtered effective cost timing.

Promotion requires improvement at the **final plant-fitness endpoint**, not just at larval performance, attack or another intermediate response.

## Mandatory counterexamples

The framework is falsifiable only if it retains cases where the expected propagation does not occur.

At minimum retain:

- James 1998 — exposure signal erased before larval realization;
- Posledovich 2015 — developmental matching affects larvae but not mature-seedpod escape;
- long-term Lathyrus — attack covariance moves without moving selection through that path;
- Ulex — alternative avoidance mechanisms converge on the same final outcome.

These are not noise. They define the conditions under which timing information is lost.

## Analysis rule

Do not pool transformation categories as if they were homologous effect sizes.

The first quantitative use of the propagation model should be one of:

- within-programme paired-stage comparisons;
- source-defined multi-stage path models;
- prospective model comparison among calendar, exposure and effective-stage coordinates;
- an evidence map of where signals are preserved, transformed or lost.

Only after several independent programmes expose homologous stage-to-stage links should a common effect family be considered.

## Current claim

A defensible current synthesis is:

> Phenological effects are not transmitted unchanged from interaction timing to fitness. Across the current IWE corpus, temporal signals can be preserved, filtered, reversed, erased or buffered as they pass through interaction stages; the key empirical problem is therefore to identify where in the causal chain timing information is converted into final reproductive consequences.

The pilot further motivates a **temporal information preservation / causal-depth hypothesis**: timing information appears most stable when the reference is defined prospectively at or near the biologically effective interaction stage, and increasingly contingent when delayed consumers, host filters, consumer targeting or alternative pathways intervene. The current 7/8 versus 2/8 provenance contrast is diagnostic only; the decisive test remains a within-programme paired comparison at final fitness.

This is broader than the original mutualist/antagonist/mixed sign comparison while remaining testable and source-provenance aware.
