# Gymnadenia factorial signed-selection anchor

Date: 2026-10-02  
Source: Sletvold, Moritz & Ågren 2015  
DOI: `10.1890/14-0119.1`  
Archive: Ecological Archives `E096-022-A1`  
Status: effect-size-ready signed-selection pilot source; outside the original IWE001–IWE032 screen.

## Why this source matters

The experiment factorially manipulated pollination and herbivory in one natural population of *Gymnadenia conopsea* and estimated phenotypic linear selection gradients on the same flowering-start coordinate and female-fitness scale in four independent treatment groups.

The source reports flowering start as day of year, so a more positive native gradient favors **later** flowering. IWE orients all selection-shift effects to a canonical axis where positive means a shift toward **earlier** flowering; therefore the native flowering-start contrasts are multiplied by -1.

## Source treatment gradients

Ecological Archives Table A2 reports:

| Treatment | Flowering-start beta ± SE |
|---|---:|
| C+H: open pollination + natural herbivory | -0.0042 ± 0.054 |
| C+E: open pollination + herbivore exclusion | +0.094 ± 0.031 |
| HP+H: supplemental hand pollination + natural herbivory | -0.160 ± 0.056 |
| HP+E: supplemental hand pollination + herbivore exclusion | -0.066 ± 0.028 |

The groups contain distinct plants, so linear contrasts of treatment-group estimates have variances equal to the sums of the relevant group variances.

## Agent-mediated contrasts

### Pollinator-mediated selection

Native definition: beta(open pollination) - beta(supplemented pollination).

- with herbivory: +0.1558, SE = 0.0777946;
- with herbivores excluded: +0.1600, SE = 0.0417732.

Because positive native flowering-start beta means later flowering, the canonical earlier-flowering effects are:

- -0.1558;
- -0.1600.

Pollinators therefore shift selection toward **later** flowering in this experiment.

### Herbivore-mediated selection

Native definition: beta(natural herbivory) - beta(herbivore exclusion).

- under open pollination: -0.0982, SE = 0.0622656;
- under supplemental pollination: -0.0940, SE = 0.0626099.

Canonical earlier-flowering effects are therefore:

- +0.0982;
- +0.0940.

Herbivores shift selection toward **earlier** flowering.

## Biological result

Pollinator and herbivore effects oppose one another on flowering phenology while being approximately additive. This produces little net directional selection on flowering time even though both ecological agents contribute non-zero selection.

That pattern is critical for IWE because it shows:

> weak net flowering-time selection does not imply weak interaction-mediated selection.

It also supplies a counterexample to a universal calendar-direction rule for antagonists. In IWE012 *Gentiana–Phengaris*, the antagonist shifts selection later; in *Gymnadenia*, herbivory shifts it earlier.

## Dependence and pooling

All four contrasts belong to one experimental programme and one dependence cluster, `DEP_GYMNADENIA_SLETVOLD2015`. They are not four independent replications.

Their covariance can be reconstructed from the four independent treatment-group beta estimates. Any future joint meta-analysis must retain that shared-cell covariance rather than treating the four contrast rows as independent.
