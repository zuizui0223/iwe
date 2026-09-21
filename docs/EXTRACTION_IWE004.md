# IWE004 extraction/adjudication receipt — Kehrberger & Holzschuh 2019

Source: Kehrberger S, Holzschuh A. 2019. *How does timing of flowering affect competition for pollinators, flower visitation and seed set in an early spring grassland plant?* Scientific Reports 9:15593. DOI `10.1038/s41598-019-51916-0`.

Archived data: Dryad DOI `10.5061/dryad.4b8gtht7t`.

Status: Tier-A direct timing–fitness evidence, but **not strict H1 synchrony evidence** under the current contract.

## Biological design

The study followed *Pulsatilla vulgaris* on eight grasslands and recorded intra-seasonal variation in:

- Julian date of bud opening;
- bee abundance;
- number of co-flowering plant species;
- flower visitation rate;
- flower longevity;
- pollinator-suitable hours;
- estimated total bee visits per flower;
- seed set under exclusion, open and hand pollination.

The focal timing predictor in the seed-set models is calendar/seasonal position (`Julian date of bud opening`), not a plant-minus-pollinator lag, absolute mismatch, or overlap index.

## Why Julian date is not strict synchrony

The animal environment changes non-monotonically in biological meaning over the season.

- bee abundance increased through the season;
- pollinator-suitable hours also increased;
- visitation to *P. vulgaris* decreased as co-flowering competitors accumulated;
- estimated total bee visits per flower marginally decreased because lower visitation and shorter floral longevity outweighed the later increase in bee abundance and suitable hours.

Thus “earlier” cannot be translated into “more synchronized with pollinators” or “later” into “less synchronized with pollinators”. The seasonal date combines pollinator abundance, interspecific competition and floral-longevity effects.

The paper itself reports that when estimated total bee visits and Julian date were entered together, Julian date had no additional explanatory power for seed set.

## Reproductive response

Open-pollinated seed set marginally decreased with later bud opening (`F[1,55] = 2.8, p = 0.098`), whereas hand-pollinated seed set did not vary with date (`F[1,56] = 0.6, p = 0.460`).

Seed set of open flowers increased with estimated total bee visits (`F[1,55] = 4.1, p = 0.047`).

These are biologically informative timing and pollination effects, but the reported date effect is not a direct synchrony coefficient.

## Executable adjudication

The registered component is:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = direct_timing_sensitivity`;
- `timing_domain = not_applicable`;
- strict-H1 status: `ineligible` for the Julian-date effect.

No IWE004 row is added to `data/extraction/direct_effects.csv` in this adjudication because the publication reports F statistics rather than the slope and sampling variance needed by the current extraction contract.

The Dryad dataset provides a transparent route for a later sensitivity-effect reconstruction. Such a row must remain `direct_timing_sensitivity`; recovering a precise slope does not convert calendar date into synchrony.

## Claim boundary

IWE004 supports the ecological chain

`seasonal position -> competition / visitation / floral longevity -> realized bee visits -> seed set`.

It does not support a strict claim that a monotonic increase in plant–pollinator temporal synchrony produced the observed seed-set pattern.
