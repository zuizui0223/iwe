# Lu 2026: open-versus-night-only modification of the light response

## Result and scope

The primary source is Lu et al. (2026), JPE DOI [10.1093/jpe/rtag160](https://doi.org/10.1093/jpe/rtag160), accepted manuscript Results page 14. This extends IWE PR #120's correction: the source −56% seed-set figure is a night-only-access response, not an unrestricted/open seed penalty.

For **Pedicularis kansuensis conspecific pollen grains per stigma**, the original source reports light-associated declines of 23.09% under open access and 53.80% under night-only access. Each treatment uses its own unlit comparator. The implied reported-scale ratios are:

- RR_open = Y_lit,open / Y_unlit,open = 0.7691;
- RR_night = Y_lit,night / Y_unlit,night = 0.4620;
- RR_open / RR_night = **1.6647186**;
- B = log(RR_open / RR_night) = **0.5096561**;
- difference between the reported relative declines = **30.71 percentage points**.

These are arithmetic transforms of **rounded published percentages**, not a reanalysis of original observations, a fitted interaction coefficient, a new biological experiment, or a meta-analytic estimate. Display approximately **1.665** or **0.510** rather than suggesting additional measurement precision.

The ratio is NOT Y_open/Y_night. It does not mean that absolute open-access pollen receipt is 66.5% greater, that daytime visitors restored 66.5% of pollen, or that viable seed output improved by that amount. It says only that the *relative response to lighting* is less negative in the reported open-arm pollen comparison than in the night-only pollen comparison.

## All eligible same-study species/endpoint pairs, without selected null imputation

The unchanged PR #120 source transcription has 2 species × 2 endpoints × 3 access arms (12 rows). Open versus night-only matching yields four paired candidates:

| Species and endpoint | Open light/unlit | Night-only light/unlit | Ratio of response ratios |
|---|---:|---:|---:|
| P. kansuensis, pollen grains/stigma | 0.7691 | 0.4620 | 1.6647 |
| P. kansuensis, developed seeds/ovules per fruit | Not recovered | 0.4400 | Not estimable |
| Euphrasia regelii, pollen grains/stigma | Not recovered | Not recovered | Not estimable |
| E. regelii, developed seeds/ovules per fruit | Not recovered | Not recovered | Not estimable |

The source reports nonsignificant effects for the unquantified entries. A nonsignificant effect is not a zero change, hence its light/unlit ratio is NOT set to 1. There is only **one original study**, not four independent experiments or twelve replicates.

## Biological interpretation

The paired pollen result is compatible with buffering when daytime access remains available. It does not by itself distinguish daytime service, nonlinear pollen response, bagging/handling differences, or source sampling error. The source also reports no significant open-arm seed-set decline, but absence of a detected decline is not equivalence or verified complete reproductive compensation.

This sharpens the cross-repository question:

**Does a disturbance's effect on a particular temporal interaction channel persist into unrestricted plant reproduction, or is it moderated by alternative channels?**

IWE supplies the interaction-consequence framing, ALAN supplies the manipulated disturbance, and chocho supplies a separate potential geographic-resource layer. Global host presence cannot supply a missing open-arm seed estimate, local visitor effectiveness, or seasonally independent partner window. Neither this one pollen contrast nor the original daytime/nighttime exclusion meta-analysis estimates a global ALAN × syndrome × island effect.

## What a comparative synthesis would require

A suitable within-study response-specific effect-modification contrast is

`B = log(RR_open) - log(RR_night)`.

For each independent study/population/time/light contrast, both ratios must use the same biological endpoint and corresponding control. Keep pollen, fruit set, seed/ovule fractions and seed counts distinct. Its sampling variance is

`Var(B) = Var(logRR_open) + Var(logRR_night) - 2 Cov(logRR_open, logRR_night)`.

The original five paired light plots can induce dependence; missing covariance is not automatically zero. We have no recovered arm variances or the required covariance here. Therefore there is **no new CI, p-value, significant interaction test or inverse-variance weight**. The publication describes interaction modelling, but its underlying Supplementary Table S4b and original observations were not retrieved. This calculation does not replace the authors' model.

Zero response ratios are not repaired with a post-hoc pseudocount. A zero leaves the corresponding log contrast undefined until an appropriate model is specified. The source adapter rejects altered endpoint definitions, duplicated access arms, unreported precision and null-to-zero imputation.

## Verification and reproducibility

Input: `data/registry/lu2026_access_scoped_contrasts_v01.csv` from merged PR #120.
Exact Git blob: `73a04ebd962a3113ebfae410c1720468094ab60a`.
Input SHA256: `b8f18e68f3efcbdc108b59fcd79df9551fd6651cea6a34a0f6ae9fdf5d7b6b43`.

Primary manuscript: https://academic.oup.com/jpe/advance-article-pdf/doi/10.1093/jpe/rtag160/68754751/rtag160.pdf

The original prose was checked again via parsed text. PDF screenshot retrieval failed; no figure points or error bars were digitized, and no PDF-content hash is asserted. Source CSV hashing verifies this transcription, not the publisher's binary PDF.

Run:

```bash
python -m pytest -q tests/test_alan_access_response_ratio.py
python scripts/audit_lu2026_response_ratios.py --output-dir results/lu2026-response-ratios
```

Outputs are `access_matched_light_response_ratios.csv` (all four candidates) and `access_response_ratio_receipt.json` (source hashes, point calculations and missingness). Local test-first verification observed the expected failure before the module existed, then all ten tests passed. The full repository CI remains a separate verification step. No existing IWE strict-H1 extraction, chocho source result, or ALAN manuscript is altered.
