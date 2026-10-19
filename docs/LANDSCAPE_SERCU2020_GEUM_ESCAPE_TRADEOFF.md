# Geum-Byturus antagonist escape tradeoff

Date: 2026-10-02  
Study: Sercu et al. 2020, *Geum urbanum × Byturus ochraceus*  
DOI: `10.1111/1365-2745.13325`  
Dryad: `10.5061/dryad.x3ffbg7dz`  
Landscape role: independent antagonist final-fitness replication of a window-relative escape tradeoff.

## Why this system matters

The current pivot predicts that antagonist effects should be expressed relative to an effective cost window rather than as a universal calendar-direction rule.

This study is especially useful because *G. urbanum* is mainly self-pollinating, so the seasonal flowering response can be interpreted without a strong countervailing requirement to track animal pollinators.

The plant has two flowering peaks:

- a large first peak around day-of-year 150;
- a second peak around day-of-year 225.

Predation by the specialist seed beetle *Byturus ochraceus* occurred almost exclusively during the first peak and beginning of July. The authors therefore defined off-peak flowering as the proportion of flowers produced in the second peak.

This is registered as a `realized_interaction_window`, not as independently censused adult availability.

## Source-level temporal and fitness results

More than half of plants experienced predation:

- 2015: 65%;
- 2016: 56%;
- 2017: 56%.

Among flowers that were predated, the average fraction of seeds eaten was approximately:

- 2015: 60%;
- 2016: 65%.

For 2015, reproductive output per flower declined through the season even without predation:

- earliest-flower seed mass intercept: 0.27 g, SE = 0.023;
- flowering-date slope in unpredated plants: -0.0027 g/day, SE = 0.0002, p < 0.001.

Predation imposed a large early-season penalty:

- predation main effect: -0.11 g, SE = 0.025, p < 0.001;
- predation × flowering-date interaction: +0.0013 g/day, SE = 0.00027, p < 0.001.

Thus later flowering reduces the relative cost of seed predation, but late flowers also intrinsically produce less seed mass.

## Final plant-level fitness geometry

The final plant-fitness response was total seed mass per plant.

For unpredated plants, the proportion of flowers in the second peak was not significantly related to total seed mass.

For predated plants, the quadratic phenology model was preferred over the linear model:

- linear AIC = 201.0;
- quadratic AIC = 194.9.

The fitted final-fitness surface peaked when approximately **36% of flowers were produced in the second flowering peak**.

This is the key landscape result:

> antagonist escape is beneficial, but complete displacement to late flowering is not optimal because later reproduction carries an abiotic cost.

The optimum is therefore internal rather than at the earliest or latest possible date.

## Lagged induced response

Plants exposed to higher predation in year t produced a larger fraction of flowers in the second peak in year t+1.

The reported 95% credible interval for the slope was:

`0.00043 to 0.01526`.

No compensatory shift was detected within the same season; the corresponding 95% interval was:

`-0.0045 to 0.0046`.

This separates a lagged induced phenological response from simple within-season compensation.

## Relation to the Cardamine result

Cardamine shows host-stage filtering of a realized interaction window and propagates that effective window into final intact reproduction.

Geum supplies a different but complementary final-fitness geometry:

- the enemy cost is concentrated in an early realized window;
- moving reproduction away from that window reduces antagonist cost;
- but the host pays an independent late-season reproductive penalty;
- final fitness therefore peaks at an intermediate degree of temporal escape.

The two systems independently support the broader principle that the optimum cannot be predicted from calendar date or antagonist presence alone.

## Claim boundary

This programme does **not** close the strongest P4 raw-adult-exposure alignment gate because adult beetle activity was not independently censused as a focal quantitative series for the analysis.

It does provide an independent final-fitness replication of a window-relative antagonist escape tradeoff using a pre-fitness realized interaction window.

It should therefore be counted as `realized_window_evidence`, not as `strong_candidate`.

## Source-backed data availability

The authors archived five public Dryad files, including flower-level and plant-level data for 2015-2017. The current branch uses the published source estimates above and does not infer missing raw coefficients.
