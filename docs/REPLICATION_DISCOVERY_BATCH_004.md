# Replication discovery batch 004 — mixed-system design audit

Date: 2026-09-25  
Status: first mixed-focused design batch complete  
Outcome: **no second strict mixed SMD cluster yet**

## Search rule

Batch 004 asks a stricter question than “does this nursery-pollination system contain all the ingredients somewhere in the literature?”

For the mixed primary estimand, the **same dependence-compatible component** must provide:

1. contemporaneous focal-partner activity/availability;
2. plant timing that is prospectively ordered as higher versus lower overlap;
3. a final plant reproductive endpoint after the partner's seed/reproductive-tissue cost; and
4. SMD-compatible uncertainty at the correct biological unit.

Two complementary papers, or two separate experiments in one paper, are not stitched together to manufacture a strict effect.

## Bopp & Gottsberger 2004 — still P1

*Silene latifolia / S. dioica × Hadena bicruris*  
DOI: `10.1111/j.0030-1299.2004.12625.x`

This remains the cleanest mixed timing-positive lead. Daily host flowering and newly laid moth eggs directly establish same-season overlap.

The published article's downstream endpoint is host choice / larval performance rather than final plant reproduction after seed consumption.

The highest-value archival target remains Bopp (2003), *Parasitismus oder Symbiose?*, Zoologica 152 (140 pp., 36 tables). A plant final-fitness table from the same timing programme would close the biological gap; no accessible full text has yet been recovered.

Decision: `blocked_final_surface`, P1.

## Dianthus sylvestris × Hadena compta — timing gate corrected

DOI: `10.1007/s11258-009-9620-5`

The paper measures flowering phenology, egg receipt, predation and final female fitness through the season. The earlier ledger therefore treated it as timing-complete and blocked only by effect form.

That was too permissive. The focal paper does not independently quantify the contemporaneous adult *H. compta* activity curve. Seasonal egg deposition/predation cannot be used as the partner window because those quantities are interaction outcomes.

Decision changed from `blocked_effect_form` to **`rejected_timing`**.

## Rheum nobile × Bradysia — damage cannot be the exposure

Song et al. 2016  
DOI: `10.1038/srep29886`

This is a genuine pollinating seed-consuming interaction and the temporal experiment follows newly opened flowers through fruit development.

The decisive source statement is methodological: the temporal experiment uses **seed predation rate as a substitute for oviposition rate**. Thus the would-be timing exposure is inferred from the subsequent cost rather than measured independently.

Additionally, seeds in larva-bearing fruits are consumed, so the temporal component does not provide a clean directly observed post-cost seed-mass surface.

Decision: **`rejected_timing`**.

Companion *Rheum* papers may establish other pieces of the biology, but IWE will not splice them across studies to create a strict synchrony effect.

## Chamaerops humilis × Derelomus chamaeropis — benefit and cost are sex-separated

Dufay 2010  
DOI: `10.1111/j.1420-9101.2010.01968.x`

This study directly tracks palm and weevil phenology and measures female seed production.

However, the larval cost occurs mainly in old **male** inflorescence rachises. In female inflorescences, eggs/larvae are eliminated when seeds begin to develop. Female seed production therefore receives pollination benefit without the focal larval seed/reproductive-tissue cost on the same reproductive surface.

Decision: **`rejected_other`** for the mixed primary estimand.

## Senita cactus × senita moth — the right pieces occur in different components

Holland, Chamberlain & Miller 2011  
DOI: `10.1111/j.1600-0706.2010.18958.x`

This programme is unusually close:

- the early flowering season has high moth density and direct pollination/oviposition censuses;
- a later flowering period has intermediate moth density;
- another component follows egg-bearing flowers to ripe fruit production.

But the final ripe-fruit outcome belongs to ant/extrafloral-nectar manipulations, not to one high-versus-low moth-overlap contrast. The strict timing and final-fitness pieces therefore do not occupy the same estimand.

Earlier long-term senita studies commonly use **fruit initiation** as fruit set, which occurs before larval seed/fruit consumption and is not a post-cost final outcome.

Decision: `blocked_final_surface`, P2 citation-mining anchor, not a ready candidate.

## What Batch 004 changes

The mixed literature is not simply missing “more studies.” Its recurrent failure mode is **component fragmentation**:

- timing measured, final plant fitness omitted;
- final plant fitness measured, partner timing inferred from damage;
- benefit and cost placed on different plant sexes/tissues;
- timing and final reproduction measured in separate experimental components.

This motivates a sharper retrieval query:

> adult pollinator/ovipositor activity through season + tagged flowers/plants followed to mature surviving seeds in the same analysis.

Bopp 2003 remains the first archival retrieval target because it belongs to a programme that already passes the hardest timing gate.
