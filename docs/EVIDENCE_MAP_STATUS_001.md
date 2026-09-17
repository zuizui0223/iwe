# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Strict question

IWE strict H1 requires a plant-partner temporal-matching exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for a quantitative effect.

For `mixed_pollinating_seed_predator`, the primary row must represent a final plant reproductive outcome after both benefit and cost can act in the focal biological unit. Benefit-only or cost-only channels are stored separately and are not substituted for net outcomes.

## Current screened corpus

After source adjudication through IWE065:

| interaction type | screened | strict `include` | strict programmes quantitatively closed | unresolved possible strict | context/timing/channel-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 7 | 1 | 6 | 4 | 0 |
| antagonist | 22 | 0 | 0 | 1 | 18 | 3 |
| mixed pollinating seed predator | 26 | 1 | 1 | 1 | 24 | 0 |

IWE001–IWE040 are the discovery corpus. IWE041 onward are post-freeze records tracked in `prospective_search_log.csv`.

IWE001 remains the quantitatively closed mutualist programme, with three dependent Corydalis population effects.

**IWE064 is now the first quantitatively closed mixed strict-H1 programme.**

## First closed mixed strict effect — IWE064

Gu et al. (2012), `Ficus curtipes × Eupristina sp.`, experimentally prevented natural fig-wasp entry and introduced a single pollinator after delays of 0, 4, 8, 12, 16, 20, 24 and >=28 days from the onset of receptivity.

`F. curtipes` is monoecious: seeds and pollinator galls occur in the same syconium, so final seed output is measured after the same pollinator has both delivered pollen and allocated ovules to pollinator larvae. This satisfies the mixed-system final-female-output rule.

Using the source Table-1 mean seed counts, SDs and group sample sizes, IWE reconstructs a weighted log-linear seed-count slope:

- `beta_native = -0.03334257 log(seed count) / day mismatch`
- `SE = 0.00306271`
- `variance = 0.0000093802`

It is stored as `log_rate_slope_per_day`, not as a generic two-group log response ratio.

## Closely related but not primary — IWE065

Zhang et al. (2012), `Ficus semicordata × Ceratosolen gravelyi`, also experimentally delayed single-pollinator entry and directly reports a Poisson seed-count slope in female syconia:

- `beta = -0.12`
- `SE = 0.002` per day of delay.

However, `F. semicordata` is dioecious. Female syconia produce seeds but do not rear pollinator offspring; the nursery cost occurs on male trees. The female seed slope therefore measures a **pollination-benefit channel**, not a same-unit net mixed outcome. It is stored in `mixed_channel_effects.csv` and excluded from mixed H1 rather than reclassified post hoc as a pure mutualist.

## Remaining strict bridges

### Mutualist

IWE008 (Qilian 2024) directly measures flowering peaks, key-pollinator peaks and individual seed setting with mismatch direction retained. The design is strict-eligible but a recoverable quantitative coefficient plus variance remains unavailable from public sources.

### Antagonist

IWE035 (wild `Helianthus annuus`) remains the only antagonist `unresolved_strict` bridge: seasonal abundance/damage of seed-feeding herbivores and plant fitness occur together, but a common synchrony coefficient plus sampling variance is still missing.

### Mixed

IWE059 (`Ficus pertusa ×` pollinating fig wasps) remains unresolved-strict. It combines crop receptivity/attractiveness timing, temporal pollinator abundance, visitation, seeds per fig and wasp production, but a registered crop-level timing effect plus variance has not yet been recovered.

## Measurement asymmetry remains, but mixed is no longer empty

The first closed Ficus experiment changes the diagnosis from `mixed strict effects absent` to `mixed strict effects rare but demonstrably recoverable`.

The broader asymmetry remains:

- mutualist mismatch studies relatively often measure plant timing + partner timing + final reproduction;
- antagonist studies usually measure flowering date plus attack/predation/selection, or nonlinear enemy windows;
- mixed nursery-pollination studies usually separate partner timing from final net plant fitness, with controlled monoecious fig experiments providing a rare exception.

A naive three-class pooled analysis would still confound interaction role with measurement design unless the systematic search recovers more comparable antagonist and mixed effects.

## Nonlinear antagonist discovery lane

Three antagonist systems provide direct timing plus final-fitness evidence that is not represented well by one slope:

- `Geum urbanum × Byturus ochraceus`: intermediate off-peak flowering optimum under predation;
- `Cardamine pratensis × Anthocharis cardamines`: temporal refugia on both sides of the butterfly flight period;
- `Erigeron glaucus × Tephritis ovatipennis`: viable seed success lowest at intermediate flowering synchrony.

This remains discovery evidence because the pattern was recognized after outcome screening.

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
5. Do not pool `log_rate_slope_per_day`, Fisher-z, SMD or generic log-response-ratio effects without a separately frozen common-scale conversion.
