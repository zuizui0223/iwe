# IWE common-scale feasibility gate

Date: 2026-09-18

## Why this gate exists

IWE now has at least one strict quantitative programme represented in each preregistered interaction class on a Fisher-z-compatible sensitivity scale:

- mutualist — IWE001;
- antagonist — IWE068;
- mixed pollinating seed predator — IWE064.

This is **coverage, not replication**.

IWE001 contributes three population rows, but all share one dependence/programme ID. Counting those rows as independent studies would inflate evidence.

## Programme-count rules

The gate uses unique dependence_id, never row count.

These are project execution rules rather than universal statistical laws:

- at least **1 independent programme per class**: class coverage exists;
- at least **2 independent programmes per class**: a cross-class model may be fit for exploratory diagnostics, but not used for the primary H1 claim;
- at least **5 independent programmes per class**: the primary cross-class model is allowed to run.

Passing the 5-per-class gate does not itself establish adequate statistical power or validity. Model diagnostics, dependence structure, effect-family compatibility and prediction intervals remain required.

## Current status

data/extraction/common_scale_fisher_z.csv contains five rows but only three independent programmes:

- mutualist: 1 programme (DEP_IWE001_LONGTERM);
- antagonist: 1 programme (DEP_IWE068_IPOMOPSIS_HYLEMYA);
- mixed: 1 programme (DEP_IWE064_FICUS_CURTIPES).

Therefore the current status is **coverage_only**.

No cross-class p-value, ranking, or H1 moderator conclusion is permitted at this stage.

## What is allowed now

Allowed:

- report that a common Fisher-z representation is technically feasible for at least one programme in each class;
- display programme-specific point estimates and uncertainty;
- audit effect-scale reconstruction;
- use the evidence map to prioritize independent replication.

Not allowed:

- fit or interpret a three-class moderator test as confirmatory;
- treat IWE001's three dependent populations as three independent mutualist programmes;
- say one interaction class has a larger/smaller synchrony effect based on the current programme counts;
- treat current point estimates as class means.

## Priority created by the gate

The next value of information is **replication, not another effect from the same programme**.

Highest-priority targets remain:

1. IWE008 or another independent mutualist programme;
2. IWE035/IWE067 or another independent antagonist programme;
3. IWE059/IWE070 or another independent mixed programme.

The primary H1 analysis stays locked until the programme-count gate is satisfied.