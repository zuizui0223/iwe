# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Strict question

IWE strict H1 requires a plant-partner temporal-matching exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for a quantitative effect.

For `mixed_pollinating_seed_predator`, the primary H1 row must represent a final plant reproductive outcome after both benefit and cost can act in the focal biological unit. Benefit-only or cost-only channels are stored separately and are not substituted for net outcomes.

H2 is separate: it preregisters the possibility that mixed systems show a non-monotonic timing-fitness response. Shape evidence is therefore not forced into a single H1 slope when the source itself reports an interior optimum or peak.

## Current screened corpus

After source adjudication through IWE066:

| interaction type | screened | strict `include` | strict programmes quantitatively closed | unresolved possible strict | context/timing/channel-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 7 | 1 | 6 | 4 | 0 |
| antagonist | 22 | 0 | 0 | 1 | 18 | 3 |
| mixed pollinating seed predator | 27 | 1 | 1 | 1 | 24 | 1 |

IWE001–IWE040 are the discovery corpus. IWE041 onward are post-freeze records tracked in `prospective_search_log.csv`.

IWE001 remains the quantitatively closed mutualist programme, with three dependent Corydalis population effects.

**IWE064 is the first quantitatively closed mixed strict-H1 programme.**

## First closed mixed strict effect — IWE064

Gu et al. (2012), `Ficus curtipes × Eupristina sp.`, experimentally prevented natural fig-wasp entry and introduced a single pollinator after delays of 0, 4, 8, 12, 16, 20, 24 and >=28 days from the onset of receptivity.

`F. curtipes` is monoecious: seeds and pollinator galls occur in the same syconium, so final seed output is measured after the same pollinator has both delivered pollen and allocated ovules to pollinator larvae. This satisfies the mixed-system final-female-output rule.

Using source Table-1 mean seed counts, SDs and group sample sizes, IWE reconstructs a weighted log-linear seed-count slope:

- `beta_native = -0.03334257 log(seed count) / day mismatch`
- `SE = 0.00306271`
- `variance = 0.0000093802`

The pooled >=28-day category contains day-28, day-32 and day-36 figs. Deleting that entire category gives `beta=-0.03516954`, `SE=0.00381401`, so the registered slope is not driven by assigning a representative age to the pooled group.

## Closely related but not primary — IWE065

Zhang et al. (2012), `Ficus semicordata × Ceratosolen gravelyi`, also experimentally delayed single-pollinator entry and directly reports a Poisson seed-count slope in female syconia:

- `beta = -0.12`
- `SE = 0.002` per day of delay.

However, `F. semicordata` is dioecious. Female syconia produce seeds but do not rear pollinator offspring; the nursery cost occurs on male trees. The female seed slope therefore measures a **pollination-benefit channel**, not a same-unit net mixed outcome. It is stored separately and excluded from mixed H1 rather than reclassified post hoc as a pure mutualist.

## Direct preregistered H2 shape evidence — IWE066

Zhang et al. (2014), `Ficus altissima × Eupristina altissima`, experimentally introduced single freshly emerged pollinators into monoecious figs on days 1–5 after the figs became accessible. The same figs subsequently yielded both seeds and pollinator offspring.

The source reports:

- `n = 27, 25, 24, 23, 21` figs on days 1–5;
- **seed production peaked on days 2–3**, rather than on day 1;
- pollinator offspring remained relatively stable through day 4 and then fell rapidly;
- across days 1–5, Poisson GLM slopes were `-0.09 ± 0.01` for seeds and `-0.16 ± 0.01` for pollinator offspring.

Because day 1 is not the seed maximum, the overall negative linear seed slope is not re-labelled as a strict synchrony effect. IWE066 enters `shape_evidence.csv` as `interior_peak_then_decline` and directly supports the preregistered H2 shape lane.

A formal quadratic coefficient/turning-point interval is **not** reconstructed because the paper text does not print day-specific seed means and uncertainties from Figure 4, and the current environment did not provide a sufficiently reproducible numerical figure extraction. The claim remains an experimentally observed interior peak, not a quantified quadratic meta effect.

## Remaining strict bridges

### Mutualist

IWE008 (Qilian 2024) directly measures flowering peaks, key-pollinator peaks and individual seed setting with mismatch direction retained. The design is strict-eligible but a recoverable quantitative coefficient plus variance remains unavailable from public sources.

### Antagonist

IWE035 (wild `Helianthus annuus`) remains the only antagonist `unresolved_strict` bridge: seasonal abundance/damage of seed-feeding herbivores and plant fitness occur together, but a common synchrony coefficient plus sampling variance is still missing.

### Mixed

IWE059 (`Ficus pertusa ×` pollinating fig wasps) remains unresolved-strict. It combines crop receptivity/attractiveness timing, temporal pollinator abundance, visitation, seeds per fig and wasp production, but a registered crop-level timing effect plus variance has not yet been recovered.

## Measurement asymmetry remains, but mixed is no longer empty

The controlled Ficus experiments change the diagnosis from `mixed strict effects absent` to `mixed strict effects rare but demonstrably recoverable`.

The broader asymmetry remains:

- mutualist mismatch studies relatively often measure plant timing + partner timing + final reproduction;
- antagonist studies usually measure flowering date plus attack/predation/selection, or nonlinear enemy windows;
- mixed nursery-pollination studies usually separate partner timing from final net plant fitness, with controlled monoecious fig experiments providing rare exceptions.

A naive three-class pooled analysis would still confound interaction role with measurement design unless the systematic search recovers more comparable antagonist and mixed effects.

## Nonlinear timing evidence

### Antagonist discovery lane

Three antagonist systems provide direct timing plus final-fitness evidence that is not represented well by one slope:

- `Geum urbanum × Byturus ochraceus`: intermediate off-peak flowering optimum under predation;
- `Cardamine pratensis × Anthocharis cardamines`: temporal refugia on both sides of the butterfly flight period;
- `Erigeron glaucus × Tephritis ovatipennis`: viable seed success lowest at intermediate flowering synchrony.

This antagonist pattern was recognized after outcome screening and remains discovery evidence subject to the prospective holdout rule.

### Mixed preregistered H2 lane

IWE066 supplies direct experimental mixed-system shape evidence because H2 was preregistered before the study was found. It does not validate the separate post-hoc antagonist shape hypothesis, and it does not yet provide a numerical curvature coefficient.

## Prior-art boundary

Munguía-Rosas et al. (2011) already meta-analyzed selection on flowering time and among-plant flowering synchrony, and its supplement separately summarizes pre-dispersal seed predation in relation to flowering time. IWE does not claim novelty for generic flowering-phenology meta-analysis or for showing that seed predators select on flowering date.

IWE's narrower target is:

> plant–interaction-partner temporal matching -> final plant reproductive fitness,

using comparable timing estimands where the published measurements allow it, with interaction role as moderator.

## Valid paper endpoints

1. **Strict meta-analysis endpoint:** enough comparable strict effects are recovered for one or more interaction classes.
2. **Evidence-architecture endpoint:** strict effects remain highly uneven across classes; IWE reports the measurement asymmetry, meta-analyzes estimable effect families/lanes, and separately synthesizes timing/shape/channel evidence without treating them as equivalent.

## Next falsification priorities

1. Complete the frozen backward/query/forward/citation closure.
2. Recover or close IWE035 to determine whether any antagonist strict effect can be obtained.
3. Recover IWE008 quantitative effects to expand the mutualist lane beyond one Corydalis programme.
4. Recover IWE059 quantitatively to determine whether the mixed strict lane can replicate beyond IWE064.
5. Search for additional mixed H2 studies with group-level numerical timing-fitness data so non-monotonicity can be tested quantitatively rather than narratively.
6. Do not pool `log_rate_slope_per_day`, Fisher-z, SMD or generic log-response-ratio effects without a separately frozen common-scale conversion.
