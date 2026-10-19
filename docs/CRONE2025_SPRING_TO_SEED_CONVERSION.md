# Spring flowering as a pre-outcome indicator of final samara conversion

**Date:** 2026-10-19  
**Status:** exploratory original-data analysis, NOT IWE strict H1 or a confirmatory stage-phase test.  
**Source:** Crone & Rapp (2025), *Mast years increase wind pollination and reduce seed predation in sugar maple*, AJB, DOI [10.1002/ajb2.70046](https://doi.org/10.1002/ajb2.70046). Frozen original CSVs and R code: [Zenodo 10.5281/zenodo.15090572](https://doi.org/10.5281/zenodo.15090572). The parent source-probe GitHub Actions run [39209740280](https://github.com/zuizui0223/iwe/actions/runs/39209740280) verified the actual six original files, source byte checksums and 272 flowering, 159 exclusion records (154 actually evaluated), 280 whole-tree seed-count and 172 samara-evaluation rows.

## Why this matters to IWE

The published annual `mast.index` uses **late-season seed counts** as an annual descriptor. It is legitimate for retrospective ecology, but it is not a partner-availability observation made before eventual seed fate. IWE's temporal propagation argument needs to distinguish a source predictor actually known *before the outcome* from a late response-associated predictor.

Here, the original **spring** qualitative flowering census covers 20 trees for each 2012–2017 year. It yields a genuinely earlier timing/intensity reference:

`spring_intensity(y) = mean_tree (none=0, low=1, medium=2, high=3)`.

The six year-wide means are: 2012 **0.50**, 2013 **2.25**, 2014 **1.30**, 2015 **1.55**, 2016 **1.90**, 2017 **3.00**. This captures annual **flowering effort**, not adult-pollinator synchrony or the exact date of flowering. Whole-year predictor variation has **six year-level clusters**; 159 seed-state rows are nested observations, not 159 independent ecological exposures.

## Original natural-control seed-state results

These values are independently computed directly from the original 159-row exclusion dataset, grouped by year and **control** treatment. The code and GitHub Actions artifact recalculate from MD5-checked original bytes; original individual-branch records are never added to the repository.

| Year | Early spring mean | Control rows | Classified pods | Intact filled / classified | Recorded predation / nonempty |
|---|---:|---:|---:|---:|---:|
| 2012 | 0.50 | 9 | 100 | 13.00% | 72.00% |
| 2013 | 2.25 | 14 | 340 | 45.00% | 10.00% |
| 2014 | 1.30 | 11 | 108 | 20.37% | 38.30% |
| 2015 | 1.55 | 13 | 176 | 32.39% | 32.94% |
| 2016 | 1.90 | **16 evaluated (18 recorded)** | 104 | 15.38% | 51.35% |
| 2017 | 3.00 | 19 | 274 | 48.91% | 3.42% |

**Exploratory descriptive patterns, 6 years:** year-level spring mean vs fraction of classified control samaras intact, Spearman **rho = +0.829** (**exact six-year two-sided permutation p = 0.0583**, 42 of 720 year-label permutations). This does **not** pass a conventional 0.05 threshold, even before accounting for exploratory endpoint choices. Spring mean vs recorded predation fraction among nonempty samaras, **rho = −0.829**, but this second contrast is especially sensitive to variable category recording. The illustrative, post-hoc split at spring mean >=2 produces two high-spring years (2013, 2017) with mean intact classified fraction **46.95%**, versus **20.29%** in the other four years. These are **means of year means**, not pooled plant/seed replications or inferential effects.

**Year-held-out exploratory prediction:** simple unweighted regression using the *spring score available before harvest* yields leave-one-year-out RMSE **0.100** for intact classified samara proportion versus **0.168** for an intercept-only comparator (~40% reduction). Each point is an annual proportion from unevenly sized control-branch samples; there is no independent forest/site, no randomized annual mast treatment and no uncertainty interval suitable for generalization. This is **not** a stage-specific versus adult-only predictive comparison. The end-of-season mast index is never promoted to a prospective predictor.

## Where does the annual timing signal survive? Seed-state decomposition

Distinguish two source-observed stages on the same harvested control samaras: (1) **nonempty vs empty**, a proxy for possible pollination/seed initiation, and (2) among **nonempty**, whether seed tissue survived to a final **intact filled** seed. The latter includes combined consequences of predation and early abortion; the experiment does not date these stages.

| Endpoint | Spearman with spring flowering | Leave-one-year-out intercept RMSE | Leave-one-year-out spring model RMSE | Relative change |
|---|---:|---:|---:|---:|
| Nonempty / all classified | +0.377 | 0.0695 | 0.0920 | **32.2% worse** |
| Intact filled / nonempty classified | +0.829 | 0.2926 | 0.1511 | **48.4% better** |
| Intact filled / all classified | +0.829 | 0.1682 | 0.1002 | **40.4% better** |

At this **one site, over six non-independent-on-longer-time-scales years**, the earlier-recorded flowering index improves year-held-out *conditional intact-seed conversion* more than the initial nonempty proportion. This stage-conversion perspective is the IWE extension; seed-predation economies of scale are already an established finding of the source study. The fractions are algebraically coupled (intact/all = nonempty/all × intact/nonempty), so the two intact endpoint results are not independent confirmations.

**Inference boundary:** An exact unadjusted two-sided year-label permutation diagnostic gives p = 0.0583 for Spearman +0.829 (n=6). It is not a confirmatory test and does not pass a conventional 0.05 threshold. There were multiple chosen endpoints/scales, and the original spring index may reflect weather, tree reproductive allocation, pollination, density of seed predators and other year-confounded factors. A null/weak nonempty relationship is not evidence that pollination has no effect.

### Spring-score sensitivity

The ordinal mean (none=0, low=1, medium=2, high=3) is **not observed flower numbers**. The source publication also describes a numerical proxy (0/500/5,000/25,000 flowering buds per category) without counting every flower, and a third coding is the fraction of high-flowering trees.

| Early-measured index | Intact/all LOYO RMSE | Intact/nonempty LOYO RMSE | Nonempty/all LOYO RMSE |
|---|---:|---:|---:|
| Ordinal category mean | 0.1002 | 0.1511 | 0.0920 |
| Authors' bud-category representative values | 0.1020 | 0.2093 | 0.0868 |
| High-flowering tree fraction | 0.1136 | 0.2456 | 0.0847 |
| Intercept-only comparator | 0.1682 | 0.2926 | 0.0695 |

The qualitative separation survives these alternative encodings, while its predictive gain is sensitive to the scaling. No scale is a measured adult–flowering phase or a tested larval timing coordinate.

## A critical calendar-only falsifier: alternate bearing

The original study identifies synchronous *alternate bearing* in sugar maple, creating a hard alternative explanation for any six-year spring-intensity association. Compare the earlier-recorded spring score with a simple **odd/even calendar year** indicator, whose value requires no spring field observation. Both are fitted using the same leave-one-year-out unweighted annual regressions; parity is **not** presented as a biological mechanism or a randomized treatment.

| Endpoint | Spring-only LOYO RMSE | Odd/even year-only LOYO RMSE | Which predicts better? |
|---|---:|---:|---|
| Nonempty / classified | 0.0920 | **0.0663** | Year parity |
| Intact / nonempty | **0.1511** | 0.1535 | Nearly tied |
| Intact / classified | 0.1002 | **0.0815** | Year parity |

**Scientific implication:** Even at the same site, the apparent spring-to-final seed association does **not** establish additional information beyond the known biennial calendar cycle. Conditional intact conversion is almost equally well predicted by year parity. An independent additional forest or longer independent series, with prior outcome-blind window definition, is needed before attributing a distinctive predictive contribution to measured spring flowering intensity. A two-term parity-plus-spring fit with six year points would be too unstable to promote as confirmation.

This negative control directly limits the IWE claim: a biologically plausible early indicator must improve over **plausible simpler time coordinates**, not merely over a constant baseline.

## Unit sensitivity: a typical seed is not a typical sampled tree

The primary analysis asks about the **fraction of all classified samaras**, pooling naturally unequal numbers of harvested samaras from the sampled branches. A different target — the **mean of tree-year seed-state fractions** — gives each sampled tree equal influence. Both are descriptively useful, but they are biologically distinct estimands and should not be intermixed.

| Year-held-out contrast | Nonempty / all classified | Intact / nonempty | Intact / all |
|---|---:|---:|---:|
| **Pooled samaras**: relative RMSE improvement | **−32.2%** (worse) | +48.4% | +40.4% |
| **Equal tree weights**, with ≥1 classified samara/tree: improvement | **+10.4%** | +46.0% | +57.2% |
| **Equal tree weights**, with ≥10 classified samaras/tree: improvement | **−26.1%** (worse) | +36.8% | +29.5% |

The weak early/nonempty trend is **not invariant to the tree/seed denominator**: under equal-tree weights with only ≥1 samara, even nonempty fraction gains a little predictive skill. In 2016, an observed tree-year (HF12) has only **2 classified samaras**, both intact/filled. That tiny 100% case equals a tree with 42 samaras in the naïve equal-tree mean, inflating the 2016 typical-tree intact fraction from 13.2% (requiring ≥10 samaras/tree) to 34.9% (accepting ≥1). Two other sampled control trees in 2016 have **zero classified samaras** and cannot be used as zero-valued *fractions*. Missing tree outcomes are never filled with an assumed zero rate.

Under the explicit ≥10-classified-samara sensitivity, the qualitative *relative* pattern (spring predicts conditional intact-seed conversion more usefully than initial nonempty fraction) remains, but the absolute gain is smaller and the restricted sampled-tree population is not a random forest sample. These thresholds were checked after seeing the data; none is a confirmatory significance criterion.

**Consequences:** The current biological finding is not an identified stage-specific causal effect, nor an assertion that spring flowering leaves the pollination stage unchanged. It is a bounded **annual scale- and unit-sensitive temporal-information pattern** with a more persistent association to terminal seed states. This must be presented alongside the source's existing masting/seed-predator interpretation.

## Essential outcome and missingness limits

1. **State and denominator**: `num.filled / total.seed` counts the proportion of **classified, harvested samaras** with intact filled seeds. It is not viable seed production per *tree*, and `total.seed` does not necessarily contain samaras missing during harvest. It should not be called maternal lifetime fitness.
2. **Unobserved missing samaras**: In 2015, control branches report **100 missing samaras** against 176 classified, so the worst/best raw filled fraction assuming all reported missing are non-intact/intact ranges from **57/276 = 20.65%** to **157/276 = 56.88%**. In 2014 control there are 18 missing against 108 classified. High-versus-low separation is *not* robust to arbitrary unobserved fate.
3. **Two kinds of original-source NA**: All 2013 records have unmeasured `num.missing` but **observed** filled/empty/grub categories. By contrast, **five 2016 original branch rows** (two control, three bagged) have **all seed state fields NA**, unmeasured missing pods and `total.seed=0` as an export placeholder. They are **unobserved branch outcomes**, not measured zero-seed branches. Exclude them from seed fraction denominator: 159 archived records give **154 evaluated rows**, matching the original article's 154-branch pollination sample. Total reproductive output remains unidentified on those missing branches.
4. **Predation-category incompleteness**: All 2013 source rows lack the optional `num.moldy`, `num.exit`, `num.wrinkle` and `num.small` fields; the five completely missing 2016 branches are excluded. Recorded grubs remain real, but annual predators' stage-specific loss rates are **not guaranteed to be measured consistently** across all years.
5. **Tree/branch nesting**: Year+tree+branch labels are reused within the original archive. Do not treat labels as distinct tagged branches, remove repeated labels as duplicates, or treat 159 branch rows as independent timing experiments.
6. **Ecological confounding**: Flowering intensity, mate-sex composition, resource availability, temperature and regional predation pressures may covary by year. Neither a high rho nor a year-level leave-one-out RMSE reduction demonstrates that flowering synchrony *causes* more intact seeds.
7. **Scale mismatch**: These are seasonal tree-intensity and harvest metrics; no exact contemporary adult activity, oviposition date, delayed larval feeding onset, or susceptibility window is measured. The result cannot populate the IWE strict synchrony `mutualist/antagonist/mixed` meta-analysis.

## Interpretation and next discriminating dataset

This is evidence that an **early-observed ecological state** can carry descriptive information about multiple later reproductive stages, and that the originally reported mast-year advantages remain a plausible annual-scale phenomenon. It is *not* evidence that a downstream stage metric generally predicts final fitness better. In fact, the 2016 low intact fraction despite relatively high spring flowering warns against a deterministic annual conversion law.

To test the IWE central hypothesis decisively, the next original-data programme must match **dated spring flowering, independent adult activity, larval or realized cost timing, and final intact mature seeds on compatible units**, then compare a simple calendar/adult predictor against a pre-outcome stage-filtered predictor using a blocked, outcome-unseen holdout. This maple programme cannot substitute for that design.

**Reproduction:** `python -m scripts.analyze_crone2025_spring_conversion --outdir /tmp/iwe-maple-spring`; deterministic software tests `tests/test_crone2025_spring_conversion.py`; original bytes fetched directly from pinned Zenodo record paths and checked against six source MD5s. The derived audit includes six-year exact permutation checks, alternative spring-score encodings and 2016 all-NA branch exclusions.
