# ALAN × IWE × chocho: reproductive outcomes and pollinator-access scope

> **2026-11-24 cross-repository source-availability correction (later than this historical review).** The below text records the **2026-11-14 acquisition state**. On **2026-11-21**, the separate `zuizui0223/alan` repository recovered the publisher-issued S4b supplementary DOCX (198,613 bytes, original SHA256 `c9cc7ea119c6a99bcfee2b6956c76988c73cf776f20944f5570d00101c3e3abe`) and extracted **all 12 reported S4b light contrasts**. See [ALAN primary-source scope](https://github.com/zuizui0223/alan/blob/main/database/alan_experiments/lu_jpe_sources/README.md), [S4b original reported table](https://github.com/zuizui0223/alan/blob/main/database/alan_experiments/lu_jpe_sources/table_S4b.csv), and [new cross-repo covariance analysis](https://github.com/zuizui0223/alan/blob/analysis/alan-arthropod-search-expansion-20261122/docs/ALAN_LU_JPE_FUNCTIONAL_BUFFERING_COVARIANCE_GATE_20261124_ja.md). The original statement "Table S4b unavailable" is therefore **historical and no longer current**. For *P. kansuensis* seed-set, the primary S4b **Unlit−Lit** coefficients are Open **+0.0445 (SE 0.0319)** and Nocturnal **+0.1332 (SE 0.0429)**. The model-scale contrast `(Lit−Unlit)_Open−(Lit−Unlit)_Night` has point estimate **+0.0887**, but its joint standard error **cannot be identified** without the shared experimental-block covariance (Cauchy–Schwarz range 0.0110–0.0748). The original model scale and independent lighting-unit covariance remain unresolved: this is **not** a percentage-point effect, a valid confidence interval, a demonstrated daytime compensation mechanism, or an additional independent experiment. The full main article Methods and original plant-level allocation are still unavailable here. Preserve all 2026-11-14 historical results below; do not recode missing published values as zero.

## Correction after full-text inspection — 2026-11-14

**The Lu JPE 2026 −56% seed-set figure must be scoped to NIGHT-ONLY access, not unrestricted/open pollination or total plant seed production.** The preceding abstract-based version of this report omitted that experimental condition. The accepted manuscript Results p14 reports the seed decline in the nocturnal treatment rather than the other two access treatments; its Discussion p16 supplies the 56.0% figure. Table S4b and original observations remain unavailable.

Full correction, primary-source page map, 12 contrasts and the future matched-access effect estimand: [Lu night-only versus open seed effect](LU2026_NIGHT_ONLY_VS_OPEN_SEED_EFFECT_CORRECTION_20261114.md).

The original pre-correction report is retained in [commit 2b3e0af](https://github.com/zuizui0223/iwe/blob/2b3e0afc264c7b1dcd49430e689cc7ca75f99298/docs/ALAN_REPRODUCTIVE_FUNCTION_OUTCOME_GATE_20261114.md) for provenance, not as the current interpretation.

## Original evidence inventory

The ledger contains nine source entries: eight paper-level manipulated-light reports and one secondary day/night exclusion literature synthesis with observational prior satellite light. These are not nine verified independent light experiments. In particular, the two Lu 2026 publications may share experimental infrastructure; block identity has not been established.

### Lu: access-specific pollen and reproductive endpoints

Lu et al. *Journal of Plant Ecology*, DOI [10.1093/jpe/rtag160](https://doi.org/10.1093/jpe/rtag160), established five paired lit/unlit plots in 2024. The same source compares two species with differing selfing capacity and visitor dependence.

| P. kansuensis access treatment | Source-reported pollen change under light | Source-reported seed-set response |
|---|---|---|
| Open day and night | −23.09% | No significant effect reported; point estimate not recovered |
| Day only | No significant effect reported; point estimate not recovered | No significant effect reported; point estimate not recovered |
| Night only | −53.80% | −56.0% scoped from Results/Discussion; Table S4b not retrieved |

Seed set is developed seeds divided by ovules per fruit (Methods p11). None of these is a count of viable seeds per whole plant. Open and day-only nonsignificance is not an exact zero, equivalence or proven full compensation.

The source also reports −49.1% nocturnal Lepidoptera visits on P. kansuensis while total nocturnal visitation remained similar and Diptera increased. Per-visit pollen effectiveness was not measured. E. regelii showed no significant pollen or seed response across access treatments and no observed night visitors; the abstract attributes 65% of seed formation to autonomous selfing. Mating system is confounded with species and nocturnal reliance, so a causal selfing moderator is not isolated by the two-species comparison.

The separate Lu *Ecology and Evolution* network study, DOI 10.1002/ece3.74368, has no source-matched seed endpoint. Its 400 survey rows and night Lepidoptera counts 838→357 must not be merged with the JPE focal-species dataset. Source-pinned calculations remain in earlier IWE PR #118 and ALAN draft PR #65.

### Li: authentic seed-count source, with a positive direction

Li et al. bioRxiv preprint DOI [10.64898/2026.07.10.737511](https://doi.org/10.64898/2026.07.10.737511) is not established peer-reviewed here. The original author's public `seedset.csv` Git blob is `b616aca5beeba1457549841477d61ca4f796a147`; raw SHA256 is `7d0311a2507fafe8e3f469196ac2efb17abc30960084aed384557cbcf7e33162`. The 79 original rows comprise 78 known seed outcomes and one unknown point-light outcome.

| Light treatment | Seed-bearing / measured plants | Counted seeds | Counted fruits |
|---|---:|---:|---:|
| Dark C | 8/26 | 672 | 32 |
| Point P | 12/25 | 967 | 33 |
| Linear array L | 20/27 | 3,729 | 149 |

The source-row L−C seed-presence difference is +0.43305; the equal-hayfield mean is +0.43131. All three physical hayfields have positive differences (+0.3333, +0.5051, +0.4556), but three fields cannot be treated as 79 independent randomized light replicates. A three-of-three sign diagnostic has minimum two-sided fraction 0.25 and is not an assignment-based randomization test.

The original source seed-per-known-plant ratio 5.3436 equals both (seed-bearing fraction ratio 2.4074 × seeds-per-seed-bearing-plant ratio 2.2196) and (fruits-per-known-plant ratio 4.4838 × seeds-per-fruit ratio 1.19175). These are accounting identities, not mediation estimates. Species composition, flower budgets and field history remain relevant.

The original `pollinated` column is `Seeds > 0`, not a measured visit or stigma pollen count. Geometry and total lamp number/footprint differ together. There is no demonstrated moth movement-corridor mechanism or seed viability test. The frozen aggregate-only source receipt remains `data/frozen/alan_li2026_original_aggregate_v01.json`; original individual records are not redistributed.

### Other sources retain their own endpoints

- Knop et al. 2017, DOI 10.1038/nature23288: original authors reported −62% nocturnal visits and −13% focal fruit set. Fruit set is not Li's seed-presence outcome.
- Boom et al. 2020, DOI 10.1038/s41598-020-75471-1: Silene–Hadena light-spectrum experiment alters fruit-infestation/fertilization components. The rounded-components green/dark seed estimate is approximately 0.515, but the original model-derived net seed test has p=.63. This is not significant halving of counted mature seeds (ALAN draft #67).
- Giavi et al. 2021, DOI 10.1038/s41467-021-22011-8: Swiss daytime visits and floral-cover proxy, without matched seed/pollen outcomes in the source reanalysis (ALAN draft #69).
- Grognuz & Knop 2026 preprint, DOI 10.13140/RG.2.2.36822.10563: light×slug experiment, visits and later seeds; folivory and florivory are distinct pathways. Raw source unavailable, model coefficients not converted into percentages (ALAN draft #70).
- Grognuz et al. 2026, DOI 10.1016/j.biocon.2025.111650: flowering schedules at 14 lit and 14 dark locations, without same-unit effective visitor and final-seed observations. A flowering shift alone is not demonstrated mismatch.

## Macro evidence and source dependence

Kendall & Nicholson 2025, DOI 10.1111/ele.70036, is a published diel-exclusion literature synthesis, not manipulated ALAN. Its separate ALAN draft #53 reanalysis has 301 paired outcomes from 118 papers. The night-bloom contrast in 196 outcome pairs/73 papers is +21.475 percentage points nighttime reproductive share (study-cluster CI +10.751 to +32.199), but only four papers compare both bloom classes. The bloom×preceding-PCNL interaction is +1.738 pp/logPCNL (CI −4.913 to +8.388; p=.6085), unresolved. These values are ALAN reanalysis outputs, not direct original-paper light-intervention results.

The observation is compatible with different reproductive sensitivity under different functional conditions, but it does not establish a universal ALAN×mating-system interaction. A significant night-only effect and nonsignificant open effect cannot by themselves substitute for a tested light×access interaction with appropriate covariance.

## Current cross-repository boundary and execution

IWE's strict seasonal synchrony requires independently measured same-season flower/animal availability and appropriate plant-reproduction effect variance. The access-specific effects here do not meet that contract. `chocho` still describes potential larval-host geography, not locally measured lighting, pollen or seed response. No source here identifies a true island/mainland lighting-by-effective-substitution reproductive contrast.

Retained original-source reproduction:

```bash
python scripts/audit_alan_reproduction_source_grain.py --download-li-author-original --out-dir results/alan-reproduction
```

Corrected Lu scope validation:

```bash
python scripts/audit_lu2026_access_scope.py --output-dir results/lu2026-access-scope
```

Both pipelines retain source hashes, unknown effects, actual units and study dependence. The new 12-row Lu table is a full-text transcription, not recovered individual observations or twelve independent studies. The correction changes interpretation and scope, not original reported numeric values or any existing IWE strict-H1 effect set.
