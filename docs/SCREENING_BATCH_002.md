# Screening batch 002 — strict synchrony, seasonal timing and nonlinear antagonist responses

Date: 2026-09-17
Status: adjudication + estimand repair

## Main result

The literature is asymmetric in what it measures.

Mutualist studies relatively often measure both plant and pollinator timing and connect mismatch to seed or fruit production. Antagonist and mixed pollinating-seed-predator studies more often measure seasonal flowering position, attack/predation and final fitness without a single monotone partner-overlap exposure.

IWE therefore keeps three non-interchangeable evidence lanes:

1. **strict synchrony H1** — explicit overlap, absolute mismatch, verified one-sided mismatch, or a timing manipulation ordered by measured partner availability;
2. **direct seasonal timing sensitivity** — flowering date/seasonal position predicts reproductive outcome in a biologically identified interaction regime, but synchrony itself is not quantitatively identified;
3. **shape evidence** — partner timing and final fitness are matched, but the timing-fitness surface is nonlinear or bidirectional and cannot be represented by one H1 slope.

No study is promoted between lanes merely to balance interaction classes.

## Strict-H1 progress

### IWE001 — Corydalis ambigua × Bombus spp.

Kudo & Ida (2013) reports `mismatch_day = bee first detection - flowering onset`. The first extraction incorrectly treated the full signed lag as a monotone mismatch axis. After freezing `TIMING_METRIC_CONTRACT.md`, strict H1 was restricted to the one-sided `mismatch_day >= 0` domain.

Recovered site-level Fisher-z effects are:

| Site | n | r | native Fisher z | variance | oriented synchrony z |
|---|---:|---:|---:|---:|---:|
| NFP | 12 | -0.6371 | -0.7533 | 0.1111 | +0.7533 |
| TOEF | 8 | -0.8330 | -1.1978 | 0.2000 | +1.1978 |
| JOZ | 4 | -0.9518 | -1.8511 | 1.0000 | +1.8511 |

These share one programme dependence structure and are not three independent publications.

### IWE002 / IWE008

IWE002 remains the next high-value Corydalis extraction, but its sign convention differs from IWE001 and dataset overlap must be mapped first.

IWE008 is valuable because it directly compares flowering and key-pollinator peak timing and reports asymmetry between the two mismatch directions. It belongs high in the extraction queue once source-level effect/variance can be recovered.

## Mixed-system audit

### IWE015 — Silene stellata × Hadena ectypa

The early window is `Hadena ectypa`-dominant and the late window is co-pollinator-dominant. Final female reproductive success is reported as successful fruits after predation.

Published summary means are:

| Year | early n | early successful fruits | late n | late successful fruits |
|---|---:|---:|---:|---:|
| 2012 | 59 | 2.66 ± 2.95 | 58 | 3.91 ± 4.13 |
| 2013 | 55 | 9.77 ± 6.91 | 55 | 8.60 ± 7.01 |

The table heading labels uncertainty as `SE`. However, the same table gives bounded proportion summaries such as `0.59 ± 0.36`; with the stated sample sizes, interpreting `0.36` as a literal SE implies an impossible SD for a [0,1] variable. Therefore the earlier delta-method variances were withdrawn.

IWE015 is now stored only in `provisional_effects.csv` with `variance_unresolved`. It contributes no quantitative meta-analytic effect until the archived Dryad rows are inspected.

It is also not strict H1: early/late changes the identity mix of pollinators as well as Hadena exposure.

### IWE014

The older Silene–Hadena study remains biologically promising but has not yielded a source-level common-scale effect plus sampling variance. It stays unresolved rather than being promoted because it matches the narrative.

## Antagonist audit: nonlinear timing is common in the strongest systems

### IWE032 — Geum urbanum × Byturus ochraceus

Decision: `include_shape`.

The host is mainly selfing, the seed predator has a restricted activity window, and the paper explicitly defines off-peak flowering relative to predator activity. Predation occurs primarily in the first flowering peak and final seed-mass fitness is measured.

Predated plants show a quadratic plant-level fitness surface with maximum predicted total seed mass at about 36% of flowers in the second/off-peak period. A single linear synchrony effect would erase this biology.

### IWE033 — Cardamine pratensis × Anthocharis cardamines

Decision: `include_shape`.

The butterfly flight/egg-laying season is shorter than the plant flowering season, leaving temporal refugia before and after antagonist activity. Infestation strongly reduces realized fecundity and the flowering response is bidirectional. This is shape evidence, not a single signed H1 slope.

### IWE034 — Erigeron glaucus × Tephritis ovatipennis

Decision: `include_shape`.

Clone-level flowering synchrony, insect seed-head damage and annual viable seed production are measured together. Low-synchrony clones partly escape the tephritid by flowering into autumn, while viable seed success is lowest at intermediate synchrony. Again, a one-slope effect is inappropriate.

These three records are stored in `data/extraction/shape_evidence.csv`.

## Peucedanum status

IWE010/IWE011 remain biologically strong evidence for a seasonal enemy window: early flowering overlaps predator oviposition and experiences much higher seed predation. But current published designs do not yet provide the same continuously observed partner-overlap exposure as strict H1. They remain timing-sensitivity/context evidence rather than being forced into the direct synchrony meta-analysis.

## Consequence for hypothesis status

H1 is unchanged.

The nonlinear antagonist pattern was recognized during screening, after outcomes were visible. It is therefore not promoted to a new confirmatory hypothesis in this discovery corpus. `HYPOTHESES.md` now registers a screening-informed shape observation with an explicit rule: any confirmatory generalization about antagonist curvature must be tested on a prospectively defined holdout set.

## Current evidence diagnosis

- **mutualist strict H1:** feasible; direct candidates exist.
- **antagonist strict H1:** sparse; strongest studies often yield nonlinear or seasonal-window estimands.
- **mixed strict H1:** very sparse; rich mechanism literature but few direct synchrony-to-net-fitness estimates.
- **shape/timing-sensitivity evidence:** substantially richer for antagonist and mixed systems.

This evidence asymmetry is itself a potentially publishable measurement result, but no cross-class ecological conclusion is yet justified.

## Next extraction order

1. IWE028 — recover Tripolium × Paroxyna source-level attack/seed-set timing effect and sampling variance; highest-priority strict antagonist candidate.
2. IWE002 — recover the 2019 Corydalis workbook and map overlap with IWE001.
3. IWE008 — recover directional community mismatch effects and dependence structure.
4. IWE014 — quantitative recovery attempt for Silene vulgaris × Hadena.
5. IWE032/033/034 — recover compatible quantitative shape parameters where source data permit, without converting them into H1 slopes.
