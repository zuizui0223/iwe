# Östergård 2007 — antagonists can exploit the host's own temporal filter

Date: 2026-10-02  
Study: *Lathyrus vernus × Bruchus atomarius*  
DOI: `10.1890/07-0346.1`  
Landscape role: independent final-fitness stage-structure evidence showing that host fruit-abortion filtering can be anticipated by the antagonist.

## Biological setup

There is a delay between beetle oviposition on young fruits and later seed consumption.

During that interval, *L. vernus* aborts many initiated fruits. Abortion is nonrandom:

- later fruits have a higher probability of abortion;
- fruits at more distal positions also abort more frequently.

In principle, this creates a host-stage filter that could delete predator eggs before they become seed-consuming larvae.

## The antagonist tracks future host retention

*Bruchus atomarius* does not oviposit randomly.

Females preferentially lay eggs on fruits with a **lower than average probability of abortion** and appear to use:

- fruit phenology;
- fruit position;
- at least one additional unidentified cue.

The source therefore shows that a pre-fitness host filter can itself become information used by the antagonist.

## Final-fitness consequence

The study explicitly compared the observed selective oviposition pattern with a simulated random-oviposition scenario.

Source values include:

- mean egg load on initiated fruits = **3.64 ± 4.14 SD**;
- expected developed beetles under random oviposition = **2.02 ± 0.11**;
- observed developed beetles under selective oviposition = **2.84 ± 0.14**.

At the plant level, the observed nonrandom oviposition pattern reduced average reproductive output relative to random oviposition, measured as intact seeds.

The paper's Figure 3 reports the proportion of plants whose intact-seed output increases or decreases under the observed selective pattern relative to the random scenario; the source conclusion is that the net effect is a **seed-predator offense**, not a defensive fruit-abortion strategy.

## Why this matters for the stage-specific IWE model

Cardamine shows that host development can filter raw exposure into a narrower effective future-cost window.

Lathyrus adds an important boundary condition:

> host-state filtering does not automatically protect the plant if the antagonist can detect which exposed units are likely to survive the filter.

Thus the effective cost window depends on both:

1. host filtering / future tissue retention; and
2. antagonist behaviour conditional on that future retention.

A more complete conceptual mapping is:

`effective cost = exposure × host filter × antagonist targeting response`.

This expression is bookkeeping, not a fitted multiplicative model.

## 21-year follow-up: timing covariance moves, selection does not follow

Valdés & Ehrlén 2021 subsequently analyzed 21 years of *L. vernus* phenology, seed predation and intact-seed fitness in the same study system.

The relationship between flowering time and seed predation varies strongly among years.

Spring temperature changes that relationship:

- March temperature × individual first flowering date on seed predation: **+0.174 ± 0.082 SE, p = 0.033**;
- April temperature × first flowering date: **−0.159 ± 0.067 SE, p = 0.017**.

The sign can therefore shift between years: some climatic combinations concentrate seed predation on earlier plants, others on later plants.

Seed predation itself strongly reduces intact-seed fitness.

Yet the among-year change in the phenology–seed-predation relationship does **not** explain among-year flowering-time selection:

- FFD × yearly covariance(FDD, seed predation): **−0.033**, 95% CI **−0.101 to +0.037**;
- FFD × yearly mean seed predation: **+0.003**, 95% CI **−0.072 to +0.078**.

This is a strong long-term boundary for the stage-specific model:

> a moving interaction window can change who is attacked without necessarily changing the net selection gradient on flowering time.

Final fitness integrates additional pathways, including direct phenology effects, resource state, pollination and other antagonists.

The long-term coefficients are stored in
`data/source_reconstructions/valdes2021_lathyrus_longterm_boundary.csv`.

## Claim boundary

Phenology is only one of several cues used by *B. atomarius*, and the study does not isolate a pure timing effect or manipulate the egg-to-seed developmental lag.

Accordingly this component is registered as `stage_structure_evidence`, not as a supporting timing-landscape programme.

It does, however, independently link a stage-dependent host filter to final intact-seed output and shows that the filter can be behaviourally circumvented by the antagonist.

Source-backed summary quantities are stored in
`data/source_reconstructions/ostergard2007_lathyrus_filter.csv`.
