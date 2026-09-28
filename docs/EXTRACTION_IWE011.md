# IWE011 extraction receipt — withdrawn strict SMD

Source: Kudo G, Shibata A. 2025. *Phenological selection mosaic of predispersal seed predation affects gender variation in an andromonoecious plant*. Journal of Ecology 113:2832–2845. DOI `10.1111/1365-2745.70130`.

Dataset/code source: Hokkaido University Data Repository DOI `10.14943/hu95572`.

Status: **former strict-H1 antagonist extraction withdrawn on 2026-09-28 after timing-provenance and exposure-unit re-audit**.

## Biological evidence retained

The programme directly measures:

- flowering phenology across permanent *Peucedanum multivittatum* plots;
- deposited *Phaulernis fulviguttella* eggs;
- fruit predation;
- final intact mature fruits.

The final response is therefore genuinely post-predation plant reproduction.

The published HA and HD final fruit-set summaries are:

| Plot | Seasonal position | n plant observations | Final fruit-set mean | SD |
|---|---|---:|---:|---:|
| HA | mid-July | 177 | 0.13 | 0.19 |
| HD | August | 127 | 0.40 | 0.29 |

Mechanically standardizing these response summaries gives the historical diagnostic contrast

`HA - HD: g = -1.1368391965, var = 0.0155963310`.

That number is no longer an admitted meta-analytic effect.

## Timing-provenance failure

The 2025 paper describes predator moths as ovipositing on host umbels, usually in mid- to late July, and records deposited eggs on plants.

The 2021 predecessor explicitly describes the mid- to late-July window as a **preliminary observation of the major oviposition period**.

Neither public paper reports a contemporaneous quantitative adult-moth census/trapping/activity series that orders plant flowering windows independently of realized egg receipt.

Under the frozen IWE timing contract, eggs deposited on host plants cannot serve as the independent partner-availability curve because egg receipt depends on host availability, host choice and interaction success.

Thus the former `ordered_by_measured_window` classification was inconsistent with the rule later applied to Cardamine and Bopp.

## Exposure-unit failure

The former contrast was one permanent plot (HA) versus one permanent plot (HD), while its Hedges-g variance treated 177 and 127 plant observations as independent group replicates.

Plant observations replicate the response **within** a plot; they do not replicate the plot-level timing exposure.

Therefore the plant-level SMD sampling variance understated the uncertainty of the timing contrast and is not retained for strict H1.

## Current classification

IWE011 remains:

- interaction class: antagonist;
- evidence provenance: direct plant timing + final post-predation reproduction;
- timing metric type: `seasonal_position`;
- timing analysis class: `direct_timing_sensitivity`;
- strict H1 status: unresolved/not currently admitted.

No IWE011 row is present in `data/extraction/direct_effects.csv`.

## Rescue route

A strict effect would require:

1. a focal-season adult *P. fulviguttella* activity/availability series independent of egg receipt or damage; and
2. timing exposure replicated at a compatible inferential unit, such as multiple plot-years prospectively ordered against that adult series.

Any rescued effect remains in `DEP_PEUCEDANUM_KUDO_PROGRAM`.

See `IWE011_TIMING_UNIT_REAUDIT_20260928.md` and `PEUCEDANUM_DEPENDENCY_MAP.md`.
