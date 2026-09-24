# IWE — Interaction Window Ecology

IWE is a **hypothesis-testing meta-analysis project** on the reproductive consequences of phenological synchrony in plant–animal interactions.

## Primary question

> Does the fitness effect of phenological synchrony differ among mutualists, antagonists, and mixed pollinating seed predators?

IWE is empirical rather than theoretical. It synthesizes published effects, preserves dependence from extraction through reference inference, and separates direct interaction phenology from occurrence-derived potential overlap.

## Primary hypotheses

- **H1 — interaction-type moderation:** synchrony effects differ among `mutualist`, `antagonist`, and `mixed_pollinating_seed_predator` systems.
- **H2 — mixed-system curvature:** in mixed systems, greater synchrony need not monotonically improve plant reproductive performance.
- **H3 — redundancy buffering:** effective partner redundancy may reduce reproductive loss under mismatch. H3 is secondary.

Strict H1 effect sizes are oriented so **positive = greater synchrony is associated with higher plant reproductive performance**. Signed lags are not automatically treated as synchrony: admissibility and orientation are governed by `docs/TIMING_METRIC_CONTRACT.md`.

## Evidence tiers

- **Tier A:** direct matched phenology–fitness evidence. A Tier-A row enters strict H1 only when `timing_analysis_class = strict_window`.
- **Tier B:** direct phenology plus intermediate functional outcome. Mechanism/context only.
- **Tier C:** occurrence-derived potential overlap. Extension/screening only; never pooled into Tier A and always `proxy_only`.

Tier A therefore describes evidence provenance, not automatic eligibility for the strict synchrony estimand. Direct seasonal-timing effects, directional mismatch effects, and unresolved signed-lag effects remain extractable without being forced into H1.

## Screening registry

`data/registry/studies.csv` is the source of truth for screening decisions. The counts and record table in `docs/SCREENING_BATCH_001.md` are generated from that registry and CI fails if the Markdown snapshot drifts.

## Dependence

Every extracted effect carries a `dependence_id`. The reference primary workflow clusters uncertainty by that identifier rather than treating effect rows as independent.

Outputs distinguish:

- `k_effects` — extracted effect rows;
- `m_dependence` — inferential dependence clusters.

With fewer than two dependence clusters in an interaction class, the workflow withholds SEs and confidence intervals. See `docs/ANALYSIS_DEPENDENCE_CONTRACT.md`.

## Current real strict-H1 corpus

The current real extraction contains seven strict-H1 rows across all three interaction classes.

Mutualists:
- `IWE029_LATE_VS_PEAK_NP_LOGOR` — *Stigmaphyllon paralias* × oil-collecting *Centris* bees; `log_odds_ratio = +1.55`.
- `IWE027_2007_HIS_M_VS_E_SEEDSET_SMD` — *Phyllodoce aleutica* × bumblebees; high-worker-bee M window versus low-visit E window; intact natural seed set; `standardized_mean_difference = +0.8518282660`.
- `IWE027_2007_GOS_M_VS_E_SEEDSET_SMD` — the same 2007 regional contrast at GOS; `standardized_mean_difference = +1.0038892388`.
- `IWE023_2015_W1_VS_W4_SEEDSET_SMD` — *Mertensia ciliata* × seasonal pollinator assemblage; experimentally shifted week 1 has >5× the contemporaneous visitation of week 4; final seed set; `standardized_mean_difference = +0.3732395638`.

Antagonists:
- `IWE011_HA_VS_HD_FINALSET_SMD` — *Peucedanum multivittatum* × *Phaulernis fulviguttella*; high-overlap HA versus low-overlap HD; final intact-fruit set; `standardized_mean_difference = -1.1368391965`.

Mixed pollinating seed predators:
- `IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — *Silene stellata* × *Hadena ectypa*; `standardized_mean_difference = -0.0453662495`.
- `IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — the same mixed system in 2013; `standardized_mean_difference = +0.0225087081`.

The two IWE027 rows share one dependence cluster and the two IWE015 rows share one dependence cluster. IWE023 is a second, independent mutualist SMD cluster. **Standardized mean difference is the first native effect family represented in all three preregistered interaction classes, and the mutualist class now reaches the frozen two-cluster minimum.** H1 nevertheless remains **not evaluable** because antagonist and mixed systems still have only one independent SMD cluster each; the reference gate requires at least two per class before inferential class contrasts are allowed.

Study/component admission is recorded in `data/registry/strict_h1_adjudications.csv`; screening inclusion alone does not authorize strict-H1 pooling.

## Replication target

The current operational priority is **not** to add more effects from already represented programmes. IWE targets the native `standardized_mean_difference` family and requires **at least two independent `dependence_id` clusters per interaction class** before class-level inference is considered minimally evaluable.

Current SMD replication state:

- mutualist: **2 independent clusters — target satisfied**;
- antagonist: 1 independent cluster;
- mixed pollinating seed predator: 1 independent cluster.

The machine-readable claim status reports both current cluster counts and remaining gaps. Search/extraction priority is frozen as:

1. second independent mixed programme;
2. second independent antagonist programme;
3. second independent mutualist programme — **satisfied by IWE023**.

Adding another year, site, or outcome inside an existing dependence cluster does not advance this replication target.

## Replication candidate readiness

The four-gate candidate ledger is `data/registry/replication_candidates.csv`. A candidate advances the two-cluster target only when all four conditions are satisfied: independent programme, independently measured timing window, post-predation final reproduction, and SMD-ready summary statistics.

Current replication-search state is:

- mixed #2: **one P1 programme-completion lead but no ready one-blocker effect** — Bopp & Gottsberger 2004 (*Silene × Hadena bicruris*) directly measures same-season flowering–moth overlap but lacks final plant reproduction in the article; Bopp's 2003 Zoologica monograph is the highest-value archival target. Batch 004 rejects *Dianthus–Hadena* and *Rheum–Bradysia* because damage/egg receipt cannot substitute for an independent partner window, rejects *Chamaerops–Derelomus* because benefit and larval cost are separated by plant sex/tissue, and keeps the senita-cactus programme only as P2 because strict timing and mature-fruit endpoints occur in different experimental components;
- antagonist #2: **one strong P1 one-blocker candidate** — Jordano et al. 1990, *Astragalus lusitanicus × Tomares ballus*. Weekly focal-season egg laying and immature-inflorescence availability directly establish the partner window, and final ripe-fruit reproduction is reported. The blocker is the correct SMD sampling unit: published RSI N is inflorescence-level within patch, so those observations cannot be treated as independent replicates of the patch-level synchrony contrast. Plant/shoot-level raw data or variance is still required;
- mutualist #2: **complete** via IWE023 (*Mertensia ciliata*). Four experimental flowering cohorts were ordered by same-season visitation; week 1 versus week 4 final seed set yields Hedges g = +0.3732395638 from published relative group means and the balanced ANOVA F statistic, with no variance imputation.

The next mixed and antagonist search targets must jointly provide contemporaneous partner activity, a prospectively orderable plant timing contrast, final realized plant reproduction, and SMD-compatible variance-bearing summaries.

No candidate is promoted by qualitative direction alone, and no SMD is reconstructed from a regression slope or model-derived fitness surface.

## Initial candidate system families

The search starts from, but is not restricted to:

- `Hadena × Caryophyllaceae`
- `Epicephala × Phyllanthaceae`
- `Tegeticula/Parategeticula × Yucca`
- `Agaonidae × Ficus`
- `Chiastocheta × Trollius`
- `Greya × Lithophragma`
- other pollinator systems with repeated phenological mismatch and reproductive outcomes
- florivore / seed-predator systems with matched phenology and reproductive outcomes

Candidate status is not admission.

## Project boundary

IWE does **not** estimate `L`, `R`, `K`, `Phi`, accessibility, invasion, fixation, occupancy, or BITA mechanism allocations. SCH/BALANCE/SLK/BITA/PAYOFF may later use IWE as external empirical context, but IWE stands as an independent meta-analysis.

## Repository layout

```text
docs/        hypotheses, screening, effect-size, timing, dependence and claim contracts
data/        registries, extraction templates and derived tables
src/iwe/     validation, screening, overlap, effect orientation and meta helpers
scripts/     executable validation and analysis entry points
examples/    synthetic software fixtures only
tests/       contract and regression tests
```

## First-release success criterion

The first release must validate registries and extracted effects, keep screening documentation synchronized to the registry, enforce the timing-metric contract in code, admit only strict Tier-A synchrony effects to H1, use `dependence_id` in uncertainty and sensitivity analyses, exclude Tier C from the primary dataset, and emit no biological conclusion before adequate real literature extraction.

See `docs/superpowers/specs/2026-09-16-interaction-window-meta-analysis-design.md` for the frozen design.
