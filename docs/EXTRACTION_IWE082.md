# IWE082 extraction receipt — Chamaedorea pinnatifrons × Brooksithrips chamaedorea

Source: Cascante-Marín A, Barrantes G, Ríos LD, Fuchs EJ. 2025. *Flowering time and pollinator abundance determine the female reproductive success in the dioecious palm Chamaedorea pinnatifrons (Arecaceae)*. Revista de Biología Tropical 73(S2):e64541. DOI `10.15517/rev.biol.trop..v73iS2.64541`.

Status: **unresolved strict-H1 mutualist candidate; independently measured specialist-thrips seasonality can order flowering windows, but plant-level dependence across repeated inflorescences is not recoverable from the published aggregate data**.

Interaction class: `mutualist`.

Dependence ID: `DEP_IWE082_CHAMAEDOREA_THRIPS`.

## Biological chain

The study followed a dioecious palm population during the 2012 reproductive season and measured:

- flowering phenology of female and male palms;
- final mature fruit production and fruit set for 115 female inflorescences from 74 female plants;
- weekly abundance of floral thrips on staminate inflorescences across 11 censuses;
- male/female neighbourhood and plant-trait covariates.

The dominant floral visitor is the specialist thrips `Brooksithrips chamaedorea`, and the source interprets the seasonal increase in female success in relation to the strong seasonal increase in thrips abundance.

## Independently measured partner window

Pollinator activity is not inferred from fruit set.

The study independently sampled adult thrips from staminate inflorescences through the season. Mean abundance increased approximately thirteen-fold, from about `20.8 ± 10.6 SE` adults per rachilla in the early flowering period to `282.0 ± 74.4 SE` in the late flowering period.

Therefore the seasonal partner window can prospectively order the flowering categories as lower versus higher pollinator availability before the female reproductive outcome is considered.

Calendar date by itself is not the IWE exposure; the external thrips activity curve is what licenses the ordering.

## Final reproductive outcome

Published female fruit set differs strongly among flowering windows:

- early: `0.030 ± 0.009 SE`, `n = 34` inflorescences;
- population peak: `0.079 ± 0.013 SE`, `n = 39`;
- late: `0.296 ± 0.027 SE`, `n = 42`.

These are final mature-fruit outcomes after pollination has acted.

## Why an aggregate contrast is not entered yet

The 115 inflorescences come from only 74 female plants. Individual palms developed 1–4 inflorescences, and inflorescences from the same plant could mature sequentially or weeks apart.

Consequently, an early-versus-late effect computed from the published inflorescence means, SEs and nominal inflorescence sample sizes would assume independence that is not guaranteed.

The paper's GLMMs for plant/neighbourhood predictors use random factors, but the published phenological-group comparison is a Kruskal–Wallis/Dunn analysis of inflorescences and does not provide the plant-level mapping required to construct a dependence-safe meta-analytic variance.

IWE therefore does not inflate precision by treating all 115 inflorescences as independent synchrony units.

## Prospective quantitative route

Preferred admission requires source-level rows containing:

- female plant identifier;
- inflorescence identifier;
- flowering date/window;
- flower number and final mature fruit count/fruit set;
- enough timing information to map the inflorescence to the independently measured thrips activity curve.

With those rows, IWE can freeze a plant-clustered model or derive one plant-level effect while retaining repeated-inflorescence dependence.

A source-reported model coefficient that directly links measured thrips availability to final female reproduction with an appropriate SE/covariance would also close the study.

## Prohibited shortcuts

IWE082 will not:

- call `late > early` a synchrony effect without the independently measured thrips curve;
- use early/late calendar date alone as partner matching;
- treat 115 inflorescences as 115 independent plants;
- use the sex-overlap Schoener index as if it measured female–thrips synchrony;
- replace final fruit set with pollinator abundance or visitation alone.

## Current source-recovery status

The peer-reviewed article is openly available and source-eligible. The article reports the aggregate phenological fruit-set values and weekly thrips trajectory, but the current public-source search has not identified a plant-ID-level raw dataset or supplementary table sufficient to resolve repeated female plants.

The current blocker is therefore **raw dependence mapping / direct partner-availability coefficient**, not biological plausibility.

## Claim ceiling

At present IWE082 supports:

> final female reproduction is much higher in flowering windows with independently observed high specialist-pollinator abundance, but the published aggregate data do not yet support an independence-safe study-level synchrony effect with sampling variance.

It does not yet enter `direct_effects.csv` or the common-scale programme gate.
