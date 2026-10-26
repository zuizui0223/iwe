# Can 2021 flower×Osmia timing models predict 2022 sampled-fruit seed set?

**Date:** 2026-10-26. **Status:** paired original-source ecological transport stress test, not a pre-registered confirmatory experiment.

**Source original data:** de Manincor/Fisogni/Rafferty 2021 greenhouse source [Zenodo 10.5281/zenodo.7264150](https://zenodo.org/records/7264150) and the distinct 2022 greenhouse experiment published in 2026 [Zenodo 10.5281/zenodo.17830772](https://zenodo.org/records/17830772). All original archived ZIP and text files are fetched directly and compared to their already-frozen MD5 hashes.

## Ecological aim and strict dependence

The 2021 *Collinsia heterophylla–Nemophila menziesii–Phacelia campanularia × Osmia lignaria* study found a small positive **within-arena** prediction difference from bloom-day-matched bee density relative to a calendar-only model. The 2022 experiment found no robust benefit of that stand-alone timing variable for sampled fruits, F1 germination or F1 seedling survival under leave-arena-out testing; room-held-out results were outcome-dependent. These findings **do not constitute a two-year matched-protocol effect estimate**.

This new original-data test asks the more stringent question: **does an externally trained timing model survive transport to the other greenhouse cohort when both are restricted to the same measured sampled-fruit seed fraction?**

No independent taxonomic or interaction-class replication is added: same three plant species, same focal pollinator, overlapping researchers, different experimental rooms/treatments and sampling in each year.

## Equivalent measured outcome, but distinct original grains

The only harmonized biological response here is **mature sampled-fruit seeds / originally classified sampled-fruit seeds plus undeveloped ovules**. The 2021 raw plant/fruit records use those counts directly; the 2022 original fruit rows have internally consistent primitive seeds and total ovules, notwithstanding 31/208 wrong source-exported `seed_set` fractions. Recompute instead of admitting unreliable derived values.

To avoid training on 181 individual sampled plants and evaluating on 60 aggregated F1 groups, both cohorts are pooled **within source arena × plant species** before any cross-cohort predictive modelling:

- 2021: 181 fully reconciled individual sampled-fruit plant outcomes into up to 24 **arena×species** response units, with eight original arenas; 228-plant observed-outcome partial-fruit sensitivity separately.
- 2022: original 208 fruit observations nested within 60 **arena×species** groups across 20 original arenas, each response is the primitive seeds/total ovule ratio of the sampled original fruits; original F1 germination and seedling survival are expressly **not** shared outcomes.
- All independently observed dated bee abundance and plant flower records contribute the **original season-wide plant species flower opportunity index**, including plants without a subsequent usable seed outcome. Missing unobserved dates are not bee zeros. Only exact same-day bee × floral count joins enter matched exposure.
- Cohort-specific flower population composition **share** among co-planted three species within each arena replaces raw flower totals, which were obtained using different original sampling frames.
- Cohort-relative bloom calendar and relative bee abundance are normalized using **predictor-only season/census information**. However target cohort predictors would only be fully known after that target bloom season; this is a retrospective test and not prospective early-spring forecasting.

## Comparator model contract and evaluation

Same fixed ridge 0.05, train-only standardization, species fixed indicators and arena×species response, no access to the target cohort's seed outcomes. Core comparisons:

- Species+flower share alone (M0)
- + bloom calendar position within that year's season (M1)
- + time-averaged observed bees (M2)
- + exact-day flowering-weighted bee density (M3)
- + difference of same-day bee density from time-averaged bee density (M4)
- + combined calendar and matched bee densities (M5/M6)
- + independently observed season-mean bees **and** matched-day bees in the same model (M7/M8): a nested ablation testing added timing information beyond overall abundance
- + season-mean bees and calendar (M9): non-window richer comparator

Use **whole-year-out** training 2021 -> testing all 2022 groups and reciprocal 2022 -> 2021; also rerun identical model variables in both years under **leave-entire-arena-out** checks. Equal-arena RMSE means 24/60 groups are **not 24/60 independent complete experiments**, and two years are not independent replicated greenhouse populations.

## Numerical results from both immutable, original MD5-verified cohorts

Original-data GitHub Actions [run 40279026018](https://github.com/zuizui0223/iwe/actions/runs/40279026018) successfully fetched **both** original Zenodo datasets and verified 2021's 181 source-complete fruit-outcome individuals, 228 observed-fruit partial-missingness sensitivity, and 2022's 208 original flower/fruit rows aggregated to 60 biological groups. **All model outcomes below are the same sampled-fruit seed fraction**, not 2022 F1 germination/cotyledon survival.

### Strict other-year cohort transfer — train entirely in the other year

Equal weighting across true held-out **arena** mean-square errors; lower RMSE is better. The seed responses from the test cohort are never used to train the model, though all test-season bloom/bee predictors are known after the recorded flowering season.

| Model | 2021 train → 2022 test (20 arenas, 60 groups) | 2022 train → 2021 test (8 arenas, 24 groups) |
|---|---:|---:|
| M0 species + flower composition share | 0.18186 | 0.14912 |
| M1 + within-cohort blooming calendar position | 0.19462 | 0.15341 |
| M2 + season-mean adult bee density | 0.17041 | 0.14700 |
| M3 + exact-date bloom-weighted adult bee density | 0.17179 | 0.13118 |
| M5 + calendar and matched bee density | **0.16493** | 0.13269 |
| M7 + season-mean bee density **and** matched bee density | 0.16706 | **0.13019** |

The independent adult bee-window predictor carries cross-cohort **reproductive prediction information** beyond a flowering-calendar-only predictor, but its information is **not universally better than a season-average abundance measure**. In 2021→2022, stand-alone matched-day exposure M3 is slightly **worse** than adult mean M2 (0.17179 vs 0.17041); a two-predictor M7 improves M2 only by **0.00336**, and M5 is the best of the listed fixed exploratory candidates. In 2022→2021, M3 and M7 do better than M2, but that does not make the 2021 source an independently replicated species or outcome.

Cross-cohort M3 versus M1 has a smaller per-arena squared error in only **10/20** test arenas in 2022 and **5/8** in 2021. A lower mean RMSE is not a unanimous site effect.

### Contradictory within-cohort outcome-blind arena holdouts

With the *same group response and the same identical feature coding*, leave-entire-arena-out within each cohort gives:

| Model | 2021 internal (8 arenas) | 2022 internal (20 arenas) |
|---|---:|---:|
| M0 species + flower share | **0.13716** | 0.16644 |
| M1 bloom calendar | 0.14044 | 0.17053 |
| M2 season-mean adult abundance | 0.14553 | **0.15821** |
| M3 matched-day adult abundance | 0.13881 | 0.15866 |
| M7 mean bee + matched-day bee | **0.17103** | 0.16015 |

This reverses the apparent advantage of the larger M7 model from the two cohort-transfer tests: **M7 is worse than M2 in both internal validations**. The incremental matched-window effect is therefore sensitive to whether validation means transport between cohorts or averaging over missing arenas within one cohort, even though training outcomes never include held-out groups. The larger model can learn cohort-specific adult-density relations that fail under within-cohort arena resampling.

### Source-original partial-fruit sensitivity

Including the **47 original 2021 plants with extra unobserved fruit rows but internally agreeing observed seed totals** increases the 2021 source to 228 eligible plants (still only eight arenas and 24 arena×species response groups).

- 2021 train → 2022 test: M2 **0.21307**, M3 **0.17426**, M5 **0.15599**, M7 **0.20253**. Here the **best** listed model differs again: calendar + bloom-window is substantially better than an adult-mean-only model, while M7 improves only modestly over M2 and is not even as good as the calendar-only M1 (**0.20002**).
- 2022 train → 2021 test: M2 **0.14376**, M3 **0.12769**, M7 **0.12610**; the small positive window direction persists in the broader observed-outcome subset.
- Such partially unmeasured original fruits may be missing non-randomly; these are **observed sampled-fruit outcome fractions**, not fully observed seed numbers per individual mother.

### Ecological inference boundary

The directly falsifiable ecological result is **heterogeneous temporal information**: date-matched adult-visit opportunity may transport some information across experimentally different greenhouse years, but the incremental reproductive contribution *after conditioning on season-wide adult abundance* is unstable across validation grain and original fruit inclusion rules.

This is more defensible than saying either that date matching universally improves reproduction or that the 2022 experiment contradicts all 2021 findings. Cohort-specific reproductive-stage endpoint, sampling differences, greenhouse temperature assignment, source outcome missingness and the three shared host taxa remain confounded in this retrospective comparison.

**No cross-cohort causal effect size, no generalizable across-taxon improvement, no standalone stage-specific larval conversion result and no new strict-H1 cluster.** The two external years are not two independent populations with randomized temperature replication, and model features were selected after examining the original articles and earlier source runs.



## Reproduction

Run `python -m scripts.analyze_osmia_crosscohort_transfer_2021_2022 --outdir /tmp/iwe-osmia-transport`. All source original rows remain at the DOI-hosted sites; GitHub CI publishes only derived source-group support, paired blocked RMSE comparisons and audit flags.

**Frozen IWE strict H1 unchanged:** two independent mutualist SMD clusters, zero antagonist or mixed strict SMD clusters.
