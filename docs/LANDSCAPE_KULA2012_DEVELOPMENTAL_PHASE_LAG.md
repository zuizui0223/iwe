# Kula 2012 — developmental phase lag reverses the cost of synchrony

Date: 2026-10-02  
Programme: *Silene stellata × Hadena ectypa*, Mountain Lake Biological Station  
Source: Abigail A. Rogers Kula 2012 PhD dissertation, Chapter 3  
Repository: University of Maryland DRUM, handle `1903/12597`  
Landscape role: mixed-system mechanism showing that adult/oviposition synchrony and larval cost synchrony can have opposite geometry.

## Design

Chapter 3 followed individual *S. stellata* plants through the 2008 and 2009 flowering seasons.

The programme measured through each season:

- adult *H. ectypa* visitation;
- co-pollinator visitation;
- individual plant flowering;
- *H. ectypa* oviposition;
- larval density;
- initiated fruit set;
- flower and fruit predation.

New flowers on focal plants were marked repeatedly, allowing individual flowering distributions to be combined with the population oviposition curve.

The source synchrony score is:

`Synchrony_i = sum_t proportion_of_plant_i_flowers_open_t × eggs_per_flower_t`.

This is a realized oviposition-window metric, not an independent adult-availability score.

## The key result: the sign reverses between years

Synchrony had no detectable effect on initiated fruit set in either year:

- 2008: chi-square = 2.33, p = 0.1271;
- 2009: chi-square = 2.21, p = 0.137.

But synchrony strongly predicted flower/fruit predation in **opposite directions**:

- **2008:** higher synchrony -> higher predation, chi-square = **46.47**, p < 0.0001;
- **2009:** higher synchrony -> lower predation, chi-square = **16.74**, p < 0.0001.

Mean synchrony was about twice as high in 2009:

- 2008: 0.16 ± 0.01 SE;
- 2009: 0.32 ± 0.03 SE.

Mean predation was:

- 2008: 0.34 ± 0.03 SE;
- 2009: 0.46 ± 0.04 SE.

The reversal therefore cannot be summarized as a universal positive or negative effect of adult/oviposition synchrony.

## Developmental phase lag explains the reversal

Flowering and oviposition shifted by more than a week between years, but larval activity began and peaked at nearly the same calendar time.

Relative to first larval observation:

- in 2008, first flowering preceded larvae by **10 d** and first egg by only **5 d**;
- in 2009, first flowering preceded larvae by **17 d** and first egg by **15 d**.

Fruit development was also faster in 2009:

- 2008 mean maturation interval: **21.3 ± 0.28 d**;
- 2009: **16.7 ± 0.40 d**.

The dissertation's mechanistic interpretation is therefore temporal:

- in 2008, plants most synchronized with oviposition remained close to peak larval activity and suffered more predation;
- in 2009, highly synchronized plants had enough developmental lead for fruits to mature and harden before large larvae became abundant, so they suffered less predation.

The same adult/oviposition overlap can therefore map to opposite plant costs depending on the delay between interaction stages.

## General mechanism

For interactions with delayed consumer stages, the effective cost window is not the adult or oviposition window itself.

Conceptually:

`effective_cost_window = exposure_window ⊗ consumer_developmental_lag × host_vulnerability`.

The convolution symbol is bookkeeping, not a fitted kernel in this analysis.

This yields a more precise version of the landscape hypothesis:

> adult synchrony predicts benefit only through the adult service stage; offspring-mediated cost is shifted by development time and by how host tissue vulnerability changes before consumers begin feeding.

This mechanism connects the mixed Silene-Hadena result to the Cardamine-Anthocharis active-egg filter: in both systems, the realized damaging window is displaced from raw interaction timing by consumer development and host state.

## Relation to IWE015

The 2008-2009 Chapter 3 data belong to the same Mountain Lake *S. stellata-H. ectypa* research programme as later IWE015 work and therefore do **not** create an independent mixed dependence cluster.

They are nevertheless important for interpreting the opposite-sign 2012/2013 diagnostic IWE015 effects: interannual changes in developmental phase relations provide a source-backed mechanism by which greater focal-partner overlap can change sign in net reproductive consequences.

No cross-year causal identity is assumed; this is a mechanistic precedent, not a post hoc explanation of the later data.

## Claim boundary

This component is not a strict mixed net-fitness effect:

- synchrony is based on egg receipt/oviposition rather than independent adult activity;
- initiated fruit set is a benefit-channel intermediate;
- predation is a cost channel rather than final viable-seed production.

It is registered as `mechanism_only` and shares the Mountain Lake dependence cluster.

Source-backed values are stored in
`data/source_reconstructions/kula2012_silene_phase_lag.csv`.
