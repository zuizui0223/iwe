# IWE066 extraction receipt — Ficus altissima × Eupristina altissima

Source: Zhang Y, Peng Y-Q, Compton SG, Yang D-R. 2014. *Premature Attraction of Pollinators to Inaccessible Figs of Ficus altissima: A Search for Ecological and Evolutionary Consequences*. PLoS ONE 9:e86735. DOI `10.1371/journal.pone.0086735`.

Status: **direct mixed-system timing experiment; admitted to preregistered H2 shape lane; no formal curvature coefficient yet**.

## Biological fit

`Ficus altissima` is monoecious. Mature figs contain both seeds and offspring of the obligate pollinating fig wasp `Eupristina altissima`. A foundress both pollinates flowers and uses ovules for larval development in the same fig, so final seed number is measured after mixed pollination benefit and nursery cost can act in the same reproductive unit.

## Timing experiment

Young figs were bagged to exclude natural wasp entry. Single freshly emerged pollinators were introduced into figs that had been accessible for different lengths of time. Fig age was measured from the onset of accessibility.

For the five experimental entry ages, source sample sizes were:

- day 1: `n=27`
- day 2: `n=25`
- day 3: `n=24`
- day 4: `n=23`
- day 5: `n=21`

After maturation, seeds and pollinator offspring in each fig were counted.

## Source-reported shape

The source states explicitly:

- seed production **peaked on days 2 and 3** after figs became accessible;
- pollinator offspring numbers were approximately stable through day 4 and then fell rapidly;
- across days 1–5, Poisson GLMs gave:
  - pollinator offspring: `beta = -0.16`, `SE = 0.01`;
  - seeds: `beta = -0.09`, `SE = 0.01`.

The negative overall seed slope cannot be interpreted as evidence that exact day-1 matching is optimal, because the same source states that seed production is higher at the interior days 2–3 than on day 1.

## H2 classification

IWE H2 was preregistered before this study was added:

> mixed pollinating-seed-predator systems may show non-monotonic reproductive responses to synchrony because increasing temporal matching can alter both benefit and cost.

IWE066 is therefore eligible as direct H2 **shape evidence**. It is coded `interior_peak_then_decline` in `shape_evidence.csv`.

The evidence is stronger than a narrative natural-history inference because timing was experimentally controlled and final same-fig seed output was measured. However, it is not yet a formal quantitative quadratic effect.

## Why no quadratic coefficient is reconstructed

The article text provides group sample sizes and the overall Poisson linear slope, but it does not print the day-specific seed means and sampling uncertainty from Figure 4. The plotted figure shows the interior peak, and the authors describe it explicitly, but IWE does not digitize bar heights into a meta-analytic curvature coefficient unless the numerical source data or a reproducible digitization audit is available.

Attempts to retrieve the publisher's large Figure-4 image/PDF through the current web environment were not reliable enough to freeze a numerical digitization. The source-text shape classification is therefore retained without inventing group means.

## Related timing mechanism

At the focal tree, adult `E. altissima` arrived before figs were physically accessible. Pollinator abundance peaked around five days after fig accessibility began and then declined. Thus the natural system itself creates a mismatch between attraction, physical accessibility and pollinator arrival, while the controlled experiment isolates the consequence of fig age at actual entry.

## Claim ceiling

IWE066 supports:

> in a monoecious fig nursery-pollination system, final seed production is non-monotonic across experimentally imposed pollinator-entry delays, with an interior maximum at approximately days 2–3 after fig accessibility.

It does not yet support:

- a numerical quadratic coefficient or turning point with confidence interval;
- a general mixed-system optimum at intermediate synchrony;
- pooling the source's overall linear Poisson slope as if day 1 were the seed optimum;
- a lifetime-fitness optimum combining all female and male reproductive components.
