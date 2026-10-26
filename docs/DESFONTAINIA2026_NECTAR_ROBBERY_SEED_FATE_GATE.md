# Desfontainia 2026: nectar robbery, actual pollination and buffered seed production

**Date:** 2026-10-26. **Status:** original-source admission pending. Independent visitor-role conflict/buffering candidate, NOT a strict IWE H1 effect or measured adult–larval phase.

**Study:** Valdivia & Orellana (2026), *Ecology and Evolution* 16, e73933, [DOI 10.1002/ece3.73933](https://doi.org/10.1002/ece3.73933); source [Zenodo DOI 10.5281/zenodo.18895003](https://zenodo.org/records/18895003). Original pinned `Raw Data Desfontainia fulgens.xlsx` MD5 `e7e59a06cc3eb7aed636620a85a1ea98`, author R script MD5 `9fd405c399ecad9c3fe54d1cd70b21c0`.

## Ecological contrast already established in original paper (NOT new IWE empirical result)

In southern Chile, native bumblebee *Bombus dahlbomii* and invasive *B. terrestris* remove nectar from the hummingbird-pollinated shrub *Desfontainia fulgens*. Destructive primary nectar robbery strongly lowers floral nectar reward (source reports ~9.25-fold less nectar in pierced flowers), and monthly flowering/robbery frequencies co-occur. Yet the authors found *no detected reduction* in mature seed production when flowers remained accessible to legitimate pollinators.

The source experimental design is **one selected flower in each of three treatments per shrub (40 shrubs)**: visitor/pollinator exclusion without robbing (−Pol −Rob), pollinator access with robber deterrent (+Pol −Rob), and pollinator access with robbing permitted (+Pol +Rob). Original reported occurrence of any mature seeds was **2/40**, **32/40**, and **28/40** respectively. The two pollinator-accessible treatments did not have a detected significant seed-output difference, but this is **NOT equivalence evidence** (especially with 40 paired shrubs), and source analysis also uses seed counts conditional on formation.

**This is a source-described independent ecological boundary for IWE:** a sizeable reduction in nectar availability need not propagate to reduced seed production when other pollinator channels remain accessible. It is not support for the claim that nectar theft provides a benefit. It distinguishes proximal resource loss, legitimate visitor service, and final female reproductive output.

## Identification hierarchy for new IWE original-data work

The local source gate retrieves exact original authors' public XLSX, R script and README (no author contacts or speculative data downloads), verifies all published MD5s, and inspects source workbook sheet column structure without changing the workbook or publishing its individual source records. It must **identify the exact shrub ID and three flower treatment rows** before any new effect calculation.

If original sheet rows verify 40 distinct shrubs × three unambiguous treatments (and actual original mature seed counts, true missingness, no merged or re-used flower IDs), a **paired-shrub** analysis can estimate the 40 within-shrub contrasts between (i) pollination access vs exclusion and (ii) robber presence vs deterrence under pollinator access. Any uncertainty interval must treat shrub as the independent biological unit; no naive n=120 independent-plant inference.

Even if source 120 flower fates are recovered, natural monthly robbery frequency and natural pollinator visitation were **not measured as the activity of the same tagged experimental flower across dates**. Do not manufacture individual seasonal phase lag or a within-lineage seed-predator effect. The design has different robber and pollinator guilds, not a moth that pollinates as adult and eats seeds as larva.

Original published no-significance p values are not automatically source-confirmed effect-size confidence intervals. A source-verifiable paired contrast may be negative, positive or uncertain and will be reported with sign and uncertainty, without false equivalence claims.

## Source status and next action

At initial draft, no original workbook sheet rows/identified individual three-treatment comparisons have been admitted. Reproduce:
`python -m scripts.probe_desfontainia2026_zenodo_source --outdir /tmp/iwe-desfontainia2026-source`.
Original publicly hosted bytes stay on Zenodo; workflow saves only source schema/key and code-provenance receipt.

The strict IWE H1 main meta-analysis remains 2 mutualist, 0 antagonist and 0 mixed dependence clusters. Independent nectar robbery source is context/role-buffering evidence, not a synchrony→fitness contrast.
