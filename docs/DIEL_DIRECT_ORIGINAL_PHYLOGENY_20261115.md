# Direct diel E under source-shared species and original phylogeny (2026-11-15)

## Question and current evidence

Building on IWE PR #125 (direct day/night reproductive difference) and commit b184b79 (original phylogenetic robustness of the previous open-referenced A), this analysis asks whether positive publication-only **E = (night-only − day-only)/(night-only + day-only)** means persist when identical species across publications and the original author tree are modelled together.

**This is the same Kendall & Nicholson (2025) published research corpus, DOI 10.1111/ele.70036, NOT independent biological replication, NOT a new ALAN manipulation, and NOT IWE strict-H1 seasonal fitness evidence.** The original authors already analysed diel and phylogenetic effects with a different SMD model. E is a bounded *outcome index*, not a percent change or a true pollen-flux partition.

## Provenance and methods

- Original treatment Git blob: 39a82d966afcdde670603add1c881ace8791ffe9.
- Original traits Git blob: 18381e550a7e405fe4f198909f0bb381bbecf1e0.
- Author tree RData Git blob: d823c2adbdd088372168addece4ec34063ad0b8a; converted 139-tip tree JSON SHA256 34324b8e97b87abdca53a6d578187d0bc239f2cab58974c48b58933398c84a7f.
- Original 1,094-row final source mapping RData Git blob: 82935a0ab6172106e798d3bee88c43359007699a; converted CSV SHA256 3be56ba387a338795037f0fcee3e41ae2d9c5bcf26434f3421565ea10f18b07b.

The original E positive-error panel has 254 exact experimental cells/100 publication IDs/100 source plant names. Two E cells of *Mitrastemon yamamotoi* (one publication, fruit and seed) lack an author-tree tip, yielding 252 cells/99 union publication IDs/99 plant taxa for the common tree-comparable panel. These remain in the complete publication-only reference and are excluded **only from the explicitly tree-common sensitivity**. No fuzzy taxonomic grafts or family pseudo-tree are invented.

Within each paper, source cells are averaged equally. Unknown within-paper sampling covariances use the same first-order upper bound as PR #125. Publication weights and original membership kernels use the actual source taxonomic mapping. Fit three conditional models on the EXACT SAME tree-common cells:

1. publication random intercept;
2. publication plus multiple-species membership;
3. publication, species membership and original shared-ancestry correlation.

Variance components are constrained nonnegative; fit by multistart REML and generalized modified KH t intervals. This is a model **sensitivity**, and component/tree uncertainty is not fully propagated. The Holm two-test summary is post-hoc exploratory, not a new prospective discovery family.

## Original-source quantitative results

| Endpoint | Covariance | Publication IDs | E (conditional nominal 95% CI) |
| --- | --- | ---: | ---: |
| Fruit | publication only | 69 | +0.137568 [+0.023008,+0.252127] |
| Fruit | publication + shared species | 69 | +0.137568 [+0.023008,+0.252127] |
| Fruit | publication + species + original phylogeny | 69 | **+0.137568 [+0.023008,+0.252127]** |
| Seed | publication only | 59 | +0.140704 [+0.026461,+0.254948] |
| Seed | publication + shared species | 59 | +0.133060 [+0.013926,+0.252194] |
| Seed | publication + species + original phylogeny | 59 | **+0.071684 [−0.155222,+0.298589]** |

In fruit set, conditional REML estimates the added species and phylogeny components at the zero boundary. This does NOT demonstrate that relatedness has no biological effect: relatively few plant species recur across actual publications and the endpoint/source selection also differs from the A study. The positive E fruit result is model-conditional. In seed set, phylogenetic covariance widens uncertainty and the adjusted mean is unresolved. **Neither endpoint supports a universal nonconditional nighttime advantage**, and combining fruit and seed into one common fitness measure would erase essential endpoint distinctions.

The earlier A source (commit b184b79) gave full-phylogeny nominal intervals crossing zero for BOTH fruit and seed. This does not conflict with the E result: A is an open-dependent rescaling of E, but source precision eligibility, species coverage, and fitted covariance vary with the index. There is no legitimate independent replication across A and E nor a tested causal difference between their fitted models.

## Independent computational verification

Local audit:

1. Reconstructed all six earlier A covariance fits using an independent tree-incidence implementation; reproduced the b184b79 published means/limits to the reported rounding.
2. Refit all six E covariance models on source-authenticated rows.
3. Independently rebuilt shared-ancestry correlation from root-to-tip paths and optimized the full E models using eigen-decomposition + Nelder–Mead, distinct from the production Cholesky + analytic-score L-BFGS-B optimizer.
4. The two full-phylogeny objective differences were at most 2.3 × 10^-13 and both independent fits converged.

GitHub Actions reruns tests and fetches all four original source files by immutable Git blob, converts the two original RData objects, reproduces the same numeric outcomes, then independently checks the two full E likelihood optima. Artifacts store **only aggregate data and audit receipts**, not the original coordinates or study notes.

## Ecological scope

The current conclusion is not a night-light exposure coefficient. Night-only and day-only pollinator exclusion treatments establish **reproductive access potential**, not the behavior of actual effective nocturnal visitors under ALAN, their replacement by day insects, autonomous selfing rates, or final viable seed supply. It cannot be directly joined to chocho butterfly larval-host geography without same-species/site/year timing, visitor and plant fitness data. Original paper conclusions are not overturned.

Reproduction:

    python scripts/run_diel_direct_lineage.py --author author.csv --traits traits.csv --tree diel.tree.out.json --original-analysis diel.all.diffs.csv --out results
    python scripts/verify_diel_direct_phylogeny.py --author author.csv --traits traits.csv --tree diel.tree.out.json --original-analysis diel.all.diffs.csv --models results/direct_phylogeny_models.csv --out results/independent_recheck.json

The primary blocker for a mechanistic IWE × ALAN causal claim is still source-matched ALAN treatment, actual partner activity/quality, and independently measured reproductive outcome. This analysis changes only the confidence attached to the previously estimated diel baseline.
