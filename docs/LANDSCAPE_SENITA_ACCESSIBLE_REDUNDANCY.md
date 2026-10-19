# Senita cactus — accessible pollinator redundancy is time dependent

Date: 2026-10-02  
Programme: Holland & Fleming, *Lophocereus schottii × Upiga virescens*  
Core sources: Fleming & Holland 1998; Holland & Fleming 2002  
DOIs: `10.1007/s004420050459`, `10.1007/s00442-002-1061-y`  
Landscape role: timing-conditioned pollinator redundancy; benefit-channel mechanism only.

## Why this matters for IWE H3

The original IWE H3 proposed that partner redundancy may buffer reproductive loss under mismatch.

The senita system shows that a simple count of alternative pollinators is not enough.

Senita cactus has:

- a specialized nocturnal senita moth pollinator;
- diurnal halictid bee co-pollinators.

Whether the bees can buffer low moth service depends on whether cactus flowers remain open after sunrise. Flower closure is temperature dependent.

Thus redundancy has a temporal accessibility condition:

`effective redundancy(t) = available alternative partners that overlap the receptive plant window at t`.

## Experimental partner contributions

Pollinator-exclusion experiments separate the contributions of moths and bees.

Selected source means (% flowers initiating fruit ± SE):

| Period | Open | Moth-only | Bee-only | Pollen supplemented |
|---|---:|---:|---:|---:|
| ORPI 1997 | 25 ± 2 | 17 ± 3 | 6 ± 2 | 39 ± 4 |
| BK May 1998 | 49 ± 7 | 52 ± 7 | 4 ± 2 | 39 ± 9 |
| BK June 1998 | 33 ± 4 | 25 ± 8 | 0.5 ± 0.5 | — |

In 1997, when fruit set was pollen limited and both partner classes were accessible, both moths and bees were needed to recover the open-pollinated level.

In May and June 1998, senita moths accounted for essentially all useful pollination and bees contributed little.

## Two natural accessibility failures

### 1. Daily access failure of the redundant partner

From 1999–2000, flowering began late enough in the hot season that flowers commonly closed before sunrise.

Because the co-pollinating bees are diurnal, this naturally removed them from the interaction window even though bees still existed in the regional pollinator community.

Open-pollinated fruit set remained 51 ± 11% in 1999 and 55 ± 8% in 2000, and the authors infer that this service was supplied nocturnally by senita moths.

### 2. Cohort gap in the specialist partner

In July 1998, senita moths were in pre-adult life stages between moth cohorts.

Open-pollinated flowers set **0% fruit**, whereas pollen-supplemented flowers set **22.5 ± 6.6%**.

The source explicitly interprets the zero fruit set as the absence of the effective nocturnal pollinator cohort; other nocturnal insects did not compensate.

This is a direct demonstration that a partner-rich community can still have zero effective redundancy if alternative partners do not overlap the plant's receptive window.

## Revised H3

The stronger hypothesis is:

> **H3 — overlap-conditioned redundancy:** reproductive buffering depends on the number of alternative partners whose activity windows overlap the focal plant's receptive period, not on partner richness alone.

Conceptually:

`R_eff(t) = sum_j I(partner_j active at t AND able to access receptive flowers at t)`.

The exact functional form is not fixed here; the important point is that redundancy is a time-indexed property.

## Relation to the landscape pivot

This result adds a fourth temporal object to the pivot:

1. partner exposure;
2. host sensitivity;
3. final plant fitness;
4. **accessibility of alternative partners**.

A plant can therefore become vulnerable to mismatch either because the focal partner shifts, because plant sensitivity changes, or because redundant partners become temporally inaccessible.

## Claim boundary

Fruit set in the 2002 exclusion experiments is the fraction of flowers initiating fruit development, not post-larval final seed production.

The result therefore supports the pollination-benefit / redundancy mechanism but is not a strict mixed net-fitness effect.

The source values used here are stored in
`data/source_reconstructions/senita_accessible_redundancy.csv`.
