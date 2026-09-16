# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Question

Before interpreting any ecological effect, ask whether the three interaction classes have been studied with the same measurement architecture.

IWE's strict H1 requires a plant-partner timing exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for an effect size.

## Current screened corpus

After source adjudication through IWE048:

| interaction type | screened | strict candidate `include` | strict effect programmes quantitatively closed | unresolved possible strict | context/timing-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 17 | 8 | 1 | 6 | 3 | 0 |
| antagonist | 17 | 0 | 0 | 1 | 13 | 3 |
| mixed pollinating seed predator | 14 | 0 | 0 | 2 | 12 | 0 |

These are screening-stage counts, not final systematic-review denominators. IWE001-IWE040 form the discovery corpus; IWE041 onward are logged under the prospective search-integrity rules.

IWE001 is the one currently closed strict-H1 programme. Its NFP, TOEF and JOZ effects are dependent population-level estimates and therefore count as one programme, not three independent studies.

For the antagonist row, IWE028 is counted as context/timing evidence because its source-level extraction receipt showed that attack and potential seed production are observed but integrated realized seed set is model-derived. IWE035 remains the only `unresolved_strict` antagonist bridge candidate because seasonal enemy abundance/damage and final plant fitness occur in the same study but a common-scale synchrony coefficient plus sampling variance has not been recovered.

For the mixed row, IWE014 and IWE019 remain unresolved possible strict candidates. All other recovered mixed studies either quantify seasonal timing without an independent partner-activity curve, quantify partner timing without final net plant fitness, or decompose benefit/cost channels without identifying one synchrony-to-net-fitness effect.

## What the asymmetry means

This is **not yet evidence that synchrony matters more for mutualists than antagonists**.

It is evidence that the literature has been measured differently:

- mutualist mismatch studies often record both plant and pollinator phenology and then seed/fruit production;
- antagonist studies often record plant date plus attack/predation, or an enemy activity window plus a fitness surface that is nonlinear;
- nursery-pollination studies often resolve benefit and cost mechanisms but do not estimate one quantitative synchrony-to-net-plant-fitness effect.

Therefore a naive three-class meta-analysis would confound interaction type with measurement design.

## Strongest current biological signal outside strict H1

Three antagonist systems recovered during screening have direct timing and final-fitness information but reject a one-slope representation:

- `Geum urbanum × Byturus ochraceus`: interior optimum in off-peak flowering under predation;
- `Cardamine pratensis × Anthocharis cardamines`: temporal refugia on both sides of the butterfly flight period;
- `Erigeron glaucus × Tephritis ovatipennis`: viable seed production is lowest at intermediate flowering synchrony.

These are stored in `shape_evidence.csv`. Because this pattern was recognized after viewing screening outcomes, it is discovery evidence and cannot be promoted to a preregistered confirmatory antagonist-curvature claim in the same corpus.

## Mixed systems expose a particularly clear measurement split

The post-freeze citation closure sharpened the mixed-system diagnosis.

- `Dianthus sylvestris × Hadena compta` (IWE041) measures plant flowering onset, Hadena predation and final unattacked mature-seed production. The two years give direct seasonal-timing slopes on net female reproduction, but the study does not independently quantify the moth activity curve.
- `Silene alba/S. dioica × Hadena bicruris` (IWE044) similarly connects flowering timing to fruit set, predation and undamaged fruit production, but includes additional fungal antagonism and no independent quantitative moth-activity curve.
- `Silene latifolia/S. dioica × Hadena bicruris` phenology work (IWE045) directly compares host flowering periods with moth activity/oviposition, but does not provide the final plant-fitness endpoint needed by strict H1.

Thus the two ingredients needed by IWE — explicit partner synchrony and final net plant fitness — are often measured in **different papers**, even within the same classic nursery-pollination system.

This is a concrete example of the broader evidence-architecture problem rather than evidence for a biological null.

## High-value mutualist extraction still open

IWE008 (`Wang et al. 2024`, Qilian alpine grassland) is design-eligible for strict H1 because plant flowering abundance, key-pollinator abundance peaks and individual-level seed setting are measured in the same community. It additionally distinguishes the two mismatch directions. Public sources confirm that pollinator-earlier mismatch has the stronger negative fecundity association and that shorter flowering duration amplifies the asymmetry, but an extractable coefficient/correlation plus sampling variance has not yet been recovered. It therefore remains quantitative-unresolved rather than being converted from significance statements.

## Consequence for the paper strategy

The current evidence supports two possible endpoints, both predeclared as valid:

1. **Strict meta-analysis endpoint:** enough comparable effects are eventually recovered to test H1 across interaction classes.
2. **Evidence-architecture endpoint:** strict effects remain concentrated in mutualisms, in which case IWE reports the systematic measurement asymmetry, performs the defensible direct meta-analysis in the classes where it is estimable, and separately synthesizes seasonal/shape evidence without pretending those estimands are equivalent.

The second endpoint is not a failed version of the first. It answers a different empirical question: which ecological claims about phenological mismatch are actually identified by the published measurements?

## Next falsification priorities

1. Continue the frozen systematic search specifically for antagonist and mixed studies containing **partner emergence/activity + directly observed final seed/fruit output + recoverable uncertainty**.
2. Attempt quantitative recovery of IWE014, IWE019 and IWE035 before concluding that the mixed/antagonist strict lanes are effectively empty.
3. Recover IWE008 coefficients/raw data so the mutualist lane does not rest on the Corydalis programme.
4. Keep all post-freeze discovery and holdout eligibility in `prospective_search_log.csv`; no post-hoc shape result can be promoted as confirmation after its outcome has already been viewed.
