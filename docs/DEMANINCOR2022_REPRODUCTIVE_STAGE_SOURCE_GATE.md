# 2022 greenhouse experiment: does temporal matching predict viable offspring?

**Date:** 2026-10-26. Source publication: de Manincor et al. (2026), *Global Change Biology*, DOI [10.1111/gcb.71074](https://doi.org/10.1111/gcb.71074). Original public frozen record [Zenodo 10.5281/zenodo.17830772](https://zenodo.org/records/17830772).

## Scientific reason for candidate

In a 2022 experiment with *Collinsia heterophylla*, *Nemophila menziesii*, *Phacelia campanularia* and *Osmia lignaria*, elevated greenhouse temperatures shifted the flower and bee activity curves but left the reported phenological synchrony approximately preserved, even as flowers, visitation, seed performance and bee reproduction deteriorated. This creates a **strong ecological counterexample** to the claim that high/unchanged temporal overlap guarantees high reproductive service or net plant fitness.

It is also a realistic test of the stronger IWE hypothesis: **is actual interaction and reproduction mediated by independently observed bee abundance/visitation and plant developmental traits rather than by a scalar phenological overlap?** Unlike mere blooming–bee overlap, the original source archive reports germination and seedling survival traits.

## Provenance and identification ceiling

- The authors' open record contains `deManincor-et-al.2025_data_pSEM.zip` (MD5 `33ff77e05c3fb77141ec21226fa3c666`) and `deManincor-et-al.2025_Warming_RScripts.txt` (MD5 `9347d7e1733ce4274a7551775ee5a71f`).
- Original related 2021 experiment in this repo is *another cohort* of the same plant/bee taxa and research group (Zenodo 10.5281/zenodo.7264150), not automatically an independent phylogenetic/evolutionary replication.
- The 2022 experiment assigns **one greenhouse room per temperature treatment**. Multiple plant or bee arenas within each room do not make temperature treatment independently replicated at the room level. Do not claim causal temperature×overlap interactions from plant-row pseudoreplication.
- Source article reports some germination/seedling trials on selected seeds from additional harvested fruits, not necessarily the **same** mother plants/tags as the daily flower–bee observations. This is exactly what original row-key inspection must verify.
- Neither earlier 2021 sampled-fruit seed formation nor this 2022 paper's mixed seed/seedling outcomes is equal to lifetime recruits per individual mother plant without actual survival linkage.

## Current hard gate

The new script `scripts/probe_demanincor2022_stage_zip.py` performs a finite, read-only source ZIP manifest and analysis-script admission audit. It refuses unknown files, validates the author-deposited original MD5s, rejects dangerous source paths and overlarge extraction, reports table column names/possible ID/DOY fields and the original model import/joins without executing author code or adding source rows to GitHub.

**No fresh original-data biological effect is yet claimed.** Only if the exact individual/arena/room+date linkage survives source inspection should an analysis compare on the same final endpoint: calendar/bloom alone, mean bee abundance, bloom×bee matched dates, realized visits, and seed/germination/seedling conversion. Prespecify held-out independently assigned room/year/site where possible; four confounded temperature rooms may not support independent treatment generalization.

**If germination/seedling survival is recorded on selected seeds without individual mother and bloom links, this study remains a valuable outcome-stage counterexample, not a predictive confirmation.** Do not invent missing IDs or average over unmatched strata.

No changes to strict IWE H1 (mutualist two clusters, antagonist zero, mixed zero). Outputs are a derived archive schema/quality report only.

## Reproduce

`python -m scripts.probe_demanincor2022_stage_zip --outdir /tmp/iwe-demanincor2022-original`. Original source files remain hosted by Zenodo; no data files or researchers' scripts are redistributed.
