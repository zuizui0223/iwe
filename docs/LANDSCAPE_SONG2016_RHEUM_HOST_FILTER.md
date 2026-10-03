# Song 2016 — a pollinating seed consumer modifies the host filter before larval cost

Date: 2026-10-03  
Study: Song et al. 2016, *Rheum nobile × Bradysia* sp.  
DOI: `10.1038/srep29886`  
Landscape role: mixed-system mechanism showing that the partner can modify host developmental filtering after oviposition.

## Interaction structure

Female *Bradysia* pollinate *Rheum nobile* while feeding and ovipositing. A single egg is placed in an ovary, and the larva later consumes the only seed in the parasitized fruit.

Because eggs are laid well before seed development, fruit abortion is a potentially lethal host filter for the fly offspring.

## Oviposition changes the host filter

The study compares oviposited flowers/fruits with intact ones.

Fruit abortion is strongly lower after oviposition:

- oviposition effect on fruit abortion: **F = 287.24, p < 0.001**;
- oviposition × year: **F = 30.23, p < 0.001**.

This cannot be explained by extra pollination benefit from the oviposition act itself: stigmatic pollen loads do not differ between pollen-feeding-only visits and pollen-feeding-plus-oviposition visits.

## Physiological mechanism appears before larvae hatch

IAA concentration is much higher in oviposited flowers/fruits:

- oviposition: **F = 355.97, p < 0.001**;
- developmental day: **F = 681.54, p < 0.001**;
- oviposition × day: **F = 140.82, p < 0.001**.

The difference persists through early fruit development.

Crucially, larvae do not hatch until late August or early September, whereas the IAA series is sampled through mid-August. The source therefore argues that the early physiological change is associated with the oviposition event/female, not larval feeding.

Fruits containing fly larvae are also larger than unparasitized fruits.

## Flowering time does not explain the filter

Across the first eight days of flower opening within plants, the study finds no significant effect of flowering sequence on:

- fruit set: F = 1.61, p = 0.16;
- fruit abortion: F = 1.30, p = 0.27;
- oviposition: F = 1.35, p = 0.25.

Fruit-abortion and oviposition rates are not correlated across flowering sequence (r = -0.15, p = 0.23).

Thus the reduced abortion of oviposited fruits is not simply the result of females choosing an early/late flower class with intrinsically higher retention.

## General implication

Lathyrus-Bruchus and Rheum-Bradysia expose opposite feedbacks around the same developmental layer.

- In Lathyrus, the antagonist **predicts and avoids** the host abortion filter.
- In Rheum, the mixed pollinating seed consumer appears to **modify** the host filter, reducing abortion after oviposition.

The effective-cost mapping should therefore not assume host vulnerability/retention is an exogenous function of time.

Conceptually:

`host_filter(t) -> host_filter(t | interaction history)`.

A fuller bookkeeping model is:

`effective future cost = f(exposure, developmental lag, host state, partner-induced host modification, consumer targeting)`.

No particular algebraic form is fitted here.

## Claim boundary

This study does not estimate a partner-relative timing effect on final whole-plant seed production.

It is therefore registered as `mechanism_only`.

Its contribution is mechanistic: the biotic interaction can alter the very host filter that maps early exposure into later reproductive cost.

Source-backed quantities are stored in
`data/source_reconstructions/song2016_rheum_host_filter.csv`.
