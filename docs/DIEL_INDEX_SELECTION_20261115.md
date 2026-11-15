# Direct day-versus-night index: source-selection and interpretation audit (2026-11-15)

## Status and lineage

This exploratory analysis extends IWE PR #123 at commit 4bb01a51 and is compatible with subsequent IWE commit b184b79 (PR #123's species + original phylogeny + endpoint-denominator robustness). Original published data are from Kendall & Nicholson (2025), DOI https://doi.org/10.1111/ele.70036, not from new field collections or an ALAN light manipulation. This analysis does NOT change the strict IWE seasonal-synchrony H1 dataset, the frozen chocho manuscript or the ALAN manuscript.

Original author files are SHA-pinned:
- data/DvN_LiteratureDataClean_2024-09-13.csv Git blob 39a82d966afcdde670603add1c881ace8791ffe9 (1,652 original treatment records, 140 original source publication identifiers).
- data/SppTraitData_clean.csv Git blob 18381e550a7e405fe4f198909f0bb381bbecf1e0.

No original coordinates, field notes or author per-plant source records are redistributed. Original source bytes are fetched transiently by GitHub Actions and their Git blob hashes are checked before analysis.

## What changed

The old matched index uses open reproduction (O), day-only (D), night-only (N):

A = (O-D)/(O+D) - (O-N)/(O+N)

The new direct diel index uses only D and N:

E = (N-D)/(N+D)

The exact identity for nonnegative values with defined denominators is:

A = E * 2*O*(D+N)/((O+D)*(O+N))

With O>0, A and E must have identical signs. They therefore CANNOT be treated as two independent confirmations of nighttime functional dominance or biological compensation. When O=0 and D,N>0, A becomes exactly zero irrespective of the nonzero direct effect E. The E index is bounded [-1,1], unitless and NOT a percent reproductive loss.

Only D and N have to be source-aligned. Missing/imprecise or duplicate unrelated open rows do not invalidate the direct comparison. The exact 14-element study/species-cultivar/site/coordinates/year/month/outcome/response-unit/additional-treatment key from PR #123 is retained. Source trait missingness is retained in primary estimates.

## Source coverage and boundary safeguards

- Matched D/N means: 392 exact source cells / 130 publication IDs / 133 plant names.
- Source SEM or SD+n and positive first-order variance: 254 cells / 100 publication IDs / 100 plant names.
- Prior A mean panel: 344 cells; 341 overlap E. Three prior A cells have both D and N zero (E mathematically undefined); 51 E cells have missing/ineligible open-arm means.
- Twenty-one prior A-precision cells have E's zero first-order delta variance (18 fruit, 3 seed). These are retained for descriptive means but NOT assigned infinite meta-analytic precision. Twenty-one other E-eligible cells enter, coincidentally leaving the total positive-variance precision count at 254.
- No zero imputation or post-hoc continuity correction. Missing source error estimates remain missing.

## Primary publication-level direct E meta-analysis

Separate FRUIT and SEED endpoints, source cell equality within publication, first-order unknown-covariance upper bound, publication-level REML with modified Hartung–Knapp intervals. Two exploratory tests use Holm adjustment.

| Endpoint | Source precision cells | Publication IDs | E (95% CI) | Holm-adjusted p |
| --- | ---: | ---: | ---: | ---: |
| Fruit set | 145 | 70 | +0.135289 [+0.022419,+0.248158] | 0.03418 |
| Seed set | 109 | 60 | +0.138884 [+0.025647,+0.252121] | 0.03418 |

Single-publication exclusions retain a nominal positive mean but both working-scale prediction intervals span zero. Fruit prediction upper interval can exceed +1 because it is a normal approximation on a naturally bounded scale; this is not a possible biological effect. The upper sampling-variance bounds alone do not guarantee conservative coverage of the final REML interval.

In the corresponding publication-level sign diagnostic the positive means occur in 40/70 fruit papers and 35/60 seed papers. Two-sided exact sign test p=0.282 and 0.245 respectively. A positive magnitude-weighted mean does not mean a confirmed majority of studies shows nighttime superiority.

## Same-cell A/E sensitivity (not independent replication)

For exact cells satisfying BOTH indices' positive precision criteria:
- Fruit, 62 publication IDs: E +0.125965 [0.007590,0.244339] versus A +0.107655 [-0.003115,0.218424].
- Seed, 55 publication IDs: E +0.117144 [-0.000982,0.235270] versus A +0.129363 [0.019421,0.239305].

Differences in CI overlap with zero are NOT an independent between-model significance test. Both models use the same biological observations. Gained vs common source cohorts are jointly bootstrapped at publication level and their descriptive differences are unresolved.

Additional weaknesses:
- Native-only seed index +0.12232 [-0.00161,0.24626], unresolved.
- Nearly balanced experimental day/night hours fruit +0.10640 [-0.11721,0.33001], unresolved.
- Unknown bloom categories remain in the main analysis; source sex-system labels cannot be converted to autonomous-selfing rates.
- Original 140-ID working source roster and bounded index are not the authors' curated 135-study phylogenetic SMD analysis.

## IMPORTANT: follow-up species/phylogeny robustness already available on main

Current IWE commit b184b79 adds a phylogenetic and repeated-species robustness model for the PRIOR A index. On a common tree-compatible panel, fully accounting for shared species and the original author phylogeny yields:
- Fruit A +0.11449 [-0.04650,+0.27548] across 66 publication IDs.
- Seed A +0.10324 [-0.07379,+0.28028] across 55 IDs.

Both intervals include zero. These are conditional nominal intervals with other limitations, but they mean neither this direct E analysis nor the older A publication-only positive interval may be promoted to a globally robust, phylogenetically independent nighttime advantage. The current E model has NOT itself yet been refitted with the original phylogenetic covariance; the previous A-based result is an informative caution, NOT an automatically transferable E p-value.

The original article already reported endpoint-dependent day/night patterns. This index exercise tests algebraic and source-selection sensitivity, not novelty of the basic diel comparison and not evidence for light-induced compensation.

## IWE × ALAN × chocho claim firewall

A day/night visitor-exclusion study measures potential reproductive value of the two diel windows. It does not demonstrate which visitors are actual effective vectors, nor their activity under artificial lighting. Source-defined chocho host-plant geographic ranges do not measure local moth visitation, adult behavior, time overlap, or plant seed output. Do not claim source-matched local ALAN×phenology×plant breeding-system interactions or independent IWE H1 effect sizes.

## Reproducibility

    python -m pytest -q tests/test_diel_index_selection.py
    python scripts/run_diel_index_selection.py --author /path/author.csv --traits /path/traits.csv --out results/diel-index-selection

The workflow .github/workflows/diel-index-selection.yml checks original Git blob hashes, reruns the original-source model and independently checks both prior exact-cell A values and the REML score-root estimates. Outputs: index_selection_models.csv, primary_two_models.csv, source_coverage.csv, unweighted_source_diagnostics.csv, leave_one_publication.csv, primary_publication_summaries.csv and index_selection_receipt.json.

The original local offline staging run passed 266 tests (two pre-existing FutureWarnings) before PR submission. CI status must be independently verified for the actual new GitHub head; the local staging result alone does not prove remote success.
