# Replication discovery batch 003 — design-signature search

Date: 2026-09-24  
Status: full-text/design adjudication complete for first design-signature batch  
Outcome: **no second strict SMD cluster yet**

## Search logic

After broad taxonomic browsing failed, this batch searched for the study design itself:

`same-season partner activity + plant early/peak/late timing + final plant reproduction`.

This found substantially closer studies than taxon-name searching, but each exposes a different missing link.

## Mixed systems

### Bopp & Gottsberger 2004 — closest timing-positive lead

*Silene latifolia ssp. alba / S. dioica × Hadena bicruris*  
DOI: `10.1111/j.0030-1299.2004.12625.x`

This paper genuinely passes the difficult timing gate. The field design records newly opened female flowers and newly laid *H. bicruris* eggs repeatedly through the same season, allowing flowering and moth oviposition/activity to be compared directly.

The blocker is downstream: the paper asks about host choice and larval performance. The quantitative endpoint emphasized after oviposition is moth pupal performance/nutritional suitability, not final plant reproduction after seed consumption.

Decision: `blocked_final_surface`, P1 citation-mining anchor.

The next move is **not** to convert moth performance to plant fitness. It is to search the linked Ulm *Silene–Hadena* programme for a companion paper/thesis containing final plant seed production on the same phenology observations.

### Scopece et al. 2018 — fitness-positive but timing-negative near-miss

*Silene latifolia × Hadena bicruris*  
DOI: `10.1093/aobpla/ply002`

The natural population component sampled 21 plants in April, 19 in May and 21 in June. The study records *Hadena* infestation and shows no predation in April versus 4.06% of fruits in May and 5.92% in June.

Two strict-contract problems prevent promotion:

1. *Hadena* seasonal presence in the focal comparison is operationalized through infestation/predated fruits, not an independently measured adult activity curve. Predation cannot be used as both exposure and cost.
2. Monthly seed-per-fruit comparisons deliberately use five fruits per plant with **no direct Hadena infection**, so that outcome is pollination efficiency rather than net post-predation reproduction.

The separate experiment does count mature fruits and total seeds, but it manipulates day-only versus night-only pollinator access. That is a diel visitor-access treatment, not flowering phenology.

Decision: `rejected_timing` for the strict replication target.

## Antagonist systems

### Sercu et al. 2020 — Geum urbanum × Byturus ochraceus

DOI: `10.1111/1365-2745.13325`

This is exceptionally strong final-fitness evidence: individual flowers are followed through the season, seed herbivory is scored, and total seed mass is calculated per flower and per plant. Predation is concentrated in the first flowering peak and substantially changes the reproductive value of early flowering.

The strict timing gate nevertheless fails. The adult beetle emergence/oviposition period is described from prior natural-history studies. The focal study observes damage/larvae, not an independent same-season adult activity curve. Under the frozen IWE rule, the observed predation peak cannot be relabelled as the missing partner-activity exposure.

Decision: `rejected_timing` for strict H1; high-value direct-timing sensitivity/context evidence.

### Bertness, Wise & Ellison 1987 — salt-marsh community

DOI: `10.1007/BF00377284`

This paper does measure insect abundance through the season and final seed losses. Consumer pressure rises through early summer, peaks in mid-July and declines in August; early, middle and late flowering marsh species experience correspondingly different losses.

The blocker is the biological unit: the timing contrast is primarily **among different plant species** and involves a consumer guild dominated by a generalist grasshopper plus species-specific consumers. This is not a clean within plant taxon × focal partner synchrony effect.

Decision: `rejected_other`; retain as community-scale ecological context.

### English-Loeb & Karban 1992 — Erigeron glaucus × Tephritis ovatipennis

DOI: `10.1007/BF00317168`

The study relates flowering synchrony, seed-head herbivory and total annual viable seed production. Low-synchrony clones partly escape *Tephritis* by extending flowering into fall.

But the published synchrony variable is synchrony with the **plant population flowering peak**, not overlap with an independently measured *Tephritis* activity curve.

Decision: `rejected_timing`.

### Atlan et al. 2010 — Ulex europaeus × Exapion ulicis

DOI: `10.1111/j.1420-9101.2009.01908.x`

Common-garden flowering types differ strongly in pod phenology, infestation and reproductive allocation. Long-flowering plants produce many pods before the seed-predation peak.

The focal weevil activity interpretation, however, relies on prior life-history work; contemporaneous infestation is the damage process itself rather than an independent activity curve.

Decision: `rejected_timing`.

## What the near-misses reveal

The missing information is now decomposed into three recurring study types:

1. **timing complete, fitness missing** — Bopp & Gottsberger 2004;
2. **fitness complete, partner timing missing** — Sercu 2020, Ulex 2010, Erigeron 1992;
3. **timing + fitness measured, biological unit incompatible** — Bertness et al. 1987.

This is much narrower than “the literature is sparse”.

## Next retrieval target

The highest-value route is now citation/programme completion rather than another broad search:

1. mine publications, theses and archived data linked to **Bopp/Gottsberger’s Ulm Silene–Hadena programme** for plant seed/fruit fitness measured on the same direct moth-activity phenology;
2. mine companion datasets/citations of final-fitness antagonist studies for **independent adult activity observations in the focal year**, especially Geum/Byturus;
3. only if those fail, continue design-signature search.

A second cluster is promoted only when all four gates coexist in one dependence-compatible programme. Evidence from two different studies is never spliced into a synthetic strict effect.


## Opportunistic replication closure — mutualist #2

Although mixed and antagonist remain the frozen search priorities, the same design-signature audit exposed a fully reconstructable independent mutualist programme in IWE023 (*Mertensia ciliata*).

The 2015 experiment has four balanced flowering cohorts (n=10 each), contemporaneous pollinator visitation that declines by more than fivefold from week 1 to week 4, final per-plant mature seed set, all four relative group means, and the same outcome's one-way ANOVA F(3,36)=1.01.

Because the design is balanced, the ANOVA identity recovers the pooled within-group residual variance on the same common scale as the reported means. The strict week-1 versus week-4 contrast gives:

- Hedges g = **+0.3732395638**;
- sampling variance = **0.1873253239**;
- dependence cluster = `DEP_MERTENSIA_GALLAGHER_CAMPBELL_RMBL`.

This raises mutualist SMD replication from one to **two independent clusters** without changing the estimand, converting a slope, or imputing variance. Mixed and antagonist still require one additional independent cluster each.
