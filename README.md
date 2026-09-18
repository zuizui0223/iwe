# IWE — Interaction Window Ecology

IWE is a **hypothesis-testing meta-analysis project** on the reproductive consequences of phenological synchrony in plant–animal interactions.

## Primary question

> Does the fitness effect of phenological synchrony differ among mutualists, antagonists, and mixed pollinating seed predators?

IWE is empirical rather than theoretical. It synthesizes published effects, preserves study dependence, and separates direct interaction phenology from occurrence-derived potential overlap.

## Primary hypotheses

- **H1 — interaction-type moderation:** synchrony effects differ among `mutualist`, `antagonist`, and `mixed_pollinating_seed_predator` systems.
- **H2 — mixed-system curvature:** in mixed systems, greater synchrony need not monotonically improve plant reproductive performance.
- **H3 — redundancy buffering:** effective partner redundancy may reduce reproductive loss under mismatch. H3 is secondary.

All primary effect sizes are oriented so **positive = greater synchrony is associated with higher plant reproductive performance**.

## Evidence tiers

- **Tier A:** direct matched phenology–fitness evidence. Primary meta-analysis only.
- **Tier B:** direct phenology plus intermediate functional outcome. Mechanism/context only.
- **Tier C:** occurrence-derived potential overlap. Extension/screening only; never pooled into Tier A.

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


## Current empirical status

The present screened corpus has quantitative strict programmes closed for:

- mutualist: 2 independent programmes;
- antagonist: 1 independent programme;
- mixed pollinating seed predator: 1 independent programme.

On the current Fisher-z common scale, each class has one independent programme, so the primary cross-class H1 gate remains **`coverage_only`**. This is a replication/effect-scale limitation, not a software failure.

The current evidence architecture is generated with:

```bash
python scripts/build_evidence_architecture.py
```

See:

- `docs/EVIDENCE_ARCHITECTURE_CURRENT.md` — interpretation of the current measurement/evidence structure;
- `data/derived/evidence_architecture_current.csv` — machine-readable snapshot;
- `docs/COMMON_SCALE_FEASIBILITY_GATE.md` — independent-programme thresholds for cross-class inference;
- `docs/SOURCE_ELIGIBILITY.md` — source forms allowed into the confirmatory primary corpus.

## Project boundary

IWE does **not** estimate `L`, `R`, `K`, `Phi`, accessibility, invasion, fixation, occupancy, or BITA mechanism allocations. SCH/BALANCE/SLK/BITA/PAYOFF may later use IWE as external empirical context, but IWE stands as an independent meta-analysis.

## Repository layout

```text
docs/        hypotheses, screening, effect-size and claim contracts
data/        registries, extraction templates and derived tables
src/iwe/     validation, overlap, effect orientation and meta helpers
scripts/     executable validation and analysis entry points
examples/    synthetic software fixtures only
tests/       contract and regression tests
```

## First-release success criterion

The first release must validate registries and extracted effects, orient effects reproducibly, exclude Tier C from the primary dataset, produce interaction-class summaries/contrasts on synthetic fixtures, and emit no biological conclusion before real literature extraction.

See `docs/superpowers/specs/2026-09-16-interaction-window-meta-analysis-design.md` for the frozen design.