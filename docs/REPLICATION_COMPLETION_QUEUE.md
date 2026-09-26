# Replication completion queue

Date: 2026-09-26  
Status: executable retrieval queue; does not change the frozen estimand

## Purpose

IWE now has enough near-miss literature that repeated generic searching is itself a source of research drift. The completion queue separates two questions that were previously mixed together:

1. **Is the biological programme eligible in principle?**
2. **Is the exact missing datum still recoverable through a concrete route?**

The candidate ledger answers the first question. `data/registry/replication_completion_routes.csv` answers the second.

A route is registered only for a candidate that is already P1/P2 and blocked rather than rejected or ready.

## Mixed order

### 1. Hurlburt 2004 — Yucca glauca × Tegeticula yuccasella

Why first: the programme architecture already contains repeated within-season adult-moth observations, marked flowering units, fruit set and mature-fruit dissections. The missing object is a date-resolved timing-to-final-fitness linkage, not an entirely new measurement domain.

Access state: long-form thesis not publicly retrieved.

Next action: obtain the University of Alberta dissertation or archived Onefour field tables through institutional/library or author routes.

Stop rule: do not keep mining annual government summaries and do not equate annual moth density with synchrony.

### 2. Rentería/Cantú — Yucca filifera × Tegeticula

Why third: article and thesis have already been audited. They contain partner timing and final seed fate, but the mature-fruit records are pooled across flowering cohorts.

Access state: thesis already recovered; public-source search is exhausted.

Next action: original fruit-level field records or author/archive material.

Stop rule: never assign pooled fruits to March/April/May without source-backed provenance.

### 3. Bopp 2003/2004 — Silene × Hadena

Why third: the Oikos paper measures flowering and oviposition phenology, but its field “moth activity” series is inferred from newly deposited eggs inside host flowers. Egg receipt is a realized interaction outcome and depends on host availability/preference, so it is not an independent partner-availability curve under the frozen timing gate. The published plant-side endpoint is also larval performance rather than final post-cost plant reproduction.

Access state: long-form Zoologica 152 monograph is catalogue-confirmed but not publicly retrieved.

Next action: inspect the monograph only for a two-part rescue: an independent focal-season adult-moth activity/availability series AND a linked final fruit/seed reproductive surface with variance.

Stop rule: do not treat egg deposition as independent partner availability, do not use larval performance as plant fitness, and do not return Bopp to P1 unless both missing surfaces are source-backed.

### 4. Thomas, Hoover & Busby / USGS 2022–2023 — Yucca jaegeriana × Tegeticula antithetica

Why fourth: the project design directly measures moth visitation, pod production, fertile seeds and larval damage on tagged trees, but only preliminary conference material is currently citable and the 2023 poster explicitly says the results are preliminary/do not cite.

Access state: active project; final quantitative source/data release not recovered.

Next action: monitor for the final publication or released dataset, then audit whether timing exposure and post-cost reproduction share a compatible biological unit before extraction.

Stop rule: do not use preliminary poster values as primary evidence and do not substitute year-level moth abundance for a strict within-season synchrony contrast.

## Antagonist order

### 1. Wen 2024 — Parnassia wightiana × florivorous beetles

Why first: the strict early/middle/late partner window is already source-defined and final seeds are measured. The only biologically important uncertainty is fate of the initially marked flowers that disappeared through beetle peduncle damage.

Access state: cited Dryad DOI/reviewer route is inactive as of the audit.

Next action: monitor for a corrected/activated repository record or obtain the fate table from a source/archive.

Stop rule: no boxplot digitization, no survivor-only interpretation as net reproduction, and no zero assignment to missing flowers without fate codes.

### 2. James 1998 — Yucca kanabensis × non-pollinating Tegeticula cheater

Why second: the thesis is public and already defines the same-season timing contrast and final damaged/intact seed endpoint.

Access state: public thesis is insufficient for timing-stratified final-seed variance.

Next action: seek plant-level raw data or author/archive summaries.

Stop rule: do not derive an SMD from timing tests that omit final-seed group means and variance.

### 3. Jordano 1987/1990 — Astragalus lusitanicus × Tomares ballus

Why third: all biological gates pass, but public variance is nested at inflorescence grain while synchrony is a patch/programme contrast.

Access state: long-form thesis not publicly retrieved.

Next action: thesis/tagged-shoot data.

Stop rule: never use 211/77 nested inflorescences as independent SMD n and never substitute the egg-load sample size into the RSI SE.

### 4. Cirsium canescens × Rhinocyllus conicus

Why fourth: same programme has genuine synchrony and final seed consequences, but public results expose separate synchrony→egg-load and damage→seed-set surfaces.

Access state: programme publications are public; same-unit raw table not yet recovered.

Next action: search programme archives/data for a unit carrying both synchrony and final viable seeds.

Stop rule: do not multiply or splice published model coefficients.

## What this queue does not do

The queue does not:

- lower the two-independent-clusters/class requirement;
- change the native SMD target;
- turn inaccessible data into evidence;
- treat a retrieval ranking as evidence quality;
- authorize combining separate studies or model surfaces into a synthetic effect.

It is an operational anti-loop device: a candidate either advances by satisfying its registered unlock condition or remains blocked.
