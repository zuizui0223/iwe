# Jackson 2022 external ecological holdout — crop regularity × known seed predators

Date: 2026-10-08
Status: **external public-data PROBE / exploratory, outcome literature already exposed**.
This is *not* original strict H1, not a causal identification design, and
not a preregistered confirmatory result.

## Primary precedent and published result

Jackson et al. (2022), *Journal of Ecology*, DOI
[10.1111/1365-2745.13867](https://doi.org/10.1111/1365-2745.13867),
used **31 years of seed-trap records across 201 woody species** in the
Barro Colorado Island forest to estimate premature seed/fruit abortion.

Across the community, **39% of seeds** were estimated to have been
abscised prematurely. The study reported an association between a
species' rate of premature seed drop and (a) whether seed predators had
been reared from that species, (b) seed mass, (c) plant abundance and
height, and (d) temporally more stable seed crop sizes.

**Crucial model gap:** the original open analysis
[`03_fit-models.R`](https://github.com/ee-jackson/premature-fruit-drop/blob/7568638780b880a83a0cbd89e777104fbb14f6b9/code/scripts/03_fit-models.R)
fits **seven separate single-predictor** binomial mixed models
(`(1|year)+(1|sp4)`). It does not jointly fit the
`cvseed_cs × seedpred_pres` interaction.

The published fitted model objects at
[`model-fits.rds`](https://github.com/ee-jackson/premature-fruit-drop/blob/7568638780b880a83a0cbd89e777104fbb14f6b9/output/results/model-fits.rds)
may contain sufficient source model frames to reconstruct the matched
species-year predictor/outcome grain, *without accessing restricted
sources or inventing values*. The one-time access check is
`scripts/probe_jackson2022_saved_model_frames.R`. It reports
whether public model objects retain exact aligned source counts and
predator status, rather than assuming downloadable original Dryad CSVs.

## Specific mechanism and opposing predictions

The IWE question is **not** just whether phenological mismatch
correlates with output. It is whether a predictable plant resource can
be exploited by an antagonist that selects its future reproductive
opportunity.

Predictability has **three distinct meanings**, which must NOT be
collapsed:

| Quantity | System | What is actually measured |
|---|---|---|
| **Crop-size regularity over years** | Jackson 2022 tropical trees | `cvseed`, species-level coefficient of temporal variation of seed crop size; **not flowering-date predictability** |
| **Predictability of which individual fruits are retained** | Östergård et al. 2007, *Lathyrus–Bruchus* | nonrandom future abortion tied to fruit position and phenology, which beetles exploit |
| **Within-inflorescence placement of the fruit-retention interval** | James et al. 1994, *Yucca elata* | a mean 5-night retention window moving among early/mid/late flowering positions |

These are nested-scale hypotheses, **not an existing homogeneous
global dataset**. The external Jackson data can test only the first
predictability dimension. No inference about per-flower egg choice or
host tissue ability can be made from annual seed traps.

A falsifiable *associational* prediction is:

> If the negative association of `cvseed` (less regular crop sizes)
> with premature abscission mainly reflects consumer exploitation of
> more regular fruiting, this association should be more negative in
> species with an independently recorded pre-dispersal seed predator.

**Alternative 1: trait/resource hypothesis.** The negative `cvseed`
association persists in species without any recorded predator, or
does not significantly differ by predator status. Stable crop
production may be correlated with resource allocation, plant traits
or monitoring/detection effort without requiring enemy exploitation.

**Alternative 2: differential sampling.** Species known to host
predators are more common, conspicuous or densely sampled; `seedpred_pres=0`
does not mean a genuine absence of enemies, and missingness/detection
could produce an apparent interaction.

## Analysis predeclared for this exploratory extension

Only if *public* saved model frames contain source-matched
`year, sp4, abscised_seeds, viable_seeds, cvseed_cs, seedpred_pres`:

1. Match exactly on **species × year**, enforcing matching counts across
   separately fitted predictor model frames; never row-bind datasets
   or count estimated seeds as independent species.
2. Separate species-level evidence from yearly repetition.
   Define one species-level total premature/viable seed outcome
   with a strictly reported species denominator. Use an explicit
   offset/pseudocount for proportions 0 or 1.
3. Compare the response-blind, fixed nested models
   `M0: logit(abscission) ~ cvseed + predator_status` and
   `M1: M0 + cvseed:predator_status`, checking group sample
   support. The interaction sign matters more than within-predictor
   significance.
4. Use **species-blocked** uncertainty / permutation or bootstrap
   (not individual seeds as replicates). Apply reasonable sensitivity
   to seed count threshold, species weighting and inclusion of plant
   traits such as seed mass and density, with exact eligible samples
   reported. Phylogenetic dependency remains a further limitation.
5. Explicitly record whether the outcome has been inspected,
   and distinguish exploratory association from external prospective
   prediction or plant-fitness causality.

No statistical results are asserted by creating the code or reading
metadata; a model-fit access probe does **not** prove viable source
linkage. The published coefficients also must not be described as
joint-adjusted effects because the original analyses were one trait
at a time.

## Executed public model-object reanalysis (2026-10-08)

The archived `model-fits.rds` file was successfully retrieved **from
the pinned public GitHub repository**, not from the underlying Dryad
deposits. Two original `glmer` model frames contained exactly matching
estimated premature and viable seed counts at **2,609 matched
species × year records from 124 tree species over 31 years**.

- 91 species have a reared/recorded pre-dispersal seed predator.
- 33 species have **no recorded predator**, which is not the same as
  experimentally confirmed absence.
- Both species-level traits are constant across years; source counts
  match exactly after joining on original species code and year.

Using one species-level response constructed from the sum of its
observed seed-trap count estimates, an equal-species-weight linear
model of smoothed log seed-loss odds gave:

| Species-level specification | CV × predator interaction coefficient |
|---|---:|
| Equal species weight (124 species; primary) | **+0.3632** |
| Cap-weighted by square root of estimated seed counts | **+0.0186** |
| Species with at least ten observed years (99 species) | **+0.7206** |
| After accounting for measured seed mass and local adult abundance (89 species; 68 predator-recorded, 21 without records) | **+0.7087** |

The **1,000-draw stratified species bootstrap** for the primary
interaction gave a percentile 95% interval **[-0.6691, +1.0022]**.
This is a descriptive bootstrap interval, not a prospective or
phylogenetically adjusted confidence statement. The adjusted fit has
**no separate uncertainty interval**, uses fewer species and must
not be presented as a statistically supported opposite mechanism.
The much smaller seed-count-weighted interaction demonstrates
that the numerical magnitude is **not stable to weighting**. These coefficients
are differences in the slope of *crop-size variation*, not flowering
dates or resource-retention probability.

**First interpretation:** the prespecified directional prediction
that documented predator hosts have a *more negative* CV–abscission
slope (expected interaction < 0) **was not supported**. The point
estimate has the opposite sign, crosses zero widely, and shrinks
towards zero under source-count weighting. It would be incorrect to
call the opposite mechanism established, or to claim that seed
predators do not exploit predictable fruits in general.

The analysis is in
`scripts/analyze_jackson2022_predator_crop_regularities.R`,
run against the exact public model-fits revision, with outputs in the
short-lived GitHub Actions artifact. The source model objects were
already fitted on the observations; this is **not an independent
validation cohort or a source-blind predeclared experiment**. Its
inference is limited by phylogenetic relatedness, varying seed-trap
sampling, nonrandom recording of seed predators, and the inability
of trap-derived immature seed counts to identify the cause of
fruit abscission.

**Mechanism nonidentification:** even a reliable positive or negative
interaction in this observational survey cannot by itself
distinguish insect-triggered abortion from plant-selected abortion
that insects learn to anticipate. Both processes can produce
predator-correlated seed-loss patterns. The individual-fruit timing
and survival records needed to distinguish them remain unavailable
in this external dataset.

## What it could change in IWE

A predator-status interaction would supply external, cross-species
**associational evidence** consistent with the idea that *regular
resource availability can amplify enemy-associated reproductive
losses*. A null interaction, or an equally strong trend in species
without recorded predators, would refute the **consumer-specific**
version of this mechanism within that dataset.

Either outcome is scientifically interpretable, but neither resolves
the original IWE strict synchrony meta-analysis. Such an external
ecological route belongs in the fitness-conversion/host-filter
manuscript only if it adds biological information beyond the original
2022 paper and remains clearly separate from the confirmatory H1
evidence ledger.

## Sources and reproducibility

- Paper: Jackson et al. 2022, DOI `10.1111/1365-2745.13867`.
- Public code and fitted models (fixed commit):
  [ee-jackson/premature-fruit-drop](https://github.com/ee-jackson/premature-fruit-drop/tree/7568638780b880a83a0cbd89e777104fbb14f6b9).
- Original `fruit_drop.csv` and `TidyTrait.csv` data are stated in
  the publication's Dryad repositories
  `10.5061/dryad.4mw6m909j` and `10.5061/dryad.230j5ch`.
  The publicly posted models are only an **alternate documented
  source** of potentially retained fitting data, not independent
  observations.
