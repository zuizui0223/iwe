# IWE065 extraction receipt — Ficus semicordata × Ceratosolen gravelyi

Source: Zhang Y, Yang D-R, Peng Y-Q, Compton SG. 2012. *Costs of inflorescence longevity for an Asian fig tree and its pollinator*. Evolutionary Ecology 26:513–527. DOI `10.1007/s10682-011-9525-3`.

Status: **strict experimental timing, mixed-system benefit channel only; excluded from mixed net H1**.

## Biological classification

`Ficus semicordata` is dioecious and is pollinated by `Ceratosolen gravelyi`.

The pollinator species is part of a nursery-pollination mutualism: wasp offspring develop in male syconia, whereas female syconia produce seeds and do not support pollinator offspring. Thus the interaction is mixed at the host-species level, but the **female seed outcome measured here contains the pollination benefit without the larval/ovule-consumption cost in the same reproductive unit**.

Under IWE's frozen mixed-system contract, that means the seed-count slope is a benefit-channel effect rather than a net mixed effect. It is therefore not entered into `direct_effects.csv` for the mixed H1 comparison.

## Experimental timing exposure

Pre-receptive syconia were bagged to exclude pollinators. Single freshly emerged pollinators were then allowed into male or female syconia of known age after receptivity began. Mature female syconia were dissected and total seeds counted; male syconia were used to quantify pollinator offspring.

The exposure is one-sided delay from the first receptive day:

`delay_days = pollinator entry age - onset of receptivity >= 0`.

## Source model

The source analyzed seed and wasp offspring counts with GLMs using Poisson errors and syconium age as a covariate.

For female seed production, the source reports:

- `beta = -0.12 log seed count / day`
- `SE = 0.002`
- `Z = -64.33`
- `P < 0.001`

For male pollinator-offspring production:

- `beta = -0.04`
- `SE = 0.002`
- `Z = -23.93`
- `P < 0.001`

The female-seed model used mature female syconia distributed across age groups; the Fig. 5 legend gives group sample sizes `18, 22, 22, 16, 12, 15, 11, 0`, totaling 116 plotted mature female syconia.

The corresponding variance for the female seed-count slope is:

`0.002^2 = 0.000004`.

## Interpretation

The exact experimental timing effect is strong and unambiguous:

> each additional day that a female syconium waited for its pollinator reduced expected seed production on the source Poisson log scale.

However, because female syconia do not also bear the pollinator larvae whose development constitutes the nursery cost, this is not the final net outcome required for the `mixed_pollinating_seed_predator` primary H1 lane.

The result is stored separately as a `pollination_benefit` channel with `effect_family = log_rate_slope_per_day`.

## Why not reclassify as a pure mutualist study

The focal animal species is a nursery pollinator whose life cycle depends on male syconia of the same host species. Reclassifying the female-tree experiment as an ordinary pure mutualism solely to admit it to H1 would change the interaction classification after seeing the data.

IWE therefore preserves the biological system class as mixed while excluding this channel-only outcome from the net mixed H1.

## Claim ceiling

IWE065 supports:

> delayed pollinator arrival causally reduces female seed production in a dioecious fig nursery-pollination system.

It does not provide:

- a net mixed benefit–cost effect on the same reproductive unit;
- a direct estimate of lifetime plant fitness;
- evidence that mixed systems as a class benefit from greater synchrony.
