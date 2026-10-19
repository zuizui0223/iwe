# Wu et al. 2015 — adult midge × susceptible wheat-stage overlap reaches final yield loss

Date: 2026-10-06  
Study: Wu et al. 2015, winter wheat × orange wheat blossom midge (*Sitodiplosis mosellana*)  
DOI: `10.5846/stxb201308112060`  
Landscape role: high-provenance antagonist final-fitness anchor with independently measured adult activity and a source-defined susceptible host stage.

## Why this study is unusually useful

The programme independently measures all of the biological ingredients that the original strict IWE literature often lacks:

1. adult *S. mosellana* occurrence through the season, monitored with yellow sticky traps;
2. wheat developmental stage through ear emergence and flowering;
3. experimental identification of the susceptible host stage by bagging ears at different developmental stages;
4. final crop yield loss;
5. across-cultivar variation in adult–host-stage overlap.

The overlap coordinate is defined before final yield loss, using the niche-overlap formulation of Geange et al.

## Host-stage filter identified experimentally

In the 2012 bagging experiment, wheat was protected beginning at different developmental stages.

The published source summary reports average yield loss of:

- **3.48%** when ears were bagged during ear emergence;
- **10.79%** when bagging was delayed until flowering.

The source therefore identifies ear emergence, rather than flowering, as the principal susceptible window for adult attack/oviposition.

This provides a pre-final host-stage filter independently of the cultivar overlap analysis.

## Adult timing is independently measured

Adults were monitored in April–May using yellow sticky traps.

In 2013, a cold event delayed the adult occurrence period to **4–13 May**, creating a strong interannual shift in adult–plant alignment.

The study then compared adult occurrence with cultivar-specific ear-emergence schedules.

## Source-reported overlap-to-final-loss contrasts

The abstract reports the following extreme source-defined groups:

| Year | Group | Cultivars | Ear-emergence window | Synchrony | Mean yield loss |
|---|---|---:|---|---:|---:|
| 2012 | maximum overlap | 23 | 22–28 Apr | **0.628** | **78.1%** |
| 2012 | minimum overlap | 3 | 28 Apr–2 May | **0.307** | **11.7%** |
| 2013 | maximum overlap | 3 | 4–11 May | **0.783** | **2.41%** |
| 2013 | minimum overlap | 11 | 15–25 Apr | **0.062** | **0.04%** |

Across more than 400 susceptible cultivars evaluated over the two years, the source reports a significant positive relationship between adult–ear-emergence synchrony and yield loss.

It also reports a significant positive relationship between the **cumulative number of adults occurring during each cultivar's ear-emergence period** and yield loss.

## Why overlap alone is not enough

The extreme groups show an important year effect.

A very high overlap score in 2013 (0.783) is associated with only 2.41% mean loss, whereas a lower maximum overlap in 2012 (0.628) is associated with 78.1% loss.

Thus overlap is not a sufficient exposure magnitude by itself.

The biologically stronger coordinate is conceptually:

`stage-matched adult exposure = adult abundance during the susceptible ear-emergence window`.

This is exactly the causal-depth distinction now central to IWE: phase alignment determines whether exposure is possible, while adult abundance determines how much exposure occurs.

## Phase-alignment status

This programme satisfies:

- independent adult timing: **yes**;
- effective/susceptible host-stage timing: **yes**;
- pre-final host-stage filter: **yes**, from the bagging experiment;
- variation in alignment: **yes**, across cultivars and years;
- final plant endpoint: **yes**, yield loss.

The accessible source summaries report that both synchrony and cumulative adults during ear emergence correlate significantly with yield loss, but do not expose the per-cultivar table or comparable model-performance statistics needed for a prospective paired test of:

1. adult/calendar timing alone;
2. overlap alone;
3. stage-matched adult exposure.

Accordingly this is a strong final-fitness anchor and a phase-gate `host_sensitivity_final` candidate, **not** `confirmatory_ready`.

## Claim boundary

This is an agricultural system, but the biological estimand is the same stage-specific antagonist problem as in the wild-plant corpus.

No common SMD is reconstructed from the source summaries, and the four extreme overlap groups are not treated as independent meta-analytic effects.

The result is used as high-provenance geometry and signal-propagation evidence only.

Source-backed summary values are stored in
`data/source_reconstructions/wu2015_wheat_midge_overlap.csv`.
