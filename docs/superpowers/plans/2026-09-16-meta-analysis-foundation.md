# IWE Meta-analysis Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first reproducible IWE release for hypothesis-testing meta-analysis of phenological synchrony effects across mutualist, antagonist, and mixed pollinating-seed-predator systems.

**Architecture:** A small Python package enforces registry and extraction contracts, separates direct phenology evidence from occurrence-derived proxies, standardizes effect direction, and builds a primary Tier-A analysis table. Statistical helpers provide transparent inverse-variance summaries and interaction-class contrasts without inventing a new meta-analytic method. Documentation freezes hypotheses, screening, effect-size rules, and claim ceilings before biological results are assembled.

**Tech Stack:** Python >=3.11, pandas, numpy, scipy, pytest, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-16-interaction-window-meta-analysis-design.md`

## Global Constraints

- IWE is an empirical meta-analysis project, not a theory repository.
- Primary interaction classes are exactly `mutualist`, `antagonist`, and `mixed_pollinating_seed_predator`.
- All primary effects are oriented so positive values mean greater synchrony is associated with higher plant reproductive performance.
- Tier C occurrence-derived potential overlap never enters the Tier-A primary meta-analysis.
- Missing effect variance is unresolved; it is not silently imputed.
- Repeated rows must retain explicit dependence identifiers.
- IWE does not estimate SCH/BALANCE/SLK/BITA/PAYOFF quantities.

---

### Task 1: Freeze project-facing contracts

**Files:**
- Modify: `README.md`
- Create: `docs/HYPOTHESES.md`
- Create: `docs/SEARCH_AND_SCREENING_PROTOCOL.md`
- Create: `docs/EFFECT_SIZE_CONTRACT.md`
- Create: `docs/CLAIM_CEILING.md`
- Create: `data/registry/systems.csv`
- Create: `data/registry/studies.csv`
- Create: `data/extraction/effect_template.csv`

**Interfaces:**
- Produces the canonical field names consumed by `iwe.schema` and `iwe.validation`.
- Produces a finite initial candidate-system registry without implying admission.

- [ ] Write documentation and CSV schemas matching the approved design.
- [ ] Verify every required field has an explicit definition and allowed values.
- [ ] Commit contract-only changes before implementation code.

### Task 2: Write contract tests first

**Files:**
- Create: `tests/test_schema.py`
- Create: `tests/test_overlap.py`
- Create: `tests/test_effects.py`
- Create: `tests/test_validation.py`
- Create: `tests/test_meta.py`
- Create: `pyproject.toml`

**Interfaces:**
- Tests require `validate_effect_rows`, `normalized_overlap`, `orient_effect`, `build_primary_dataset`, `fixed_effect_summary`, and `class_contrasts`.

- [ ] Add tests for accepted interaction classes and evidence tiers.
- [ ] Add tests that Tier C is excluded from primary data.
- [ ] Add tests for mismatch-to-synchrony sign reversal.
- [ ] Add tests for overlap bounds and deterministic interval overlap.
- [ ] Add tests for inverse-variance class summaries and contrasts.
- [ ] Commit failing tests before production implementation.

### Task 3: Implement validation and effect orientation

**Files:**
- Create: `src/iwe/__init__.py`
- Create: `src/iwe/schema.py`
- Create: `src/iwe/overlap.py`
- Create: `src/iwe/effects.py`
- Create: `src/iwe/validation.py`

**Interfaces:**
- `normalized_overlap(start_a, end_a, start_b, end_b) -> float`
- `orient_effect(value, exposure_direction) -> float`
- `validate_effect_rows(df) -> list[str]`
- `build_primary_dataset(df) -> pandas.DataFrame`

- [ ] Implement minimal behavior required by Task 2 tests.
- [ ] Reject unknown classes, tiers, duplicate primary IDs, missing dependence IDs, invalid variances, and unregistered effect families.
- [ ] Keep source rows immutable; derived orientation fields are explicit.
- [ ] Commit when tests are logically satisfied.

### Task 4: Implement transparent primary meta helpers

**Files:**
- Create: `src/iwe/meta.py`
- Create: `examples/synthetic_effects.csv`

**Interfaces:**
- `fixed_effect_summary(df, group_col="interaction_type") -> pandas.DataFrame`
- `class_contrasts(summary) -> pandas.DataFrame`

- [ ] Compute inverse-variance pooled estimate, standard error, normal 95% interval, Q statistic, and row count per class.
- [ ] Compute pairwise differences among the three preregistered interaction classes using independent-class variance approximation for the synthetic release.
- [ ] Label these as software/reference summaries, not the final publication model.
- [ ] Commit implementation and synthetic fixture.

### Task 5: Add executable workflow and CI

**Files:**
- Create: `scripts/validate_registry.py`
- Create: `scripts/validate_extraction.py`
- Create: `scripts/build_meta_dataset.py`
- Create: `scripts/run_primary_meta.py`
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Commands operate on repository-relative CSV paths and return nonzero on contract failure.
- Primary meta script exports class summaries and preregistered contrasts.

- [ ] Add command-line wrappers using only package functions.
- [ ] CI installs editable package and runs `pytest -q` plus validation of the synthetic fixture.
- [ ] Commit workflow.

### Task 6: Verify release boundary

**Files:**
- Modify: `README.md` only if verification exposes an ambiguity.

- [ ] Run/inspect CI for the feature branch or pull request.
- [ ] Confirm no Tier-C proxy can enter the primary dataset.
- [ ] Confirm no synthetic/example row is described as biological evidence.
- [ ] Confirm the repository contains no claim of support for H1-H3 before real extraction.
- [ ] Open a pull request with a bounded summary and next empirical task: systematic search + duplicate-independent extraction.
