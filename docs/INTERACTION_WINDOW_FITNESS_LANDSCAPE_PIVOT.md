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


The expanded audit shows that the interaction window itself has three separable temporal ingredients:

- **partner exposure** — when the focal interacting animal is available, or when pollination/attack is realized;
- **host sensitivity** — how strongly that same interaction changes final reproduction at the plant's current developmental stage;
- **accessible redundancy** — which alternative partners are actually active and able to use receptive flowers at that same time.

IWE therefore uses the empirical bookkeeping relation

`impact(t) = f(exposure(t), host_sensitivity(t), accessible_redundancy(t))`

without assuming a multiplicative functional form. IWE012 and IWE031 show why exposure and sensitivity must be separated, while the senita-cactus programme shows why partner richness cannot be treated as time-invariant redundancy: a moth cohort gap produced zero open-pollinated fruit set when alternative pollinators were temporally inaccessible.

This makes three distinctions explicit:

1. side — plant earlier than, within, or later than the interaction window;
2. interaction role — mutualist, antagonist, or mixed;
3. reference provenance — what biological observation defines the interaction window.

## Two linked estimands

The pivot now has two complementary quantitative objects.

### A. Window-relative fitness geometry

When a partner or realized-interaction window is identifiable, estimate the shape of W(tau). This is the mechanistically preferred coordinate because calendar-date signs can reverse among systems.

### B. Signed interaction-induced selection shift

When studies estimate flowering-time selection under contrasted interaction environments, retain the signed change in the directional selection gradient:

delta_beta_agent = beta_agent_context - beta_reference_context.

For comparability, the pilot orients this to a canonical flowering-time coordinate in which positive means a shift toward earlier flowering and negative means a shift toward later flowering.

The signed-selection module does not pretend that calendar early/late is itself a universal mechanism. Its role is diagnostic: it tests whether interactions rotate the seasonal fitness surface and whether apparent sign heterogeneity can be explained by each system's position relative to its interaction window.

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

### G2 — composite antagonist impact window

For an antagonist, final post-cost reproduction can be lowest where partner exposure is high, where the plant is especially vulnerable, or where both coincide. A temporal refugium can therefore arise through escape from antagonist exposure, greater tolerance at another plant stage, or both.

The estimand is not merely negative synchrony. It is the geometry of the reproductive-cost surface and which temporal component creates it.

### G3 — directional asymmetry

Early escape and late escape are not assumed equivalent. Tests retain core-vs-early and core-vs-late contrasts separately, exactly as already frozen for the Cardamine preflight.

### G4 — mixed benefit-cost phase decoupling

In mixed pollinating-seed-predator systems, benefit and cost can share a partner yet have different temporal shapes. IWE014 provides a concrete boundary case: early and late flowering have similar pollination success while seed predation is higher early.

For interactions in which adults provide the benefit but offspring impose the cost, the two channels can also be separated by **consumer development time**. Kula 2012 shows that flowering × oviposition synchrony predicted greater predation in 2008 but lower predation in 2009 because the delay from flowering/egg deposition to larval activity was longer in 2009 and fruits matured faster.

Thus the cost channel should be treated conceptually as:

`effective cost window = exposure window ⊗ developmental lag × host vulnerability`.

The net fitness optimum can therefore shift even when adult synchrony is unchanged or increases. The target is the relative timing, developmental phase and amplitude of benefit and cost channels, not merely a quadratic term on one synchrony score.

### G5 — calendar sign is not invariant

Interaction class is not expected to predict a universal early-versus-late calendar direction. The same antagonist class can favor later flowering in one system and earlier flowering in another. The general prediction is instead window-relative: antagonistic interactions can favor temporal escape from the effective cost window, while mutualistic interactions can favor movement toward an effective service window.

Signed selection-gradient contrasts are therefore retained rather than converted to absolute magnitudes.

### G6 — redundancy is overlap-conditioned

Alternative partners buffer mismatch only when they are active and can access receptive flowers at the relevant time.

Define the time-indexed quantity conceptually as:

`R_eff(t) = sum_j I(partner_j active at t AND able to access receptive flowers at t)`.

This is not a fixed richness count. Senita cactus provides the motivating test: diurnal bee co-pollinators become ineffective when flowers close before sunrise, and a gap between senita-moth cohorts in July 1998 coincided with 0% open-pollinated fruit set despite the broader pollinator community.

### G7 — host filters are interaction-dependent

The host developmental filter that maps exposure into future reproductive cost need not be fixed.

In *Lathyrus–Bruchus*, the antagonist uses fruit phenology, position and additional cues to concentrate eggs on fruits with low future abortion probability, partly circumventing the filter.

In *Rheum–Bradysia*, oviposition itself lowers fruit abortion and changes IAA dynamics before larvae hatch, indicating that the interaction can modify the filter.

Effective-window inference must therefore distinguish plant-intrinsic filtering from consumer targeting and partner-induced host modification.

### G8 — mechanistic stage matching is not sufficient for final-fitness prediction

Stage alignment can strongly affect consumer performance without predicting the final plant endpoint.

Posledovich 2015 experimentally changes host phenological stage at oviposition and developmental temperature. Those variables alter larval performance, but the probability that the host outgrows the larva and forms mature seedpods depends only on host species.

Likewise, in the 21-year *Lathyrus* series, spring climate changes which flowering phenologies suffer seed predation, yet year-to-year variation in the flowering-date–seed-predation covariance does not explain flowering-time selection on intact-seed fitness.

The confirmatory target is therefore final reproductive geometry, not mechanism alone.


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

For the signed-selection module, treatment contrasts are pooled only when the trait coordinate, agent contrast, fitness interpretation and uncertainty are compatible. Published absolute differences are never back-converted into signed effects. Contrasts lacking covariance or a source-reported interaction test remain evidence-map results rather than pooled estimates.

## Pilot result

The current pilot registry contains **29 components from 27 studies and 25 dependence clusters**.

Under the original high-provenance requirement, strong final-fitness anchors are currently:

- mutualist: 3 programmes;
- antagonist: 1 programme, currently blocked by Cardamine female-flight timing;
- mixed: 1 programme, currently on the IWE015 variance hold.

Under the broadened landscape question, while preserving reference provenance rather than pooling it away, the pilot has recoverable programme clusters in:

- mutualist: **4**;
- antagonist: **5**;
- mixed: **2**.

This does not make the three-class meta-analysis inferentially ready. Boundary and mechanism-only rows are deliberately excluded from those programme counts. The result instead shows that the original design asked every study to identify the same temporal object even though the literature measures complementary parts of the mechanism: partner exposure, realized attack, host-stage sensitivity, accessible redundancy, and benefit-cost channel timing.

### First quantitative results on the pivot

The branch now contains multiple complementary kinds of timing evidence.

1. **IWE001 directional mismatch.** On the plant-earlier side of the Corydalis-Bombus mismatch axis, larger plant lead is associated with lower natural seed set at all three sites: NFP r = -0.578 (n = 11), TOEF r = -0.833 (n = 8), and JOZ r = -0.952 (n = 4). The partner-earlier side is too sparse for the registered Fisher-z variance. All sites remain one dependence cluster.

2. **IWE011 realized antagonist cost surface.** Using the five permanent plots as the exposure units, the early-to-late flowering rank is weakly related to initial fruit set (Spearman rho = -0.316) but strongly positively related to final fruit set and intact fruit number (rho = +0.800 for both). With only five plots these are descriptive associations, but they avoid the withdrawn plant-level pseudoreplication and show that the seasonal fitness gradient emerges mainly after seed predation.

3. **IWE012 selection reversal.** In Gentiana pneumonanthe populations without Phengaris alcon, flowering-time selection favors earlier flowering, whereas predator-present populations favor later flowering. The descriptive source-mean shifts are -0.41 in 2010 and -0.40 in 2011 on the canonical earlier-flowering axis; the source Predation x Phenology tests are p < 0.001 in both years. No variance for the derived mean difference is invented.


4. **IWE014 mixed channel decoupling.** In *Silene vulgaris*, early and late plants have similar pollination success but early plants experience greater seed predation. This identifies a mixed-system cost curve that changes seasonally without a matching change in the benefit channel; it remains source-summary evidence because no independent adult-*Hadena* activity curve or variance-bearing early/late net-fitness contrast is available.

5. **Althoff 2005 mixed benefit window.** In *Yucca filamentosa × Tegeticula cassandra*, peak flowering date predicts lower pollinator abundance in both years (path coefficients -0.37 in 2001 and -0.27 in 2002), while pollinator abundance predicts higher relative fruit set (+0.60 and +0.48). This independently identifies the service side of a mixed interaction window, but fruit set precedes larval seed consumption and therefore remains a benefit-channel mechanism rather than net mixed fitness.

6. **Senita overlap-conditioned redundancy.** Pollinator-exclusion experiments show that co-pollinator buffering is available only when alternative partners overlap the receptive flower window. In July 1998, senita moths were between adult cohorts and open-pollinated fruit set was 0%, while pollen-supplemented flowers set 22.5 ± 6.6% fruit. In later hot seasons, flowers closed before sunrise and naturally excluded diurnal bees. This motivates a time-indexed effective-redundancy term rather than partner richness alone.

7. **Kula 2012 developmental phase lag.** In the same Mountain Lake *Silene–Hadena* programme, individual flowering × oviposition synchrony predicted predation in opposite directions across years: higher synchrony increased predation in 2008 (chi-square = 46.47, p < 0.0001) but decreased predation in 2009 (chi-square = 16.74, p < 0.0001). Flower/egg-to-first-larva delays were 10/5 days in 2008 versus 17/15 days in 2009, and fruit maturation was faster in 2009 (16.7 vs 21.3 days), identifying developmental phase lag as a mechanism that can reverse cost geometry.

8. **Trollius–Chiastocheta flower-age gradient.** Different pollinating seed-predator species oviposit from flower day 1 through day 7 or later. Because each visit fertilizes a fraction of the ovules still unfertilized, marginal adult pollination benefit declines with flower age while delayed larval seed cost persists. The classic cost-benefit analysis places equality around 4–5 eggs/flower, while natural annual means span 2.3–7.25.

9. **Glochidion–Epicephala annual phase structure.** Adult moths pollinate and oviposit in April–May, host fruits and moth eggs remain dormant May–December, and larvae hatch and consume seeds in January–February. Adult service and offspring cost are therefore separated by roughly eight months. This is registered as stage-structure evidence rather than a timing-effect programme.

10. **IWE031 host-stage sensitivity.** Timed monarch herbivory on *Asclepias fascicularis* separates when damage occurs from natural monarch availability. Early herbivory most strongly affects plant size, whereas late herbivory has the strongest effect on viable-seed production. This directly demonstrates that the reproductive impact window depends on plant stage as well as antagonist exposure.


11. **IWE032 host filtering of antagonist exposure.** In *Cardamine pratensis × Anthocharis cardamines*, the source-reported Gaussian peak for all eggs occurs at flowering-date z = -1.10, whereas the peak for "active" eggs capable of producing damaging late-instar larvae occurs at z = -0.61. Host-stage filtering therefore shifts the effective cost window **+0.49 SD later** and narrows its Gaussian sigma from **0.92 to 0.66** (28.3% narrower). This mechanism result is distinct from the still-blocked strict female-flight route.


12. **Independent host-filter replication.** Arnaldo et al. 2014 followed 127 *Gentiana pneumonanthe* shoots and 837 *Phengaris alcon* eggs in Portugal. Egg load was highest in the first third of the flight period, while offspring survival varied with flower-bud size, flower developmental stage, and oviposition period. This independently supports host-state filtering of antagonist exposure, but remains mechanism-only because final plant reproduction was not measured.


13. **Taxonomically distinct host filtering.** In the *Yucca glauca–Tegeticula yuccasella* nursery-pollination system, resource allocation makes late-opening flowers more likely to abort when basal fruits are already present; all moth eggs in an aborted flower die. This supplies a distinct plant-allocation route by which a realized interaction can be deleted before becoming an effective future seed-predation cost. It is mechanism-only, not a final-fitness effect.

14. **Lathyrus host-filter offense and long-term null.** *Bruchus atomarius* preferentially oviposits on fruits with lower future abortion probability; observed selective oviposition yields more developed beetles than a random allocation (2.84 ± 0.14 vs 2.02 ± 0.11) and reduces average intact-seed output relative to random oviposition. Over 21 years, spring temperatures alter which flowering phenologies suffer seed predation, but the yearly covariance between flowering date and seed predation does not explain flowering-time selection (estimate -0.033, 95% CI -0.101 to +0.037).

15. **Posledovich 2015 developmental-race boundary.** Host stage at oviposition and temperature strongly affect *Anthocharis cardamines* larval performance, but the probability that the attacked plant outgrows the larva and forms mature seedpods depends only on host species identity. This directly falsifies the assumption that better stage alignment must improve prediction of the final plant endpoint.

16. **Rheum–Bradysia partner-modified host filter.** Oviposition strongly reduces fruit abortion (F = 287.24, p < 0.001) and elevates IAA before larvae hatch (oviposition F = 355.97; oviposition × day F = 140.82; both p < 0.001), while flowering sequence does not explain oviposition or abortion. The interacting partner can therefore modify the host filter itself.

A separate factorial source, Sletvold et al. 2015 Gymnadenia conopsea, provides an important sign check. Reconstructed from Ecological Archives Table A2, pollinators shift selection toward later flowering (canonical estimates -0.1558 and -0.1600 depending on herbivory context), whereas floral herbivores shift selection toward earlier flowering (+0.0982 and +0.0940 depending on pollination context). These four contrasts have reconstructable SEs because the treatment groups are independent.

A third programme, Thomsen & Sargent 2017 Lythrum salicaria, experimentally imposed meristem damage. The flowering-start gradient was -0.28 under damage and -0.03 in controls, giving an oriented damage-mediated shift of +0.25 toward earlier flowering with source-reported SE = 0.10. The same experiment found essentially no pollination-by-damage modification of flowering-time selection (three-way contrast +0.01 ± 0.12).

Taken together, the Gentiana, Gymnadenia and Lythrum results reject a simple calendar rule such as "antagonists favor late flowering." They instead motivate the stronger window-relative question: why does an interaction rotate the flowering-time fitness surface in different calendar directions across systems?

### Existing large discovery universe

Caruso et al. 2019 already assembled 755 directional selection-gradient records with SEs, including 139 flowering-phenology records, and constructed 487 same-trait/same-fitness treatment pairs. Their Table 2 contains 90 flowering-phenology treatment-pair studies, including 39 supplemental-hand-pollination pairs. Their published synthesis intentionally used the absolute treatment difference |beta_i - beta_j| to quantify strength of agent-mediated selection. That makes the deposited database a high-value discovery universe for IWE's signed delta-beta question, because the published magnitude analysis discards exactly the direction information needed here.

The Dryad manifest and workbook identities are verified, but current unauthenticated file-byte routes are access-limited. Until the non-duplicated workbook is lawfully ingested, Caruso is treated as a search universe rather than as new IWE quantitative evidence.

## Success criterion

Keep this pivot only if it achieves at least one of the following without relaxing source provenance:

- recovers directional or two-sided fitness geometry from multiple independent programmes;
- gives antagonist studies a legitimate temporal-escape estimand without pretending egg/attack timing is independent adult availability;
- yields at least two independent mixed programmes with separable benefit/cost or net-fitness timing;
- demonstrates a reproducible evidence-architecture result showing that identifiable landscape geometry differs by interaction role and reference provenance.

If none of these are achieved, this branch remains an exploratory diagnosis and main is not rewritten retrospectively.
