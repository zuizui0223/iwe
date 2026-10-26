# IWE: Which biological clock retains information about final reproduction?

**Date:** 2026-10-19
**Status:** exploratory, cross-programme evidence synthesis. **Not a new meta-analysis** or an updated strict-H1 claim. All source programmes retain their original dependence units, endpoints, and temporal-reference provenance.

## Central ecological question

> When does the timing of a plant–animal encounter predict the plant's subsequent reproductive performance, and when does the temporal signal become buffered, reversed, or lost before the reproductive endpoint?

A simple notion of "synchrony" conflates at least three different clocks:

1. **Calendar/plant state:** season, year, first flowering date, or flowering intensity.
2. **Effective service or exposure:** the dates when a suitable partner is active **AND** flowers/reproductive tissue are receptive or vulnerable.
3. **Conversion/fate:** how that exposure is translated into effective pollination, consumer survival, tissue abortion/retention, and finally intact seed production.

Biological hierarchy is **not** a claim that every downstream variable must outperform every upstream variable. It predicts **conditional propagation**, potentially erased by host compensation, consumer mortality, partner substitution, or other reproductive constraints.

## Two genuinely new original-data sensitivity tests

| Dimension | 2025 Acer saccharum original data | 2023 three plants × Osmia lignaria original data |
|---|---|---|
| DOI | 10.5281/zenodo.15090572 | 10.5281/zenodo.7264150 |
| Source grain | 2012–17 **six annual exposure years** at one forest | 2021 **eight experimental arenas**, three host species, one bee; 181 strictly source-complete plants |
| Earlier state predictor | Spring qualitative flowering intensity (0–3, 20 trees per year) | Plant first flowering DOY, dated open-flower counts |
| Partner-time predictor | **Absent** (no independently observed annual pollinator or antagonist availability curve) | Independently observed arena-day Osmia density; dated open-flower-count-weighted density |
| Downstream response | Intact filled / classified **harvested samaras**; not maternal annual total intact seed output | Mature seeds / (seeds + undeveloped ovules) in sampled fruits; not maternal lifetime reproduction |
| Simple falsifier | Known odd/even **alternate-bearing calendar** | Adult mean bee density, first flowering day, mean observed-day flowering date and census-day coverage |
| Exact validation | Leave-one-**year**-out; six years, no extra forest | Leave-one-**arena**-out; eight arenas and common plant set |
| Direction/result | Spring RMSE **0.1002**, but simpler alternate-bearing **0.0815** — distinct spring predictive value **not supported** | Bloom×bee RMSE **0.20605** vs first-flower calendar **0.21021** and adult mean **0.22138** — **small positive exploratory signal** |
| Design/robustness | n=6, Spearman spring/intact +0.829, exact 2-sided label permutation **p=0.0583**; tree/seed weighting and missing samaras sensitive | Only **4/8** arenas better than first flowering; true phase ranks **2/23** among cyclic census-index shifts, 51.2% bloom observation covered, matched 228-record partial-fruit scenario retains small advantage |
| Strict IWE H1 class effect | **Zero new clusters** | **Zero new clusters** |

### Third analysis, same maple programme: a different endpoint changes the clock ranking

PR [#101](https://github.com/zuizui0223/iwe/pull/101) recovered and tested **2012–2024** spring tree flowering against standardized **30-second autumn seed counts** at matched tree × year grain: **259 paired tree-years across 13 years** in **the same Harvard Forest programme**. This is NOT an independent new plant–animal interaction programme, nor an independently validated intact/viable-seed fitness endpoint. The 2012–2017 samara-classification analysis above is a distinct sampling frame/outcome and should not be numerically merged with these annual seed counts.

| Same maple programme, different sampled output | Validation / denominator | Spring-only RMSE | Simpler odd/even calendar RMSE | Legitimate inference |
|---|---|---:|---:|---|
| **2012–2017** fraction of *classified harvested samaras* with intact filled seed | 6 years, leave-year-out; year-aggregated rates | 0.1002 | **0.0815** | Spring category does **not** outperform alternate-bearing calendar for this **conditional harvested-seed fraction** |
| **2012–2024** log1p(standardized autumn *seed count*) | 259 tree-years, 13 held-out annual blocks | **1.2941** | 1.4630 | Individual spring **flowering effort** predicts later *sampled seed rain* better than parity in this source |
| **Actively flowering restriction** of above autumn count response | 179 tree-years across 10 seasonal blocks, bloom-positive plants and years | **1.5498** | 1.6796 | Spring signal is not only a trivial absence-of-flowers versus absence-of-seeds result; the restriction was nevertheless constructed in this retrospective analysis |

Additional diagnostics in [the exact long-term original source audit](MAPLE_LONGTERM_TEMPORAL_GRAIN_2012_2024.md): for 179 actively flowering tree-years, adding the *other 19 trees' spring mean* to focal spring reduces leave-year-out RMSE **1.5498 → 1.5002** (about **3.2%**, modest and not a demonstrated pollination-synchrony effect). A fixed historical 2012–2017 fit applied to later actively flowering years 2019–2021/2023 (76 tree-years) gives focal flowering alone **1.5140**, focal+other trees **1.5007**, focal+previous autumn count **1.4401**. The source records no independent adult availability, consumer-stage clock, or direct viable seed output per tree.

**Scientific consequence:** The statement "spring phenology adds no information beyond a two-year clock" would be **false across reproductive endpoints**. The narrower and correct finding is: an earlier plant-state indicator can contain distinct information about *sampled seed production*, but may not improve prediction of the *fraction of sampled seeds that survive intact*. This is a potentially useful **quantity-versus-quality propagation contrast**, but it does not establish a causal conversion bottleneck: the endpoints come from different sampling programmes/years and do not trace the same tagged reproductive units. Treat all three panels above as **one dependence programme** with different observational outputs, not three independent tests.

These are **different estimands and different temporal scales** and their RMSE values must never be pooled or used as direct evidence that one biological system has a stronger effect. Their joint contribution is a **methodologically explicit ecological falsification principle**: a biologically richer time reference must beat plausible simpler clocks before it can be claimed to add reproductive information.

Frozen original-source audits:
- [Harvard maple](CRONE2025_SPRING_TO_SEED_CONVERSION.md), merged by IWE PRs #98/#100.
- [Three plant species × Osmia](DEMANINCOR2023_THREE_SPECIES_SERVICE_WINDOW.md), merged by PR #102.

## Separate 2022 cohort: high observed synchrony need not carry reproductive information

A second greenhouse experiment from the **same de Manincor/Fisogni/Rafferty group and identical three plants + Osmia pollinator** was published in 2026 (Global Change Biology, DOI 10.1111/gcb.71074; original public data Zenodo 10.5281/zenodo.17830772). It is a **different year/cohort**, not a new independent taxon-level programme. The authors found that warming preserved phenological synchrony but reduced interactions and multiple reproductive success components. Our source-level original-data reanalysis adds a prospective-in-measurement-order, yet outcome-exposed, paired calendar/bee-window comparison.

**Exact source units:** 208 fruit records (120 plant-prefix group IDs), within 60 **room × arena × species** units in 20 real arenas. All F1 germination/cotyledon outcomes come from **six seeds per group**, totalling **360** measured seeds; the group values are repeated across 208 fruit rows, not 208 independent F1 trials. Original 2022 seed/ovule raw counts close for all 208 fruit rows but their derived `seed_set` is inconsistent on **31/208**; the IWE response is recomputed from the original seed and ovule counts. Daily bee census covers **96.4%** of observed flowering on average on same days.

| Distinct stage (same 60 original source groups) | Leave-one-arena-out calendar model RMSE | Bloom-weighted same-day bee exposure RMSE |
|---|---:|---:|
| Sampled-fruit seed fraction | **0.13719** | 0.14010 |
| F1 germination / six sown | **0.19683** | 0.20968 |
| F1 cotyledon survival / six sown | **0.22184** | 0.23882 |

In *20 within-room arena holdouts*, bloom×bee exposure alone **does not** beat the flowering calendar at any of these stage outputs (better in 8/20, 6/20, 7/20 arenas respectively). This is an empirically grounded counterexample to **guaranteed predictive benefit** from a better measured synchrony window.

A **four-room-out extrapolation**, necessarily omitting any held-out room categorical term, gives a different answer for sampled fruits: bloom×bee RMSE **0.19255**, versus calendar **0.21096** and adult mean **0.19810**. Yet it still worsens F1 germination (0.25877 vs calendar 0.23607) and cotyledon survival (0.26621 vs 0.23882). Each treatment has **only one physical room**; these four folds are a stringent domain shift, *not* independently randomized warming-treatment replications. Predictor ranking is thus **sensitive to the validation scale and the reproductive endpoint**, as expected under a conditional information-conversion hypothesis.

The authors' 2021 cohort showed a small within-arena positive for sampled fruit seed fraction, but different source endpoints, room protocols, sampling windows and validation groups make a formal "2021 positive / 2022 negative" effect-size meta comparison indefensible. **Do not infer an identified causal year reversal.** See [exact original source, group and model gates](DEMANINCOR2022_REPRODUCTIVE_STAGE_SOURCE_GATE.md). This contributes **zero** new strict H1 effects and no downstream antagonist/mixed stage test.

## Already documented multi-stage positive results and counterexamples

| Programme | Source-backed finding | What survives to plant outcome? | Identification boundary |
|---|---|---|---|
| **Cardamine–Anthocharis** | Peak of active eggs capable of producing damaging larvae moves **+0.49 flowering-date SD later** than all eggs and narrows by **28.3%**; early vs late ecotypes differ in dehiscence before larval completion (**34% vs 4%**) | Host stage filters oviposition to later potential reproductive damage | Only 1 source programme; ecotype averages are not same-unit causal proof; contemporaneous female-flight raw distribution for adult-only prediction comparison is unresolved |
| **Silene–Hadena** (Kula 2012) | Synchrony–predation direction **reversed across 2008/2009** with different larval-development and fruit-maturation timing | Consumer-stage delay is consistent with cost-sign reversal | Larvae first observed mobile, not feeding onset; 2009 detection margin spans zero under uncertainty; outcome is **predation**, not reconstructed final intact seeds |
| **Mertensia ciliata** | >5× variation in visits across experimentally shifted flowering weeks but no significant seed-set treatment effect in one experiment; separate watering experiment affects seeds without significant timing×water interaction | Encounter-frequency information can be buffered by visitor quality or downstream reproductive resources | The null does not prove equivalent seed set and experiments belong to one programme |
| **Gols 2025: Sinapis versus Brassica** | Comparable experimentally timed herbivory in the same study changes components; integrated seed-number×germination reproductive potential **buffered in Sinapis arvensis** but **stage-sensitive in Brassica nigra** | Same insect and study yield contrasting final propagation patterns by host | One experiment/dependence programme; reproductive potential is a constructed index, not observed offspring recruitment |
| **Parkinsonia–Penthobruchus** | Source-reported early exposure model vs late survival-filter model shifts **leave-region-out RMSE 20.58 → 4.92 percentage points** | Egg-to-effective-consumer conversion can explain final seed damage | Parasitism/hatch and mature damage recorded in same late sample, no prospective forecasting or identified added phase matching benefit |
| **Riemer 2024: Pisum–Cydia** | 88 pea fields: independent moth first arrival × flowering improves damaged-seed prediction over flowering-only (**9.20 → 7.36 pp RMSE**) | Adult×host phenology adds information in a different crop antagonist system | Held-out unit is a **field**, not independent year; response is damaged-seed percentage, not net plant seed output; stage-specific offspring filter unmeasured |

The list is **selected and outcome-aware**, not a systematic completeness sample. Do not turn proportions of rows in this table into estimated frequencies of ecological phenomena across taxa.

## Independent resource-limitation boundary: Sinapis arvensis (not a phase test)

The publicly archived [Höfer et al. (2022) original Sinapis source](HOFER2022_RESOURCE_SERVICE_LIMITING_STAGE_AUDIT.md), Zenodo 10.5281/zenodo.7335086, supplies **one** additional independent original plant-reproduction programme in a water-manipulation design, but **no date-resolved pollinator-availability curve**. Fifty of 53 source plants link fully to total seasonal flower counts, visitor taxon/group observation rates and estimated total seeds. The valid independent physical blocks are **five shelters**, not 50 plants or 427 visitor-group records.

Under identical five-shelter-held-out regression, visitor observation rate without plant flowering supply predicts log(1 + author-estimated whole-plant seeds) poorly (water+visitors RMSE **0.7900**); water+flowers has **0.4885**; adding visitors conditional on flower abundance reduces RMSE to **0.4417**. Removing the flowers-from-the-visitor-rate denominator retains a modest positive difference (water+flowers+visitor/day **0.4469**); both visitor conditionals improve **4/5 shelters**. In 29 source plants with stigma pollen, adding pollen receipt does not improve the conditional flower model; source timing and missingness limit that comparison.

**Critical later source consistency check:** 47/50 admissible Sinapis plants have more counted pods than the apparent season-total flower index, precluding a valid pods/flower fruit-set interpretation. Furthermore, **50/50 reported estimated seed totals exactly equal pod count × source mean seeds per pod**, so total seed numbers are calculated from these components rather than independently observed. Among the same 50 individuals, visitor/day adds more held-shelter predictive information to pod numbers (RMSE 0.54436 → 0.47570; 4/5 shelters) than to mean seeds per pod (0.15433 → 0.14386; 3/5 shelters), whereas flowering duration predicts seeds/pod with RMSE 0.13662. This is a **descriptive distinction in stage-component responses**, not a traced causal conversion chain or additional source replication. See [component audit](HOFER2022_FRUIT_SEED_CONVERSION_AUDIT.md).

**This is a different biological clock and endpoint** from the three-plant Osmia source: aggregated visitors over the flowering season and whole-plant *estimated seed number*, not day-matched adult density and sampled-fruit seed proportion. The original authors already documented drought effects mediated mainly by fewer flowers; IWE contributes an explicit block-held-out *conditional resource-versus-visitor information* comparison. The cross-programme interpretation is **conditional service information may exist in multiple systems, while only Osmia directly tests date-matched adult–flower overlap.** There is still no identified host-stage conversion mechanism nor cross-taxon causal timing superiority.

## The most defensible nontrivial synthesis

**Temporal coincidence is not itself a reproductive payoff.** The informativeness of any measured "matching" variable depends on whether it corresponds to the biological gate currently limiting reproductive success. That gate may be adult access to receptive flowers, a vulnerable tissue window, egg/larval establishment, retention or abortion, effective pollination, or resource availability for seed maturation.

The specific, falsifiable extension beyond generic "timing matters" is:

> **Conditional timing-information hypothesis:** in an independently validated dataset with the same reproductive endpoint, a biologically matched interaction coordinate should add predictive information over season/calendar and time-averaged partner availability **only when the matching window contains an exposure-to-fitness conversion step not already saturated or compensated at a later stage**.

This is a *candidate* generalization. The de Manincor **2021 cohort** provides a small *date-matched adult–flower* original-data positive test against adult-mean, calendar, coverage, and shifted-phase controls, while the **2022 separate cohort** shows that this predictive advantage is not invariant to reproductive stage or arena-versus-room holdout design. Höfer offers a separately replicated **resource-conditioned visitor-information** diagnostic without date-specific animal timing; neither measures a delayed antagonist stage. The maple **2012–2017 intact-seed-fraction** analysis shows how an apparent spring-to-seed relationship loses uniqueness to a simpler known biennial clock, whereas the **13-year sampled seed-count** analysis shows that spring flowering effort *can* carry more year-held-out predictive information than that same simple clock for a distinct output. Their difference emphasizes endpoint grain rather than establishing a general stage-filtering law. The Cardamine and Gols evidence motivates *where* conversion occurs, but not a cross-programme predictive-superiority claim.

### Mandatory falsifiers of this candidate hypothesis

1. **Simpler clock:** calendar, known cycles, and adult mean density must be measured or controlled, not ignored.
2. **Matched sampling:** all models on identical plant/fruit/source IDs and endpoints, with missing source outcomes explicitly recorded.
3. **True holdout:** block by field/year/arena, leaving independent biological units unseen by model selection; multiple plants in one arena are not replicate communities.
4. **Mechanistic ablation:** a stage-filtered exposure model must beat **filter-only**, not just calendar-only, in a programme that genuinely measures both. A response exposed at harvest cannot be presented as a forecast.
5. **Null/compensation check:** if seeds are limited by resources or effective service is saturated, observed temporal overlap need not affect reproduction.

## State of the project and next decisive source

- **Frozen strict H1 on main:** 2 mutualist independent SMD clusters, **0 antagonist / 0 mixed**. These studies do not change that.
- **Exploratory landscape on pivot:** original source retrieval and controlled model comparisons have succeeded for maple (six-year intact-fraction and **13-year seed-count** distinct endpoints), three-plant bee source (date-matched adult service), and *Sinapis* (season-aggregated resource-versus-visitors boundary). These are **three taxonomically distinct source programmes including two de Manincor annual cohorts, with separate response grains**, not exchangeable effects. All have strict claim ceilings and original-source audit receipts. No causal stage-generalization estimate has been obtained.
- **Next required dataset:** multiple independent years/sites with independently dated adult partner availability, directly observed pre-outcome host susceptibility and effective consumer/service state, and **mature intact seeds on the SAME tagged reproductive units**. Predeclare matching models: context/calendar; adult-only; host-sensitive window; conversion-filter-only; matched window × filter. Use held-out years or programmes for comparison.
- **Priority among already screened sources:** numeric 2012–2014 female Anthocharis flight data for the Cardamine same-year comparison, or a linked Hurlburt Yucca flowering-date-to-mature-fruit record; neither may be imputed from eggs, post-harvest damage or other units. A new independently sourced open dataset meeting this contract is preferable to repeated recovery attempts that cannot unlock the join.

**Scientific endpoint:** the project presently supports heterogeneous *propagation and buffering of timing signals* in named systems and a modest original-data adult bloom-overlap prediction signal in one experimental community. It **does not** yet support a universal superiority law for downstream stage-specific timing, a three-interaction-class meta-analytic effect, or an adaptive evolutionary conclusion.
