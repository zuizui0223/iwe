# Slimon 2026: is old Mompha simply a carry-forward of new Mompha?

Original data archive: [Slimon & Agrawal (2026), DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509),
official `Freese Stats.zip`, verified MD5
`151bbd516fc0032af2a2598cb5529c78`.
Audit date: 2026-10-13.
Executable source audit:
`scripts/audit_slimon2026_old_mompha_stockflow.py`.
Source-derived numerical receipt:
`data/source_reconstructions/slimon2026_old_mompha_stock_flow.csv`.

## Identification question and major original-source correction

Previous IWE PR #95 found a positive `new Mompha(t)`–`old Mompha(t+7)`
association within original plants after plant and survey-day
conditioning. However, this might be **partially source bookkeeping**,
not independent maturation of tracked larvae.

Directly reviewed **original R code**, rather than guessed common
names, identifies the tissue states:

- `exp1_time_series.R`, original **line 159**:
  `mompha` is a *field gall count*; `OLDmompha` is a
  *desiccated flower-bud count*.
- `exp2_time_series.R`, original **line 119**:
  the same field-gall versus desiccated-bud distinction.

Therefore source **new/old labels refer to damage/tissue appearance**,
not known young/old ages of individually identifiable insects. The
source paper concerns specialist bud/fruit damage on
*Oenothera biennis*; external taxonomic work independently
documents *M. stellella* in flower buds and
*M. brevivittella* in immature fruits
([Bruzzese et al. 2019](https://doi.org/10.1371/journal.pone.0207833)).

This corrects the prior temptation to interpret two weekly source
count columns as an insect developmental clock. It does **not**
invalidate the observed timing association; it changes what
the measured variables represent.

## Direct original numerical stock-flow identity check

For each original plant with an actual source count at the same
four numeric fields `new(t)`, `old(t)`, `new(t+7)` and
`old(t+7)`, test a possible *pure stock carry-forward*:

`old(t+7) = old(t) + new(t)`.

Never fabricate a week, fill a missing source cell with zero,
or treat exp2's 828 blank/unkeyed exported rows as plants.

| Source check | Experiment 1 | Experiment 2 |
|---|---:|---:|
| Complete numeric original plant × week pairs | **795** | **641** |
| All-zero `new(t), old(t), old(t+7)` pairs | 224 | 300 |
| Nontrivial plant × weeks (at least one of those counts positive) | **571** | **341** |
| Identity on all pairs | 420/795 = **52.8%** | 382/641 = **59.6%** |
| **Identity on nontrivial pairs** | **196/571 = 34.3%** | **82/341 = 24.0%** |
| Sum change `old(t+7)-old(t)` | +47 | −50 |
| Sum source `new(t)` across same pairs | 807 | 450 |

The naive higher apparent identity percentage is inflated by
trivial zero records. **Old damage is not an exact cumulative
sum of new observations** on most biologically active
plant-weeks. The observed season-scale changes in old also
differ markedly from same-week new totals.

But non-identity to this simplistic formula **does not
independently authenticate** insect ages, oviposition timing
or complete separate source measurement; damaged buds may
senesce, fall, persist or be recounted, and original data
contain missing stage observations. We cannot identify
the exact biological fate of each gall.

## Why the cumulative helper is not new empirical reproduction

The author archive includes two distinct long-format
`momphaCALC` helpers:

| Source long helper | Rows | Plants with original ID |
|---|---:|---:|
| `momphaCALC_exp1.csv` | 1,716 | 156 |
| `momphaCALC_exp2.csv` | 1,116 | 123 |

Columns contain original `mompha`, `OLDmompha`, several
`increase`, `gained`, `lost` terms, and
`TOTAL_Mompha`. The published R scripts explicitly
use these inputs to build the end-of-season Mompha
damage accounting. `TOTAL_Mompha` must **not** be
counted as an independently observed adult activity
curve, a further independent cohort, or final measured
intact viable seeds.

Source stage screening also established the exp2 old
export's **951 physical rows** contain only **123 rows
with plant IDs**, and the additional **828** rows have
no numeric Mompha counts or other substantive metadata.
The additional rows create no biological replication.
The two experimental components' flowering records are
both dated **2023**, not independent annual field years.

## Biological interpretation and inference gate

Supported:
- new visible gall observations are temporally associated
  with later desiccated-bud observations on the same plants;
- the source's desiccated-bud counts **do not obey a simple
  universal, deterministic carry-forward formula**;
- the original research treats both counts as inputs to a
  derived cumulative herbivore-damage metric.

**Not supported:** a tagged *Mompha* larva becoming older
over seven days, a measured egg-to-larva lag, direct
adult flight availability, true host bud denominator,
or a source-verified same-unit intact mature-seed response.

The ecological question is therefore **how phenology
determines exposure of developing buds, and how visible
galls progress to retained or desiccated bud damage**,
not whether two labels on raw spreadsheets by themselves
prove insect generation time.

Next original-data discriminator: marked individual
flower-bud/gall trajectories linking initial infestation
to its later visible and senescent state, plus terminal
observed viable seeds and independent adult moth activity.

**Strict H1 unchanged:** mutualist 2, antagonist 0,
mixed 0. The above is a source-supported exploratory
damage-stage measurement audit and is not a strict
phenological synchrony–final fitness effect.
