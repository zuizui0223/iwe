# Slimon 2026: original same-plant, same-survey flower and Mompha observations

Date: 2026-10-10. Scope: **stage-detection diagnostics only**, not
a new independent adult moth season, direct stage-to-viable-seed
fitness effect, or evidence that a counted *Mompha* appeared on the
same date that it originally oviposited.

## Why this test is biologically important

The earlier original-data reanalysis linked first/last flowering
DOY to plant-level final *Mompha stellella* infestation and a
fruit-opportunity denominator. Yet *M. stellella* is a **flower-bud
borer**, not an adult pollinator of open flowers. A related specialist,
*M. brevivittella*, develops in immature fruit; *Schinia florida*
is yet another seed predator. Their **accessible plant-tissue
windows are not interchangeable**.

Independent source for the *M. stellella* **bud** versus *M.
brevivittella* **developing fruit** contrast:
[Bruzzese et al. (2019), PLOS ONE,
DOI 10.1371/journal.pone.0207833](https://doi.org/10.1371/journal.pone.0207833),
section "Mompha and onagraceae".
[Cook-Patton et al. (2017), Journal of Ecology,
DOI 10.1111/1365-2745.12717](https://doi.org/10.1111/1365-2745.12717)
independently note that a *M. stellella*-galled bud yields no viable
seed output, while a *M. brevivittella* fruit hole costs an
approximate fraction of developing seeds. These source-specific
effect pathways are different and must not be silently pooled.

**Falsifiable question:** does using open-flower abundance at the
same weekly survey date define a valid consumer-access window for
a species occupying buds? A positive *Mompha* observation when
the snapshot count of open flowers is zero is a negative-control
against treating **open flowers on the census day** as a necessary
condition for observing a floral-bud specialist. It is not evidence
of new oviposition on a no-flower day.

## Source files and exact temporal matching

The original Zenodo deposit
[10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509)
was reread with verified archive MD5
`151bbd516fc0032af2a2598cb5529c78`.
Two original experiments have flowering records dated **2023**,
not two independent years. The script
`scripts/analyze_slimon2026_plant_visit_stage_lag.py` joins the
author's original **weekly flower count** columns
`df2_exp1.csv`/`df2_exp2.csv` to **weekly new Mompha
observation** columns
`df2_exp1_M.csv`/`df2_exp2M.csv` by
`experiment × original plant ID × exact survey MM_DD`.
The original `main_exp*.csv` and `d_pheno*.csv` give each
plant's first and last recorded flowering.

A missing date, missing plant, missing count or source date
without a matching counterpart is **not filled with zero**.
The same plant's successive visits are **not independent
replicates**; the denominators here are explicitly plant-visits
for within-source description, not SMD sample sizes.

## Recovered stage/detection facts

| Measurement | Experiment 1 | Experiment 2 |
|---|---:|---:|
| Plants with four original source objects | 149 | 123 |
| Exactly matched survey dates | 11 | 9 |
| Exact-date matched plant visits | 1,468 | 987 |
| Plant-visits **before first recorded flowering** | 22 | 129 |
| Of these, Mompha-positive plant-visits | **1** | **28** |
| Mompha counts on those pre-first visits | 1 | 74 |
| Mompha-positive visits **within first–last window** | 405 | 191 |
| Of these, **zero open flowers** at visit | 290 | 156 |
| Visits **after last recorded flowering** | 455 | 361 |
| Mompha-positive visits after last | **0** | **0** |

**Experiment 2 has 17 further plant visits** with an unknown or
unreconstructable individual flowering window; five are
Mompha-positive, with 11 reported Mompha observations. They
are *not* reclassified as before or after flowering.

Per-phase source numbers are in
`data/source_reconstructions/slimon2026_exact_plant_visit_mompha_stage.csv`.
The source date-by-date verification is reproducible on the
official original archive using the included script and
`.github/workflows/slimon2026-plant-visit-stage-lag.yml`.
No original raw data are redistributed in this repository.

## Necessary denominator check: many zero-flower observations

Counting only Mompha-positive visits would misleadingly suggest that
buds/no-open-flower snapshots were **preferred**. Because the flower
surveys are discrete weekly snapshots, the baseline opportunity for
each class must be included:

| Original experiment | Positive / all visits with **zero open flowers** | Positive / all visits with **at least one open flower** |
|---|---:|---:|
| exp1 | **291 / 1,198 = 24.3%** | **115 / 270 = 42.6%** |
| exp2 | **188 / 877 = 21.4%** | **36 / 110 = 32.7%** |

Thus Mompha positivity at a weekly snapshot is **more frequent when
there are open flowers**, in both experiments. This does not conflict
with the known **bud-feeding** biology: open flowers may indicate
overall reproductive activity and correlated bud abundance, while the
visible Mompha stage may postdate oviposition. Crucially, these
numbers also **rule out the unsupported claim that the majority of
Mompha-positive no-open snapshots demonstrates preferential attack on
flowerless plants**.

The units of these comparisons are **repeated plant-visits**, not
independent plants or independent adult moths. Calendar season,
individual size, cumulative tissue exposure, shared environmental
conditions, and source detection stages are not controlled. There
is no valid source-certified hazard ratio or test of oviposition
preference. This contrast is a diagnostic of **detection timing and
resource opportunity**, not a causal biological preference estimate.

Machine-readable four-row receipt:
`data/source_reconstructions/slimon2026_plant_visit_open_flower_baseline.csv`.

### What the numbers support

1. **Open flowers at a weekly census are an invalid necessary-stage
   rule for identifying observed bud-borer activity.**
   More than half of Mompha-positive visits during the
   individual first–last flowering period have **zero open flowers
   at that visit** (290/405 and 156/191). This need not be a
   surprising or selective pattern, because even a
   continuously flowering plant can have no open flower on
   a particular weekly survey day; the proportion of **all**
   zero-open-flower visits must be considered before inferring
   preference.
2. **The observed Mompha-stage window can precede the first
   observed open flower.** Experiment 2 reports 28 pre-first
   positive plant-visits, consistent with the species' known
   bud-feeding biology, but also compatible with imperfect
   date/individual onset ascertainment and a delayed detection
   stage. We do **not** infer the exact oviposition day.
3. **No positive newly observed Mompha count occurs after the
   individual's last recorded flower** among the 455/361
   later matched plant-visits. This restricts the positive
   detection window within these particular surveys; it does
   not prove all prior larvae died, that insects were absent,
   or that the underlying attack hazard became zero.
4. This is one 2023 source programme with two distinct
   experiments, not 2 independent year-level replications.
   Correlation between plant flower totals and new Mompha totals
   may reflect plant size and survey opportunity as well as
   stage matching.

### Mechanistic next discriminator

To distinguish **bud exposure, realized larval detection lag,
and floral resource supply**, one needs flower **bud
abundance/ontogenetic stage** and a known Mompha oviposition or
newly initiated gall date on the *same plant/date*, recorded
before or independent of final fruit outcomes. A model of
Mompha new observations from open-flower count alone should
be compared with a source-defined **bud-stage availability**
model and, where justified, previous-visit host stage.
This archive documents the detection series but **does not
yet supply the relevant quantitative bud denominator**.
A retrospective fit alone would be descriptive, not a
held-out confirmation.

## Hard non-promotion boundary

*Mompha stellella* is a bud-boring antagonist, *M. brevivittella*
a fruit-seed consumer, and *Schinia florida* a distinct moth:
no cross-species adult-window substitution is acceptable. A
visible gall/count is not an independent adult-flight measure,
and the source `fitness_seed` is derived from fruit counts
and genotype coefficients rather than full individual intact
seed observations. Hence the original strict-H1 corpus
remains **mutualist 2 / antagonist 0 / mixed 0 independent
clusters**. Neither a new effect nor an additional
independent temporal treatment was admitted.

## Operational source-integrity note

One official Zenodo fetch timed out and another served bytes
that did not match the source's pinned MD5. The final successful
source retrieval and the original full-repo CI run independently
passed. The script always rejects unverifiable archive bytes and
never treats a transport failure as evidence that a biological
stage observation is absent.
