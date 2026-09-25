# Candidate audit — Parnassia wightiana × florivorous beetles

Date: 2026-09-25  
Source: Wen et al. (2024), *Ecology and Evolution* 14:e70380  
DOI: `10.1002/ece3.70380`  
Dryad: `10.5061/dryad.b2rbnzsqg`  
Candidate: `ANT002_PARNASSIA_WEN_2024`  
Decision: **P1 `blocked_final_surface` pending raw-data audit**

## Why this is a strong timing candidate

The Site A seasonal comparison is pre-ordered by an observed antagonist window, not by the reproductive response.

The authors divide flowering into:

- early: June, when no chewing beetles were observed;
- middle: 1–15 July, when <20% of flowers carried chewing beetles;
- late: 16 July–1 August, when >70% of flowers carried chewing beetles.

The florivore *Nonarthra variabilis* dominates the observed beetle fauna and beetle feeding begins in July, peaking after 10 July into early August.

Thus the exposure qualifies as `seasonal_position / strict_window / ordered_by_measured_window` in principle: late flowers are more synchronized with the measured florivore activity window than early flowers.

## Final reproduction

For each seasonal cohort the authors initially marked and bagged 60 flowers after petals wilted. In September they collected fruits and counted seeds per fruit.

Recovery was:

| cohort | initial marked flowers | recovered fruits |
|---|---:|---:|
| early | 60 | 31 |
| middle | 60 | 41 |
| late | 60 | 25 |

The paper reports a strong decline in seeds per recovered fruit across these periods (Kruskal-Wallis chi-square=41.215, df=2, p<0.001), with early flowers highest and late flowers lowest.

## Why the published figure/test is not yet an SMD-ready net fitness effect

The same methods section states that some tagged flowers were lost because beetles chewed the peduncle.

That matters because the focal antagonist cost has two routes:

1. reduced seed production among fruits that survive to collection;
2. complete loss of a reproductive unit when florivory damages the peduncle and prevents fruit development.

The publication's Figure 5B and Kruskal-Wallis test analyze **seeds per recovered fruit**. Treating only 31/41/25 survivors as the final sample would condition on survival through one of the focal antagonist effects.

Conversely, assigning zero seeds to every unrecovered flower is not justified from the article alone, because the text does not provide a row-level fate code proving that every unrecovered unit was lost to beetles rather than another cause.

IWE therefore does not:

- digitize the boxplot to estimate means/SDs;
- transform the Kruskal-Wallis statistic into an SMD;
- treat 31/41/25 survivor fruits as though the focal peduncle-loss process did not exist;
- assign zero seed output to missing flowers without source-backed fate information.

## Dryad publication/access audit

The article cites Dryad DOI `10.5061/dryad.b2rbnzsqg` and a reviewer-share URL. A 2026-09-25 audit changes how IWE must describe that deposit.

Current checks found:

- the exact Dryad DOI does not resolve to an active dataset;
- the cited reviewer-share URL returns 404;
- exact DOI/title searches do not expose a published Dryad record.

Dryad's own documentation explains the relevant workflow: a reviewer sharing link is temporary access to an uncurated submission, while the reserved DOI activates when the dataset is actually published after curation. The presence of a reserved DOI in the paper therefore does **not** establish that the raw table is currently public or retrievable.

This is not evidence that the authors never submitted data. It is a current-access result: **no active published Dryad record was recoverable in this audit**.

The scientific unlock remains unchanged. If a corrected/public archive or source table becomes available, IWE needs to determine whether it contains enough information to reconstruct final reproduction at the initially marked-flower or plant grain, for example:

`flowering cohort + fruit fate + final seed count`.

If unrecovered flowers have source-coded beetle-damage fate, a strict net reproductive outcome could be constructed without imputation. If the data contain only seed counts for surviving fruits, this candidate remains blocked.

## Gate status

| gate | status |
|---|---|
| independent programme | yes |
| contemporaneous antagonist window | yes |
| final post-antagonist reproduction | **partial pending fate audit** |
| SMD-ready raw/group variance | not yet audited |
| status | **P1 blocked_final_surface** |

## Comparison with other antagonist P1 routes

Parnassia remains biologically one of the strongest antagonist candidates, but it no longer receives priority merely because the paper cites a nominally public raw dataset.

- **Parnassia–florivore**: timing contrast is excellent; final net-fitness surface is blocked and the cited Dryad record is not currently active/retrievable.
- **Astragalus–Tomares**: biological effect is present; correct-unit plant/shoot variance is unavailable.
- **Yucca–cheater**: biological effect is present; timing-stratified final-seed summary is unpublished.
- **Cirsium–Rhinocyllus**: direct synchrony and final seed consequences exist in one long-term programme, but only as separate model surfaces; source-level final-seed-by-synchrony summaries would be needed.

No route is promoted by access assumptions.
