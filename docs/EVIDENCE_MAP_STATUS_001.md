# IWE evidence-map status 001

Date: 2026-09-17
Status: screening-stage diagnostic, not final systematic-review counts

## Question

Before interpreting any ecological effect, ask whether the three interaction classes have been studied with the same measurement architecture.

IWE's strict H1 requires a plant-partner timing exposure and a final plant reproductive outcome at compatible biological grain, plus enough uncertainty information for an effect size.

## Current screened corpus

After source adjudication of IWE001-IWE034:

| interaction type | screened | strict candidate `include` | strict effect programmes quantitatively closed | unresolved possible strict | context/timing-only | nonlinear shape lane |
|---|---:|---:|---:|---:|---:|---:|
| mutualist | 16 | 8 | 1 | 6 | 2 | 0 |
| antagonist | 10 | 0 | 0 | 0 | 7 | 3 |
| mixed pollinating seed predator | 8 | 0 | 0 | 2 | 6 | 0 |

IWE001 is the one currently closed strict-H1 programme. Its NFP, TOEF and JOZ effects are dependent population-level estimates and therefore count as one programme, not three independent studies.

For the antagonist row, IWE028 is counted as context/timing evidence because its source-level extraction receipt showed that attack and potential seed production are observed but integrated realized seed set is model-derived. Its registry row may temporarily retain `unresolved` until the next registry-sync commit; the extraction receipt is the adjudication authority.

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

## Newly recovered mixed-system lead

Dufay (2010), DOI `10.1111/j.1420-9101.2010.01968.x`, studied `Chamaerops humilis × Derelomus chamaeropsis` and directly compared host flowering phenology with pollinator emergence. Female fruit production was pollen/pollinator limited and highest three-seeded-fruit proportions occurred when female anthesis matched the end of male anthesis. The system is an important nursery-pollination phenology lead, but costs are borne mainly through larval development in male inflorescences whereas female fruit success is measured separately. It therefore should not be labelled a strict net mixed-effect until individual/population-scale benefit and cost can be placed on one fitness scale.

## Consequence for the paper strategy

The current evidence supports two possible endpoints, both predeclared as valid:

1. **Strict meta-analysis endpoint:** enough comparable effects are eventually recovered to test H1 across interaction classes.
2. **Evidence-architecture endpoint:** strict effects remain concentrated in mutualisms, in which case IWE reports the systematic measurement asymmetry, performs the defensible direct meta-analysis in the classes where it is estimable, and separately synthesizes seasonal/shape evidence without pretending those estimands are equivalent.

The second endpoint is not a failed version of the first. It answers a different empirical question: which ecological claims about phenological mismatch are actually identified by the published measurements?

## Next falsification priorities

1. Search specifically for antagonist studies containing **partner emergence/activity + directly observed final seed/fruit output + recoverable uncertainty**.
2. Attempt quantitative recovery of IWE014 and IWE019 before concluding that the mixed strict lane is empty.
3. Extract IWE002 and IWE008 so the mutualist lane does not rest on one long-term Corydalis programme.
4. Freeze a search-completion rule before interpreting the class imbalance as a literature-level result.
