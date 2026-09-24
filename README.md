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

The current real extraction contains six strict-H1 rows across all three interaction classes.

Mutualists:
- `IWE029_LATE_VS_PEAK_NP_LOGOR` — *Stigmaphyllon paralias* × oil-collecting *Centris* bees; `log_odds_ratio = +1.55`.
- `IWE027_2007_HIS_M_VS_E_SEEDSET_SMD` — *Phyllodoce aleutica* × bumblebees; high-worker-bee M window versus low-visit E window; intact natural seed set; `standardized_mean_difference = +0.8518282660`.
- `IWE027_2007_GOS_M_VS_E_SEEDSET_SMD` — the same 2007 regional contrast at GOS; `standardized_mean_difference = +1.0038892388`.

Antagonists:
- `IWE011_HA_VS_HD_FINALSET_SMD` — *Peucedanum multivittatum* × *Phaulernis fulviguttella*; high-overlap HA versus low-overlap HD; final intact-fruit set; `standardized_mean_difference = -1.1368391965`.

Mixed pollinating seed predators:
- `IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — *Silene stellata* × *Hadena ectypa*; `standardized_mean_difference = -0.0453662495`.
- `IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — the same mixed system in 2013; `standardized_mean_difference = +0.0225087081`.

The two IWE027 rows share one dependence cluster and the two IWE015 rows share one dependence cluster. **Standardized mean difference is now the first native effect family represented in all three preregistered interaction classes.** H1 nevertheless remains **not evaluable** because each SMD class currently has only one independent dependence cluster; the reference gate requires at least two per class before inferential class contrasts are allowed.

Study/component admission is recorded in `data/registry/strict_h1_adjudications.csv`; screening inclusion alone does not authorize strict-H1 pooling.

## Replication target

The current operational priority is **not** to add more effects from already represented programmes. IWE targets the native `standardized_mean_difference` family and requires **at least two independent `dependence_id` clusters per interaction class** before class-level inference is considered minimally evaluable.

Current SMD replication state:

- mutualist: 1 independent cluster;
- antagonist: 1 independent cluster;
- mixed pollinating seed predator: 1 independent cluster.

The machine-readable claim status reports both current cluster counts and remaining gaps. Search/extraction priority is frozen as:

1. second independent mixed programme;
2. second independent antagonist programme;
3. second independent mutualist programme.

Adding another year, site, or outcome inside an existing dependence cluster does not advance this replication target.

## Replication candidate readiness

The four-gate candidate ledger is `data/registry/replication_candidates.csv`. A candidate advances the two-cluster target only when all four conditions are satisfied: independent programme, independently measured timing window, post-predation final reproduction, and SMD-ready summary statistics.

Current highest-priority blocked candidates are:

- mixed #2: `IWE014` (*Silene vulgaris × Hadena*) — biologically admissible, blocked only by unrecovered mean + SD/SE + n;
- mixed #2 alternate: *Silene ciliata × Hadena consparcatoides* — independent Iberian programme, blocked only by unrecovered post-predation fecundity summary statistics;
- antagonist #2: no current one-blocker candidate. Full-text audit demotes `IWE013` (*Actaea spicata × Eupithecia immundata*): the 2008 paper imports the predator oviposition window from earlier studies rather than measuring partner activity contemporaneously, so it fails the frozen strict-window timing gate before SMD recovery is considered. The next search target is an independent antagonist programme with contemporaneous predator activity, final plant reproduction, and variance-bearing group summaries.

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
