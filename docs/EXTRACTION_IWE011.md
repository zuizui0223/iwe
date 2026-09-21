# IWE011 extraction receipt — Kudo & Shibata 2025

Source: Kudo G, Shibata A. 2025. *Phenological selection mosaic of predispersal seed predation affects gender variation in an andromonoecious plant*. Journal of Ecology 113:2832–2845. DOI `10.1111/1365-2745.70130`.

Dataset and reproducible code: Hokkaido University Data Repository DOI `10.14943/hu95572`.

Status: **first strict-H1 antagonist effect admitted to the IWE primary table**.

## Phenological design

The five permanent plots HA, HL, HC, KD and HD occupy a local snowmelt-driven flowering gradient.

Across 2020–2023:

- HA flowered in mid-July;
- HL in mid- to late July;
- HC in late July to early August;
- KD in early to mid-August;
- HD in early to late August.

The predator moth *Phaulernis fulviguttella* lays eggs mainly in mid- to late July. The study reports intense predation in early-flowering plots and negligible predation in late-flowering plots.

For a prospectively defined extreme timing contrast, IWE uses:

- HA = high predator-overlap end;
- HD = low predator-overlap end.

This contrast is fixed from flowering and predator activity timing, not from the reproductive response.

## Final reproductive outcome

The study directly measured developing fruits, predation damage and mature intact fruits.

Final fruit-set rate is the number of intact fruits divided by the number of perfect flowers per plant.

Published Table 1 reports, pooled over 2020–2023:

| Plot | Timing interpretation | n | Final fruit-set mean | SD |
|---|---|---:|---:|---:|
| HA | high predator overlap | 177 | 0.13 | 0.19 |
| HD | low predator overlap | 127 | 0.40 | 0.29 |

These are post-predation reproductive outcomes, unlike the pre-predation fruit-number response emphasized in IWE010.

## Effect reconstruction

IWE defines the native contrast as

`high overlap HA - low overlap HD`.

The pooled standard deviation is

`s_p = sqrt(((n_HA-1)s_HA^2 + (n_HD-1)s_HD^2) / (n_HA+n_HD-2))`.

Cohen's `d` is corrected with

`J = 1 - 3/(4df - 1)`

to obtain Hedges' `g`.

Using the published summaries:

- pooled SD = 0.2369102996;
- Cohen's d = -1.1396718523;
- J = 0.9975144988;
- Hedges' g = **-1.1368391965**.

Sampling variance is reconstructed as

`Var(g) = J^2 * [(n1+n2)/(n1*n2) + d^2/(2df)]`

giving

`Var(g) = 0.0155963310`.

The total number of plant observations in the two extreme groups is 304.

## Executable classification

The extraction row is:

`IWE011_HA_VS_HD_FINALSET_SMD`.

Registered fields:

- `interaction_type = antagonist`;
- `evidence_tier = A`;
- `phenology_source = direct_activity`;
- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`;
- `outcome_family = final_fruit_set`;
- `effect_family = standardized_mean_difference`;
- `effect_native = -1.1368391965`;
- `variance_native = 0.0155963310`.

Because the exposure is already ordered from lower to greater antagonist synchrony, the oriented effect retains its negative sign.

## Dependence

IWE011 reuses permanent plots from the 2017–2019 IWE010 study and explicitly identifies that work as the previous study.

The effect therefore uses:

`DEP_PEUCEDANUM_KUDO_PROGRAM`.

See `PEUCEDANUM_DEPENDENCY_MAP.md`.

## Interpretation boundary

The negative strict-H1 effect is directionally consistent with the antagonist hypothesis: the high-overlap plot has lower final reproductive success than the low-overlap plot.

However, this is an observational population contrast. Plot identity, snowmelt environment and correlated plant traits are not experimentally held constant.

Accordingly, the row is valid direct timing–fitness evidence but must not be described as a causal estimate of seed-predator synchrony by itself.

## Effect-family boundary

This effect is a standardized mean difference. It is not numerically pooled with the IWE029 log-odds ratio.

The reference workflow now stratifies summaries by native effect family. H1 interaction-class comparisons require a common effect family or a separately registered conversion rule.
