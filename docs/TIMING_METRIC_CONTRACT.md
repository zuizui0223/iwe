# Timing metric contract

Date: 2026-09-16
Status: frozen before extraction beyond IWE001; executable schema wired 2026-09-21

## Why this contract exists

Phenological studies use several non-equivalent timing variables. A signed lag can distinguish whether the plant or its partner is early, whereas an absolute mismatch collapses the two directions. Experimental flowering-date treatments may not measure partner phenology directly. A generic rule of multiplying every variable called `mismatch` by -1 is therefore insufficient for quantitative synthesis.

IWE will preserve the native timing definition before any orientation or pooling.

## Executable fields

The extraction table carries three timing-contract fields that are validated before any primary dataset is built:

- `timing_metric_type` — the native mathematical/biological timing definition;
- `timing_analysis_class` — whether the effect is admissible to the strict synchrony estimand or belongs to a sensitivity/directional/unresolved/proxy path;
- `timing_domain` — the observed or design domain needed to interpret direction relative to matching.

The registered `timing_analysis_class` values are:

- `strict_window` — eligible for the strict H1 synchrony dataset if all other validation rules pass;
- `direct_timing_sensitivity` — direct seasonal/timing effect without sufficient partner-window information for strict synchrony;
- `directional_mismatch` — a separately estimated one-sided signed-lag response;
- `unresolved_for_strict_h1` — the native effect is extractable, but the information required to orient it as synchrony is not yet demonstrated;
- `proxy_only` — Tier-C occurrence-derived timing evidence.

The registered `timing_domain` values are `nonnegative`, `plant_earlier_only`, `partner_earlier_only`, `both_sides`, `ordered_by_measured_window`, `unknown`, and `not_applicable`.

`build_primary_dataset()` admits only rows with `evidence_tier == "A"` and `timing_analysis_class == "strict_window"`. Thus a scientifically useful Tier-A extraction may remain outside the strict H1 estimand until its orientation contract is satisfied.

## Canonical timing classes

Every extracted Tier-A effect must be assigned one `timing_metric_type`:

- `overlap_index` — larger native values mean greater temporal overlap by construction;
- `absolute_mismatch` — non-negative distance from temporal matching, irrespective of which partner is earlier;
- `plant_minus_partner` — signed plant timing minus partner timing;
- `partner_minus_plant` — signed partner timing minus plant timing;
- `experimental_plant_shift` — experimental early/late plant timing without a directly measured partner-timing variable;
- `seasonal_position` — observational early/late position in a season, used only when contemporaneous partner availability is measured sufficiently to interpret the contrast;
- `other_registered` — allowed only after a source-specific definition is documented in an extraction receipt.

## Required source definition

For every real effect, the extraction receipt must state:

1. the biological events being compared (for example flowering onset and first queen-bee detection, or flowering peak and pollinator-abundance peak);
2. the source equation or verbal definition of the timing metric;
3. which sign corresponds to plant earlier, exact matching, and partner earlier;
4. whether the metric is signed or absolute;
5. whether the effect is based on observed partner activity, a timing manipulation, or a proxy;
6. the analyzed timing domain when strict H1 orientation depends on a one-sided restriction.

Source terminology is retained even when it conflicts with terminology in another paper.

## Canonical lag

For signed timing analyses IWE defines an optional canonical lag

`lag_PP = plant_timing - partner_timing`.

Therefore:

- `lag_PP < 0`: the plant is earlier than the partner;
- `lag_PP = 0`: matched focal timing;
- `lag_PP > 0`: the plant is later than the partner.

A source using `partner_timing - plant_timing` must be multiplied by -1 before being represented as `lag_PP`.

`lag_PP` is **not** itself a synchrony score. Moving from -7 to -3 days is greater synchrony, whereas moving from +3 to +7 days is lower synchrony. Consequently, a single linear coefficient on signed lag cannot in general be re-labelled as an effect of synchrony.

## Primary H1 synchrony estimand

For the primary H1 analysis, an effect may be oriented as `greater synchrony -> plant reproductive performance` only when one of the following is justified:

### A. Explicit overlap

The source uses an overlap metric whose biological direction is known. No sign transformation is needed if larger means more overlap.

Executable rule: `timing_metric_type = overlap_index`, `timing_analysis_class = strict_window`, and `exposure_direction = synchrony`.

### B. Absolute mismatch

The source uses `|plant_timing - partner_timing|` or another non-negative mismatch magnitude. The effect is multiplied by -1 so that larger oriented effects correspond to greater synchrony.

Executable rule: `timing_metric_type = absolute_mismatch`, `timing_domain = nonnegative`, `timing_analysis_class = strict_window`, and `exposure_direction = mismatch`.

### C. One-sided mismatch domain

All observations used for the effect lie on one declared side of matching, and the source biology supports monotonic movement toward or away from zero. Example: flowering always occurs on or before bee emergence, so an increase in `plant - bee` from -7 to 0 is an increase in synchrony.

The extraction receipt must show that the one-sided restriction is true for the analyzed rows. Signed `plant_minus_partner` or `partner_minus_plant` rows cannot use `strict_window` with `timing_domain = unknown` or `both_sides`; validation fails closed.

For signed metrics, `exposure_direction` is also checked against the metric convention and declared side. For example, `partner_minus_plant` on `plant_earlier_only` must be `mismatch`, while `plant_minus_partner` on the same domain must be `synchrony`.

### D. Experimental timing contrast with a measured interaction window

An experimental plant-timing treatment may enter H1 if partner availability across treatments is measured and the treatment can be ordered prospectively as more versus less matched. The contrast must be based on that order, not simply on `late > early`.

Executable strict-window rows using `experimental_plant_shift` or `seasonal_position` require `timing_domain = ordered_by_measured_window`.

## Directional mismatch is a separate estimand

When data span both sides of matching, IWE will not force them into one linear synchrony slope. Instead, where data permit, estimate directional responses separately:

- `plant_earlier_mismatch`: `lag_PP < 0`;
- `partner_earlier_mismatch`: `lag_PP > 0`.

These rows use `timing_analysis_class = directional_mismatch` and must themselves be one-sided.

This supports a predeclared directional-mismatch analysis motivated by systems in which the two mismatch directions have asymmetric reproductive effects. The 2024 Qilian alpine-community study is an example where pollinator-earlier and flower-earlier mismatch patterns were reported to differ in fecundity impact.

Directional mismatch is a moderator/shape analysis, not a replacement for H1.

## Experimental flowering-time studies

Studies that manipulate flowering date but do not directly quantify a partner timing curve remain scientifically useful, but they are not automatically strict synchrony effects.

They are classified as:

- `strict_window` if contemporaneous partner availability allows treatments to be ordered by matching;
- `direct_timing_sensitivity` if flowering time is experimentally changed and reproductive output is measured but the partner window is not explicitly recoverable.

The latter may enter a predeclared sensitivity analysis and may support statements about seasonal timing effects, but not the strict claim that phenological synchrony caused the response.

## IWE001 source-specific convention

Kudo & Ida (2013) Appendix A reports `Mismatch day` as bumblebee first-detection date minus flowering-onset date. Thus its native sign is `partner_minus_plant`:

- positive: plant flowers before bee detection;
- zero: matching onset/detection;
- negative: bee detection precedes flowering.

A row-level audit of the actual annual values used in the three site correlations shows that **NFP, TOEF, and JOZ all span both sides of zero**. The native whole-site effects are therefore registered as:

- `timing_metric_type = partner_minus_plant`;
- `timing_analysis_class = unresolved_for_strict_h1`;
- `timing_domain = both_sides`.

This is a resolved exclusion from the strict synchrony estimand, not a pending documentation gap. A whole-site signed correlation cannot be promoted to `strict_window` by any sign transformation. A separate one-sided directional re-extraction is allowed where the annual data provide enough observations.

## IWE002 source-specific adjudication

Kudo & Cooper (2019) defines mismatch as

`flowering onset - bee emergence`,

i.e. `plant_minus_partner`, the opposite native algebraic sign from IWE001. Negative values mean flowering occurred before bee emergence.

The long-term component uses the Nopporo population from 1999–2017. This extends the Nopporo/NFP series used in IWE001 rather than providing an independent biological replication. Any later IWE002 extraction from this series must therefore share a Corydalis/Nopporo dependence cluster with the overlapping IWE001 evidence.

The paper's experimental individual-level mismatch spans `-9` to `+11` days, so the pooled mismatch slope is explicitly two-sided. It cannot be relabelled as a strict synchrony slope.

The snow-removal manipulation also cannot be represented as one universally ordered `strict_window` contrast across years: controls flowered after bee emergence in 2014, 2015 and 2017 and concurrently in 2016, whereas removal plots flowered concurrently in 2014–2015 and before bee emergence in 2016. The same treatment therefore moved plants toward matching in some years and through/past matching in another.

Accordingly, no whole-series or pooled-treatment IWE002 effect is admitted to `direct_effects.csv` as strict H1 evidence. Valid future routes are:

- a source-backed one-sided directional mismatch extraction;
- a year-specific experimental contrast ordered prospectively by distance from the measured bee-emergence window; or
- a non-strict `direct_timing_sensitivity` effect if only the treatment response, rather than a matching contrast, is recoverable.

See `EXTRACTION_IWE002.md` and `CORYDALIS_DEPENDENCY_MAP.md`.

## IWE004 source-specific adjudication

Kehrberger & Holzschuh (2019) uses Julian date of bud opening as the focal seasonal timing variable. Bee abundance and pollinator-suitable hours increased over the season, whereas visitation and estimated total bee visits to *Pulsatilla vulgaris* decreased as co-flowering competition increased and floral longevity shortened.

Calendar date therefore does not provide a monotonic axis of plant–pollinator synchrony in this study.

The registered component is:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = direct_timing_sensitivity`;
- `timing_domain = not_applicable`.

Recovering the raw Julian-date slope from Dryad would make the timing-sensitivity effect quantitative, but would not make it strict H1 evidence.

## IWE011 source-specific adjudication

Kudo & Shibata (2025) directly records final intact-fruit production across five permanent *Peucedanum multivittatum* plots along a flowering gradient. The predator moth *Phaulernis fulviguttella* concentrates oviposition in mid- to late July.

For the predeclared extreme contrast:

- HA flowers in mid-July and represents the high predator-overlap end;
- HD flowers in early to late August and represents the low predator-overlap end.

The exposure is therefore registered as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

The final intact-fruit-set contrast is reconstructed from published Table 1 as Hedges' `g = -1.1368391965` for high overlap minus low overlap. The negative sign means greater antagonist synchrony is associated with lower final reproductive performance.

This is observational across permanent plots, not an experimental manipulation of synchrony. See `EXTRACTION_IWE011.md` and `PEUCEDANUM_DEPENDENCY_MAP.md`.

## IWE015 source-specific adjudication

Zhou et al. (2020) explicitly conducts early and late experiments in two measured partner-activity windows:

- early = *Hadena ectypa*-dominant, corresponding to the adult activity peak of the mixed pollinating seed predator;
- late = co-pollinator-dominant, after *H. ectypa* activity drops.

The final female-fitness measure is the number of successful fruits, defined as initiated fruits that escape *H. ectypa* predation.

The 2012 and 2013 contrasts are therefore registered as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

Each effect is high focal-partner overlap (early) minus low focal-partner overlap (late). The source reports mean ± SE and n, so IWE reconstructs SD as `SE * sqrt(n)` before calculating Hedges g.

Both year effects share one dependence cluster, `DEP_SILENE_STELLATA_HADENA_MLBS`.

See `EXTRACTION_IWE015.md`.

## IWE023 source-specific adjudication

Gallagher & Campbell (2020) experimentally shifted *Mertensia ciliata* flowering onset into four weekly cohorts in 2015 while directly observing the same-season pollinator community during each cohort.

The partner-availability ordering is fixed independently of seed set:

- week 1 has the higher-availability window;
- week 4 has the lower-availability window;
- measured visitation is more than fivefold higher in week 1 than week 4.

The week-1 versus week-4 seed-set contrast is therefore registered as:

- `timing_metric_type = experimental_plant_shift`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

The order is based on contemporaneous observed visitation, not on calendar date or on the seed-set result. The final seed-set SMD is reconstructed separately from the reported balanced-group means and ANOVA residual variance.

All IWE023 evidence uses `DEP_MERTENSIA_GALLAGHER_CAMPBELL_RMBL`. See `EXTRACTION_IWE023.md`.

## IWE027 source-specific adjudication

Kameyama & Kudo (2009) measures both flowering timing and bumble-bee seasonal activity in 2007. Early to mid-July has very low queen visitation; worker bees appear in late July and visit frequency then rises abruptly and remains high.

For the 2007 E-to-M contrasts at HIS and GOS:

- E = lower-overlap early seasonal window;
- M = higher-overlap worker-bee seasonal window.

The extracted intact natural seed-set effects use:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

Only 2007 is admitted. The 2006 seed-set summaries are not promoted to strict H1 because partner activity was not directly measured that year.

Both 2007 site effects share `DEP_IWE027_TAISETSU_2007`. See `EXTRACTION_IWE027.md`.

## IWE029 source-specific adjudication

Carneiro & Machado (2025) sampled *Stigmaphyllon paralias* during two within-season windows chosen after monitoring pollinator activity:

- peak flowering with scarce legitimate oil-bee visitation;
- late flowering 3–4 weeks later with high pollinator activity.

Measured visit marks occurred on 7.5% of peak flowers versus 93.6% of late flowers. The two-level seasonal exposure is therefore independently ordered by a measured partner-activity window.

The natural-pollination seed-set contrast is registered as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

The published binomial model coefficient for late versus peak natural-pollination seed set is extracted as `log_odds_ratio = 1.55`, with `SE = 0.25`.

See `EXTRACTION_IWE029.md` for the coefficient-direction audit and effect-family boundary.

## Claim boundary

IWE will never treat:

- signed lag as absolute synchrony without checking its domain;
- `early` or `late` as inherently good/bad or matched/mismatched;
- calendar date as partner synchrony unless partner availability is measured;
- first detection, peak abundance and full activity overlap as interchangeable timing events;
- occurrence-derived phenology as direct interaction timing.

A study can remain `unresolved_for_strict_h1` or move to a timing-sensitivity analysis if its timing definition cannot support the strict H1 estimand. That is preferable to changing the estimand after seeing the result.
