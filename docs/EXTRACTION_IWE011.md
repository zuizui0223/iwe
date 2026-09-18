# IWE011 extraction adjudication — Peucedanum multivittatum × Phaulernis fulviguttella

Source: Kudo G, Shibata A. 2025. *Phenological selection mosaic of predispersal seed predation affects gender variation in an andromonoecious plant*. Journal of Ecology 113:2832–2845. DOI `10.1111/1365-2745.70130`.

Associated public dataset: HUSCAP item 95572, `Kudo$Shibata_JEcol_Data.zip`.

Status: **closed as timing/context evidence; not strict H1**.

## What the published study establishes

The study follows five alpine plots over 2020–2023 along a flowering phenology gradient. Early-flowering populations experience much greater predispersal seed predation because the focal moth concentrates oviposition in early summer, whereas late-flowering populations largely escape attack.

The published article therefore supplies strong biological evidence that seasonal flowering position changes exposure to a predispersal seed predator and changes final female reproductive success.

## Raw-data audit

The exact HUSCAP archive was downloaded and inspected.

`All_Plots_Data.csv` contains 685 plant rows with:

- `Year`
- `Plot`
- `ID`
- `HflowerN`
- `MflowerN`
- `InitialFruitN`
- `Height`
- `OvipN`
- `FinalFruitN`
- `PredationR`

`HA_Plot_Data.csv` contains 106 plants from the intensive HA plot with flower number, initial/final fruit information, damaged fruits and male-fitness variables.

These files are valuable for reproducing flowering-gradient, oviposition, predation and fitness analyses.

## Why the study does not identify the strict IWE H1 estimand

Strict H1 requires a direct plant–partner temporal-matching exposure such as an overlap index, signed lag with a valid one-sided domain, or an independently measured partner-activity window that can prospectively order plant timing as more versus less matched.

The public source package does **not** contain a repeated date-by-date `Phaulernis` activity or oviposition curve for each plot/year. `OvipN` is a per-plant seasonal total, not a time-localized activity distribution.

Consequently, IWE cannot reconstruct:

`plant flowering distribution × predator activity distribution -> final fitness`

from these data without importing an unobserved predator timing curve.

Plot identity or calendar flowering position also cannot be silently relabelled as synchrony. Doing so would mix site, snowmelt and other environmental differences into the primary exposure.

## Permitted use

IWE011 remains useful as:

- direct seasonal-timing evidence;
- evidence that predator pressure is concentrated in early summer;
- a final-fitness antagonist study;
- context for measurement asymmetry in the antagonist literature;
- a dependence-related companion to IWE010.

It may enter a separately labelled seasonal-timing sensitivity synthesis if that lane is developed prospectively.

## Prohibited use

IWE011 must not contribute a strict H1 effect by:

- correlating `OvipN` with `FinalFruitN` and calling that phenological synchrony;
- treating plot order as a synchrony score;
- inferring a predator activity curve from the narrative alone;
- combining flowering date and total egg load algebraically to manufacture an overlap metric.

## Final adjudication

The record is **context_only**, not `unresolved_strict`.

The limitation is now informational rather than computational: the public article and raw package do not contain the time-resolved partner-activity exposure required by the frozen strict H1 definition.
