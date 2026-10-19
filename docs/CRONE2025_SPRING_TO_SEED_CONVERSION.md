# Spring flowering as a pre-outcome indicator of final samara conversion

**Date:** 2026-10-19  
**Status:** exploratory original-data analysis, NOT IWE strict H1 or a confirmatory stage-phase test.  
**Source:** Crone & Rapp (2025), *Mast years increase wind pollination and reduce seed predation in sugar maple*, AJB, DOI [10.1002/ajb2.70046](https://doi.org/10.1002/ajb2.70046). Frozen original CSVs and R code: [Zenodo 10.5281/zenodo.15090572](https://doi.org/10.5281/zenodo.15090572). The parent source-probe GitHub Actions run [39209740280](https://github.com/zuizui0223/iwe/actions/runs/39209740280) verified the actual six original files, source byte checksums and 272 flowering, 159 exclusion, 280 whole-tree seed-count and 172 samara-evaluation rows.

## Why this matters to IWE

The published annual \`mast.index\` uses **late-season seed counts** as an annual descriptor. It is legitimate for retrospective ecology, but it is not a partner-availability observation made before eventual seed fate. IWE's temporal propagation argument needs to distinguish a source predictor actually known *before the outcome* from a late response-associated predictor.

Here, the original **spring** qualitative flowering census covers 20 trees for each 2012–2017 year. It yields a genuinely earlier timing/intensity reference:

\`spring_intensity(y) = mean_tree (none=0, low=1, medium=2, high=3)\`.

The six year-wide means are: 2012 **0.50**, 2013 **2.25**, 2014 **1.30**, 2015 **1.55**, 2016 **1.90**, 2017 **3.00**. This captures annual **flowering effort**, not adult-pollinator synchrony or the exact date of flowering. Whole-year predictor variation has **six year-level clusters**; 159 seed-state rows are nested observations, not 159 independent ecological exposures.

## Original natural-control seed-state results

These values are independently computed directly from the original 159-row exclusion dataset, grouped by year and **control** treatment. The code and GitHub Actions artifact recalculate from MD5-checked original bytes; original individual-branch records are never added to the repository.

| Year | Early spring mean | Control rows | Classified pods | Intact filled / classified | Recorded predation / nonempty |
|---|---:|---:|---:|---:|---:|
| 2012 | 0.50 | 9 | 100 | 13.00% | 72.00% |
| 2013 | 2.25 | 14 | 340 | 45.00% | 10.00% |
| 2014 | 1.30 | 11 | 108 | 20.37% | 38.30% |
| 2015 | 1.55 | 13 | 176 | 32.39% | 32.94% |
| 2016 | 1.90 | 18 | 104 | 15.38% | 51.35% |
| 2017 | 3.00 | 19 | 274 | 48.91% | 3.42% |

**Exploratory descriptive patterns, 6 years:** year-level spring mean vs fraction of classified control samaras intact, Spearman **rho = +0.829**. Spring mean vs recorded predation fraction among nonempty samaras, **rho = −0.829**, but this second contrast is especially sensitive to variable category recording. The illustrative, post-hoc split at spring mean >=2 produces two high-spring years (2013, 2017) with mean intact classified fraction **46.95%**, versus **20.29%** in the other four years. These are **means of year means**, not pooled plant/seed replications or inferential effects.

**Year-held-out exploratory prediction:** simple unweighted regression using the *spring score available before harvest* yields leave-one-year-out RMSE **0.100** for intact classified samara proportion versus **0.168** for an intercept-only comparator (~40% reduction). Each point is an annual proportion from unevenly sized control-branch samples; there is no independent forest/site, no randomized annual mast treatment and no uncertainty interval suitable for generalization. This is **not** a stage-specific versus adult-only predictive comparison. The end-of-season mast index is never promoted to a prospective predictor.

## Essential outcome and missingness limits

1. **State and denominator**: \`num.filled / total.seed\` counts the proportion of **classified, harvested samaras** with intact filled seeds. It is not viable seed production per *tree*, and \`total.seed\` does not necessarily contain samaras missing during harvest. It should not be called maternal lifetime fitness.
2. **Unobserved missing samaras**: In 2015, control branches report **100 missing samaras** against 176 classified, so the worst/best raw filled fraction assuming all reported missing are non-intact/intact ranges from **57/276 = 20.65%** to **157/276 = 56.88%**. In 2014 control there are 18 missing against 108 classified. High-versus-low separation is *not* robust to arbitrary unobserved fate.
3. **Missingness itself unrecorded**: Every 2013 exclusion-source row has \`num.missing=NA\`, and **5 rows in 2016** likewise have it unknown. \`NA\` is **not zero**. Do not calculate optimistic/pessimistic missing-pod bounds for an annual group containing unknown missing counts.
4. **Predation categories changed**: In all 2013 source rows, the optional \`num.moldy\`, \`num.exit\` and other subcategories are \`NA\`; several 2016 rows also have these unobserved. Recorded grub counts are real, but predator-pathway proportions across years are **not a measurement-invariant series**. The table is descriptive only.
5. **Tree/branch nesting**: Year+tree+branch labels are reused within the original archive. Do not treat labels as distinct tagged branches, remove repeated labels as duplicates, or treat 159 branch rows as independent timing experiments.
6. **Ecological confounding**: Flowering intensity, mate-sex composition, resource availability, temperature and regional predation pressures may covary by year. Neither a high rho nor a year-level leave-one-out RMSE reduction demonstrates that flowering synchrony *causes* more intact seeds.
7. **Scale mismatch**: These are seasonal tree-intensity and harvest metrics; no exact contemporary adult activity, oviposition date, delayed larval feeding onset, or susceptibility window is measured. The result cannot populate the IWE strict synchrony \`mutualist/antagonist/mixed\` meta-analysis.

## Interpretation and next discriminating dataset

This is evidence that an **early-observed ecological state** can carry descriptive information about multiple later reproductive stages, and that the originally reported mast-year advantages remain a plausible annual-scale phenomenon. It is *not* evidence that a downstream stage metric generally predicts final fitness better. In fact, the 2016 low intact fraction despite relatively high spring flowering warns against a deterministic annual conversion law.

To test the IWE central hypothesis decisively, the next original-data programme must match **dated spring flowering, independent adult activity, larval or realized cost timing, and final intact mature seeds on compatible units**, then compare a simple calendar/adult predictor against a pre-outcome stage-filtered predictor using a blocked, outcome-unseen holdout. This maple programme cannot substitute for that design.

**Reproduction:** \`python -m scripts.analyze_crone2025_spring_conversion --outdir /tmp/iwe-maple-spring\`; deterministic software tests \`tests/test_crone2025_spring_conversion.py\`; original bytes fetched directly from pinned Zenodo record paths and checked against six source MD5s.
