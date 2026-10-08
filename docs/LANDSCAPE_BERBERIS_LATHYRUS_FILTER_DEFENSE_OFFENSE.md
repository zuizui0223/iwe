# Same plant reproductive filter, opposite ecological outcomes?

**Date:** 2026-10-08  
**Scope:** independently sourced ecological comparison, **not a new strict-H1 effect**, and not a causal cross-species meta-estimate.

**Crucial difference in biological units:** *Lathyrus* involves abortion
of **entire immature fruits**, so oviposited eggs in those fruits are
lost along with all potential seeds. *Berberis* involves **individual
seed abortion inside fruits that were retained to sampling**, and
a second, potentially valuable sibling seed may remain. They are
related but **not the same physical host filter**. The observed
contrast cannot identify the effect of information predictability
without controlling reproductive-unit scale, sibling value and
plant resource status.

### 1. Plant strategy can depend on the value of a surviving sibling seed

Meyer et al. (2014), *The American Naturalist*, DOI
[10.1086/675063](https://doi.org/10.1086/675063), examined
*Berberis vulgaris × Rhagoletis meigenii*. Fruits were collected from
two habitats, with and without oviposition punctures.
The authors explicitly separate *one-seeded* and *two-seeded*
fruits and used likelihood/Monte Carlo models to test whether the
abortion of individual seeds was consistent with random mortality.

A source-exact reconstruction of **Table 1** shows:

| Pine-habitat source fruit state | Without oviposition puncture | With puncture |
|---|---:|---:|
| **Two-seeded fruits:** exactly one seed aborted | **131/463 (28.3%)** | **61/80 (76.3%)** |
| **One-seeded fruits:** the sole seed aborted | **16/418 (3.8%)** | **1/38 (2.6%)** |

The same source Table 1 documents scrub-habitat categories;
all 8 source combinations are frozen in
`data/source_reconstructions/meyer2014_berberis_published_fruit_states.csv`.

### Resource context changes the meaning of an oviposition cue

The original table also gives a striking **observational, not
causal**, environmental interaction. For two-seeded fruits, exactly
one seed was aborted in:

| Habitat | No egg-laying puncture | Puncture present |
|---|---:|---:|
| Moist pine forest | **28.3%** (131/463) | **76.3%** (61/80) |
| Dry scrub | **68.8%** (64/93) | **71.8%** (356/496) |

Thus a large *puncture-associated* difference occurs in the
moister forest, whereas the drier habitat already has many partially
aborted fruits without punctures. This is consistent with resource
stress acting through the same fruit-decision surface, **not** proof
that drought eliminates parasite defense. The original article also
found no significant difference between pine-punctured and
scrub-unpunctured **distributions of fruit states** (source
χ²=1.6, P>0.45). These are distinct samples, with habitat and
population identity confounded; no within-plant response to an
experimentally randomized puncture or watering treatment is
identified here.

**Important outcome caveat:** the paper's *state definition* deliberately
groups larva-eaten seeds with living seeds in its **nonaborted**
category. These are counts of *abortion patterns* among sampled mature
fruits, **not numbers of intact viable seeds or proof of absolute
fitness gain**. Moreover, thousands of fruit observations are
clustered in plants/populations, and puncture status was not
randomly assigned. The small 38-fruit one-seeded punctured group has
limited precision. We do not compute fruit-independent p-values.

The source's fitted selective-mortality model for two-seeded fruits
estimates *first selected seed vs sibling seed* mortality:
- pine without puncture: **22.5% vs 10.6%**;
- pine with puncture: **78.0% vs 3.2%**;
- scrub without puncture: **72.1% vs 7.5%**;
- scrub with puncture: **79.0% vs 12.5%**.

**Do not interpret fitted latent mortality parameters as directly
observed per-seed experimental responses.** The paper reports that
the selective model fits the two-seed state frequencies
perfectly *by construction*; its evidence against the uniform model
comes from the latter failing to explain stressed groups, not
from an independently validated perfect forecast. This matters
for the level of inference IWE can transport.

The authors interpret the low abortion of a valuable final seed
as a conditional defensive allocation strategy. Yet the exact
plant-level net-seed gain is a model interpretation informed by
earlier mechanistic work, not a timing-manipulation effect estimated here.

### 2. An antagonist can exploit predictable fruit retention

Östergård et al. (2007), *Ecology*, DOI
[10.1890/07-0346.1](https://doi.org/10.1890/07-0346.1),
followed *Lathyrus vernus × Bruchus atomarius*.
The beetles preferentially laid eggs in fruits predicted to remain
through development, using position and phenology plus unmeasured cues.
The paper compares *observed* successfully developed beetles
(**2.84 ± 0.14**) with a *simulated random oviposition* expectation
(**2.02 ± 0.11**). Those distributions reflect different
underlying fruit counts (**N=238 observed, N=410 initiated in the
random scenario**, according to the primary text). The **~40.6%**
arithmetic contrast is therefore illustrative, not a controlled
treatment effect or a valid cross-fitness SMD.

This study shows a biological **offensive route**: predictable fruit
retention allows a seed predator to avoid wasting offspring on
fruit that plants will abort. Observational and simulation-based
findings support selective oviposition, not a universal adaptive
response to all host filters.

### 3. A sharper falsifiable hypothesis: two independent axes

The relevant moderator is not the amount of fruit abortion alone.
Two other things must vary *separately*:

1. **Protectable reproductive value:** how much intact offspring
   can be saved by aborting one egg-bearing seed, fruit or ovule,
   especially whether a viable sibling seed remains.
2. **Information available to the consumer:** how accurately a
   seed predator can forecast fruit retention *before* selecting a
   unit, rather than after the host responds to the attack.

A within-system design would randomize viable-sibling availability
and oviposition exposure; independently manipulate the reliability
of pre-oviposition host-retention cues (without changing absolute
fruit resource quantity), then record actual egg placement, host
abortion, surviving larvae and **net intact seeds per initial
flower/ovule**. The genuine prediction is a **crossed interaction**,
not that one axis independently always improves plant fitness.

Competing predictions, not assumed outcomes:

| Consumer can predict future retention | Sibling seed protectable | Mechanism that could dominate |
|---|---|---|
| Low | Yes | Abortion may remove consumers while preserving siblings |
| High | Yes | Consumer targeting may circumvent defense |
| Low | No | Abortive loss can sacrifice the last reproductive unit |
| High | No | Consumer may exploit retention, with little defensible sibling value |

Critically, the matrix is **a proposal for an experiment**;
neither of these published datasets contains the crossed manipulation.
Species, fruit structure and predator are different, and each
experiment also differs in sample grain. No comparative coefficient
is estimated by pooling their tables.

### 4. Exact IWE outcome boundary

- Neither paper has a verified contemporaneous independent
  adult-flight **phenological-overlap contrast linked to final plant
  reproduction with group variance**.
- The 2014 *Berberis* source measures oviposition punctures, not a
  same-season adult activity/flowering synchrony curve.
- The 2007 *Lathyrus* source measures selective egg placement
  and post-abortion reproductive outcomes, not a separate
  adult-focal timing effect matching strict H1.
- The *Berberis* seed state table explicitly combines **eaten**
  with **living** in the nonaborted category.
- Both are ecological *mechanism boundaries* for the post-exposure
  conversion gate, **not new H1 independent antagonist clusters**.

### Original publication data access

The Wiley *Ecology* article explicitly links Figshare collection
`10.6084/m9.figshare.c.3300059` as supporting research data.
Meyer et al. (2014) have original supplementary fruit-state counts in
Dryad `10.5061/dryad.k8m7b` (one published Word file).
A finite, no-auth public-API metadata audit is implemented in
`scripts/probe_ostergard2007_meyer2014_archives.py` and runs with
the source-linked endpoints only. An API listing or publisher page
does **not** establish that row-level or plant-ID raw observations
have been recovered; no formal meta-effect is generated.
