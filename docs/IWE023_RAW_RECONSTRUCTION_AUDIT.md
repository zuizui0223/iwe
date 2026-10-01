# IWE023 raw plant-level reconstruction audit

Date: 2026-10-01  
Study: Gallagher & Campbell (2020), *Pollinator visitation rate and effectiveness vary with flowering phenology*  
Article DOI: `10.1002/ajb2.1439`  
Dryad DOI: `10.7280/D19X0D`  
Public workbook: `gallagher&campbell_phenologyExperimentData.xlsx`  
Decision: **keep the current strict effect; add a non-promoting raw-data verification route**

## Why revisit IWE023

IWE023 is currently reconstructed from:

- four published relative seed-set means;
- balanced group size `n=10`;
- the source one-way ANOVA `F(3,36)=1.01`.

That reconstruction is algebraically valid, but the public Dryad deposit contains the plant-level phenology-experiment workbook. Direct raw verification can remove dependence on rounded group means and the rounded F statistic.

This is a verification exercise, not a new estimand.

## Frozen raw estimator

The raw audit preserves the existing estimator exactly.

For all four phenology weeks:

1. calculate plant-level seed set;
2. calculate the four raw group means;
3. reconstruct the one-way ANOVA residual sum of squares across **all four** weeks;
4. define `MS_within = SS_within / (N - 4)`;
5. use `sqrt(MS_within)` as the common standardizer;
6. calculate week 1 minus week 4 Hedges g;
7. retain the full ANOVA residual degrees of freedom for the Hedges correction and denominator-uncertainty term.

The audit does **not** switch to a separate two-group pooled SD, because that would silently change the current effect-size estimator.

## Dissertation model verification

The Gallagher (2017) dissertation was re-audited directly before this raw workflow was accepted.

The source defines experimental seed set per potted plant as:

`number of mature seeds / number of flowers`.

For the phenology manipulation, the dissertation states that seed set and seed mass were analyzed using the **per-plant mean** as responses in linear models with approximately normal residuals. For each response variable the first model tested the effect of phenology week alone.

The Results then reports, specifically for seed set of experimental plants:

`F(3,36) = 1.01, P = 0.4`.

Table 2.2 reports the corresponding observed experimental seed-set means after division by the maximum weekly mean:

`[0.85, 1.00, 0.91, 0.69]`.

Thus the current published-summary reconstruction uses the correct response, the correct four phenology groups, the correct residual degrees of freedom, and a one-factor model whose ANOVA identity is compatible with recovering the common within-group residual variance. The nearby `F(3,36)=0.79` value in the dissertation refers to **soil moisture**, not seed set, and is not used by IWE.

## Published acceptance checks

Before a raw candidate is marked ready, the workbook must reproduce all frozen published checks:

- four phenology groups;
- `n=10` plants per group;
- group means relative to the maximum approximately `[0.85, 1.00, 0.91, 0.69]`;
- one-way ANOVA `F ≈ 1.01`.

Default executable tolerances are:

- relative group mean: ±0.02;
- F statistic: ±0.03.

The tolerances accommodate printed rounding but are not effect-selection thresholds.

## Public archive status

Dryad publicly lists:

- `gallagher&campbell_phenologyExperimentData.xlsx` — 96.33 KB;
- `gallagher&campbell_nonSpatialData_phenologyExperiment.pdf`;
- the pollinator-effectiveness workbook and metadata file.

The Dryad landing page resolves the individual workbook file stream, but direct binary retrieval returns HTTP 403 both in the current execution environment and from a GitHub Actions Ubuntu runner (tested 2026-10-01 against file stream 341732). The public source therefore exists, but automated cloud retrieval is currently blocked; raw verification requires obtaining the workbook through an interactive browser/library download or another source-authorized route.

## Executable workflow

First inspect the workbook without interpreting response columns:

`python scripts/audit_iwe023_raw.py <workbook.xlsx> <output_dir> --inventory-only`

This writes:

- `workbook_inventory.csv` — sheet names, dimensions and exact column names.

Then run the raw audit with explicit source columns. If seed set is already a plant-level column:

`python scripts/audit_iwe023_raw.py <workbook.xlsx> <output_dir> --sheet <sheet> --week-col <week> --plant-col <plant> --seed-set-col <seed_set>`

If the workbook instead stores mature seeds and flower counts:

`python scripts/audit_iwe023_raw.py <workbook.xlsx> <output_dir> --sheet <sheet> --week-col <week> --plant-col <plant> --mature-seeds-col <seeds> --flowers-col <flowers>`

For non-numeric/non-orderable week labels, add:

`--week-order <week1>,<week2>,<week3>,<week4>`

## Outputs

The executable audit writes:

- `workbook_inventory.csv`;
- `week_summary.csv`;
- `anova_audit.csv`;
- `raw_effect_candidate.csv`;
- `audit_status.json`.

The command never edits the evidence registry.

## Promotion rule

If the raw workbook reproduces all frozen published checks, compare its exact raw-data g and variance against the current published-summary reconstruction.

A registry update is justified only as a **precision/provenance refresh** of the same effect ID:

`IWE023_2015_W1_VS_W4_SEEDSET_SMD`.

The effect ID, dependence ID, exposure definition, effect family and biological claim must not change.

If the raw workbook does not reproduce the frozen source checks, keep the current published reconstruction and audit the source-data mapping before any registry mutation.

## Unit semantics

The raw route does not alter the current strong unit alignment:

- experimental flowering-time assignment: plant;
- final seed-set response: plant;
- design type: `experimental_individual_timing`;
- inference scope: `experimental_manipulation`.

See `STRICT_EFFECT_UNIT_PROVENANCE_CONTRACT.md`.
