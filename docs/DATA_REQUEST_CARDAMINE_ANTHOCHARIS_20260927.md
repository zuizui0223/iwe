# Minimal fallback data request — Cardamine × Anthocharis adult flight dates

Date: 2026-09-27  
Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024`  
Purpose: fallback only after the identified public Figure 4 PowerPoint and Davies 2019 Ecology supplements have been inspected and shown not to contain the required 2012–2014 female timing object

## Public-assets-before-request rule

Before using this request, inspect the official Wiley Figure 4 PowerPoint for DOI `10.1002/ece3.11330` and Davies (2019) Ecology supporting files `ecy2612-sup-0001-AppendixS1.pdf`, `ecy2612-sup-0002-AppendixS2.pdf`, and `ecy2612-sup-0003-AppendixS3.pdf`. Accept only embedded/source numerical 2012–2014 female capture+recapture events or exact year-specific q10/q90 flight-window values. Do not digitize graphical coordinates. If those public assets supply the timing object, this request is unnecessary.

## Scientific need

Davies & Saccheri (2024) state that the female *Anthocharis cardamines* flight season in Dibbinsdale Nature Reserve was determined from dates of capture and recapture of all females encountered during the focal study seasons.

The public Dryad archive already contains the longitudinal *Cardamine pratensis* plant trajectories for 2012–2014, but it does not contain those female capture/recapture dates.

IWE needs only the adult timing object required to define plant–antagonist synchrony independently of plant reproductive outcome.

## Minimal requested object

Preferred row-level format:

| field | meaning |
|---|---|
| `year` | 2012, 2013 or 2014 |
| `female_id` | individual mark ID if retained; optional if unavailable |
| `capture_doy` | day of year for first capture |
| `recapture_doy` | day of year for each recapture, one row per event or equivalent long format |

An event-level long table is equally acceptable:

`year, female_id, event_type, event_doy`

If row-level records cannot be shared, a source-backed year-specific numeric summary sufficient to reproduce the paper's female flight window is acceptable, for example the sample size and exact median / 25th / 75th / 10th / 90th percentile days shown in Figure 4.

## What is not requested

Do **not** request:

- plant final intact reproductive units;
- seed-pod survival;
- egg counts;
- larval counts;
- modelled fitness values;
- a precomputed synchrony effect.

Those quantities are either already public or are response/mechanism variables that must remain inaccessible while the exposure rule is being fixed.

## Planned use before response access

After receiving the adult timing object, IWE will:

1. verify that the dates correspond to the 2012–2014 Dibbinsdale seasons used in the 2024 paper;
2. define the adult female flight window separately for each year using a source-compatible rule;
3. reconstruct each plant's flowering interval from the already-public repeated `Flowers` observations;
4. apply the already-frozen three-level onset exposure (`early_refugium`, `core_flight`, `late_refugium`);
5. audit `core_vs_early` and `core_vs_late` separately against the already-frozen realized-reproduction outcome.

If the recovered dates do not provide adequate plants for either frozen direction-specific contrast, no SMD will be manufactured and no alternate cut-point will be introduced.

## Provenance to include in any reply/archive

Please retain, where available:

- collector / data-owner attribution;
- study year;
- site = Dibbinsdale Nature Reserve;
- confirmation that records are the capture + recapture data underlying the 2024 paper's female flight-period Figure 4;
- any sampling exclusions applied before the figure was produced.

## Request wording

A concise request should ask only for:

> the 2012–2014 female *Anthocharis cardamines* capture/recapture dates (or the exact year-specific numerical flight-period summaries underlying Figure 4) from the Dibbinsdale study reported in Davies & Saccheri (2024), DOI 10.1002/ece3.11330.

No biological conclusion depends on receiving the data; the candidate remains blocked until the source-backed timing object is available.
