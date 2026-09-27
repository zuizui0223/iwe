# Cardamine timing-only exposure freeze

Date: 2026-09-27  
Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024`  
Status: frozen before recovery of the missing 2012–2014 female capture/recapture dates and before any individual reproductive response analysis

## Purpose

This document freezes the response-blind timing exposure for the *Cardamine pratensis × Anthocharis cardamines* raw-data route.

The source describes **bidirectional phenological escape**: flowering can occur in an early refugium before the core female flight period or in a late refugium after it. Those two routes may differ biologically, so IWE does not collapse them into one generic "low synchrony" group.

No egg, larval, dehiscence, intact-RU, or other response/mechanism variable is read when timing groups are assigned.

## Source anchors

Davies & Saccheri (2024) state that:

- every focal ramet was followed from first flowering until dehiscence at 5–7 day intervals;
- newly flowering plants were individually labelled;
- female *A. cardamines* strongly favor newly flowering plants for oviposition;
- the female flight season was determined from dates of capture and recapture of all females encountered in Dibbinsdale Nature Reserve;
- the source flight-season boxplots show the median, 25th/75th percentiles, and 10th/90th percentile whiskers;
- the plant has access to phenological refugia on both sides of the butterfly flight period.

These points make **first flowering relative to the female flight distribution** the appropriate response-blind onset exposure. Egg receipt is not used as the exposure.

## Plant timing

For each `year × ecotype × plant_id`:

> `first_flowering_doy = minimum DOY with open flowers > 0`.

Pre-flowering observations do not count as flowering. Egg presence cannot make a plant flowering.

## Adult timing

For each focal year independently, use all source-backed female capture + recapture event DOYs.

Define:

- `adult_q10_doy` = empirical 10th percentile;
- `adult_q90_doy` = empirical 90th percentile.

Executable quantiles use linear interpolation (pandas default / R type 7). The q10–q90 boundaries are used because they reproduce the source's displayed central flight window without selecting a threshold from plant reproductive outcomes.

Earlier Dibbinsdale seasons, male records, pooled-sex summaries, and egg-laying dates are not admissible substitutes for the missing 2012–2014 female event dates.

## Frozen three-level exposure

Within each year:

- `early_refugium`: first flowering DOY < female q10;
- `core_flight`: female q10 <= first flowering DOY <= female q90;
- `late_refugium`: first flowering DOY > female q90.

Ecotype is retained and never pooled at this stage.

The three-level representation is deliberate. A plant beginning just before the female flight window and a plant beginning after it are both less exposed at onset than a core-flight plant, but they represent opposite directions of phenological escape and can differ in mechanism. IWE therefore preserves direction rather than treating both as one exchangeable category.

## Frozen SMD directions

If source-backed outcomes later permit SMDs, only these contrasts are allowed within each `year × ecotype` stratum:

1. `core_vs_early = core_flight - early_refugium`;
2. `core_vs_late = core_flight - late_refugium`.

Both are oriented as greater adult-flight synchrony/exposure minus a phenological refuge. Positive values mean greater synchrony is associated with greater plant reproductive performance; negative values mean greater synchrony is associated with lower performance.

The two refugia are never pooled into one denominator group. The two contrast rows share the same programme `dependence_id` and therefore do not create independent replication.

## What remains blocked

This timing freeze does not authorize an SMD.

After the female event dates are recovered, IWE must inspect the timing table **without response columns** and determine which year × ecotype × direction contrasts satisfy the predeclared minimum group-size rule. No contrast may be kept or discarded based on reproductive values, effect sign, effect magnitude, or p-value.

No alternate percentile, calendar cut-point, ecotype pooling, early/late pooling, or response-driven grouping may be introduced to rescue a sparse contrast.

## Executable implementation

`src/iwe/cardamine_timing.py` provides:

- `first_flowering_dates()`;
- `adult_flight_windows()`;
- `cardamine_timing_only_exposure()`.

The implementation reads timing columns only. Regression tests verify that response and egg columns cannot alter the timing assignments.

## Fail-closed conditions

The timing stage stops if:

- a plant year lacks a matching adult timing year;
- the adult timing object is not source-backed female 2012–2014 Dibbinsdale capture/recapture data (or an explicitly equivalent numeric source);
- the recovered data cannot reproduce a year-specific flight distribution without figure digitization;
- a planned core-vs-refugium contrast lacks enough plants before outcomes are inspected.

In those cases Cardamine remains blocked; no SMD is manufactured.
