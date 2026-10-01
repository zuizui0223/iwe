# IWE015 Dryad variance audit

Date: 2026-09-27  
Study: Zhou et al. (2020), *Silene stellata × Hadena ectypa*  
Article DOI: `10.1111/evo.13965`  
Dryad DOI: `10.5061/dryad.6q573n5w1`  
Decision: **quantitative hold pending raw-data recomputation**

Timing is **not** the blocker. Zhou et al. Figure 1 reports same-season 2012 and 2013 adult *H. ectypa* and co-pollinating moth density (moths observed per flower ×100) separately from egg density. The adult moth series provides an admissible `direct_adult_census` partner-window basis. Raw variance verification therefore remains the only quantitative gate before a draft strict re-admission can be constructed.

## Public archive verification

The Dryad landing page is public and identifies a single version published 2020-03-31. It exposes the female experiment files required for a direct check of Table 1:

- `2012_early_female.csv`
- `2012_late_female.csv`
- `2013_early_female.csv`
- `2013_late_female.csv`
- `data_analysis.R`
- `README.txt`

The archive also contains the corresponding male/genotype files and `eggdat.csv`.

Stable Dryad download-link file IDs are now pinned so authenticated retrieval does not require another discovery pass:

| source object | Dryad file ID |
|---|---:|
| `2012_early_female.csv` | `278487` |
| `2012_late_female.csv` | `278488` |
| `2013_early_female.csv` | `278490` |
| `2013_late_female.csv` | `278492` |
| `data_analysis.R` | `278500` |
| `README.txt` | `278498` |

The landing page is public, while direct file-stream requests return HTTP 403 in the current runtime. This is an access-layer/authentication blocker, not source-object uncertainty.


## Why the published dispersion cannot be used literally

Table 1 explicitly states `SE=standard error` and labels all entries as mean ± SE.

However, the same table reports bounded outcomes that make the label internally impossible. For example:

- 2012 early fruit-initiation proportion: mean 0.91, printed dispersion 0.19, n=59;
- if 0.19 were an SE, the implied SD would be `0.19 * sqrt(59) ≈ 1.46`;
- a [0,1]-bounded proportion cannot have SD > 1.

The predation-rate entries create the same contradiction. Therefore the current literal-SE reconstruction is invalid.

## Independent diagnostic from the dissertation ANOVA

The 2017 dissertation reports the same Table 1 values and repeats the label `SE=standard error`, so the inconsistency predates the journal typesetting stage.

It also reports a significant year effect on fruit-predation rate when averaging across pollinator types: `F = 45.35`.

As a **diagnostic only**, reconstructing a simple raw-scale 2×2 year × seasonal-period ANOVA from the four published predation-rate cell means and sample sizes gives:

- treating the printed 0.36 / 0.35 / 0.30 / 0.24 dispersions as **SD**: year-effect `F ≈ 52.3`;
- treating them as **SE** and expanding to `SD = SE * sqrt(n)`: year-effect `F ≈ 0.91`.

The SD interpretation is therefore qualitatively compatible with the source's large year effect, whereas the literal-SE interpretation is not. However, the source does not document enough detail here to guarantee that this hand reconstruction matches the exact transformed/model specification used for the reported ANOVA. This check is **supporting evidence only** and does not authorize IWE015 re-admission without the raw Dryad recomputation.

## Why IWE does not simply relabel the values SD

The contradiction strongly suggests a source-label/table-assembly error, and the successful-fruit dispersions look numerically plausible as SDs. But that remains an inference until the archived female rows are recalculated.

Two diagnostic reconstructions are therefore kept conceptually separate:

1. literal `SE * sqrt(n)` reconstruction — rejected by the bounded-outcome consistency check;
2. direct use of the printed dispersions as SD-like values — plausible, but not promoted without raw confirmation.

No IWE015 row is currently admitted to `data/extraction/direct_effects.csv`.

## Raw-data acceptance test

Promotion requires all four female CSVs to reproduce, for each year × season:

1. adult-plant sample size used in Table 1;
2. mean successful-fruit count;
3. sample SD and SE of successful-fruit count;
4. fruit-initiation and predation-rate dispersions sufficiently closely to identify whether the table reports SD, SE, or another summary.

The audit must also inspect `data_analysis.R` to verify the exact construction of successful fruits and any row filtering before summary statistics.

Only after these checks may the 2012 and 2013 Hedges-g rows return to the strict corpus.

## Current consequence

The IWE015 programme still passes the biological timing and final-reproduction gates, but contributes **zero quantitative strict-H1 effects and zero current mixed SMD dependence clusters** until raw variance verification succeeds.


## Executable raw audit

The repository now provides:

`python scripts/audit_iwe015_raw_variance.py <2012_early.csv> <2012_late.csv> <2013_early.csv> <2013_late.csv> <output_dir> --successful-fruits-col <column>`

Optional cross-check columns:

- `--fruit-initiation-col <column>`
- `--predation-rate-col <column>`

The command writes:

- `group_audit.csv` — exact n, raw mean, raw SD, raw SE, and whether the printed dispersion matches raw SD or raw SE;
- `bounded_component_audit.csv` — optional fruit-initiation/predation checks including the distribution-free Bhatia–Davis upper bound;
- `raw_effect_candidates.csv` — raw-data Hedges g for early minus late in 2012 and 2013, calculated directly from the individual successful-fruit values;
- `audit_status.json` — a non-promoting machine-readable status.

The raw-effect calculation never uses the Table 1 dispersion. Table 1 is used only to verify that each CSV reproduces the published experiment sample size and rounded mean before a candidate raw effect is emitted as ready.

The command never edits `data/extraction/direct_effects.csv`. Re-admission remains a separate transactional step after the audit output is inspected.
