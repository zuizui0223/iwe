# IWE032: public PMC Cloud supplementary-source audit (2026-11-24)

Status: **source recovered, required female-flight timing not recovered**.
This is a non-promoting source-readiness receipt; it does not create or replace a strict H1 effect.

## Motivation and source

The 2024 Davies & Saccheri study (DOI [10.1002/ece3.11330](https://doi.org/10.1002/ece3.11330); PMCID **PMC11056787**) defined the 2012–2014 *Anthocharis cardamines* female flight periods from **female capture and recapture dates**. Egg receipt and oviposition curves in the plant transect data are separate, realized-interaction variables.

Prior source-asset probes [documented on pivot](https://github.com/zuizui0223/iwe/blob/pivot/interaction-window-landscape/docs/CARDAMINE_PUBLIC_TIMING_AUXILIARY_AUDIT_20260928.md) received HTTP 403 on the publisher endpoints for Figure 4 PowerPoint and Davies (2019) Ecology Appendices S1–S3. In August 2026 PMC replaced its legacy FTP/OA API with the [official open-access AWS Cloud Service](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/). This run used that official NLM channel, not scraped publisher geometry or an unauthorized mirror.

## Actual successful retrieval

The [Github Actions receipt](https://github.com/zuizui0223/iwe/actions/runs/45377595390) shows:

- Official S3 metadata `PMC11056787.1.json`: PMID/PMCID/DOI identity checked; licence **CC BY**.
- Metadata property `media_urls` is empty, **but this is not proof of missing supplementary files**.
- The S3 ListObjectsV2 endpoint for prefix `PMC11056787.1/` returned **14 source objects**, including two DOCX supplements.
- `ECE3-14-e11330-s001.docx` (Table S1): **19,086 bytes**, SHA256 `33248aa9f9cde4cf278da410c4667c109e597c1cba7d1d4b61df86b19965434a`. Extracted text has 2012/2013/2014 tokens but **no female or capture/recapture text tokens**.
- `ECE3-14-e11330-s002.docx` (Figure S1): **403,543 bytes**, SHA256 `f0cbb7f190c9e4c27a356765c42e5b30518e40377581689808691ff8823a48a8`. Extracted text has a female token but **no capture/recapture or DOY text tokens**.
- DOI/source checks passed and the metadata-only artifact was retained; no publisher binaries were committed to GitHub.

The prior publisher-403 finding is therefore **partly superseded**: the two 2024 supplementary Word documents are actually available via NLM's official Cloud Service. The 2019 Ecology appendices and the official 2024 Figure 4 PowerPoint remain separate unresolved sources.

**No new adult monitoring events, numeric annual female q10/q90 quantiles, or source-authorized calendar-day boundaries were extracted.** Absence of keyword tokens from Word paragraphs is not a proof that pictures or unattested objects contain no usable source data. An additional archive-part scan checks chart/embedded spreadsheet parts separately, but no graphical digitization is permitted regardless of the outcome.

## Scientific decisions / admission firewall

The plant side remains backed by the six [Dryad 2012–2014 transect workbooks](https://doi.org/10.5061/dryad.v9s4mw741). They do not measure independent adult activity. Therefore:

1. Keep `ANT002_CARDAMINE_ANTHOCHARIS_2024` and `IWE032` **blocked_timing_linkage**; no new strict-H1 SMD or antagonist dependence cluster.
2. Do not use observed eggs, late larvae, published percent predation, image axis positions, 2005–2010 MRR series or 2019 mean emergence as substitutes for the 2012–2014 female capture/recapture distribution.
3. Figure 4 Day 1 is a **year-specific relative** date, not calendar DOY. Any genuine numeric events require a verified same-year origin before joining plant calendar DOYs.
4. The earliest observed first open flower is an upper bound on true individual flowering onset unless a source-backed preceding non-flowering visit exists. Keep the existing partial-identification and 0/3/5/7/10/14-day lag sensitivities.
5. Next same-unit gate: only if 2012–2014 female events (or exact annual q10/q90) are source-backed, run `scripts/run_cardamine_preflight.py` on source-normalized plants, keeping core-vs-early and core-vs-late as dependent but separate contrasts. Observe the `adult_provenance.json` and final intact RU variance contract.
6. Study-level phase/fate observations (34% vs 4% dehiscence before larval completion; chi-square p=.003) are valuable **stage-to-final-fate mechanisms**, not a contemporaneous female-adult timing SMD.

## Reproducibility and stop rule

The non-promoting official cloud probe lives in `scripts/probe_cardamine_pmc_cloud.py`; tests `tests/test_cardamine_pmc_cloud.py`; workflow `.github/workflows/cardamine-pmc-cloud-probe.yml`. It checks exact DOIs and licences, limits retrieval to two source-named DOCX files and writes only hash/part/keyword diagnostics.

After inspecting embedded numeric objects, if no source-certified 2012–2014 female event/quantile series is found, close this NLM Cloud route as **retrieval-success / timing-not-found** and do not repeat general public searches. The next distinct no-contact candidates are the archived 2019 appendices (three separate PDFs) or original Figure 4 PowerPoint **only when accessible and containing authored numeric tables**; otherwise maintain the institutional/archive request route. This audit does not email authors.
