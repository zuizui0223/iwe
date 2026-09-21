# Peucedanum dependency map

Date: 2026-09-21
Status: frozen before adding antagonist quantitative effects

## Purpose

IWE010 and IWE011 are successive studies of the same *Peucedanum multivittatum* × *Phaulernis fulviguttella* research programme in the Taisetsu Mountains.

They use different observation periods but overlapping permanent plots and the same phenological gradient. Publication year therefore cannot be used as an independence boundary.

## Confirmed plot continuity

IWE010 (Kudo & Shibata 2021) surveyed nine populations during 2017–2019:

`HA, PK, KE, HL, HC, HD, KD, KL, KT`.

IWE011 (Kudo & Shibata 2025) explicitly states that its five plots

`HA, HL, HC, KD, HD`

were established in 2017 and that the previous 2017–2019 study reported intense predation in the early plots HA/HL and little predation in the late plots KD/HD.

Thus all five IWE011 plots are contained in the IWE010 landscape/programme.

## Time periods

- IWE010: 2017–2019.
- IWE011: 2020–2023 for the five-plot survey, plus a 2021 experiment in HA.

The observation years do not overlap between the published landscape surveys, but the sites, focal species pair, phenological mechanism and research programme do.

## Executable dependence decision

Under the current one-level IWE dependence representation, any effect from either publication uses:

`DEP_PEUCEDANUM_KUDO_PROGRAM`.

This is conservative. A future nested model could separate non-overlapping years while retaining plot/programme correlation, but the current schema cannot represent those levels simultaneously without understating dependence.

## IWE010 extraction boundary

The published 2021 fruit-number analysis was designed to represent pollination success: fruits later damaged by the seed predator were deliberately included in the recorded fruit number.

Therefore that published fruit-set coefficient is not a final post-predation reproductive outcome for strict antagonist H1.

The archived Dryad workbook includes reproductive data and potentially permits reconstruction of intact mature fruit production for 2018–2019. Until such a reconstruction and its sampling variance are audited, IWE010 remains quantitatively unresolved for strict H1.

## IWE011 extraction route

IWE011 directly counts intact mature fruits after predation and reports final fruit-set means for the five plots.

Predator moths concentrate oviposition in mid- to late July. Plot HA flowers in mid-July and is the highest-overlap end of the measured gradient; plot HD flowers in early to late August and is the latest/lowest-overlap end.

The HA-versus-HD contrast is therefore fixed using timing information rather than reproductive outcome values. The reconstructed effect is documented in `EXTRACTION_IWE011.md`.

## Analysis consequence

Multiple IWE010/IWE011 effect rows can increase descriptive coverage, but they do not mechanically add independent programme clusters. CR1 uncertainty, leave-one-dependence sensitivity and H1 evaluability use the shared `DEP_PEUCEDANUM_KUDO_PROGRAM` identifier.
