# Lythrum simulated-herbivory selection shift

Date: 2026-10-02  
Source: Thomsen & Sargent 2017, *Evidence that a herbivore tolerance response affects selection on floral traits and inflorescence architecture in purple loosestrife*  
DOI: `10.1093/aob/mcx026`  
Status: effect-size-ready signed-selection source; simulated antagonist damage, not a natural partner-window study.

## Design

The split-plot experiment combined simulated meristem herbivory with pollen supplementation in *Lythrum salicaria*. The source measured direct linear selection on flowering start and reports treatment-specific gradients plus ANCOVA contrasts.

For flowering start:

- clipped/damage treatment: beta = -0.28 ± 0.06;
- control: beta = -0.03 ± 0.08;
- source damage-treatment × flowering-start contrast: delta beta = +0.25 ± 0.10, P = 0.05 under the source contrast coding.

The native trait is flowering-start Julian day, so negative beta favors earlier flowering.

## IWE orientation

IWE defines the ecological effect as:

beta(damage present) - beta(control)

which is:

-0.28 - (-0.03) = -0.25

on the native later-date coordinate.

The canonical IWE axis is positive = shift toward earlier flowering, so the oriented effect is:

+0.25, SE = 0.10.

## Pollinator interaction control

The same table reports:

- pollination treatment × flowering-start contrast = -0.07 ± 0.06;
- pollination × damage × flowering-start contrast = +0.01 ± 0.12.

The paper therefore finds no evidence that the damage treatment changes pollinator-mediated selection on flowering start. The direct damage-mediated shift is the supported result.

## Claim boundary

This experiment supports a causal effect of simulated herbivory/damage on the flowering-time selection surface. It does not identify the seasonal activity window of a natural herbivore and must not be used as a strict synchrony effect.

It is an independent signed-selection programme from Gymnadenia and Gentiana, with dependence ID `DEP_LYTHRUM_THOMSEN_SARGENT2017`.
