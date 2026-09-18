# IWE070 extraction receipt — Silene stellata × Hadena ectypa phenological synchrony

Source: Kula AR. 2012. *Quantifying context-dependent outcomes of the interaction between Silene stellata (Caryophyllaceae) and its pollinating seed predator, Hadena ectypa (Noctuidae), a potential mutualist*. PhD dissertation, University of Maryland. Handle `1903/12597`.

Relevant unit: Chapter 3, *Host plant synchrony with its pollinating seed predator contributes to the interaction outcome between Silene stellata (Caryophyllaceae) and Hadena ectypa (Noctuidae)*.

Status: **unresolved strict-H1 candidate; direct synchrony identified, final net effect not yet recoverable**.

## Direct timing exposure

The study followed individual focal plants and calculated flowering synchrony with `H. ectypa` oviposition through time. Oviposition is used as a measure of adult pollinating-seed-predator activity because adult females nectar/pollinate before oviposition.

Plants with `synchrony=0` flowered after the last observed Hadena egg, whereas the highest synchrony values occurred close to peak oviposition. This is a direct plant–partner temporal-matching metric, not calendar flowering date alone.

## Outcome architecture

Marked flowers were followed through senescence and laboratory processing. The chapter reports:

- initiated fruit set;
- flower/fruit predation by Hadena larvae;
- temporal oviposition and larval-density information.

The two years differ in flowering and oviposition phenology.

## Reported synchrony results

Initiated fruit set:

- 2008: `chi-square(1)=2.33, P=0.1271`;
- 2009: `chi-square(1)=2.21, P=0.137`.

Direct synchrony therefore did not detectably change fruit initiation in either year.

Hadena predation:

- 2008: higher synchrony predicted **higher** predation, `chi-square(1)=46.47, P<0.0001`;
- 2009: higher synchrony predicted **lower** predation, `chi-square(1)=16.74, P<0.0001`.

Thus the direction of the antagonist/cost component reverses between years.

## Why no primary effect is entered yet

IWE strict H1 requires a final plant reproductive outcome after pollination benefit and seed-predation cost can both act.

The indexed Chapter-3 results model initiated fruit set and predation separately. A single source coefficient for surviving mature fruits, mature seeds, or another final net female-fitness endpoint has not yet been recovered.

IWE therefore does **not**:

- combine the two chi-square tests algebraically;
- derive an effect magnitude from P values;
- assume that a predation coefficient equals a net plant-fitness coefficient.

No row is added to `direct_effects.csv` at this stage.

## What would close IWE070

Because individual flowers were followed through final processing, IWE070 could become a quantitative strict mixed effect if the underlying dissertation data or appendix allow reconstruction, at plant level, of:

1. the reported synchrony index; and
2. a final surviving-fruit or mature-seed outcome.

A slope/correlation plus sampling variance would then be extracted prospectively from the recovered data.

## Dependence

IWE070 belongs to the broader Kula/Reynolds/Dudash/Fenster `Silene stellata × Hadena ectypa` programme and may overlap years/plants with IWE015/IWE016 and related publications. Any future quantitative row must carry a shared programme-level dependence identifier.

## Claim ceiling

Current evidence supports:

> individual plant synchrony with adult Hadena activity changes the predation component of a mixed pollinating-seed-predator interaction, and the sign of that effect reverses between years.

It does not yet support a quantitative synchrony effect on final net plant fitness.


## Public-source recovery audit — 2026-09-18

A targeted recovery pass checked the public University of Maryland dissertation record, the indexed Chapter-3 text, the related 2013 American Journal of Botany paper, and the 2011 ESA abstract.

The public dissertation abstract confirms that synchrony between S. stellata flowering and H. ectypa oviposition was one of the core analyses and that synchrony effects on flower/fruit predation differed among seasons.

The ESA abstract is especially informative about data availability: in 2008 and 2009 all flowers on 114 and 94 plants, respectively, were marked, followed through senescence, and processed in the laboratory. The stated final analysis targets included seed set, fruit set, oviposition and flower/fruit/seed predation.

However, the indexed Chapter-3 results expose initiated fruit set and predation models, not a coefficient for final mature seed or surviving-fruit fitness as a function of synchrony. The related 2013 American Journal of Botany paper likewise reports initiated fruit set and predation, not a strict final synchrony-to-net-fitness coefficient.

Therefore the existence of processed seed data is **not** treated as evidence that the required net effect is recoverable from the published analysis.

### Locked adjudication

Current state:

`unresolved_raw_data_required`

IWE070 can close only if plant-level data become available containing, at minimum:

- plant identifier;
- the published flowering-Hadena synchrony metric or enough date-level records to reconstruct it;
- final surviving fruit and/or mature-seed outcome from the same marked flowers.

P values, chi-square statistics for initiated fruit set and predation, and annual means are insufficient substitutes.

No source coefficient is entered into `direct_effects.csv` from the currently public material.
