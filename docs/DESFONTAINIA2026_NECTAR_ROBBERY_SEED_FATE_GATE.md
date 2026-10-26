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

**Source recovery and matched-shrub experiment now completed.** The original workbook, author R script and README passed immutable source MD5 checks in [GitHub Actions 40282024289](https://github.com/zuizui0223/iwe/actions/runs/40282024289); **10 software tests passed** and 40 original nonduplicated shrub IDs linked exactly to three seed outcomes. The separate nectar sheet has 400 flower observations on 40 numbered shrubs. The same shrub ID does **not** prove it was the same flower used for final seed production.

### Direct mature seed output on 40 paired shrubs

| Original treatment | Flowers with any mature seeds | Mean mature seeds/flower | Median |
|---|---:|---:|---:|
| Bagged, pollinators excluded (−P−R) | **2/40 (5%)** | **5.175** | 0 |
| Pollinators present, robber deterrent (+P−R) | **32/40 (80%)** | **26.125** | 10 |
| Pollinators present, robbery permitted (+P+R) | **28/40 (70%)** | **31.350** | 17.5 |

- **Pollinators present vs bagged** (+P−R minus −P−R): mean **+20.950 mature seeds per shrub-selected flower**, paired n=40 bootstrap 95% interval **+9.575 to +32.575**. Seed presence difference **+75 percentage points** [**+60 to +87.5**]. Exact paired binary discordance p≈**1.86×10⁻⁹**, exploratory.
- **Robber allowed vs deterred with pollinators present** (+P+R minus +P−R): mean **+5.225 mature seeds**, paired bootstrap 95% interval **−12.175 to +22.400**. Seed presence changes by **−10 percentage points** [**−30 to +10**]. Exact matched binary discordance p≈**0.4545** (6 shrubs have seeds only in robber-allowed flowers; 10 only in robber-deterred flowers).

These **wide intervals neither show a biologically important reduction nor rule one out**; failure to reject a null is not an equivalence demonstration. The original shrub-paired counts include many zeros/skewed seeds. Notably the naturally robbed, already-open flower (+P+R) was *selected because it was already perforated*, whereas deterrent tape was applied to a separate bud *before opening*. Different flower-selection and anthesis histories prevent causal identification of the effect of robbery from this comparison.

### Same-shrub nectar reward difference is also now source-verified

[Original source execution 40282515054](https://github.com/zuizui0223/iwe/actions/runs/40282515054) verified the literal nectar status levels `Robada` (200 flowers) and `No dañada` (200 flowers), matching **40 original shrub IDs** also present in the seed experiment.

Only **186 robbed and 180 undamaged flowers** have recorded numeric nectar volumes (14 and 20 source missing volumes respectively). Missing floral reward observations were **not imputed to zero**. On the 40 original shrubs, using each shrub's mean observed volume per status:

- Mean pierced-flower nectar **0.481025 µL**; mean intact-flower nectar **4.448854 µL** — **9.249× more standing nectar** in intact flowers.
- Paired shrub-mean difference **pierced − intact = −3.967829 µL**, shrub-resampled 95% nonparametric bootstrap interval **−5.379825 to −2.553392 µL**.
- An exploratory *between-shrub* rank correlation of recorded nectar depletion with the completely different experimental flowers' seed-count contrast (robber permitted − robber deterred) was **Spearman ρ=+0.1381**. It is a selected, descriptive association, **not** a measured same-flower nectar→seed mediation pathway, an equivalence result, or evidence that losses in one flower cause higher/lower seeds in another.

**What this establishes:** an individually sourced, **large proximal nectar reward loss** exists in the same focal shrub population for which a mature seed-count contrast is much more uncertain. Legitimate pollinator access strongly contributes to seed formation. **It does not establish that robbery has literally zero reproductive cost or that a plant compensates by a measured developmental mechanism.** Additional independently paired or experimentally randomized flower reward restoration and time-specific pollinator access would be needed to identify the conversion/buffering process.

Source outcomes are 40 *paired shrubs*, NOT 400 experimentally replicated seed fates or 120 independent plant treatments.

### Reproduction

`python -m scripts.probe_desfontainia2026_zenodo_source --outdir /tmp/iwe-desfontainia2026-source`

`python -m scripts.analyze_desfontainia2026_paired_seed_fate --outdir /tmp/iwe-desfontainia2026-source`

The original 2026 published Excel and author R code remain on Zenodo. The workflow exports only aggregate paired contrasts, original source hashes, paired bootstrap and source unit/missingness receipts; no individual original plants or workbook is redistributed.

The strict IWE H1 main meta-analysis remains 2 mutualist, 0 antagonist and 0 mixed dependence clusters. Independent nectar robbery source is context/role-buffering evidence, not a synchrony→fitness contrast.
