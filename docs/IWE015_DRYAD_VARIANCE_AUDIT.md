# IWE015 Dryad variance audit

Date: 2026-09-27  
Study: Zhou et al. (2020), *Silene stellata × Hadena ectypa*  
Article DOI: `10.1111/evo.13965`  
Dryad DOI: `10.5061/dryad.6q573n5w1`  
Decision: **quantitative hold pending raw-data recomputation**

## Public archive verification

The Dryad landing page is public and identifies a single version published 2020-03-31. It exposes the female experiment files required for a direct check of Table 1:

- `2012_early_female.csv`
- `2012_late_female.csv`
- `2013_early_female.csv`
- `2013_late_female.csv`
- `data_analysis.R`
- `README.txt`

The archive also contains the corresponding male/genotype files and `eggdat.csv`.

## Why the published dispersion cannot be used literally

Table 1 explicitly states `SE=standard error` and labels all entries as mean ± SE.

However, the same table reports bounded outcomes that make the label internally impossible. For example:

- 2012 early fruit-initiation proportion: mean 0.91, printed dispersion 0.19, n=59;
- if 0.19 were an SE, the implied SD would be `0.19 * sqrt(59) ≈ 1.46`;
- a [0,1]-bounded proportion cannot have SD > 1.

The predation-rate entries create the same contradiction. Therefore the current literal-SE reconstruction is invalid.

## Why IWE does not simply relabel the values SD

The contradiction strongly suggests a source-label/table-assembly error, and the successful-fruit dispersions look numerically plausible as SDs. But that remains an inference until the archived female rows are recalculated.

Two diagnostic reconstructions are therefore kept conceptually separate:

1. literal `SE * sqrt(n)` reconstruction — rejected by the bounded-outcome consistency check;
2. direct use of the printed dispersions as SD-like values — plausible, but not promoted without raw confirmation.

No IWE015 row is currently admitted to `data/extraction/direct_effects.csv`.

## Year-specific mean-only biological signal (source Table 1; 2026-10-08)

The source table was transcribed into `data/source_reconstructions/iwe015_published_table1.csv` exactly as printed, including the disputed `SE` label. These are **group means only**, not admitted effect sizes. Define the contrast consistently as **early Hadena-dominant − late co-pollinator-dominant**, within year:

| Year | Successful fruits: early / late | Early − late fruits per plant | Fruit predation: early / late | Early − late predation |
|---|---|---:|---|---:|
| 2012 | 2.66 / 3.91 | **−1.25** | 0.59 / 0.41 | **+18 percentage points** |
| 2013 | 9.77 / 8.60 | **+1.17** | 0.20 / 0.19 | **+1 percentage point** |

The mean successful-fruit contrast **changes sign**: the high-Hadena early period has fewer successful fruits in 2012 but more in 2013. The early–late predation contrast is much larger in 2012. This jointly motivates a test of whether the timing-to-fitness direction depends on the strength of the delayed seed-predation cost, rather than on nominal early/late or pollinator identity alone.

The pattern **does not establish** a statistically significant year-by-season interaction, an effect of moth timing itself, or an adult-service-versus-larval-cost causal decomposition. Different plants occupied the two calendar windows, environmental conditions and flower supply can differ, and the study's reported negligible *year variation in floral-trait selection gradients* is not a test of these final-fruit means. The two years share `DEP_SILENE_STELLATA_HADENA_MLBS` and cannot be counted as independent mixed programmes.

The printed uncertainty problem is independently checkable without raw files. For `n` plant-level observations bounded between 0 and 1, with sample mean `p`, the **largest possible sample SE** is `sqrt(p*(1-p)/(n-1))`. For the 2012 early fruit-initiation proportion (`p=0.91`, `n=59`) this bound is approximately **0.0376**, whereas Table 1 prints **0.19** and labels it SE. The same incompatibility occurs for all four initiation and four predation entries if their sample sizes equal the listed adult-plant counts. The test `tests/test_iwe015_published_table1.py` makes this constraint executable.

**Decision: descriptive contrast identified, strict-H1 quantitative hold unchanged.** Neither the bounded-outcome contradiction nor the direction reversal licenses relabelling any printed dispersion as SD. Require the Dryad female CSVs and `data_analysis.R` before constructing Hedges g or uncertainty; do not add an SMD based on this mean-only transcription.

Primary source: Zhou et al. (2020), *Evolution* 74:1321–1334, DOI https://doi.org/10.1111/evo.13965, Table 1 and Methods/Results.

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
