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

The current real extraction contains four strict-H1 rows across all three interaction classes:

- `IWE029_LATE_VS_PEAK_NP_LOGOR` — mutualist; *Stigmaphyllon paralias* × oil-collecting *Centris* bees; late high-pollinator window versus peak low-pollinator window; natural-pollination seed set; `log_odds_ratio = +1.55`.
- `IWE011_HA_VS_HD_FINALSET_SMD` — antagonist; *Peucedanum multivittatum* × *Phaulernis fulviguttella*; high-overlap mid-July HA versus low-overlap August HD; final intact-fruit set; `standardized_mean_difference = -1.1368391965`.
- `IWE015_2012_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — mixed pollinating seed predator; *Silene stellata* × *Hadena ectypa*; Hadena-dominant early window versus co-pollinator-dominant late window; successful fruits; `standardized_mean_difference = -0.0453662495`.
- `IWE015_2013_EARLY_VS_LATE_SUCCESSFRUIT_SMD` — the same mixed system and contrast in 2013; `standardized_mean_difference = +0.0225087081`.

The two IWE015 rows share one dependence cluster, so the mixed class still contributes only one independent cluster. The standardized-mean-difference family now contains antagonist and mixed evidence, whereas the mutualist strict effect remains on the log-odds scale. H1 therefore remains **not evaluable**: no single native effect family spans all three interaction classes, and no class yet has the minimum two independent dependence clusters required for reference inference.

Study/component admission is recorded in `data/registry/strict_h1_adjudications.csv`; screening inclusion alone does not authorize strict-H1 pooling.

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
