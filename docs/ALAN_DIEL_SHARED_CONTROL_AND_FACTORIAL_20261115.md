# ALAN × IWE: Night-access vulnerability and shared-dark-control audit

**Status: source-aware methodological/experimental evidence gate, not a new ecological meta-effect.** Sources inspected through 2026-11-15. The central research question is whether the *marginal value of nocturnal access* predicts **realized light-induced final reproduction changes**. Do not equate the nighttime access meta-analysis with a lighting experiment.

## 1. A naive negative beta can be caused entirely by denominator reuse

Let `D` = reproduction in dark/day-only access, `O` = dark/open (day+night) access, and `L` = lit/open access. Then the proposed moderator and response are

`V = 1 - D/O` and `y = log(L/O)`.

If treatment-arm sample means are independent apart from sharing the exact observed `O`, the first-order covariance of their sampling error is

`Cov(V,y) = -D Var(O)/O^3`.

Thus **Cov(V,y) < 0 with D>0 even when light has NO true effect**. This can produce an apparently favorable negative β_V from source error alone. It is not guaranteed to have a particular size or sign in a real study with clustered, correlated sampling; the general covariance must use the full original arm-means covariance matrix.

A fixed-seed simulation with eight *synthetic* taxa, 20,000 datasets and true `lit/open = dark/open = 0.60` everywhere gives:

| Plants sampled per arm | Shared-dark-O mean naive beta | Fraction negative | Independent-dark-O mean beta | Fraction negative |
|---|---:|---:|---:|---:|
| 20 | −0.1996 | 73.06% | −0.0035 | 50.63% |
| 40 | −0.1228 | 68.71% | −0.0027 | 50.58% |
| 60 | −0.0880 | 66.39% | −0.0021 | 50.47% |
| 200 | −0.0284 | 59.15% | −0.0002 | 50.23% |

This reproduces the **problem**, not an ecological effect, and cross-checks the previous ALAN draft PR #78 synthetic control demonstration. The independent-O comparator splits an *ideal hypothetical* original unit; arbitrarily splitting flowers in the same light-assignment site does not guarantee independent controls.

## 2. Proper factorial target and uncertainty

When **the same experimental study** has dark/day `D0`, dark/open `O0`, lit/day `D1`, and lit/open `O1`, use

`Δ = log(O1/O0) − log(D1/D0)`.

Negative Δ would indicate a more negative light response with night access available than with only daytime access, **not** necessarily moth-caused damage. Lighting could alter daytime pollinators, floral physiology, seed herbivory, or the timing and quantity of floral resources. Δ needs four genuinely distinct original arm mean outcomes, original randomization/cluster data, and their sampling covariance. A significant treatment main effect or a significant day/night main effect does **not** substitute for Δ. Shared dark controls among contrasts must enter their variance covariance.

For a general four-arm covariance matrix `Σ`, the code calculates gradients of V, y, and Δ and propagates `JΣJᵀ`; it refuses a missing/indefinite covariance matrix. The source check keeps exact `P1` dark-only nighttime access dependence separate from `P3` experimentally lit open reproduction. Species-only or country-separated night dependence is an exploratory **external transport** covariate and not a same-site measurement.

## 3. What the original experiments actually permit

### Macgregor et al. (2019), *Ecosphere* DOI 10.1002/ecs2.2550

Direct factorial experiment in *Silene latifolia*, five field lighting locations, four temporal rotations, five light treatments (unlit, HPS/LED × full/part-night) and four pollinator-access treatments. Published rates **pooled across light treatments**: open = 72.0%, day-only = 37.6%, night-only = 52.8%. The original authors' independent-guild union calculation is 70.5472%; the published open rate is 1.4528 percentage points higher. This restates original source arithmetic without an independent uncertainty estimate or behavioral compensation proof.

**These pooled percentages are NOT the dark-only D0 and O0**. Feeding them into a light-effect regression to calculate V_dark would contaminate the moderator with illuminated observations. The source paper DID test of light×caging was **not significant**; the actual interaction coefficient, SE and full lighting×access arm counts were not obtained. Nonsignificant is not evidence of equality or equivalence (the authors explicitly report limited interaction power).

Original 417 flowers on 169 female plants: 194 successfully seeded; 46 were classified as parasitized and the paper analyzed seed count/mass for 148 nonparasitized successful flowers. This is **post-pollination selection**, not a common final viable-seeds-per-original-flower outcome. One moth raised from a damaged seed capsule was identified as *Lacanobia oleracea*, so the recorded damage cannot simply be attributed to *Hadena bicruris* nursery pollination. Other individuals' identities remain unresolved; one reared moth does not demonstrate no *Hadena* present. **Neither the true species-specific nursery cost nor lighting×caging effect size is re-estimable from this published aggregate**.

Paper and supporting info: https://doi.org/10.1002/ecs2.2550. Original full PDF source: https://eprints.whiterose.ac.uk/id/eprint/149121/1/Macgregor_et_al_2019_Ecosphere.pdf. ALAN source audit pins PDF SHA256 `e0f83cc2086f2f494f175b0d1eee8495cf9153dd62f9ca7f35338ff9e5f1ad1c` and records missing source seed CSVs; GitHub Actions will independently check its text and digest. The original supplementary Appendix S1 and raw source assignment rows remain absent.

### Lu et al. (2026), *Journal of Plant Ecology* DOI 10.1093/jpe/rtag160

Five paired lit/dark plots, two species and four access treatments (exclusion, day-only, night-only, open). The accepted manuscript reports the *Pedicularis kansuensis* −56% seed-set change in the **night-only access treatment**, not a −56% whole-plant open-access outcome. The seed-set metric is developed seeds per ovule among formed fruits. Open-access seed change is described as not statistically significant but its estimate and shared covariance are not recovered. *Euphrasia regelii* is a different species and mating-system state; its nonsignificant response is not an exact zero.

Macgregor and Lu contain a factorial **experimental design**; neither yields independently re-estimable Δ with its original published four-arm light×access covariance from the currently accessible files. Macgregor's article does report one nonsignificant factorial interaction test; that is not an independently recomputed numerical null. The existing Lu network paper may share experimental infrastructure with the reproductive paper; this is not resolved and cannot supply a new independent reproductive unit.

## 4. Source and publication gates

`data/registry/alan_iwe_light_access_source_v01.csv` pins the only two original light×access factorial papers in this currently reviewed source set, not an exhaustive systematic global review. A genuine future dataset will require a new versioned evidence ledger with validated four cells, actual source means and same-unit covariance. The current gate is **2 factorial-design papers / 1 reported nonsignificant interaction test / 0 re-estimable numerical Δ / 0 legitimate cross-study beta_V**.

The executable negative control rejects nonfinite or zero denominators, covariance asymmetry, covariance non-PSD, missing original arms, and accidental promotion of a paper-level design statement to observed causal coefficients. No new strict IWE H1 effects, no chocho habitat effect and no ALAN paper inference is declared.

## 5. Reproduction

From repository root:

```bash
python -m pytest -q tests/test_alan_joint_factorial.py tests/test_alan_joint_factorial_cli.py
python scripts/audit_alan_joint_factorial.py --output-dir results/alan_joint_factorial
```

GitHub workflow checks the source reference and source DOI, repeats the null with a fixed seed, and publishes only aggregate synthetic diagnostics/source metadata. The code can compute real four-cell interaction after original arm means and covariance are recovered, but **no such empirical result is claimed**.
