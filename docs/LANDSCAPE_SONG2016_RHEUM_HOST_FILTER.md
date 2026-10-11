# Song 2016 — Rheum oviposition, host retention and the choice–manipulation ambiguity

Date: 2026-10-08 (re-audited from the original Methods)
Study: Song et al. 2016, *Rheum nobile × Bradysia* sp.
DOI: 10.1038/srep29886
Evidence status: **source-observed stage association + pre-hatch auxin association**.
Not a causal experiment on fly oviposition, not experimentally verified
host manipulation, not an intact-seed fitness effect, not strict H1.

## Ecological result that really survives the source audit

Female *Bradysia* pollinate while feeding/ovipositing on *R. nobile*.
A fly egg is deposited in the only ovule/ovary; the developing larva
later consumes that fruit's one seed. Abortive young fruits remove
the fly's provisioning opportunity, so host fruit retention is a
biological conversion gate **for pollinator offspring**.

The source makes several observational comparisons:

- Flowers naturally **selected** for egg-laying had much lower fruit
  abortion than flowers not selected (Table 2: **F(1,24)=287.24, P<0.001**;
  oviposition × year **F(1,24)=30.23, P<0.001**).
- Early pre-hatch oviposited flowers/fruits had higher **IAA** than
  bagged, hand-pollinated, non-oviposited flowers/fruits (Table 4:
  oviposition group **F=355.97, P<0.001**, with six collection stages).
- Pollen deposition after pollen-feeding versus pollen-feeding-plus-
  oviposition visits did **not differ significantly** in a 40-flower
  comparison (t=0.76, df=38, P=0.45).
- With flower opening sequence, no significant trend was detected
  for abortion (**F(7,49)=1.30, P=0.27**) or oviposition
  (**F(7,49)=1.35, P=0.25**).

These findings show biological co-occurrence and early physiology.
They **do not** demonstrate `oviposition causes retention` or
`IAA causally mediates increased retention`. A non-significant
flower-date, position or morphological difference is not evidence
that female insects fail to detect unmeasured host-quality cues.

## The decisive source-design distinction

**There is a real randomised manipulation in this paper — but it
randomises pollination treatment, not moth oviposition.**

| Source component | Randomised? | Units and comparison | Identifiable result |
|---|---|---|---|
| 2013/2015 pollination experiment | **Yes**, pollen source/handling among heads within plants | 7 plants; open vs bagged self vs bagged outcross | No detected difference in fruit set/abortion under **pollen treatment**; cannot isolate an oviposition effect |
| 2013/2014 flower fate after visits | **No**, the flies naturally choose the flowers | 7 plants/year; 200 labelled flowers/plant followed to ripe fruit | Association of natural egg receipt with lower abortion; **not** a randomised manipulation |
| 2015 IAA comparison | **No**, egg status remains naturally selected | 5 plants; fly-oviposited flowers versus **bagged and hand-pollinated** no-fly flowers, six developmental stages | IAA group association; egg status, fly behaviour and bag/hand treatment are not isolated |
| 2015 flowering-sequence cohort | **No**, day measured rather than randomized | 8 plants; first eight opening days | Lack of detectable calendar-order trend does not rule out unmeasured flower quality |
| 2015 fruit-size comparison | **No**, larvae present/absent | 6 plants; ten fruits per class per plant | Fruit size is not **intact seeds remaining after larval feeding** |

The original Methods say the 2013/2014 comparison was undertaken
“to determine the **correlation** between fruit set, fruit abortion and
fly oviposition.” Its use of an ANOVA *oviposition factor* does not
convert natural female choice into an intervention. The study's
IAA experiment **also** used a different pollination/handling regime
for non-oviposited flowers, so no direct mediator effect is identified.

Source Methods: https://pmc.ncbi.nlm.nih.gov/articles/PMC4945934/
(Flower fate and fly oviposition; Concentration of IAA; Pollination
experiments; Results Tables 1–4).
Machine-readable component-level audit:
`data/source_reconstructions/song2016_rheum_causal_design_audit.csv`.

## Two mechanisms remain empirically compatible

**Selection:** a latent pre-oviposition flower condition (resource supply,
IAA or another cue) increases both the chance a female chooses a flower
and the probability the plant retains it.

`U_pre → egg_receipt` and `U_pre → fruit_retention/IAA`.

**Induced manipulation:** an egg-laying act, female secretion,
mechanical wounding or associated visitor behaviour changes local
auxin physiology and subsequent retention.

`egg_laying_intervention → IAA_change → fruit_retention`.

Either can produce the observed pairwise comparisons when egg receipt
is self-selected. The higher IAA before larval hatching makes direct
**larval-feeding induction** implausible during that early phase, but
does not rule out selection on pre-existing host physiology.
Likewise, observational similarity in sampled floral morphology,
flower timing and pollen loads does not block all unmeasured backdoors.

### Why even arbitrarily significant observations cannot solve this

This is a mathematical identification problem, not merely a small-
sample power problem. For **illustration only**, suppose an
unpublished, synthetic population had
`P(egg)=0.5`,
`P(retained|egg)=0.8`,
`P(retained|no egg)=0.4`.

The same joint 2×2 table is produced by either:

- **Causal model A:** randomize eggs with probability 0.5, then
  egg-bearing fruit retention is 0.8 versus 0.4 without eggs;
  the experimental average egg effect is **+0.4**.
- **Selection-only model B:** preexisting latent host viability
  `U=retained` has prevalence 0.6, female choice
  `P(egg|U=1)=2/3` and `P(egg|U=0)=1/4`;
  egg receipt has **zero causal effect** because `U`, not the egg,
  determines retention.

Both models give precisely the same observed probabilities:
`P(egg,retained)=0.40`,
`P(egg,aborted)=0.10`,
`P(no egg,retained)=0.20`,
`P(no egg,aborted)=0.30`.
A statistical test can make the observational association arbitrarily
precise without discriminating these mechanisms. **These probabilities
are synthetic, NOT values estimated for Rheum.** The numerical
counterexample is unit-tested in
`tests/test_host_retention_causal_gate.py`.

## Final fitness can be opposite from fruit retention

A plant can mature more fruits carrying fly offspring while losing
their **only seed** to larvae. Let:

- `q_E` be the probability an *egg-bearing* fertilised flower
  reaches ripe fruit;
- `q_N` be the probability a comparable **non-oviposited**
  fertilised flower reaches ripe fruit;
- `s_E` be the probability that a ripe fruit reached from an
  egg-bearing flower has its one seed consumed by the fly.

Then **if exchangeability were experimentally enforced**, intact seeds
per initial fertilised flower are `q_E × (1 − s_E)` versus `q_N`.
Higher fruit retention after oviposition (`q_E > q_N`) would improve
*net maternal intact-seed output* **only if**
`s_E < 1 − q_N/q_E`. That threshold is conceptual — **neither
the source's observed q values nor a source-recovered s_E are
identified as exchangeable treatment quantities**. Do not compute
a numerical fitness benefit from the abortion ANOVA.

This is also why treating the increased size of parasitised fruits
as a host benefit is particularly problematic: the developing larva
can consume the only potential seed inside.

## Historical benchmark: female choice versus manipulation was tested before 2016

Brody & Morita (2000), *Oecologia*, DOI
`10.1007/PL00008867`, directly framed this same mechanistic dilemma
for the non-pollinating seed predator *Hylemya* on
*Ipomopsis aggregata*. They experimentally **restricted female
choice** by enclosing females with flowers; oviposited flowers in
the no-choice treatment still had significantly higher fruit set
than bagged controls without caged flies. This is stronger
evidence against a **pure free-choice explanation** than the
natural egg-vs-no-egg *Rheum* comparison. However, the accessible
abstract does not prove the egg alone was randomized or distinguish
ovipositor puncture from caged-female contact and handling; it does
not expose later intact-seed output after larvae fed.

Therefore **"female choice or host manipulation" is an established
research question (at least since 2000), not IWE's new discovery**.
The actionable IWE extension is to couple independently identifiable
consumer choice and induced changes in host retention with
*post-consumer plant intact-seed fitness* and partner timing.
This study is a separately controlled benchmark and **not** another
strict H1 antagonist synchrony effect.

## Opposite egg-load pattern in another pollinating seed predator

Goto et al. 2010 (*Ecology Letters*, DOI
`10.1111/j.1461-0248.2009.01425.x`) documented
*Glochidion acuminatum–Epicephala* nursery pollination.
In that system, flower abortion **increased** with
moth egg load and with ovule damage. Their source-based
**random-abortion counterfactual model** estimated that
selective abortion increased plant seed output by **16%**;
female moth fitness could be reduced by as much as **62%**
when selecting pre-infested flowers.

This sharpens a biological boundary that does **not**
follow from flowering synchrony alone:

- In *Rheum*, one flower produces one ovule/seed and generally
  one Bradysia egg; the lower abortion among naturally
  egg-bearing flowers can benefit flies even if each surviving
  larva completely consumes its maternal plant seed.
- In *Glochidion*, multiple ovules and sometimes multiple eggs
  create scope for rejecting *egg-heavy* reproductive units,
  reducing future larval costs while retaining other fruits.
  The **16%** is compared with a *modelled* random-abortion
  baseline, not randomized plant abortion, and is not a
  common-effect estimate with Rheum.

**Testable mechanistic moderator:** Does the plant-side
retention response depend jointly on egg intensity **and**
how many viable offspring can still be saved by aborting a
unit? An observational egg-count×ovule-count interaction
would not identify induced plant discrimination without
blocking flower quality and family/resource dependence.
This must not be simplified into “all pollinating seed
predators manipulate hosts” or “all plants sanction high
egg loads.”

Pinned bibliographic source summary:
`data/source_reconstructions/goto2010_glochidion_abortions_costs.csv`.

## Exact experiment needed for causal separation

Within each randomly chosen plant and position/phenological block,
use independent reproductive units allocated before fly arrival to
matched interventions:

1. **Natural fertilisation standardised** by manual pollen delivery
   to all treatment flowers and sham netting/handling.
2. **Fly contact without eggs**, **sham ovipositor puncture** where
   feasible, and **confirmed single-egg oviposition** in assigned
   floral units, distinguishing physical wounding from the insect
   or its egg. The design requires an ethically and biologically
   credible technique to randomise/restrict successful oviposition;
   merely selecting naturally visited versus not visited flowers
   is inadequate.
3. **Auxin pathway perturbation and rescue** as independent
   manipulation, to distinguish an IAA effect from correlated IAA.
4. Tag all initial fertilised ovules and track **fruit loss,
   egg/larval survival and mature intact seeds**, not retained
   fruits alone. Analyse plant-level clustering, fruit position
   and time; do not elevate flowers to independent plants.

A differential change in abortion after *randomised* egg-associated
exposure would reject a pure selection-only explanation in that
experimental context. A true mediator claim additionally needs an
IAA-specific perturbation and control for any direct hormonal effect.

## Consequence for IWE

- **Preserve** Rheum as mixed `mechanism_only`: strong
  association of naturally observed oviposition with retention
  and with pre-hatch IAA.
- **Withdraw the stronger causal wording** “oviposition changes
  the filter” and “host manipulation has been shown” in secondary IWE
  descriptions. Both selection and modification remain live.
- **Do not infer** maternal fitness benefit from fruit retention
  when the larva may consume the only seed.
- **No** independently dated adult synchrony → final intact
  seed response and no new H1 mixed dependence cluster.

Source summary values are retained unchanged in
`data/source_reconstructions/song2016_rheum_host_filter.csv`.
