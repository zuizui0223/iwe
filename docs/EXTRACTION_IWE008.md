# IWE008 extraction receipt — Qilian alpine plant–pollinator mismatch study

Source: Wang W, Du J, He Z, Miao C, Wu J, Ma D, Zhao P. 2024. *Pollinator peaking earlier than flowering is more detrimental to plant fecundity*. Science of the Total Environment 917:170458. DOI `10.1016/j.scitotenv.2024.170458`; PMID `38290677`; PII `S0048-9697(24)00595-3`.

Status: **strict-H1 design eligible; quantitative effect/variance unresolved**.

## Why this is a high-value strict study

The study was conducted in an alpine grassland community in the Qilian Mountains, China. It directly combines:

1. plant flowering-abundance phenology;
2. insect visitation monitoring;
3. identification of a key pollinator and its abundance peak;
4. the temporal difference between peak flowering and peak key-pollinator abundance;
5. individual-level seed-setting measurements.

Thus the exposure is a directly observed plant–partner timing relationship rather than a calendar-date proxy.

## Directional mismatch is part of the estimand

The source explicitly distinguishes two states:

- flower peak occurs earlier than key-pollinator peak;
- key-pollinator peak occurs earlier than flower peak.

The reported fitness impacts are asymmetric, with the `pollinator peaks earlier` state having the stronger negative association with seed setting. Flowering duration modifies this asymmetry, with shorter flowering duration associated with a larger difference between the two mismatch directions.

IWE therefore must preserve the sign/direction of the peak-time difference. This paper must **not** be reduced to `abs(peak difference)` before direction-specific effects have been extracted.

## Current recoverable evidence

Publicly accessible bibliographic/abstract/discussion material confirms:

- direct plant and pollinator phenology monitoring;
- individual-level seed-setting comparison;
- explicit directional mismatch classification;
- a stronger plant-fecundity impact when the pollinator peak precedes the flower peak;
- flowering duration as a modifier.

The currently accessible sources do not expose the species-level or group-level coefficient/correlation together with a sampling variance/covariance structure adequate for entry into `direct_effects.csv`.

No effect size is therefore reconstructed from the abstract, significance statements, figure descriptions, or qualitative direction.

## Required quantitative recovery

Before IWE008 enters strict H1, recover one of the following from article tables/supplement/raw data:

- species-level seed-setting coefficient versus signed peak-time difference and its SE/variance;
- correlation plus sample size within a declared mismatch direction;
- individual-level data sufficient to reconstruct the registered model;
- model coefficient/covariance for a directional interaction, preserving species/site dependence.

If multiple plant species contribute effects, they must share study/site dependence identifiers rather than being counted as independent publications.

## Dependence and unit warning

The paper is a community study. Even if many plant species become extractable, they share site, sampling year, observer protocol and pollinator community. Species-level rows therefore require a common higher-level dependence identifier.

## Claim ceiling

At the present stage IWE008 supports only:

> the source design directly links signed plant–key-pollinator peak mismatch to individual-level plant fecundity and reports asymmetric effects of mismatch direction.

It does not yet supply a quantitative IWE meta-analysis row.

## Data-recovery status

As of 2026-09-17:

- ScienceDirect bibliographic/full-page retrieval is partially blocked by publisher access controls;
- PubMed and indexed article pages confirm DOI, PII, authors and design;
- targeted searches using DOI, PII, title, `supplementary`, `mmc`, and `data` did not recover a public supplementary dataset or repository containing the needed quantitative effects;
- a 2025 EGU abstract by Jun Du repeats the same central result but does not add extractable effect/variance information.

The study remains `unresolved` quantitatively rather than being excluded.
