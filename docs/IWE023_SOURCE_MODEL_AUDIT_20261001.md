# IWE023 source-model audit — 2026-10-01

Study: Gallagher & Campbell, *Pollinator visitation rate and effectiveness vary with flowering phenology*  
Article DOI: `10.1002/ajb2.1439`  
Dissertation source: Gallagher (2017), Chapter 2  
Dryad DOI: `10.7280/D19X0D`  
Decision: **current IWE023 SMD reconstruction remains valid; add exact regression protection**

## Question

IWE023 reconstructs a common within-group SD from:

- four published relative experimental seed-set means: `[0.85, 1.00, 0.91, 0.69]`;
- `n=10` plants per phenology week;
- reported `F(3,36)=1.01`.

Because the dissertation contains several nearby ANOVAs, this audit asks whether `F(3,36)=1.01` is truly the four-week seed-set model required by the reconstruction.

## Response definition

The dissertation defines experimental plant seed set at the plant level as:

`number of mature seeds / number of flowers`.

For the phenology experiment, each plant contributes a per-plant mean seed-set response.

## Statistical model

The dissertation states that, for each response variable in the phenology manipulation, the first analysis tested the effect of **phenology week alone**.

Seed set and seed mass used per-plant means as responses in linear models, and their residuals were approximately normally distributed.

Thus the seed-set test is compatible with a one-factor four-group ANOVA decomposition.

## F-statistic provenance

The Results states:

- experimental plant seed set did not vary among phenology weeks;
- `F(3,36)=1.01, P=0.4`.

This is the statistic used by IWE.

A separate nearby value,

`F(3,36)=0.79, P=0.5`,

belongs to the **soil-moisture** check among phenology groups and is not used in the effect-size reconstruction.

## Relative group means

Dissertation Table 2.2 reports observed experimental seed-set values after dividing each weekly mean by the highest observed weekly mean:

| week | observed relative experimental seed set |
|---|---:|
| June 23 | 0.85 |
| June 30 | 1.00 |
| July 7 | 0.91 |
| July 14 | 0.69 |

These are exactly the four values currently used by IWE.

## Design/sample size

The public Dryad methodology and dissertation figure caption agree that:

- 10 plants were assigned to each phenology week;
- 40 plants flowered and entered the four-week experiment;
- Figure 2.4 experimental means are calculated from ten plants per week.

Therefore the source residual degrees of freedom are:

`40 - 4 = 36`.

## Consequence for the existing reconstruction

The current algebra is source-compatible:

1. recover `MS_between` from the four balanced group means;
2. use `F = MS_between / MS_within`;
3. recover the common within-group residual variance;
4. standardize week 1 minus week 4 using that common residual SD;
5. retain residual df=36 in the Hedges correction.

Current registered result remains:

- `g = +0.3815303645`;
- `var(g) = 0.1937181574`.

No quantitative hold is required.

## Raw-data route

The public Dryad workbook `gallagher&campbell_phenologyExperimentData.xlsx` remains the preferred provenance upgrade.

Automated direct download of Dryad file ID `341732` returns HTTP 403 both from the current runtime and from a GitHub Actions runner, so workbook bytes have not yet been inspected here.

The already-merged `scripts/audit_iwe023_raw.py` is non-promoting and requires the raw workbook to reproduce:

- weeks 1–4;
- n=10/week;
- residual df=36;
- the four relative means;
- `F≈1.01`.

## Regression protection

`tests/test_iwe023_raw.py` now includes an exact synthetic four-group dataset constructed to have:

- the four published relative means;
- n=10/week;
- the exact published `F=1.01`.

The test requires the raw-audit implementation to reproduce:

- `g=0.3815303645`;
- `var=0.1937181574`;
- residual df=36.

This prevents a future raw-audit refactor from silently changing the frozen IWE023 estimator.
