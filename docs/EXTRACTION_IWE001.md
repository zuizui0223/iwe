# IWE001 extraction receipt — Kudo & Ida 2013

Source: Kudo G, Ida TY. 2013. *Early onset of spring increases the phenological mismatch between plants and pollinators*. Ecology 94:2311–2320. DOI `10.1890/12-2003.1`.

Data source: Ecological Archives `E094-213-A1`, Appendix A, Table A1.

Status: direct Tier-A native extraction; **not yet admissible to the strict H1 synchrony estimand**.

## Source variables

Table A1 reports, by population and year:

- natural-pollination seed set;
- seed-set sample size;
- flowering onset date;
- first detection date of bumblebee queens;
- signed phenological mismatch in days.

The source defines the mismatch column as bumblebee first-detection date minus flowering-onset date. Therefore the native metric is `partner_minus_plant`:

- positive: flowering starts before bee detection;
- zero: matched onset/detection;
- negative: bee detection precedes flowering.

The metric is signed, not an absolute mismatch distance.

## Extraction estimand

For each population separately, retain years with both:

1. natural-pollination seed set; and
2. reported mismatch day.

Compute the ordinary Pearson correlation

`r = cor(mismatch_day, natural_seed_set)`

across annual observations within that population.

The registered IWE effect family is Fisher-z correlation:

`z_native = atanh(r)`

with sampling variance

`var(z_native) = 1 / (n - 3)`.

This reconstruction is intentionally simple and source-transparent. It is **not** described as the original paper's fitted regression coefficient, and it does not weight annual means by the number of flowers/plants used to estimate seed set.

## Executable timing classification

The three extracted effects are currently encoded as:

- `timing_metric_type = partner_minus_plant`;
- `timing_analysis_class = unresolved_for_strict_h1`;
- `timing_domain = unknown`;
- `exposure_direction = mismatch` retained only as the native biological reading on the plant-earlier side, not as permission to sign-flip the effect for H1.

The present receipt does **not** list the actual mismatch-day values used in each site-level correlation. It therefore does not establish that all analyzed observations lie on one side of matching.

Under `TIMING_METRIC_CONTRACT.md`, a signed `partner_minus_plant` slope may enter the strict synchrony analysis only if the analyzed rows are shown to be one-sided. Until that row-level audit is added, `build_primary_dataset()` excludes all three IWE001 effects and no oriented synchrony effect is produced.

## Extracted population effects

| Site | Years with complete mismatch + natural seed set | n | Pearson r: mismatch vs seed set | Native Fisher z | Variance |
|---|---|---:|---:|---:|---:|
| NFP | 1999–2003, 2005–2012 | 13 | -0.6823367403 | -0.8334735665 | 0.1000000000 |
| TOEF | 1999–2003, 2005–2008 | 9 | -0.9041525384 | -1.4945171706 | 0.1666666667 |
| JOZ | 2002, 2003, 2007–2009, 2011, 2012 | 7 | -0.8184761715 | -1.1521836148 | 0.2500000000 |

All three site effects share `dependence_id = DEP_IWE001_LONGTERM` and must not be treated as three fully independent publications.

## Missingness decisions

- NFP 2004 has no natural seed-set estimate and is excluded.
- TOEF 2004 has no bumblebee-detection/mismatch value and is excluded.
- JOZ years without a bumblebee-detection/mismatch value are excluded.
- No value is imputed.

## Required follow-up for strict H1

Before any IWE001 row can be promoted to `timing_analysis_class = strict_window`:

1. record the actual mismatch-day values for every annual observation entering each site correlation;
2. verify separately for NFP, TOEF and JOZ whether all included values are `>= 0` (plant earlier or matched) or all are `<= 0` (partner earlier or matched);
3. set `timing_domain` to `plant_earlier_only` or `partner_earlier_only` only when the corresponding condition is demonstrated;
4. let validation derive/check the permitted `exposure_direction` from the native metric convention and domain.

If a site's analyzed values span both sides of zero, the current whole-site linear correlation cannot be relabelled as a strict synchrony effect. That site must remain outside H1 or be re-extracted as directional one-sided effects if the source data support doing so.

## Claim boundary

This receipt supports only the existence and extraction of a direct site-level association between signed plant–pollinator timing lag and natural seed set in the Kudo & Ida long-term dataset.

It does not establish:

- causal effects of synchrony;
- a one-sided timing domain for any of the three extracted site correlations;
- independence among the three sites;
- independence from later Corydalis publications;
- equivalence between first bee detection and the full pollinator activity distribution;
- an absolute-distance mismatch effect;
- a general mutualist meta-analytic effect.

## Dependency follow-up

Before combining IWE001 with IWE002 or IWE003, map population names and observation years across the three Corydalis publications. Shared populations/years must receive a common higher-level dependency identifier or be represented by a non-overlapping extraction.
