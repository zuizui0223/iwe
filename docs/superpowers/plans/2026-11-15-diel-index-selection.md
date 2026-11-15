# Diel direct-index source-selection audit: archived implementation plan

> Original analysis was performed locally on 2026-11-15 from the frozen IWE PR #123 source; this note travels with the subsequent GitHub PR.

**Goal:** Test whether a positive publication-weighted matched diel effect depends on the open-referenced normalization A or requirement for an eligible open arm. Direct E=(N-D)/(N+D) must be calculated without inventing missing open, zero-value errors or source precision.

**Inputs:** Kendall & Nicholson (2025), DOI 10.1111/ele.70036, accepted original 1,652-row author file (Git blob 39a82d966afcdde670603add1c881ace8791ffe9), trait blob 18381e550a7e405fe4f198909f0bb381bbecf1e0.

**Design:** Reuse exact study×taxon×site×year×metric×unit matching, calculate E and first-order covariance bounds, aggregate source cells within publication, fit FRUIT and SEED REML separately, Holm-adjust the two primary p values. Compare A/E only on exactly shared precision-eligible cells, retain all published means in secondary diagnostics, run publication-block leaveouts and publication bootstrap.

**Negative controls:** A is a positive algebraic reweighting of E when open>0 and not independent evidence; both-zero D/N is undefined; zero delta variance cannot create infinite precision; sample selection contrast cannot be interpreted as randomized; incomplete flowering or mating-system traits cannot be used to exclude primary data; ALAN is absent.

**Execution:** Baseline 252 tests. Red missing-module tests observed before implementation, 14 new green tests; 266 total local tests passed. Independent delta gradients, PSD covariance, original matched-cell agreement and REML likelihood score checked. New remote CI and original-source Action required before merging. After IWE b184b79, include the explicit caveat that previous A loses interval exclusion of zero when the original phylogeny and shared species are modeled; direct E has not received the same phylogenetic refit.
