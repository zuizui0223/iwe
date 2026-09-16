# IWE001 extraction receipt — Kudo & Ida 2013

Source: Kudo G, Ida TY. 2013. *Early onset of spring increases the phenological mismatch between plants and pollinators*. Ecology 94:2311–2320. DOI `10.1890/12-2003.1`.

Data source: Ecological Archives `E094-213-A1`, Appendix A, Table A1.

Status: first direct Tier-A extraction.

## Source variables

Table A1 reports, by population and year:

- natural-pollination seed set;
- seed-set sample size;
- flowering onset date;
- first detection date of bumblebee queens;
- signed phenological mismatch in days.

The source defines the mismatch column as the temporal difference between flowering onset and first bumblebee detection. Positive values occur when bee detection follows flowering onset; negative values occur when bees are detected before flowering onset.

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

The source exposure is `mismatch`, so IWE's orientation step multiplies `z_native` by `-1`. Thus a positive oriented value means lower mismatch / greater temporal alignment is associated with higher seed set.

This reconstruction is intentionally simple and source-transparent. It is **not** described as the original paper's fitted regression coefficient, and it does not weight annual means by the number of flowers/plants used to estimate seed set.

## Extracted population effects

| Site | Years with complete mismatch + natural seed set | n | Pearson r: mismatch vs seed set | Native Fisher z | Variance | Oriented Fisher z |
|---|---|---:|---:|---:|---:|---:|
| NFP | 1999–2003, 2005–2012 | 13 | -0.6823367403 | -0.8334735665 | 0.1000000000 | +0.8334735665 |
| TOEF | 1999–2003, 2005–2008 | 9 | -0.9041525384 | -1.4945171706 | 0.1666666667 | +1.4945171706 |
| JOZ | 2002, 2003, 2007–2009, 2011, 2012 | 7 | -0.8184761715 | -1.1521836148 | 0.2500000000 | +1.1521836148 |

All three site effects share `dependence_id = DEP_IWE001_LONGTERM` and must not be treated as three fully independent publications.

## Missingness decisions

- NFP 2004 has no natural seed-set estimate and is excluded.
- TOEF 2004 has no bumblebee-detection/mismatch value and is excluded.
- JOZ years without a bumblebee-detection/mismatch value are excluded.
- No value is imputed.

## Claim boundary

This receipt supports only the existence and extraction of a direct site-level association between signed plant–pollinator timing mismatch and natural seed set in the Kudo & Ida long-term dataset.

It does not establish:

- causal effects of synchrony;
- independence among the three sites;
- independence from later Corydalis publications;
- equivalence between first bee detection and the full pollinator activity distribution;
- an absolute-distance mismatch effect;
- a general mutualist meta-analytic effect.

## Dependency follow-up

Before combining IWE001 with IWE002 or IWE003, map population names and observation years across the three Corydalis publications. Shared populations/years must receive a common higher-level dependency identifier or be represented by a non-overlapping extraction.
