# Comerford et al. (2025) *Jadera* — independent mixed partner source gate

Date: 2026-10-19. Primary article: Comerford, Carroll & Egan (2025),
*A New Twist on an Old Story: Pollination and Seed Predation in
Jadera haematoloma*, *The American Naturalist* **206:179–191**,
[DOI 10.1086/736460](https://doi.org/10.1086/736460).
Published original data: [Dryad DOI
10.5061/dryad.2bvq83c2b](https://doi.org/10.5061/dryad.2bvq83c2b).

**New independent mixed biological system:** *Jadera haematoloma*
is a hemipteran whose adults transfer pollen and whose
offspring reduce plant seed viability. The authors' peer-reviewed
field/greenhouse/laboratory results demonstrate separate
**adult service** and **offspring cost** pathways. This is
independent of the prior IWE Yucca/Tegeticula and Silene/Hadena
systems; it is therefore a genuine **candidate programme**,
but **not** an additional admitted timing/fitness SMD.

## Original datasets are different experiments and host plants

The original **published Dryad metadata/abstract** lists five
experiments conducted at Rice University in 2018–2019, including:
- greenhouse pollination on **Cardiospermum halicacabum**;
- field pollination on **Koelreuteria elegans**;
- insect longevity after nectar feeding;
- an offspring seed viability damage experiment;
- separate pollen-capture tests.

An original file called `Greennhouse_time.zip` exists. Its
filename **does not verify** adult phenology time, a natural
independent activity census, or source-consistent within-plant
calendar timing. The seed-cost experiment must not be joined
to the differently hosted service experiments using trial
number or generic plant labels. Separate evidence for adult
pollination and offspring seed predation cannot be subtracted
to manufacture the final intact-seed fitness of the
*same host plant unit*.

## Official source access attempted with no email or author contact

The official [Dryad REST API](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/README.md)
returned publication metadata and the published version-linked
original file list, version ID **367420**, with **nine** listed
source files. The source-only workflow
`scripts/probe_jadera2025_dryad_source.py` retrieved the
original metadata, requested the exact published dataset ZIP,
then requested each of the **source-version-issued individual
file IDs**, also trying its public `stash/downloads/file_stream`
route. In this GitHub runner environment:
- dataset archive ZIP endpoint: **HTTP 401**;
- individual file REST downloads: **HTTP 401**;
- published public file_stream routes: **HTTP 403**;
- publication metadata/file IDs: **retrieved**;
- source raw file bytes: **0 of 9 recovered**.

These are **access-environment failures**, not evidence that the
published data are absent or that their original 2018–2019
phenology/fitness effects are zero. No raw original rows,
specific original plant IDs, dates or seed viability effects
have been extracted; no artificial observations or
numeric fitness estimates were generated.

Machine-readable exact file-access receipt:
`data/source_reconstructions/jadera2025_public_original_access_gate.csv`.

## IWE source-admission decision

The experiment-level claim *adult pollination vs nymph
seed predation* is **source-backed** at the paper and dataset
abstract level. It offers useful external biological contrast
for IWE's **time-lagged service and offspring cost** mechanism.
The strict-H1 admission checks currently fail:

1. No source-verified independently censused
   adult *Jadera* activity period paired with host flowering
   in the **same** original host/year/plot unit;
2. No recovered original per-unit date-linked
   final intact-seed fitness, after offspring
   seed predation, for the same native treatment/host
   used to estimate pollination;
3. Different **Cardiospermum** and **Koelreuteria**
   pollination experiments cannot be combined as
   the same host population, and nymph cost is an
   experimentally distinct outcome channel;
4. No source-native timing contrast SMD with valid
   biological replicate dependence can yet be extracted.

**Conclusion:** this independent mixed-system study
*adds a distinct positive service/cost ecological example*,
but **adds zero strict-H1 mixed independent clusters**.
Any future direct source read must first establish
actual adult-date, unit ID, host species and mature-seed
fields. Until then it remains an externally sourced,
non-promoting *mixed interaction case*, not a meta-analytic
effect or a claim that its benefit and cost cancel.
