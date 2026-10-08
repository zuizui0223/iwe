# Labouche et al. (2013): randomized egg placement identifies part of the conversion filter

Date: 2026-10-08
System: *Silene latifolia × Hadena bicruris*
Source: Labouche & Bernasconi, *Functional Ecology* (2013),
DOI [10.1111/1365-2435.12062](https://doi.org/10.1111/1365-2435.12062).
Evidence: **randomized egg-placement to short-run attack and fruit-development
responses**, but not a manipulation of flowering or partner synchrony,
and not mature intact-seed fitness.

## A real randomization—not observational oviposition choice

The study randomized **137 female host plants**, one experimental
flower per plant, to a fertilized moth egg placed:

- **inside the corolla near the ovary**: N=71 plants;
- **outside on the petal**: N=66 plants.

Flowers were bagged to prevent naturally laid eggs. All were
hand-pollinated, and authors performed matching touch/wetting
control actions in both treatment groups. Egg donor (nine female
moths), host population and timing of manual placement were handled
under the source's allocation scheme. Thus **location** of one egg was
experimentally manipulated; egg presence was not a randomized
yes-versus-no contrast.

## Stage-specific outcomes after randomized placement

| Source-defined endpoint | Inside (reported mean ± SE) | Outside | Source P |
|---|---:|---:|---:|
| Successful larval attack/fruit entry (population means) | 44 ± 8% | 29 ± 4% | 0.033 |
| Initial fruit development at day 10 (population means) | 83 ± 4% | 97 ± 2% | 0.005 |
| Mass among *developed* fruits at day 10 | 511 ± 26 mg (N=63) | 576 ± 24 mg (N=59) | 0.047 |

The first two are intention-to-treat-group summaries at the **plant**
allocation grain. The percentages are reported as mean ± SE across
eight source populations; they are not exact integer
`44% × 71` or `83% × 71` success counts, and no
binomial plant-level table is inferred.

The third endpoint conditions on the fruit having developed
after egg placement. It is therefore a **selected post-treatment
subset** and cannot be equated to the total causal effect of
placement on plant fitness.

In the same study, **15/42 fruits with successful attack aborted**
versus **1/81 without successful attack** among day-10
developed fruits (P<0.0001). This large observational association
does **not** independently identify
`successful attack → plant abortion`: attack success is a
post-randomization outcome that depends on egg position, host state
and larval establishment. Conditioning on attack can induce selection
bias and cannot be interpreted as a second randomized comparison.

## A second reversal among selected survivors

Among **32 living larvae from successfully attacked, developing
fruits**, larval mass was higher when eggs had originally been
placed **outside** rather than inside the flower
(source **F(1,22)=5.62, P=0.03**). Larvae from fruit
classified as **aborted** were also heavier than those in
nonaborted developed fruits (**F(1,22)=7.91, P=0.01**).

This should not be flattened into a reversal of the causal
treatment effect: the egg-position randomization is real,
but this comparison includes *only the larvae still alive
and recovered after multiple post-treatment filters*.
The study does not report a complete independent seed/larval
fitness distribution for every initially assigned egg.
Neither P-value establishes that abortion benefits larval fitness
or that the larvae eventually survive after fruit separation.

However, the mere occurrence of living larvae in fruits
identified as aborted at the early day-10 collection warns
against an automatic rule that **host fruit abortion is
synonymous with immediate consumer death**. That rule
can be appropriate for immobile eggs in some Yucca stages
but must be separately verified for mobile Hadena larvae.

Source-preserved conditional analysis:
`data/source_reconstructions/labouche2013_conditional_larval_mass.csv`.
No numerical group means are digitized from Figure 6.

## What it resolves, versus the Rheum ambiguity

In Song et al. 2016 *Rheum nobile–Bradysia*, the strong natural
egg–fruit-retention and pre-hatch IAA associations do not
distinguish female site selection from egg-triggered physiology,
because no egg placement was randomized.

Labouche 2013 **does identify** a source-controlled effect of
**where the egg was placed** on early fruit development and attack.
It demonstrates that a pre-larval exposure geometry, independent of
adult encounter abundance, changes the chance that an observed
interaction reaches the damaging stage.

This is not a direct test of whether an egg's molecular secretion
causes auxin-mediated fruit retention in *Rheum*, nor a universal
answer to the female-choice-versus-host-manipulation question:
the plant/animal species, outcome and manipulated variable differ.
The egg-position treatment also differs in egg–tissue contact, so
the exact physiological path is not isolated.

## The crucial terminal fitness boundary

The authors measured day-10 fruit development, mass, attack
and larvae; they did **not** produce a complete
**post-larval intact mature-seed count per originally treated plant**
for this experiment. Hence the randomized difference in early fruit
development cannot be promoted as a final maternal benefit from
outside eggs. Larval survival is a separate, selected downstream
stage, and an aborted attacked fruit may spare a plant seed cost
while sacrificing the reproductive unit.

Nor does the treatment shift **adult moth phenology** relative to
host flowering: it shifts spatial egg placement. Therefore:

- **causal early-stage filter evidence: yes**;
- **causal time-of-oviposition / timing-overlap contrast: no**;
- **strict mixed-H1 SMD cluster: no**;
- **after-larval plant net fitness: not observed at the same unit**.

Machine-readable source numbers are in
`data/source_reconstructions/labouche2013_randomized_egg_position.csv`
and
`data/source_reconstructions/labouche2013_postattack_fruit_abortion.csv`.

## Why this matters for the new IWE hypothesis

It separates three processes previously grouped under generic
"host filtering":

1. **partner site choice**: females decide whether and where to lay eggs;
2. **plant/consumer geometry**: an experimentally shifted egg location
   changes pre-attack survival and early fruit development;
3. **maternal cost/benefit**: the intact mature seed consequences
   of those changed attack probabilities, still unidentified here.

When comparing phenotype or phase effects, use the relevant stage:
an early gate may be causally identified even if a final outcome
remains unknown. Extrapolating a randomized early stage to terminal
plant fitness without measuring it would repeat the same
evidence-linkage mistake that IWE's strict contract prohibits.
