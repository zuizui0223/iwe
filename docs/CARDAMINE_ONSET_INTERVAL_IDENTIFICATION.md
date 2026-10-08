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
not source-certified. This scenario should be repeated with alternative
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
