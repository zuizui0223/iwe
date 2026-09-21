# IWE001 extraction receipt — Kudo & Ida 2013

Source: Kudo G, Ida TY. 2013. *Early onset of spring increases the phenological mismatch between plants and pollinators*. Ecology 94:2311–2320. DOI `10.1890/12-2003.1`.

Data source: Ecological Archives `E094-213-A1`, Appendix A, Table A1.

Status: direct Tier-A native extraction; **whole-site signed-lag effects are not admissible to the strict H1 synchrony estimand**.

## Source variables

Table A1 reports, by population and year:

- natural-pollination seed set;
- seed-set sample size;
- flowering onset date;
- first detection date of bumblebee queens;
- signed phenological mismatch in days.

The source mismatch column is bumblebee first-detection date minus flowering-onset date. Therefore the native metric is `partner_minus_plant`:

- positive: flowering starts before bee detection;
- zero: matched onset/detection;
- negative: bee detection precedes flowering.

The metric is signed, not an absolute mismatch distance.

## Native whole-site extraction

For each population separately, retain years with both natural-pollination seed set and a reported mismatch day, then compute

`r = cor(mismatch_day, natural_seed_set)`

across annual observations within that population.

The registered effect family is Fisher-z correlation:

`z_native = atanh(r)`

with sampling variance

`var(z_native) = 1 / (n - 3)`.

This reconstruction is source-transparent and is not represented as the original paper's fitted regression coefficient.

## Row-level domain audit

The Ecological Archives table directly resolves the timing-domain question.

### NFP — Nopporo Forest Park

Analyzed mismatch days:

`4, 1, 1, 7, 7, 3, 1, 2, 7, 7, -1, 1, 0`

Domain counts: 11 positive, 1 zero, 1 negative.

### TOEF — Tomakomai Experimental Forest

Analyzed mismatch days:

`3, 5, 1, 7, 4, 5, 7, -1, 2`

Domain counts: 8 positive, 0 zero, 1 negative.

### JOZ — Jozankei forest

Analyzed mismatch days:

`5, 2, -7, 5, -8, -1, 2`

Domain counts: 4 positive, 0 zero, 3 negative.

All three extracted site correlations therefore span both sides of exact matching.

## Executable timing classification

The three native whole-site effects are encoded as:

- `timing_metric_type = partner_minus_plant`;
- `timing_analysis_class = unresolved_for_strict_h1`;
- `timing_domain = both_sides`;
- `exposure_direction = mismatch` retained only as source-direction metadata, not as permission to orient the whole coefficient as synchrony.

Because each whole-site correlation spans both sides of zero, no single sign transform can convert it into a monotonic synchrony effect. These rows are retained as native Tier-A evidence but are permanently excluded by `build_primary_dataset()`.

This is no longer a missing-information problem. Promotion of these whole-site coefficients to `strict_window` would violate the timing contract.

## Extracted population effects

| Site | Years with complete mismatch + natural seed set | n | Pearson r: mismatch vs seed set | Native Fisher z | Variance | Timing domain |
|---|---|---:|---:|---:|---:|---|
| NFP | 1999–2003, 2005–2012 | 13 | -0.6823367403 | -0.8334735665 | 0.1000000000 | both sides |
| TOEF | 1999–2003, 2005–2008 | 9 | -0.9041525384 | -1.4945171706 | 0.1666666667 | both sides |
| JOZ | 2002, 2003, 2007–2009, 2011, 2012 | 7 | -0.8184761715 | -1.1521836148 | 0.2500000000 | both sides |

All three site effects currently share `dependence_id = DEP_IWE001_LONGTERM`.

## Directional re-extraction route

The public annual table permits a predeclared directional analysis without forcing the whole signed slope into H1.

On the plant-earlier side (`partner_minus_plant > 0`), the available annual counts are:

- NFP: n = 11;
- TOEF: n = 8;
- JOZ: n = 4.

On the partner-earlier side (`partner_minus_plant < 0`), the counts are only:

- NFP: n = 1;
- TOEF: n = 1;
- JOZ: n = 3.

Thus the partner-earlier side is too sparse for the registered Fisher-z sampling variance, while the plant-earlier side is potentially extractable as `timing_analysis_class = directional_mismatch`.

No directional subset row is added to the extraction CSV in this receipt; a dedicated directional-analysis output must prevent double counting with the native whole-site rows.

## Missingness decisions

- NFP 2004 has no natural seed-set estimate and is excluded.
- TOEF 2004 has no bumblebee-detection/mismatch value and is excluded.
- JOZ years without a bumblebee-detection/mismatch value are excluded.
- No value is imputed.

## Claim boundary

This receipt supports the existence of direct site-level associations between signed plant–pollinator timing lag and natural seed set, and it establishes that the native whole-site effects are two-sided.

It does not establish:

- a causal effect of synchrony;
- an absolute-distance mismatch effect;
- a strict H1 synchrony effect from any whole-site IWE001 coefficient;
- independence among the three sites;
- independence from later Corydalis publications;
- equivalence between first bee detection and the full pollinator activity distribution;
- a general mutualist meta-analytic effect.

## Dependency follow-up

IWE002 monitors the Nopporo population from 1999–2017 and explicitly describes the 2013 study as its previous study. The IWE002 long-term series therefore extends the IWE001 NFP series rather than supplying an independent replication. Cross-publication dependence is documented in `CORYDALIS_DEPENDENCY_MAP.md`.
