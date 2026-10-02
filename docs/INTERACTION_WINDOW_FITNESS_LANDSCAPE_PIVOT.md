# IWE interaction-window fitness-landscape pivot

Date: 2026-10-02  
Status: exploratory pivot on a separate branch; the frozen strict-H1 synchrony analysis on main is unchanged.

## Why pivot

The original IWE question asks whether the plant-fitness effect of phenological synchrony differs among mutualists, antagonists, and mixed pollinating seed predators. The strict implementation deliberately requires a partner-activity window that can order plant timing independently of the plant reproductive response.

That contract is useful for a causal synchrony claim, but the current evidence audit shows a structural mismatch between that estimand and the literature. Antagonist studies commonly measure realized interaction timing (eggs, attack, infestation or seed predation) rather than an independent adult-activity curve. Mixed systems additionally require benefit and cost to be linked to the same plant timing and final reproductive surface.

The pivot does not weaken or overwrite the strict synchrony contract. It asks a broader ecological question while preserving the provenance of the timing reference.

## New primary question

> How does plant reproductive performance vary across the temporal position of an interaction window, and how does the geometry of that fitness landscape differ among mutualistic, antagonistic, and mixed interactions?

Write relative timing as:

tau = plant timing - interaction-window timing

The target is the shape of W(tau), rather than a single monotonic coefficient labelled synchrony.

This makes three distinctions explicit:

1. side — plant earlier than, within, or later than the interaction window;
2. interaction role — mutualist, antagonist, or mixed;
3. reference provenance — what biological observation defines the interaction window.

## Window-reference classes

Landscape evidence is never pooled across these classes without an explicit sensitivity model.

### independent_partner_activity

The window is defined by adult census, trapping, visitation, capture/recapture or another activity measure that can be evaluated independently of the focal plant reproductive outcome.

This is the strongest reference class and contains the strict-H1 subset when all other synchrony conditions are met.

### realized_interaction_window

The window is defined by egg receipt, oviposition, attack, infestation, larval occupancy, damage or seed predation.

These observations are not treated as independent partner availability. They can nevertheless describe when realized antagonistic or mixed interactions occur and can support a descriptive fitness-landscape analysis if timing and final reproduction are linked at a defensible unit.

### historical_partner_window

Partner timing is imported from another season, study or historical source. This can motivate a timing interpretation but cannot identify the focal-season interaction window.

### seasonal_position_only

The study measures flowering time or experimental timing and reproduction but no defensible partner-relative window. These rows support seasonal timing sensitivity, not an interaction-window claim.

### direct_interaction_manipulation

The timing of herbivory, attack, pollination or another interaction is experimentally imposed. This can identify sensitivity to interaction timing even when it does not reconstruct a natural partner-availability curve.

## Fitness channels

The pivot separates rather than conflates:

- net_reproduction — final plant reproductive performance after benefits and costs;
- benefit_channel — pollination, pollen receipt or another positive reproductive channel;
- cost_channel — oviposition, fruit loss, seed loss or another antagonistic channel;
- total_offspring_fitness — an integrated fitness measure beyond simple seed or fruit count;
- potential_reproduction — pre-cost or model-derived potential reproduction; mechanism only unless linked to final realized reproduction.

For mixed pollinating seed predators, the ecological target is:

W_net(tau) = B(tau) - C(tau)

The benefit and cost curves need not peak at the same tau, so the net optimum can be displaced from peak partner activity.

## Geometry hypotheses

### G1 — mutualist peak

For a mutualist whose reference window represents partner availability, final reproduction is expected to be lower away from the effective interaction window than within it. The two sides are estimated separately whenever data permit; symmetry is not assumed.

### G2 — antagonist trough / temporal escape

For an antagonist, final post-cost reproduction can be lowest in the realized or independently measured interaction window and higher in an early and/or late temporal refugium.

The estimand is therefore not merely negative synchrony. It is whether an interaction window creates a trough in the final-reproduction surface.

### G3 — directional asymmetry

Early escape and late escape are not assumed equivalent. Tests retain core-vs-early and core-vs-late contrasts separately, exactly as already frozen for the Cardamine preflight.

### G4 — mixed displacement or curvature

In mixed pollinating-seed-predator systems, benefit and cost can share a partner but differ in timing or strength. The net fitness optimum may therefore occur before, within or after the partner-activity maximum and may be non-monotonic.

This is a stronger formulation of the original H2 and becomes a central target rather than an optional quadratic afterthought.

## Evidence hierarchy and claim boundary

The pivot separates geometry evidence from causal window identification.

- independent_partner_activity can support a partner-relative timing claim, subject to the original unit and variance rules.
- realized_interaction_window can support a descriptive escape-from-realized-attack or oviposition claim, but not a claim that independent adult availability caused the pattern.
- seasonal_position_only cannot be relabelled as partner synchrony.
- historical windows remain contextual unless the focal timing linkage is recovered.
- no lower reference class is silently promoted to a higher one.

## Pilot recovery strategy

The first pass prioritizes already-screened IWE programmes:

1. re-extract one-sided responses from IWE001/IWE002 where the raw signed mismatch series permit it;
2. retain IWE023/IWE027/IWE029 as high-provenance mutualist anchors;
3. restore IWE015 after its variance audit as the strongest mixed net-fitness anchor;
4. use IWE032 Cardamine as the strongest antagonist early/core/late design once the 2012-2014 female timing object is recovered;
5. audit IWE011/IWE014 and related programmes as realized_interaction_window evidence rather than forcing them through the independent-adult-activity gate;
6. keep IWE031 as a distinct experimental interaction-timing route, not as natural synchrony.

## Meta-analytic rule

The first quantitative model does not pool all native effect families into one universal effect.

Preferred order:

1. reconstruct within-programme geometry on its native scale;
2. convert only clearly homologous contrasts to a common family, such as center-vs-early and center-vs-late Hedges g;
3. cluster by dependence_id;
4. estimate interaction-type moderation only after independent replication exists within the same geometry/effect family;
5. otherwise report an evidence map plus programme-level landscapes.

The existing CR2 minimum-information rule remains in force for robust class-level meta-analytic inference.

## Pilot result

The initial registry contains 14 components from 14 screened studies and 13 dependence clusters.

Under the original high-provenance requirement, strong final-fitness anchors are currently:

- mutualist: 3 programmes;
- antagonist: 1 programme, currently blocked by Cardamine female-flight timing;
- mixed: 1 programme, currently on the IWE015 variance hold.

Under the broadened landscape question, while preserving reference provenance rather than pooling it away, the pilot has recoverable programme clusters in:

- mutualist: 4;
- antagonist: 4;
- mixed: 2.

This does not make the three-class meta-analysis inferentially ready. It shows that the main loss of antagonist evidence came from asking for independent adult availability, not from an absence of timing-fitness biology.

## Success criterion

Keep this pivot only if it achieves at least one of the following without relaxing source provenance:

- recovers directional or two-sided fitness geometry from multiple independent programmes;
- gives antagonist studies a legitimate temporal-escape estimand without pretending egg/attack timing is independent adult availability;
- yields at least two independent mixed programmes with separable benefit/cost or net-fitness timing;
- demonstrates a reproducible evidence-architecture result showing that identifiable landscape geometry differs by interaction role and reference provenance.

If none of these are achieved, this branch remains an exploratory diagnosis and main is not rewritten retrospectively.
