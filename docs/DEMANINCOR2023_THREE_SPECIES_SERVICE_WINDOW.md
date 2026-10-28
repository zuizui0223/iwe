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

The original `seedset_flowervisit.txt` **header contains nine whitespace tokens for eight-column source rows**. Its combined `plant sp` header must be read explicitly, rather than shifting seed and ovule columns. The original `seeds.txt` also has **four rows with an empty, TAB-delimited ovule field**, while its seed-set and seed-mass fields remain present. Whitespace-splitting would shift columns and corrupt both fitness and model training: the corrected reader preserves all original TSV fields and treats the empty biological cell as missing, never as zero. The script enforces source checksum and schema and joins by **arena × plant species × original plant ID**.

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
- **M6:** M0 + open-flower-weighted mean DOY **on the same dates with a bee census** (temporal calendar-only control)
- **M7:** M0 + matched-day mean DOY + matched bloom×bee density
- **M8:** M0 + fraction of recorded open flowers on days with bee-density observations (coverage-only control)
- **M9:** M0 + matched-day mean DOY + coverage fraction
- **M10:** M0 + matched-day mean DOY + coverage fraction + matched bloom×bee density

The new key *falsification* is whether **M3 improves on M2**, not merely on M0/M1. If the observed adult density averaged throughout the arena predicts just as well, an apparent plant-specific interaction-window benefit may be explained by a baseline abundance proxy, not special temporal alignment.

Window density is:

`sum_t[open_flower_count_i(t) × bee_density_arena(t)] / sum_t[open_flower_count_i(t)]`

over **exact days observed in both source files**. It is an *abundance-weighted bloom exposure*, not a signed plant/animal onset lag, verified pollen transfer per flower, or later reproductive stage. Missing bee-count days are excluded, **never** imputed as zero abundance.

## MD5-verified empirical results (independent original Zenodo data)

The dedicated GitHub Actions original-data run now passes, independently reproducing the exact 181-plant original-data join and all model comparisons. Evidence is [source run 39222729826](https://github.com/zuizui0223/iwe/actions/runs/39222729826) and the full IWE software suite [CI 39222780364](https://github.com/zuizui0223/iwe/actions/runs/39222780364). **These are exploratory, response-exposed model choices, not a prospective held-out-study performance estimate.**

| Fixed source-comparable prediction model | Leave-one-ARENA-out RMSE, equal arena weights |
|---|---:|
| M0 species + warming + total flowering | 0.21081 |
| M1 + first flowering DOY | 0.21021 |
| M2 + **adult bee mean density alone** | **0.22138** |
| M3 + **open-flower × actual bee census DOY** | **0.20605** |
| M4 + first flowering DOY + bloom×bee | 0.20609 |
| M5 + measured visits to individual plant | 0.21130 |
| M6 + **bloom center DOY on observed bee-census dates** | 0.21473 |
| M7 + observed-day bloom center DOY + bloom×bee | 0.21084 |
| M8 + fraction of flowering observed on bee census dates | 0.20962 |
| M9 + observed-day bloom center DOY + coverage | 0.21374 |
| M10 + calendar DOY + coverage + bloom×bee | 0.21127 |

The M3 interaction-window measure predicts sampled fruit seed formation **better than** an adult-abundance-only reference (M2), absolute first flowering day (M1), and calendar position on the **same bee-census days** (M6), under a fixed identical plant subset and leave-one-arena-out workflow. Relative to M1 the M3 RMSE reduction is **1.98%**; versus M2 **6.92%**. The gain is small, and adding the other predictors (M7/M10) *worsens* held-out accuracy relative to M3, so "more temporal detail always improves reproduction prediction" is directly unsupported.

The gain is heterogeneous among the eight true grouped validation units. M3 has smaller within-arena MSE than M1 in **4/8 arenas**, versus M2 in **5/8**, and versus M6 in **4/8**. These arena signs forbid a universal treatment/plant-species conclusion. They are not 181 independent confirmations, nor three independent experimental programmes.

### A stricter calendar-shift falsifier

Within each of eight arenas, cyclically shift the bee-density values over the original **23 bee-census dates** without changing the plants' flowering dates, original observation coverage, abundance distribution, source outcome, or leave-one-arena-out folds. The same survey-index shift is applied across all arenas.

- Unshifted genuine bloom×bee M3 RMSE: **0.20605**
- Median M3 RMSE among the **22 nonzero shifts**: **0.21280**
- Unshifted phase ranked **2nd of 23** in the sense that two shifts (including the true one) yield equal or better error
- With matched calendar and coverage controls M10, **3/23** shifts yield equal or better error than the true alignment

The real alignment is unusually good **within this small diagnostic set**, but this is not a valid randomly assigned treatment, preregistered shuffle test or calibrated P-value. Cyclic wrapping may break continuous seasonality, source coverage is sparse, and the study was selected after reviewing the outcomes.

### Incomplete sampled fruits and sparse bee-census day sensitivity

**Original strict complete-case**: 181 plants, 66 *Collinsia*, 57 *Nemophila*, 58 *Phacelia*. The observed fraction of each plant's recorded flowering represented on a bee census date averages **51.2%**. No missing bee density is set to zero.

Restricting to plants with at least **50%** of flowering observations on coincident bee days produces **87 plants in all eight arenas**; the M3 leave-one-arena-out RMSE is **0.18646**, versus M1 **0.19621**, M2 **0.21702** and M6 **0.20191**. The sample is selected after source observation and not a randomized robustness trial.

**Partly missing original sampled fruits**: exactly **47** additional plants have one or more fruit rows with unknown raw seed/ovule counts, but their *available raw fruit sums still match the author's summarized observed outcome*. Including only these recorded observed totals as a sensitivity (never inventing any missing seeds) expands the dataset to **228 plants** from the same eight arenas. On this broader observed-output basis, M3 RMSE is **0.19495**, versus M1 **0.19800**, M2 **0.20063**, M6 **0.20118** and M9 **0.20045**. The direction of the small gain survives this missingness scenario, but the true unobserved fruit outcomes remain unidentified; these 228 are not 228 plants with complete lifetime reproduction.

### Ecological interpretation

The direct and novel-to-IWE comparison is not that warming changes phenology, visits, or seed set — the original article already establishes such effects. It is a **time-reference test**: in this experimental community, an independently observed bee census weighted by the dates flowers are receptive explains a little more held-out sampled-fruit reproduction than abundance averaged across the whole observed season, or absolute flowering calendar position. A strong mechanistic/causal interpretation remains open because the same paper supplies **one community, one year, eight arenas**, and abundance, resource supply, flower-stage effects, and treatment differences coexist. It is an **adult-service timing test**, not the downstream larval conversion bottleneck proposed for antagonists and mixed seed predators.

## Current claim ceiling

What is directly source-supported:

1. Multiple plants and three taxa share an experimentally established source design with open-flower calendars, independent bee-density dates and terminal sampled-fruit seed set on linkable biological IDs.
2. The adult-density × host-bloom predictor can be evaluated under identical sample/outcome and held-out arena groups against calendar and adult-density baselines.
3. The MD5-verified original-data source run shows a **small** positive predictive difference that survives the mean adult-density, matched-day calendar, bee-census coverage, phase-shift and partial-fruit-record sensitivity checks, but does not repeat in every arena.

**Not supported:** a statistically general advantage of deeper stage-specific timing, a causal role for floral overlap independent of temperature, a species-independent adaptive rule, an adult–larva phase model, a measured net plant lifetime fitness effect, or strict IWE H1 admission. The original article has already examined warming, phenology, visitation and reproduction; any apparent prediction improvement here is an exploratory *IWE time-reference and out-of-arena comparator*, not a new claim that warming depresses seed set.

## Reproduction

`python -m scripts.analyze_demanincor2023_service_window --outdir /tmp/iwe-3species-original`

No individual source files are redistributed. The job only uploads an MD5-verification/validation/results JSON and **24 derived arena×species summaries**, so future analyses cannot confuse nested raw records with independent exposure units.
