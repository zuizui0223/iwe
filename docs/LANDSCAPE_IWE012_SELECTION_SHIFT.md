# IWE012 antagonist selection-shift evidence

Date: 2026-10-02  
Study: Valdés & Ehrlén 2017, *Gentiana pneumonanthe × Phengaris alcon*  
DOI: `10.1002/ecy.1633`  
Landscape role: antagonist-conditioned seasonal fitness landscape.

## Why this matters for the pivot

IWE012 was rejected from strict synchrony because the focal study does not provide an independently measured adult-butterfly activity curve that can order plant timing by partner overlap.

That exclusion remains correct for strict H1.

For the landscape question, however, the study provides unusually strong evidence that an antagonist changes the **slope of the plant fitness landscape over flowering time**.

Fitness is the number of intact fruits, traits are standardized within populations, and fitness is relativized within populations.

## Replicated selection shift

The published mixed models test whether predator presence changes selection on flowering phenology.

| Year | Plants | Populations | Predation × Phenology Wald chi-square |
|---|---:|---:|---:|
| 2010 | 2000 | 20 | 15.38*** |
| 2011 | 1598 | 16 | 14.95*** |

The paper reports the same biological direction in both years:

- without *P. alcon*, selection favors earlier flowering;
- with *P. alcon*, preferential attack on early-flowering plants shifts selection toward later flowering.

This is not a partner-synchrony coefficient. It is a replicated **interaction-induced rotation of the temporal fitness slope**.

## Mechanistic attack link

Among populations with the butterfly, early flowering predicts attack in both years.

| Year | Plants | Predator-present populations | chi-square | reported estimate |
|---|---:|---:|---:|---:|
| 2010 | 1000 | 10 | 38.84*** | +0.300 |
| 2011 | 1099 | 11 | 38.24*** | +0.968 |

The source additionally reports that advancing phenology by one developmental stage, approximately one week, corresponds on average to 0.87 additional eggs per plant.

Thus the fitness-slope shift is linked to a measured realized-interaction mechanism: earlier plants receive more predator eggs.

## What it identifies

IWE012 identifies:

1. a temporal plant trait axis;
2. antagonist-mediated attack along that axis;
3. final intact-fruit fitness;
4. a repeated predator-presence × timing effect across two years.

It does **not** independently identify the adult *P. alcon* availability curve, so it remains outside the strict synchrony dataset.

## Ecological interpretation

The key result is stronger than “seed predators favor late flowering.”

The baseline seasonal landscape favors early flowering, but the antagonist adds a timing-dependent cost concentrated on earlier plants and can reverse the net slope.

That means the observed fitness landscape is a combination of:

- a baseline plant seasonal payoff surface;
- a time-structured antagonist cost surface.

This motivates separating **partner exposure** from **plant fitness sensitivity** rather than reducing every study to distance from a partner peak.

Machine-readable statistics are in `data/derived/iwe012_antagonist_selection_shift.csv`.
