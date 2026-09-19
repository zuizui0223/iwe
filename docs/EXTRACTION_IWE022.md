# IWE022 extraction receipt — Trifolium barnebyi × spring bee community

Source: Handley JC, Tronstad LM. 2023. *Pollinators limit seed production in an early blooming rare plant: evidence of a mismatch between plant phenology and pollinator emergence*. Nordic Journal of Botany 2023:e03877. DOI `10.1111/njb.03877`.

Public data record: Dryad `10.5061/dryad.s4mw6m9bg`.

Status: **unresolved strict-H1 mutualist candidate; source design is promising but strict plant–partner matching requires a raw site/date join that has not yet been executed**.

Interaction class: `mutualist`.

Provisional dependence ID: `DEP_TRIFOLIUM_BARNEBYI`.

## Source eligibility

The biological study is a peer-reviewed journal article and satisfies `docs/SOURCE_ELIGIBILITY.md`.

The Dryad record lists the raw files:

- `2021TrifoliumBarnebyiBees.csv`;
- `2021TrifoliumBarnebyiSeedSet.csv`;
- `2021TrifoliumBarnebyiPollen.csv`;
- monitoring/climate data and a README.

## What the published source establishes

The experiment sampled seed set at three study areas and pollinators at the same study sites during the same 2019 flowering season.

The seed-set file is documented to contain, among other variables:

- treatment (`Bagged`, `HP`, `Open`);
- unique plant-cluster identifier;
- viable seeds and viable seeds per flower;
- `HPJulianDay`, the Julian day on which the hand-pollinated flowers in that cluster were pollinated;
- study area and sampling trip.

The bee file is documented to contain:

- taxonomic identity;
- trap deployment and retrieval dates/times;
- Julian day and sampling week;
- trap-hours and insect catch rate;
- site/location/replicate identifiers.

The source article reports that bee catch rate increased through the flowering season and that viable seed production was substantially higher in later-blooming plants.

The earlier open report associated with the same programme additionally reports:

- viable seeds per flower increased with Julian day (`t = 2.5, p = 0.017`);
- viable seeds per flower versus bee catch rate had `t = 0.86, p = 0.39`.

These are useful source anchors but are **not automatically IWE strict synchrony effects**.

## Why the published regressions are not entered directly

IWE does not equate:

- calendar/Julian date with plant–partner synchrony;
- bee abundance alone with temporal overlap;
- a seasonal trend in seed set with a mismatch effect.

A strict IWE022 effect requires the plant timing state and independently observed pollinator availability to be linked at compatible spatial and temporal grain before reproductive outcome is used.

The published `Julian day -> seed set` coefficient therefore remains seasonal-timing evidence.

The published `bee catch -> seed set` analysis is closer to the biological mechanism, but the article text alone does not expose enough row-level mapping to verify that each reproductive observation is paired prospectively with the appropriate site/date pollinator-availability state.

## Prospective raw-data adjudication rule

If the two Dryad tables are materialized, strict admission will be decided **before calculating the seed-set effect** using the following checks:

1. restrict final plant outcome to naturally pollinated `Open` flowerheads;
2. establish a plant-cluster flowering/timing anchor from source fields only (for example the cluster-level hand-pollination Julian day or sampling trip) without inspecting seed outcome;
3. aggregate bee activity independently by the finest compatible source site × sampling interval;
4. verify a documented mapping between each plant area/timing anchor and a contemporaneous pollinator activity interval;
5. require that partner availability prospectively orders the plant observations as more versus less matched, or supports a source-faithful continuous activity-at-flowering metric;
6. only then calculate a registered study-level effect and sampling variance.

If site/date compatibility is insufficient, IWE022 is adjudicated to `context_only`; calendar date will not be substituted for synchrony.

## Candidate quantitative route if compatibility is confirmed

The preferred common-scale route is a Fisher-z correlation across independent plant clusters:

`r = cor(partner_activity_at_plant_timing, open_treatment_viable_seeds_per_flower)`

followed by:

`z = atanh(r)`

and

`var(z) = 1 / (n - 3)`.

This route is valid only if the partner-activity score is derived entirely from bee timing/site information before the plant reproductive outcome is inspected.

Plant clusters remain the biological observational units. Multiple insects from one trap interval are not independent synchrony replicates.

## Current data-access audit

On 2026-09-19, the Dryad landing page and file metadata were accessible, but all tested public file-stream routes for the bee, seed-set and README files returned approximately 4.3 kB HTML anti-bot responses rather than CSV/text data, even after establishing a landing-page cookie session.

The workflow `.github/workflows/iwe022-dryad-audit.yml` explicitly rejects those HTML responses as raw data.

This is a data-access blocker, not evidence against strict eligibility.

## Claim ceiling

At present IWE022 supports:

> seed production and pollinator availability both change strongly across the same spring flowering season, and the archived source structure appears capable of testing a plant-timing × partner-availability relation if the row-level tables can be joined at compatible site/date grain.

It does not yet contribute an effect to `direct_effects.csv` or `common_scale_fisher_z.csv`.
