# IWE031 host-stage sensitivity evidence

Date: 2026-10-02  
Study: Rasmussen & Yang 2023, *Asclepias fascicularis × Danaus plexippus*  
Article DOI: `10.1002/ecy.3854`  
Data DOI: `10.5061/dryad.69p8cz93c`  
Landscape role: experimental identification of time-dependent plant sensitivity to antagonist damage.

## Design

The experiment imposed monarch larval herbivory at three plant ages plus an undamaged control:

- early: monarchs added to 60-day-old plants on 11 May 2015;
- mid: monarchs added to 74-day-old plants;
- late: monarchs added to 88-day-old plants;
- none: no monarchs added.

This is not a reconstruction of the natural monarch activity window. It is a direct manipulation of **when the same antagonistic interaction occurs**.

## Reproductive result

The source reports qualitatively different timing effects across plant endpoints:

- early-season herbivory has the strongest effect on plant size;
- late-season herbivory has the strongest effect on production of viable seeds.

The fruiting figure defines the reproductive endpoint as the number of seeds germinated out of all seeds produced, used as a proxy for seed viability.

## Why it matters

IWE031 isolates a dimension that the original synchrony formulation did not represent:

> equal biological interaction types can have different fitness consequences solely because the host is at a different developmental stage.

Therefore an antagonist “interaction window” is not determined only by when the antagonist is available.

It also depends on the plant's **time-varying vulnerability or tolerance**.

Conceptually, the reproductive impact at time `t` should be treated as a function of at least:

`impact(t) = f(partner exposure(t), host sensitivity(t))`

without assuming that the function is multiplicative.

IWE031 primarily identifies the second term.

## Quantitative boundary

The Dryad archive publicly lists `HP_Seeds_Updated.csv` and the other source tables, but direct file retrieval in the present audit path returns HTTP 403. The accessible article/figure text establishes treatment timing and qualitative ordering, but does not expose the raw means and variances needed for a new effect-size row.

IWE031 is therefore registered as `experimental_timing_evidence`, not as a meta-analytic effect.
