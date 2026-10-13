# Caruso 2019 as a signed phenology-selection discovery universe

Date: 2026-10-02  
Article DOI: `10.1111/evo.13639`  
Dryad DOI: `10.5061/dryad.2v8c5g0`  
Status: discovery universe only; row-level workbook ingest remains access-blocked.

## What already exists

Caruso et al. compiled 755 directional selection-gradient records with associated SEs from 36 articles. Of these, 139 records are flowering-phenology records.

For the treatment-comparison analysis, the authors created 487 pairs of records that measured selection on the same trait through the same fitness component in different treatments. Table 2 reports **90 flowering-phenology treatment-pair studies**, of which **39** are supplemental-hand-pollination comparisons.

The database therefore contains a much larger potential signed phenology-selection universe than the current IWE pilot.

## Why this is not the same analysis

The published estimand intentionally discards direction:

`|beta_i - beta_j|`.

That answers how strongly an environmental manipulation changes selection. IWE's pivot asks a different question:

`delta_beta_agent = beta_agent_context - beta_reference_context`

with the sign preserved after trait-axis orientation.

A large absolute shift can be:

- toward earlier flowering;
- toward later flowering;
- a complete sign reversal;
- or a magnitude change without reversal.

Those cases are biologically different for interaction-window ecology.

## Acquisition state

Dryad publicly verifies two workbooks:

- `Exp_stud_NOTdup_Dryad.xls`;
- `Exp_stud_dup_Dryad.xlsx`.

The non-duplicated workbook is the required source-of-truth inventory. Existing audits in the broader project verified the manifest and database scope, but the current unauthenticated Dryad file-byte route returns an authorization error. No workbook rows are therefore counted as IWE evidence yet.

The duplicated workbook is dependence-audit material only and must never be counted as additional studies.

## Frozen rescreen before outcome inspection

Once the non-duplicated workbook is lawfully ingested:

1. retain flowering-phenology records only;
2. preserve source trait orientation before any sign conversion;
3. pair only same experiment × same trait × same fitness component contrasts;
4. classify manipulated factor as pollination, herbivory/seed predation, other biotic, or abiotic from the primary source rather than assuming every "other biotic" manipulation is antagonistic;
5. orient each contrast to the canonical earlier-flowering axis;
6. preserve article/experiment dependence;
7. do not construct contrast variances by assuming zero covariance when a treatment coefficient is shared across comparisons;
8. keep mixed and factorial multi-agent experiments as structured contrast sets rather than duplicated independent rows.

## Feasibility implication

Even before workbook ingest, the published architecture establishes that the signed-selection pivot is not a two-study curiosity: **90 flowering-phenology treatment pairs already exist in the source database**. The unresolved question is how many survive biological agent classification, orientation, dependence, and uncertainty gates.
