# IWE015 timing-source and unit audit — 2026-10-01

Study: Zhou et al. (2020), *Variable and sexually conflicting selection on Silene stellata floral traits by a putative moth pollinator selective agent*  
DOI: `10.1111/evo.13965`  
Dryad DOI: `10.5061/dryad.6q573n5w1`  
Decision: **strict timing gate remains biologically eligible; quantitative hold is variance-only**

## Why this audit was needed

After the 2026-09-28 antagonist re-audit, IWE explicitly forbids using host egg receipt, attack, infestation or damage as though those quantities were an independent partner-availability curve.

IWE015 also records *Hadena ectypa* eggs, so its former "Hadena-dominant versus co-pollinator-dominant" timing assignment needed to be checked against that rule before any raw variance restoration.

## Same-season adult partner evidence

The 2012–2013 field-experiment methods state that the authors conducted pollinator surveys throughout the flowering season in each study year to confirm the dominant status of *H. ectypa* and the co-pollinating moth assemblage.

Figure 1 reports two distinct adult moth-density series for each year:

- *H. ectypa* moth density;
- co-pollinating moth density.

Moth density is defined as:

`number of H. ectypa or co-pollinating moths per flower × 100`.

Thus the early and late experimental windows are supported by same-season direct adult moth observations.

The study also reports egg density, but that is a separate oviposition series. The egg series is not required to order the strict partner window and must not be registered as its provenance.

## Frozen window interpretation

For each focal year:

- early experiment = *H. ectypa*-dominant adult-moth context;
- late experiment = co-pollinator-dominant context after adult *H. ectypa* density declines.

Therefore the intended restored timing fields remain:

- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- `exposure_direction = synchrony`.

If IWE015 returns to the strict corpus, its strict-window provenance must be registered as same-season direct adult moth survey/census evidence, **not** `egg_receipt` or `oviposition_success`.

## Exposure and response units

The early and late experiments used different naturally flowering plants selected into the experimental population for each one-week period.

The timing state is therefore a seasonal experimental **context**, not an individual-level randomized assignment of flowering week.

Plant-level successful-fruit counts provide response sampling within that context.

If restored, IWE015 unit provenance should therefore be conservative:

- design type: fixed-context/observational seasonal comparison rather than randomized timing manipulation;
- exposure grain: seasonal experimental window;
- response grain: plant;
- variance interpretation: within-context response sampling;
- inference scope: descriptive association;
- causal claim allowed: no.

The plant n values can describe the response distributions within early and late contexts, but they must not be described as independent replications of the seasonal window itself.

The two years remain dependent members of one Mountain Lake programme cluster.

## Raw schema information

The archived `data_analysis.R` reads the four female files as:

- `2012_early_female.csv`;
- `2012_late_female.csv`;
- `2013_early_female.csv`;
- `2013_late_female.csv`.

For female reproductive fitness it uses column:

`ft`.

It then defines relative female fitness as:

`rf = ft / mean(ft)`.

A public GitHub mirror of the analysis script reproduces this code and the four exact Dryad filenames. The mirror is useful for schema discovery but does not replace source-file verification of the raw observations.

The executable IWE015 raw audit now defaults its successful-fruit field to `ft`.

## Remaining blocker

The timing gate is **not** the current blocker.

The only current quantitative blocker is the internally inconsistent Table 1 dispersion label:

- Table 1 calls the printed values SE;
- bounded proportion entries prove the literal-SE interpretation impossible;
- the printed values look numerically SD-like;
- but primary extraction will not relabel them without source-row confirmation.

Restoration therefore still requires the four female CSVs to reproduce the published n, means and raw dispersion.

## Restoration transaction

If raw verification succeeds, restoration should update all of the following together:

1. re-add the 2012 and/or 2013 quantitative effect rows using raw SDs;
2. replace the pending adjudications with exact `eligible + strict_extracted` rows;
3. add same-season adult-moth provenance rows to `strict_window_provenance.csv`;
4. add conservative fixed-context unit-provenance rows to `strict_effect_unit_provenance.csv`;
5. retain `DEP_SILENE_STELLATA_HADENA_MLBS` for both years;
6. rebuild evidence-audit and claim-status outputs.

No restoration may use the egg-density curve as the independent partner window, and no restored claim may be described as a randomized causal timing treatment.
