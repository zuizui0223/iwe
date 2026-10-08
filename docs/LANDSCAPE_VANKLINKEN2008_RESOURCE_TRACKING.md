# Van Klinken & Flack 2008 — temporal tracking inertia limits final seed loss

Date: 2026-10-03  
Study: *Parkinsonia aculeata × Penthobruchus germaini*  
DOI: `10.1111/j.1365-2664.2008.01478.x`  
Landscape role: independent antagonist final-seed-loss evidence for stage-specific resource tracking.

## Why this system matters

The stage-specific IWE model predicts that plant reproductive cost depends not only on whether an antagonist is present, but on whether the antagonist's effective oviposition window tracks the short-lived host stage that can be consumed.

This study tests that quantity directly at continental scale.

Sites were surveyed repeatedly at 4–6 week intervals from 2000 to 2003. The programme tracked:

- seed availability through time;
- *P. germaini* egg density on seeds;
- immature beetle mortality and parasitism;
- final seed predation.

The exposure is realized oviposition on seeds, not independent adult abundance, so it is registered as a `realized_interaction_window`.

## Final reproductive cost

Despite substantial egg loads, annual seed predation was relatively low:

- mean seed predation: **2–30%**;
- mean egg density: **0.55–3.2 eggs per seed**.

Immature mortality was also substantial, but temporal tracking remained an independent limiter.

The deterministic model predicts only **5–56%** seed predation at observed egg densities even if direct immature-stage mortality is removed.

## The temporal mismatch

At any site, pod maturation was relatively synchronous.

The source reports that:

- pod maturation occurred about **6 weeks before pod drop**;
- egg density consistently **declined when pods matured**;
- egg density therefore failed to peak when the largest number of seeds was available.

This is temporal tracking inertia at the stage that matters to final seed loss.

The beetle population tracks broad between-region and between-year differences better than sharp within-season resource peaks, but fails to match the short pulse of maximal seed availability.

## Paired simpler-versus-stage diagnostic

The source tables permit a limited but fully source-backed comparison across **seven matched region-season combinations**.

To avoid changing pod location across predictors, the simple comparator uses the **annual mean egg density on ground pods** from Table 2.

The stage-specific comparator uses the egg density measured on ground-pod samples collected at the first survey at least 40 days after peak pod fall, the same late-season sampling frame used for observed seed predation in Table 5.

A third coordinate applies only pre-final biological filters measured in that same source:

`filtered stage exposure = stage-matched egg density × (1 - egg parasitism) × egg hatch`.

No final seed-predation value enters this coordinate.

The resulting descriptive performance is:

| Coordinate | Pearson r with observed seed predation | Spearman rho | Leave-one-region-out RMSE (pp) | Leave-one-region-out MAE |
|---|---:|---:|---:|---:|
| Annual ground-pod egg density | **0.476** | 0.571 | **20.58** | 19.04 |
| Stage-matched egg density | **0.596** | 0.571 | **19.93** | 16.10 |
| Filtered stage exposure | **0.938** | 0.929 | **4.92** | 4.78 |

The three source-defined comparisons above show a large apparent gain after adding egg parasitism and hatch. An additional **post-outcome, non-confirmatory ablation** (all ten single-variable candidates retained in the companion file) shows a sharper limitation: **joint nonparasitized × hatch fraction alone**, *without either egg-density or timing term*, obtains leave-one-region-out RMSE **4.11 pp**, slightly lower than **4.92 pp** for stage-matched egg density multiplied by the same survival fraction. Stage matching alone improves 20.58 to only 19.93 pp. Consequently, these data **do not isolate incremental predictive value of stage alignment once downstream survival is known**. The dominant measured contrast is survival/conversion eligibility, and even that result needs independent validation. Region blocking is required because VRD, Barkly and Central Queensland each contribute two seasons; row-wise leave-one-out would leak the same region into training and test sets.

This is the first independent IWE programme with an explicit **simpler-coordinate versus stage/filter-coordinate diagnostic** pointing in the predicted direction.

It is deliberately not called confirmatory for three reasons:

1. **n = 7** region-season combinations from only **4 regions**;
2. the exposure is realized oviposition on seeds, not an independently measured adult-flight or adult-abundance window;
3. the strongest coordinate incorporates egg parasitism and hatch, which are mechanistically close to seed consumption and are not a host-specific developmental filter.

The diagnostic is therefore registered as `paired_realized_positive`, not `confirmatory_ready`.

The reconstruction is executable in
`scripts/build_vanklinken2008_paired_stage_diagnostic.py`,
with source rows in
`data/source_reconstructions/vanklinken2008_paired_stage_diagnostic.csv`
and generated outputs in
`data/derived/vanklinken2008_paired_stage_rows.csv`
and
`data/derived/vanklinken2008_paired_stage_metrics.csv`.

## General implication

The result provides an independent final-reproduction analogue of the stage-specific window logic:

> a consumer can be abundant and well established yet impose weak final reproductive cost if its realized oviposition window fails to track the host's brief vulnerable-resource peak.

The relevant coordinate is not calendar date alone and not annual antagonist abundance.

It is the alignment between:

1. the host seed-availability pulse;
2. the realized oviposition pulse;
3. subsequent seed destruction.

## Relation to other IWE systems

- Cardamine shows that only a subset of egg exposure becomes future damaging larvae.
- Kula 2012 shows that developmental phase lag can reverse the sign of synchrony on predation.
- Parkinsonia shows that a consumer can fail one stage earlier: oviposition itself does not track the resource pulse, limiting annual seed loss.

Together these systems separate adult presence, realized exposure, developmental conversion and final reproductive cost.

## Claim boundary

This study does not provide individual flowering-time fitness gradients and does not test adult partner availability.

It is therefore not strict H1.

It does, however, directly connect temporal resource tracking to **final annual seed loss**, so it is registered as `realized_window_evidence`, not mechanism-only.

Source-backed quantities are stored in
`data/source_reconstructions/vanklinken2008_resource_tracking.csv`.
