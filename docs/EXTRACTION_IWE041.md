# IWE041 extraction receipt — Dianthus sylvestris × Hadena compta

Source: Collin C, Shykoff JA. 2010. *Flowering phenology and female fitness: Impact of a pre-dispersal seed predator on a sexually polymorphic species*. Plant Ecology 206:1–13. DOI `10.1007/s11258-009-9620-5`.

Status: **admitted to direct seasonal-timing sensitivity; not admitted to strict H1 synchrony**.

## Biological system

`Hadena compta` is both a pollinator and a predispersal seed predator of `Dianthus sylvestris`. The study followed flowering plants through the season and measured fruiting, caterpillar seed predation and final female reproductive success.

The final relative reproductive outcome is the fraction of flowers that produced unattacked fruits containing mature seeds available for dispersal. This is preferable to using visitation or attack alone because it already integrates successful fruit production and loss to seed predation.

## Timing exposure

The exposure is **plant flowering onset / seasonal position**. It is not a direct overlap index with an independently measured moth-activity distribution.

Therefore:

```text
flowering onset -> final reproductive success
```

is directly estimable, whereas

```text
plant-Hadena synchrony -> final reproductive success
```

is not identified under the IWE strict-H1 contract.

The study is consequently stored in `timing_sensitivity_effects.csv`, never `direct_effects.csv`.

## Quantitative effects

The paper reports linear slopes (± 1 SE) for relative reproductive success versus flowering-onset period:

| Year | slope | SE | variance |
|---|---:|---:|---:|
| 2001 | -0.037 | 0.009 | 0.000081 |
| 2003 | -0.076 | 0.030 | 0.000900 |

Both years therefore show lower net female reproductive success among plants beginning flowering later in the season.

The reported absolute-reproductive-success slopes are also negative (`-0.13 ± 0.03` in 2001 and `-0.29 ± 0.07` in 2003), but these are retained as corroborating source information rather than additional meta rows to avoid double counting the same plants/outcome process.

## Sample/dependence handling

The field sample comprised 333 plants in the 2001 analysis set described for flowering phenology and 119 plants rescored in 2003. The reported model degrees of freedom indicate some complete-case loss, so the stored sample sizes are descriptive and are **not** used to reconstruct uncertainty. Sampling variance is calculated only as the square of the source-reported SE.

Both annual rows share:

`dependence_id = DEP_IWE041_DIANTHUS_HADENA`

and are not treated as independent biological systems.

## Interpretation ceiling

IWE041 supports:

> seasonal position predicts final reproductive success in a mixed pollinating-seed-predator system.

It does not by itself support:

- a strict effect of plant–moth synchrony;
- a causal claim that Hadena timing alone generated the flowering-date slope;
- a net benefit of greater or lesser partner overlap;
- an independent replication of two biological systems from the two study years.

## Prospective-integrity note

IWE041 was discovered after the search-completion freeze, but its outcome direction was visible during discovery before any holdout assignment. It is therefore **ineligible as a blind confirmatory record** for the screening-informed antagonist/mixed shape hypothesis. It remains eligible for the preregistered evidence map and timing-sensitivity synthesis.
