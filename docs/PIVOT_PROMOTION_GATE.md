# IWE pivot promotion gate

Date: 2026-10-02  
Applies to: `pivot/interaction-window-landscape`  
Status: prospective gate for deciding whether the pivot should replace or only supplement the original strict-H1 framing.

## Central candidate principle

The pivot is not promoted merely because signed flowering-time selection differs among studies.

The stronger ecological hypothesis is:

> Biotic interactions may look idiosyncratic on an absolute calendar axis, but become more predictable when plant phenology is expressed relative to the effective interaction window.

The proposed geometry is:

- mutualist: selection/fitness tends to pull plant timing toward an effective service window;
- antagonist: selection/fitness tends to favor temporal escape from an effective cost window;
- mixed pollinating seed predator: benefit and cost windows can overlap imperfectly, producing displacement, asymmetry, or curvature in net fitness.

Calendar early/late is therefore a diagnostic coordinate, not the final generalizing coordinate.

## Why this gate is needed

The pilot already contains opposite calendar signs within the antagonist class:

- Gentiana–Phengaris shifts selection toward later flowering;
- Gymnadenia herbivory shifts selection toward earlier flowering;
- Lythrum simulated damage shifts selection toward earlier flowering.

It also contains coordinate-specific mutualist effects in Arabidopsis, where pollinators affect flowering start and flowering end differently.

These results are sufficient to reject a naive universal calendar-direction rule, but they do not yet prove convergence after window alignment.

## Promotion tests

### P1 — complete signed-search universe before class-level claims

The Caruso 2019 non-duplicated flowering-phenology treatment-pair universe must be screened with the signed-rescreen contract before a general statement about the frequency or direction of agent-induced selection shifts.

All eligible contrasts are retained, including nulls and sign patterns that contradict the pivot.

The duplicated Caruso workbook is dependence-audit material only.

### P2 — preserve phenology coordinates

Flowering start, peak, end, duration, and other phenology coordinates are not pooled merely because all can be oriented as early versus late.

A common quantitative pool requires a biologically homologous coordinate or an explicit multivariate/hierarchical model.

### P3 — window provenance remains explicit

Every programme used for the window-relative test is assigned one of the existing window-reference classes:

- independent_partner_activity;
- realized_interaction_window;
- historical_partner_window;
- seasonal_position_only;
- direct_interaction_manipulation.

Only the first class can by itself support a claim about independently identified partner availability.

### P4 — direct alignment test

The key confirmatory comparison is not whether calendar signs differ.

For programmes with sufficient timing data, fit or reconstruct effects on the most resolved stage-specific coordinates the source supports:

1. an absolute calendar/seasonal timing coordinate;
2. an independently measured adult partner/service window;
3. a realized encounter or oviposition window;
4. a delayed consumer window after development;
5. an **effective interaction-window coordinate** after host-stage filtering determines which exposure events can actually contribute to final reproduction.

Then ask whether biologically relevant between-programme heterogeneity is reduced as the coordinate moves from calendar timing toward the biologically effective stage-specific window.

The Cardamine source demonstrates why raw exposure and effective cost are not interchangeable: the Gaussian peak for total egg exposure occurs at flowering-date z = -1.10, while the peak for active eggs capable of reaching damaging late instars occurs at z = -0.61 and has a narrower sigma (0.66 versus 0.92).

Cardamine now also provides a positive final-fate phase contrast independent of Figure 4. The early ecotype has a longer flowering-to-oviposition interval than the late ecotype (11.50 versus 5.72 d), and among plants bearing final-instar larvae 34% versus 4% dehisce before larval completion (overall fate chi-square(df=2)=11.95, p=0.003). The remaining IWE032 blocker is therefore not whether stage phase matters to final fate; it is the numeric adult-flight coordinate required to compare adult-only versus stage-specific explanatory geometry on the same programme.

Kula 2012 adds the mixed-system analogue. In *Silene stellata–Hadena ectypa*, flowering × oviposition synchrony predicts **more** predation in 2008 but **less** predation in 2009. First-flower/egg-to-**first detected mobile larva** delays change from 10/5 d to 17/15 d, while the mean flower-marking-to-fruit-collection interval changes from 21.3 ± 0.28 SE to 16.7 ± 0.40 SE days. A descriptive detection margin changes from **-11.3 d to +0.3 d**. However, the 2009 maturation-only ±2SE range (**-0.50 to +1.10 d**) spans zero, larvae were observed after beginning inter-flower movement under a 2–4-day survey schedule, and initial feeding time was not measured. Therefore this does **not** establish that fruits matured before larval damage or identify a safe threshold. The signed predation reversal remains observed; developmental lag remains a candidate explanation and a coordinate for independent validation.

An independent Portuguese Gentiana-Phengaris programme additionally shows that offspring survival varies with host bud size, bud developmental stage, and oviposition period, while Yucca-Tegeticula provides a taxonomically distinct filter in which resource-driven flower abortion kills all eggs in exposed flowers. These replicate host-state filtering at the mechanism level but do not yet test final plant-fitness convergence.

The architecture of stage separation is replicated across independent systems, but **predictive superiority of stage matching remains unproven**. In Parkinsonia-Penthobruchus (seven region-season units), annual egg density gives leave-one-**region**-out RMSE **20.58 pp**, stage-matched density **19.93 pp**, and stage-matched density filtered by observed parasitism and hatch **4.92 pp**. An additional outcome-exposed exploratory ablation shows that nonparasitized × hatch fraction **alone** gives RMSE **4.11 pp**, without timing or egg-density information. The apparent gain therefore cannot be assigned to stage matching. The full 10-model comparison is explicitly non-confirmatory because it was added after inspecting the same outcomes, with n=7 and no independent adult timing. **Table 5 additionally measures parasitism/hatch and final seed predation on the same late-collected pods**; these are contemporaneous diagnostic components, not separately observed prospective predictors. A source with independently dated pre-outcome filter measurements is still required for a predictive confirmation. Posledovich 2015 is a direct boundary: experimental stage matching and temperature change herbivore performance, yet the mature-seedpod escape endpoint depends only on host species. The 21-year Lathyrus series likewise shows climate-driven movement in the phenology–seed-predation relationship without a corresponding effect of that covariance on flowering-time selection. No claim of "collapse", "convergence", or "effective-window superiority" is allowed without paired comparisons satisfying the full timing-provenance contract.

### P5 — effective windows cannot be defined circularly

An effective interaction window may be estimated from a pre-fitness mechanistic filter such as stage-specific attack survival, successful pollen transfer, experimentally identified host sensitivity, or a measured delay distribution from adult encounter/oviposition to the damaging consumer stage.

It may **not** be defined by choosing the timing transformation that maximizes the final fitness association in the same data.

Whenever possible, the filter defining the effective window must be estimated independently of the final reproductive response or validated in a separate component of the study.

Effective-window filters can be host-side or post-exposure consumer-side. Host-side filters include tissue maturation, abortion and developmental vulnerability. Consumer-side conversion filters include egg hatch, parasitoid escape or stage survival before damage is expressed. The latter are admissible only when fixed from pre-final source measurements rather than selected to optimize the final-fitness fit.

The filter itself may be interaction-dependent. Lathyrus-Bruchus shows antagonist targeting of fruits likely to survive abortion, whereas Rheum-Bradysia shows oviposition-associated physiological modification that reduces abortion before larvae hatch. Effective-window definitions must preserve these feedbacks rather than treating host vulnerability as a fixed calendar function.

### P6 — mixed systems remain a distinct geometry test

Mixed pollinating seed predators are not forced into the mutualist or antagonist sign rule.

Where benefit and cost channels can be separated, preserve:

`W_net(tau) = B(tau) - C(tau)`.

A mixed-system result is informative if the net optimum is displaced from the partner-activity maximum or if benefit and cost surfaces peak at different relative times.

For stage-structured partners, the cost surface is not anchored automatically to adult activity or oviposition. Consumer developmental lag and host maturation must be preserved prospectively. A particularly strong test is a sign change in the relationship between adult/oviposition synchrony and later cost that is predicted by a measured shift in the adult-to-consumer phase lag.

### P6b — redundancy claims require temporal accessibility

A redundancy-buffer claim cannot use partner richness alone.

When alternative partners are proposed to buffer mismatch, the relevant quantity is their effective overlap with the receptive plant window. Senita cactus is the motivating boundary: diurnal bee co-pollinators are unavailable when flowers close before sunrise, and a gap between senita-moth cohorts coincides with zero open-pollinated fruit set despite the broader pollinator community.

Redundancy evidence is therefore classified separately from the core raw-window/effective-window convergence test and is not counted as proof of that convergence.


### P7 — null and boundary systems are mandatory

The evidence map must retain systems in which:

- interaction manipulation changes fitness but not flowering-time selection;
- antagonist damage does not alter selection;
- pollination changes non-phenological traits but not phenology;
- timing effects exist without a defensible interaction window;
- alternative mechanisms produce similar final fitness despite very different positions relative to an antagonist window;
- stage matching strongly affects consumer performance but not the final plant reproductive endpoint;
- climate or other drivers move the phenology–interaction relationship without moving the resulting plant selection gradient.

Registered boundaries now include *Ulex europaeus* (temporal escape vs predator satiation), Posledovich 2015 (developmental matching affects larvae but not mature-seedpod escape), and the 21-year *Lathyrus* series (climate changes phenology–seed-predation covariance without changing selection through that pathway).

These are not failed studies. They are necessary tests of whether the proposed window rule is selective rather than tautological. Boundary rows are not counted as programmes supporting the window-relative prediction.

### P8 — dependence and uncertainty are not relaxed

Repeated years, sites, traits, or contrasts from one programme share the appropriate dependence cluster.

A signed contrast without defensible SE/covariance can be reported with its source interaction test or interval, but cannot be made inverse-variance-ready by assuming zero covariance.

The existing CR2 minimum-information rule remains the inferential gate for any pooled class estimate.

## Prospective prediction identification

**The strict paired-model interpretation requirements are now separated in `docs/PROSPECTIVE_PREDICTION_IDENTIFICATION_GATE.md`.** A positive stage/final-fate correlation, a retrospective region-blocked reconstruction and a prospective forecast are not equivalent evidence.

Parkinsonia's egg survival fractions and final seed fate were assessed in the same late pod collections, and its strongest observed survival-only model was selected after inspecting those outcomes. It cannot close the prospective predictive-superiority gate, regardless of its low region-blocked descriptive RMSE.

For promotion, require a genuinely pre-outcome conversion/stage coordinate and an outcome-unseen comparison against **both** upstream adult/host timing **and** the survival/filter-only comparator, with independent temporal or spatial validation.

## Branch decision rule

### Promote the pivot toward the main IWE paper if

the expanded signed evidence continues to show substantial calendar-sign/coordinate heterogeneity **and** multiple independently replicated programmes with identifiable interaction windows support a more coherent window-relative interpretation.

### Retain as a secondary analysis if

signed selection shifts are common but too few studies identify the interaction window to test whether re-alignment explains the heterogeneity.

### Abandon as the main framing if

the broader outcome-complete rescreen shows that the apparent calendar-sign heterogeneity was a pilot artifact, or if window alignment does not improve biological interpretability beyond generic seasonal timing.

## Immediate empirical priorities

1. complete IWE002 directional reconstruction without counting it as independent from IWE001;
2. resolve IWE015 raw variance for the mixed net-fitness anchor;
3. recover IWE032 female-flight dates and compare the adult-flight coordinate with the already-positive stage-specific evidence: active-egg effective window plus the 11.50-vs-5.72 d ecotype phase contrast that predicts 34%-vs-4% dehiscence before larval completion;
4. The **stage chain itself is now independently replicated**, with one positive paired realized comparison and direct nulls. Cardamine closes exposure -> active-consumer filtering -> final reproduction; Parkinsonia shows within the same seven region-season units that stage-matched and pre-final filtered exposure predicts final seed loss better than annual exposure; Glochidion-Epicephala documents an ~8-month adult-service to larval-cost separation; Trollius-Chiastocheta links flower age to the marginal benefit/cost balance; Kula 2012 shows phase-lag-associated sign reversal in predation. But Posledovich 2015 and the long-term Lathyrus analysis show that stage/timing effects need not propagate to final plant selection. The remaining stronger gate is therefore narrower: an **independent programme with source-backed adult/raw timing in which phase alignment varies and predicts final post-cost plant reproduction better than the simpler adult/calendar coordinate**;
5. treat the Hurlburt *Yucca glauca–Tegeticula* route as a one-key completion problem: adult timing and mature seed output are source-backed; inspect the public thesis only for a marked clone/inflorescence/flowering-date -> mature-fruit join;
6. ingest and screen the Caruso non-duplicated phenology treatment-pair database when lawful file access is available;
7. retain design-matched null/boundary systems and test overlap-conditioned redundancy rather than static partner richness.

This gate deliberately makes the hardest claim — window-relative convergence — contingent on data that have not yet been inspected under that comparison.
