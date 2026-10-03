# Interaction-window landscape: exposure, sensitivity, and mixed-channel timing

Date: 2026-10-02  
Status: empirical synthesis for the pivot branch.

## Revised biological object

The first pivot formulation defined a fitness landscape over relative timing:

`W(tau)`, where `tau` is plant timing relative to an interaction window.

The expanded audit shows that a single “partner window” is still too simple.

Observed fitness consequences can arise from three separable temporal components:

1. **partner exposure** — when the focal interacting animal is available or when realized attack/pollination occurs;
2. **host sensitivity** — how much the same interaction changes final plant fitness at a given plant stage;
3. **accessible redundancy** — which alternative partners are simultaneously active and able to access receptive plant structures.

We therefore treat the realized timing effect as:

`impact(t) = f(exposure(t), host_sensitivity(t), accessible_redundancy(t))`

This is a bookkeeping decomposition, not a claim that the quantities multiply.

## Evidence already present in IWE

### Mutualist exposure mismatch — IWE001

On the plant-earlier side of the *Corydalis–Bombus* system, larger lead before bee detection is associated with lower natural seed set at all three sites with estimable one-sided correlations.

This primarily identifies the partner-exposure side of the problem.

### Antagonist-induced slope reversal — IWE012

In *Gentiana–Phengaris*, predator presence changes flowering-time selection in both years, while earlier flowering strongly predicts attack.

This shows that a time-structured antagonist cost can rotate or reverse the net seasonal fitness slope.

### Host-stage vulnerability — IWE031

Timed monarch herbivory experimentally shifts the same antagonist interaction among 60-, 74-, and 88-day-old milkweed plants. Late herbivory is most damaging to viable-seed production even though early herbivory most strongly affects plant size.

The study therefore independently links **host-stage sensitivity to final reproduction** under direct interaction-timing manipulation. Because realized foliage removal is itself measured and can vary along the treatment pathway, this is not interpreted as equal damage applied at three dates. It identifies the causal effect of interaction timing without reconstructing a natural partner activity curve.

### Mixed benefit-cost decoupling — IWE014

Early and late *Silene vulgaris* plants have similar pollination success but different seed-predation costs, with higher predation early.

The benefit and cost channels therefore do not share one temporal response.

### Independent mixed service window — Althoff 2005

In *Yucca filamentosa × Tegeticula cassandra*, adult pollinator activity was measured through the same flowering seasons as plant phenology and relative fruit set.

The source path analysis is replicated across years:

- peak flowering date -> pollinator/day = **-0.37** in 2001 and **-0.27** in 2002;
- pollinator/day -> relative fruit set = **+0.60** in 2001 and **+0.48** in 2002.

Thus later flowering moves plants away from the effective pollinator-service window and reduces the positive channel of the mixed interaction. Because relative fruit set precedes larval seed consumption, this is benefit-channel evidence rather than net mixed fitness.

### Accessible redundancy — senita cactus

The *Lophocereus schottii–Upiga virescens* programme shows why alternative-pollinator richness cannot be treated as a fixed buffer.

Pollinator-exclusion experiments show that senita moths and diurnal bees can both contribute under some flowering conditions, but their effective availability is time dependent. In hot late seasons, flowers close before sunrise and physically exclude diurnal bees. In July 1998, senita moths were between adult cohorts; open-pollinated flowers produced **0% fruit**, while pollen-supplemented flowers produced **22.5 +/- 6.6%**.

This motivates:

`R_eff(t) = sum_j I(partner_j active at t AND able to access receptive flowers at t)`.

The mechanism is stronger than generic partner redundancy: a community can contain alternative pollinators yet have zero effective redundancy at the focal plant window.

### Developmental phase lag separates adult benefit from offspring cost — Kula 2012

The 2008–2009 *Silene stellata–Hadena ectypa* experiment provides a direct within-system test of why adult synchrony cannot stand in for the later seed-predation window.

Individual plant flowering was combined with the seasonal oviposition curve to calculate synchrony. Synchrony did not alter initiated fruit set in either year, but its relationship with flower/fruit predation reversed:

- 2008: higher synchrony -> higher predation, chi-square = **46.47**, p < 0.0001;
- 2009: higher synchrony -> lower predation, chi-square = **16.74**, p < 0.0001.

The phase relationship changed sharply. First flowering and first egg preceded first larval observation by only **10 and 5 days** in 2008, compared with **17 and 15 days** in 2009. Fruit maturation was also faster in 2009 (**16.7 ± 0.40 d** versus **21.3 ± 0.28 d**).

Thus plants highly synchronized with adult oviposition in 2009 could mature and harden fruits before large larvae became abundant. The adult/oviposition window and the damaging larval window are therefore temporally distinct biological objects.

Conceptually:

`effective cost window = exposure window ⊗ consumer developmental lag × host vulnerability`.

This is not a fitted convolution in the current analysis. It is the mechanistic bookkeeping required by the source data.

### Independent mixed timing gradient — Trollius–Chiastocheta

The globeflower system provides an independent way to expose the same stage problem. Different *Chiastocheta* species oviposit at different flower ages, from the first day of flowering through day 7 and even after flowering.

Pellmyr's cost-benefit analysis shows why timing matters. Each visit fertilizes a fixed proportion of the ovules that remain unfertilized, so marginal pollination benefit declines as the flower ages. Larval seed consumption does not decline in parallel. The estimated benefit-cost break-even occurs around **4–5 eggs per flower**, while natural annual means span **2.3–7.25 eggs per flower**.

Thus moving the adult interaction later in host development lowers the marginal service component while preserving offspring cost. The stage-specific benefit-cost ratio is therefore observable in a second, independent nursery-pollination system.

### Extreme annual phase lag — Glochidion–Epicephala

*Glochidion lanceolarium × Epicephala lanceolaria* provides a much larger temporal scale.

Adult moths pollinate and oviposit in **April–May**. Developing fruits and eggs then remain dormant from **May through December**. Fruits reactivate in **January–February**, eggs hatch, and larvae consume developing seeds. Adults eclose in mature fruit in **March–April**, just before the next flowering season.

The adult service and offspring cost windows are therefore separated by roughly **eight months**. Mature intact and infested seed counts are directly reported across four populations.

This system does not estimate a treatment effect of phase lag, so it is registered as `stage_structure_evidence`, not as a supporting fitness-landscape programme. Its value is generality: stage separation occurs from days (Silene) to months (Glochidion).

### Strong direct mixed anchor — IWE015

Early and late experiments are independently ordered by *Hadena ectypa* activity and successful fruits are post-predation final reproduction. Once the raw variance audit is closed, this is the strongest route for connecting partner exposure to a mixed net-fitness outcome.

### Host filtering of antagonist exposure — IWE032

*Cardamine pratensis × Anthocharis cardamines* supplies a direct quantitative demonstration that raw exposure and effective fitness cost can occupy different temporal windows.

The paper reports Gaussian flowering-date curves for total egg load and for "active" egg load, where active eggs are laid early enough after flowering to produce damaging late-instar larvae:

- total-egg peak: z = -1.10, sigma = 0.92;
- active-egg peak: z = -0.61, sigma = 0.66.

Thus host-stage filtering moves the effective antagonist peak **+0.49 flowering-date SD later** and narrows the effective window by **28.3%**. The plant does not experience every oviposition event as an equivalent future reproductive cost.

This is the clearest current quantitative evidence for the decomposition `impact(t) = f(exposure(t), host_sensitivity(t))`.

The source also closes the chain to final plant reproduction. Using its own Equation 1, observed intact-RU fractions, fifth-instar survival `L = 0.22`, and phenotype-specific active-egg Gaussians, the predicted fitness trough occurs at the effective cost-window center. Relative to the no-active-larva baseline, the reconstructed trough is **29.98% lower for high-fecundity ramets** and **13.72% lower for medium-fecundity ramets**.

This is the first IWE programme where a host filter defined before final fitness is quantitatively propagated to final reproduction.

### Independent host-filter replication — Arnaldo 2014

A geographically independent Portuguese *Gentiana pneumonanthe–Phengaris alcon* programme follows the same causal layer without using final plant fitness to define the filter. Across 127 shoots and 837 eggs, egg deposition varies over three flight-period intervals, while offspring survival depends on flower-bud size, flower developmental stage, and oviposition period.

The reported survival-model coefficients include +0.350 for bud length, -1.088 for flower developmental stage, -0.881 for period 2 versus period 1, and -0.536 for period 3 versus period 1.

This does **not** imply that host filtering has the same direction in all systems. Instead it independently supports the more general mechanism:

> the mapping from raw antagonist exposure to biologically effective cost is conditional on host phenological state.

Because this study measures butterfly offspring performance rather than final plant reproduction, it remains mechanism-only evidence.


### Taxonomically distinct host-allocation filter — Jadeja 2017

The *Yucca glauca–Tegeticula yuccasella* nursery-pollination mutualism provides a third architecture. *Yucca* flowers open sequentially, and late distal flowers become more likely to abort when already initiated basal fruits are present. Every moth egg inside an aborted flower dies.

Here the host filter is not larval survival conditional on tissue age. It is a plant resource-allocation decision that removes an entire realized interaction after oviposition.

Together, Cardamine, Portuguese Gentiana and Yucca show three distinct mechanisms by which host state changes the mapping from raw interaction events to effective future cost:

1. developmental timing determines whether predator offspring remain active;
2. tissue developmental state changes offspring performance;
3. host resource allocation deletes exposed reproductive units entirely.

This satisfies the branch's first taxonomic-breadth milestone for **host filtering as a mechanism**, but none of the mechanism-only replications should be counted as final plant-fitness effect sizes.

### Host filters can be anticipated or manipulated

Two additional systems show that host filtering is not necessarily an exogenous plant-only layer.

In *Lathyrus vernus–Bruchus atomarius*, late/distal fruits are more likely to abort, but females preferentially oviposit on fruits with lower future abortion probability. The observed selective pattern produces more developed beetles than a random allocation scenario (**2.84 ± 0.14 vs 2.02 ± 0.11**) and lowers average intact-seed output relative to random oviposition.

In *Rheum nobile–Bradysia*, the feedback goes further: oviposition itself strongly reduces fruit abortion (**F = 287.24, p < 0.001**) and elevates IAA before larvae hatch (**oviposition F = 355.97; oviposition × day F = 140.82; both p < 0.001**). Flowering sequence does not explain the abortion or oviposition patterns.

The effective host filter can therefore be predicted, circumvented or physiologically modified by the interacting animal.

### Boundary: stage matching can matter to the consumer but not the plant endpoint

Posledovich 2015 experimentally varies host phenological stage at oviposition and temperature during development. These manipulations alter larval performance and the developmental race, but the probability that the initial host outgrows the larva and forms mature seedpods depends only on host species identity.

The 21-year *Lathyrus* series supplies a natural long-term analogue. Spring temperature changes the sign and strength of the flowering-phenology–seed-predation relationship, but the yearly covariance between flowering date and seed predation does not explain flowering-time selection on intact-seed fitness (**estimate -0.033, 95% CI -0.101 to +0.037**).

These are mandatory nulls against turning a mechanistically sensible stage coordinate into an automatic final-fitness predictor.

### Independent antagonist escape tradeoff — Sercu 2020

A separate *Geum urbanum–Byturus ochraceus* programme shows that temporal escape need not drive plants toward an extreme calendar date. Predation occurred almost exclusively during the first flowering peak, while later flowers had intrinsically lower seed output. Among predated plants, final total seed mass was therefore maximized at an intermediate strategy: about **36% of flowers in the second flowering peak**.

The flower-level model also shows why the optimum is internal. In unpredated plants, seed mass declined by **0.0027 g per day** (SE 0.0002), while predation reduced early-flower seed mass by **0.11 g** (SE 0.025) and weakened the seasonal decline through a positive predation × date interaction of **0.0013 g per day** (SE 0.00027). Plants exposed to more predation subsequently shifted more flowering into the second peak in the following year (95% credible interval for the lagged slope 0.00043–0.01526).

This is registered as a realized interaction window rather than independently measured adult beetle availability. It independently links antagonist-window escape to final plant fitness and demonstrates a key boundary condition: **escape itself can have a cost, producing an interior temporal optimum rather than “later is always better.”**

### Boundary: temporal escape is not the only avoidance route — Atlan 2010

A common-garden *Ulex europaeus* system provides a deliberately retained boundary case. Long-flowering plants placed more reproduction before the main seed-predation peak, whereas short-flowering plants reproduced during the peak but partly reduced attack through density-dependent predator satiation.

Despite those contrasting routes, whole-season pod infestation was approximately **29% in long-flowering plants and 30% in short-flowering plants**, and maternal flowering type did not significantly alter annual pod or seed production.

This prevents a timing-only version of G2. Moving away from an antagonist window can be advantageous, but its final-fitness value depends on whether plants possess alternative avoidance mechanisms such as predator satiation. Window position therefore needs ecological moderators, not just a universal distance-from-enemy rule.

### Strong direct antagonist anchor — IWE032

The same Cardamine programme also provides independently measured female butterfly flight plus plant trajectories to dehiscence and a predeclared early/core/late analysis. Recovering the numeric 2012–2014 female capture/recapture timing object would connect the highest-provenance adult-exposure axis to both temporal escape directions.

The active-egg result above does **not** substitute for that missing adult-flight object; the two components remain separately registered.

## Revised hypotheses

### G1 — service-window decline

For mutualists, reproductive benefit declines as plant timing moves away from an effective partner-service window, but early and late mismatch need not be symmetric.

### G2 — antagonist impact windows are composite

A reproductive-cost window can be created by high partner exposure, high host sensitivity, or their coincidence. Therefore the strongest cost need not occur at the adult antagonist activity peak.

### G3 — antagonists can rotate the seasonal fitness slope

If attack is concentrated on one side of the flowering distribution, antagonist presence can move or reverse the net temporal optimum.

### G4 — mixed benefit and cost channels can be phase-decoupled

In nursery-pollination systems, pollination benefit and offspring-mediated reproductive cost need not peak together or change at the same rate. When the adult provides pollination and delayed offspring consume reproductive tissues, developmental lag can move the damaging window relative to the adult service window and can even reverse the sign of an adult-synchrony effect on cost.

The net optimum therefore depends on relative timing, developmental lag, host vulnerability and amplitude of the two channels, not merely on total synchrony. Trollius adds a host-stage gradient in marginal benefit, while Glochidion demonstrates that adult service and larval cost can be separated by most of a year.

### G5 — endpoint choice changes the apparent window

Timing effects on plant size, fruit initiation, consumer performance, mature seedpods, viable seeds, and final post-predation reproduction are not interchangeable. Primary inference should privilege final reproduction while intermediate endpoints diagnose mechanism.

A stage coordinate that improves prediction of larval performance does not automatically improve prediction of plant fitness.

### G6 — redundancy is a temporal overlap property

Mismatch buffering depends on alternative partners whose activity windows actually overlap the receptive plant window. Partner richness alone is insufficient when alternative partners are inactive, developmentally unavailable, or physically excluded by the plant's daily flowering schedule.

### G7 — host filters are interaction-dependent

Host retention and vulnerability can change in response to consumer targeting or partner-induced physiological modification. Effective-window reconstruction should therefore preserve whether the filter is:

- plant-intrinsic;
- predicted/circumvented by the antagonist;
- modified by the interaction itself.



## Consequence for analysis

The project should not attempt one universal meta-analytic coefficient yet.

The next empirical product is a **mechanism-resolved evidence map plus homologous within-family quantitative contrasts**:

- directional mismatch correlations where signed-lag raw data exist;
- predator-presence × flowering-time selection shifts;
- controlled early/mid/late interaction-timing contrasts;
- mixed benefit and cost channels kept separate before deriving net reproduction;
- time-indexed accessible redundancy kept separate from static partner richness;
- strict independent-partner-window effects retained as the highest-provenance subset.

This framing preserves the original causal discipline while using the antagonist and mixed literature for the biological quantities it actually measures.
