# Althoff 2005 — mixed-system pollination-benefit window

Date: 2026-10-02  
Study: Althoff, Segraves & Pellmyr 2005, *Yucca filamentosa × Tegeticula cassandra*  
DOI: `10.1890/04-1454`  
Landscape role: independently measured partner-activity / pollination-benefit mechanism within a mixed pollinating seed predator.

## Design

Flowering *Yucca filamentosa* were surveyed in 2001 and 2002.

For each focal plant, the study measured:

- peak flowering date;
- plant morphology and flower number;
- yucca-moth pollinator abundance through the flowering period;
- florivore abundance;
- relative fruit set.

Because *T. cassandra* is both the obligate pollinator and a seed-consuming nursery pollinator, this is biologically a mixed interaction.

The study does not, however, carry relative fruit set through larval seed consumption to final viable-seed output. It therefore identifies the **benefit channel**, not net post-cost reproduction.

## Direct temporal result

In both years, peak pollinator abundance occurred significantly earlier than peak population flowering.

The source path analysis gives:

| Year | Path | Coefficient |
|---|---|---:|
| 2001 | peak flowering date → pollinator/day | **−0.37** |
| 2001 | pollinator/day → relative fruit set | **+0.60** |
| 2002 | peak flowering date → pollinator/day | **−0.27** |
| 2002 | pollinator/day → relative fruit set | **+0.48** |

All four paths are significant in the source figure.

Thus later-flowering plants received fewer pollinator moths, and plants with more pollinator moth activity achieved higher relative fruit set.

## Interpretation

This supplies an independently measured service-window mechanism in a mixed nursery-pollination system:

> movement away from the effective pollinator window reduces the plant's positive reproductive channel.

The result is replicated across two years within one programme.

It complements IWE014, where early and late *Silene vulgaris* had similar pollination success but different predation cost, and IWE015, where the same focal partner's early-vs-late dominance is linked to successful fruits but raw variance remains unresolved.

Together these systems support treating mixed interactions as separate temporal benefit and cost surfaces rather than one undifferentiated synchrony coefficient.

## Claim boundary

This component must **not** be promoted to strict mixed net fitness because:

- relative fruit set precedes the seed-consumption cost of *Tegeticula* larvae;
- final viable seeds after larval consumption are not the response used in the path model;
- other florivores also occur in the community.

Accordingly the component is registered as:

- `window_reference_class = independent_partner_activity`;
- `fitness_channel = benefit_channel`;
- `outcome_finality = not_final`;
- `landscape_status = mechanism_only`.

The source-backed coefficients are stored in
`data/source_reconstructions/althoff2005_yucca_benefit_paths.csv`.
