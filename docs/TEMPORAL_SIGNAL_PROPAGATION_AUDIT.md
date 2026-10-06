# IWE temporal signal-propagation audit

_Generated from data/registry/temporal_signal_components.csv; do not edit counts by hand._

## Scope

- Registered propagation links: **18**
- Studies: **17**
- Dependence clusters: **17**
- Links reaching a final plant-fitness endpoint: **15** from **14 studies**

A propagation link is not an effect size. It records whether a source-backed timing signal is preserved, transformed, reversed, erased, buffered, or fails to track a downstream stage. Multiple links from one programme retain one dependence cluster.

## Transformation states

| Transformation | Links |
|---|---:|
| buffered | 3 |
| erased | 3 |
| preserved | 7 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 2 |
| tracking_inertia | 1 |

## Interaction classes

| Interaction type | Links |
|---|---:|
| antagonist | 10 |
| mixed_pollinating_seed_predator | 4 |
| mutualist | 4 |

## Provenance of the upstream temporal reference

| Window-reference class | Links |
|---|---:|
| direct_interaction_manipulation | 3 |
| independent_partner_activity | 4 |
| realized_interaction_window | 9 |
| seasonal_position_only | 2 |

## Transformations observed in chains that reach final plant fitness

| Transformation | Links |
|---|---:|
| buffered | 2 |
| erased | 2 |
| preserved | 7 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 1 |
| tracking_inertia | 1 |

## Final-link transformations by interaction class

This matrix is descriptive for the targeted pilot corpus. It is not a literature-wide prevalence estimate.

| Interaction type | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| mutualist | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| antagonist | 3 | 1 | 1 | 2 | 1 | 1 | 0 |
| mixed_pollinating_seed_predator | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Interpretation

The current pilot falsifies the idea that a phenological effect can be represented by one invariant synchrony coefficient carried unchanged from encounter to fitness. Source-backed timing signals are observed to persist, reverse sign, be shifted by host/consumer filtering, disappear before the next consumer stage, be buffered by alternative ecological routes, or fail to track moving resources. In the current targeted set, all four mutualist service-window links that reach final plant fitness are classified as preserved, whereas antagonist and mixed links occupy multiple transformation states. This class pattern is a hypothesis-generating contrast, not a prevalence estimate.

Positive downstream propagation is not confined to Cardamine. Aucuba provides a direct timing manipulation in which complete gall induction that prevents seed production falls from 80.9% before 15 June to 8.8% after the host tissue window closes. Wise 2015 independently preserves experimentally shifted adult wheat-midge exposure timing to final seed damage/yield loss, while Wu 2015 links independently monitored adult occurrence × susceptible ear emergence to final yield loss across >400 cultivars. Cardamine adds ecotype-level phase-to-final-fate alignment, while Kula provides an independent mixed-system mechanistic sign reversal as a response-independent phase-safety margin crosses zero; Kula stops at predation rather than final plant fitness.

Equally important are explicit nulls and buffers. James shows a flowering-time signal at oviposition that disappears by realized cheater larval load. Posledovich shows host-stage matching that affects herbivore performance but not the mature-seedpod escape endpoint. Long-term Lathyrus shows a moving phenology-predation covariance that does not explain flowering-time selection on intact-seed fitness. Hemborg–Després Trollius shows a different transformation: early flowers on multi-flowered plants receive more oviposition and higher relative predation, yet the additional reproductive units buffer that cost so multi-flowered plants finish with higher annual seed output.

The confirmatory target is therefore signal propagation to final plant fitness, not the mere existence of a biologically plausible stage-specific timing mechanism.
