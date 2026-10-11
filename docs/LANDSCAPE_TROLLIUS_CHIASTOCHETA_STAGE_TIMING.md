# Trollius–Chiastocheta — flower-age timing changes the benefit-cost ratio

Date: 2026-10-02  
Core sources: Pellmyr 1989; Després & Jaeger 1999  
DOIs: `10.1007/BF00377197`, `10.1046/j.1420-9101.1999.00088.x`  
Landscape role: independent mixed-system mechanism showing that adult interaction timing changes the marginal pollination benefit relative to delayed larval seed cost.

## System

*Chiastocheta* adults pollinate *Trollius europaeus* while visiting flowers and ovipositing. Their larvae later consume developing seeds.

Thus each fly lineage creates:

- an immediate adult pollination benefit;
- a delayed larval seed-consumption cost.

The system is independent of the *Silene–Hadena* and *Yucca–Tegeticula* programmes in IWE.

## Flower age partitions the adult interaction window

The fly species are temporally partitioned across the life of a flower.

Després & Jaeger 1999 report approximate oviposition timing:

- *C. rotundiventris*: mainly day 1, with a few eggs on day 2;
- *C. setifera*: begins around day 2;
- *C. macropyga*: days 3–6;
- *C. trollii*: begins around day 5;
- *C. inermella*: from day 5, with most eggs on day 7;
- *C. dentifera*: begins around day 6 and oviposits mainly after flowering.

The guild therefore supplies a natural flower-age gradient of adult service/oviposition timing.

## Why the benefit-cost ratio changes with timing

Pellmyr 1989 showed that each fly visit fertilizes a fixed proportion of the ovules that remain unfertilized at that time.

Consequently, the **marginal pollination benefit declines with flower age**: later visitors encounter fewer unfertilized ovules and initiate fewer additional seeds.

The offspring cost does not decline in parallel. The cost-benefit analysis treats larval seed consumption as sufficiently stable that later ovipositing lineages can consume more seeds than their mothers newly fertilize.

The source estimates:

- benefit-cost equality at roughly **4–5 eggs per flower**;
- observed population means of **2.3–7.25 eggs per flower** across three years.

Natural populations therefore operate around and across the region where small changes in adult pollination efficacy or oviposition intensity can alter the plant's net balance.

## Stage-specific interpretation

The key quantity is not generic synchrony with `Chiastocheta`.

It is the timing of the **adult service event within flower development**, combined with a later offspring cost.

For an early visitor:

- many ovules remain available for pollination;
- the adult visit can create substantial new seed benefit;
- larvae later consume part of that seed crop.

For a late visitor:

- much of the potential pollination benefit has already been realized;
- the adult can still oviposit;
- the delayed larval cost remains.

Thus the same adult-pollinator / larval-seed-predator architecture changes from more beneficial to less beneficial as the interaction moves across flower age.

## Relation to the stage-specific IWE model

This is an independent mixed-system replication of the central stage distinction:

> adult service and delayed offspring cost must be aligned to plant developmental state separately.

It complements Kula 2012 in two ways.

- Kula varies the **lag from oviposition to damaging larvae** across years.
- Trollius–Chiastocheta varies the **plant developmental stage at adult service/oviposition** across fly species.

Both show that a single synchrony score can erase the stage relation that determines the benefit-cost balance.

## Attempted population-level phase-composition test — closed

Suchan et al. 2015 (DOI `10.1002/ece3.1544`) initially looked like a route to connect species-specific oviposition timing to final plant seed output across eight *T. europaeus* populations.

That route does **not** survive source audit.

The 2009–2011 population table records only **Chiastocheta presence/absence**, not the identity or relative abundance of early- versus late-ovipositing *Chiastocheta* species. Pollinator observations identify *Chiastocheta* as a group rather than resolving the timing guild by species.

More importantly, the study's reported "net seed set" is not a direct count of post-larval mature seeds. It is calculated as pre-predation seed set multiplied by a previously published egg-density cost function:

`net seed set = seed set × (1 - 0.66 × x^0.26)`,

where `x` is egg density per carpel.

Therefore the 8-population dataset cannot be used to test:

`early-vs-late Chiastocheta composition -> observed final plant seed output`.

Doing so would require both a source-backed species/timing composition for each population-year and directly observed post-predation seed fate. Neither is present in the 2015 dataset.

This route is closed rather than left as an open completion target.

## Claim boundary

This component is mechanism evidence, not a strict mixed final-fitness effect.

- Adult timing is inferred from observed oviposition timing within flower age, so the provenance is `realized_interaction_window`.
- The classic cost-benefit calculation is a seed-balance mechanism rather than a variance-bearing high-versus-low timing contrast in final whole-plant reproduction.
- The several *Chiastocheta* species should not be treated as independent plant-level experimental replications.

The source-backed synthesis is stored in
`data/source_reconstructions/trollius_chiastocheta_timing_cost_benefit.csv`.
