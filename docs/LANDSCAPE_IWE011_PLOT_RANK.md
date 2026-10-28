# IWE011 — plot-level seasonal antagonist landscape

Date: 2026-10-02  
Study: Kudo & Shibata 2025, *Peucedanum multivittatum × Phaulernis fulviguttella*  
DOI: `10.1111/1365-2745.70130`  
Status: quantitative descriptive landscape evidence; not a strict independent-adult-window effect.

## Why revisit IWE011

The former HA-versus-HD Hedges-g extraction was correctly withdrawn because it compared one early plot with one late plot while treating hundreds of plants as independent timing-exposure replicates.

The landscape pivot does not restore that SMD.

Instead, the published five-plot design is used at its actual exposure grain: **plot**.

Figure 1 orders the populations from consistently early to late flowering:

`HA < HL < HC < KD < HD`.

Table 1 reports plot-level pooled reproductive summaries across 2020–2023.

## Plot summaries

| Plot | Phenology rank | Initial fruit set | Final fruit set | Intact fruits |
|---|---:|---:|---:|---:|
| HA | 1 | 0.50 | 0.13 | 3.1 |
| HL | 2 | 0.52 | 0.32 | 11.8 |
| HC | 3 | 0.42 | 0.25 | 10.2 |
| KD | 4 | 0.52 | 0.48 | 18.5 |
| HD | 5 | 0.42 | 0.40 | 14.7 |

The source reports that initial fruit set before predation is relatively stable across plots, whereas final fruit set is lowest in the earliest populations; approximately 71% of fruits are damaged in HA and predation is negligible in late KD/HD populations.

## Reconstructed five-plot associations

Using plot as the unit and the early-to-late rank fixed from Figure 1:

| Outcome | Spearman rho | two-sided p |
|---|---:|---:|
| Initial fruit set | -0.3162 | 0.6042 |
| Final fruit set | +0.8000 | 0.1041 |
| Intact fruit number | +0.8000 | 0.1041 |

With only five plots these are deliberately labelled **descriptive associations**, not a new inferential meta-analytic effect.

The biologically useful contrast is between the response surfaces: the early-to-late rank has little relationship with pre-predation fruit initiation, but a strong positive rank association emerges after predation.

## Interpretation

IWE011 therefore gives a concrete example of a cost surface being added after pollination:

1. initial fruit-set success is broadly similar across the flowering gradient;
2. realized moth oviposition/predation is concentrated early in the season;
3. final intact reproduction consequently increases toward later populations.

This is compatible with temporal escape from a **realized antagonist window**, but the window is defined from oviposition/predation rather than an independent adult-moth census. It remains lower-provenance than IWE032 for a causal partner-availability claim.

## Reproducibility

Source values are stored in `data/source_reconstructions/iwe011_plot_table1.csv`.

`scripts/build_iwe011_plot_rank_landscape.py` verifies the five-plot phenology order and rebuilds `data/derived/iwe011_plot_rank_landscape.csv`.

Plant observation counts are preserved as source metadata but are never used as five-plot timing replication.
