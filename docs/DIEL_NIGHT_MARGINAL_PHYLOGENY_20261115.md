# Nighttime marginal reproductive access: original phylogeny and outcome denominators

## Main quantitative finding — source-replay, not artificial-light effect (2026-11-15)

This study extends IWE PRs #122–126 and reanalyses the original
Kendall & Nicholson (2025), Ecology Letters, DOI 10.1111/ele.70036,
public data. No new biological experiment is added.

Different questions must remain separate:

- Nighttime versus daytime **dominance**: E=(N-D)/(N+D), where
  N=night-only and D=day-only pollinator access. IWE PR #126 found
  a positive conditional mean for fruit set but an unresolved seed
  mean after the original plant phylogeny was incorporated.
- Nighttime **marginal reproductive opportunity**:
  M_N=(O-D)/(O+D), where O=unrestricted day+night access. Positive
  means removing the night-access option reduces measured source
  reproduction relative to open access. M_N is a bounded source
  outcome contrast, NOT percent seed loss or a night-light response.
  It does not establish that the lost function was performed by moths.

The original author data (1,652 treatments) contain 344 nighttime
marginal mean comparisons and 246 precision-eligible comparisons
with original SE/SD+n and positive first-order variance. Two of the
246 cells cannot be matched to a tip in the authors' 139-tip tree
and remain in the whole-publication source reference. A complete
source vs author-tree panel comparison is reported below.

| Outcome | Panel / dependence | Source publications | M_N [nominal conditional 95% CI] |
| --- | --- | ---: | ---: |
| Broad source fruit set | Full source, publication only | 62 | +0.28680 [+0.20191,+0.37168] |
| Broad source fruit set | Tree-comparable, publication only | 61 | +0.29418 [+0.20891,+0.37944] |
| Broad source fruit set | Tree-comparable, publication+species+phylogeny | 61 | **+0.28367 [+0.18220,+0.38514]** |
| Broad source seed set | Full source, publication only | 55 | +0.22507 [+0.14206,+0.30808] |
| Broad source seed set | Tree-comparable, publication only | 54 | +0.22654 [+0.14302,+0.31005] |
| Broad source seed set | Tree-comparable, publication+species+phylogeny | 54 | **+0.22173 [+0.13570,+0.30776]** |

Original studies' species membership and original shared-ancestry
tree correlation are used, not a made-up family phylogeny.
Publishing similar-looking A/E/M_N values from the **same underlying
field studies** is not independent replication.

### The reproducible and biologically meaningful denominator limit

The broad source "fruit set" field has many ambiguous units:
92 of 137 precision-eligible fruit cells were literally labelled
"NA", and another 22 were labelled generic "proportion".
Only a handful explicitly report a fruit/flower denominator.
The broad positive fruit result MUST NOT be equated with a
resolved worldwide effect on the proportion of originally
available flowers that mature viable fruits.

For source SEED set, a defensible homogeneous outcome subset
is seeds per fruit/capsule/pod:

| Original outcome | Study IDs | Publication-only M_N | Original-tree M_N |
| --- | ---: | ---: | ---: |
| Seeds per fruit (conditional on a formed fruit) | 32 | +0.17459 [+0.07620,+0.27299] | **+0.17286 [+0.07697,+0.26875]** |

This denominator-specific result means the night-access condition
has a positive average association with seeds per formed fruit
in the source experiments. It does NOT count how many fruits or
mature viable seeds were produced per whole plant. Pollen
deposition, autonomous selfing, flower abundance and final plant
fitness must not be inferred from this conditional endpoint.
A hypothetical strict original-flowers-to-fruits source subgroup
is not claimed to have sufficient precision for a species/phylogeny
meta-analysis.

### What the evidence does and does not establish

The original source study already synthesized the importance of
day and night pollination. This is an exploratory original-tree
and measurement-denominator robustness check for M_N, not a
new experimental finding or a claim that the original authors
had not tested diel pollination.

The comparable ALAN Draft PR #78
(https://github.com/zuizui0223/alan/pull/78) assembled
day/open nighttime-dependence ratios as 1−D/O across many
of the SAME original field studies. That ratio differs
mathematically from M_N and is not a second independent
effect. ALAN PR #78 also showed that the direct observed
nighttime dependence of Silene cannot be assigned to the
same experimental population/light dose from a different
country's lighting study.

Most importantly, none of these 344 comparisons randomly
assigns nightlight to flowers. A physical night-exclusion
contrast cannot be used as a proxy for moth sensitivity to
night lighting. A plant may depend on night access but receive
effective pollen from vertebrates or insects tolerant of local
spectrum/dose; indirect plant responses to lighting can differ.

The full causal test still requires **matched species,
site-year, lighting assignment, day-only/open/possibly
night-only access, same reproductive denominator, and
appropriate shared-control covariance**. Macgregor et al.
2019 (Ecosphere DOI 10.1002/ecs2.2550) reported an ALAN ×
day-night access interaction as NONSIGNIFICANT in its
Silene latifolia field experiment. Lu et al. 2026 (JPE
DOI 10.1093/jpe/rtag160) observed nighttime-only seed
loss in Pedicularis, but complete original treatment-level
means and variance were not recovered. These are two
different experimental programmes; no pooled causal light
interaction coefficient is warranted.

### Inferential quality and original source restrictions

Original source SEM/SD+n can refer to nested flowers, fruits
or plants; those are not verified independent lighting units.
The first-order unknown-covariance upper bounds protect some
source sampling correlation but not all study-design
uncertainty. Publication/source selection and correlated
species remain. Conditional plug-in REML/Hartung-Knapp intervals
do not fully integrate variance-component or phylogenetic
branch uncertainty. Positive average source contrasts need
not appear for all species, habitats or independent studies.
No statistically justified "nighttime pollination always
superior" or "night light always harmful" conclusion is made.

## Reproduction, source pins and original limits

- Original treatment table Git blob:
  39a82d966afcdde670603add1c881ace8791ffe9.
- Original trait table Git blob:
  18381e550a7e405fe4f198909f0bb381bbecf1e0.
- Original phylogeny RData Git blob:
  d823c2adbdd088372168addece4ec34063ad0b8a.
- Original 1,094-row paper analysis RData Git blob:
  82935a0ab6172106e798d3bee88c43359007699a.
- Original-tree JSON SHA256 after source conversion:
  34324b8e97b87abdca53a6d578187d0bc239f2cab58974c48b58933398c84a7f.
- Original study-to-tree CSV SHA256 after conversion:
  3be56ba387a338795037f0fcee3e41ae2d9c5bcf26434f3421565ea10f18b07b.

Commands:

    python scripts/run_diel_night_phylogeny.py --author author.csv \
      --traits traits.csv --tree diel.tree.out.json \
      --original-analysis diel.all.diffs.csv --out results/

    python scripts/verify_diel_night_phylogeny.py --author author.csv \
      --tree diel.tree.out.json --original-analysis diel.all.diffs.csv \
      --models results/night_marginal_phylogeny_models.csv \
      --denominators results/night_marginal_denominator_coverage.csv \
      --out results/independent_eigensolver_verification.json

All upstream author files are fetched anew by GitHub Actions and
must pass exact original Git blob checks. Analytical outputs are
aggregate-only model results, source denominator coverage,
across-paper species dependence and audit receipts; no
original paper site coordinates or literature notes
are redistributed. IWE strict-H1 effects created: zero.
