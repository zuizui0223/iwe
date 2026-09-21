# IWE002 extraction receipt — Kudo & Cooper 2019

Source: Kudo G, Cooper EJ. 2019. *When spring ephemerals fail to meet pollinators: mechanism of phenological mismatch and its impact on plant reproduction*. Proceedings of the Royal Society B 286:20190573. DOI `10.1098/rspb.2019.0573`.

Open manuscript: Hokkaido University HUSCAP.

Archived source data: Dryad DOI `10.5061/dryad.q4fm37m`, file `Kudo&Cooper_SourceData.xlsx`.

Status: direct Tier-A study with two analyzable components, but **no pooled IWE002 effect is currently admissible to the strict H1 synchrony table**.

## Study components

### A. Long-term natural monitoring

The study monitored the Nopporo population from 1999–2017.

Flowering phenology was measured within a 20 m × 20 m area of a large population. Naturally pollinated seed set was measured annually for 30–60 plants, except in 2004. Queen-bee emergence was monitored in the same forest.

The paper defines mismatch as

`flowering onset date - bee emergence date`.

Therefore:

- `timing_metric_type = plant_minus_partner`;
- negative: flowering before bee emergence;
- zero: matched onset/emergence;
- positive: flowering after bee emergence.

The long-term paper models naturally pollinated seed set against this signed mismatch variable with a binomial GLM.

### B. Snow-removal experiment

Snow removal was conducted in 2014–2016 using paired control/removal plots; all six plots were treated as controls in 2017.

The experiment advanced flowering onset by approximately 3–8 days. The biological ordering relative to bee emergence changed by year:

- control plots: flowering after bee emergence in 2014, 2015 and 2017; concurrent in 2016;
- removal plots: concurrent with bee emergence in 2014 and 2015; before bee emergence in 2016.

At the individual-plant level, reported mismatch values span `-9` to `+11` days.

## Strict-H1 timing adjudication

### Long-term signed mismatch slope

The long-term coefficient is a signed `plant_minus_partner` effect. A single signed slope can represent strict synchrony only on a demonstrated one-sided domain.

The Nopporo programme demonstrably includes years on both sides of matching. The overlapping IWE001 NFP series already contains both positive and negative values under the opposite-sign source convention, and the 2019 paper's figure and analysis retain signed mismatch over the extended 1999–2017 series.

Decision: **do not add the whole long-term signed slope to the strict H1 extraction table**.

### Pooled experimental mismatch slope

The individual-level experimental mismatch explicitly spans `-9` to `+11` days.

Decision: `timing_domain = both_sides`; a pooled mismatch coefficient is not a strict synchrony effect.

### Snow-removal treatment contrast

A treatment contrast cannot be labelled globally as “more synchrony” versus “less synchrony” because the treatment's position relative to bee emergence changes across years. In 2014–2015 removal moved flowering toward matching, while in 2016 it moved flowering from concurrent timing to plant-earlier mismatch.

Decision: **no single pooled treatment contrast is admitted as `strict_window`**.

## Valid extraction routes

IWE002 remains valuable for three predeclared routes.

1. **Directional mismatch analysis.** Reconstruct one-sided `plant_minus_partner < 0` and/or `> 0` effects if the archived raw data provide enough independent observations and recoverable sampling uncertainty.

2. **Year-specific strict experimental contrasts.** A year may qualify if control and treatment can be ordered prospectively by distance from the measured bee-emergence timing and the effect plus sampling variance can be recovered. These rows must retain shared experiment/year dependence.

3. **Direct timing sensitivity.** A treatment effect may be retained as `direct_timing_sensitivity` when it estimates reproductive sensitivity to altered flowering time but cannot be represented as a strict matching contrast.

No IWE002 row is added to `data/extraction/direct_effects.csv` by this receipt.

## Cross-publication dependence

The manuscript explicitly describes Kudo & Ida (2013) as the previous study and monitors the Nopporo population from 1999–2017.

IWE001 NFP covers the same Nopporo programme during 1999–2012, with the native site-level correlation using years with complete mismatch and seed-set data. IWE002 therefore extends, rather than independently replicates, the Nopporo evidence.

Any future IWE002 row based on the long-term Nopporo series must share a dependence cluster with overlapping IWE001 NFP evidence. See `CORYDALIS_DEPENDENCY_MAP.md`.

## Data availability boundary

The Dryad record confirms an archived source workbook, `Kudo&Cooper_SourceData.xlsx`. The dataset metadata are public. The current adjudication uses the open manuscript and published timing-domain information; no effect is reconstructed from inaccessible or inferred cell values.

Raw-data effect extraction should be done only after the workbook contents are available and provenance can be recorded.

## Claim boundary

This receipt supports:

- direct phenology-to-seed-set evidence in IWE002;
- the native `plant_minus_partner` sign convention;
- two-sided mismatch in the pooled experiment;
- non-independence of the long-term Nopporo series from IWE001 NFP.

It does not support:

- treating the whole signed long-term slope as a strict synchrony effect;
- treating the pooled experimental mismatch slope as strict synchrony;
- treating snow removal as a single consistently ordered synchrony manipulation across years;
- counting IWE001 NFP and IWE002 long-term monitoring as independent studies.
