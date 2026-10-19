# Three plant species × one bee: can a dated interaction window predict seed set?

**Date:** 2026-10-19. **Status:** original-source exploratory test; independent of strict IWE H1, not a confirmatory effective-stage comparison.  
**Source:** de Manincor, N., Fisogni, A. & Rafferty, N. E. (2023), *Ecology Letters* 26:323–334, DOI [10.1111/ele.14158](https://doi.org/10.1111/ele.14158). Frozen 2021 greenhouse experimental original data [Zenodo 10.5281/zenodo.7264150](https://zenodo.org/records/7264150).

## Why this is more relevant to IWE than the maple annual result

The original experimental community has flowering and independent pollinator density observed by *calendar day*, plus measured seed/ovule state for individual sampled fruits. The three plants are:

- **CH** — *Collinsia heterophylla*
- **NM** — *Nemophila menziesii*
- **PC** — *Phacelia campanularia*

The focal partner is **Osmia lignaria**, with ambient C1–C4 and warmed (+4 °C) W5–W8 **eight arena-level exposure units**. This permits a *within-programme, cross-species* test of the partner activity × flowering window, without treating all plants within one arena as independent experimental treatments.

Source files, each retrieved from the exact frozen Zenodo record and verified by its published **MD5**:

| Original file | Original records | Essential measure |
|---|---:|---|
| `flower_onset.txt` | 318 | Plant-level first flowering DOY |
| `flower_count.txt` | 9,266 | Plant × DOY number of open flowers |
| `bee_density.txt` | 184 | Arena × DOY observed bee density |
| `seeds.txt` | 600 | Sampled fruit count of seeds and remaining ovules |
| `seedset_flowervisit.txt` | 234 | Per-individual summarized seed/ovule outcome and observed visitation rate |

## Original source-integrity funnel

The original `seedset_flowervisit.txt` **header contains nine whitespace tokens for eight-column source rows**. Its combined `plant sp` header must be read explicitly, rather than shifting seed and ovule columns. The script enforces the exact source schema and joins on **arena × plant species × original plant ID**.

Initial original-source reconciliation:

- **234** summarized sampled-fruit plant outcomes
- **1** has no matching original fruit record
- **3** have numerical seed/ovule disagreements between summary and raw records
- **47** more have at least one raw fruit record with seed or ovule count missing
- **2** more have no first-flowering date
- **181** match complete source fruit counts, onset and open-flower/bee-census observations
- **8/8 arenas** and **3/3 plant species** represented; species sample sizes **66 CH, 57 NM, 58 PC**

The denominator is **mature seed / (mature seeds + undeveloped ovules) in sampled fruits**, NOT every reproductive unit per mother plant, whole-lifetime total fitness, future seed germination or recruitment. Exclusions may be outcome-dependent; full/complete-case sensitivity and missingness are part of the audit, not hidden zero-filled outcomes.

## Frozen descriptive models: same plants, leave one entire arena out

Every model uses the same 181 individuals and the same eight held-out arena folds. In each fold, all continuous predictors are standardized **from training arenas only**. Models are unweighted, treating each sampled plant outcome as one observation, and ridge regularization of **0.05** is fixed throughout; no hyperparameter selection inside folds. Primary RMSE weighs the eight arena errors equally.

- **M0:** species + warming treatment + log cumulative observed open flowers
- **M1:** M0 + first flowering DOY (calendar only)
- **M2:** M0 + mean arena-wide adult bee density during census dates (non-window control)
- **M3:** M0 + **open-flower-count-weighted bee density on the exact matching census DOYs** (adult–host timing window)
- **M4:** M0 + first flowering DOY + window density
- **M5:** M0 + directly realized visits per plant, a different downstream observation

The new key *falsification* is whether **M3 improves on M2**, not merely on M0/M1. If the observed adult density averaged throughout the arena predicts just as well, an apparent plant-specific interaction-window benefit may be explained by a baseline abundance proxy, not special temporal alignment.

Window density is:

`sum_t[open_flower_count_i(t) × bee_density_arena(t)] / sum_t[open_flower_count_i(t)]`

over **exact days observed in both source files**. It is an *abundance-weighted bloom exposure*, not a signed plant/animal onset lag, verified pollen transfer per flower, or later reproductive stage. Missing bee-count days are excluded, **never** imputed as zero abundance.

## Initial non-confirmatory screening result

An independently calculated original-rows pilot, before the committed source-hashed CI run, yielded:

| Comparable model | Equal-arena held-out RMSE |
|---|---:|
| M0 context | 0.21081 |
| M1 + calendar flowering date | 0.21021 |
| M3 + bloom-weighted bee density | **0.20605** |
| M4 + calendar and bloom-weighted bee density | 0.20609 |
| M5 + realized visits | 0.21130 |

The improvement of M3 versus M1 is **0.00415 on a 0–1 seed-set scale (~2% relative)**. This is small, one programme, eight arenas only. The critical M2 comparison (non-window adult mean density) and ≥50% source-observed-flowering-coverage subset are computed by the new executable; do not promote the apparent timing-specific improvement until both are inspected.

**Major observation gap:** only approximately **51.2% of observed open-flower counts** fall on dates for which the same arena has a recorded bee-density observation, averaged across eligible plants. Missing census days cannot be treated as bees absent. The eight arenas were planted with three species simultaneously, so species-specific plant rows do not create three independent community-level experiments.

## Current claim ceiling

What is directly source-supported:

1. Multiple plants and three taxa share an experimentally established source design with open-flower calendars, independent bee-density dates and terminal sampled-fruit seed set on linkable biological IDs.
2. The adult-density × host-bloom predictor can be evaluated under identical sample/outcome and held-out arena groups against calendar and adult-density baselines.
3. An initial association of modest positive direction exists, subject to source-integrity execution, common-date observational gaps, alternate reference and missing-fruit selection.

**Not supported:** a statistically general advantage of deeper stage-specific timing, a causal role for floral overlap independent of temperature, a species-independent adaptive rule, an adult–larva phase model, a measured net plant lifetime fitness effect, or strict IWE H1 admission. The original article has already examined warming, phenology, visitation and reproduction; any apparent prediction improvement here is an exploratory *IWE time-reference and out-of-arena comparator*, not a new claim that warming depresses seed set.

## Reproduction

`python -m scripts.analyze_demanincor2023_service_window --outdir /tmp/iwe-3species-original`

No individual source files are redistributed. The job only uploads an MD5-verification/validation/results JSON and **24 derived arena×species summaries**, so future analyses cannot confuse nested raw records with independent exposure units.
