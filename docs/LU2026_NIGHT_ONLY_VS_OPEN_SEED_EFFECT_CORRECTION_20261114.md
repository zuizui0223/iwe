# Lu JPE 2026: the night-only seed penalty is not the open-pollination penalty

> **2026-11-24 cross-repository source-availability correction (later than this historical review).** The below text records the **2026-11-14 acquisition state**. On **2026-11-21**, the separate `zuizui0223/alan` repository recovered the publisher-issued S4b supplementary DOCX (198,613 bytes, original SHA256 `c9cc7ea119c6a99bcfee2b6956c76988c73cf776f20944f5570d00101c3e3abe`) and extracted **all 12 reported S4b light contrasts**. See [ALAN primary-source scope](https://github.com/zuizui0223/alan/blob/main/database/alan_experiments/lu_jpe_sources/README.md), [S4b original reported table](https://github.com/zuizui0223/alan/blob/main/database/alan_experiments/lu_jpe_sources/table_S4b.csv), and [new cross-repo covariance analysis](https://github.com/zuizui0223/alan/blob/analysis/alan-arthropod-search-expansion-20261122/docs/ALAN_LU_JPE_FUNCTIONAL_BUFFERING_COVARIANCE_GATE_20261124_ja.md). The original statement "Table S4b unavailable" is therefore **historical and no longer current**. For *P. kansuensis* seed-set, the primary S4b **Unlit−Lit** coefficients are Open **+0.0445 (SE 0.0319)** and Nocturnal **+0.1332 (SE 0.0429)**. The model-scale contrast `(Lit−Unlit)_Open−(Lit−Unlit)_Night` has point estimate **+0.0887**, but its joint standard error **cannot be identified** without the shared experimental-block covariance (Cauchy–Schwarz range 0.0110–0.0748). The original model scale and independent lighting-unit covariance remain unresolved: this is **not** a percentage-point effect, a valid confidence interval, a demonstrated daytime compensation mechanism, or an additional independent experiment. The full main article Methods and original plant-level allocation are still unavailable here. Preserve all 2026-11-14 historical results below; do not recode missing published values as zero.

## Material correction to the earlier abstract-only audit

DOI: [10.1093/jpe/rtag160](https://doi.org/10.1093/jpe/rtag160).
Primary source: [33-page accepted manuscript](https://academic.oup.com/jpe/advance-article-pdf/doi/10.1093/jpe/rtag160/68754751/rtag160.pdf), Results p14, Methods p11, Discussion p16.

The prior IWE PR #119 claim ledger stored a **−56% seed-set effect without its pollinator-access arm**. The number comes from the original authors, but applying it to unrestricted reproduction loses a consequential experimental condition. The Results restrict the reported seed decline to **nocturnal-only access rather than the other two access treatments**. The Discussion provides −56.0% in the nocturnal-pollination paragraph. We retain that number with this scope and explicitly flag that the underlying Table S4b has not been retrieved.

`seed_set` here means developed seeds / total ovules **per fruit**, not seeds per plant, total reproductive output, viable seed count, or a −56 percentage-point change.

## Source-scoped light versus dark comparisons

| Plant | Access | Stigma conspecific pollen | Seed/ovule fraction |
|---|---|---|---|
| Pedicularis kansuensis | Open (day and night) | −23.09%, source-reported decrease | No significant effect reported; estimate not recovered |
| P. kansuensis | Day only | No significant effect reported; estimate not recovered | No significant effect reported; estimate not recovered |
| P. kansuensis | Night only | −53.80%, source-reported decrease | −56.0% assigned from Results/Discussion scope; Table S4b unavailable |
| Euphrasia regelii | Open | No significant effect reported; estimate not recovered | No significant effect reported; estimate not recovered |
| E. regelii | Day only | No significant effect reported; estimate not recovered | No significant effect reported; estimate not recovered |
| E. regelii | Night only | No significant effect reported; estimate not recovered | No significant effect reported; estimate not recovered |

The full 2-species × 3-access × 2-outcome grid has 12 contrasts. Three numeric percentage changes are retrievable from the prose. Nine nonsignificant contrasts have **unknown point estimates**, not zero. No means, SEM, effect-size variance, or p-value is fabricated from figure captions or the stated plant sample size. The complete-exclusion arm is in the design, but it is not assigned an unreported light-effect contrast in this 12-row table.

## Experimental units recovered from the actual Methods

The field design had five lit/unlit plot pairs, 5 × 5 m plots, and treatment-control separation above 30 m. Mean illumination was 4.52 ± 0.23 **SEM** lux, with a 0.69–8.99 lux range; controls were below 0.1 lux. Nighttime illumination was 19:30–05:30 and field observations were July–August 2024.

The text reports 20 plants per treatment combination and three to five fruits per plant for seed set. It does not clearly locate those 20 plants within the five paired plot replicates. Neither 20 nor 20×5 is treated as the number of independent lighting units. Plant/site allocation and the covariance of access-arm estimates remain missing.

The same paper records 126 nocturnal visits on P. kansuensis. Total nocturnal visits were similar between lighting conditions despite lower Lepidoptera and increased Diptera visitation. Per-visit pollen efficiency was explicitly not measured. These visits are NOT the all-survey 838→357 Lepidoptera events in the other Lu network article. Potential sharing of field infrastructure remains unresolved; publication names, date or location alone cannot prove data independence or identity.

## Ecological interpretation

The observed impairment of nocturnal function does **not** by itself identify a loss of unrestricted seed set. Even this self-incompatible plant has daytime pollen vectors. The result is compatible with daytime buffering, a nonlinear/saturating pollen-to-seed response, and/or imprecise open-arm effects. It does not establish complete compensation, equivalence, or absence of harm.

Likewise, E. regelii differs in both autonomous selfing and its observed absence of nocturnal visitors. Two species cannot separate mating-system causation from differences in visitor dependence, floral biology, or environment. A significant effect in one species and a nonsignificant effect in another is not itself a significant cross-species interaction.

### A common-unit meta-analytic target

For each independently replicated source study, population, year, reproductive endpoint and ALAN contrast, keep:

- `L_N = log(Y_lit,night / Y_dark,night)`;
- `L_O = log(Y_lit,open / Y_dark,open)`;
- the potential buffering contrast `B = L_O − L_N`.

A positive B would describe a less-negative (or more-positive) light response with unrestricted access than with night-only access. It is an effect-modification estimand, NOT automatic proof of daytime behavioral compensation. Shared experimental blocks and related outcomes require the covariance term in Var(B) = Var(L_O) + Var(L_N) − 2 Cov(L_O,L_N). Bagging/handling effects also matter. No continuity correction should be selected after seeing a zero arm; bounded reproductive outcomes may instead require binomial/beta-binomial models with proper clustering.

This paper's open seed point estimate and the contrast covariance are unavailable here. Accordingly **B is not estimated**, and no global coefficient or strict IWE synchrony effect is created. For `chocho`, geographic resource availability remains a separate stage: neither worldwide host presence nor a nocturnal visitor label supplies Y_lit/open or the needed local timing. For `alan`, retain light spectrum, dose and duty cycle separately from pollinator access and reproductive assurance.

## Access and provenance limits

Crossref metadata were downloaded in source-probe run [43593452266](https://github.com/zuizui0223/iwe/actions/runs/43593452266); the runner's official publisher/PDF requests returned 403. The exact PDF URL supplied by Crossref was readable through cached web full-text extraction. The PDF binary was not downloaded and its SHA256 is unknown. The metadata hash is **not** a PDF-content hash.

PDF screenshots failed. No figure points or error bars were digitized or visually verified. The official Supplementary Data listing was located, but the original Table S4b and plant-level observations were not recovered. A completed retrieval-probe workflow is not a successful original-data acquisition.

The page-level source map is `data/registry/lu2026_fulltext_scope_source_v01.json`. The corrected legacy claim table retains all original reported numeric entries and adds pollination access/endpoint definition. The programme ledger now records the five paired source blocks and the full-text evidence status. The previous broad interpretation is superseded, not erased from Git history.

## Reproduction

```bash
python -m pytest -q tests/test_lu2026_pollination_access_scope.py
python scripts/audit_lu2026_access_scope.py --output-dir results/lu2026-access-scope
```

Outputs are a 12-row source-scoped transcription and a machine-readable limitations/correction receipt. They are **not** a raw-data reanalysis, 12 independent experiments, a newly significant study effect, or a new IWE strict-H1 cluster.
