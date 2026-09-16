# IWE systematic search completion rule v1

Freeze date: 2026-09-17
Status: prospective for literature expansion after IWE001-IWE040

## Scope boundary

IWE001-IWE040 are the **discovery corpus**. They were assembled iteratively while the estimand, timing contract, and evidence lanes were being clarified. They may be used for the preregistered H1 analysis when eligible, but they cannot serve as an independent confirmation set for hypotheses first recognized during their screening (especially the antagonist nonlinear/shape observation).

All unique empirical citations first identified after this freeze enter the prospective expansion corpus.

## Search question

Recover empirical plant-animal studies in which temporal matching, mismatch, overlap, or flowering position relative to a biologically identified animal interaction window can be connected to a quantitative plant reproductive or fitness outcome.

The search must recover null, adverse, nonlinear and non-significant outcomes as well as supportive outcomes.

## Search sources

The minimum reproducible search has four components.

### A. Finite backward-search seed sets

Screen the empirical source lists from:

1. Elzinga et al. 2007, *Time after time: flowering phenology and biotic interactions*, DOI `10.1016/j.tree.2007.05.006`;
2. Munguía-Rosas et al. 2011, *Meta-analysis of phenotypic selection on flowering phenology suggests that early flowering plants are favoured*, DOI `10.1111/j.1461-0248.2011.01601.x`, including the supporting source/effect tables.

Every plant-animal empirical source involving flowering/reproductive timing is logged, even when it is excluded from IWE.

### B. Reproducible database queries

Run the following concept families in OpenAlex and PubMed through the freeze/search date. Equivalent database syntax may be used, but the concepts must not be narrowed after seeing outcomes.

**Mutualist query family**

`(phenolog* OR synchron* OR mismatch OR overlap OR "flowering time" OR "flowering date") AND (pollinat* OR "pollinator emergence" OR "pollinator activity") AND ("seed set" OR "fruit set" OR fecund* OR fitness OR reproduction)`

**Antagonist query family**

`(phenolog* OR synchron* OR mismatch OR overlap OR "flowering time" OR "flowering date") AND ("seed predator" OR "seed predation" OR florivor* OR "flower predator" OR oviposition OR herbivor*) AND ("seed set" OR "fruit set" OR fecund* OR fitness OR reproduction)`

**Mixed/nursery-pollination query family**

`(phenolog* OR synchron* OR mismatch OR overlap OR "flowering time") AND ("nursery pollination" OR "pollinating seed predator" OR Hadena OR Epicephala OR Tegeticula OR Parategeticula OR Chiastocheta OR Greya OR Agaonidae OR "fig wasp") AND (seed* OR fruit* OR fecund* OR fitness OR reproduction)`

No lower publication-year limit is used.

### C. Forward-citation search

Forward-screen citations to the two seed syntheses and to every strict-H1 admitted or unresolved-strict empirical paper. A forward-citing paper is retained for title/abstract screening if it contains at least one timing concept and one plant reproductive/fitness concept.

### D. Citation closure

For every newly admitted or unresolved-strict study, screen its references for earlier empirical studies of the same plant-animal system and its citing literature for later studies. Newly found citations are recursively logged until no unlogged eligible/unresolved citation is produced.

## Deduplication

Deduplicate in this order:

1. DOI (case-insensitive canonical form);
2. other persistent source ID;
3. normalized title + first author + year.

Multiple publications from the same biological dataset remain separate publication records but receive a shared `dependence_id` or dataset-family identifier during extraction.

## Screening decisions

Each record receives exactly one screening state:

- `include` — eligible strict-H1 candidate;
- `include_shape` — direct timing + final fitness but irreducibly nonlinear/bidirectional for a single H1 slope;
- `context_only` — biologically relevant but missing the strict timing/fitness identification required by H1;
- `exclude` — outside the biological/evidence scope;
- `unresolved` / `unresolved_strict` — source information is insufficient for final adjudication.

A class is never balanced by promoting weaker evidence from another class.

## Completion rule

The systematic search is complete only when all of the following are true:

1. every citation from the two finite seed sets has a logged screening decision;
2. every result returned by the frozen OpenAlex and PubMed query families through the search date has been deduplicated and screened;
3. forward-citation screening is complete for both seed syntheses and all admitted/unresolved-strict studies;
4. recursive citation closure produces zero new unlogged empirical candidates in one complete pass;
5. every `unresolved_strict` record has either been adjudicated or has a documented inaccessible-information reason that cannot be repaired from article, supplement, repository, or linked data;
6. the final query rerun adds zero new unique records published on or before the original search cutoff.

The number of eligible effects, their signs, or whether H1 becomes statistically evaluable is **not** a stopping criterion.

## Prospective holdout for the screening-informed shape hypothesis

The antagonist nonlinear/shape expectation was recognized after outcomes in IWE001-IWE040 were visible. It is therefore discovery-only in that corpus.

For citations first identified after this freeze:

1. assign a stable biological `system_cluster_key` before reading the full result section, using plant genus + focal animal genus (or the narrowest defensible animal guild when genus is unavailable);
2. hash the normalized `system_cluster_key` with SHA-256;
3. clusters whose hexadecimal hash begins with `0`, `1`, `2`, or `3` are reserved as **shape holdout** (approximately 25% of clusters);
4. holdout papers may be screened for basic eligibility and source availability, but the direction/shape of their timing-fitness result is not used to formulate or tune the discovery shape model;
5. a quantitative confirmatory shape model must be frozen using non-holdout evidence before holdout outcome extraction is analyzed.

This holdout applies only to the post-hoc shape hypothesis. It does not remove eligible studies from the preregistered H1 meta-analysis after the holdout test is complete.

## Prior-art boundary

Munguía-Rosas et al. 2011 already meta-analyzed phenotypic selection on plant flowering time and among-plant flowering synchrony. IWE does not claim novelty for meta-analyzing flowering phenology per se.

IWE's distinct estimand is temporal matching between the plant and a biologically identified interaction partner, with interaction role as a moderator and with direct-vs-proxy and timing-shape distinctions enforced prospectively.

## Valid terminal outcomes

The search may terminate with any of these outcomes:

- enough comparable evidence for the preregistered three-class H1 meta-analysis;
- H1 evaluable only for a subset of interaction classes;
- strict evidence too sparse for cross-class H1, but a systematic evidence-architecture result showing why the classes are not presently comparable;
- a well-supported null or equivalence pattern.

No positive ecological pattern is required for completion.
