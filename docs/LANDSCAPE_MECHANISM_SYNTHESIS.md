# Interaction-window landscape: exposure, sensitivity, and mixed-channel timing

Date: 2026-10-02  
Status: empirical synthesis for the pivot branch.

## Revised biological object

The first pivot formulation defined a fitness landscape over relative timing:

`W(tau)`, where `tau` is plant timing relative to an interaction window.

The expanded audit shows that a single “partner window” is still too simple.

Observed fitness consequences can arise from two separable temporal components:

1. **partner exposure** — when the interacting animal is available or when realized attack/pollination occurs;
2. **host sensitivity** — how much the same interaction changes final plant fitness at a given plant stage.

We therefore treat the realized timing effect as:

`impact(t) = f(exposure(t), host_sensitivity(t))`

This is a bookkeeping decomposition, not a claim that the two quantities multiply.

## Evidence already present in IWE

### Mutualist exposure mismatch — IWE001

On the plant-earlier side of the *Corydalis–Bombus* system, larger lead before bee detection is associated with lower natural seed set at all three sites with estimable one-sided correlations.

This primarily identifies the partner-exposure side of the problem.

### Antagonist-induced slope reversal — IWE012

In *Gentiana–Phengaris*, predator presence changes flowering-time selection in both years, while earlier flowering strongly predicts attack.

This shows that a time-structured antagonist cost can rotate or reverse the net seasonal fitness slope.

### Host-stage vulnerability — IWE031

Timed monarch herbivory shows that the same antagonist interaction has endpoint-specific effects depending on plant age: late herbivory is most damaging to viable-seed production even though early herbivory most strongly affects plant size.

This identifies host sensitivity independently of a natural partner activity curve.

### Mixed benefit-cost decoupling — IWE014

Early and late *Silene vulgaris* plants have similar pollination success but different seed-predation costs, with higher predation early.

The benefit and cost channels therefore do not share one temporal response.

### Strong direct mixed anchor — IWE015

Early and late experiments are independently ordered by *Hadena ectypa* activity and successful fruits are post-predation final reproduction. Once the raw variance audit is closed, this is the strongest route for connecting partner exposure to a mixed net-fitness outcome.

### Host filtering of antagonist exposure — IWE032

*Cardamine pratensis × Anthocharis cardamines* supplies a direct quantitative demonstration that raw exposure and effective fitness cost can occupy different temporal windows.

The paper reports Gaussian flowering-date curves for total egg load and for "active" egg load, where active eggs are laid early enough after flowering to produce damaging late-instar larvae:

- total-egg peak: z = -1.10, sigma = 0.92;
- active-egg peak: z = -0.61, sigma = 0.66.

Thus host-stage filtering moves the effective antagonist peak **+0.49 flowering-date SD later** and narrows the effective window by **28.3%**. The plant does not experience every oviposition event as an equivalent future reproductive cost.

This is the clearest current quantitative evidence for the decomposition `impact(t) = f(exposure(t), host_sensitivity(t))`.

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

In nursery-pollination systems, pollination benefit and offspring-mediated reproductive cost need not peak together or change at the same rate. The net optimum depends on their relative timing and amplitude, not merely on total synchrony.

### G5 — endpoint choice changes the apparent window

Timing effects on plant size, fruit initiation, viable seeds, and final post-predation reproduction are not interchangeable. Primary inference should privilege final reproduction while intermediate endpoints diagnose mechanism.

## Consequence for analysis

The project should not attempt one universal meta-analytic coefficient yet.

The next empirical product is a **mechanism-resolved evidence map plus homologous within-family quantitative contrasts**:

- directional mismatch correlations where signed-lag raw data exist;
- predator-presence × flowering-time selection shifts;
- controlled early/mid/late interaction-timing contrasts;
- mixed benefit and cost channels kept separate before deriving net reproduction;
- strict independent-partner-window effects retained as the highest-provenance subset.

This framing preserves the original causal discipline while using the antagonist and mixed literature for the biological quantities it actually measures.
