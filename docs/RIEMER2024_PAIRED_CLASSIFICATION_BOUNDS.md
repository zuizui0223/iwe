# Riemer 2024: paired classification margins, not identified transitions

_Generated from the 2024 article Tables 3–4 via data/source_reconstructions/riemer2024_pea_moth_prediction.csv._

## Published source totals

- 88 fields; flowering-only M1: **75 correct, 2 overestimated, 11 underestimated**.
- First-moth-arrival × flowering M3: **84 correct, 1 overestimated, 3 underestimated**.
- Net correct-classification gain: **9 fields**; underestimation difference: **-8 fields**.
- Field-wise LOOCV RMSE reduction: **20.0%** (published model summaries; no newly fit model).

## Every mathematically compatible field correctness table

The source has not released an exact 88-field paired prediction table. The intersection of the M1 and M3 wrong-field sets is therefore unknown. With 13 M1 mistakes and four M3 mistakes, the intersection can have **0 through 4** fields; all five possibilities are listed, with no synthetic field records or inferred overlap.

| Wrong under both | M1 wrong / M3 right | M1 right / M3 wrong | Right under both | Conditional exact McNemar two-sided tail |
|---:|---:|---:|---:|---:|
| 0 | 13 | 4 | 71 | 0.049042 |
| 1 | 12 | 3 | 72 | 0.035156 |
| 2 | 11 | 2 | 73 | 0.022461 |
| 3 | 10 | 1 | 74 | 0.011719 |
| 4 | 9 | 0 | 75 | 0.003906 |

The conditional two-sided tail area ranges **0.003906–0.049042** over every algebraically compatible overlap. These numbers are **not a new reported inferential p-value**: original models were compared/selected using the same data; outcomes and field-year correlations are unavailable, and no independent-year validation has been performed. Do not label the improvement confirmed in a fresh year or use McNemar significance to promote it.

## Scientific boundary

- The **nine-field net classification advantage** is supported by source marginals and does not require knowing which fields changed.
- The identity of improved vs worsened fields, error covariance, year-by-year performance, false-negative rate and generalization to unseen seasons remain unidentifiable from these totals.
- First *male* trap occurrence is an independently measured adult proxy, not direct female oviposition or a delayed larval survival filter.
- M3 adds an adult-arrival × flowering statistical interaction; there is no adult-only or truly host-filtered stage-specific comparator in Tables 3–4.
- There is also a textual inconsistency in the original article: Table 3 lists M4 LOOCV MAE as **4.85**, whereas the paragraph below Table 3 cites **4.70**. Use the printed Table 3 value, flag the discrepancy, and do not invent revised field predictions.

**Decision:** Retain Riemer as a strong within-corpus adult-plus-host-timing diagnostic, not a confirmatory effective-consumer-window superiority or strict-H1 SMD.

Source: Riemer, Schieler & Saucke (2024), https://doi.org/10.1111/eea.13430 (Tables 3–4 and data availability).
