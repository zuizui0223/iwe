# Temporal signal transformation contract

Date: 2026-10-06  
Status: adjudication contract for `data/registry/temporal_signal_components.csv`.

## Purpose

The transformation ledger is intended to describe what happens biologically to a source-backed temporal signal as it propagates downstream.

It must not become a sign-picking exercise in which a convenient pairwise contrast is called `preserved` whenever its point estimate has the expected sign.

Adjudication follows the source's full design, downstream endpoint, and stated mechanism.

## General rule

Assign the transformation using the **broadest source-defined comparison needed to describe the downstream fate of the upstream timing signal**.

A selected extreme-group sign is insufficient when the source's full treatment series or model shows that the upstream effect is compensated, absent, reversed, or otherwise transformed.

Statistical significance is not itself the transformation state, but a source-level null across the designed timing series cannot be ignored merely because one frozen pairwise point estimate has the expected sign.

## States

### preserved

Use only when the source-backed temporal ordering retains the same biological direction at the downstream endpoint without a source-demonstrated compensatory process eliminating the net response.

Evidence may be a continuous slope, source-defined group contrast, manipulation, or other design-compatible estimate.

### preserved_net_changed_mechanism

Use when the final direction is retained, but the source demonstrates that the component pathways generating that final direction differ across contexts.

This is stronger than merely having different intermediate effect sizes: the mechanism producing the same net direction must itself change.

### shifted_filtered

Use when downstream biology selects, shifts, or narrows a subset of the upstream temporal exposure so that the effective window is displaced relative to the raw one.

### sign_reversed

Use when downstream processing makes the biological direction opposite to the upstream timing relationship.

### erased

Use when an upstream timing relationship is demonstrably present but no longer predicts the downstream stage, and the source does not identify a compensatory pathway that preserves performance.

### buffered

Use when an upstream timing difference/cost is real, but a source-backed compensatory mechanism substantially dampens or removes its effect at the downstream endpoint.

The compensatory mechanism must be identified rather than inferred solely from a non-significant final test.

### tracking_inertia

Use when the consumer/partner timing fails to track a moving resource or host window, so upstream resource timing is not translated into corresponding consumer exposure.

## IWE023 adjudication precedent

*Gallagher & Campbell 2020, Mertensia ciliata* is the guardrail example.

Source-backed observations:

- total pollinator visitation declines by more than fivefold from week 1 to week 4;
- seed set across the four experimental flowering weeks has `F(3,36)=1.01`, i.e. no significant week effect;
- the proportion of visits by more effective bumblebees increases through the season, countering the decline in total visitation;
- the frozen week-1 minus week-4 SMD remains positive (`g=+0.3815`).

The propagation state is therefore **buffered**, not preserved.

The strict-H1 SMD remains valid because that estimand only requires a prospectively ordered high-versus-low partner-availability contrast and a final response. Transformation adjudication asks a different biological question: whether the upstream visitation signal survives the full downstream process.

## Separation from effect extraction

Changing a propagation state must never silently:

- remove or reorient a valid strict-H1 effect;
- alter its effect size;
- change dependence assignment;
- change source-defined exposure ordering.

The extraction registry and the propagation registry answer different questions.

## Conservative tie-break rule

When two states seem plausible, prefer the state that acknowledges a source-demonstrated transformation over `preserved`.

Examples:

- expected-sign pairwise estimate + source-demonstrated compensation -> `buffered`;
- expected-sign net endpoint + different underlying pathways across years -> `preserved_net_changed_mechanism`;
- raw exposure peak differs from effective damaging peak -> `shifted_filtered`.

This rule is intentionally conservative because the temporal-information hypothesis is strongest when counterexamples are retained rather than explained away.
