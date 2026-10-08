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

## Cross-scale ecological contrast: egg burden remains negatively associated with female fitness

The original paper additionally reports directly quantified oviposition **only in the early season**. The mean eggs per flower decreased between years, from **1.04 (2012)** to **0.55 (2013)** (Welch t=4.27, P<0.001, source-reported). Within these early-season samples, the association between a plant's average egg receipt and its female reproductive success is **negative in both years**:

| Year | Mean eggs per early flower | Egg burden versus female fitness, Spearman r | Source P | Early − late successful fruits per plant |
|---|---:|---:|---:|---:|
| 2012 | 1.04 | −0.26 | 0.049 | −1.25 |
| 2013 | 0.55 | −0.40 | 0.003 | +1.17 |

The authors report no significant association between egg receipt and **male** fitness in either year. In other words, the early group has higher mean intact-fruit production in 2013 **while a plant-level increase in oviposition is still associated with lower female fitness within that season**. This is an empirically observed *cross-scale sign difference* between a between-group fruit-count contrast and a within-group oviposition association—not a statistically demonstrated Simpson's paradox, and not evidence that a moth egg directly caused the negative within-group association. Egg receipt is jointly related to moth choice, floral display and subsequent herbivory.

Source data are transcribed separately into `data/source_reconstructions/iwe015_source_egg_fitness_correlations.csv`; source publication section: "Oviposition preference of *Hadena ectypa*". Crucially, **there are no late-season egg observations on the same design**. A year-level egg-load difference cannot substitute for an early-versus-late independent adult-activity contrast.

The paper's source-level fruit-initiation comparison reports **F(3,224)=0.47, P>0.10**, while fruit predation differs among experiments (**F(3,224)=48.1, P<0.001**) and between years (**F(1,226)=45.35, P<0.001**). These do not independently test the specific year × flowering-period interaction in final fruit counts. Lack of a fruit-initiation difference is not equivalence of pollination or effective service.

**Unresolved biological-unit/denominator discrepancy (hard hold):** The paper's *Oviposition and flower fate* methods say that flowers opening in each 1-week experimental period were tagged and followed, reporting 280/239 such *measured flowers* in 2012 and 294/281 in 2013. Its *Female fitness components* methods then say that all labelled reproductive units were harvested to score initiated, eaten and successful fruits. Nonetheless Table 1 reports **9.77 successful fruits per 2013-early plant** and **8.60 per 2013-late plant**, while the described measured flowers are only **294/55=5.35** and **281/55=5.11 flowers per plant**, respectively. At the cohort-total scale, rounded Table 1 counts would imply roughly **537 and 473** successful fruits—both larger than 294 and 281 observed flowers. This is impossible **if and only if** the flower counts and successful-fruit counts cover the same labelled reproductive units. One cannot resolve it by merely assuming the measured flowers were a separate floral-trait subsample: the methods explicitly associate the reported flower counts with the tagged oviposition/fate survey. It is also not proof of an error in the primary data; different counting periods, flower universes, outcome definitions or reporting conventions may explain it. **The denominator join is unresolved until the female CSVs and R script identify the exact flowering units contributing to each Table 1 outcome.** The machine-readable descriptive inventory is `data/source_reconstructions/iwe015_labelled_flower_denominator_audit.csv` and has no inferred fitness conversion rates.

Finally, Table 1 totals 227 adult plants, but the source's one-way F(3,224) and two-year F(1,226) degrees of freedom would imply N=228 in simple unweighted ANOVA without omitted groups. This one-observation discrepancy is an **audit query, not proof of an error**: the raw source model may use different records or transformations. Reconcile sample membership from `data_analysis.R` before accepting source inferential claims as directly reproduced.

**Candidate biological mechanism to falsify:** a strong local oviposition-associated female cost can persist across years even when the *group-level* early-minus-late fruit ranking changes, because flower supply, partner service, and realized survival through larval feeding vary independently. Any test must keep the female-count, male-paternity and predation channels separate; do not manufacture a signed pooled synchrony effect.

## Frozen biological questions for raw readmission

The two-year crossover creates a falsifiable distinction between an **exposure-to-cost change** and a **flower-supply/fitness-denominator change**. Before inspecting the raw plant-level outcomes, fix the following checks:

1. **Total realized reproduction (primary):** compare intact successful-fruit **counts per plant** between source-defined early and late windows separately for 2012 and 2013; preserve year-specific estimates and one shared programme dependence cluster. Do not call source-labelled dispersions SD.
2. **Flower supply and reproductive conversion (diagnostic):** report total flowers/labelled units, fruit-initiation counts or proportions, attacked versus intact fruit counts and missing/destroyed-unit definitions using the original R code. Ask whether the crossover in per-plant intact fruits persists on a defensible flower-denominator scale. A change in fruit counts alone is not evidence of more successful pollination per flower.
3. **Stage mediation (mechanistic, not automatic causal):** test whether the year-specific change in the early–late predation contrast covaries with the change in final intact fruits. Predation occurs downstream of flowering/partner exposure, so conditioning on it is **not** a confounder-adjusted estimate of the total timing effect. Treat decomposition as descriptive unless exposure and mediator assumptions can be justified.

The source tracks flower number and harvested reproductive units, but some entirely consumed pistils have unknown initiation status and were excluded from the paper's initiation denominator. This missing-outcome mechanism must be preserved rather than coding such units as confirmed initiation failures. Early and late groups are different plants, and there are only two years: no claim of replicated temporal moderation or independently identified pollination-versus-seed-consumption pathways follows from Table 1 alone.

## Raw-data acceptance test

Promotion requires all four female CSVs to reproduce, for each year × season:

1. adult-plant sample size used in Table 1;
2. mean successful-fruit count;
3. sample SD and SE of successful-fruit count;
4. fruit-initiation and predation-rate dispersions sufficiently closely to identify whether the table reports SD, SE, or another summary.

The audit must also inspect `data_analysis.R` to verify the exact construction of successful fruits and any row filtering before summary statistics.

Only after these checks may the 2012 and 2013 Hedges-g rows return to the strict corpus.

## Current consequence

The IWE015 programme contains independently observed contemporaneous adult timing and a reported final post-predation fruit outcome, but **the exact alignment of the published fruit-count universe with the source-defined one-week flowering groups is now provisional** because of the 2013 measured-flower/successful-fruit discrepancy. Consequently, the evidence is withheld on **both** sample-unit/outcome-linkage and raw-variance verification grounds. It contributes **zero quantitative strict-H1 effects and zero mixed SMD dependence clusters**. Recovery of dispersion alone is insufficient: the final RU must also be tied to a source-defined flowering exposure.


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
