# Screening batch 001 — interaction-window evidence

Date: 2026-09-16
Status: first-pass screening; effect extraction not yet complete

## Purpose

This batch is the first empirical screen for IWE. It applies the frozen primary question:

> Does the effect of greater plant–animal phenological synchrony on plant reproductive performance differ among mutualists, antagonists, and mixed pollinating seed predators?

The batch is deliberately conservative. Famous nursery-pollination systems are not admitted to Tier A merely because both phenology and fitness have been studied somewhere in the system. The timing exposure and reproductive outcome must be linkable within the same biological context.

## Search strata used

The first pass targeted:

- plant–pollinator phenological mismatch with seed/fruit outcomes;
- experimental flowering-time shifts with reproductive outcomes;
- predispersal seed predators interacting with flowering phenology;
- `Hadena × Caryophyllaceae` nursery pollination;
- `Epicephala × Phyllanthaceae` nursery pollination;
- `Ficus × Agaonidae` timing studies;
- `Trollius × Chiastocheta` nursery pollination;
- `Lithophragma × Greya` nursery pollination.

Search terms combined variants of `phenological mismatch`, `flowering time`, `pollinator emergence`, `seed set`, `fruit set`, `seed predation`, `pollinating seed predator`, `nursery pollination`, and focal system names.

## Batch counts

Twenty-one publications were registered.

| Candidate class | Include | Unresolved | Context only | Total |
|---|---:|---:|---:|---:|
| mutualist | 4 | 3 | 2 | 9 |
| antagonist | 0 | 3 | 1 | 4 |
| mixed pollinating seed predator | 2 | 1 | 5 | 8 |
| **Total** | **6** | **7** | **8** | **21** |

`include` means the publication currently appears to satisfy the biological Tier-A screen and should proceed to quantitative extraction. It does not mean an effect size has already been recovered or that the study will survive variance/dependence checks.

## First extraction queue

### Mutualist

1. `IWE001` — Kudo & Ida 2013, *Corydalis ambigua* × overwintered bumblebee queens, DOI `10.1890/12-2003.1`.
   - Direct multi-year mismatch and seed-set data.
   - Strong Tier-A candidate.
   - Must be dependency-mapped against later Corydalis papers.

2. `IWE002` — Kudo & Cooper 2019, DOI `10.1098/rspb.2019.0573`.
   - Nineteen-year monitoring plus snow-removal experiment.
   - Direct mismatch-to-seed-production evidence.
   - Potential data overlap with IWE001.

3. `IWE004` — Kehrberger & Holzschuh 2019, *Pulsatilla vulgaris*, DOI `10.1038/s41598-019-51916-0`.
   - Flowering timing, pollinator activity/visitation and seed set in matched grasslands.
   - Raw-data route reported.

4. `IWE005` — Rafferty & Ives 2012, DOI `10.1890/11-0967.1`.
   - Experimental flowering-time shifts.
   - Seeds produced after pollinator visits provide a direct reproductive response.
   - Two focal plant species may provide separate biological units while retaining publication-level dependence.

### Mixed pollinating seed predator

5. `IWE014` — Pettersson 1991, *Silene vulgaris × Hadena*, DOI `10.1111/j.1600-0587.1991.tb00632.x`.
   - Same partner contributes pollination and seed predation.
   - Early versus late flowering changes predation while final seed set is available.
   - Full quantitative extraction is required to establish recoverable variance.

6. `IWE015` — Zhou et al. 2020, *Silene stellata × Hadena ectypa*, DOI `10.1111/evo.13965`.
   - Early/late seasonal windows differ in the contribution of the pollinating seed predator.
   - Direct reproductive data and archived raw data are reported.
   - Year and sex-function outcomes must remain dependent rather than being treated as independent studies.

## Unresolved high-value studies

The most important unresolved records are:

- `IWE003` — Liew & Kudo 2026: likely usable but population/year overlap with earlier Corydalis studies must be mapped.
- `IWE007` — de Manincor et al. 2023: reproduction declines under warming, but warming alters multiple plant/pollinator traits as well as phenology; a mismatch-specific effect must be isolated.
- `IWE008` — Wang et al. 2024: explicit pollinator–flowering peak mismatch and seed setting across an alpine community; quantitative extraction and dependence structure need full-text/data adjudication.
- `IWE010` / `IWE011` — Kudo & Shibata 2021/2025: strong antagonist timing systems, but the strict synchrony-to-net-reproduction effect must be reconstructed and the two publications are likely dependent.
- `IWE012` — Valdés & Ehrlén 2017: seed predators reverse flowering-time selection, but partner activity is not yet represented as an explicit overlap metric.
- `IWE019` — Liu et al. 2014: direct fig/fig-wasp phenology and abortion during a poorly matched crop, but the plant-fitness estimand is not yet clean enough for Tier A.

## Important negative result of the screen

The classic nursery-pollination literature contains abundant evidence for pollination benefits, larval costs, specialization, host tracking, and variation among years or populations. However, many canonical papers do **not** directly estimate the IWE primary relation:

`phenological synchrony -> final plant reproductive performance`.

Examples currently retained as `context_only` include Epicephala host tracking, the foundational Japanese Glochidion–Epicephala study, Trollius–Chiastocheta cost/benefit work, and Lithophragma–Greya mutualism/redundancy studies.

This gap must not be repaired by relaxing the Tier-A definition after seeing the literature.

## Emerging design issue: antagonist timing versus explicit synchrony

Antagonist studies often measure plant flowering time and show that seed predators attack early or late flowers, but do not independently estimate an animal activity curve. IWE therefore keeps two concepts separate:

1. **strict synchrony evidence** — plant timing is explicitly matched to partner activity/availability;
2. **direct seasonal-timing evidence** — plant timing predicts antagonist exposure/fitness but the partner activity curve is not directly quantified.

The first remains eligible for the primary H1 model. The second may later form a predeclared sensitivity analysis, but it will not be silently promoted into the primary dataset.

## Dependence risks already identified

- Corydalis programme: `IWE001`, `IWE002`, `IWE003` may share populations and years.
- Peucedanum programme: `IWE010`, `IWE011` likely share sites and/or years.
- Silene stellata–Hadena programme: multiple publications share the same focal population/system and may share years.

Publication count therefore cannot be used as the effective sample size.

## Next quantitative tasks

1. Recover source/raw data for IWE001, IWE002, IWE004, IWE005, IWE014 and IWE015.
2. Freeze a dataset-overlap map for the Corydalis and Peucedanum publication families before effect estimation.
3. Determine the native effect form in each source (slope, correlation, experimental contrast, or reconstructable response ratio).
4. Recover sampling variance without automatic imputation.
5. Admit effects only after direction can be oriented as `greater synchrony -> higher plant reproductive performance`.
6. Separately adjudicate whether IWE008 and the antagonist timing papers qualify for strict H1 or only the broader sensitivity analysis.

No pooled ecological result is reported from this batch. Screening status is not biological evidence.
