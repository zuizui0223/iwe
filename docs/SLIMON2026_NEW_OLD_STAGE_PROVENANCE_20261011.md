# IWE: original new–old Mompha temporal-stage observation link

Date: 2026-10-11. Source: [Slimon & Agrawal (2026),
Zenodo DOI 10.5281/zenodo.19488509](https://doi.org/10.5281/zenodo.19488509).
Exact source archive `Freese Stats.zip`, checksum MD5
`151bbd516fc0032af2a2598cb5529c78`.

Script: `scripts/analyze_slimon2026_new_old_mompha.py`.
Source grain CSV:
`data/source_reconstructions/slimon2026_new_old_mompha_grain.csv`.
Results CSV:
`data/source_reconstructions/slimon2026_new_old_mompha_original_stage.csv`.

**Status:** original source-derived, exploratory, **NOT**
individually tracked insect transformation, actual oviposition
dating, observed plant fitness, or strict-H1 effect admission.

## Source population and the 951-row puzzle

The official original README names `df2_exp1_M.csv` and
`df2_exp2M.csv` as **weekly new Mompha counts**, and
`df2_exp1OM.csv` and `df2_exp2OM.csv` as
**weekly old Mompha counts**.

Do not treat the filename descriptions as independently
verified larval ages, or a new/old observation on successive
visits as a followed individual insect.

Direct inspection of all four original CSVs establishes:

| Original experimental table | Physical rows | Rows with original plant ID | Distinct plants | Rows with no ID and numeric Mompha stage data |
|---|---:|---:|---:|---:|
| exp1 new | 159 | 157 | 157 | 0 |
| exp1 old | 159 | 157 | 157 | 0 |
| exp2 new | 123 | 123 | 123 | 0 |
| exp2 old | **951** | **123** | **123** | **0** |

**Resolution:** the 828 additional rows in the exp2 old
series have **no original plant ID, no numeric old-stage
measurement and no nonempty auxiliary field**. They are
empty/unlinkable export rows, NOT 828 additional experimental
plants, independently replicated surveys, unrecognized
positive larvae, or meaningful repeated plant rows.

There are no duplicated nonempty original plant IDs in
these four stage tables. All results refer to **source
original-ID-keyed complete-case observations only**,
not an estimated population-level attack probability.

Both experiments' source flowering records are dated
**2023**, so they are two experimental components of **one
programme**, not replicated independent flowering years.

## The actual stage relation we could test

On each original plant and *literal exact weekly* survey
date `t`, compare original `new Mompha(t)`, `old
Mompha(t)`, `old Mompha(t+7)`, and `new Mompha(t+7)`.
Do not impute source missing visits, use nearest dates,
convert nonnumeric cells into zeros, aggregate the
physical rows as independent insects, or infer the time
at which an egg was laid.

| Verified source result | exp1 | exp2 |
|---|---:|---:|
| Plants observed at both original stages | 153 | 122 |
| Matched plant × first-week date pairs | 795 | 641 |
| Exact first-week dates | 6 | 6 |
| Pairs with new Mompha present at t | 273 | 165 |
| old Mompha present at t+7 among new-positive pairs | **229/273 (83.9%)** | **131/165 (79.4%)** |
| old Mompha present at t+7 among new-zero pairs | **266/522 (51.0%)** | **101/476 (21.2%)** |

In an **exploratory linear probability model** with original
plant and survey date effects, and additional original
`old(t)` and `new(t+7)` indicators, the joint
`new(t)` coefficients are **+0.225** (exp1) and
**+0.397** (exp2). The `old(t)` coefficients
are +0.265 and +0.177, respectively. Following-week
`new(t+7)` has a negative association (about −0.123
in each experiment), reflecting an additional temporal
relationship, not a causal negative control.

Because this is one observational programme with no
individual identification of the moths, the findings
**cannot** tell whether a specific `new` Mompha became
a specific `old` Mompha seven days later. Continuing
host reproductive activity, correlated gall burden,
observation/detection timing, and adult availability
remain competing explanations. The original source
label *old* does not establish exact biological age.

## Why this adds ecology beyond the previous PR

The prior-week flowering association in PRs #93–94
involved a **proxy for reproductive stage** (open
flowers), whereas this analysis directly relates
**two distinct observed insect-stage labels**. A
positive new(t)–old(t+7) relation is therefore a
more proximal empirical test of **stage progression
and visible insect retention**. It increases confidence
that observed insect-stage time series contain
nontrivial time structure, but does not prove
larval developmental timing or final reproductive
selection.

The original published work involves seed predator
damage and reconstructed seed-fitness variables, but
the publicly audited table does **not** provide
the individually linked, post-larval intact viable-seed
outcome and independent adult moth activity window
required to promote strict IWE antagonist H1.

## Inference limitations and stop rule

- Source plant×date pairs repeatedly measure the
  same individuals. Never use 795 or 641 as counts
  of independent host plants or experimental units.
- In-sample fixed-effect coefficients describe the
  observational records only; they are not causal
  egg-to-larva probabilities or prospective forecasts.
- No egg marks, independently censused *Mompha*
  adults, known bud-at-risk denominators or source
  observed mature intact seeds were recovered.
- Do not pool exp1 and exp2 as independent study
  programmes or add another H1 effect.
- To test the biological transition directly,
  observations must label the same gall or egg/larva
  over time, ideally alongside the plant bud stage
  and viable-seed fate.

**strict-H1 independent clusters unchanged:**
mutualist **2**, antagonist **0**, mixed **0**.
