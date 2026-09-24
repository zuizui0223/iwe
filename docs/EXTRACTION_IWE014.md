# IWE014 quantitative-recovery receipt — Pettersson 1991

Source: Pettersson MW. 1991. *Flower herbivory and seed predation in Silene vulgaris (Caryophyllaceae): effects of pollination and phenology*. Ecography 14:45–50. DOI `10.1111/j.1600-0587.1991.tb00632.x`.

Related dissertation: Pettersson MW. 1992. *Pollination, oviposition and seed predation by flower visiting insects in bladder campions (Silene vulgaris s.l., Caryophyllaceae)*. Uppsala University.

Status: **second independent mixed programme confirmed; strict-H1 biology eligible; SMD quantitative extraction pending source variance**.

## Why this programme is independently useful

The study concerns *Silene vulgaris* and its noctuid *Hadena* flower visitors in a Pettersson/Uppsala research programme. It is distinct from IWE015, which concerns *Silene stellata × Hadena ectypa* at Mountain Lake Biological Station in Virginia.

Any eventual IWE014 effect is therefore assigned to:

`DEP_IWE014_SILENE_VULGARIS_PETTERSSON`.

This dependence identifier is distinct from:

`DEP_SILENE_STELLATA_HADENA_MLBS`.

Thus IWE014 is a genuine candidate for the **second independent mixed-system cluster**, not another row from the IWE015 programme.

## Strict timing biology

The study compares two flowering seasons with markedly different pollinator abundance. Noctuid moths of *Hadena* act both as pollinators and as seed predators.

The source reports the coupled pattern:

- lower pollinator abundance -> lower percentage of pollinated flowers;
- lower *Hadena* activity -> less flower/fruit destruction and fewer seed capsules preyed upon;
- the low-pollinator/low-Hadena season nevertheless has higher final seed set because the predation cost is lower.

The paper also reports within-season timing structure: early-flowering individuals have similar pollination success but higher seed predation than late-flowering individuals.

The cross-season comparison therefore has a measured partner-activity ordering independent of the final reproductive value. Under the IWE contract it is admissible in principle as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- mixed pollinating seed predator interaction class.

## Why no effect row is created yet

The accessible abstract/full-text metadata establish the direction of pollinator abundance, seed predation, and final seed set, but do not expose all statistics required for the registered SMD contract.

For an SMD extraction IWE requires the high- and low-overlap groups to have source-backed:

- final post-predation reproductive mean;
- SD, or SE together with n;
- sample size.

At present the missing source-table variance/sample-size combination has not been recovered. The original article is available through publisher/JSTOR metadata, and the 1992 Uppsala dissertation is bibliographically confirmed, but no machine-readable source table with the required values has been recovered in the current workflow.

IWE therefore does **not** digitize figures, infer error bars, invent n, or back-calculate variance from significance alone.

## Executable state

The strict adjudication registry records:

- `strict_h1_status = eligible`;
- `quantitative_status = pending`;
- target `effect_family = standardized_mean_difference`.

Because no effect row exists yet, IWE014 does not count toward the executable two-cluster replication target. The mixed class remains at one extracted SMD dependence cluster.

## Exact recovery target

The next source-recovery action for IWE014 is deliberately narrow: recover the original numerical final-seed-set summaries for the two partner-abundance seasons, including variance and n.

If those values are recovered, the contrast will be computed with the existing Hedges-g contract and assigned to `DEP_IWE014_SILENE_VULGARIS_PETTERSSON`.

No change to the estimand, effect family, or timing definition is permitted merely to make the second cluster count.

## Claim boundary

IWE014 already supports the qualitative ecological conclusion that a year with lower *Hadena*/pollinator activity can have higher net seed set because reduced seed-predation costs offset reduced pollination.

It does not yet supply a variance-bearing SMD and therefore does not yet satisfy the second mixed-cluster target.
