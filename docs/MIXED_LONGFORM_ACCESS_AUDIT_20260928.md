# Mixed long-form access audit — 2026-09-28

This audit separates **source discovery/access** from **biological eligibility** for the two legacy mixed-system completion routes that do not require author contact.

## Hurlburt 2004 — public thesis located

Candidate: `MIX002_HURLBURT_2004`  
System: *Yucca glauca × Tegeticula yuccasella*  
Priority: P1  
Current blocker: `blocked_timing_linkage`

### Repository object

University of Alberta Libraries Scholaris now exposes the dissertation as a public item:

- Donna Darlene Hurlburt (2004)
- *Persistence of the moth: yukka mutualism at the northern edge of range*
- DOI: `10.7939/r3-fe1d-kj80`
- primary file: `NQ95948.pdf`
- file size reported by the repository: 7.27 MB
- PhD, University of Alberta

The title spelling `yukka` above follows the current repository metadata. Government recovery/status documents cite the same dissertation as *Persistence of the moth-yucca mutualism at the northern edge of range*, 179 pp.

The previous route state `longform_not_public` was therefore wrong. The source is public; this execution environment receiving HTTP 403 from Scholaris is an execution/access limitation, not source unavailability.

### Why the thesis remains high value

Independent public programme summaries establish that the Onefour work contains:

- repeated adult moth observations during the flowering season;
- marked flowering clones/inflorescences;
- fruit-set follow-up;
- mature-fruit dissections;
- multi-year observations spanning 1999–2003.

These facts make the missing quantity narrow: whether the thesis tables/appendices preserve a **within-season, date-resolved join** from plant flowering position and adult *Tegeticula* availability into final fruit or viable-seed reproduction with variance.

Annual moth-density and fruit indices remain insufficient because they erase the phenological contrast.

### Executable next step

Retrieve `NQ95948.pdf` from the DOI/repository and audit, in this order:

1. table of contents and list of tables;
2. methods defining adult *Tegeticula yuccasella* counts through flowering;
3. identifiers used for marked clones/inflorescences;
4. final fruit/seed variables and their sampling units;
5. any date/cohort-level table that carries both timing and final reproduction;
6. variance-bearing summaries or raw-unit data.

No author contact is needed unless the public PDF itself proves to omit the required table.

## Bopp 2003 — library/ILL target pinned

Candidate: `MIX002_BOPP_2004`  
System: *Silene latifolia / S. dioica × Hadena bicruris*  
Priority: P2  
Current blocker: `blocked_timing_linkage`

### Exact long-form source

Sigrun Bopp (2003), *Parasitismus oder Symbiose? Beziehungen zwischen einem parasitischen Bestäuber (Hadena bicruris HUFN., Lepidoptera: Noctuidae) und seinen Wirtspflanzen (Silene-Arten, Caryophyllaceae)*.

- series: Zoologica 152
- publisher: Schweizerbart, Stuttgart
- extent: X + 140 pages
- tables: 36
- ISBN: `978-3-510-55039-5`

SLUB Dresden catalogue confirms the volume. No public digitized copy was recovered in the current search.

### Why the 2004 Oikos article is insufficient

The Oikos paper reports plant flowering and *H. bicruris* oviposition phenology, but the apparent field moth-activity period is reconstructed from eggs newly deposited in host flowers. Egg receipt depends on host availability and host choice and therefore cannot serve as an independent adult-partner availability curve under the IWE timing contract.

The paper also emphasizes oviposition choice and larval performance rather than a linked final post-seed-predation plant reproductive endpoint.

### Exact rescue test for the monograph

The monograph can promote the programme only if its 36 tables resolve **both**:

1. independent adult *H. bicruris* activity/availability through the focal season, measured separately from host egg receipt; and
2. final host fruit/seed reproduction after larval cost, with variance at a defensible unit that can be linked to the timing contrast.

Finding only one surface does not promote the candidate.

### No-contact next step

Acquire Zoologica 152 by library/ILL using ISBN `978-3-510-55039-5`, then audit the 36 tables against the two-part rescue test. This path does not require contacting the author.

## Registry consequence

- Hurlburt access becomes `repository_public_pending_audit`; public search is complete and the source itself is identified.
- Bopp remains `longform_not_public`, but its no-contact retrieval route is now a precise ISBN-based library/ILL request rather than an open-ended search.
- Neither change adds evidence or an independent cluster. Both only make the completion queue truthful and executable.
