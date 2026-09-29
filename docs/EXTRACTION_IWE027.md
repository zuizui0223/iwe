# IWE027 extraction receipt — Kameyama & Kudo 2009

Source: Kameyama Y, Kudo G. 2009. *Flowering phenology influences seed production and outcrossing rate in populations of an alpine snowbed shrub, Phyllodoce aleutica: effects of pollinators and self-incompatibility*. Annals of Botany 103:1385–1394. DOI `10.1093/aob/mcp037`.

Status: **strict-H1 mutualist SMD evidence extracted for two 2007 sites**.

## Timing and pollinator activity

The study established early-, middle-, and late-snowmelt plots (E, M, L) at two sites, Lake Hisago (HIS) and Mt Goshiki (GOS). Flowering proceeded sequentially from mid-July to late August.

Bumble-bee activity was measured directly in 2007. In early to mid-July only queens visited and visit frequency was very low. Worker *Bombus hypocrita sapporensis* appeared in late July, after which visit frequency increased abruptly and remained high through late August.

Because direct partner activity was measured only in 2007, IWE does not use the 2006 seed-set summaries as strict-H1 effects.

For 2007, the E-to-M contrast crosses the documented seasonal transition from the low-visit early window into the high worker-bee window. It is therefore registered as:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

The effect is always oriented as higher-overlap M minus lower-overlap E.

## Reproductive outcome

Natural-condition seed set was measured on randomly selected intact flowers. Fruits were harvested just before dehiscence, and seed-set rate was the proportion of ovules that developed into mature seeds.

Table 4 reports mean ± SE and sample size for each site × plot × year combination.

## HIS 2007

Intact natural seed set:

- high-overlap M: mean = 0.77, SE = 0.03, n = 24;
- low-overlap E: mean = 0.62, SE = 0.04, n = 24.

IWE reconstructs group SDs as `SE * sqrt(n)`, then calculates Hedges g:

`g = +0.8518282660`

`var(g) = 0.0885105687`.

Effect ID:

`IWE027_2007_HIS_M_VS_E_SEEDSET_SMD`.

## GOS 2007

Intact natural seed set:

- high-overlap M: mean = 0.65, SE = 0.05, n = 24;
- low-overlap E: mean = 0.40, SE = 0.05, n = 24.

The reconstructed effect is:

`g = +1.0038892388`

`var(g) = 0.0915777666`.

Effect ID:

`IWE027_2007_GOS_M_VS_E_SEEDSET_SMD`.

## Why 2006 is excluded from strict H1

The same paper reports 2006 seed set, and the flowering gradient also existed that year. However, seasonal bumble-bee activity was directly assessed only in 2007.

Using the 2007 animal-activity curve to relabel 2006 E/M plots as strict synchrony would violate the IWE rule that a seasonal-position contrast requires measured partner availability sufficient to order that contrast.

The 2006 component is therefore registered as non-strict/pending rather than silently promoted.

## Unit semantics

The 2007 E and M treatments are **fixed 20 × 20 m plots**, while the reported seed-set summaries sample 24 randomly selected inflorescences within each plot. The resulting SMD sampling variance therefore quantifies uncertainty in the response distribution **within those fixed plot contexts**. It must not be interpreted as 24 independent replications of the seasonal timing exposure.

This is admissible as a descriptive fixed-context association because partner visitation was measured independently in the focal season and the source itself compares seed set among plots. It is not an experimental estimate of a replicated timing treatment.

Executable unit provenance:

- `design_type = fixed_context_group_comparison`;
- `exposure_grain = plot`;
- `response_grain = inflorescence`;
- `variance_interpretation = within_context_response_sampling`;
- `inference_scope = descriptive_association`;
- `causal_claim_allowed = no`.

The HIS and GOS contrasts provide two site-specific response contrasts but remain one conservative programme-level dependence cluster.

## Dependence

HIS and GOS are distinct sites, but the two extracted effects share:

- one paper;
- one study year;
- one regional seasonal pollinator-activity series;
- one analysis programme.

They are conservatively assigned to one dependence cluster:

`DEP_IWE027_TAISETSU_2007`.

Thus two effect rows do not become two independent mutualist studies.

## Effect-family consequence

Both effects are `standardized_mean_difference`.

At the time of the original extraction, IWE011 and IWE015 also appeared to place SMD rows in the antagonist and mixed classes. Subsequent source audits changed that status:

- IWE015 is on quantitative hold pending raw variance verification;
- the former IWE011 strict SMD was withdrawn on 2026-09-28 because its partner window was based on oviposition/egg observations and its one-plot-versus-one-plot exposure used plant n as if the timing exposure were independently replicated.

The current strict SMD family therefore has two independent **mutualist** clusters (IWE027 and IWE023) and zero antagonist/mixed clusters. H1 is not evaluable.

## Claim boundary

IWE027 supports a positive within-region association between moving from the directly observed low-bumble-bee seasonal window to the high-worker-bee window and intact natural seed set in 2007.

It does not establish an experimental causal effect of synchrony, and the two site effects are not treated as independent meta-analytic replications.
