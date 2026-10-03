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
