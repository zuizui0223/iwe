# Slimon & Agrawal 2026: original 2023 flowering window, fruit opportunity and Mompha loss

Source: Kelley F. Slimon & Anurag A. Agrawal (2026),
[Zenodo DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509),
original deposited `Freese Stats.zip` (MD5
`151bbd516fc0032af2a2598cb5529c78`).
Reproducible code: `scripts/analyze_slimon2026_window_edges.py`.
Primary scope: **exploratory original-data, non-promoting**.

## Correct provenance — two experiments, not two flowering years

Original `main_exp1.csv` contains first flowering dates such as
`7/12/23`, while `main_exp2.csv` includes `7/7/23`.
Linked `d_pheno.csv` and `d_pheno_exp2.csv` last-flower
records likewise refer to **2023**. The initial evidence inventory
incorrectly labelled exp1 as a separate **2022 flowering** cohort.
The corrected original data distinguish `experiment` (`exp1` vs
`exp2`) from `flowering_calendar_year` (2023 in BOTH).
The broader source project collected some material in 2022 and 2023,
but these two reproductive tables are **not two independent annual
replications**. Both experiments remain within one published
research programme.

The original plant IDs were linked only **within each experiment**,
never across experimental cohorts. Exact joint original
plant-ID counts from the original host phenology, flowering end,
final fruit, and Mompha component CSVs are:

| Source experiment | Source four-file shared plants | Valid first+last flowering date records |
|---|---:|---:|
| exp1 | 148 | 148 |
| exp2 | 123 | 120 |

Repeated Schinia-stage rows (including 951 records in experiment 2)
are not treated as independent plants. The archive's *Schinia*
adult records are focal-plant observations, not an independently
calibrated whole-season flight curve, while exp2's source
`df2_exp2F.csv` has larval columns only.

## A predeclared two-edge analysis

For each experiment separately, compare each plant's directly
source-recorded **first** and **last** flowering DOY with four raw
component outcomes: the original `schinia` fruit-damage count,
`FINAL_Mompha` galled/reproductive-unit count, `lg frt` count,
and `sm frt` count. These are **not** observed viable seed numbers.

To distinguish exposure opportunity from absolute damage count,
calculate one additional *sensitivity proxy*:

`Mompha_share_proxy = FINAL_Mompha / (lg_frt + sm_frt + FINAL_Mompha)`,

only when all source inputs exist and its denominator is positive.
It is an algebraic fraction of observed source-count components,
NOT a directly measured per-flower oviposition risk, seed survival
probability, or validated count of intact seeds. Relative timing
itself is observational; herbivory treatments did **not**
randomize flowering onset/duration.

The script predeclares all first/last × source count/proxy
correlations; no outcome-dependent selection of significant
contrasts. As a sensitivity check, each first/last relationship
with the **Mompha proxy** is also reported as a partial
rank-correlation after residualizing the *other flowering edge*,
the original experimental treatment, and source genotype fixed
categories. The latter correlations are descriptive and come with
**no calibrated inferential p-values or confidence intervals**.
No cross-experiment meta-analysis, Hedges g, source-native seed
reconstruction, or updated strict-H1 cluster count is performed.

## Actual original-data directional results

These four rows are preserved in
`data/source_reconstructions/slimon2026_two_edge_observed_component_associations.csv`.

| Experiment | Flowering axis | Mompha count ρ | Mompha proxy ρ | Conditional proxy ρ | Large-fruit count ρ |
|---|---|---:|---:|---:|---:|
| exp1 | first flower DOY | +0.084 | **+0.372** | +0.186 | −0.424 |
| exp1 | last flower DOY | +0.135 | −0.068 | +0.137 | +0.248 |
| exp2 | first flower DOY | +0.060 | **+0.285** | +0.234 | −0.419 |
| exp2 | last flower DOY | +0.505 | **+0.412** | +0.356 | +0.253 |

Both experiments show an **earlier first flowering day associated with
more large fruit**, and a **later last flowering day associated with
more large fruit**, consistently with production opportunity.
Mompha **absolute counts** versus first flowering are near zero in
both, whereas opportunity-normalized proxy associations with later
first flowering are positive in both. This is not an experimental
demonstration that Mompha selectively attacks late first flowers;
the ratio is coupled to fruit counts, and time-varying plant size,
flower supply, genotype and source measurement cannot be
causally resolved with this diagnostic.

The last-flowering association differs between experiments:
exp1's raw last-date/proxy rank correlation is weakly negative,
exp2's strongly positive. After conditioning on genotype,
treatment and first flowering, both are positive but have
different magnitude. This points to **context/experimental-design
dependence** instead of a universal late-flowering penalty.
It does not constitute two independently replicated field seasons.

## Hard interpretation gates

- The original source `fitness_frt` is constructed from fruit
  counts minus Schinia losses and weighted Mompha brevivittella
  injury. `fitness_seed` further multiplies by source
  genotype-specific seed factors. These are valuable **native
  reproductive models**, not an individually observed
  post-predation viable-seed series.
- `FINAL_Mompha` and `schinia` refer to **different
  seed-predator taxa**; Schinia adult occurrence cannot stand
  in for a Mompha adult availability window.
- The proxy denominator includes the outcome component. Its
  correlations can reflect compositional constraints and
  reproductive opportunity, not necessarily **true within-flower
  attack hazard**.
- Genotype, treatment and other-edge adjustment only handles
  recorded variables. Stage-dependent missingness, flowering
  amount and experimental context can still confound.
- Original 2023 experimental components belong to **one
  dependence programme**, not 2022 and 2023 annual replication.
- Original results were already public and the source SEM
  hypotheses known. This is **outcome-exposed exploratory
  reanalysis**, not blind confirmatory evidence.

**IWE admission decision:** Strict H1 antagonist clusters added:
**zero**. The new evidence is a **nonpromoting mechanistic
window-edge / opportunity-denominator stress test**,
not a claim of plant fitness rescue or general causal selection.
