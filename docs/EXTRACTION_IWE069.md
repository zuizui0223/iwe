# IWE069 extraction receipt — Ficus hispida × Ceratosolen solmsi marchali

Source: Liu C, Yang D-R, Compton SG, Peng Y-Q. 2013. *Larger Fig Wasps Are More Careful About Which Figs to Enter – With Good Reason*. PLoS ONE 8:e74117. DOI `10.1371/journal.pone.0074117`; PMCID `PMC3781092`.

Status: **direct experimental timing, mixed-system pollination-benefit channel; excluded from mixed net H1**.

## Biological classification

`Ficus hispida` is functionally dioecious. Female figs contain female flowers and produce seeds; male figs contain nursery flowers that rear offspring of the obligate pollinating fig wasp `Ceratosolen solmsi marchali`.

The same pollinator species therefore participates in a nursery-pollination mutualism at the host-species level, but seed production and pollinator larval cost occur on different plant sexes. Female seed production cannot be treated as a same-reproductive-unit mixed benefit–cost outcome.

## Experimental timing exposure

Pre-receptive figs were bagged to exclude natural fig-wasp entry. Freshly emerged pollinators were experimentally presented to figs of known age after the onset of receptivity. Experiments were repeated in three seasons:

- WRS — warm rainy season;
- CDS — cold dry season;
- WDS — warm dry season.

For the reproductive-success experiment, single pollinators entered figs of varying ages. Mature female figs were scored for final seed number; male figs were scored for pollinator offspring and empty galls.

The timing exposure is one-sided:

`delay_days = pollinator entry age - first receptive day >= 0`.

## Source-reported female seed effects

Table 4 reports Poisson GLMs of seed number against fig age at pollinator entry:

| season | beta | SE | variance |
|---|---:|---:|---:|
| WRS | -0.10 | 0.003 | 0.000009 |
| CDS | -0.08 | 0.001 | 0.000001 |
| WDS | -0.16 | 0.002 | 0.000004 |

All three estimates therefore show lower expected seed production when female figs wait longer for pollination.

The source also reports corresponding negative age effects on pollinator offspring in male figs:

- WRS: `-0.19 ± 0.006`;
- CDS: `-0.08 ± 0.001`;
- WDS: `-0.13 ± 0.003`.

Those male-offspring effects are retained as biological context and are not combined algebraically with female seed effects into an invented net plant-fitness quantity.

## Storage decision

The three female seed slopes are stored in:

`data/extraction/mixed_channel_effects.csv`

with:

- `channel = pollination_benefit`;
- `effect_family = log_rate_slope_per_day`;
- shared dependence ID `DEP_IWE069_FICUS_HISPIDA`.

They are not entered into `direct_effects.csv`.

## Why this matters despite exclusion from net H1

IWE065 (`Ficus semicordata`) and IWE069 independently show the same qualitative timing effect in dioecious fig systems: delaying a pollinator after the onset of receptivity strongly reduces female seed production.

That provides replicated evidence for a timing-sensitive **benefit channel** within nursery pollination. It does not replicate IWE064's stricter monoecious same-syconium net mixed outcome.

## Claim ceiling

IWE069 supports:

> experimentally delaying pollinator entry reduces female seed production in three seasonal replicates of a dioecious fig nursery-pollination system.

It does not support:

- a same-unit net mixed benefit–cost effect;
- a class-level mixed synchrony estimate;
- treating the three seasonal rows as three independent biological systems;
- adding female seed and male wasp-offspring coefficients into a synthetic lifetime-fitness metric.
