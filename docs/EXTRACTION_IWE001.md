# IWE001 extraction receipt — Kudo & Ida 2013

Source: Kudo G, Ida TY. 2013. *Early onset of spring increases the phenological mismatch between plants and pollinators*. Ecology 94:2311–2320. DOI `10.1890/12-2003.1`.

Data source: Ecological Archives `E094-213-A1`, Appendix A, Table A1.

Status: first direct Tier-A extraction; **timing-domain audit repaired on 2026-09-16**.

## Source variables

Table A1 reports, by population and year:

- natural-pollination seed set;
- seed-set sample size;
- flowering onset date;
- first detection date of bumblebee queens;
- signed phenological mismatch in days.

The native `Mismatch day` is first bee-detection date minus flowering-onset date (`partner_minus_plant`):

- positive: plant flowers before first bee detection;
- zero: onset/detection match;
- negative: bees are detected before plant flowering.

The transcribed source rows used for audit are frozen in `data/extraction/source_rows/IWE001_appendix_A1.csv`.

## Why the original all-row extraction was not admissible for strict H1

The first IWE001 extraction correlated the signed mismatch column with seed set over all complete years and then reversed its sign. That was not sufficient for the strict H1 synchrony estimand. A signed lag that spans both sides of zero is not an absolute synchrony score: moving from +7 to 0 days increases matching, but moving from 0 to -7 days decreases onset synchrony even though the signed value continues to fall.

This contradicted `docs/TIMING_METRIC_CONTRACT.md`, which permits a signed lag in strict H1 only on a declared one-sided mismatch domain.

The all-row signed-lag effects are therefore superseded and are not retained in `direct_effects.csv`.

## Repaired strict-H1 estimand

For each population separately:

1. require natural-pollination seed set and mismatch day;
2. retain only years with `mismatch_day >= 0`, so flowering onset is on or before first bee detection;
3. within this one-sided domain, larger native mismatch is unambiguously farther from matching;
4. compute Pearson `r = cor(mismatch_day, natural_seed_set)` across annual observations;
5. convert to Fisher z, `z_native = atanh(r)`;
6. use `var(z_native) = 1/(n-3)`;
7. mark `exposure_direction = mismatch`, so the IWE orientation step multiplies the native z by -1.

A positive oriented value therefore means that movement toward onset matching, within the plant-earlier side of the interaction window, is associated with higher seed set.

This remains an observational association and does not make first bee detection equivalent to the full activity distribution.

## Extracted population effects after timing-domain repair

| Site | Strict-H1 years | n | Pearson r: mismatch vs seed set | Native Fisher z | Variance | Oriented Fisher z |
|---|---|---:|---:|---:|---:|---:|
| NFP | 1999–2003, 2005–2009, 2011–2012 | 12 | -0.6371151442 | -0.7533026655 | 0.1111111111 | +0.7533026655 |
| TOEF | 1999–2003, 2005–2006, 2008 | 8 | -0.8329788653 | -1.1977886791 | 0.2000000000 | +1.1977886791 |
| JOZ | 2002, 2003, 2008, 2012 | 4 | -0.9518477411 | -1.8510818557 | 1.0000000000 | +1.8510818557 |

All three effects share `dependence_id = DEP_IWE001_LONGTERM`. JOZ is deliberately low precision after the one-sided restriction; its large sampling variance must be retained rather than repaired by ad hoc pooling.

## Excluded from strict H1 but preserved for directional work

- NFP 2010: mismatch = -1 day;
- TOEF 2007: mismatch = -1 day;
- JOZ 2007: mismatch = -7 days;
- JOZ 2009: mismatch = -8 days;
- JOZ 2011: mismatch = -1 day.

These rows are not biological negatives. They represent the opposite mismatch direction (pollinator detected before flowering) and belong to the predeclared directional-mismatch analysis if enough comparable evidence accumulates.

Other missingness:

- NFP 2004: no natural seed-set estimate;
- TOEF 2004: no bee-detection/mismatch value;
- several JOZ years: no bee-detection/mismatch value.

No value is imputed.

## Dependence and later Corydalis papers

IWE001 overlaps conceptually and potentially biologically with IWE002 (Kudo & Cooper 2019) and IWE003 (2026). Before any joint meta-analysis, population identities and observation years must be mapped. Shared rows must not be counted twice. IWE002 also uses the opposite algebraic mismatch convention in its prose, so source-specific sign handling remains mandatory.

## Claim boundary

This receipt supports a direct site-level association between one-sided plant-earlier phenological mismatch and natural seed set in the Kudo & Ida long-term dataset.

It does not establish:

- a causal effect of synchrony;
- an effect when the pollinator is earlier than the plant;
- independence among the three site effects;
- independence from later Corydalis publications;
- equivalence between first bee detection and full pollinator activity;
- a general mutualist effect.
