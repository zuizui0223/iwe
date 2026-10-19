# Sinapis: does visitor information appear in pods or seeds per pod?

**Date:** 2026-10-19. **Status:** original-data exploratory component analysis, not a flowering–animal synchrony effect, causal mediation, or a strict IWE H1 effect.

**Source:** Höfer et al. (2022), original public [Zenodo 10.5281/zenodo.7335086](https://zenodo.org/records/7335086). Frozen source MD5 validated. Parent analysis [HOFER2022_RESOURCE_SERVICE_LIMITING_STAGE_AUDIT.md](HOFER2022_RESOURCE_SERVICE_LIMITING_STAGE_AUDIT.md).

## Critical source-grain correction: pods exceed the reported flower index

The live source workflow recovered **50 identical plant IDs** from 53 original Sinapis plants, across **15 plots in 5 shelters**. Every admissible plant has a recorded source pod number and source average seeds per pod, but **47/50 plants have more recorded pods than the variable called `sumflower`**, with a median pods / `sumflower` ratio of **2.2946**.

The source README describes `sumflower` as season-total flower production; yet this observable contradiction demonstrates that the *recorded flower quantity* is NOT a defensible complete denominator of the eventual pods for these plants without resolving sampling grain or data semantics. **Do not** interpret `pods/sumflower`, `seedsperplant/sumflower`, or any model on these derived ratios as fruit set per flower or effective conversion rate. They were excluded from the admitted stage models after detecting the original-data mismatch. Using the flower observation variable as a *predictor/index* is possible; treating it as a calibrated number of all reproductive opportunities is not.

The author source's estimated total seed production is strongly algebraically linked to pod number × source mean seeds per pod. An apparent association appearing in both pod number and total estimated seed count therefore does NOT furnish independent source replication or a fully traced seed-fate pathway.

## Independent component outcomes retained

On the same 50 source-complete individuals and original five sheltered physical groups, separately model:

- **Pods/plant**: `log1p(pods)`, cumulative fruit number (not pod set probability).
- **Mean seeds/pod**: `log1p(avgseed)`, source's within-fruit seed count indicator (not seed viability).
- **Estimated total seeds/plant**: `log1p(seedsperplant)`, retained for reference and algebraic audit only.

Use the same response-matched source plant observations and equal-weight leave-one-**shelter**-out predictive comparisons, with training-only standardized linear ridge (fixed 0.05), never treating 414 visited taxon/group records or 15 plots as independent shelter treatments. **Never compare the absolute RMSE of differently transformed stage responses; only relative improvements within a fixed response.**

## Original source-derived results

An independent, MD5-verified original-data execution at [GitHub Actions 39232690865](https://github.com/zuizui0223/iwe/actions/runs/39232690865) reported:

| Source outcome (all n=50, 5 shelters) | Water + flower index RMSE | Add visitor/day RMSE | Relative improvement | Shelters improved |
|---|---:|---:|---:|---:|
| Count of pods per plant | 0.54436 | **0.47570** | **12.6%** | 4/5 |
| Source mean seeds per pod | 0.15433 | **0.14386** | **6.8%** | 3/5 |
| Author-estimated total seed count | 0.48852 | **0.44686** | **8.5%** | 4/5 |

Using author visitor/flower/day instead produces relative reductions **15.2%**, **8.9%**, and **9.6%**, respectively, against each outcome's water + flower-index baseline. The independent visitor/day coding does not explicitly divide by the flower index, weakening a simple mathematical-ratio explanation.

### Alternative environmental/seasonal predictors

The source measured continuous stem water potential (SWP), as well as flowering duration. On the **same original plants**:

- Pods: water treatment + flower index + SWP RMSE **0.54678**; adding visitor/day **0.48331**. Visitor information continues to improve 4/5 shelters.
- Seeds/pod: adding flowering duration alone yields **0.13662** versus flower-index baseline **0.15433**, improving all 5 shelters. This is numerically better than adding visitor/day **0.14386**, suggesting that available plant-season duration carries additional information about within-pod seeds.
- Estimated seeds: water + flower index + SWP **0.49222** versus + SWP + visitor/day **0.45162**. No causal water × visit interaction is identified.

### What survives—and what does not

This **single-study, post-outcome model comparison** suggests that visitor observations may be more informative about the number of eventual pods than about the average number of seeds within each pod *under these fixed models and data*. It does NOT prove visit-mediated fruit formation, nor statistically identify a difference between stage-specific effects: all three outcomes partly share the same measured quantities and five shelters are insufficient for robust universal inference.

The apparent advantage of visitation after controlling the reported flower index cannot automatically be described as a post-flowering biological conversion gate. Because `sumflower` and pod counts demonstrably have incompatible observed magnitudes, resource/flower-supply adjustment is imperfect and the visitor slope may proxy latent display, microhabitat, maternal effects or other shared factors.

The observed **within-pod flowering-duration signal** is a useful falsifiable boundary: longer reproductive opportunity could relate to pod seed count independently of visitor pressure, but it is not a measured time-to-ovule maturation effect.

## Next meaningful verification

A source-correct biological stage test would need **individually tagged flower-to-fruit fates** or a demonstrably complete floral opportunity denominator plus later intact viable-seed results, with dated visitor windows on those same tagged plants. This source lacks that contract. Keep it as **resource-conditional correlational evidence**, not a strict H1 or a general timing-law support.

## Reproduction and status

Code: `scripts/analyze_hofer2022_conversion_components.py`; tests: `tests/test_hofer2022_conversion_components.py`; original-source GitHub Actions: `.github/workflows/hofer2022-fruit-seed-conversion.yml`.

The final script exports only a derived numerical report with source-count inconsistency flags; source rows remain in the original Zenodo archive. All source analyses preserve frozen main H1 mutualist 2 / antagonist 0 / mixed 0 independent clusters.
