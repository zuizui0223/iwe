# Nighttime ALAN exposure and next-day reproductive function: IWE × ALAN bridge

Status 2026-11-15: source-pinned exploratory reanalysis of an ALAN Draft PR #78 dataset derived from original published Supplementary Table S3. No new independent biological observations or validated causal meta effect.

## The important ecological correction

The original Grognuz & Knop (2026) PREPRINT, DOI 10.13140/RG.2.2.36822.10563, used potted Trifolium pratense and Centaurea jacea with 3 nights of ALAN/dark exposure crossed with slug presence/absence. Target flowers were kept under fine-mesh bags except for a subsequent 90-minute DAYTIME pollinator-choice experiment, after which they were rebagged until seed formation. The source includes separate fully bagged control flowers: Trifolium 0/9 bore seeds; Centaurea 3/30 bore some seeds. Consequently nighttime exclusion is not provably perfect, but the vast majority of successful pollination occurred during the daytime choice.

The study demonstrates that nighttime lighting history can alter reproductive success in flowers receiving nearly all their pollination opportunities during the day. Thus ALAN effects must not be MODELLED as occurring EXCLUSIVELY through direct nighttime moth visitation to the focal flower. This does not by itself refute moderation by true baseline nighttime reliance: the plants' baseline dark-day/dark-open dependence was not measured in this experiment.

Possible distinct mechanisms are nocturnal effective pollen delivery, next-day pollinator behavior or flower condition, slug/other herbivory, and direct plant photophysiology. None of these component effects or mediation paths is individually isolated by these summaries.

Author source: https://www.researchgate.net/publication/401424487_Artificial_light_at_night_restructures_daytime_plant-pollinator_interactions_through_direct_and_herbivore-mediated_pathways
Raw data repository DOI https://doi.org/10.17632/drhzznh4ps.1. We have NOT obtained the actual author source CSV; this reanalysis uses only an independently checked 28-round source-derived table of means and source n created in ALAN Draft PR #78, using source commit 331b729ec43b680f6b1f20cfd796a40e92307994 and exact Git blob 92283023f36872d24b17a637e493e9d3bcda9bb0.

## Source-defined factorial comparison and actual numbers

28 daytime choice rounds: 20 Trifolium and 8 Centaurea; 16 original target pots per round, so 448 potential outcomes, 425 measured seeds, 23 missing values. Four treatments per round: dark/no slug; dark/slug; lit/no slug; lit/slug. Multiple rounds reused plants and nightly lighting locations: 28 choice rounds are NOT 28 independent experimental light assignments.

Each round's original four means are treated equally within its plant species. They are NOT treated as 16 independent experimental lamp sites. Only exact site/light-replicate covariance or full independent assignment is sufficient for a new confirmatory causal CI.

| Plant species | Rounds | Mean seeds dark, both slug conditions | Lit | Lit/dark | No-slug lit/dark | Slug-present lit/dark |
|---|---:|---:|---:|---:|---:|---:|
| Trifolium pratense | 20 | 4.9250 | 3.5188 | 0.7145 | 0.8052 | 0.6378 |
| Centaurea jacea | 8 | 1.4792 | 1.0573 | 0.7148 | 0.2708 | 1.1714 |

Both species have lower source block-mean daytime seed production after nightly ALAN even without experimental slugs. However this does NOT identify a direct plant-light mechanism, its magnitude in independent installation sites, or a species-level significance test. In Centaurea the slug-present arm reverses descriptively; the paper did not establish a significant light×slug interaction for seed reproduction.

Original published author model: daytime visitation coefficient beta=-0.38 (95% interval -0.60 to -0.16; p=.013), and later seed production coefficient beta=-0.40 (95% interval -0.73 to -0.08; p=.014). Those are author MODEL estimates, NOT log ratios calculated from these four treatment means; there is NO valid newly fitted mediation coefficient.

## Missing outcomes and bagging controls

Original source observation counts are 425, missing are 23. Trifolium: observed total seeds dark 783 and lit 540, with dark-side missing 2 and lit-side missing 7 pots. Centaurea: observed total seeds dark 94 and lit 62, with dark missing 6 and lit missing 8.

An extreme sensitivity thought experiment assumes all missing dark pots would have produced zero seeds and asks how many seeds each missing lit pot would need to produce for total-seed equality. Trifolium requires >34.714 missing-lit seeds per pot, Centaurea requires >4.000. These are tipping values, NOT imputed outcomes or 95% intervals. Centaurea is particularly sensitive to incomplete seed measurements.

Three out of 39 fully bagged control flowers produced some seeds; this rejects an absolute statement that none of the flower's seeds could arise outside the daytime choice. It does not invalidate the source statement that most pollination occurred during the 90-minute daytime session.

## Relationship to original IWE and ALAN evidence

IWE #127 estimates the marginal reproductive value of nighttime access in the original Kendall & Nicholson daytime-nighttime exclusion experiments. These are baseline pollinator-access measures, not light responses. The Grognuz daytime carryover experiment measures a DIFFERENT light-associated reproductive pathway and cannot be combined with IWE #127 as a shared-source beta or independent replication.

IWE #128 corrected a false ALAN vulnerability beta: moderator V=1-D/O and response y=log(L/O) reuse a dark-open denominator. Their measurement errors induce a negative correlation under a true zero ALAN effect. This new study also lacks original dark-open vs dark-day-only nocturnal dependence, and cannot be assigned a numerical V based on flower morphology or other species elsewhere.

Macgregor et al. (2019), DOI 10.1002/ecs2.2550, has a true light×day/night-access factorial design but its interaction SE and treatment cells are still absent; its published light×caging interaction was reported nonsignificant. Lu et al. (2026), DOI 10.1093/jpe/rtag160, reported a -56 percent seed-set change in the NIGHT-ONLY access arm, NOT the open-access whole-plant seed output. Boom et al. (2020) describes a nursery pollinator-seed predator with nonsignificant model-derived total seed yield despite component changes. Knop et al. (2017) tested lighting×ALL-visitor-bagging, not nocturnal-specific exclusion. These outcomes are not one homogeneous meta-effect.

The scientifically admissible revised prediction is conditional: ALAN's reproductive effect may travel via nocturnal pollen loss, next-day carryover, direct floral physiology, or opposing seed-predator pathways. Their relative contribution requires truly matched original experimental units, four-arm outcomes, corrected shared control covariance and stage-consistent denominators. Present evidence does NOT provide a common ALAN×night dependence interaction beta or island×ALAN field experiment.

## Reproducibility and source provenance

Run the IWE script scripts/audit_alan_daytime_carryover.py with --alan-derived-block-source pointing to the immutable ALAN-derived CSV and --out-dir selecting an output directory. The GitHub workflow at .github/workflows/alan-daytime-carryover-source.yml automatically downloads that exact file from the pinned upstream ALAN commit and verifies its original Git blob; it rechecks all eight source published pot means, all 28 rounds, true observed seed totals and missingness, source control-flower failure rates, per-species no-slug/light contrasts, and lack of independent lighting SE. Aggregate-only outputs are a two-species CSV and a JSON evidence receipt. The original individual 448 author pot observations and source location records are not redistributed.

Conclusion: documented daytime carryover is an important second PATHWAY, not an additional independently verified light-allocation experiment or new IWE seasonal synchrony H1 effect.
