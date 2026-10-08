# Cardamine public auxiliary timing audit — 2026-09-28

Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024`  
Primary source: Davies & Saccheri (2024), DOI `10.1002/ece3.11330`  
Plant data: Dryad DOI `10.5061/dryad.v9s4mw741`  
Decision: **retain P1 `blocked_timing_linkage`; insert one final no-contact public-asset retrieval step before archive/contact**

## Exact missing object

The plant side is no longer the blocker.

The 2024 Dryad archive contains the six 2012–2014 early/late ecotype transect workbooks, with plant-level day of year, open flowers, buds, seed-pods, eggs, larvae and dehiscence information. The repository already has a frozen response-blind timing rule and a frozen realized-reproduction outcome rule.

The only missing object is one of:

1. the 2012–2014 female *Anthocharis cardamines* capture + recapture event DOYs used to construct Figure 4; or
2. exact source-backed year-specific q10/q90 female flight-window boundaries equivalent to those events.

Once recovered, no further exposure design is needed. The data can go directly through the existing provenance-guarded Cardamine preflight.

## 2016 Liverpool thesis route

Davies (2016), University of Liverpool thesis DOI `10.17638/03001785`, is a same-programme long-form source.

The accessible indexed text confirms that the mark-release-recapture/POPAN component used for male/female emergence schedules covers **2005–2010**. That timing series is biologically relevant background but it predates the focal 2012–2014 Cardamine transects.

Therefore:

- 2005–2010 female emergence schedules cannot substitute for the 2012–2014 female flight distributions;
- no back-projection or climatological reuse is allowed;
- the earlier MRR series remains context only.

## Davies 2019 Ecology auxiliary route

Davies (2019), *Ecology* 100:e02612, DOI `10.1002/ecy.2612`, analyzes *A. cardamines* phenology in one wild population over 14 generations and explicitly studies emergence timing and emergence synchronization.

The Wiley record publicly exposes three supporting-information files:

- `ecy2612-sup-0001-AppendixS1.pdf` — 143.4 KB;
- `ecy2612-sup-0002-AppendixS2.pdf` — 401.8 KB;
- `ecy2612-sup-0003-AppendixS3.pdf` — 146.6 KB.

Those exact supplement endpoints were reached in the 2026-09-28 audit, but all three returned HTTP 403 in the current execution environment.

The public article metadata/abstract establishes only that the programme quantified emergence phenology and synchronization across 14 generations. It does **not** expose the 2012–2014 female capture+recapture event distribution or exact q10/q90 values in the accessible HTML.

This makes the three supplements a legitimate no-contact retrieval target, but not evidence yet.

### Acceptance test for the 2019 supplements

A supplement can unlock Cardamine only if it contains source-backed 2012, 2013 and 2014 female timing at sufficient resolution to reproduce the 2024 Figure 4 flight window, for example:

- female capture/recapture event dates;
- a year-specific female event table;
- exact q10 and q90 boundaries from the same event distribution.

A year-level mean first-capture date, SD of first-capture date, fitted emergence date, or generic synchronization statistic is **not** equivalent to the 2024 capture+recapture distribution and must not be substituted.

## 2024 official Figure 4 PowerPoint route

The Wiley article exposes an official PowerPoint download endpoint for Figure 4:

`action/downloadFigures?doi=10.1002%2Fece3.11330&id=ece311330-fig-0004&partId=`

The endpoint is real: the current web execution reaches it and identifies the returned content as `application/vnd.ms-powerpoint`, but cannot ingest that binary content type. Direct container retrieval is also blocked by the execution environment's network/DNS restrictions.

This asset is therefore another concrete no-contact target.

### Acceptance test for the PowerPoint

The PowerPoint may be used only if inspection shows that it contains **source numerical data**, such as:

- embedded chart data;
- editable chart-series values;
- an embedded spreadsheet/data table with year-specific female event or quantile values.

A raster image, vector artwork, box/whisker geometry, or editable drawing primitives without an embedded source data table are **not** accepted. Reading box positions or coordinates would be figure digitization, which remains prohibited.

## Supporting information of the 2024 paper

The 2024 article lists:

- `ece311330-sup-0001-TableS1.docx`;
- `ece311330-sup-0002-Figures.docx`.

The public metadata identify these as Table S1 and Figure S1, not as the missing female event table. They remain low-priority cross-checks but do not change the blocker.

## No-contact retrieval order

Before any author or institutional data request:

1. retrieve the official 2024 Figure 4 PowerPoint in a normal browser/library environment and inspect only for embedded source data;
2. retrieve the three 2019 Ecology appendices and search for source-backed 2012–2014 female event dates or exact q10/q90 values;
3. optionally inspect the two 2024 supporting Word files for an explicit numeric flight-window table.

If none contains the exact timing object, the public/no-contact route is exhausted and the next step becomes a narrowly scoped institutional archive or author request for the female event DOYs/q10/q90 values only.

## Stop rules

Do not:

- manually digitize Figure 4;
- infer q10/q90 from box/whisker pixel or vector coordinates;
- use egg receipt as adult availability;
- substitute 2005–2010 POPAN/MRR dates;
- substitute 2019 mean first-capture or emergence-synchronization summaries;
- change the frozen early-refugium/core-flight/late-refugium thresholds after outcome inspection;
- pool early and late refugia.

## Registry consequence

The completion route is now classified `public_asset_runtime_blocked` with next action `retrieve_public_asset`.

This does not promote the candidate and does not add evidence. It only prevents a premature move to email/contact while identified public assets remain uninspected outside the current runtime.

## 2026-10-08 official publisher binary route: independently tested access

To avoid repeated generic searching, the exact source-linked binary files now
have one isolated, nonpromoting access audit:

- 2024 Davies & Saccheri **Figure 4 PowerPoint**: the official Wiley
  `action/downloadFigures` endpoint for `ece311330-fig-0004`;
- 2019 Davies *Ecology* **Appendices S1–S3**: the three official
  `ecy2612-sup-0001/0002/0003-AppendixS*.pdf` files.

The repository code is `scripts/probe_cardamine_public_timing_assets.py`,
its no-network tests are `tests/test_cardamine_public_timing_asset_probe.py`,
and the one-time public retrieval is
`.github/workflows/cardamine-publisher-asset-probe.yml`.

The probe **does not digitize the figure**, infer a flight distribution from
shapes or boxes, or treat an Office/PDF signature as numeric source data.
For Office Open XML, it reports any `ppt/charts/` or
`ppt/embeddings/` objects merely as *candidates to inspect*; an old binary
OLE PowerPoint is classified as unknown numeric status even if downloaded.
Source authenticity, chart-series identity, 2012–2014 year coverage,
female capture-versus-recapture grain, and exact q10/q90 values all still
require inspection before Cardamine's timing/final-fitness preflight.

**Observed outcome (GitHub-hosted runner 2026-10-08):** the source-asset
workflow [run 37752302689](https://github.com/zuizui0223/iwe/actions/runs/37752302689)
passed **9 no-network tests**, but recovered **0/4 source files**. The 2024
official Figure 4 PowerPoint and all three 2019 Ecology supporting PDFs
independently returned **HTTP 403**. Workflow `success` describes robust
probe execution, not successful document retrieval. The downloadable artifact
contains an access manifest, **not the publication binary files**.

This closes the identified **anonymous direct-publisher/GitHub-runner route
in this environment** without establishing that the public materials are
globally inaccessible or that they contain no embedded source data.
The source-backed 2012–2014 female capture/recapture series and/or exact
year-specific flight q10/q90 values remain **unrecovered**. P1
`blocked_timing_linkage` and the frozen preflight are unchanged.
The next legitimate step is a permitted institutional/library binary
download or narrowly scoped archive request. Do not repeat anonymous
downloads, digitize plot geometry, substitute egg receipt, or count
the existing ecological stage/final-fate contrasts as a strict timing SMD.
