# Slimon & Agrawal (2026): genuine raw adult observations, but modeled seed fitness

Source archive: [Zenodo DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509).
Source material: `Freese Stats.zip`, `READ_ME_Phenological_plasticity.txt`;
experiment dates listed as spring–fall 2022 and 2023. Archive and
actual original R scripts were accessed in one GitHub-hosted,
**source-only** run. The original data/code are **not committed**.

## Biological question this independent antagonist programme raises

Two cohorts of *Oenothera biennis* exposed to different early-herbivory
conditions subsequently flowered earlier *and* continued flowering
later. The repository summary describes opposite effects at the two
ends of the flowering season: earlier flowering reduced seed-predator
damage, late flowering increased it, with the two effects largely
cancelling. The net plant outcome was largely associated with the
increase in flower/fruit production.

This is valuable source-level evidence against collapsing both
**the leading edge and trailing edge** into one generic "more
synchrony" or first-flowering-date effect. However, randomly assigned
early-herbivory treatment is **not** a randomized flowering-time shift;
the specific phenology-mediated biological path remains an interpreted
model component, not an isolated `do(flowering_onset)` effect.

## Original data, not a literature-summary guess

The run recovered both exact files (2026-04-09 Zenodo source record)
and their script/CSV schemas. The original **2022**
`df2_exp1F.csv` contains direct focal-host records of
*Schinia florida* adults on six dates (not merely egg receipt):

| 2022 adult observation date | Numeric plant records | Plants with positive counts | Sum of adult detections |
|---|---:|---:|---:|
| Jul 11 | 169 | 2 | 2 |
| Jul 12 | 169 | 1 | 1 |
| Jul 18 | 169 | 2 | 2 |
| Jul 20 | 169 | 3 | 5 |
| Jul 21 | 169 | 1 | 5 |
| Jul 26 | 169 | 3 | 3 |
| **Six-date total** | *repeated measures* | *repeated measures* | **18 detections** |

Eighteen is **not** 18 independently marked moths, and 169 is
**not** 169 independent adult-activity windows. Direct counts
are made on focal host plants, conditional on available/visited
flowers. Their coverage is limited to six dates and cannot be
extrapolated to unobserved later months as zero moth activity.

**Species-identity gate:** The archive also contains
`momphaCALC_exp1.csv`, `momphaCALC_exp2.csv`, and
`fflr_overlap_ex1.csv` / `fflr_overlap_ex2.csv`, whose original
README defines the latter as **flower–Mompha overlap** rather than
adult *Schinia* overlap. This is not the same interacting
seed-predator species as the directly counted adult *Schinia florida*.
Adult *Schinia* detections must **not** be used as a substitute
independent partner window for *Mompha stellella* seed predation.
The source archive's *Mompha* observations are counts of realized
host-associated stages, not a separately validated adult
availability curve.

The original 2022 `main_exp1.csv`, `df2_exp1F.csv`,
and `fitness_exp1.csv` share 153 original plant IDs (157 host
IDs, 169 *Schinia* observation IDs and 165 fruit-sheet IDs).
This is a **real record-linkage opportunity**, but it alone
does not establish an independent partner-window estimand or
an observed intact-seed fitness effect.

The 2023 `df2_exp2F.csv` has 951 rows and 123 unique plant
IDs shared with original host/fruit tables, but its four recorded
`sf_*` columns are **all larvae** (Jul 26, Aug 2, Aug 9 and Aug
16). Do not interpret the 951 rows as 951 independent plants,
or larvae as contemporaneous adult partner availability.

### Critical final-endpoint audit from original R code

The 2022 `exp1_pubver.R` defines, at source lines 93–95:

- `fitness_frt = total.frt - [schinia + 0.2*sm.brev + 0.2*lg.brev.FIT]`;
- `fitness_potential = total.frt + FINAL_Mompha`;
- `fitness_diff = schinia + 0.2*sm.brev + 0.2*lg.brev + FINAL_Mompha`.

The script also constructs `fitness_seed` as a
genotype-specific multiple of `fitness_frt` (source R lines
104–106). The 2023 `exp2_pubver.R` calculates an analogous
`fitness_frt` from fruit counts and weighted damage
(R lines 126–128), while the originally archived 2023 *Schinia*
time series consists of larval measurements only.

Therefore the paper's native **reconstructed reproductive
performance** is scientifically meaningful but is **not a
complete plant-by-plant observed, post-consumption intact seed
count**. The `0.2` weighting and genotype multipliers are
part of the original source model, not direct measurements
and must never be silently converted into a strict native
Hedges-g contract.

## Identification/admission decision

- Independent biological programme relative to older IWE sources:
  **yes**, conditional on the 2026 source metadata.
- Natural seasonal plant flowering data and predator damage:
  **yes**.
- Dated adult *Schinia* observations in 2022:
  **yes, focal-host conditional, sparse and not a full demonstrated
  independent seasonal availability curve**.
- Dated adult *Schinia* observations in 2023 source stage table:
  **no; larvae only**.
- Source-derived *Mompha* flowering overlap:
  **realized host-stage overlap**, not recovered independent adult
  *Mompha* flight or trapping. Species substitution from
  *Schinia* adult detections is forbidden.
- Correct-unit observed post-larval intact seed numbers:
  **not verified**; native seed fitness constructed from fruit
  counts and source damage coefficients.
- Strict antagonist-H1 effect/SMD: **not admitted**.
- Inferentially independent antagonist clusters added: **0**.
- Qualitative ecological use: **separate early/late window-edge
  effects and possible cancellation**, retained outside the
  confirmatory class-level claim.

The source-provenance table
`data/source_reconstructions/slimon2026_original_focal_stage_observations.csv`
pins the actual **2022 adult observation** dates/counts and
the 2023 larvae-only boundary. It is a source-inventory receipt,
not raw-data redistribution, a fitted exposure curve or an
invented effect.

Future reanalysis could use the original experimental programme
to investigate *how* induced changes at both flowering edges
jointly affect total fruit production and predator damage, with
genotype, cohort, repeated measurements and source-defined
fitness estimands preserved. Because the source abstract and
native model already expose the outcome, such a reanalysis would
be **exploratory**, not a blind preregistered confirmation.

**Stop rule:** without a documented adult availability curve
independent of focal reproductive outcome and actual terminal
plant fitness at the same biological unit, do not add this
candidate to strict-H1 or use 2023 larval counts as adult timing.
