# IWE temporal signal-propagation audit

_Generated from data/registry/temporal_signal_components.csv; do not edit counts by hand._

## Scope

- Registered propagation links: **33**
- Studies: **29**
- Dependence clusters: **27**
- Links reaching a final plant-fitness endpoint: **30** from **26 studies**
- Final-fitness links with a directly comparable upstream/downstream direction: **29**

A propagation link is not an effect size. It records whether a source-backed timing signal is preserved, transformed, reversed, erased, buffered, or fails to track a downstream stage. Multiple links from one programme retain one dependence cluster.

## Transformation states

| Transformation | Links |
|---|---:|
| buffered | 6 |
| erased | 3 |
| preserved | 16 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 5 |
| tracking_inertia | 1 |

## Interaction classes

| Interaction type | Links |
|---|---:|
| antagonist | 16 |
| mixed_pollinating_seed_predator | 4 |
| mutualist | 13 |

## Provenance of the upstream temporal reference

| Window-reference class | Links |
|---|---:|
| direct_interaction_manipulation | 11 |
| independent_partner_activity | 7 |
| realized_interaction_window | 9 |
| seasonal_position_only | 6 |

## Transformations observed in chains that reach final plant fitness

| Transformation | Links |
|---|---:|
| buffered | 5 |
| erased | 2 |
| preserved | 16 |
| preserved_net_changed_mechanism | 1 |
| shifted_filtered | 1 |
| sign_reversed | 4 |
| tracking_inertia | 1 |

## Final-link transformations by interaction class

This matrix is descriptive for the targeted pilot corpus. It is not a literature-wide prevalence estimate.

| Interaction type | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| mutualist | 10 | 0 | 1 | 0 | 2 | 0 | 0 |
| antagonist | 6 | 1 | 3 | 2 | 2 | 1 | 0 |
| mixed_pollinating_seed_predator | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Final-link transformations by timing-reference provenance

This table is descriptive at the propagation-link level. IWE032 contributes two final-fitness links to the realized-interaction class, so these rows are not treated as independent studies.

| Timing reference | Preserved | Shifted / filtered | Sign reversed | Erased | Buffered | Tracking inertia | Net preserved, mechanism changed |
|---|---:|---:|---:|---:|---:|---:|---:|
| independent_partner_activity | 6 | 0 | 0 | 0 | 1 | 0 | 0 |
| direct_interaction_manipulation | 8 | 0 | 1 | 1 | 1 | 0 | 0 |
| realized_interaction_window | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| seasonal_position_only | 1 | 0 | 2 | 0 | 2 | 0 | 0 |

Prospectively defined timing references (independent partner activity or direct timing manipulation) are exact preserved in **14/18** final-fitness links. Among links whose upstream/downstream direction is directly comparable, they retain direction in **14/18**. Realized-interaction or seasonal-position references are exact preserved in **2/12** links; among direction-comparable links they retain direction in **3/11**.

The shifted-filtered IWE032 total-egg -> active-egg link is explicitly marked direction-incomparable and is not counted as a directional failure. Excluding all IWE032 direction-comparable realized/seasonal links changes direction retention from 3/11 to 2/10, while the prospective group remains 14/18.

This contrast is not an inferential prevalence estimate: the corpus is targeted, interaction class, endpoint, causal depth and study design are confounded, and some programmes contribute more than one propagation link. It motivates—but does not identify—a causal-depth hypothesis. In particular, the prospective category mixes independent adult monitoring with direct experimental timing manipulation.

## Antagonist-only dependence-cluster sensitivity

To reduce confounding by interaction class and repeated links, final-fitness links are also collapsed to one retention state per dependence cluster within antagonists.

| Antagonist timing provenance | Programmes | All direction-comparable final links retain direction | Mixed retention | No direction-comparable final link retains direction |
|---|---:|---:|---:|---:|
| prospective | 6 | 4 | 1 | 1 |
| realized_or_seasonal | 7 | 1 | 0 | 6 |

Within antagonists alone, prospective timing references yield **4/6 programmes with all direction-comparable final links retained**, 1 mixed, and 1 none-retained. Once direction-incomparable links are excluded from this binary summary, realized/seasonal references yield **1/7 all-retained**, 0 mixed, and 6 none-retained. This programme-level sensitivity removes the mutualist-class imbalance and collapses repeated links, while remaining descriptive rather than inferential.

## Antagonist-only exact-reference sensitivity

The prospective category still mixes observational adult monitoring with direct timing experiments. The same antagonist links are therefore split by their exact timing-reference class.

| Antagonist reference class | Programmes | All retained | Mixed | None retained |
|---|---:|---:|---:|---:|
| independent_partner_activity | 1 | 1 | 0 | 0 |
| direct_interaction_manipulation | 5 | 3 | 1 | 1 |
| realized_interaction_window | 5 | 1 | 0 | 4 |
| seasonal_position_only | 2 | 0 | 0 | 2 |

This split makes the design confounding explicit: independent adult monitoring and direct timing manipulations should not be interpreted as one biological causal-depth treatment. The table is a diagnostic for where confirmatory matched-design evidence is still missing.

## Interpretation

The current pilot falsifies the idea that a phenological effect can be represented by one invariant synchrony coefficient carried unchanged from encounter to fitness. Source-backed timing signals are observed to persist, reverse sign, be shifted by host/consumer filtering, disappear before the next consumer stage, be buffered by alternative ecological routes, or fail to track moving resources. In the current targeted mutualist set, five final-fitness links are classified as preserved: IWE001, IWE027, IWE029 and the two plant species in IWE005. IWE023 Mertensia is classified as buffered: visitation declines more than fivefold across flowering cohorts, but changing pollinator composition/effectiveness prevents a significant seed-set response across weeks. The two IWE005 links share one dependence cluster and are not two independent studies. Antagonist and mixed links occupy multiple additional transformation states. This class pattern is a hypothesis-generating contrast, not a prevalence estimate.

Positive downstream propagation is not confined to Cardamine. Aucuba provides a direct timing manipulation in which complete gall induction that prevents seed production falls from 80.9% before 15 June to 8.8% after the host tissue window closes. Wise 2015 independently preserves experimentally shifted adult wheat-midge exposure timing to final seed damage/yield loss, while Wu 2015 links independently monitored adult occurrence × susceptible ear emergence to final yield loss across >400 cultivars. Cardamine adds ecotype-level phase-to-final-fate alignment, while Kula provides an independent mixed-system mechanistic sign reversal as a response-independent phase-safety margin crosses zero; Kula stops at predation rather than final plant fitness.

Equally important are explicit nulls and buffers. Mertensia shows a prospective mutualist signal that is buffered: total visitation falls more than fivefold, but a shift toward more effective bumblebee visits leaves no significant seed-set difference across flowering weeks. Gols 2025 gives an independent prospective antagonist stress test within one experiment: herbivory timing is buffered before integrated reproductive potential in Sinapis arvensis but preserved in Brassica nigra. James shows a flowering-time signal at oviposition that disappears by realized cheater larval load. Posledovich shows host-stage matching that affects herbivore performance but not the mature-seedpod escape endpoint. Long-term Lathyrus shows a moving phenology-predation covariance that does not explain flowering-time selection on intact-seed fitness. Hemborg–Després Trollius shows a different transformation: early flowers on multi-flowered plants receive more oviposition and higher relative predation, yet the additional reproductive units buffer that cost so multi-flowered plants finish with higher annual seed output.

The confirmatory target is therefore signal propagation to final plant fitness, not the mere existence of a biologically plausible stage-specific timing mechanism.
