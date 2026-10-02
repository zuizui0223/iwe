# IWE pivot promotion gate

Date: 2026-10-02  
Applies to: `pivot/interaction-window-landscape`  
Status: prospective gate for deciding whether the pivot should replace or only supplement the original strict-H1 framing.

## Central candidate principle

The pivot is not promoted merely because signed flowering-time selection differs among studies.

The stronger ecological hypothesis is:

> Biotic interactions may look idiosyncratic on an absolute calendar axis, but become more predictable when plant phenology is expressed relative to the effective interaction window.

The proposed geometry is:

- mutualist: selection/fitness tends to pull plant timing toward an effective service window;
- antagonist: selection/fitness tends to favor temporal escape from an effective cost window;
- mixed pollinating seed predator: benefit and cost windows can overlap imperfectly, producing displacement, asymmetry, or curvature in net fitness.

Calendar early/late is therefore a diagnostic coordinate, not the final generalizing coordinate.

## Why this gate is needed

The pilot already contains opposite calendar signs within the antagonist class:

- Gentiana–Phengaris shifts selection toward later flowering;
- Gymnadenia herbivory shifts selection toward earlier flowering;
- Lythrum simulated damage shifts selection toward earlier flowering.

It also contains coordinate-specific mutualist effects in Arabidopsis, where pollinators affect flowering start and flowering end differently.

These results are sufficient to reject a naive universal calendar-direction rule, but they do not yet prove convergence after window alignment.

## Promotion tests

### P1 — complete signed-search universe before class-level claims

The Caruso 2019 non-duplicated flowering-phenology treatment-pair universe must be screened with the signed-rescreen contract before a general statement about the frequency or direction of agent-induced selection shifts.

All eligible contrasts are retained, including nulls and sign patterns that contradict the pivot.

The duplicated Caruso workbook is dependence-audit material only.

### P2 — preserve phenology coordinates

Flowering start, peak, end, duration, and other phenology coordinates are not pooled merely because all can be oriented as early versus late.

A common quantitative pool requires a biologically homologous coordinate or an explicit multivariate/hierarchical model.

### P3 — window provenance remains explicit

Every programme used for the window-relative test is assigned one of the existing window-reference classes:

- independent_partner_activity;
- realized_interaction_window;
- historical_partner_window;
- seasonal_position_only;
- direct_interaction_manipulation.

Only the first class can by itself support a claim about independently identified partner availability.

### P4 — direct alignment test

The key confirmatory comparison is not whether calendar signs differ.

For programmes with sufficient timing data, fit or reconstruct effects on:

1. an absolute calendar/seasonal timing coordinate;
2. a relative raw partner-exposure coordinate where adult activity is independently identified;
3. an **effective interaction-window coordinate** when host-stage filtering or interaction success changes which exposure events actually contribute to final reproduction.

Then ask whether biologically relevant between-programme heterogeneity is reduced by raw partner-window alignment and whether it is reduced further by effective-window alignment.

The Cardamine source now demonstrates why these are not interchangeable: the Gaussian peak for total egg exposure occurs at flowering-date z = -1.10, while the peak for active eggs capable of reaching damaging late instars occurs at z = -0.61 and has a narrower sigma (0.66 versus 0.92). An independent Portuguese Gentiana-Phengaris programme additionally shows that offspring survival varies with host bud size, bud developmental stage, and oviposition period, while Yucca-Tegeticula provides a taxonomically distinct filter in which resource-driven flower abortion kills all eggs in exposed flowers. These replicate host-state filtering at the mechanism level but do not yet test final plant-fitness convergence.

No claim of "collapse", "convergence", or "effective-window superiority" is allowed without paired comparisons across independent programmes.

### P5 — effective windows cannot be defined circularly

An effective interaction window may be estimated from a pre-fitness mechanistic filter such as stage-specific attack survival, successful pollen transfer, or experimentally identified host sensitivity.

It may **not** be defined by choosing the timing transformation that maximizes the final fitness association in the same data.

Whenever possible, the filter defining the effective window must be estimated independently of the final reproductive response or validated in a separate component of the study.

### P6 — mixed systems remain a distinct geometry test

Mixed pollinating seed predators are not forced into the mutualist or antagonist sign rule.

Where benefit and cost channels can be separated, preserve:

`W_net(tau) = B(tau) - C(tau)`.

A mixed-system result is informative if the net optimum is displaced from the partner-activity maximum or if benefit and cost surfaces peak at different relative times.

### P7 — null and boundary systems are mandatory

The evidence map must retain systems in which:

- interaction manipulation changes fitness but not flowering-time selection;
- antagonist damage does not alter selection;
- pollination changes non-phenological traits but not phenology;
- timing effects exist without a defensible interaction window.

These are not failed studies. They are necessary tests of whether the proposed window rule is selective rather than tautological.

### P8 — dependence and uncertainty are not relaxed

Repeated years, sites, traits, or contrasts from one programme share the appropriate dependence cluster.

A signed contrast without defensible SE/covariance can be reported with its source interaction test or interval, but cannot be made inverse-variance-ready by assuming zero covariance.

The existing CR2 minimum-information rule remains the inferential gate for any pooled class estimate.

## Branch decision rule

### Promote the pivot toward the main IWE paper if

the expanded signed evidence continues to show substantial calendar-sign/coordinate heterogeneity **and** multiple independently replicated programmes with identifiable interaction windows support a more coherent window-relative interpretation.

### Retain as a secondary analysis if

signed selection shifts are common but too few studies identify the interaction window to test whether re-alignment explains the heterogeneity.

### Abandon as the main framing if

the broader outcome-complete rescreen shows that the apparent calendar-sign heterogeneity was a pilot artifact, or if window alignment does not improve biological interpretability beyond generic seasonal timing.

## Immediate empirical priorities

1. complete IWE002 directional reconstruction without counting it as independent from IWE001;
2. resolve IWE015 raw variance for the mixed net-fitness anchor;
3. recover IWE032 female-flight dates and fit its early/core/late antagonist surface, then compare raw female-flight alignment with the already reconstructed active-egg effective window;
4. Cardamine now closes one prospectively defined effective-window filter to final plant reproduction through the source fitness equation. Geum-Byturus independently links a realized antagonist window to final plant fitness and shows an interior escape optimum at 36% second-peak flowering, while host-filter mechanism breadth has two additional replications (Portuguese Gentiana-Phengaris and Yucca-Tegeticula). The remaining stronger gate is an **independent second programme** that explicitly separates raw exposure from a pre-fitness effective-window filter and then links that filtered window to final plant reproduction;
5. ingest and screen the Caruso non-duplicated phenology treatment-pair database when lawful file access is available;
6. add design-matched null/boundary systems, including published cases where antagonist damage did not alter flowering-time selection.

This gate deliberately makes the hardest claim — window-relative convergence — contingent on data that have not yet been inspected under that comparison.
