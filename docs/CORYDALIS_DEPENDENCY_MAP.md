# Corydalis dependency map

Date: 2026-09-21
Status: frozen before adding IWE002 quantitative effects

## Purpose

The Corydalis literature contains repeated observations from the same research programme. Publication identifiers are therefore not independent-effect identifiers.

This map records confirmed and unresolved overlap before additional effects are added.

## Confirmed programme structure

| Record | Population/site | Years represented | Relationship | Dependence decision |
|---|---|---|---|---|
| IWE001 NFP | Nopporo Forest Park | 1999–2012, with complete seed-set + mismatch rows in 1999–2003 and 2005–2012 | original long-term Nopporo series | `DEP_CORYDALIS_KUDO_LONGTERM` |
| IWE001 TOEF | Tomakomai Experimental Forest | 1999–2008, with complete rows in 1999–2003 and 2005–2008 | same 2013 multi-site study | `DEP_CORYDALIS_KUDO_LONGTERM` |
| IWE001 JOZ | Jozankei forest | complete rows in 2002, 2003, 2007–2009, 2011, 2012 | same 2013 multi-site study | `DEP_CORYDALIS_KUDO_LONGTERM` |
| IWE002 long-term | Nopporo | 1999–2017; natural seed set measured every year except 2004 | direct extension of IWE001 NFP | any future row must use `DEP_CORYDALIS_KUDO_LONGTERM` |
| IWE002 snow-removal experiment | Nopporo | 2014–2017 observations; removal applied 2014–2016 | same population/programme and partially concurrent with extended monitoring | any future row defaults to `DEP_CORYDALIS_KUDO_LONGTERM` unless a stronger nested model is implemented |

## Direct overlap: IWE001 NFP ↔ IWE002

The IWE002 manuscript describes the 2013 paper as the authors' previous study and states that the present long-term monitoring was conducted in Nopporo from 1999–2017.

The IWE001 NFP extraction uses the Nopporo Forest Park series through 2012. Its complete seed-set + mismatch years are:

`1999, 2000, 2001, 2002, 2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012`.

Those years are contained directly inside the IWE002 1999–2017 series. IWE002 is therefore an extension of the same longitudinal evidence, not a new independent replication.

No analysis may count IWE001 NFP and an IWE002 long-term effect as two independent studies.

## Why the cluster is programme-level

The current IWE schema has one dependence level, `dependence_id`.

IWE001 already contains three site effects from one publication, and those effects were deliberately not treated as independent publication-level replicates. IWE002 adds a confirmed longitudinal extension at Nopporo plus an experiment embedded in the same population and years.

Until IWE implements nested/crossed dependence levels, the conservative executable representation is one programme-level cluster:

`DEP_CORYDALIS_KUDO_LONGTERM`.

This may sacrifice some efficiency, but it prevents known repeated evidence from producing pseudo-replication.

## IWE003 — unresolved overlap

IWE003 (Liew & Kudo 2026) compares four Corydalis ambigua populations with different snowmelt regimes over 3–5 years, with annual variation reported for 2020–2024. Its abstract also refers to long-term monitoring in an early-snowmelt population.

The publicly available abstract does not identify the four site names or establish which, if any, is Nopporo, Tomakomai, or Jozankei.

Therefore:

- IWE003 remains `unresolved` for dependency mapping;
- no IWE003 quantitative effect may be assigned an independent cluster merely because its publication year is later;
- site identity and observation-year overlap must be recovered from full text/data before extraction.

If a population is confirmed to continue the Kudo Nopporo/earlier programme, it must inherit `DEP_CORYDALIS_KUDO_LONGTERM` under the current one-level scheme.

## Analysis consequence

The programme-level cluster is the unit used by:

- CR1 uncertainty in `cluster_robust_summary()`;
- leave-one-dependence sensitivity;
- H1 evaluability counts.

Multiple Corydalis effect rows may increase descriptive information, but they do not mechanically increase `m_dependence`.
