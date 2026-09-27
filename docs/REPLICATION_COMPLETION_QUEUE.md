# Replication completion queue

Date: 2026-09-27  
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

### 1. Davies & Saccheri 2024 — Cardamine pratensis × Anthocharis cardamines

Why first: this candidate already has the hardest biological pieces in public sources. Female butterfly flight season was independently measured from capture/recapture of females in Dibbinsdale Reserve, while individually labelled ramets were followed every 5–7 days from first flowering to dehiscence. Dryad exposes the plant trajectories needed to reconstruct flowering intervals, potential fecundity and final intact reproductive units.

Access state: public plant data are complete enough for the response, but the Dryad archive does not include the female capture/recapture date list used to define the adult flight window. Public retrieval has now been exhausted across the article/supplements, Dryad, indexed Dibbinsdale publications and the 2016 Liverpool thesis route.

Next action: recover only the source-backed 2012–2014 female capture/recapture dates (or an equivalent numeric flight-window table), then run the already-frozen three-level timing preflight. Core-vs-early and core-vs-late remain separate.

Stop rule: no Figure 4 digitization, no egg-receipt surrogate for adult availability, no response-driven cut-points, no pooling of early and late refugia, and no alteration of the frozen exposure after outcome inspection.

### 2. Wen 2024 — Parnassia wightiana × florivorous beetles

Why second: the strict early/middle/late partner window is already source-defined and final seeds are measured. The only biologically important uncertainty is fate of the initially marked flowers that disappeared through beetle peduncle damage.

Access state: cited Dryad DOI/reviewer route is inactive as of the audit.

Next action: monitor for a corrected/activated repository record or obtain the fate table from a source/archive.

Stop rule: no boxplot digitization, no survivor-only interpretation as net reproduction, and no zero assignment to missing flowers without fate codes.

### 3. James 1998 — Yucca kanabensis × non-pollinating Tegeticula cheater

Why third: the thesis is public and already defines the same-season timing contrast and final damaged/intact seed endpoint.

Access state: public thesis is insufficient for timing-stratified final-seed variance.

Next action: seek plant-level raw data or author/archive summaries.

Stop rule: do not derive an SMD from timing tests that omit final-seed group means and variance.

### 4. Jordano 1987/1990 — Astragalus lusitanicus × Tomares ballus

Why fourth: all biological gates pass, but public variance is nested at inflorescence grain while synchrony is a patch/programme contrast.

Access state: long-form thesis not publicly retrieved.

Next action: thesis/tagged-shoot data.

Stop rule: never use 211/77 nested inflorescences as independent SMD n and never substitute the egg-load sample size into the RSI SE.

### 5. Cirsium canescens × Rhinocyllus conicus

Why fifth: same programme has genuine synchrony and final seed consequences, but public results expose separate synchrony→egg-load and damage→seed-set surfaces.

Access state: programme publications are public; same-unit raw table not yet recovered.

Next action: search programme archives/data for a unit carrying both synchrony and final viable seeds.

Stop rule: do not multiply or splice published model coefficients.

### 6. Eureka 2001 — squarrose knapweed × Larinus/Urophora

Why sixth: this programme has an unusually clean timing architecture for an antagonist candidate. Adult seed predators were sampled independently by 100 sweep-net sweeps each week. After flowering began, up to 200 open flowers per week were tagged as cohorts and collected 4–6 weeks later as mature seed heads for dissection. The public synthesis therefore links an independent adult-activity window to source-defined flower cohorts.

Access state: **public route exhausted**. The 2016 Applied Entomology and Zoology synthesis publishes weekly adult phenology plus cohort infestation percentages. The 2006 Western Society of Weed Science abstract independently confirms fates of individually marked flowerheads and programme-level reproductive impact. The 2001 Rieder et al. paper provides earlier site/year flowerhead-quality context. None exposes weekly Eureka 2001 mature viable-seed means with sampling variance.

Next action: retrieve the original Evans/Rieder/Toler/Newbold 2001 Eureka marked-head field/lab table from an institutional or programme archive. Required unlock: flowering cohort/date plus final mature viable-seed production and variance-bearing information at the same marked-head unit.

Stop rule: do not repeat generic public searches; do not use infestation percentage as plant fitness; do not infer seed counts merely because heads were dissected; do not splice seed-destruction values from California, other sites or other years into the 2001 Eureka timing programme.

## What this queue does not do

The queue does not:

- lower the two-independent-clusters/class requirement;
- change the native SMD target;
- turn inaccessible data into evidence;
- treat a retrieval ranking as evidence quality;
- authorize combining separate studies or model surfaces into a synthetic effect.

It is an operational anti-loop device: a candidate either advances by satisfying its registered unlock condition or remains blocked.
