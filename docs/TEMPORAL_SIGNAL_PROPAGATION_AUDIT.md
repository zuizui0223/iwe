# IWE temporal signal-propagation audit

_Generated from data/registry/temporal_signal_components.csv; do not edit counts by hand._

## Scope

- Registered propagation links: **19**
- Studies: **18**
- Dependence clusters: **18**
- Links reaching a final plant-fitness endpoint: **16** from **15 studies**

A propagation link is not an effect size. It records whether a source-backed timing signal is preserved, transformed, reversed, erased, buffered, or fails to track a downstream stage. Multiple links from one programme retain one dependence cluster.

## Transformation states

| Transformation | Links |
|---|---:|
| buffered | 3 |
| erased | 3 |
| preserved | 8 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 2 |
| tracking_inertia | 1 |

## Interaction classes

| Interaction type | Links |
|---|---:|
| antagonist | 11 |
| mixed_pollinating_seed_predator | 4 |
| mutualist | 4 |

## Provenance of the upstream temporal reference

| Window-reference class | Links |
|---|---:|
| direct_interaction_manipulation | 3 |
| independent_partner_activity | 5 |
| realized_interaction_window | 9 |
| seasonal_position_only | 2 |

## Transformations observed in chains that reach final plant fitness

| Transformation | Links |
|---|---:|
| buffered | 2 |
| erased | 2 |
| preserved | 8 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 1 |
| tracking_inertia | 1 |

## Final-link transformations by interaction class

This matrix is descriptive for the targeted pilot corpus. It is not a literature-wide prevalence estimate.

| Interaction type | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| mutualist | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| antagonist | 4 | 1 | 1 | 2 | 1 | 1 | 0 |
| mixed_pollinating_seed_predator | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Final-link transformations by timing-reference provenance

This table is descriptive at the propagation-link level. IWE032 contributes two final-fitness links to the realized-interaction class, so these rows are not treated as independent studies.

| Timing reference | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| independent_partner_activity | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| direct_interaction_manipulation | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| realized_interaction_window | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| seasonal_position_only | 0 | 0 | 0 | 0 | 1 | 0 | 0 |

Prospectively defined timing references (independent partner activity or direct timing manipulation) retain the signal direction in **7/8** final-fitness links (7/8 are exact preserved). Realized-interaction or seasonal-position references retain direction in **2/8** links (1/8 exact preserved).

The descriptive contrast is not driven by the duplicated Cardamine dependence cluster. If either of the two IWE032 final-fitness links is removed, direction retention in the realized/seasonal group is 1/7 or 2/7, while the prospective group remains 7/8.

This contrast is not an inferential prevalence estimate: the corpus is targeted, interaction class and timing provenance are confounded, and some programmes contribute more than one propagation link. It is a source-backed diagnostic supporting the next hypothesis that temporal signals are most stable when timing is defined prospectively at or near the biologically effective interaction stage.

## Antagonist-only dependence-cluster sensitivity

To reduce confounding by interaction class and repeated links, final-fitness links are also collapsed to one retention state per dependence cluster within antagonists.

| Antagonist timing provenance | Programmes | All final links retain direction | Mixed retention | No final link retains direction |
|---|---:|---:|---:|---:|
| prospective | 4 | 3 | 0 | 1 |
| realized_or_seasonal | 5 | 0 | 1 | 4 |

Within antagonists alone, prospective timing references yield **3/4 programmes with all final links direction-retaining** and 1/4 with none. Realized/seasonal references yield **0/5 all-retained**, 1/5 mixed (Cardamine), and 4/5 none-retained.

This programme-level sensitivity removes the mutualist-class imbalance and collapses the duplicated Cardamine final links. It remains descriptive rather than inferential because the targeted programmes differ in endpoint and study design.

## Interpretation

The current pilot falsifies the idea that a phenological effect can be represented by one invariant synchrony coefficient carried unchanged from encounter to fitness. Source-backed timing signals are observed to persist, reverse sign, be shifted by host/consumer filtering, disappear before the next consumer stage, be buffered by alternative ecological routes, or fail to track moving resources. In the current targeted set, all four mutualist service-window links that reach final plant fitness are classified as preserved, whereas antagonist and mixed links occupy multiple transformation states. This class pattern is a hypothesis-generating contrast, not a prevalence estimate.

Positive downstream propagation is not confined to Cardamine. Aucuba provides a direct timing manipulation in which complete gall induction that prevents seed production falls from 80.9% before 15 June to 8.8% after the host tissue window closes. Wise 2015 independently preserves experimentally shifted adult wheat-midge exposure timing to final seed damage/yield loss, while Wu 2015 links independently monitored adult occurrence × susceptible ear emergence to final yield loss across >400 cultivars. Cardamine adds ecotype-level phase-to-final-fate alignment, while Kula provides an independent mixed-system mechanistic sign reversal as a response-independent phase-safety margin crosses zero; Kula stops at predation rather than final plant fitness.

Equally important are explicit nulls and buffers. James shows a flowering-time signal at oviposition that disappears by realized cheater larval load. Posledovich shows host-stage matching that affects herbivore performance but not the mature-seedpod escape endpoint. Long-term Lathyrus shows a moving phenology-predation covariance that does not explain flowering-time selection on intact-seed fitness. Hemborg–Després Trollius shows a different transformation: early flowers on multi-flowered plants receive more oviposition and higher relative predation, yet the additional reproductive units buffer that cost so multi-flowered plants finish with higher annual seed output.

The confirmatory target is therefore signal propagation to final plant fitness, not the mere existence of a biologically plausible stage-specific timing mechanism.
