# Temporal information preservation hypothesis

Date: 2026-10-06  
Status: exploratory synthesis generated from the IWE pivot; not a literature-wide prevalence claim and not a replacement for the confirmatory phase-alignment gate.

## Question

Most phenological mismatch studies ask:

> How much do two phenologies overlap, and is mismatch associated with fitness?

The IWE evidence suggests a different question is often more informative:

> **When a timing signal is observed at one stage of an interaction, under what conditions is its direction preserved to final fitness rather than shifted, reversed, erased or buffered downstream?**

This is the **temporal information preservation hypothesis**.

## Causal-chain view

Represent the biological chain schematically as:

`timing -> encounter/service/oviposition -> effective consumer/service stage -> final fitness`.

A timing effect can undergo several source-backed transformations:

- `preserved` — the upstream temporal ordering retains its direction at final fitness;
- `shifted_filtered` — only a temporally filtered subset of exposure becomes effective;
- `sign_reversed` — a downstream stage reverses the upstream temporal relationship;
- `erased` — an upstream timing relationship no longer predicts the downstream state;
- `buffered` — a real timing cost is compensated before whole-organism fitness;
- `tracking_inertia` — consumer timing fails to follow a moving resource window;
- `preserved_net_changed_mechanism` — final direction persists although the component pathways producing it change.

These states are not effect sizes and are not ordinal scores.

## Current source-backed diagnostic

Restrict the temporal signal-propagation ledger to links reaching a final plant-fitness endpoint.

There are currently **30 final-fitness links from 26 studies**.

### Prospectively defined timing references

Timing is considered prospective here when it is based on either:

- `independent_partner_activity`; or
- `direct_interaction_manipulation`.

Among eighteen final-fitness links with these references:

- independent partner activity: **6/7 exact preserved**, **1/7 buffered**;
- direct timing manipulation: **8/11 preserved**, **1/11 sign-reversed**, **1/11 erased**, **1/11 buffered**.

Combined:

- exact preservation: **14/18**;
- direction retention among direction-comparable links: **14/18**.

The prospective exceptions are biologically informative rather than treated as noise.

- IWE023 *Mertensia ciliata*: total visitation falls by more than fivefold across experimental flowering cohorts, but later cohorts receive a higher proportion of more-effective bumblebee visits and seed set does not differ significantly across weeks (F(3,36)=1.01). The frozen week-1 versus week-4 SMD remains positive, but the source-level causal signal is classified as buffered rather than preserved.
- Gols 2025: the same direct herbivory-timing experiment yields different downstream states in two brassicaceous hosts. Timing is buffered before integrated reproductive potential in *Sinapis arvensis* (ontogeny p=0.81) but preserved in *Brassica nigra* (p<0.001).

The retained examples include mutualist service windows as well as antagonists such as Aucuba, Wu wheat-midge, Wise wheat-midge and experimentally timed *Asclepias–monarch* herbivory. Thus preservation is not unique to mutualism, while Mertensia supplies a prospective mutualist counterexample in which changing pollinator composition buffers a large visitation decline before final seed set.

The mandatory exception is Posledovich 2015: host stage and temperature alter herbivore performance, but the mature-seedpod escape endpoint is erased with respect to those predictors.

### Realized-interaction or seasonal references

Among twelve final-fitness links whose upstream reference is `realized_interaction_window` or `seasonal_position_only`:

- exact preservation: **2/12**;
- one shifted/filtered Cardamine link changes window position/width and is explicitly **direction-incomparable**;
- among the remaining eleven direction-comparable links, direction retention including `preserved_net_changed_mechanism` is **3/11**;
- the remaining links are reversed, erased, buffered or tracking-inertial.

This group includes Peucedanum, Cardamine raw egg exposure, long-term Lathyrus, Ulex, Parkinsonia, Dianthus and Trollius buffering.

### Dependence sensitivity

Cardamine contributes two final-fitness propagation links to the realized-interaction class.

The shifted/filtered total-egg -> active-egg Cardamine link is direction-incomparable and is not counted as a directional failure. Excluding all IWE032 direction-comparable realized/seasonal links changes realized/seasonal direction retention from **3/11 to 2/10**; prospective direction retention remains **14/18**.

No formal p-value is used because the corpus is targeted, reference provenance is confounded with biological system and interaction class, and propagation links are not guaranteed to be independent sampling units.

### Antagonist-only programme-level sensitivity

The provenance pattern is not solely a mutualist-versus-antagonist contrast.

After restricting to antagonists and collapsing all final-fitness links within each dependence cluster:

- prospective timing references: **4/6 antagonist programmes all direction-retaining**, 1 mixed (Gols 2025), 1 none-retaining;
- realized/seasonal references: after excluding direction-incomparable links from the binary retention summary, **1/7 all-retaining**, 0 mixed, 6 none-retaining.

This removes the mutualist-class contribution—including the Mertensia buffer—and collapses repeated Cardamine links while refusing to treat a shifted window as a directional failure. The added Gols programme prevents the prospective antagonist set from looking artificially homogeneous: one plant species preserves the timing effect and another buffers it within the same experiment. The comparison remains descriptive because the antagonist programmes differ in endpoint, design and biological system.

## Biological interpretation

The diagnostic suggests that the important distinction may not be mutualist versus antagonist versus mixed interaction per se.

A stronger candidate principle is:

> **Temporal effects may be more likely to survive to final fitness when timing is defined prospectively at, or close to, the biological stage that actually delivers service or damage.**

The current corpus cannot identify that mechanism from provenance alone. “Prospective” mixes independent adult monitoring with direct experimental timing manipulation, so stronger retention could partly reflect design quality, intervention control or endpoint choice rather than biological causal proximity.

Mertensia and Gols make the qualification essential: even prospectively defined timing can be buffered by changes in partner effectiveness or by compensatory host responses, and closely related hosts can differ in whether the signal reaches final reproduction.

Upstream calendar timing, realized attack proxies and coarse seasonal position also leave more intervening biological opportunities for the signal to be rewritten, but that causal-depth interpretation remains a hypothesis to be tested with matched designs.

Those transformations already have distinct empirical mechanisms in IWE:

- consumer developmental lag;
- host-stage filtering;
- consumer targeting of host units likely to survive;
- partner-induced modification of host retention;
- alternative partner buffering;
- resource tracking failure;
- compensation across reproductive units.

## Relation to existing mismatch theory

This hypothesis does not claim that buffering is new.

Major prior frameworks already establish important pieces:

- Visser & Gienapp 2019 emphasize the need to connect mismatch to evolutionary and demographic fitness consequences.
- Kharouba & Wolkovich 2020 identify a theory-data disconnect and argue for experiments that directly link timing to fitness.
- Kharouba et al. 2023 report limited support for the terrestrial match-mismatch hypothesis and emphasize assumptions and alternative fitness drivers.
- Weir & Phillimore 2024 explicitly synthesize buffering of phenological mismatch, including mechanisms that reduce mismatch costs and damp performance variation at higher organizational levels.

IWE extends this direction by treating buffering as **one of several possible transformations of temporal information** and by tracking transformation state through an explicit interaction-stage chain.

The candidate novelty is therefore not "mismatch effects can be buffered."

It is:

> **Phenological information can be preserved, transformed or lost between interaction stages, and the position/provenance of the timing measurement may predict whether its direction survives to final fitness.**

## Predictions

### TIP1 — prospective effective-stage references preserve direction more often, conditional on design

Timing defined independently of final outcomes, especially at a source-backed service/susceptibility stage, should more often retain its direction to final fitness than calendar or outcome-entangled timing proxies **when study design and endpoint depth are comparable**.

This prediction is **not identified by the current descriptive contrast**, because independent adult monitoring, direct timing manipulations, biological systems and endpoints are unevenly distributed among provenance classes.

### TIP2 — additional biological transformations create more opportunities for information loss

Longer chains containing delayed consumers, host filtering, partner behavior, compensation or alternative partners should show more shifted, reversed, erased or buffered states.

This is a causal-depth prediction, not yet an inferential result.

### TIP3 — interaction class is secondary to causal position

Mutualist service windows may often appear stable because service is causally close to reproduction.

Antagonist signals can also be preserved when measured at an effective susceptible stage, as shown by Aucuba and wheat-midge systems.

Conversely, mixed and antagonist signals measured upstream can be transformed repeatedly before final reproduction.

### TIP4 — the decisive test is paired predictive improvement

Within the same programme and final-fitness dataset, a prospectively defined effective-stage coordinate should predict final fitness better than a simpler calendar/adult-only coordinate if the hypothesis is correct.

This is exactly the current `confirmatory_ready` gate.

## Falsification criteria

The hypothesis should be weakened or rejected if:

1. systematic expansion of the corpus causes prospectively defined final-fitness links to show transformation/loss as often as lower-provenance links; Mertensia and the buffered Sinapis arm of Gols 2025 are already counterexamples and must remain in the denominator;
2. paired within-programme comparisons repeatedly show no predictive improvement from effective-stage alignment;
3. the provenance contrast disappears after dependence-aware programme-level aggregation;
4. transformation state is explained by study design or endpoint selection rather than biological causal position.

Posledovich 2015 and long-term Lathyrus are retained specifically because they already demonstrate that mechanistic stage effects need not reach final plant fitness.

## Next empirical test

The highest-value next dataset is not another example of stage structure.

It is one programme containing, at compatible units:

1. a simpler timing coordinate;
2. a prospectively defined effective-stage coordinate;
3. final plant reproduction;
4. enough unit-level data to compare predictive performance without defining the effective coordinate from the outcome.

Current near-routes are IWE032 Cardamine and Hurlburt Yucca; Wu wheat-midge is a strong stage-matched final-fitness example but lacks a genuinely stage-free adult-only comparator by design. Parkinsonia supplies a non-confirmatory paired realized comparison, but it sharpens the hypothesis: stage matching alone reduces leave-one-region-out RMSE by only 3.2%, whereas adding the source-measured parasitism and hatch filters reduces RMSE by 76.1% relative to the annual exposure comparator. The useful extra information is therefore the biologically relevant conversion from exposure to effective future consumer pressure, not causal depth for its own sake.

Until one of those paired comparisons closes, temporal information preservation remains a strongly motivated exploratory hypothesis rather than a confirmatory general law.
