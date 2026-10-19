# IWE — Long-term maple source: individual versus population temporal information

Source: Crone & Rapp (2025), American Journal of Botany, DOI 10.1002/ajb2.70046. Author-deposited original data: https://zenodo.org/records/15090572 (DOI 10.5281/zenodo.15090572).

Audit date: 2026-10-19. Status: exploratory, observational, **one original research programme**. This is NOT strict IWE H1 evidence, partner-stage synchrony, or an independent replication of effective-stage forecasting.

## Original data and biological meaning

Spring flowering observations cover 20 marked trees per year in 2012–2024 (260 original tree-year observations). The same years have 260 autumn standardized seed-count records. The literal tree × calendar-year join gives **259 matched observations**. The one unmatched record is autumn HF28 in 2022, with no spring census row; its zero sampled seeds do not license inserting an unobserved zero spring category. Across 2011–2024 the archive contains 280 seed-count rows; 2011 supplies a previous-year seed index for the 2012 model.

Spring categories score none=0, low=1, medium=2 and high=3. This is a rough ORDINAL flowering-effort measurement, not a calendar flower date, exact flower number, partner activity curve, or synchrony.

Autumn seed numbers count seeds during the source's standardized 30-second tree survey, with total.count = EC.count + JR.count. The outcome is log(1 + sampled seed count), NOT intact/viable seed output per tree. The 2012–2017 samara evaluation in the earlier IWE audit is a different sample and cannot be substituted for this endpoint.

## Models and independence contract

Compare a constant model, the focal tree's own spring flowering category, odd/even calendar year, a community reference calculated as the **other 19 trees' average** (excluding focal flowering mechanically), and small additive combinations.

Validation is leave-one-whole-year-out (LOYO), never holding out one tree but training on others observed during the same test year. There are at most **13 calendar-year blocks**, with repeated trees at one forest, not 259 independent experiments or population replications.

For 2018–2024 evaluation, hold out all later calendar years when fitting on 2012–2017 data. Here a preceding autumn (year t−1) seed-count predictor is temporally available before year t. It is intentionally **forbidden in LOYO**: a training row from t+1 would contain the held-out year t's actual seed outcome as a predictor, contaminating test inference. The chronological comparison is a retrospective test of fixed simple formulas, not a prospective pre-registered deployment.

## Original source results: full 2012–2024 panel

259 matched tree-years, 13 annual blocks. Endpoint: RMSE of predicted log(1 + autumn sampled count); smaller is better.

| Model | LOYO RMSE |
|---|---:|
| Constant | 1.75779 |
| Calendar odd/even parity | 1.46302 |
| Population spring category alone | 1.37419 |
| **Focal spring category alone** | **1.29410** |
| Focal + odd/even parity | 1.28718 |
| Focal + other-tree spring | 1.28552 |
| Focal + other-tree spring + parity | 1.30542 |

This is compatible with a strong individual spring-effort indicator for eventual autumn seed rain, but it is partly a straightforward pattern of trees with **no spring flowers and no autumn seeds**. Those easy zeros can artificially make a seasonal predictor look better. This does not identify pollination benefit or downstream herbivore cost.

## Restrict to actively flowering trees (response-independent)

Before examining autumn seed outcomes, use spring observations to require: (1) at least five of 20 marked trees flowering during the year; and (2) the focal tree itself flowering. That leaves **179 tree-years across 10 years**: 2012–2017, 2019–2021, 2023. This excludes 2018, 2022 and 2024 based solely on the paucity of source-observed spring flowers.

| Model | LOYO RMSE |
|---|---:|
| Constant | 1.84891 |
| Calendar parity alone | 1.67956 |
| Population spring category alone | 1.58575 |
| **Focal spring category alone** | **1.54977** |
| Focal + parity | 1.53353 |
| Focal + other-tree spring | **1.50022** |
| Focal + other-tree spring + parity | 1.55393 |

Focal flowering still beats the two-year calendar clock in this restricted dataset. Adding other trees' spring flowering improves the focal-only RMSE by only about **3.2%** and fails to yield consistent large gains once parity is also included. The reference-model differences have NOT been evaluated as confirmatory causal effects, and the inclusion filter was formalized after seeing the original archive.

## Fixed 2012–2017 train / 2018–2024 historical future test

The actively flowering subset has 103 training tree-years from 2012–2017 and 76 testing tree-years from just four later flowering seasons (2019, 2020, 2021, 2023). Test years with no active flowering were excluded by the spring-only rule.

| 2012–2017 model | Later test RMSE |
|---|---:|
| Focal spring only | 1.51401 |
| Focal + odd/even parity | 1.46999 |
| Focal + other-tree spring | 1.50066 |
| **Focal + previous autumn seed abundance** | **1.44012** |
| Focal + other-tree spring + parity | 1.49070 |

Previous autumn seed abundance may carry a modest additional signal. It is not proof of resource depletion or selection mediated by animals. Alternate bearing, climate, maternal resources, sex allocation and seed-count sampling can all cause a historical relationship. The historical train/test split was evaluated in this exploration after inspecting the long series.

## Scientific conclusion for IWE

At this original study and its annual temporal resolution:

- Focal flowering effort can predict autumn sampled seed abundance better than a simple parity clock, including among already-flowering trees.
- Population-scale flowering, reproductive history, and season can contribute modestly and inconsistently beyond focal flowering; no stable, large added population-synchrony advantage has been demonstrated.
- This is a cross-scale **negative/boundary control**, not validation of stage-specific plant–animal synchrony. No dated partner adult window, oviposition, larval developmental lag, same-unit mature viable seed outcome, or multi-site replication is observed.

The main IWE question remains: **does a response-independent effective encounter/developmental-stage coordinate predict final viable reproduction better than host calendar, adult timing and simpler resource/survival baselines, in independently held-out biological units?** This maple archive cannot answer that question. It should remain a bounded descriptive case, not accumulate more same-source analyses as independent support.

## Reproduce

Run: python -m scripts.analyze_maple_crossscale_2012_2024 --outdir /tmp/iwe-maple-13yr

The script fetches the two exact public original Zenodo files, verifies their MD5 signatures and original count identities, and saves ONLY a 13-row annual aggregate and model-diagnostic JSON, without redistributing the original tree data.

Tests: tests/test_maple_crossscale_2012_2024.py

Actions: .github/workflows/maple-crossscale-13years.yml

Strict IWE class corpus remains mutualist 2, antagonist 0, mixed 0 dependence clusters; no new meta effect is promoted.
