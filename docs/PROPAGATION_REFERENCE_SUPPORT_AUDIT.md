# IWE timing-reference support / positivity audit

_Generated from temporal_signal_components.csv and propagation_endpoint_audit.csv._

## Strict observed mature-seed/yield endpoint

- Direction-comparable links: **18**
- Distinct dependence clusters across these links: **14**

| Interaction class | Timing reference | Links | Clusters | Direction retained |
|---|---|---:|---:|---:|
| mutualist | independent_partner_activity | 6 | 5 | 5 |
| mutualist | direct_interaction_manipulation | 5 | 3 | 4 |
| mutualist | realized_interaction_window | 0 | 0 | 0 |
| mutualist | seasonal_position_only | 2 | 2 | 1 |
| antagonist | independent_partner_activity | 1 | 1 | 1 |
| antagonist | direct_interaction_manipulation | 2 | 2 | 2 |
| antagonist | realized_interaction_window | 1 | 1 | 0 |
| antagonist | seasonal_position_only | 0 | 0 | 0 |
| mixed_pollinating_seed_predator | independent_partner_activity | 0 | 0 | 0 |
| mixed_pollinating_seed_predator | direct_interaction_manipulation | 0 | 0 | 0 |
| mixed_pollinating_seed_predator | realized_interaction_window | 0 | 0 | 0 |
| mixed_pollinating_seed_predator | seasonal_position_only | 1 | 1 | 0 |

## Within-programme cross-reference support

For this diagnostic, a cross-reference programme must contain at least one independent-partner/direct-manipulation link and one realized/seasonal link with the **same** dependence ID. This is only a necessary coverage condition, never sufficient for a paired prediction comparison.

- Strict mature-seed/yield cross-family programmes: **0**
- All direction-comparable final endpoints (different endpoint types kept separate for inference): **0** cross-family programmes among **29** links

## What can and cannot be concluded

- The existing preservation proportions compare **different programmes, methods and biological endpoints**, not two timings observed on the same study units.
- A zero stratum is missing support, **not** an observed failure of preservation. Repeated rows from one dependence cluster are not independent replications.
- Direct experimental timing manipulations and direct adult-activity monitoring are distinct designs. Neither should be called a measured effective consumer stage without that stage actually being observed.
- Even a positive cross-reference count would not prove paired model superiority: same endpoint, same units, pre-outcome filters, response-blind model selection and genuinely held-out predictions are still required.
- These tables are diagnostic for the **targeted, outcome-aware pilot corpus**, not a population prevalence estimate, causal effect or eligible strict-H1 meta-analysis.

**Decision:** Do not infer a general advantage of downstream or prospective timing from cross-programme direction-retention percentages. Keep the conversion-bottleneck hypothesis exploratory until a genuine same-unit paired comparison passes the prospective gate.
