# IWE014 Pettersson 1991 — propagation audit stops at the timing-to-final-seed join

Date: 2026-10-07  
Study: Pettersson 1991, *Silene vulgaris × Hadena*  
DOI: `10.1111/j.1600-0587.1991.tb00632.x`  
Decision: propagation state remains **blocked**; do not infer a final timing signal from channel summaries.

## What the source establishes

The study measures pollination, *Hadena* herbivory/seed predation and seed production across two flowering seasons.

It shows two important temporal patterns.

1. Across flowers opening at different parts of the season, the percentage pollinated and the percentage of seed capsules destroyed are positively correlated.
2. Early-flowering individuals have similar pollination success to late-flowering individuals but suffer higher seed predation.

These results are strong evidence for **seasonal benefit-cost channel decoupling** and are already retained in the landscape registry.

## Why the propagation link is not yet frozen

The temporal-signal propagation ledger asks a stricter question: what happens to one source-defined upstream timing contrast at a final plant-fitness endpoint?

The currently recoverable source summaries do not provide a variance-bearing or otherwise explicit early-versus-late **final seed-output comparison** that can be joined to the same seasonal timing contrast.

The paper reports year-level net results—for example, the low-pollinator year has lower pollination but also lower *Hadena* damage and higher seed set—but a year contrast is not the same exposure as early versus late flowering within a season.

Likewise, higher early seed predation cannot be silently converted into lower final seed output without the source-defined final comparison.

## Decision

IWE014 remains useful for mixed benefit/cost timing, seasonal channel decoupling, and the biological motivation for separate B(t) and C(t).

But it is moved from propagation `candidate` to `blocked` with reason `timing_to_final_linkage`.

No transformation state—preserved, reversed, buffered or otherwise—is assigned until a source-backed seasonal timing group is explicitly linked to final seed output.

This is intentionally conservative and prevents channel evidence from being promoted into a final-fitness propagation result.
