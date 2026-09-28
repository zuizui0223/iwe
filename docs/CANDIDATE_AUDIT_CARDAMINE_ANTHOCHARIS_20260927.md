# Candidate audit — Cardamine pratensis × Anthocharis cardamines

Date: 2026-09-27  
Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024`  
Primary source: Davies & Saccheri (2024), *Ecology and Evolution*, DOI `10.1002/ece3.11330`  
Public plant data: Dryad DOI `10.5061/dryad.v9s4mw741`  
Decision: **promote to P1 `blocked_timing_linkage`**

## Why this candidate is unusually strong

Most antagonist near-misses fail because the animal window is inferred from eggs/damage or because final plant reproduction is reported on a different biological surface.

This programme contains both of the difficult measurements independently.

### 1. Independent antagonist flight window

The source states that the flight season of female *Anthocharis cardamines* was determined from the dates of capture and recapture of all females encountered in Dibbinsdale Nature Reserve.

This is a direct adult-activity measurement. It is not reconstructed from eggs on plants, larval damage, infestation or seed loss.

The paper uses those capture + recapture dates to display the seasonal female flight window in Figure 4.

### 2. Longitudinal plant phenology and final reproduction

Every focal *Cardamine pratensis* ramet on the transects was kept under observation from first flowering until dehiscence and revisited every 5–7 days.

At each visit the study recorded:

- day of year;
- open flowers;
- buds;
- seed-pods;
- newly laid and older eggs;
- first- through fifth-instar larvae;
- plant state/notes, including dehiscence.

The Dryad archive contains six spreadsheets covering early and late ecotypes in 2012–2014 with these repeated plant-level records.

The paper defines potential fecundity as the maximum number of reproductive units

`buds + flowers + seed-pods`

and evaluates realized reproduction using the number of reproductive units remaining intact at dehiscence. Final-instar larvae frequently consume most or all reproductive tissue; the source reports an average reduction in realized fecundity of about 70% for infested plants.

Thus final intact reproductive units are a source-defined post-antagonist reproductive outcome rather than an intermediate damage measure.

## Why no SMD is extracted yet

The plant Dryad archive does **not** include the female butterfly capture/recapture table used to construct the adult flight window.

The paper shows the flight distribution graphically, but IWE will not digitize Figure 4 to manufacture the missing numeric exposure.

Egg-laying dates in the plant spreadsheets also cannot replace the missing adult window. Egg receipt is a realized interaction outcome that depends on plant availability and oviposition choice; the frozen timing contract explicitly forbids recycling it as independent partner availability.

Therefore the biological timing gate is source-confirmed, but the exact numerical timing linkage is not yet executable from the public archive.

## Exact unlock condition

Recover either:

1. the 2012–2014 female *A. cardamines* capture/recapture date list used by the source; or
2. a source-backed numeric table defining the female flight interval/distribution for each study year.

The useful minimal object is:

`year, female_id_or_capture_record, capture_or_recapture_DOY`

An equivalent year-specific numeric flight-window summary is acceptable if it preserves enough information to apply a predeclared overlap rule without figure digitization.

## Pre-analysis firewall

Recovery of the adult dates does **not** automatically authorize an SMD.

Before inspecting final intact-RU response distributions, IWE must commit a source-specific raw-data contrast rule using timing information only.

That rule may use:

- the source-backed female adult flight window; and
- plant flowering intervals reconstructed from repeated open-flower observations.

It may not use:

- egg counts;
- larval occurrence;
- intact-RU values;
- seed-pod survival;
- response-driven quantiles or cut-points.

The exposure grouping must therefore exist before final reproduction is consulted.

If the recovered source-backed female dates fail to populate either frozen core-vs-refugium contrast adequately, the candidate remains outside the SMD target. No alternate binning or pooling is introduced after response inspection.

## Outcome guardrail

The paper's Table 1 compares larval-grazed versus ungrazed plants. That comparison quantifies the cost of larval attack; it is **not** the synchrony effect and cannot be used as the antagonist replication SMD.

The candidate must instead compare plants ordered by independently measured plant–adult-flight synchrony, with final intact reproductive units as the response.

Potential fecundity varies with plant phenotype and flowering time, so any eventual raw-data extraction must also preserve the source-defined biological unit and avoid turning plant size differences into a synchrony effect. A proportion or other source-compatible normalization may be considered only under a separately frozen extraction rule; it is not decided in this audit.

## Current gate state

| gate | status |
|---|---|
| independent programme | yes |
| independently measured antagonist activity | yes |
| longitudinal plant timing | yes |
| final post-antagonist reproduction | yes |
| raw plant response data public | yes |
| numeric adult flight dates public/recovered | **no** |
| frozen SMD contrast executable | **yes, pending the missing female date object** |
| candidate status | **P1 blocked_timing_linkage** |

## Why this route ranks first

The other antagonist P1 routes require unreleased fate data, unpublished plant-level summaries or correct-unit historical variance.

Here, the plant trajectories and final response are already public. The missing object is narrowly limited to the adult capture/recapture dates that the paper explicitly used.

This makes `ANT002_CARDAMINE_ANTHOCHARIS_2024` the highest-value current completion target, without changing the strict timing or SMD contracts.


## Public retrieval closure — 2026-09-27

A second retrieval pass did not recover the focal 2012–2014 adult-date table.

Audited public routes now include:

- the 2024 article and its publisher supplementary files;
- Dryad `10.5061/dryad.v9s4mw741`, which lists only six plant-transect spreadsheets plus README;
- indexed Dibbinsdale *A. cardamines* publications;
- the 2016 University of Liverpool PhD thesis/programme route.

The older Dibbinsdale mark–release–recapture study documents daily fieldwork and female/male emergence schedules for **2005–2010**. Those dates cannot be substituted for the focal 2012–2014 seasons.

No source-backed 2012–2014 female capture/recapture date list or numeric year-specific flight-window table was recovered publicly.

Generic public search is exhausted, but two **identified public binary-asset routes remain uninspected** because of this execution environment: the official Wiley Figure 4 PowerPoint for the 2024 paper and Davies (2019) Ecology Appendices S1–S3. These must be checked first for embedded/source-backed 2012–2014 female capture+recapture dates or exact q10/q90 values. The 2016 Liverpool MRR/POPAN timing series is 2005–2010 and cannot substitute. If the identified public assets do not contain the timing object, the remaining route is a narrowly scoped archive/contact request. The exposure and outcome rules are already frozen, so any recovered source-backed timing object can go directly to the non-promoting preflight.
