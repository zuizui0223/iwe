# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Question

Before interpreting any ecological effect, ask whether the three interaction classes have been studied with the same measurement architecture.

IWE's strict H1 requires a plant-partner timing exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for an effect size.

## Current screened corpus

After source adjudication through IWE058, including the source-level overrides in `data/registry/adjudication_overrides.csv`:

| interaction type | screened | strict candidate `include` | strict effect programmes quantitatively closed | unresolved possible strict | context/timing-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 7 | 1 | 6 | 4 | 0 |
| antagonist | 22 | 0 | 0 | 1 | 18 | 3 |
| mixed pollinating seed predator | 19 | 0 | 0 | 0 | 19 | 0 |

These are screening-stage counts, not final systematic-review denominators. IWE001-IWE040 form the discovery corpus; IWE041 onward are logged under the prospective search-integrity rules.

The mutualist `include` count is seven, not eight, because IWE004 was subsequently source-adjudicated from `include` to `context_only`: the Pulsatilla study has direct flowering timing, estimated pollinator availability and seed set, but it does not identify a focal plant-partner overlap/mismatch variable under the frozen strict-H1 contract.

IWE001 remains the one currently closed strict-H1 programme. Its NFP, TOEF and JOZ effects are dependent population-level estimates and therefore count as one programme, not three independent studies.

For antagonists, IWE035 remains the only `unresolved_strict` bridge candidate because seasonal enemy abundance/damage and final plant fitness occur in the same study but a common-scale synchrony coefficient plus sampling variance has not been recovered. IWE028 is context/timing evidence after full source adjudication rather than unresolved strict evidence.

For mixed pollinating seed predators, **no currently screened study remains strict-admitted or unresolved-strict**. IWE014 and IWE019 were both resolved downward after source-level review: IWE014 contains seasonal timing plus final seed set but no independent Hadena activity curve, whereas IWE019 directly measures Ficus–Wiebesia timing but does not estimate a comparable synchrony-to-final-seed effect with sampling uncertainty.

## What the asymmetry means

This is **not evidence that synchrony matters more for mutualists than antagonists or mixed interactions**.

It is evidence that the literature has been measured differently:

- mutualist mismatch studies often record both plant and pollinator phenology and then seed/fruit production;
- antagonist studies often record plant date plus attack/predation, or an enemy activity window plus a fitness surface that is nonlinear;
- nursery-pollination studies often resolve benefit and cost mechanisms but do not estimate one quantitative synchrony-to-net-plant-fitness effect.

Therefore a naive three-class meta-analysis would confound interaction type with measurement design.

## Strongest biological signal outside strict H1

Three antagonist systems recovered during screening have direct timing and final-fitness information but reject a one-slope representation:

- `Geum urbanum × Byturus ochraceus`: interior optimum in off-peak flowering under predation;
- `Cardamine pratensis × Anthocharis cardamines`: temporal refugia on both sides of the butterfly flight period;
- `Erigeron glaucus × Tephritis ovatipennis`: viable seed production is lowest at intermediate flowering synchrony.

These are stored in `shape_evidence.csv`. Because this pattern was recognized after viewing screening outcomes, it is discovery evidence and cannot be promoted to a preregistered confirmatory antagonist-curvature claim in the same corpus.

## Mixed systems expose a cross-lineage measurement split

The post-freeze citation closure and frozen mixed query show that the split is not confined to one Hadena study.

### Hadena systems

- `Dianthus sylvestris × Hadena compta` (IWE041) measures flowering onset, predation and final unattacked mature-seed production. Two direct seasonal-timing slopes are recoverable, but no independent moth activity curve identifies partner synchrony.
- `Silene alba/S. dioica × Hadena bicruris` (IWE044) connects flowering timing to fruit set, predation and undamaged fruit production, but again lacks an independent quantitative moth-activity curve.
- `Silene × Hadena` phenology work (IWE045) directly compares host flowering with moth activity/oviposition, but does not provide the final plant-fitness endpoint required by strict H1.

### Trollius–Chiastocheta

- IWE054 measures oviposition, seed predation and annual seed output, but the focal axes are flower size/number, altitude and fly abundance rather than partner synchrony.
- IWE055 demonstrates species-specific oviposition timing across flower ages and interaction outcomes from mutualistic to parasitic, but this is within-flower-age niche partitioning rather than seasonal phenological matching.
- IWE056 has visitation and net seed set under a floral-architecture manipulation, not a timing manipulation.

### Glochidion–Epicephala

- IWE017 measures host–Epicephala phenological tracking in detail but not a synchrony-to-final-plant-fitness effect.
- IWE057 quantifies how Epicephala egg load/ovule damage and selective abortion affect seed production, but timing is not the exposure.

Thus explicit partner synchrony and final net plant fitness are repeatedly measured in **different experiments or papers**, even within canonical nursery-pollination systems. This is a measurement-architecture result, not a biological null.

## High-value mutualist extraction still open

IWE008 (`Wang et al. 2024`, Qilian alpine grassland) is design-eligible for strict H1 because plant flowering abundance, key-pollinator abundance peaks and individual-level seed setting are measured in the same community. It additionally distinguishes the two mismatch directions. Public sources confirm that pollinator-earlier mismatch has the stronger negative fecundity association and that shorter flowering duration amplifies the asymmetry, but an extractable coefficient/correlation plus sampling variance has not yet been recovered. It therefore remains quantitative-unresolved rather than being converted from significance statements.

## Prior-art boundary

Munguía-Rosas et al. (2011) already meta-analyzed phenotypic selection on flowering time and among-plant flowering synchrony, and its supplement separately summarizes pre-dispersal seed predation in relation to flowering time. IWE therefore does not claim novelty for meta-analysis of flowering phenology or for showing that seed predators can select on flowering date.

The narrower target is a common plant–interaction-partner temporal-matching estimand connected to final plant reproductive fitness, with interaction role as moderator. See `docs/PRIOR_ART_BOUNDARY_V1.md`.

## Consequence for the paper strategy

The current evidence supports two valid endpoints:

1. **Strict meta-analysis endpoint:** enough comparable effects are eventually recovered to test H1 for the classes in which the strict estimand is actually measured.
2. **Evidence-architecture endpoint:** strict effects remain concentrated in mutualisms, in which case IWE reports the systematic measurement asymmetry, performs the defensible direct meta-analysis where estimable, and separately synthesizes seasonal/shape evidence without pretending those estimands are equivalent.

The second endpoint is not a failed version of the first. It answers which ecological claims about phenological mismatch are actually identified by published measurements.

## Next falsification priorities

1. Complete the frozen backward/query/forward/citation-closure search before treating class imbalance as final.
2. Attempt quantitative recovery of IWE035 before concluding the antagonist strict lane is effectively empty.
3. Recover IWE008 coefficients/raw data so the mutualist strict lane does not rest on the Corydalis programme.
4. Keep all post-freeze discovery and holdout eligibility in `prospective_search_log.csv`; no post-hoc shape result can be promoted as confirmation after its outcome has already been viewed.
