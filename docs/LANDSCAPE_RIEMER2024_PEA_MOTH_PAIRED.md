# Riemer 2024 — independent adult timing improves final pea-seed damage prediction

Date: 2026-10-08  
Study: Riemer, Schieler & Saucke 2024, *Pisum sativum × Cydia nigricana*  
DOI: `10.1111/eea.13430`  
Landscape role: high-provenance antagonist adult × host-stage final-seed-damage evidence and a paired prospective predictive positive.

## Design

The study followed **88 unsprayed field-pea fields** in North Hesse across **2016–2019**.

For each field the source measured:

- pea flowering onset, BBCH 60, in growing degree days (GDD);
- first male *C. nigricana* arrival in field pheromone traps, also in GDD;
- final infestation as the percentage of damaged seeds in 100 randomly collected pods;
- spatial distance to the nearest previous-year pea field.

Adult moth timing is measured independently of plant damage and final seed outcomes.

## Paired timing-model comparison

The source compares general additive models on the same 88-field final damaged-seed endpoint.

| Model | Timing information | R2 | ΔAIC | LOOCV MAE | LOOCV RMSE | Correct low/high classification |
|---|---|---:|---:|---:|---:|---:|
| M1 | flowering onset only | 0.58 | 44.28 | 6.42 | 9.20 | 85.23% |
| M2 | distance + flowering | 0.65 | 32.35 | 6.15 | 8.61 | 85.23% |
| M3 | **first moth arrival × flowering** | **0.78** | **4.84** | **4.81** | **7.36** | **95.45%** |
| M4 | distance + moth × flowering | 0.80 | 0 | 4.85 | 7.16 | 95.45% |

Relative to flowering timing alone, adding the independently monitored adult-arrival × host-flowering interaction:

- reduces LOOCV RMSE from 9.20 to 7.36: **20.0% lower**;
- increases predicted-vs-observed R2 from 0.58 to 0.78;
- raises correct low/high infestation classification from 85.23% to 95.45%: **+10.22 percentage points**.

Adding spatial distance after the temporal interaction only modestly changes RMSE (7.36 to 7.16) and does not improve classification beyond 95.45%.

## Biological interpretation

The key source result is not simply that early flowering or early moth arrival is risky.

Infestation is highest when the susceptible flowering period coincides with early moth arrival. Fields flowering substantially before or after the main adult arrival period, or fields receiving late first moth arrival, tend to have lower damaged-seed percentages.

This is a high-provenance plant–antagonist timing coordinate because:

1. adult timing is measured independently with pheromone traps;
2. host susceptible timing is measured independently as BBCH 60;
3. the interaction between those temporal coordinates is specified before the final seed-damage outcome;
4. predictive performance is evaluated by leave-one-out cross-validation on final seed damage.

## Why this is stronger than a calendar-only timing effect

The paired comparison directly asks whether independent partner timing adds predictive information beyond host flowering date.

It does.

This therefore supplies a second type of positive paired diagnostic beside Parkinsonia:

- Parkinsonia: realized oviposition → stage matching → survival-filtered effective exposure;
- pea moth: host flowering alone → **independent adult-arrival × flowering**.

The two positives improve prediction at different causal layers.

## Claim boundary

This programme is **not** `confirmatory_ready` for the full stage-specific phase-alignment contract.

It does not separately measure:

- delayed larval timing relative to pod development;
- a pre-final host filter or larval-survival conversion stage;
- an adult-only comparator distinct from the host-flowering baseline.

The paired comparison is therefore classified as `paired_prospective_positive`, not as proof that a fully effective consumer-stage coordinate outperforms both calendar and adult-only timing.

It is nevertheless a strong high-provenance landscape anchor because independent adult timing and final seed damage are measured in the same field-level programme.

Source-backed model metrics are stored in
`data/source_reconstructions/riemer2024_pea_moth_prediction.csv`.
