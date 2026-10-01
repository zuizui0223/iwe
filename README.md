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

`docs/EVIDENCE_AUDIT_STATUS.md` is the generated paper-facing audit of the full evidence funnel. It keeps publication screening (32 registered publications) separate from the broader replication-candidate ledger (50 programme/completion leads), and CI fails if its strict-effect, cluster, rejection, or completion-route counts drift from the registries.

`data/registry/search_runs.csv` and `docs/SEARCH_COVERAGE_STATUS.md` separately track systematic-search completeness. The current search claim remains `targeted_only` until all required Web of Science, Scopus, dissertation/grey-literature, and citation-snowball runs are completed, exported, and deduplicated.

## Dependence

Every extracted effect carries a `dependence_id`. The reference primary workflow clusters uncertainty by that identifier rather than treating effect rows as independent.

Outputs distinguish:

- `k_effects` — extracted effect rows;
- `m_dependence` — inferential dependence clusters.

The reference workflow now uses a REML working random-effects model with CR2 dependence-robust uncertainty. A two-cluster class is only a replication milestone: inferential SEs/CIs are withheld whenever the conservative cluster df (`m_dependence - 1`) is below 4. See `docs/ANALYSIS_DEPENDENCE_CONTRACT.md`.

## Current real strict-H1 corpus

The current real extraction contains four strict-H1 rows, all in the mutualist class. IWE015 mixed evidence remains on a quantitative hold pending raw Dryad variance verification, and the former IWE011 antagonist SMD was withdrawn on 2026-09-28 after the same independent-partner-window and exposure-unit rules were applied retrospectively.

Mutualists:
- `IWE029_LATE_VS_PEAK_NP_LOGOR` — *Stigmaphyllon paralias* × oil-collecting *Centris* bees; `log_odds_ratio = +1.55`.
- `IWE027_2007_HIS_M_VS_E_SEEDSET_SMD` — *Phyllodoce aleutica* × bumblebees; high-worker-bee M window versus low-visit E window; intact natural seed set; `standardized_mean_difference = +0.8518282660`.
- `IWE027_2007_GOS_M_VS_E_SEEDSET_SMD` — the same 2007 regional contrast at GOS; `standardized_mean_difference = +1.0038892388`.
- `IWE023_2015_W1_VS_W4_SEEDSET_SMD` — *Mertensia ciliata* × seasonal pollinator assemblage; experimentally shifted week 1 has >5× the contemporaneous visitation of week 4; final seed set; `standardized_mean_difference = +0.3815303645`.

Antagonists:
- no quantitative strict-H1 row currently admitted.
- The former IWE011 HA-versus-HD SMD is retained only as a diagnostic seasonal contrast: the source window is based on oviposition/egg observations rather than an independent adult-moth activity series, and one HA plot versus one HD plot cannot use plant n as replicated timing exposure.

Mixed pollinating seed predators:
- no quantitative strict-H1 row currently admitted.
- IWE015 (*Silene stellata × Hadena ectypa*) remains timing/final-outcome eligible but is withheld until `docs/IWE015_DRYAD_VARIANCE_AUDIT.md` is closed. Zhou et al. Figure 1 provides same-season 2012/2013 adult *H. ectypa* and co-pollinator moth density, so the future strict window is fixed as `direct_adult_census`; egg density is explicitly not used. Any raw-data return must go through `build_iwe015_promotion_packet.py` so effects, adjudications, window provenance and unit provenance are restored atomically.

The two IWE027 rows share one dependence cluster and IWE023 supplies a second independent mutualist SMD cluster. The two-cluster threshold remains a **replication milestone only**. H1 is not inferentially evaluable: the reference CR2 workflow requires at least 4 conservative cluster degrees of freedom (therefore at least 5 dependence clusters per class under the current intercept-only reference) before reporting inferential SEs/CIs.

Study/component admission is recorded in `data/registry/strict_h1_adjudications.csv`; screening inclusion alone does not authorize strict-H1 pooling. Every current real `strict_window` effect must also pass `data/registry/strict_window_provenance.csv`; CI rejects egg receipt, attack, infestation, damage and seed predation as substitutes for independent partner-window evidence. Every current strict effect must additionally pass `data/registry/strict_effect_unit_provenance.csv`, which records exposure grain, response grain, variance meaning and whether the claim is experimental or descriptive.

## Replication target

The current operational priority is **not** to add more effects from already represented programmes. IWE keeps **two independent `dependence_id` clusters per interaction class** as the discovery/replication milestone, but this is no longer an inferential gate. Reference inference is withheld until the conservative CR2 cluster df is at least 4.

Current SMD replication state:

- mutualist: **2 independent clusters — discovery milestone satisfied, not inferentially sufficient**;
- antagonist: **0 quantitative strict clusters after the IWE011 timing/unit re-audit**;
- mixed pollinating seed predator: **0 quantitative clusters while IWE015 is on variance hold**.

The machine-readable claim status reports both current cluster counts and remaining gaps. Search/extraction priority is frozen as:

1. restore IWE015 only after raw Dryad variance verification, while continuing the second independent mixed-programme search;
2. recover a first valid antagonist SMD cluster under the independent-partner-window and exposure-unit rules, then continue toward the two-cluster discovery milestone;
3. additional independent programmes in all classes after the two-cluster discovery milestone, because two clusters do not support robust inference.

Adding another year, site, or outcome inside an existing dependence cluster does not advance this replication target.

## Replication candidate readiness

The four-gate candidate ledger is `data/registry/replication_candidates.csv`. A candidate advances the discovery milestone only when all four conditions are satisfied: independent programme, independently measured timing window, post-predation final reproduction, and SMD-ready summary statistics. Reaching two clusters does not authorize H1 inference.

Current replication-search state is:

- mixed #2: **two P1 archival/completion routes, none ready, plus two P2 routes**. (1) Hurlburt 2004 (*Yucca glauca × Tegeticula yuccasella*) repeatedly counted adult moths in fresh flowers during 1999–2003, followed marked clones/inflorescences to fruit set and dissected mature fruit. The PhD is now located in the public University of Alberta Scholaris repository (DOI `10.7939/r3-fe1d-kj80`, primary file `NQ95948.pdf`); the next task is direct table/appendix audit rather than author contact. (2) Rentería & Cantú 2003 / Rentería 2000 thesis (*Yucca filifera × Tegeticula yuccasella*) directly measures the same-season adult moth window, individual-plant reproductive phenology and mature viable/damaged seeds, but the 500 mature fruits are not keyed back to flowering cohort/date. P2 conditional: Bopp & Gottsberger 2004 (*Silene × Hadena*) measures flowering and oviposition phenology, but the published “moth activity” series is reconstructed from newly deposited eggs in host flowers and therefore is not an independent partner-availability curve. Bopp 2003 Zoologica 152 (ISBN `978-3-510-55039-5`, 140 pp., 36 tables) is catalogue-confirmed and should be acquired by library/ILL; it can rescue the programme only if it contains both independent adult-moth activity and linked final plant reproduction. P2 prospective: the USGS 2022–2023 *Yucca jaegeriana × Tegeticula antithetica* project has the right design but no final citable unit-level source release. Sambucus is dropped after supplement audit because no quantitative partner-activity series is present;

A separate **P2 prospective** mixed route is the active USGS 2022–2023 *Yucca jaegeriana × Tegeticula antithetica* study: its design directly measures moth visitation, pod production and fertile seeds, but only preliminary poster/conference summaries are currently citable and no final unit-level dataset/publication has been recovered. It is tracked as `blocked_source_release`, not counted as evidence.
- antagonist strict-SMD recovery: **three P1 completion routes, none ready, plus four P2 leads**. New top route: Davies & Saccheri 2024, *Cardamine pratensis × Anthocharis cardamines*. Female butterfly flight is independently measured from capture/recapture, and public Dryad ramet trajectories run from first flowering to dehiscence with final intact reproductive units; the only missing timing object is the numeric female capture/recapture distribution underlying the source flight window. Before any contact route, IWE now explicitly targets the official Figure 4 PowerPoint and Davies 2019 Ecology Appendices S1–S3 for embedded/source-backed 2012–2014 female event or q10/q90 values; this runtime reaches those asset endpoints but cannot ingest their binary contents. Existing P1 routes remain Wen et al. 2024 *Parnassia* fate data and James 1998 yucca-cheater timing-stratified final seeds, alongside Cardamine as the top P1 route. *Astragalus–Tomares* is demoted to P2 after re-audit: the published synchrony series uses newly laid eggs rather than an independent adult-activity curve and the focal contrast is one patch versus one patch. Other P2 routes are *Cirsium–Rhinocyllus* same-unit data, Pilson 2000 wrong native effect form, and Eureka 2001 squarrose-knapweed cohort final-seed surface. The Eureka public route is now exhausted: weekly adult phenology and marked-head infestation are public, but cohort-level mature viable-seed means/variance are not; only archive recovery can unlock it. Cardamine is not yet extracted: Figure 4 will not be digitized and eggs will not define adult activity. The response-blind exposure is now frozen as three onset-timing groups—early refugium, core female flight, late refugium—and any future SMD keeps core-vs-early and core-vs-late as separate dependent effects;
- mutualist #2: **complete** via IWE023 (*Mertensia ciliata*). Four experimental flowering cohorts were ordered by same-season visitation; week 1 versus week 4 final seed set yields Hedges g = +0.3815303645 from published relative group means and the balanced ANOVA F(3,36), retaining residual df=36 in the standardizer correction, with no variance imputation. A non-promoting raw audit is now available for Dryad `10.7280/D19X0D` / file `gallagher&campbell_phenologyExperimentData.xlsx` (file ID `341732`); it requires the raw workbook to reproduce the published 4×10 design, relative means and F before generating a replacement candidate.

The next mixed and antagonist search targets must jointly provide contemporaneous partner activity, a prospectively orderable plant timing contrast, final realized plant reproduction, and SMD-compatible variance-bearing summaries.

No candidate is promoted by qualitative direction alone, and no SMD is reconstructed from a regression slope or model-derived fitness surface.


### Completion-route queue

`data/registry/replication_completion_routes.csv` turns the still-blocked P1/P2 programmes into an executable retrieval queue. A route records the exact unlock datum, access state, next action and a stop rule, so repeated generic searching cannot masquerade as progress.

Current order is:

- mixed: Hurlburt 2004 *Yucca* archival timing linkage → Rentería/Cantú *Yucca filifera* fruit provenance → Bopp 2003 conditional two-surface audit → USGS 2022–2023 *Yucca jaegeriana* source-release watch;
- antagonist: Cardamine–Anthocharis female capture/recapture dates → Wen 2024 *Parnassia* fate table → James 1998 yucca-cheater plant-level summaries → Jordano *Tomares–Astragalus* independent adult timing + replicated exposure rescue → *Cirsium–Rhinocyllus* same-unit programme data → 2001 Eureka squarrose-knapweed marked-head archive table.

`blocked_source_release` is explicitly allowed in this queue, but it remains prospective and contributes **zero** strict-H1 evidence until a citable final source exposes compatible timing and post-cost reproduction.



### Cardamine raw workbook normalization

Dryad publishes six Cardamine transect workbooks (early/late ecotypes × 2012–2014). `scripts/normalize_cardamine_workbooks.py` reads the documented XLSX format (metadata row 1, headers row 2) and produces:

- `plant_timing.csv` for the response-blind timing stage;
- `plant_summaries.csv` with source-backed `max_ru` and `final_intact_ru`;
- `raw_normalization_audit.csv` with every excluded plant and reason.

The normalizer is intentionally conservative: a final outcome is accepted only when a unique row marked `d` in the source Height column contains numeric buds, flowers and seed-pods. Missing dehiscence RU is never replaced with the previous visit.

### Cardamine preflight

The top antagonist P1 route has a response-blind executable preflight. Once source-backed 2012–2014 female *Anthocharis* event dates and source-normalized plant outcomes are available, run:

`python scripts/run_cardamine_preflight.py <plant_timing.csv> <adult_events.csv> <adult_provenance.json> <plant_summaries.csv> <output_dir>`

The command first validates an adult-timing provenance manifest, then writes the frozen three-level timing exposure, explicit outcome-missingness/SMD audit, eligible year × ecotype × direction Hedges-g rows, and a status JSON. Core female-flight onset is compared separately against early and late refugia; the two escape directions are never pooled. Real manifests must identify Dibbinsdale female capture/recapture records for exactly 2012–2014; older MRR seasons, male records, and egg dates fail closed. It **never** appends those rows to `data/extraction/direct_effects.csv`; promotion still requires source verification and strict-H1 adjudication.


### Cardamine promotion packet

When real, source-backed 2012–2014 female flight dates become available and the Cardamine preflight yields estimable strata, `scripts/build_cardamine_promotion_packet.py` can build a **non-mutating transactional draft**. It simulates the coordinated changes required to promote IWE032:

- append strict Cardamine effect rows;
- replace `ADJ_IWE032_PENDING` with exact eligible/strict-extracted adjudications;
- change the replication candidate to `ready`;
- remove Cardamine from the completion queue and renumber the remaining routes.

The virtual post-promotion state must pass the existing effect, adjudication, candidate and completion-route validators before any draft is emitted. The command never edits repository registries itself.

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
