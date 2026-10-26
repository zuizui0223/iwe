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

Use **whole-year-out** training 2021 -> testing all 2022 groups and reciprocal 2022 -> 2021; also rerun identical model variables in both years under **leave-entire-arena-out** checks. Equal-arena RMSE means 24/60 groups are **not 24/60 independent complete experiments**, and two years are not independent replicated greenhouse populations.

## Numerical outcome and claim ceiling

**Pending original source CI at initial PR.** The script fails if original source MD5, 181/228 source plant counts, 24/60 arena-species group support, original seed/ovule closure, source identities or calendar/bees availability change. Only after both actual full repository tests and source-original workflow succeed will it record direction and stage effect.

What could be learned: whether temporal matching adds stable out-of-cohort *prediction* after harmonizing the same seed fraction. What cannot be learned: independently replicated evolutionary adaptation, a statistically identified warming effect, a general across-taxon interaction benefit, causal effects of pollinator density, or the exact tagged-fate identity of an individual seed.

If source protocols differ enough that cohort mean responses are not transportable, register **domain shift and measurement non-equivalence** rather than forcing effects into a common meta SMD.

## Reproduction

Run `python -m scripts.analyze_osmia_crosscohort_transfer_2021_2022 --outdir /tmp/iwe-osmia-transport`. All source original rows remain at the DOI-hosted sites; GitHub CI publishes only derived source-group support, paired blocked RMSE comparisons and audit flags.

**Frozen IWE strict H1 unchanged:** two independent mutualist SMD clusters, zero antagonist or mixed strict SMD clusters.
