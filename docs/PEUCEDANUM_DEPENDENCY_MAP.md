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

## Current extraction boundary

IWE010 and IWE011 remain a valuable direct seasonal-timing programme, but neither currently supplies a strict H1 effect.

Two independent problems were identified in the 2026-09-28 re-audit.

First, the programme's source-defined *Phaulernis* seasonal window is based on oviposition/egg observations on host umbels rather than a contemporaneous quantitative adult-moth abundance/availability series. Egg receipt cannot satisfy the frozen independent-partner-window gate.

Second, the former IWE011 HA-versus-HD SMD compared one permanent plot with one permanent plot while using plant response observations as independent group n. Response replication within a plot cannot substitute for replication of a plot-level timing exposure.

IWE010 has an additional outcome problem: its published fruit number is measured before intensive predation and deliberately includes later-predated fruits.

IWE011 does measure final intact mature fruits, but the former strict SMD has therefore been withdrawn.

## Rescue architecture

A future Peucedanum strict effect requires:

1. source-backed focal-season adult *P. fulviguttella* activity/availability measured independently of egg receipt/damage;
2. a timing exposure with genuine replication at the inferential unit, for example multiple plot-years prospectively ordered relative to that adult window; and
3. a final post-predation reproductive response summarized at that compatible structure.

Any rescued quantitative effect from either publication remains in `DEP_PEUCEDANUM_KUDO_PROGRAM`.

See `IWE011_TIMING_UNIT_REAUDIT_20260928.md`.
