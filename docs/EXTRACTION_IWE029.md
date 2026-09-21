# IWE029 extraction receipt — Carneiro & Machado 2025

Source: Carneiro LT, Machado IC. 2025. *Evolutionary consequences of flowering–pollinator asynchrony: the case of a floral oil-producing plant and its oil-collecting bees*. Annals of Botany 136:745–754. DOI `10.1093/aob/mcaf126`.

Study year/site: 2020, Parque Nacional do Catimbau, Pernambuco, Brazil.

Status: **first real strict-H1 effect admitted to the IWE primary table**.

## Timing design

The study sampled the same plant population at two distinct periods separated by approximately 3–4 weeks.

- first period: usual peak flowering of *Stigmaphyllon paralias*, with many flowering plants but very scarce pollinator visitation;
- second period: late flowering, deliberately established after continued monitoring when pollinator activity was high.

The authors did not claim to monitor the full pollinator activity curve across the entire flowering season. Instead, the design captured two strongly contrasting plant–pollinator overlap scenarios.

Legitimate oil-bee visitation was independently verified from characteristic necrotic lesions on the flag petal:

- peak-flowering flowers: 7.5% visited, 134 flowers observed;
- late-flowering flowers: 93.6% visited, 140 flowers observed.

Three *Centris* oil-bee species were observed.

## Strict-H1 timing classification

This is not an `overlap_index` in the mathematical sense. The native exposure is a two-level seasonal position whose order is supported prospectively and independently by measured pollinator activity.

The effect is therefore registered as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

For this study, moving from peak to late sampling means moving from the low-overlap/scarce-pollinator window to the high-overlap/high-pollinator window.

## Reproductive outcome

Pollen limitation was evaluated with natural pollination (NP) and pollen supplementation (HP) at both sampling periods.

The study initially assigned 45 plants per treatment at each sampling time. After tag losses, the binomial seed-set analysis used `n = 173` plants in total.

Reported model coefficients were:

| Predictor | Estimate | SE |
|---|---:|---:|
| Flowering time | +1.55 | 0.25 |
| Treatment | +1.41 | 0.24 |
| Flowering time × treatment | -1.26 | 0.31 |

The accompanying results establish the group ordering:

- at peak flowering, pollen supplementation increased seed-set probability about threefold relative to natural pollination;
- at late flowering, seed set was high and similar under natural and supplemented pollination;
- pollen-limitation index was 0.74 at peak and 0.03 at late flowering.

These statements and the three coefficient signs jointly identify the model reference cell as peak + natural pollination for the published main effects: the positive treatment coefficient represents the HP benefit at peak, the negative interaction represents the reduced HP benefit at late flowering, and the positive flowering-time coefficient therefore represents late versus peak under natural pollination.

## Extracted strict effect

The IWE strict-H1 effect is the natural-pollination late-versus-peak seed-set contrast:

`log OR = +1.55`

with

`SE = 0.25`

and registered sampling variance

`var = 0.25^2 = 0.0625`.

Positive orientation is retained because late flowering is the independently measured high-pollinator-overlap window.

The extraction row is:

`IWE029_LATE_VS_PEAK_NP_LOGOR`.

Its dependence identifier is:

`DEP_IWE029_CATIMBAU_2020`.

All additional IWE029 effects from these peak/late samples must remain in the same dependence cluster.

## Effect-family boundary

The native model is binomial, so this coefficient is registered as `log_odds_ratio`.

It must not be numerically pooled with Fisher-z correlations, standardized slopes, standardized mean differences or log response ratios unless a conversion rule is explicitly registered.

The primary meta helper now fails closed when more than one effect family is present without such a conversion.

## Current inferential meaning

This row changes the real strict-H1 dataset from zero rows to one row.

It does **not** create an inferential meta-analytic result by itself. Because it contributes only one dependence cluster to the mutualist class, the dependence-aware reference summary retains the point estimate but withholds its cluster-robust SE and confidence interval as `insufficient_dependence_clusters`.

## Data availability

The paper states that the underlying dataset is available upon request. Supplementary material provides figures but not the raw analysis table.

The current extraction therefore uses the published model coefficient and standard error only; no unpublished cell values are reconstructed.

## Claim boundary

IWE029 supports a direct within-population association in which a measured high-pollinator-overlap seasonal window had higher naturally pollinated seed-set odds than a measured low-overlap window.

It does not by itself establish:

- a general mutualist effect;
- an across-study pooled effect;
- independence of multiple effects from the same Catimbau population/year;
- a continuous dose–response to synchrony;
- a causal effect isolated from every other seasonal environmental difference.
