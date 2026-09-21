# IWE087 extraction receipt — Rhododendron aureum × Bombus spp.

Source: Kudo G, Hirao AS, Kawai Y. 2011. *Pollination Efficiency of Bumblebee Queens and Workers in the Alpine Shrub Rhododendron aureum*. International Journal of Plant Sciences 172:70–77. DOI `10.1086/657282`.

Public version of record: Hokkaido University HUSCAP handle `2115/47946`.

Status: **unresolved strict-H1 mutualist candidate; biological estimand and 2007 plot-level reconstruction are frozen before exact figure-value extraction**.

Interaction class: `mutualist`.

Dependence ID: `DEP_IWE087_RHODODENDRON_BOMBUS`.

## Why this can close an independent common-scale programme

The 2007 source contains four spatially distinct plots with different flowering seasons:

- early-snowmelt fellfield plots F1 and F2, flowering in June;
- later snowbed plots S1 and S2, flowering in July–August.

At peak flowering in each plot, bumblebee visitation was independently observed for six hours in a fixed quadrat. Natural fruit set was measured from randomly sampled inflorescences in the same plots.

Thus the registered biological chain is:

```
pollinator activity at the focal plot's flowering peak
-> natural fruit set in that plot
```

This is direct partner availability at plant flowering, not calendar date alone.

## Frozen primary exposure

Use the source Table 1 visitation frequency in 2007:

| plot | visits per hour |
|---|---:|
| F1 | 0.098 |
| F2 | 0.067 |
| S1 | 2.62 |
| S2 | 1.25 |

These values were measured on June 14 (F1), June 20 (F2), July 27 (S1) and August 8 (S2), each at peak flowering.

The primary exposure is therefore `direct_activity` and `exposure_direction = synchrony`: larger values mean greater observed effective-partner availability while the plant population is flowering.

No transformation or re-ordering based on fruit set is permitted.

## Frozen primary outcome

Use 2007 **natural fruit-set ratio per inflorescence** from source Figure 2A for the same four plots.

Fruit set is chosen prospectively over seed set because:

1. all four plots have 2007 fruit-set estimates;
2. the source interprets the fellfield–snowbed fruit-set difference as quantitative pollen limitation driven by visitation frequency;
3. seed-set ratio is available only for F2 and S2 and is additionally affected by caste-dependent geitonogamy/self-pollen interference, leaving only two timing units and a qualitatively different pathway.

The 2007 fruit-set sample sizes printed in Figure 2A are:

- F1: `n = 35` inflorescences;
- F2: `n = 40`;
- S1: `n = 40`;
- S2: `n = 40`.

Those within-plot inflorescences improve estimation of each plot mean but do not create independent timing units.

## Frozen quantitative effect

The independent timing units are the four plots.

After reproducibly recovering the four 2007 plot means:

```
r = cor(visits_per_hour, plot_mean_fruit_set)
z = atanh(r)
variance(z) = 1 / (4 - 3) = 1
```

The native exposure direction is synchrony, so no sign flip is applied.

All rows/evidence from this study share one programme:

`DEP_IWE087_RHODODENDRON_BOMBUS`.

The estimate is deliberately imprecise because `n = 4`. The small variance denominator is not enlarged by treating inflorescences as independent timing replicates.

## Frozen figure-extraction rule

Exact fruit-set means will **not** be read by eye.

Primary extraction must use the HUSCAP version-of-record PDF and a deterministic vector-PDF route:

1. open PDF page containing Figure 2A;
2. recover text coordinates for the y-axis tick labels and plot/year labels directly from the PDF text layer;
3. recover the four filled circular 2007 mean markers directly from PDF vector drawing objects;
4. map marker y coordinates onto the source y-axis by a linear calibration using the printed numeric ticks;
5. assign x positions to F1/F2/S1/S2 using the printed plot/year labels;
6. recover all four markers without manual point selection;
7. verify that recovered values lie within the source-text reported fellfield and snowbed fruit-set ranges and that all four 2007 sample-size labels are present.

If vector extraction cannot uniquely identify all four means, the primary reconstruction remains unresolved. Manual pixel clicking or visual transcription cannot replace it.

A rasterized extraction may be used only as a labelled validation of the vector result, never as the primary value source.

## Dependence and confounding caveat

The four plots are independent spatial timing units but the contrast is observational. Snowmelt habitat, flowering season and bumblebee caste covary strongly with partner availability.

Therefore a recovered IWE087 effect is a direct **association** between partner availability at flowering and final fruit set. It is not a causal estimate that isolates timing from all habitat or caste differences.

## Relation to earlier Rhododendron work

The paper incorporates some 2003 reproductive data from Hirao et al. (2006), but the registered IWE effect is restricted to **2007**, because direct plot-level visitation frequency is measured for all four plots in that year.

Older early/late-season results are retained as context and are not counted as additional independent programmes.

## Claim ceiling

Before vector extraction, IWE087 supports:

> four published alpine populations were observed at their flowering peaks in 2007, with >10-fold variation in bumblebee visitation and matched natural fruit-set measurements, providing a prospectively defined route to an independent mutualist Fisher-z effect.

No effect magnitude or H1 conclusion is claimed until the deterministic PDF extraction is executed.
