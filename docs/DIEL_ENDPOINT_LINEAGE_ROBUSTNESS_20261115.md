# Endpoint and original-phylogeny robustness of the paired diel contrast

## Status and change in interpretation

Continuation of PR123, exploratory reanalysis of Kendall & Nicholson (2025), DOI 10.1111/ele.70036. All source data are existing published measurements, not new independent experiments. The same paired index A and source sampling bounds are retained.

**The positive pooled difference is NOT robustly resolved once shared species and the original phylogeny are modelled together.** Point estimates remain positive, but both conditional intervals cross zero. This is not proof of no difference, or evidence that phylogeny causes the preceding result. It constrains the broader interpretation of PR123.

## Source recovery and overlap

Original author tree: `output/DvN_plant_phylogeny final.RData`, Git blob `d823c2adbdd088372168addece4ec34063ad0b8a`, SHA256 `e4b35d5a58631e338ce8cafa17638b3eaba02c1fd06b792aefb532b00fe81717`. Original final analysis: `output/DvN_analysis_dataframe final.RData`, blob `82935a0ab6172106e798d3bee88c43359007699a`, SHA256 `b0aa1fa67fc484fa0000ed5f08119733d710d1c21e41c7ac0a018c1c50f6345a`. Both were independently downloaded and checked in [source stage run 43664636302](https://github.com/zuizui0223/iwe/actions/runs/43664636302).

The tree contains 139 original tips. The final source dataframe has the published 1,094 effect rows and 135 publication IDs. Exact original-name to accepted-tip mapping is used; no fuzzy match, new graft, inferred branch length or family-label pseudo-tree.

PR123's source panel remains 344 mean cells/114 IDs; its joint-precision panel remains 254 cells/94 publication IDs/92 source taxa. Four mean cells have no author-tree tip: Saponaria officinalis (Jabbari_2013; already lacks eligible precision) and Mitrastemon yamamotoi (Suetsugu_2018; two eligible endpoint cells). The tree-comparable precision panel therefore has 252 cells/93 IDs/91 source taxa. Both unmapped taxa stay in the full reference and descriptive coverage; all three covariance models use the SAME reduced comparison panel. No other trait-complete filter is applied.

## Publication-level multiple-species membership

Each publication keeps its previous equal-cell mean effect and first-order upper sampling-variance bound, including the previous within-publication unknown-covariance bound. The sensitivity covariance is

`V = diag(v_publication_bound) + tau_publication I + tau_species Z Z' + tau_phylogeny Z R Z'`.

Z contains each publication's proportion of source cells belonging to each accepted species; rows sum to 1. R is the Brownian shared-ancestry correlation calculated from the original dated tree. A publication covering multiple species is NOT assigned a guessed single species. Study, species and phylogenetic variance components are estimated by multistart REML, allowing boundary-zero solutions.

Intervals use generalized modified-KH t scaling, publication-count minus one degrees of freedom, conditional on fitted components/tree. They are **model-conditional robustness intervals, not a guaranteed conservative multilevel procedure**. Variance-component estimation and phylogeny uncertainty are not fully propagated. Publication IDs are not proven independent biological sampling programmes. This is NOT a replication of the original authors' cell-level multilevel SMD model.

## Results on identical tree-comparable panels

| Endpoint | Dependence model | Publication IDs | A [conditional nominal 95% interval] |
|---|---|---:|---:|
| Fruit | Publication only | 66 | +0.15451 [+0.03496,+0.27406] |
| Fruit | Publication + shared species | 66 | +0.13106 [+0.00527,+0.25685] |
| Fruit | Publication + species + original phylogeny | 66 | +0.11449 [-0.04650,+0.27548] |
| Seed | Publication only | 55 | +0.14344 [+0.03319,+0.25369] |
| Seed | Publication + shared species | 55 | +0.12117 [+0.00364,+0.23871] |
| Seed | Publication + species + original phylogeny | 55 | +0.10324 [-0.07379,+0.28028] |

Unchanged full reference results are +0.15160 (67 IDs) and +0.14152 (56 IDs), exactly reproducing PR123. Removing the unavailable tree taxon is not the reason for the uncertainty change. Six covariance-sensitivity p-values are also reported with Holm adjustment; none is below .05. This newly declared robustness family is not a retroactive replacement of PR123's two-test family. The main warning does not depend on that multiplicity choice: the full covariance model's nominal intervals already cross zero.

There are nine species appearing in multiple publications for each endpoint; the maximum is three publications for one species. Thirteen pairs of fruit publications and ten seed pairs share species. Removing all publications involving one accepted species at a time does NOT remove the positive publication-only interval. That is a different question from modelling many correlated species jointly. The phylogenetic variance component is not tested as a biological driver and must not be called a confirmed explanatory mechanism.

## Reproductive denominators

Literal source unit labels were classified BEFORE subgroup effect estimates were run. Generic `proportion`, missing `NA`, and count-to-proportion conversions lacking the denominator are not silently classified as fruits per flower. All remain in the primary/reference models, with an explicit unit-mapping table.

The eligible seed panel contains 71 cells/32 publications measuring seeds per fruit (including pods/capsules), 9 cells/6 publications seeds per plant, 6 cells/6 publications seeds per ovule, and just 1 cell/1 publication seeds per flower. Other categories include viable-seed fractions/counts and unspecified denominators. Classes are not necessarily disjoint publication samples.

Exploratory publication-level contrasts:
- Seeds per fruit: A=+0.09796 [-0.04689,+0.24281], 32 IDs.
- Seeds per plant: +0.34545 [-0.05610,+0.74700], 6 IDs.
- Seeds per ovule: +0.36155 [-0.22413,+0.94723], 6 IDs.
- Seeds per flower: one ID, no pooled estimate.

No denominator subgroup supports a precise universal positive difference. This is not a test showing that subgroup effects are zero or differ statistically; smaller panels and composition changes limit precision. More seeds per surviving fruit is not automatically more viable seeds per whole plant. Broad source labels do not establish the total reproductive-fitness endpoint needed for IWE strict H1.

## Relation to the original paper

The [original published paper](https://doi.org/10.1111/ele.70036) was unresolved overall, but its seed-set stratum was already positive (source SMD 0.521 [0.229,0.812]). Its phylogenetic signal estimate was low and unresolved. Thus the prior abbreviated 'original found no difference' summary was incomplete: the original already distinguished endpoints.

Our index is algebraically

`A = ((N-D)/(N+D)) * [2 O (N+D)/((O+D)(O+N))]`.

For positive O and defined denominators, it has the SAME sign as N-D. It is a reweighting of the same measured diel difference, not independent new biological evidence. It requires an open arm and differs from the original SMD weighting, source selection and hierarchy. Zero-open cases have A=0 without proving direct day/night equality. These checks do not identify which single change accounts for all differences from the original study.

## Verification and execution record

Parent baseline: 252 tests passed after restoring an examples directory omitted from the temporary staging tar. Added tests: 12. Full suite: 264 passed (two pre-existing warnings). The new test initially failed because the module was absent (expected RED). A malformed cycle-test fixture was corrected without changing scientific results.

Independent edge-incidence covariance versus shared-ancestral-path calculations agree within 4.5e-16. All six covariance fits were independently recomputed using eigen-decomposition and derivative-free Nelder-Mead, versus Cholesky/analytic-score L-BFGS-B, agreeing in means within 2.5e-9 and objectives within 3e-14. The A/direct-index identity was checked on 1,000 positive triples. These validate implementation, not ecological identifiability or nominal interval coverage.

The plan was written locally before inspecting subgroup model results: preserve original matched cells; map literal denominators; compare publication-only, species and phylogenetic covariance on common panels; do not graft unavailable taxa; no model shopping or new causal hypothesis. The shared-species kernel includes exact multiple membership rather than family-balanced pseudo-replication.

Run `scripts/run_diel_endpoint_lineage.py` with the hash-verified original treatments/traits, decoded original tree and final analysis dataframe. `scripts/verify_diel_lineage_numerics.py` independently checks numerical results. Only aggregate models, coverage, dependence counts, leave-species-out summaries and provenance are exported. No coordinates or original literature notes are in the analytical output.

No ALAN coefficient, pollinator compensation, island effect, phenotype evolution, selfing mechanism or new IWE strict-H1 effect is inferred. ALAN and chocho manuscripts/branches remain unchanged. Stronger evidence requires matched functional endpoints and independent ecological mechanisms, not relabelling the same diel contrast as repeated independent evidence.
