# IWE029 extraction receipt — Stigmaphyllon paralias × oil-collecting Centris bees

Source: Carneiro LT, Machado IC. 2025. *Evolutionary consequences of flowering–pollinator asynchrony: the case of a floral oil-producing plant and its oil-collecting bees*. Annals of Botany 136:745–754. DOI `10.1093/aob/mcaf126`.

Status: **Tier A strict H1; second independent quantitatively closed mutualist programme**.

## Why the timing contrast is strict

The authors sampled two different sets of flowering individuals at two points within the same reproductive season.

- **Peak-flowering period:** the plant population had many flowers, but legitimate oil-bee visitation was very scarce.
- **Late-flowering period:** 3–4 weeks later, sampling was deliberately established when pollinator activity was high.

The paper explicitly treats the two periods as strongly contrasting flowering–pollinator overlap states.

The partner-activity ordering is independent of seed outcome. Legitimate oil-bee visitation was indexed by the diagnostic necrotic lesion produced during oil collection:

- peak period: lesions on 7.5% of 134 flowers;
- late period: lesions on 93.6% of 140 flowers.

Three Centris species were observed: `C. aenea`, `C. caxiensis`, and `C. perforator`.

Thus the registered exposure is categorical:

`low overlap (peak) -> high overlap (late)`

and is stored with:

- `phenology_source = direct_interaction`;
- `exposure_direction = synchrony`.

This timing order is not inferred from seed set.

## Seed-set experiment

At each time point the study initially used 90 different flowering individuals, for 180 plants total. One to three fresh flowers per plant were tagged for phenotypic, pollen-limitation, fitness, and visitation measurements.

The pollen-limitation analysis compared natural pollination (NP) with supplemental hand pollination (HP) across the two flowering periods. Tag loss reduced the complete model sample to:

`n = 173`.

Seed set was modelled with a binomial GLM using:

- flowering time: peak vs late;
- treatment: NP vs HP;
- flowering-time × treatment interaction.

The source reports:

| term | estimate | SE |
|---|---:|---:|
| flowering time | +1.55 | 0.25 |
| treatment | +1.41 | 0.24 |
| flowering time × treatment | -1.26 | 0.31 |

The reported biological pattern confirms the source coding: under natural pollination, late/high-overlap plants had much higher seed set than peak/low-overlap plants, whereas supplemental pollen largely removed that difference. The pollen-limitation index was 0.74 at peak flowering and 0.03 late in flowering.

## Registered effect

For the natural-pollination reference condition, the flowering-time main effect is the high-overlap versus low-overlap log-odds contrast:

- `log OR_native = +1.55`;
- `SE = 0.25`;
- `Var = 0.0625`;
- `n = 173` for the source seed-set GLM.

Because higher overlap is already the positive exposure direction, no sign reversal is applied.

The effect is registered as:

`IWE029_SPAR_OVERLAP_LOGOR`

with:

- `effect_family = log_odds_ratio`;
- `outcome_family = seed_set`;
- `dependence_id = DEP_IWE029_STIGMAPHYLLON_CENTRIS`.

## Why this is independent replication

IWE029 is a Brazilian dry-forest Malpighiaceae–oil-bee system and is biologically and geographically independent of the Japanese `Corydalis ambigua × Bombus` programme used in IWE001.

It therefore supplies a second strict mutualist programme rather than another row from the same long-term system.

## What is not done

IWE does not:

- convert this log odds ratio to Fisher-z without a prospectively registered conversion;
- use the hand-pollinated contrast as an additional independent effect;
- count the three Centris species as three independent partners;
- interpret the study as a continuous per-day mismatch slope;
- infer lifetime fitness from seed set.

## Claim ceiling

IWE029 supports:

> Within this population and season, plants sampled during the directly observed high pollinator-overlap period had substantially greater natural-pollination seed-set odds than plants sampled during the low-overlap period.

It does not establish a class-level mutualist synchrony effect by itself.
