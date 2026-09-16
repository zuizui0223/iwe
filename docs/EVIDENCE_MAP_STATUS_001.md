# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Strict question

IWE strict H1 requires a plant-partner temporal-matching exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for a quantitative effect.

## Current screened corpus

After source adjudication through IWE063, including `data/registry/adjudication_overrides.csv`:

| interaction type | screened | strict `include` | strict programmes quantitatively closed | unresolved possible strict | context/timing-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 7 | 1 | 6 | 4 | 0 |
| antagonist | 22 | 0 | 0 | 1 | 18 | 3 |
| mixed pollinating seed predator | 24 | 0 | 0 | 1 | 23 | 0 |

IWE001–IWE040 are the discovery corpus. IWE041 onward are post-freeze records tracked in `prospective_search_log.csv`.

IWE001 is the only quantitatively closed strict programme so far; its three population effects remain dependent estimates, not three independent studies.

## Source-level corrections that matter

- IWE004 was downgraded from `include` to `context_only`: flowering timing, estimated pollinator availability and seed set are present, but no focal plant-partner overlap/mismatch variable is identified.
- IWE014 was resolved from `unresolved` to `context_only`: seasonal position, Hadena pollination/predation and final seed set are present, but no independent Hadena activity curve identifies strict synchrony.
- IWE019 was resolved from `unresolved` to `context_only`: Ficus–Wiebesia timing is measured directly, but no comparable synchrony-to-final-seed effect with sampling uncertainty is estimated.
- IWE028 was resolved from `unresolved` to `context_only`: enemy attack and potential seed production are observed but the strict realized-fitness timing effect is not directly identified.

## Remaining strict bridges

### Mutualist

IWE008 (Qilian 2024) is design-eligible: plant flowering peaks, key-pollinator abundance peaks and individual seed setting are measured, with mismatch direction retained. A quantitative effect plus variance has not yet been publicly recovered.

### Antagonist

IWE035 (wild `Helianthus annuus`) remains the only antagonist `unresolved_strict` bridge: seasonal abundance/damage of seed-feeding herbivores and plant fitness occur together, but a common synchrony coefficient plus sampling variance is still missing.

### Mixed

IWE059 (`Ficus pertusa ×` pollinating fig wasps) is the only mixed `unresolved_strict` bridge recovered so far. It combines crop receptivity/attractiveness timing, temporal pollinator abundance, visitation, seeds per fig and wasp production. Crops attracting wasps earlier are most heavily visited but mature fewer seeds and pollinator offspring per fig. A registered crop-level matching effect and sampling variance have not yet been recovered.

## Measurement asymmetry

The current table is **not** evidence that synchrony is biologically more important for mutualists.

It is evidence that interaction classes have been studied with different measurement architectures:

- mutualist mismatch studies often measure plant timing + partner timing + final seed/fruit output in the same study;
- antagonist studies often measure flowering date + attack/predation/selection, with enemy timing implicit or with nonlinear temporal refugia;
- mixed nursery-pollination studies often measure partner timing and final net plant fitness in separate experiments or focus on benefit/cost mechanisms rather than one synchrony effect.

A naive three-class pooled meta-analysis would therefore confound interaction role with measurement design.

## Nonlinear antagonist discovery lane

Three antagonist systems provide direct timing plus final-fitness evidence that is not well represented by one slope:

- `Geum urbanum × Byturus ochraceus`: intermediate off-peak flowering optimum under predation;
- `Cardamine pratensis × Anthocharis cardamines`: temporal refugia on both sides of the butterfly flight period;
- `Erigeron glaucus × Tephritis ovatipennis`: viable seed success lowest at intermediate flowering synchrony.

Because this pattern was recognized after outcome screening, it remains discovery evidence. Post-freeze records whose outcomes were already visible are explicitly barred from serving as blind shape confirmation.

## Mixed-system split is cross-lineage

The same missing-link pattern now appears across Hadena, Trollius–Chiastocheta, Glochidion–Epicephala and Ficus–fig-wasp systems.

Examples:

- IWE041: plant seasonal timing + Hadena predation + final female fitness, but no independent moth activity curve;
- IWE045: direct host-flowering × Hadena activity timing, but no compatible final plant-fitness effect;
- IWE054: Trollius oviposition/seed predation + annual seed output, but timing is not the focal axis;
- IWE017: Epicephala–host phenological tracking, but no synchrony-to-final-plant-fitness effect;
- IWE057: Epicephala exploitation + seed-production consequences, but timing is not the exposure;
- IWE019: direct Ficus–Wiebesia timing, but no pooled strict seed-fitness effect;
- IWE059: the closest current Ficus bridge, still quantitatively unresolved.

## Prior-art boundary

Munguía-Rosas et al. (2011) already meta-analyzed selection on flowering time and among-plant flowering synchrony, and its supplement separately summarizes pre-dispersal seed predation in relation to flowering time. IWE therefore does not claim novelty for generic flowering-phenology meta-analysis or for showing that seed predators select on flowering date.

IWE's narrower target is:

> plant–interaction-partner temporal matching -> final plant reproductive fitness,

using a common timing estimand where the published measurements allow it, with interaction role as a moderator.

See `docs/PRIOR_ART_BOUNDARY_V1.md`.

## Valid paper endpoints

1. **Strict meta-analysis endpoint:** enough comparable strict effects are recovered for one or more interaction classes.
2. **Evidence-architecture endpoint:** strict effects remain concentrated in mutualisms; IWE then reports the systematic measurement asymmetry, meta-analyzes only estimable strict lanes, and separately synthesizes timing/shape evidence without treating those estimands as equivalent.

The second endpoint is not a failed version of the first.

## Next falsification priorities

1. Complete frozen backward/query/forward/citation closure before treating the class imbalance as final.
2. Attempt numerical recovery of IWE035 and IWE059 before declaring antagonist/mixed strict lanes effectively empty.
3. Recover IWE008 quantitative effects so the mutualist strict lane does not rest on one Corydalis programme.
4. Continue prospective-integrity logging for every IWE041+ record.
