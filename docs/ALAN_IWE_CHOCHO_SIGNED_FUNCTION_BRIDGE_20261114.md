# ALAN × IWE × chocho: a signed interaction-window bridge

Source-locked exploratory cross-project audit, 2026-11-14. The aim is to
separate **artificial night light as a disturbance of interaction
opportunity** from the more ambitious (unproven) proposition that ALAN
causes seasonal mismatch, altered host use and final plant fitness
across islands and mainlands.

## Scientific relationship

- IWE asks whether independently documented seasonal flowering–
  animal availability overlap predicts **final plant reproductive
  consequences** across mutualist, antagonist and mixed systems.
  Its strict Tier-A/strict-H1 standard requires genuinely independent
  partner activity windows, correct within-programme units, final
  reproduction and compatible variance. Neither artificial-light
  treatment versus dark nor nocturnal versus diurnal visitation alone
  satisfies this specific synchrony contrast.
- chocho's frozen GEB result reconstructs **potential geographic
  availability of butterfly larval host plants** while holding known
  host taxon identities fixed. That does not establish actual local
  host phenophase, egg deposition, larval success, butterfly occupancy
  or any night-light exposure.
- ALAN studies show that light (intensity, spectrum, timing and spatial
  context) can perturb animal activity and plant flowering and can
  have opposing effects on distinct interaction services. Satellite
  VIIRS radiance is not ground-measured lux/spectrum or a manipulated
  light treatment.

A proposed future interaction-level conceptual sequence is:
ALAN light and spectrum × baseline guild/life stage →
changed diel activity / seasonal activity / flowering availability
→ measured pollen delivery and oviposition or damage
→ final viable seed output, moderated by breeding assurance and
reproductive compensation. The chain requires SAME site, flower,
animal, date/clock time and correct study dependence; none of the
global photo/host envelopes currently supplies that joint population.

## Two authentic source-backed experimental programmes — no pooled meta

### Experiment 1. Tibetan 2024 field, Lu et al. 2026

Primary article DOI: https://doi.org/10.1002/ece3.74368.
ALAN draft PR #65: https://github.com/zuizui0223/alan/pull/65
Original row-level Europe PMC supplementary workbook:
SHA256 ba7e15e66986f64943a38fd294e49d7128cf7719d318578f6b805d29cde8f98f.
Frozen ALAN source commit 7c065318e9476ea92541df1d89c36c54edb8d268.
Its original-source replay Actions #43567618252 succeeded.

All-survey ORIGINAL visitation worksheet, nocturnal visit-event counts:

| Outcome | Dark | Lit |
| --- | ---: | ---: |
| All-night total visits | 1,312 | 848 |
| Lepidoptera, mainly moths | 838 | 357 |
| Diptera | 54 | 151 |

These 400 original day/night survey records are within ONE original
experiment and FIVE true field blocks, not hundreds of independent
light manipulations. Other insect groups also occur. The original
400-row total-vs-guild conservation audit flags some rows; never
reallocate missing order visits to make totals equal.

The partial Diptera visit increase is 97 events versus 481 lost
Lepidoptera visits, a count-replacement ratio of 97/481 = 20.17%.
For the TWO groups ONLY, a hypothetical equal pollen weighting for
Lepidoptera and unknown pollen weight r for Diptera gives:

  R(r) = (357 + 151*r) / (838 + 54*r).

To break even at the count-weighted level needs r=481/97=4.95876.
This is **NOT measured pollen transfer effectiveness**; the
actual per-visit relative effectiveness is unknown, the outcome
may be nonlinear, and all other insect orders are ignored.
A complete seven-point r sensitivity is exported.

ALAN draft PR #72 independently audits a dangerous provenance
issue: the source author's 1,038-row focal plant visitor worksheet
has more recorded night Diptera than the nominal all-survey sheet
(106 vs 54 dark, 181 vs 151 lit). It is NOT safe to subtract the
focal species rows from the total worksheet as though the two were
perfectly nested. Our bridge intentionally reads ONLY the
original all-survey visitation counts.

### Experiment 2. Dutch mixed nursery pollination, Boom et al. 2020

Primary publication DOI:
https://doi.org/10.1038/s41598-020-75471-1.
ALAN draft PR #67:
https://github.com/zuizui0223/alan/pull/67
ALAN source-verified original JATS SHA256
182dafe1e99fef5453ecf0d1d1401361fe949fd8d8617ae040588fd19795154f.
Source original replay Actions #43570186936 succeeded.

The same species Hadena bicruris acts as adult pollen vector and
offspring seed predator on Silene latifolia. Light treatments were
local ground-level dark, white, green or red (~7.6±1.2 lux nominal
artificial illumination), not satellite VIIRS.

Original treatment mean fractions:

| Light | Fruit set | Fruit infestation | Fertilized ovules in sampled uninfested fruit | Original calculated seeds per flower |
| --- | ---: | ---: | ---: | ---: |
| dark | .73 | .28 | .56 | 117 |
| white | .78 | .44 | .49 | 86 |
| green | .75 | .53 | .43 | 61 |
| red | .71 | .33 | .47 | 90 |

Reconstruct the ORIGINAL algebraic estimate using rounded means:

  p(fruit set) × [1 − p(fruit infested)] ×
  p(fertilized ovules among noninfested fruit) × 404 mean ovules.

For green versus dark, the ratio is approximately 0.515.
That is a decomposition of published rounded treatment means,
NOT independent raw mature-seed observations or regression mediation.
Fruit set overall was unresolved (source p=.17); fruit infestation
changed by spectrum (p less than .001) and ovule fertilization
by spectrum (p less than .01), but the model-derived net seeds per
flower test was NONSIGNIFICANT (original ANOVA p=.63).
Neither a proven net halving of fitness nor a general global
light-spectrum rule can be inferred.

### Direct link into the existing IWE candidate corpus

The preexisting candidate MIX002_BIERE_HONDERS_1996 lists a
Silene alba / Silene dioica × Hadena bicruris mixed nursery
system. Silene alba is a synonym within Silene latifolia
subsp. alba per Kew POWO (https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:921549-1).
The shared Hadena species and partial plant taxon identity make
the 1996 source and Dutch 2020 manipulation biologically relevant.
They are DIFFERENT papers, different populations and different
exposures. The composite historical "Silene alba / Silene dioica"
is not the same as an exactly matched single latifolia population.
The historic 1996 IWE source remains REJECTED_TIMING because
no independently measured same-season Hadena activity window
supports the preregistered seasonal synchrony contrast.
The Boom light experiment does not supply that missing object.

## The island and trait caution

ALAN main's spatial photographic observation:
five-year strict 7,982 photo-cell-years/710 island cell-years,
island×log(1+VIIRS) original white-floral-region ROI association
about -2.497 percentage points. Broader 20,543 photo-cell-years
attenuate to -1.205 with an interval crossing zero.
This is PHOTO WHITE COMPONENT, not verified white-flower species
prevalence, moth-pollination or pollinator-mediated evolution.
The legacy GloBI moth visitation documentation interaction
-1.902 did not retain a negative sign after the updated source
(version 0.11), so do not use it as evidence of genuine night
pollinator disappearance or island specialization.

The older actual chocho Anthocharis host geography remains
native 162 vs contemporary 272 resource units (110 source-defined
added), and an egg-observation-conditional 14-host WCVP scenario
168/274/106. No locally linked night-light experiment exists
for that butterfly in these sources. Anthocharis cardamines is
principally day-active; a moth experimental response must not be
applied mechanically to butterfly egg use. Both changes in host
identity and in temporal availability need their own evidence.

## What would count as a new macro/functional test

The core question is NOT a universal negative moth-ALAN slope.
The strongest discriminating hypothesis is CHANNEL-GATED
NET-REPRODUCTIVE VULNERABILITY: a light-associated decline in
effective nocturnal pollination affects final seed output
especially where measured autonomous selfing and effective
alternative pollen vectors fail to compensate and/or light
increases antagonistic seed-loss components.

Predeclare distinct measures and replicate at the proper grain:

- Exposures: manipulated ground lux and light spectrum (source
  treatment); separate observational VIIRS/PCNL with urban,
  climate, observer effort, vegetation and original island
  baseline adjustments.
- Times: HOURS OF DAY flowering availability versus independently
  measured effective pollen vectors, and separately DAYS OF YEAR
  flowering season versus same-season partner activity.
  Night-only/day-only is not a seasonal synchrony treatment.
- Functions: actual effective conspecific pollen delivery, ovule
  fertilization, fruit set, final mature viable seed, and
  seed loss by offspring florivores/seed predators. Never
  substitute one outcome for another.
- Biotic states: self-compatible versus verified autonomous
  selfing; true pollen limitation; before-light pollinator channel;
  site-specific effective moth, fly, bee, bat, bird or lizard
  replacement. Flower visitors and animal predators are not
  automatic pollen vectors.
- Contrasts: physical island versus ecologically/phylogenetically
  matched mainland populations at similar exposure and sampling
  effort, with multiple actual ALAN manipulations/site-years.
  No inference from a pooled photo/plant × globally joined
  host-species relationship alone.

A 2026 Swiss experimental floral-phenology paper measured daily
opening/closing and seasonal phenophase shifts at 14 illuminated
vs 14 dark locations (DOI 10.1016/j.biocon.2025.111650); it
does NOT yet yield same-location butterfly/moth partner-activity
overlap and viable-seed evidence. The existing ALAN macro PR
#64 explicitly records H3 true seasonal/diel mismatch and H4
island-prior-pollinator-shift interactions as NOT ESTIMABLE.

## Executable source receipt

From iwe root, run:

  python scripts/audit_alan_iwe_chocho_function.py --output-dir outputs/alan_bridge

Generates source-fixed all-survey guild changes, an explicitly
HYPOTHETICAL fly effectiveness threshold sweep, the complete
four-spectrum mixed moth pollinator/seed-predator arithmetic,
and one provenance/claim-ceiling receipt.

The program rejects drift in published rows or original source
signatures, a wrong source workbook/sheet, an IWE reclassification,
and nonrepresentative composite shortcuts. No addition to
data/extraction/direct_effects.csv, IWE strict H1 or the
chocho/alan submission manuscripts is authorized by this audit.
