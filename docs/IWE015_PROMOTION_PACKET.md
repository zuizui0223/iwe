# IWE015 transactional re-admission packet

Date: 2026-10-01  
Study: `IWE015` — *Silene stellata × Hadena ectypa*  
Status: executable draft builder; never mutates evidence registries

## Purpose

IWE015 is currently biologically eligible but quantitatively held because the published Table 1 dispersion label is internally inconsistent.

A raw-data variance repair must not restore the effect rows by itself. Re-admission also needs to preserve the strict partner-window and effect-unit contracts introduced after the original extraction.

Therefore:

`scripts/build_iwe015_promotion_packet.py`

takes the two ready year-specific rows produced by `audit_iwe015_raw_variance.py` and constructs one validated virtual transaction.

## Source-backed timing basis

Zhou et al. (2020) Figure 1 contains separate 2012 and 2013 time series for:

- adult *H. ectypa* moth density;
- adult co-pollinating moth density;
- egg density.

Adult moth density is defined as number of moths observed per flower ×100.

The strict timing basis is therefore:

`window_basis = direct_adult_census`.

Egg density is not used to define partner availability.

Earlier Reynolds et al. 2005–2006 adult-density work is valuable system context but is not needed to back-project a historical window into 2012–2013.

## Unit semantics

The early and late field experiments use distinct plants.

A returning effect is registered as:

- design type: `observational_individual_timing`;
- exposure grain: plant;
- response grain: plant;
- variance: `individual_effect_sampling`;
- inference: `descriptive_association`;
- causal claim: no.

The seasonal period was not randomized, so the effect is not promoted as a causal timing manipulation.

## Required raw input

The builder requires exactly two raw effect rows:

- year 2012;
- year 2013.

For each year:

- `raw_effect_ready = true`;
- finite Hedges g;
- finite positive sampling variance;
- raw early and late n >=2.

These are expected to come from the four female Dryad CSVs after the raw audit has reproduced the published group n and rounded successful-fruit means.

## Atomic draft transaction

For both years the packet drafts:

1. a strict Tier-A effect row in `direct_effects.csv`;
2. replacement of the current pending adjudication with `eligible + strict_extracted`;
3. a strict-window provenance row using `direct_adult_census`;
4. a strict effect-unit provenance row using plant-level descriptive semantics.

The virtual combined state is then passed through:

- effect-row validation;
- strict adjudication validation;
- strict partner-window provenance validation;
- strict effect-unit provenance validation.

Any failure aborts packet construction.

## Outputs

The executable builder writes:

- `draft_direct_effects_append.csv`;
- `draft_strict_adjudications_replacement.csv`;
- `draft_window_provenance_append.csv`;
- `draft_unit_provenance_append.csv`;
- complete virtual post-promotion versions of all four registries;
- `promotion_manifest.json`.

The manifest explicitly records:

- `window_basis = direct_adult_census`;
- `egg_receipt_used_as_window = false`;
- `direct_repo_mutation_performed = false`;
- `transactional_validation_passed = true`.

## Boundary

This packet does not make raw data available and does not change the current evidence count.

IWE015 contributes zero strict rows until the raw variance audit succeeds and a source-audited promotion transaction is actually applied.
