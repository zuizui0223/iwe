# IWE propagation endpoint sensitivity

_Generated from temporal_signal_components.csv and propagation_endpoint_audit.csv._

## Endpoint types

Mature seed/yield, intact post-cost fruits, terminal seedpod or gall fates, mature-seed damage, constructed reproductive potential and source-model fitness predictions are **different biological endpoints**, not exchangeable replicates of one fitness measurement.

| Endpoint | Links |
|---|---:|
| derived_reproductive_index | 5 |
| intermediate_only | 3 |
| observed_mature_seed_or_yield | 18 |
| observed_postcost_reproductive_units | 2 |
| observed_seed_damage_only | 1 |
| observed_terminal_fate | 3 |
| source_model_predicted_final | 1 |

## Retention under nested endpoint definitions

Retained direction means preserved or preserved_net_changed_mechanism. Incomparable links never enter the direction denominator.

| Scope | Reference | Links | Direction comparable | Direction retained | Exact preserved | Clusters |
|---|---|---:|---:|---:|---:|---:|
| mature_seed_yield | prospective_design | 14 | 14 | 12 | 12 | 10 |
| mature_seed_yield | realized_or_seasonal | 4 | 4 | 1 | 1 | 4 |
| plus_postcost_fruits | prospective_design | 14 | 14 | 12 | 12 | 10 |
| plus_postcost_fruits | realized_or_seasonal | 6 | 6 | 2 | 1 | 6 |
| plus_terminal_fates | prospective_design | 16 | 16 | 13 | 13 | 12 |
| plus_terminal_fates | realized_or_seasonal | 7 | 7 | 3 | 2 | 7 |
| original_final | prospective_design | 18 | 18 | 14 | 14 | 13 |
| original_final | realized_or_seasonal | 12 | 11 | 3 | 2 | 11 |

## Antagonist dependence-cluster sensitivity

Repeated links within a dependence cluster are collapsed; no comparable link means no classification, not a failure.

| Scope | Reference | Programmes | All retained | Mixed | None |
|---|---|---:|---:|---:|---:|
| mature_seed_yield | prospective_design | 3 | 3 | 0 | 0 |
| mature_seed_yield | realized_or_seasonal | 1 | 0 | 0 | 1 |
| plus_postcost_fruits | prospective_design | 3 | 3 | 0 | 0 |
| plus_postcost_fruits | realized_or_seasonal | 2 | 0 | 0 | 2 |
| plus_terminal_fates | prospective_design | 5 | 4 | 0 | 1 |
| plus_terminal_fates | realized_or_seasonal | 3 | 1 | 0 | 2 |
| original_final | prospective_design | 6 | 4 | 1 | 1 |
| original_final | realized_or_seasonal | 7 | 1 | 0 | 6 |

## Scope and interpretation

- Terminal gall or mature-seedpod fate is informative, but is not an intact-seed count.
- Seed number multiplied by germination is constructed reproductive potential, not observed offspring recruitment.
- A predicted intact reproductive-unit value propagated through a source equation is not independently observed final fitness.
- Percentage of mature seeds consumed measures a cost, not automatically net reproductive production per plant.
- The original final-link denominator remains unchanged. These are nested descriptive sensitivity subsets, not post-hoc claims that a previously included study was scientifically invalid.
- Timing provenance is confounded with biological system, study design and endpoint; these ratios cannot identify a causal stage effect or demonstrate out-of-sample predictive superiority.
