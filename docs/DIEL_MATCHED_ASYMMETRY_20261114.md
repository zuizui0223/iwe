# Matched diel reproductive asymmetry and anthesis: source-conditional, not universal night superiority

## Question and distinction from PR122

PR122 estimated separate night-marginal and day-marginal reproductive effects, sometimes from different subsets of publications. This follow-up FIRST pairs the two quantities within exactly the SAME study, plant/cultivar, locality/site-period, coordinates, year/month interval, reproductive metric, original units and additional treatment.

For O=open day-and-night access, D=day-only access and N=night-only access:

`A = (O-D)/(O+D) - (O-N)/(O+N) = 2*O*(N-D)/[(O+D)*(O+N)]`.

Positive A means the normalized night-marginal contribution is larger than the normalized day-marginal contribution in that source experiment. A is a DIFFERENCE OF INDICES, not a percentage loss, a per-hour efficiency, a pollinator-species effect or an ALAN response. For O>0 its sign is the sign of N-D; the nonlinear magnitude depends on the common open reference. Its possible range is [-2,2].

This is a new exploratory reanalysis of Kendall & Nicholson (2025), DOI [10.1111/ele.70036](https://doi.org/10.1111/ele.70036), not independent field replication. The original paper already investigated day/night differences and anthesis traits using phylogenetic models, finding no overall difference in its different full analysis population. The current open-arm-supported subset, effect definition and covariance treatment differ; this does NOT overturn that published conclusion or newly discover that anthesis matters.

## Sources and coverage

Original author dataset Git blob `39a82d966afcdde670603add1c881ace8791ffe9` contains 1,652 rows /140 publication IDs, not the published paper's final 135-study analysis roster. Original trait blob `18381e550a7e405fe4f198909f0bb381bbecf1e0` has 142 name records. Source identities are SHA-verified before reading results.

- 344 matched usable mean cells, 114 publication IDs, 114 taxa.
- 254 cells with supported positive delta precision for the joint contrast, 94 publication IDs, 92 taxa. PR122 had 276 cells/96 IDs with precision for AT LEAST ONE contrast; this paired test requires all O,D,N means/errors. This is mathematical contrast eligibility, not arbitrary complete-case filtering.
- Fruit: 151 cells /67 publication IDs /68 taxa.
- Seed: 103 cells /56 publication IDs /55 taxa.
- Closed/hand-pollinated arms are NOT required. Trait-missing plants stay in the main meta-analysis. The native-only, known-unit, balanced-hours and four-arm subsets are sensitivity checks, not primary exclusions.

The source `breeding_system` variable is hermaphrodite/monoecious/dioecious, NOT self-compatible versus self-incompatible or autonomous selfing. It is not used as a reproductive-assurance moderator. The author `bloom_period_simple` is a species-level day/night/both annotation, not measured flowering receptivity at each study site/year. Missing values remain unknown, and both is never relabelled day or night.

## Uncertainty and predeclared test family

Differentiate A jointly with respect to O,D,N. The common open mean enters only once: its gradient is `2D/(O+D)^2 - 2N/(O+N)^2`. The first-order variance bound is `(sum |g_i SEM_i|)^2`, with the zero-covariance variance as a sensitivity only. Use original SE or SD/sqrt(n), n>=2, and never add arbitrary continuity corrections to a zero denominator or regularize zero derivative variance.

Multiple cells within a publication are averaged with an additional covariance upper bound, leaving one effect per publication per endpoint. Primary fruit and seed models use REML with modified Hartung-Knapp t intervals and Holm adjustment across TWO tests. Upper sampling-variance bounds do not guarantee wider final random-effects CIs because the fitted heterogeneity and weights also change. Publication IDs are not verified independent field programmes, and repeated species phylogeny remains unmodelled.

## Primary paired results

| Outcome | Publications | A | 95% CI | Holm-adjusted p |
|---|---:|---:|---:|---:|
| Fruit set | 67 | +0.151600 | +0.034016 to +0.269185 | 0.024083 |
| Seed set | 56 | +0.141522 | +0.032312 to +0.250732 | 0.024083 |

The positive average paired asymmetry is not merely a subtraction of two meta-analyses with different memberships. However, between-publication prediction intervals span zero: fruit [-0.722,1.026], seed [-0.594,0.877]. The result is not universal across species or settings.

No individual publication dominates (maximum weight 1.84% fruit; 2.24% seed). Every one-publication deletion retains a positive nominal 95% interval; worst deletion p=.02214 fruit, .02308 seed. These are influence diagnostics, not hundreds of additional tests of the hypothesis.

## Sensitivities that weaken a universal claim

| Sensitivity | Fruit A [95% CI] | Seed A [95% CI] |
|---|---|---|
| Native plants only | +0.16283 [+0.03566,+0.28999] (60 IDs) | +0.13334 [+0.01302,+0.25366] (50 IDs) |
| Reported day/night access durations within 10% | +0.11696 [-0.08913,+0.32305] (19 IDs) | +0.30355 [+0.08529,+0.52181] (14 IDs) |
| Explicit original response unit | +0.16576 [-0.03208,+0.36360] (22 IDs) | +0.15508 [+0.03639,+0.27376] (50 IDs) |
| Also has a complete-exclusion mean | +0.14359 [-0.00273,+0.28991] (48 IDs) | +0.07794 [-0.06622,+0.22210] (33 IDs) |

Subsetting changes both precision and source composition. Loss of significance is not evidence that a subset effect is zero or demonstrably different from the full-panel effect. Access duration, bagging effects, publication selection and outcome definitions still matter.

## Original anthesis classes: targeted secondary association

Within each publication and bloom class, first average matched A. Resample the whole publication, retaining both class entries together when the publication includes day- and night-blooming plants. The reported trait association is the night-class minus day-class difference of equal-publication means; it is NOT inverse-variance meta-regression or a randomized flowering-time effect. A 10,000-replicate study bootstrap is accompanied by family-balanced resampling and all-mean versus precision-only panels. Two-outcome Bonferroni simultaneous intervals use 97.5% marginal bootstrap intervals. These two secondary outcomes are exploratory and separate from the two primary tests; no global all-analyses familywise discovery claim is made.

Precision panel:
- Fruit: night-bloom class mean A=+0.33383 (35 publication IDs), day-bloom class A=-0.08937 (16 IDs). Difference **+0.42320**, nominal95 CI [+0.14935,+0.68252], two-endpoint-adjusted interval [+0.11764,+0.72358]. Family-balanced difference +0.45929, nominal95 [+0.14377,+0.77533].
- Seed: night-class +0.25598 (31 IDs), day-class -0.00050 (11 IDs). Difference **+0.25649**, nominal95 [-0.05673,+0.55685]; unresolved. Family-balanced interval also includes zero.

Only **TWO fruit publications and ONE seed publication** with precision compare both anthesis classes. Even with all reported means, there are only three and two respectively. Consequently the association is predominantly BETWEEN studies, regions and taxa. A causal anthesis explanation cannot be separated from these differences. Traits are not a substitute for local visitor identity, and family balancing is not a phylogenetic model.

In the all-mean panel, fruit class association remains positive by publication bootstrap (+0.29356, nominal95 [+0.08225,+0.49752]); its family-balanced two-endpoint-adjusted interval includes zero. The seed association remains unresolved. This limitation is retained, not hidden by precision filtering.

### Explicitly post-hoc composition sensitivity

After noting unequal day/night source representation, average the two class-specific means at a hypothetical 50:50 class weight using the same joint publication bootstrap. This is NOT an estimated global plant-frequency distribution or a correction to the primary result.

- Fruit precision panel hypothetical A=+0.12223, nominal95 [-0.02331,+0.26978].
- Seed precision panel hypothetical A=+0.12774, nominal95 [-0.03513,+0.29460].

Both include zero. Thus source composition materially limits extrapolation from this literature to a universal claim that nighttime function is more important. This sensitivity does not erase the actual within-experiment signal in the assembled source population.

## IWE, ALAN, and chocho

The paired test supplies a functional exclusion benchmark, not a lighting experiment. It does not measure floral-hour/seasonal mismatch, species-specific per-visit pollen efficacy, light-induced compensation, final viable seeds or island/mainland causal contrasts. Blooming class cannot be converted into confirmed moth pollination, autonomous selfing or ALAN susceptibility. The geographic host opportunities in chocho remain a separate scale. No strict IWE H1 effects or modifications of the frozen chocho/ALAN manuscripts are created.

## Reproduction and checks

```bash
python -m pytest -q tests/test_diel_matched_asymmetry.py
python scripts/run_diel_matched_asymmetry.py --author /path/author.csv --traits /path/traits.csv --out results/diel-matched
```

Existing 240 tests plus 12 new tests passed locally (252 total; two pre-existing warnings). Analytic gradients pass finite-difference checks, and random valid covariance matrices stay below the variance bound. All 344 source A values equal the difference of the PR122 exact-cell marginal values within 4.4e-15. Independent REML score-root calculations reproduce the two primary variance-minimization fits within 3e-9.

Outputs: `matched_models.csv`, `matched_source_coverage.csv`, `anthesis_associations.csv`, `matched_leave_one_publication.csv`, `matched_asymmetry_receipt.json`, and workflow `independent_numerical_verification.json`. Output is aggregate-only; original site coordinates and literature notes remain transient.

## Execution design record

Continuation chosen: exact paired-source contrasts plus a preselected anthesis question. Rejected: subtract PR122's separately pooled means; require all trait fields or all four experimental arms; infer self-compatibility from sexual system. The original pre-result plan was saved locally before implementation, twelve expected missing-module test failures observed, then twelve tests passed. The 50:50 class-weight sensitivity was added only after the source-composition imbalance was observed and is labelled post-hoc above. No primary test family was changed in response to results.
