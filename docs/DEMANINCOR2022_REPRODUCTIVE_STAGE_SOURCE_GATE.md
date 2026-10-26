# 2022 greenhouse three-plant Osmia system — time reference versus later seed fate

**Date:** 2026-10-26. Status: source-hashed **exploratory original-data reanalysis**, NOT a confirmatory adult-fitness clock law or an IWE strict H1 effect.

Original data [Zenodo 10.5281/zenodo.17830772](https://zenodo.org/records/17830772) and de Manincor et al., *Global Change Biology* (2026), [DOI 10.1111/gcb.71074](https://doi.org/10.1111/gcb.71074). An entirely new 2022 experimental cohort, but the **same focal three plant species (*Collinsia*, *Nemophila*, *Phacelia*) and *Osmia lignaria*** as the authors' 2021 experiment already evaluated in IWE.

## Research question

The original paper reports that warming can preserve flowering–bee phenological synchrony while reducing mutualist visits and reproduction, and that seed germination and seedling survival respond differently. In IWE, test the falsifiable narrower question:

**Does actual independently dated bee density during floral display predict the fate of sampled fruit and F1 offspring more accurately than plant flowering season position or season-average adult abundance, at exactly matched source units?**

Do NOT presuppose that a richer biological time coordinate always improves prediction. The original outcome interpretation is already in the published study; this IWE model comparison was devised after source outcomes were seen.

## Three critical original-source fixes

**1. Original R-export columns.** All the tables were R `write.table` exports containing an *unnamed leading 1…N row index*. Reading them by whitespace/TSV header alignment without first verifying and removing this sequential index shifted every response. The source reader drops only exactly sequential leading indices, and rejects arbitrary unknown extra columns. ZIP MD5 `33ff77e05c3fb77141ec21226fa3c666`, original source R script MD5 `9347d7e1733ce4274a7551775ee5a71f`.

**2. True independent reproductive units.** There are **208 sampled flower/fruit rows**, comprising **120 source plant-prefix group keys**, nested in **60 original temperature × arena × plant-species groups**. Each such group contributes **six tested F1 seeds**, a total of **360 seeds**. The original pSEM tables repeat the same group-level `germ`, `cotyl`, and bee-nest outcomes across multiple fruit rows: **148 repeated observations** beyond the 60 F1 groups. In each of 60 groups, germ/cotyl/seeds-sown is exactly constant. Do NOT fit n=208 as 208 independent germination experimental units.

**3. Seeds and ovules arithmetic.** Original `seeds + undeveloped ovules = total ovules` holds for **208/208** source fruit rows, but the published derived `seed_set` fraction fails `seeds / total ovules` in **31/208 rows**. The predictor audit discards that unreliable derived fraction and recomputes the proportion from the self-consistent primitive seed/ovule counts. Germination and cotyledon fraction closure pass all groups.

## Actual time resolution and experimental level

Original independently observed bee abundance: **560 room × arena × DOY records** (=20 arenas × 28 bee census days). Original flower counts: **60 physical room × arena × plant-species groups**, plus nonphysical treatment totals that are *excluded* from group analysis. Across real groups, a mean **96.4%** of recorded bloom abundance is on dates with a same-arena bee census (range 79.4–100%). This exceeds the 2021 experiment's ~51.2% same-day coverage, though the protocols differ.

Four treatments (ambient A, W2, W4, W6) each occupy exactly **one greenhouse room** with five physical arenas. Group outcomes from the three plant species share each arena, and arenas share their temperature room. Thus temperature treatment is **not independently replicated at the room level**; 20 arenas are the within-room holdout units, NOT 20 independent warmed greenhouse experiments.

## Fixed exploratory within-room prediction comparison

60 plant-species × arena groups, each outcome averaged or counted **once per source group**, leave-one-entire-arena-out (20 folds, holding out all three plant species simultaneously). Same folds for all models; equal-arena RMSE; training-only standardized linear ridge λ=0.05; fixed species and room controls and log season-total open flowers.

- M0 = species + room + bloom amount
- M1 = M0 + bloom-weighted flowering mean DOY (calendar)
- M2 = M0 + source time-averaged arena bee count
- M3 = M0 + exact-date open-flower-count-weighted independent bee count
- M4 = M0 + bloom calendar DOY + matched bee count
- M5 = M0 + observed season-level visitation rate
- M6 = M0 + time-averaged bee count + matched bee count

Responses (never pooled numerically):
(i) `seeds / total ovules` recomputed from original sampled fruits aggregated to 60 groups;
(ii) `F1 germinated / 6 seeds sown` per group;
(iii) `F1 survived to cotyledon / 6 sown` per group.

| 2022 source outcome | M0 context | M1 calendar | M2 adult mean | M3 flower×bee exact dates | M4 calendar + overlap | M5 source visits |
|---|---:|---:|---:|---:|---:|---:|
| Sampled-fruit seed fraction | **0.13517** | 0.13719 | 0.13983 | 0.14010 | 0.14269 | 0.13294 |
| F1 germination fraction | 0.20782 | 0.19683 | 0.19709 | 0.20968 | **0.19453** | 0.20339 |
| F1 cotyledon survival fraction | 0.23563 | **0.22184** | 0.23120 | 0.23882 | 0.22286 | 0.23636 |

Interpret only **within-response** RMSE. M3 alone does not improve the M1 flowering-calendar benchmark in any of the three 2022 outcomes; it is worse in **12, 14 and 13 of the 20 arena folds** (seed fraction, germination, cotyledon survival respectively). The detailed win counts are 8/20, 6/20 and 7/20. A model containing both M1 calendar and M3 matched bees has a *tiny* advantage for F1 germination (0.19453 vs M1 0.19683), but not the other responses. Seven compared models, one experimental cohort and outcome-exposed choices preclude confirmatory significance claims.

## A stricter held-out ROOM/temperature stress test

The exact same 60 biological group responses were tested again by leaving an **entire original temperature room** out, with 4 folds (each holds 5 arenas × 3 species = 15 groups). **Room dummy predictors are removed from every comparator**, because a withheld room is an unseen treatment level. This tests transport across temperature/room domains but **cannot identify temperature causality**: one room per temperature remains completely confounded.

| Source outcome, room-held-out RMSE | M1 flowering calendar | M2 adult mean | M3 matched bloom×bee | M4 calendar + matched bloom×bee |
|---|---:|---:|---:|---:|
| Sampled-fruit seed fraction | 0.21096 | 0.19810 | **0.19255** | 0.20407 |
| F1 germination / six sown | 0.23607 | 0.25103 | 0.25877 | **0.22288** |
| F1 cotyledon survival / six sown | **0.23882** | 0.25822 | 0.26621 | 0.24142 |

**Sensitivity is biologically important:** On this different validation target, M3 alone *does* predict sampled-fruit seed fraction better than M1 and M2 (whereas it did not in leave-arena-out folds), but does NOT improve either germination or cotyledon survival. The calendar-plus-overlap model has its best F1 germination score, yet it adds parameters in only four independent room holdouts and model choices were response-aware.

Therefore **do not generalize the within-room negative result to a universal absence of flower–bee timing information**. The safer result is stage- and validation-grain dependence: any modest temporal exposure signal that appears in some fruit-seed predictions is not a stable standalone predictor of downstream offspring survival. Both evaluations use the same research programme, not independent replications. Never compare the RMSE magnitudes directly across the two distinct validation designs.

## Interpretation with the 2021 experiment

In the authors' 2021 greenhouse experiment (public Zenodo 7264150; IWE PR #102), matched-date bloom×bee density reduced **sampled-fruit seed formation RMSE** relative to plant flowering calendar by around 2% in a **different eight-arena design**. In 2022, at **60 grouped plant × arena × species units with F1 seeds**, the matched-date bee-window variable **fails** to beat a simpler calendar reference under **20 within-room arena holdouts**, while a different **four-room-out extrapolation** gives a modest gain for sampled-fruit seed fraction but **not** downstream germination or seedling survival.

The data therefore supply a **new directly source-tested boundary**: *temporal overlap can be well observed but offer no reproducible standalone incremental reproductive information beyond a simpler plant clock*. This is compatible with the 2026 author's demonstration that temporal synchrony alone need not sustain functional mutualism. The two years do NOT constitute a controlled paired two-year test of the same identical outcome/protocol, so **do not infer a statistically significant year interaction or a universal reversal**.

## Remaining limitations

- Adult date-specific density and flowers are arena/species-level, not individually observed exposure at each source-sampled flower.
- Sampled fruits and the subsequent six-sown-seed group test do **not** establish a traced individual maternal seed → germination → offspring survival chain; source group repetition is known.
- One room per temperature level. Room and temperature are inseparable; no causal warming effect or independent-treatment replication is identified.
- At most **20 physical arena holdout blocks** within four rooms; three co-planted taxa do not become three independent study programmes.
- Original paper and outcome variables were seen before model selection; this is a diagnostic reanalysis, not prospectively validated population-wide forecast.
- No antagonist or mixed pollinating seed-predator system is included, so no three-class IWE H1 contrast follows.
- Results do not demonstrate a causal bottleneck, experimental host compensation, or a general fitness superiority principle.

## Reproduce

Original-source MD5/ZIP audit: `scripts/probe_demanincor2022_stage_zip.py`; actual biological unit check: `scripts/audit_demanincor2022_reproduction_units.py`; held-out outcome models: `scripts/analyze_demanincor2022_grouped_stage_windows.py`.

Software fixture tests: `tests/test_demanincor2022_stage_zip.py`, `tests/test_demanincor2022_reproduction_units.py`, `tests/test_demanincor2022_grouped_stage_windows.py`. CI workflow: `.github/workflows/demanincor2022-stage-source.yml`. Source archived bytes remain on Zenodo; outputs are aggregated diagnostics only.

**Claim ceiling:** one additional 2022 cohort, zero new strict-H1 effect clusters, no generalized predictive-stage law.
