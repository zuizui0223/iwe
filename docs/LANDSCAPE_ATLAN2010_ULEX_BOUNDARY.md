# Ulex predator-avoidance boundary system

Date: 2026-10-02  
Study: Atlan et al. 2010, *Ulex europaeus* seed predation and flowering phenology  
DOI: `10.1111/j.1420-9101.2009.01908.x`  
Landscape role: final-fitness boundary evidence against a timing-only escape rule.

## Why this is a boundary case

The interaction-window pivot predicts that plant fitness can improve by moving reproduction away from an antagonist cost window. That mechanism is real, but it need not be the only route to the same final outcome.

In a common garden, *Ulex europaeus* maternal families differed strongly in flowering schedule:

- long-flowering plants produced most pods before the main seed-predation peak;
- short-flowering plants concentrated reproduction during the predation peak.

The two phenologies therefore expose plants to different temporal positions relative to the enemy window.

## Alternative avoidance mechanisms

The two flowering types reduce predator damage in different ways.

Long-flowering plants use temporal escape: a larger share of reproduction is completed before predator pressure peaks.

Short-flowering plants reproduce during the predator peak, but synchronous fruiting increases local resource density and can reduce per-fruit attack through predator satiation.

This creates a direct test of whether temporal displacement is uniquely required for lower final damage.

## Final outcome

Across the whole reproductive season, the total proportion of infested pods was nearly identical:

- long-flowering type: approximately **29%**;
- short-flowering type: approximately **30%**.

Maternal flowering type had no significant effect on annual pod production, seeds per pod, or seeds per shoot in the reported common-garden analysis.

Thus strongly different temporal strategies can converge on similar whole-season enemy damage and annual reproduction.

## Interpretation

This system is not evidence against temporal escape itself. It is evidence against a stronger and overly simple rule:

> plants must move reproduction away from the antagonist window to reduce its final fitness cost.

Here, temporal escape and density-mediated predator satiation are alternative routes to a similar seasonal outcome.

The more defensible generalization is therefore conditional:

> the fitness effect of relative timing depends on the alternative mechanisms available for reducing interaction cost.

This makes density/resource concentration a candidate moderator of window-relative fitness landscapes.

## Claim boundary

The seasonal enemy window is inferred from observed infestation/predation dynamics, so this component is registered as `realized_interaction_window`, not independently measured adult availability.

The result is retained as `boundary_evidence` and is deliberately excluded from the branch's count of programmes supporting the window-relative rule.

Its role is to test selectivity and prevent the pivot from becoming tautological.
