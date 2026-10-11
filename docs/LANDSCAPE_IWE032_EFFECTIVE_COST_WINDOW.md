# IWE032 — host filtering shifts the effective antagonist window

Date: 2026-10-02  
Study: Davies & Saccheri 2024, *Cardamine pratensis × Anthocharis cardamines*  
DOI: `10.1002/ece3.11330`  
Status: quantitative mechanism evidence; the strict independent-female-flight extraction remains blocked.

## Distinction from the strict Cardamine route

The strict IWE032 preflight still requires source-backed numeric 2012–2014 female capture/recapture timing. Figure 4 demonstrates that the female flight season lies between flowering modes, but its numeric event distribution has not been recovered.

The landscape pivot can nevertheless use a different source-reported object without pretending it is adult availability: the paper separately models **all eggs laid** and **active eggs** capable of producing damaging late-instar larvae.

## Host-stage filter

Eggs laid within 7 days of first flowering are classified as active. Eggs laid later than 8 days fail to produce fifth-instar larvae in the reported survival comparison.

Thus realized oviposition is not equivalent to effective reproductive cost: the plant's timing relative to egg laying determines whether an exposure remains biologically active.

## Source-reported Gaussian windows

For standardized flowering date `z`, Figure 6 reports:

- total egg load: `2.14 * exp[-0.5 * ((z + 1.10) / 0.92)^2]`, R2 = 0.46;
- active egg load: `1.49 * exp[-0.5 * ((z + 0.61) / 0.66)^2]`, R2 = 0.33;
- active load, high-fecundity ramets: center = -0.53, sigma = 0.63;
- active load, medium-fecundity ramets: center = -0.76, sigma = 0.78.

The first two curves allow a direct source-parameter comparison:

| Quantity | Total egg exposure | Effective active exposure |
|---|---:|---:|
| Peak flowering z | -1.10 | -0.61 |
| Gaussian sigma | 0.92 | 0.66 |
| Amplitude | 2.14 | 1.49 |

Derived from those published parameters:

- the effective peak moves **+0.49 SD later** along the standardized flowering axis;
- the effective window width falls to **0.717** of the total-egg width, a **28.3% narrowing**;
- active-load amplitude is **0.696** of total egg-load amplitude.

## Fitness consequence

The same paper reports that larvae strongly reduce intact reproductive units and uses the active-load curves to calculate flowering-date fitness. High-fecundity ramets benefit from both early and late flowering, while medium-fecundity ramets benefit primarily from late flowering; when fecundity classes are aggregated, a bimodal flowering curve is favored.

This is therefore not just a timing proxy. It provides a mechanistic link from oviposition timing, through stage-dependent survival of the antagonist, to the shape of the plant fitness landscape.

## Ecological consequence for IWE

IWE032 supplies direct evidence for the revised decomposition:

`effective cost window != raw partner exposure window`.

Host timing filters antagonist exposure before it reaches final fitness. In this case the filter both **translates** and **narrows** the temporal cost window.

That result explains why an adult-activity peak alone cannot generally define the fitness-relevant interaction window. The biologically relevant target is the exposure curve after host-stage filtering.

## Reproducibility

Source curve parameters are stored in `data/source_reconstructions/iwe032_cost_window_parameters.csv`.

`scripts/build_iwe032_effective_cost_window.py` rebuilds the derived shift and narrowing metrics in `data/derived/iwe032_effective_cost_window.csv`.

No digitization and no raw-data variance reconstruction are used.
