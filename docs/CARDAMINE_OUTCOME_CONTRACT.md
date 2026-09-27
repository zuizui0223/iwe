# Cardamine outcome and SMD freeze

Date: 2026-09-27  
Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024`  
Status: frozen before recovery of the missing 2012–2014 female capture/recapture dates and before real individual-response analysis

## Purpose

The timing-only exposure is already frozen in `CARDAMINE_TIMING_ONLY_CONTRACT.md`.

This document separately freezes the plant response scale and the rule for converting an eventual timing-only exposure table into SMD rows. The separation is deliberate: no outcome quantity can alter the adult-flight window or synchrony classification.

## Source-compatible response

Davies & Saccheri (2024) define potential fecundity as the maximum number of reproductive units on a ramet:

`max_ru = max(buds + flowers + seed_pods)`.

They define realized reproduction from the reproductive units remaining intact at dehiscence and report `% intact = intact RU / max RU` in Table 1.

The 2016 Dibbinsdale thesis independently uses the percentage of reproductive units reaching maturity as a flowering-time reproductive-success measure.

The frozen primary raw response is therefore:

`realized_fraction = final_intact_ru / max_ru`.

This normalization is fixed before exposure recovery because flowering time and ecotype covary with plant size; using absolute final RU alone could mix potential fecundity with synchrony.

## Source normalization required before the outcome helper

For each year × ecotype × plant:

- `max_ru` must be reconstructed from the repeated source observations as the maximum of `buds + flowers + seed_pods`;
- `final_intact_ru` must be the source-backed number of reproductive units remaining intact at dehiscence;
- a value of zero is allowed only when the source record supports zero intact reproductive units, including explicit complete reproductive-tissue consumption;
- plants ending for an ambiguous, non-source-backed reason are missing/censored, not silently assigned zero;
- egg counts, larval counts, attack status and synchrony group may not be used to impute either outcome component.

Because the Dryad spreadsheets are currently not downloadable in this execution environment, the raw spreadsheet-to-`final_intact_ru` parser is not guessed here. It must be implemented only after the actual files can be inspected and their dehiscence/notes convention verified.

## Frozen stratum rule

After the missing female adult dates are recovered:

1. build the timing-only exposure table with the already frozen q10–q90 rule;
2. build the outcome table independently;
3. join only by `year, ecotype, plant_id`, retaining the full timing-exposure table so missing/censored outcomes are explicitly counted rather than silently dropped;
4. analyze every `year × ecotype` stratum in which both `higher_synchrony` and `lower_synchrony` have at least two source-backed outcomes and positive within-group SD;
5. do not pool early and late ecotypes before effect calculation;
6. do not retain or drop a stratum because of effect direction, effect magnitude, p-value or biological attractiveness.

The audit reports, by timing group, both the number of exposed plants and the number with source-backed outcomes. Missing/censored outcomes may reduce the analyzable sample but are never converted to zero and are never hidden by an inner join.

The minimum of two source-backed outcomes per group is the mathematical minimum for an independent-group sampling variance, not a fitted power threshold.

## Frozen effect

For every mathematically estimable year × ecotype stratum:

- native effect family: `standardized_mean_difference`;
- contrast: `higher_synchrony - lower_synchrony`;
- response: `realized_fraction`;
- estimator: the existing IWE independent-group Hedges g helper;
- orientation: positive means greater synchrony is associated with higher plant reproductive performance, matching the global IWE orientation.

For an antagonist system, a biologically expected harmful synchrony effect would therefore be negative, but no sign is required for admission.

All Cardamine effects share:

`DEP_CARDAMINE_DIBBINSDALE_2012_2014`.

Multiple years/ecotypes can add effect rows but never count as multiple independent programmes.

## What remains blocked

This outcome freeze does not make Cardamine ready.

The source-backed 2012–2014 female capture/recapture dates (or equivalent numeric flight-window summaries) are still absent. Until that timing object is recovered, no real synchrony group assignments or SMDs are calculated.

If exposure recovery produces no year × ecotype stratum satisfying the predeclared mathematical estimability rule, the candidate remains blocked. No percentile, ecotype pooling, calendar cut-point or response-driven regrouping may be introduced to rescue it.

## Executable implementation

`src/iwe/cardamine_outcome.py` provides:

- `cardamine_realized_fraction()`;
- `cardamine_smd_audit()`;
- `cardamine_smd_effects()`.

The module requires a source-normalized plant summary rather than guessing raw spreadsheet conventions. Tests use synthetic data only and verify:

- outcome calculation ignores eggs/timing extras;
- ecotypes remain separate;
- the contrast direction is higher minus lower synchrony;
- all estimable strata share one dependence cluster;
- an underpowered stratum is reported rather than rescued by selecting another cut-point.


## Preflight command

The frozen stages are composed by `src/iwe/cardamine_pipeline.py` and exposed through:

`python scripts/run_cardamine_preflight.py <plant_timing.csv> <adult_events.csv> <adult_provenance.json> <plant_summaries.csv> <output_dir>`

Before timing is calculated, `src/iwe/cardamine_provenance.py` validates that a real adult-timing manifest names the Cardamine candidate, Dibbinsdale Nature Reserve, female capture/recapture events, and exactly the 2012–2014 focal years. This prevents accidental substitution of older Dibbinsdale MRR seasons, male dates or egg dates.

Outputs are:

- `timing_exposure.csv`;
- `outcome_smd_audit.csv`;
- `smd_effects.csv`;
- `preflight_status.json`.

The preflight is deliberately non-promoting: it does not edit `data/extraction/direct_effects.csv`, strict-H1 adjudications, or claim status. Real rows require a separate source-verification/adjudication step after the missing adult timing object has been recovered.
