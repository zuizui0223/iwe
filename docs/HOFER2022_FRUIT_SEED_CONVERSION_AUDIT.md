# Sinapis: where does visitor information enter reproductive conversion?

**Date:** 2026-10-19. **Status:** source-reproducible exploratory process diagnostic; no animal flight phenology, no strict IWE H1 effect.

**Source:** Höfer et al. (2022), original public Zenodo [10.5281/zenodo.7335086](https://zenodo.org/records/7335086). All source files are retrieved from the original DOI and verified against frozen MD5 hashes. Parent whole-plant seed audit: [HOFER2022_RESOURCE_SERVICE_LIMITING_STAGE_AUDIT.md](HOFER2022_RESOURCE_SERVICE_LIMITING_STAGE_AUDIT.md).

## New biological discriminator

The earlier source model found that floral visitation without flower number predicted seeds poorly, while visits conditional on flower count modestly improved the held-out prediction of total estimated seeds. **Does visitor information enter at the fruit formation stage or at the within-fruit seed stage?**

Compare five original-source quantities on the same plant sample:

1. Total pods on the plant: count of fruit production.
2. Pods per season-total flower count: fruit/flower conversion proxy, NOT exact individually followed flowers.
3. Author-reported average seeds per pod: within-fruit seed production proxy, not viable-seed germination.
4. Estimated total seeds per recorded flower: later reproductive conversion.
5. Source-estimated total seeds: reference source outcome from the previous audit.

**These stage responses share algebraic source inputs and are NOT five independent ecological effects.** Author estimated seed totals may be derived partly from pod numbers and average per-pod seeds, so source identity must be described, not mistaken for replication or causal mediation.

## Same biological units and five independent shelter holdouts

- 53 original focal plants in 15 plots nested in 5 experimental shelters, three source water treatments.
- Join all originally observed visitors by plant, maternal ID, plot, shelter, and treatment. Taxon/group rows cannot become independent plants.
- Link original pod count and average seeds per pod by exact same plant ID; missing source cells and zero-pod plants do not contribute fabricated seed-per-pod values.
- Fit all five separate response models to an IDENTICAL complete-case plant subset, leaving one entire shelter out at a time.
- Baseline water treatment + log total flowers; add visitor/flower/day and visitor/day separately. Also compare measured continuous stem water potential (SWP) and visitor/day after SWP, and source flowering duration.
- Use source plant-level target, training-only standardized fixed ridge 0.05, equal five-shelter RMSE and paired shelter wins. Only within-stage relative predictive changes can be compared; different response units prohibit pooling RMSE across stages.

## Original-data admission and numerical results

**Source run pending at first draft.** Execution:

    python -m scripts.analyze_hofer2022_conversion_components --outdir /tmp/iwe-hofer2022-stages

The script must confirm the exact number of source pods/seed-per-pod complete plants and check source-estimated seed totals against pod-count x average-pod-seed algebra. It then produces per-stage held-shelter RMSE and visitor-added improvement.

**Scientific discriminator:** If visitor information is associated mainly with fruit conversion but not within-pod seeds, this would motivate a service-stage gate. If it predicts none of the downstream ratios, it would weaken an interpretation beyond overall resource allocation. Neither result identifies causal effects from observational visitation rates.

## Claim ceiling

- No original date-specific partner activity: no IWE adult–flower synchrony or phase-lag effect.
- Naturally observed visits are not randomized service intensity.
- Estimated total seed number and per-pod counts are not direct observed germination/recruitment or maternal lifetime fitness.
- Partly algebraically linked outputs, one source experiment and just 5 shelters, cannot support a new cross-taxon universal inference.
- No new strict IWE H1 effect or independent dependence cluster is admitted.

Outputs contain only a derived audit JSON, not redistributed individual original CSVs.
