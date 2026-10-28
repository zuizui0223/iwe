# Labouche 2013 — which parts of a defensive floral trait pathway are causal?

Source: Labouche & Bernasconi (2013), *Functional Ecology* 27:509–521.
DOI: [10.1111/1365-2435.12062](https://doi.org/10.1111/1365-2435.12062)
Scope: an **egg-placement causal control**; **not** a strict synchrony or mature-seed result.

## Three biological arrows, three identification standards

| Arrow | Source component | Judgment |
|---|---|---|
| Constrained corolla depth → natural oviposition location | Observational common garden, one measured infested flower per plant (N=71); egg-inside logit coefficient −4.69 ± 1.5 SE, P=0.003 | **Trait association only**. Corolla depth not manipulated. |
| Assigned egg location → successful attack and day-10 fruit development | Random inside 71 vs outside 66 plants, one flower each, 8 plant origins; attack 44 ± 8 vs 29 ± 4%; fruit development 83 ± 4 vs 97 ± 2%, all population mean ± SE | **Causal effect of egg location on early outcomes**. Not causal effect of egg presence or a timing shift. |
| Egg location and/or corolla depth → intact mature seeds | Original experiment ended at day 10, with no same-assignment mature intact-seed outcome | **Unidentified terminal fitness**. |

A model-fitted crossover at **19 mm** of constrained corolla tube is the
point where predicted natural egg placement outside exceeds 50%; it is
**not** an experimentally established host defence threshold. Likewise,
the egg-location association with fertilized ovules among 80 developed
infested fruits was non-significant (P=0.2); this is **not** a powered
equivalence test or proof that pollination costs are absent. The
egg-free 40-fruit subgroup's corolla depth versus fertilized-ovule
association was also non-significant (P=0.47).

## Counterfactual claim boundary

The randomized study compares **inside vs outside conditional on all
experimental flowers receiving an egg**. It cannot identify
`do(egg_absent)` or `do(corolla_extension)`. The observational study
suggests a trait-mediated physical constraint, but combining two
separately identified links by verbal transitivity is not proof of
total trait → final fitness mediation. In particular, genetic/family
background or correlated floral dimensions can affect oviposition
position, and host or moth traits can modify the probability of attack.

There is additional **post-treatment conditioning**:

- Only developed fruits enter the fruit-mass result (N=63 inside and
  N=59 outside); their means cannot give the marginal mass effect
  among all 137 assigned plants.
- Attack-success versus abortion is observational within randomized
  treatments, since attack is not assigned.
- Larval mass samples only 32 recovered living larvae, whose survival
  and extraction are downstream of position. Outside-heavier is not
  evidence of a causal reversal in marginal larval fitness.

The absence of final mature seeds and independently measured
adult–flower timing means this programme must remain absent from
strict H1 effect counts. It is an **independent causal positive control
for conversion geometry**, not an independent mixed timing/final
fitness cluster. Non-significance of other pathways cannot be used
to assert a zero effect.

## Falsifiable next step

A factorial experiment would manipulate **mechanical floral access**
(e.g., a validated corolla-access perturbation and sham) and
**egg position**, while monitoring pollinator deposition under natural
access, subsequent larval fate and **all originally tagged flower-to-
intact-mature-seed outcomes**. A second experiment could compare
random egg **presence** vs matched sham to disentangle egg effects.
Do not claim a precise physiological mediator without its manipulation.

All source statistics above are original-source summaries; no
plant-level data, binomial success counts or seed-fitness effects
are reconstructed. Source audit data:
`data/source_reconstructions/labouche2013_trait_position_service.csv`,
`labouche2013_randomized_egg_position.csv`,
`labouche2013_postattack_fruit_abortion.csv`, and
`labouche2013_conditional_larval_mass.csv`.
