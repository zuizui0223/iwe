# Original Sinapis resource-supply versus visitation seed-production audit

**Date:** 2026-10-19  
**Status:** exploratory original-data test, not a phenological synchrony H1 effect, not a causal visitation treatment, not a pre-registered prediction model.

## Source and grain

Höfer et al. (2022), *Reduced seed set under water deficit is driven mainly by reduced flower numbers and not by changes in flower visitations and pollination*. Original [Zenodo 10.5281/zenodo.7335086](https://zenodo.org/records/7335086); all original source files are retrieved read-only and verified by frozen MD5. The source article already establishes the plant-resource-mediated drought pattern. IWE now compares the *incremental reproductive information* of floral visitor rates conditional on observed flower supply, using source IDs and experimental shelters.

- **53** original Sinapis arvensis individuals in **15 plots nested within 5 shelters**, three water treatments: Control, PrecipRed and Drought. Twenty source mother IDs are recorded, but do not supply 20 independent shelter treatments.
- Floral_traits.csv has seasonal flower totals, flowering duration, stem water potential, pollen receipt and **source-estimated total seeds per plant**.
- Int_data.csv has **427** original visitor taxon/group rows linked to original plant, mother, plot, shelter and water treatment. These are *nested categories*; they are not independent experimental plants.
- **50 plants** are complete on the primary flower+visitor+seed measures in all 5 shelters (11/8/8/11/12). They contribute **414 visitor-group records**; 3 of 53 are excluded for required original values missing. Water-treatment counts: Control 16, Drought 15 and PrecipRed 19.
- Visitor intensity is aggregated over the flowering-season observation days, NOT available as an independent day-by-day animal activity series. No adult phase lag or direct pollination-date overlap is inferred.

The response is **log(1 + source-estimated whole-plant total seed count)**, not intact viable seed survival, germination or lifetime offspring fitness. **Later original-component audit (PR #106): in all 50 source-complete plants this total is exactly pods × average seeds per pod within numerical rounding**; hence it is a deterministic **estimated product**, not an independently counted seed-fate endpoint. Further, **47/50 plants have a source pod count larger than the putative season-total `sumflower`**, so this flower index cannot be treated as a validated complete flower-opportunity denominator. The visitor-after-flower predictive gain is real for those recorded variables but does not by itself identify a **fruit-set conversion probability**. See [component audit](HOFER2022_FRUIT_SEED_CONVERSION_AUDIT.md). Predictors summarize the observed same field season; these are **retrospective, not pre-outcome forecasts**.

## Registered descriptive contrasts

For every model use the **identical 50 original plants** and leave **one whole source shelter** out of fitting, with equal weight for the five held-out shelter mean square errors. Each source plant has one outcome, even if its visitors were grouped into many taxonomic rows. The fixed model is training-fold standardized linear ridge regression (penalty 0.05); no per-model retuning after observing the holdouts.

| Model | Leave-whole-shelter-out RMSE |
|---|---:|
| M0 water treatment only | 0.76863 |
| M1 water + seasonal flower total | 0.48852 |
| M2 water + visitor groups' visit/flower/day rate | 0.79002 |
| **M3 water + flowers + visitor/flower/day** | **0.44172** |
| M4 seasonal flower total only | 0.47974 |
| M5 water + flowers + flowering duration | 0.48749 |
| **M6 water + flowers + visitor/day, not divided by flowers** | **0.44686** |

The author-defined **total flower supply** offers far more predictive information than water labels or visitation alone for estimated total seed production. On the same original plants, adding visitor information after the flower-count term **improves RMSE about 9.6%** (M3 vs M1), and **about 8.5%** with the independent daily visitor-rate coding M6 (no explicit denominator of flower number). Both conditional visit models improve per-shelter mean-square error in **4/5 original shelters**.

This resists a simple algebraic ratio objection: the improvement is not confined to visit/flower/day, which already divides by flower abundance. It **does not** establish a causal pollinator benefit or mechanistic resource × service interaction. Visitor abundance, maternal/genetic vigor, fertility, spatial variation, and assigned water treatments can be associated with unmeasured conditions.

## Possible pollen-receipt conversion layer

There are source-measured nonmissing stigma-pollen counts for just **29 of the 50** primary plants, spread over all five shelters. Refit all listed models to **the identical 29-plant subset**:

| Source pollen-subset model | Held-out shelter RMSE |
|---|---:|
| Water + flowers | 0.54770 |
| Water + flowers + floral visitor rate | **0.51489** |
| Water + flowers + stigma pollen grains | 0.59340 |
| Water + flowers + visitor rate + stigma pollen | 0.53339 |

Adding source stigma pollen does not improve these particular predictive comparisons. This is a limited *null boundary* for a small, likely selected subgroup: timing of pollen measurement and source tagged flower/final seed linkage are not established. It is **not evidence that pollen receipt generally does not matter** or that visits causally improve fertilization.

## Biological interpretation and IWE claim ceiling

A useful empirical pattern is that **plant reproductive opportunity (seasonal flower abundance) and observed visitation are not interchangeable explanations of total seed number**. Visit intensity alone can be uninformative yet become informative once floral supply is accounted for. This independently motivates a **conditional service-information** hypothesis complementary to the date-resolved three-plant Osmia finding, but it does not replicate a stage-specific timing prediction: **no daily animal window is measured here**.

Limitations:
- one year and five experimental shelters; plant and visitor-category rows are nested, not independent trials;
- treatment-vs-visitor causal mediation is not identified by observational visitor rates;
- counts refer to source-estimated whole-plant seed abundance, not sampled fruit seed fraction or independently observed viable offspring;
- models and this source were chosen after examining published ecological outcomes, so lower holdout RMSE is *exploratory*;
- pollen-stage subset is small (29 plants), possible missing-not-at-random selection;
- **no new strict-H1 effect** and no common meta-analytic effect size is constructed.

This programme therefore supports a **resource-versus-visitor conversion boundary**, not a universal reproduction advantage from phenological synchrony. Before a confirmatory cross-taxon claim, recover independent programmes with dated partner activity, measured flower/tissue receptivity, and later intact viable seeds at a linked biological unit; compare calendar, adult mean, exposure-aligned, and conversion-filter-only models using untouched years/sites.

## Reproduction

- Original public source gate: scripts/probe_hofer2022_resource_gate.py
- Direct original plant-level comparison: scripts/analyze_hofer2022_resource_limits.py
- Deterministic regression tests: tests/test_hofer2022_resource_gate.py and tests/test_hofer2022_resource_limits.py
- Original-source / full-project GitHub Actions workflows run on IWE PR #105.

Only metadata and derived source-validated analysis JSON files are stored in CI, never the original individual CSV rows.
