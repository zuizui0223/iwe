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

## Why the Dryad deposit changes the priority

Unlike the Tomares and James blockers, this source explicitly deposits the **full dataset** in Dryad.

The raw-data audit needs only to establish whether the dataset contains enough information to reconstruct a final outcome at the initially marked-flower or plant grain, for example:

`flowering cohort + fruit fate + final seed count`.

If unrecovered flowers have source-coded beetle-damage fate, a strict net reproductive outcome such as total mature seeds per initially marked flower can be constructed without imputation. If the data contain only seed counts for surviving fruits, this candidate remains blocked.

The current web/runtime environment could reach the article and Dryad DOI metadata but not retrieve the Dryad files; the share/API path returned an access/404 failure. This is an access-path limitation, not evidence that the data are unavailable.

## Gate status

| gate | status |
|---|---|
| independent programme | yes |
| contemporaneous antagonist window | yes |
| final post-antagonist reproduction | **partial pending fate audit** |
| SMD-ready raw/group variance | not yet audited |
| status | **P1 blocked_final_surface** |

## Comparison with other antagonist P1 routes

This is now the highest retrieval priority because the missing information is nominally public.

- **Parnassia–florivore**: raw dataset public; need final fate/seed audit.
- **Astragalus–Tomares**: biological effect present, but correct-unit thesis/raw data are not public.
- **Yucca–cheater**: biological effect present, but timing-stratified final seed summary is not published.

If the Dryad raw table closes the fate question, Parnassia is the most direct route to antagonist cluster #2.
