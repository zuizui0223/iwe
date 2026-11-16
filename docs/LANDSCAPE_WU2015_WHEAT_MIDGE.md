# Wu 2015 — strong stage-matched yield prediction, but no stage-free adult comparator

Date: 2026-10-07  
Study: Wu et al. 2015, winter wheat × *Sitodiplosis mosellana*  
DOI: `10.5846/stxb201308112060`  
Landscape role: high-provenance adult timing + susceptible-host-stage + final yield-loss evidence; not confirmatory for stage-specific superiority.

## Source design

The study independently monitored adult orange wheat blossom midge activity with yellow sticky traps through April–May.

A bagging experiment identified **ear emergence** as the susceptible host stage. More than 400 susceptible winter-wheat cultivars were then scored for:

- cultivar ear-emergence timing;
- overlap with the adult occurrence curve;
- final yield loss after larval feeding.

The stage-overlap metric is a niche-overlap index between the cultivar ear-emergence window and the adult occurrence distribution.

## Exact 2012 stage-overlap result

The original Figure 5 left/2012 panel prints:

- synchronization versus yield loss: **r = 0.935**;
- **p = 0.005**.

The panel can be identified as 2012 from the displayed ear-emergence class dates, matching the source's 2012 timing groups.

The text also reports:

- maximum synchronization = **0.628**, 23 cultivars, mean yield loss **78.1%**;
- minimum synchronization = **0.307**, 3 cultivars, mean yield loss **11.7%**.

For 2013:

- maximum synchronization = **0.783**, 3 cultivars, mean yield loss **2.42%**;
- minimum synchronization = **0.062**, 11 cultivars, mean yield loss **0.04%**.

## Why Figure 6 does not provide the confirmatory simpler comparator

The source also reports a significant positive relationship between yield loss and the cumulative number of adults caught **during each cultivar's ear-emergence stage**.

That predictor is not stage-free adult abundance.

It is already conditioned on the experimentally identified susceptible host window:

`adult abundance integrated over cultivar ear-emergence interval`.

Therefore Figure 5 and Figure 6 compare two **stage-informed** predictors:

1. normalized temporal overlap / synchronization;
2. adult abundance accumulated within the susceptible ear-emergence window.

Neither is a cultivar-varying adult-only timing/abundance predictor independent of host stage.

A season-total adult count is shared by all cultivars within a year and therefore cannot explain cultivar-to-cultivar yield-loss variation.

## Confirmatory consequence

Wu 2015 strongly supports:

`independent adult timing × susceptible host stage -> final yield loss`.

It does **not** supply the confirmatory comparison:

`simpler adult-only/calendar predictor vs stage-matched predictor -> final fitness`.

Recovering the per-cultivar table could improve quantitative reconstruction of the stage-matched relationship, but it cannot create the missing stage-free comparator without changing the source design.

Accordingly the phase-alignment registry should mark:

- paired simpler-vs-stage comparison = `no`, not `partial`;
- status remains `host_sensitivity_final`.

## Claim boundary

The exact r = 0.935, p = 0.005 is retained as source-backed evidence for the 2012 stage-overlap panel only.

No Figure 6 r value is reconstructed from cropped images, and no scatter points are digitized.

Source-backed values are stored in
`data/source_reconstructions/wu2015_wheat_midge_stage_metrics.csv`.
