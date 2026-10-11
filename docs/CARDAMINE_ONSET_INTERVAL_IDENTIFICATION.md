# Cardamine IWE032: first-observed flowering is interval-censored

Date: 2026-10-08. Status: **non-promoting response-blind onset
sensitivity**, not a source recovery and not a newly admitted effect.

## Why the first observation is not a point onset

Davies & Saccheri 2024, DOI 10.1002/ece3.11330, Methods §2.3,
state that monitored transects were revisited every **5–7 days**;
newly flowering plants were individually labelled at visits.
Their independently observed female flight curve was built from
2012–2014 capture **and recapture** dates (source Figure 4), which
are still unavailable in the repository as numeric year-specific events.

IWE's existing `first_flowering_dates` intentionally returns the
first date **with observed open flowers**. For a continuously monitored
unit with validated no-flower history, true onset lies between the
last verified nonflowering visit and first positive visit. For newly
labelled plants without that individual visit history, first positive
flowering is only an **upper bound**. Even a mean 5–7 day survey cadence
does not automatically establish a hard seven-day bound on that
individual's true onset, especially when flowering episodes might
occur unobserved between surveys.

## Partial-identification classifications

Let `u` be first observed positive-flower DOY; let `l` be an
independently verifiable lower bound (if any). The true onset lies
in `[l,u]` if `l` exists, or is left-censored `(?,u]`.
Let `a` and `b` be independent female flight q10/q90 DOYs.

- **Certifiable early:** `u < a`.
- **Certifiable core:** `l >= a` and `u <= b`.
- **Certifiable late:** `l > b`.
- Otherwise, preserve `boundary_sensitive` or
  `unresolved_left_censored` rather than claiming an exact class.

When no `l` exists, **only early refuge can be certified** from
`u` and the adult flight distribution alone. A new 7-day sensitivity
scenario explicitly substitutes `l_scenario=max(1,u-7)`; classifications
stable under this scenario are **conditional on the assumption**,
not provided-bound conditional. This scenario should be repeated with alternative
lags, and never be used to turn a missing bound into a fact.

This audit intentionally keeps observation-based timing groups used
in the frozen existing analysis **unchanged**. It adds a missing
identification check that must be resolved before a future Cardamine
promotion can be described as robust to onset observation error.
The calculation is independent of eggs, damage and intact RU.

## Executable non-promoting audit

`src/iwe/cardamine_onset_audit.py` exposes
`audit_cardamine_onset_intervals(plant_observations, adult_events,
source_lower_bounds=None, scenario_max_detection_lag_days=7)`.

Input `source_lower_bounds` is optional and must contain
`year,ecotype,plant_id,earliest_possible_doy,source_locator`.
A source locator is **necessary but not sufficient** provenance:
someone must inspect the original date-labelled record and rule
out earlier unobserved onset before treating a lower bound as valid.
No data-independent source locator can prove authenticity.

This function never appends effects, counts an antagonist strict-H1
cluster or admits a final-fitness prediction.

## What remains to be resolved

1. Recover numeric 2012–14 female capture/recapture dates or sufficient
   year-specific numeric window summaries; egg dates are inadmissible.
2. Use the source's raw plant visits to distinguish records with a
   genuine preceding non-flowering observation from newly tagged
   first-positive records. Preserve the unobserved-onset possibility.
3. Recompute core-vs-early and core-vs-late comparisons under
   source-identifiable groups and separately under prespecified
   observation-lag scenarios. Report all group losses and variance.
4. Do not promote a stable assumed-7-day result as a proven full
   onset date, and do not invent last-zero visits.

Source: https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.11330

## New SMD-level sensitivity (added 2026-10-08)

`src/iwe/cardamine_onset_sensitivity.py` now re-evaluates actual
within-year × ecotype `core_vs_early` and `core_vs_late` Hedges g
after **response-blind classification** under four alternative exposure
assignments:

- `observed_point`: the original **first observed** flowering day, not
  necessarily true onset;
- `provided_bound_conditional_only`: only groups robust to a separately
  source-located inclusive onset interval; an unlocated late/core
  plant is dropped even if its observed day lies late;
- `scenario_stable_only`: only groups invariant under an explicitly
  assumed maximum observation delay (0, 3, 5, 7, 10 and 14 days);
- `scenario_earliest_all`: assign **all** plants the earliest day
  permitted by that assumed delay. This is an adversarial
  coherent-shift scenario, not an estimate of true onset.

The direct timing, independent adult event records and outcomes are
required as separate inputs. The module freezes all classifications
without reading eggs, larval load or plant reproductive outcomes; only
then does it join intact reproductive-unit fractions to calculate
Hedges g and its working variance using the existing, unchanged
`cardamine_smd_audit`/`cardamine_smd_effects` contract.

`scripts/run_cardamine_preflight.py` additionally writes
`onset_effect_sensitivity.csv`, including timing-group exclusion
counts, estimability, g, and variance. An optional
`--source-onset-bounds FILE.csv` accepts individual `earliest_possible_doy`
and `source_locator` fields, but a locator by itself is **not**
authenticated original data; independent human source validation is
necessary. The status JSON accordingly records
`original_lower_bound_locators_human_verified_by_pipeline=false`.

**Interpretation stop rule:** a synthetic lag sensitivity, however
stable, does not establish actual onset-day accuracy or admit H1
effects. If the provided-bound conditional subset has fewer than two outcomes
per group or zero variance, report `eligible_smd=false`, not an
imputed or borrowed effect. A difference between observed-point and
assumed-earliest g is evidence of **analysis sensitivity under an
assumption**, not an observed population-level effect reversal.

Source public Dryad sheets are **six plant transect workbooks**, not a
numeric female flight-event dataset:
https://doi.org/10.5061/dryad.v9s4mw741.
The source README also records **half-day DOYs** for transects
surveyed across two successive days; do not round dates before the
timing audit. Female flight observations remain a distinct unrecovered
data object.

## Independent risk: source Figure 4's **relative Day 1** is not raw DOY

The published Davies & Saccheri (2024) Figure 4 caption defines **Day 1
separately in each year as the first observed early-ecotype flowering
date** at Dibbinsdale. This is a different temporal coordinate from
calendar day of year (DOY), including when both happen to be in
the numeric range 1–366. This distinction is independent of the
5–7-day observation-lag issue above.

A numerical figure value `figure_day1=30` cannot be compared with
`plant_doy=120` without a **source-backed, same-year calendar
anchor**. The conversion, if its inputs are independently
established, would be

`adult_calendar_doy = figure_relative_day + observed_first_early_calendar_doy - 1`,

using the study's Figure-4 Day-1 convention. No anchor is assumed, no
figure is digitized, and no adult values are recovered here.

For **real** IWE032 timing input, the provenance manifest must
explicitly declare:

- `adult_event_doy_basis=calendar_day_of_year`;
- `plant_observation_doy_basis=calendar_day_of_year`;
- `adult_calendar_origin_source_locator` locating the original
  date-stamped female capture/recapture records or a reviewed
  year-specific transformation;
- `figure_digitization_performed=false`.

These declarations are necessary but not sufficient: an entered
locator is **not automatically verified** by the validator. Actual
raw-source inspection is still required before evidence admission.
The validator also rejects DOY 366 in non-leap 2013 or 2014.

Real Cardamine input that instead supplies Figure-4-relative
numbers must fail closed, even if numeric ranges and other study
metadata pass. Synthetic test fixtures can omit these real-source
declarations but never authorize real H1 promotion.

Source: Davies & Saccheri (2024), Figure 4 caption,
https://doi.org/10.1002/ece3.11330.
