# Legacy mixed-system phenology audit

Date: 2026-09-24  
Decision: Pettersson (1991) and Biere & Honders (1996) remain direct seasonal-timing evidence but **do not satisfy the frozen strict synchrony gate**.

## Why the candidate ledger was re-opened

The first replication ledger treated both studies as if an independently measured *Hadena* activity window existed and only quantitative SMD recovery remained. A later study designed specifically to quantify *Silene–Hadena* synchrony provides a direct audit of that assumption.

Rogers Kula (2012), Chapter 3, reviews Pettersson (1991) and Biere & Honders (1996) immediately before introducing a dedicated synchrony design. The review states that:

- Pettersson and Biere–Honders documented seasonal changes in pollination, fruit set and seed predation;
- such changes might reflect changing *Hadena* density/visitation through the season;
- **the potential effects of pollinating-seed-predator phenology had not been quantified** in that earlier work;
- the new study therefore collected both individual plant flowering and *Hadena* activity and explicitly calculated synchrony.

That distinction matches IWE's frozen timing contract: outcome-associated plant calendar position is not itself partner synchrony.

## Pettersson 1991 — IWE014

Source: *Silene vulgaris × Hadena spp.*  
DOI: `10.1111/j.1600-0587.1991.tb00632.x`

The paper remains biologically valuable:

- early and late flowering positions differ in seed predation;
- pollination and capsule destruction covary within the season;
- final seed production is discussed.

However, the strict H1 exposure cannot be created by treating seed predation or pollination outcome as a proxy for the missing *Hadena* seasonal activity curve. Doing so would orient the exposure using the response/mediator.

Gate outcome:

| gate | decision |
|---|---|
| independent programme | yes |
| independently quantified focal-season partner activity | **no** |
| final plant reproduction | yes |
| strict-H1 status | **rejected_timing** |

The earlier `blocked_summary_stats` classification is therefore withdrawn.

## Biere & Honders 1996

Source: *Silene alba / S. dioica × Hadena bicruris*  
DOI: `10.2307/3545936`

This study strongly links flowering phenology to fruit set, seed predation, and undamaged-fruit production. It is useful evidence that calendar position changes the net outcome of a mixed interaction.

But the later synchrony study explicitly distinguishes this earlier work from designs that quantify both host flowering and pollinating-seed-predator activity. No independent focal-season *Hadena* activity window has been recovered from the 1996 study.

Gate outcome:

| gate | decision |
|---|---|
| independent programme | yes |
| independently quantified focal-season partner activity | **no** |
| final plant reproduction | yes |
| strict-H1 status | **rejected_timing** |

## Consequence for the replication target

Mixed #2 is not currently a summary-statistics recovery problem. It is a **study-discovery problem**.

The next eligible independent mixed programme must contain, in the same focal season/context:

1. measured partner activity/availability,
2. plant phenology that can be ordered prospectively by overlap,
3. final post-cost plant reproduction, and
4. raw data or summary variance compatible with the frozen SMD family.

The Rogers Kula / Mountain Lake *S. stellata × H. ectypa* synchrony work does quantify both partner activity and host flowering, but it belongs to the same Mountain Lake programme represented by IWE015 and therefore cannot satisfy the independent-cluster target.
